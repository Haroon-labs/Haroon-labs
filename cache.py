"""Cache management for GitHub stats to minimize API calls."""

import json
import hashlib
from pathlib import Path
from typing import Dict, Optional


class StatsCache:
    """Manages local caching of per-repo stats (commit counts, LOC deltas)."""

    def __init__(self, cache_file: str = ".stats_cache.json"):
        self.cache_file = Path(cache_file)
        self.data: Dict = self._load_cache()

    def _load_cache(self) -> Dict:
        """Load cache from disk, return empty dict if file doesn't exist."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_cache(self) -> None:
        """Persist cache to disk."""
        with open(self.cache_file, "w") as f:
            json.dump(self.data, f, indent=2)

    def _hash_repo_key(self, owner: str, repo: str) -> str:
        """Generate a hashed key for repo (owner/repo)."""
        repo_id = f"{owner}/{repo}"
        return hashlib.sha256(repo_id.encode()).hexdigest()[:12]

    def get_repo_stats(self, owner: str, repo: str) -> Optional[Dict]:
        """
        Retrieve cached stats for a repo.
        Returns: {"commit_count": int, "additions": int, "deletions": int, "last_updated": str}
        """
        key = self._hash_repo_key(owner, repo)
        return self.data.get(key)

    def set_repo_stats(
        self, owner: str, repo: str, commit_count: int, additions: int, deletions: int
    ) -> None:
        """
        Store stats for a repo in cache.

        Args:
            owner: Repository owner login
            repo: Repository name
            commit_count: Total commits in repo
            additions: Total lines added
            deletions: Total lines deleted
        """
        key = self._hash_repo_key(owner, repo)
        self.data[key] = {
            "owner": owner,
            "repo": repo,
            "commit_count": commit_count,
            "additions": additions,
            "deletions": deletions,
            "last_updated": str(Path.cwd()),  # TODO: Replace with actual timestamp
        }
        self._save_cache()

    def has_commit_count_changed(self, owner: str, repo: str, current_count: int) -> bool:
        """
        Check if commit count has changed since last cache.
        Returns True if repo is new or count changed (repo needs re-walk).
        """
        cached = self.get_repo_stats(owner, repo)
        if cached is None:
            return True  # New repo
        return cached["commit_count"] != current_count

    def clear_cache(self) -> None:
        """Clear all cached data."""
        self.data = {}
        self._save_cache()

    def get_all_repos(self) -> Dict[str, Dict]:
        """Return all cached repos."""
        return self.data
