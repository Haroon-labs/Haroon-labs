"""GitHub GraphQL API client with rate-limit aware queries."""

import requests
from typing import Dict, List, Optional
from github_queries import GitHubGraphQLQueries
from cache import StatsCache


class GitHubClient:
    """Client for GitHub GraphQL API v4."""

    def __init__(self, token: str, cache: Optional[StatsCache] = None):
        """
        Initialize GitHub client.

        Args:
            token: Fine-grained personal access token
            cache: Optional StatsCache instance
        """
        self.token = token
        self.api_url = "https://api.github.com/graphql"
        self.cache = cache or StatsCache()
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def _execute_query(self, query: str, variables: Dict) -> Dict:
        """Execute a GraphQL query and return response."""
        payload = {"query": query, "variables": variables}
        response = requests.post(
            self.api_url, json=payload, headers=self.headers, timeout=30
        )
        response.raise_for_status()
        data = response.json()

        if "errors" in data:
            raise RuntimeError(f"GraphQL error: {data['errors']}")

        return data.get("data", {})

    def get_user_profile_stats(self) -> Dict:
        """
        Fetch user profile stats: followers, total repos, total stars.

        Returns:
            {
                "login": str,
                "follower_count": int,
                "total_repos": int,
                "total_stars": int,
                "repositories": [
                    {
                        "name": str,
                        "owner": str,
                        "stars": int,
                        "total_commits": int
                    }
                ]
            }
        """
        all_repos = []
        after = None
        total_stars = 0

        while True:
            variables = GitHubGraphQLQueries.get_user_profile_variables(after=after)
            result = self._execute_query(
                GitHubGraphQLQueries.USER_PROFILE_QUERY, variables
            )

            viewer = result.get("viewer", {})
            repos = viewer.get("repositories", {})

            for repo in repos.get("nodes", []):
                if repo:
                    repo_data = {
                        "name": repo.get("name"),
                        "owner": repo.get("owner", {}).get("login"),
                        "stars": repo.get("stargazers", {}).get("totalCount", 0),
                        "total_commits": repo.get("defaultBranchRef", {})
                        .get("target", {})
                        .get("history", {})
                        .get("totalCount", 0),
                    }
                    all_repos.append(repo_data)
                    total_stars += repo_data["stars"]

            if not repos.get("pageInfo", {}).get("hasNextPage"):
                break
            after = repos.get("pageInfo", {}).get("endCursor")

        return {
            "login": viewer.get("login"),
            "follower_count": viewer.get("followers", {}).get("totalCount", 0),
            "total_repos": viewer.get("repositories", {}).get("totalCount", 0),
            "total_stars": total_stars,
            "repositories": all_repos,
        }

    def get_repo_commit_history(
        self, owner: str, repo: str, walk_history: bool = False
    ) -> Dict:
        """
        Fetch commit history for a repo.

        Args:
            owner: Repository owner
            repo: Repository name
            walk_history: If True, walk entire commit history. If False, use cached data.

        Returns:
            {
                "name": str,
                "owner": str,
                "total_commits": int,
                "total_additions": int,
                "total_deletions": int
            }
        """
        # Get total commit count first
        variables = GitHubGraphQLQueries.get_repo_summary_variables(owner, repo)
        result = self._execute_query(
            GitHubGraphQLQueries.REPO_SUMMARY_QUERY, variables
        )
        repo_data = result.get("repository", {})
        total_commits = (
            repo_data.get("defaultBranchRef", {})
            .get("target", {})
            .get("history", {})
            .get("totalCount", 0)
        )

        # Check cache to see if we need to re-walk commit history
        cached = self.cache.get_repo_stats(owner, repo)
        if cached and not walk_history:
            if not self.cache.has_commit_count_changed(owner, repo, total_commits):
                return {
                    "name": repo,
                    "owner": owner,
                    "total_commits": cached["commit_count"],
                    "total_additions": cached["additions"],
                    "total_deletions": cached["deletions"],
                }

        # Walk entire commit history
        total_additions = 0
        total_deletions = 0
        after = None

        while True:
            variables = GitHubGraphQLQueries.get_repo_commit_history_variables(
                owner, repo, after=after
            )
            result = self._execute_query(
                GitHubGraphQLQueries.REPO_COMMIT_HISTORY_QUERY, variables
            )
            repo_data = result.get("repository", {})
            commits = (
                repo_data.get("defaultBranchRef", {})
                .get("target", {})
                .get("history", {})
            )

            for commit in commits.get("nodes", []):
                if commit:
                    total_additions += commit.get("additions", 0)
                    total_deletions += commit.get("deletions", 0)

            if not commits.get("pageInfo", {}).get("hasNextPage"):
                break
            after = commits.get("pageInfo", {}).get("endCursor")

        # Cache the results
        self.cache.set_repo_stats(owner, repo, total_commits, total_additions, total_deletions)

        return {
            "name": repo,
            "owner": owner,
            "total_commits": total_commits,
            "total_additions": total_additions,
            "total_deletions": total_deletions,
        }

    def get_all_stats(self) -> Dict:
        """
        Fetch all profile statistics: followers, repos, stars, commits, LOC.

        Returns:
            {
                "login": str,
                "follower_count": int,
                "total_repos": int,
                "total_stars": int,
                "total_commits": int,
                "total_additions": int,
                "total_deletions": int,
                "repositories": [...]
            }
        """
        # Get user profile (has repo list and stars)
        profile = self.get_user_profile_stats()

        # Walk commit history for each repo (intelligently cached)
        total_commits = 0
        total_additions = 0
        total_deletions = 0

        for repo_info in profile["repositories"]:
            commit_data = self.get_repo_commit_history(repo_info["owner"], repo_info["name"])
            total_commits += commit_data["total_commits"]
            total_additions += commit_data["total_additions"]
            total_deletions += commit_data["total_deletions"]

        return {
            "login": profile["login"],
            "follower_count": profile["follower_count"],
            "total_repos": profile["total_repos"],
            "total_stars": profile["total_stars"],
            "total_commits": total_commits,
            "total_additions": total_additions,
            "total_deletions": total_deletions,
            "repositories": profile["repositories"],
        }
