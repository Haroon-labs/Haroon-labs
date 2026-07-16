# GitHub Profile Stats Generator

A Python tool that generates an auto-updating SVG dashboard of your GitHub statistics.

## Features

- **GraphQL v4 API**: Queries your GitHub profile for commits, repos, stars, followers
- **Smart Caching**: Only re-walks commit history for repos whose commit count changed
- **LOC Tracking**: Total lines added/deleted across all repos (owned + collaborator + org-member)
- **SVG Rendering**: Parses and updates an SVG template with your stats
- **ASCII Art**: Converts your profile photo into ASCII characters
- **GitHub Actions**: Runs on a cron schedule and auto-commits updated SVG back to repo

## Project Structure

```
├── github_queries.py    # GraphQL query templates
├── github_client.py     # API client + stat fetching logic
├── cache.py             # Local caching to minimize API calls
├── ascii_converter.py   # Image to ASCII art conversion
├── svg_renderer.py      # Renders stats into SVG template
├── main.py              # Entry point: fetches stats and renders SVG
├── .env.example         # Environment variable template
├── .github_workflows_stats.yml   # GitHub Actions workflow template
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
   [*] Fetching GitHub profile statistics...
   [OK] GitHub Profile Stats:
     Login: yourname
     Followers: 123
     Repos: 45
     Stars: 678
     Commits: 9012
     Lines Added: 345,678
     Lines Deleted: 123,456
     Net LOC: 222,222
   [STATS] Stats saved to stats.json
   ```

## Usage

### Option 1: Stats Only (no image)
```bash
python main.py
# Outputs: stats.json
```

### Option 2: Full Profile Card (stats + ASCII art from photo)
```bash
python main.py path/to/your/photo.jpg
# Outputs: stats.json, ascii_art.txt, profile.svg
```

### Option 3: Manual steps (if you want more control)

```bash
# Step 1: Fetch GitHub stats
python main.py

# Step 2: Convert image to ASCII
python -c "from ascii_converter import ASCIIConverter; ASCIIConverter(70).convert_to_file('photo.jpg')"

# Step 3: Render SVG
python -c "from svg_renderer import SVGRenderer; r = SVGRenderer(); r.render_from_files()"
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

## SVG Rendering

The SVG renderer:
- Loads ASCII art from `ascii_art.txt`
- Loads GitHub stats from `stats.json`
- Combines them side-by-side in a dark-themed SVG
- Auto-formats stats with dot-padding alignment
- Outputs to `profile.svg`

### Customization

**ASCII Art Width:**
```python
converter = ASCIIConverter(width=80)  # Default 70
```

**SVG Theme:**
```python
renderer = SVGRenderer(
    bg_color="#0d1117",      # Dark theme
    text_color="#c9d1d9"
)
```

## GitHub Actions (Auto-Update)

To auto-update your profile SVG daily:

### Step 1: Create workflow file

In your profile repo root, create:
```
.github/workflows/stats.yml
```

Copy the contents from `.github_workflows_stats.yml` in this project.

### Step 2: Update image path

In `.github/workflows/stats.yml`, change:
```yaml
run: python main.py path/to/your/photo.jpg
```

To your actual photo path. For example:
```yaml
run: python main.py "assets/profile-photo.jpg"
```

### Step 3: Commit workflow

```bash
git add .github/workflows/stats.yml
git commit -m "feat: add GitHub stats auto-update workflow"
git push
```

### Step 4: Test manually

Go to your repo → Actions tab → "Update GitHub Stats" → "Run workflow"

## How GitHub Actions works

Every day at midnight UTC (or on manual trigger):
1. Workflow checks out your repo
2. Installs Python + dependencies
3. Runs `python main.py <photo_path>`
4. Fetches fresh GitHub stats
5. Converts photo → ASCII art
6. Renders ASCII + stats → SVG
7. Commits `profile.svg` back to repo
8. Pushes changes

The SVG is now fresh with your latest stats!

## Rate Limiting

- Initial run (fresh cache): ~20-50 API points (depends on repo count)
- Subsequent runs (with cache): ~5-10 API points
- GitHub's limit: 5,000 points/hour

Safe to run hourly if needed.

## Troubleshooting

### GitHub Token Issues
- Token must be fine-grained (not classic)
- Scopes: `read:user`, `public_repo` (or `repo` for private)
- Check `.env` file has real token, not placeholder

### Image Conversion Fails
- Requires `numpy` and `imageio` libraries
- Install with: `pip install imageio-ffmpeg numpy`
- Supported formats: JPG, PNG, GIF, BMP

### Workflow not running
- Check `.github/workflows/stats.yml` exists (case-sensitive path)
- Check YAML syntax (use 2-space indents)
- Verify photo path is repo-relative

## Architecture

### `github_queries.py`
Defines GraphQL query templates:
- `USER_PROFILE_QUERY` — user info, repos, stars
- `REPO_COMMIT_HISTORY_QUERY` — paginated commit data
- `REPO_SUMMARY_QUERY` — total commits per repo

### `github_client.py`
Main API client:
- Authenticates with GitHub token
- Executes queries with pagination
- Intelligently caches results
- Aggregates stats across all repos

### `cache.py`
Caching layer:
- Stores per-repo stats with hashed keys
- Detects when commit counts change
- Skips unnecessary API calls

### `ascii_converter.py`
Image processing:
- Resizes image maintaining aspect ratio
- Converts to grayscale
- Maps pixel brightness to ASCII characters
- Outputs formatted ASCII art

### `svg_renderer.py`
SVG generation:
- Combines ASCII art + stats
- Formats with dot-padding alignment
- Uses GitHub dark theme colors
- Outputs self-contained SVG

## License

MIT

## Support

For issues, questions, or contributions, please open an issue on GitHub.
