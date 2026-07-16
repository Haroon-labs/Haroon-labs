# GitHub Actions Setup

To auto-update your profile SVG daily:

## Step 1: Create workflow file

In your profile repo root, create:
```
.github/workflows/stats.yml
```

Copy the contents from `.github_workflows_stats.yml` in this project.

## Step 2: Update image path

In `.github/workflows/stats.yml`, change:
```yaml
run: python main.py path/to/your/photo.jpg
```

To your actual photo path. For example:
```yaml
run: python main.py "assets/profile-photo.jpg"
```

## Step 3: Commit workflow

```bash
git add .github/workflows/stats.yml
git commit -m "feat: add GitHub stats auto-update workflow"
git push
```

## Step 4: Test manually

Go to your repo → Actions tab → "Update GitHub Stats" → "Run workflow"

## How it works

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

## Troubleshooting

**Workflow not running:**
- Check workflow file is in `.github/workflows/` (not `.github_workflows_`)
- Check YAML syntax (use 2-space indents)

**Photo path error:**
- Use repo-relative paths: `"photo.jpg"` or `"assets/photo.jpg"`
- Ensure file exists in repo before first run

**Permission denied:**
- The workflow has default `GITHUB_TOKEN` with push permission
- If needed, create a fine-grained PAT and add as `secrets.GITHUB_TOKEN`

**Stats not updating:**
- Check workflow logs in Actions tab
- Verify `.env` → `GITHUB_TOKEN` is being used (or pass as secret)
