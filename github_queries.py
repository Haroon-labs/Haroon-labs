"""GitHub GraphQL v4 API queries for profile statistics."""


class GitHubGraphQLQueries:
    """GraphQL query templates for fetching GitHub profile data."""

    # User profile info: repos, stars, followers, commits
    USER_PROFILE_QUERY = """
    query($first: Int!, $after: String) {
      viewer {
        login
        followers {
          totalCount
        }
        repositories(first: $first, after: $after, affiliations: [OWNER, COLLABORATOR, ORGANIZATION_MEMBER]) {
          totalCount
          pageInfo {
            hasNextPage
            endCursor
          }
          nodes {
            id
            name
            owner {
              login
            }
            stargazers {
              totalCount
            }
            defaultBranchRef {
              target {
                ... on Commit {
                  history(first: 1) {
                    totalCount
                  }
                }
              }
            }
          }
        }
      }
    }
    """

    # Fetch commit history for a specific repo (paginated)
    REPO_COMMIT_HISTORY_QUERY = """
    query($owner: String!, $name: String!, $first: Int!, $after: String) {
      repository(owner: $owner, name: $name) {
        id
        defaultBranchRef {
          target {
            ... on Commit {
              history(first: $first, after: $after) {
                totalCount
                pageInfo {
                  hasNextPage
                  endCursor
                }
                nodes {
                  oid
                  additions
                  deletions
                  committedDate
                }
              }
            }
          }
        }
      }
    }
    """

    # Get repo summary: total commits, total LOC changes
    REPO_SUMMARY_QUERY = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        id
        name
        defaultBranchRef {
          target {
            ... on Commit {
              history(first: 1) {
                totalCount
              }
            }
          }
        }
      }
    }
    """

    @staticmethod
    def get_user_profile_variables(first: int = 100, after: str = None) -> dict:
        """Variables for user profile query."""
        return {"first": first, "after": after}

    @staticmethod
    def get_repo_commit_history_variables(
        owner: str, name: str, first: int = 100, after: str = None
    ) -> dict:
        """Variables for repo commit history query."""
        return {"owner": owner, "name": name, "first": first, "after": after}

    @staticmethod
    def get_repo_summary_variables(owner: str, name: str) -> dict:
        """Variables for repo summary query."""
        return {"owner": owner, "name": name}
