# GitHub Profile Stats Generator

A Python tool that generates an auto-updating SVG dashboard of your GitHub statistics.

## Features

- **GraphQL v4 API**: Queries your GitHub profile for commits, repos, stars, followers
- **Smart Caching**: Only re-walks commit history for repos whose commit count changed
- **LOC Tracking**: Total lines added/deleted across all repos (owned + collaborator + org-member)
- **SVG Rendering**: Parses and updates an SVG template with your stats
- **GitHub Actions**: Runs on a cron schedule and auto-commits updated SVG back to repo

## Project Structure

```
├── github_queries.py    # GraphQL query templates
├── github_client.py     # API client + stat fetching logic
├── cache.py             # Local caching to minimize API calls
├── main.py              # Entry point: fetches stats and outputs JSON
├── svg_renderer.py      # (next) Renders stats into SVG template
├── .env.example         # Environment variable template
├── stats.json           # Output from main.py (intermediate)
└── .stats_cache.json    # Local cache of per-repo stats
```

## Setup

1. **Create a fine-grained personal access token:**
   - Go to https://github.com/settings/tokens?type=beta
   - Scopes needed: `read:user`, `public_repo` (or `repo` for private repos)
   - Copy token

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and paste your token
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the stats fetcher:**
   ```bash
   python main.py
   ```

   Output:
   ```
   ✅ GitHub Profile Stats:
     Login: yourname
     Followers: 123
     Repos: 45
     Stars: 678
     Commits: 9012
     Lines Added: 345,678
     Lines Deleted: 123,456
     Net LOC: 222,222
   📊 Stats saved to stats.json
   ```

## Caching Strategy

The cache (`.stats_cache.json`) stores per-repo data:
- **Repo name** (hashed): `sha256(owner/repo)[:12]`
- **Fields**: `owner`, `repo`, `commit_count`, `additions`, `deletions`, `last_updated`

When you run `main.py`:
1. Fetch total commit count for each repo (cheap query)
2. Check cache: if commit count unchanged, skip walking history
3. For new repos or changed repos: walk full commit history (paginated)
4. Update cache with new LOC deltas

This stays well within GitHub's 5,000 point/hour rate limit.

## Next Steps

### Phase 2: SVG Rendering

Create `svg_renderer.py` to:
- Load an SVG template with named `id` elements (e.g., `<text id="commits">0</text>`)
- Parse `stats.json` output from main.py
- Update text nodes with formatted numbers
- Auto-justify padding with dots (e.g., `Commits........1234`)
- Write updated SVG to disk

You'll design the SVG template separately; the renderer will accept a template path and output path.

### Phase 3: GitHub Actions Workflow

Create `.github/workflows/stats.yml` to:
- Run on cron schedule (e.g., daily at midnight)
- Set `GITHUB_TOKEN` secret
- Run `main.py` + `svg_renderer.py`
- Commit + push updated SVG back to repo
- Embed SVG in your profile README

## Rate Limiting

- Initial run (fresh cache): ~20-50 API points (depends on repo count)
- Subsequent runs (with cache): ~5-10 API points
- GitHub's limit: 5,000 points/hour

Safe to run hourly if needed.
