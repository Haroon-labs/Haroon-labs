# Quickstart

This repo automatically generates the README card for [github.com/Haroon-labs](https://github.com/Haroon-labs) — including live stats (repos, stars, commits, lines of code) and a neofetch-style info panel.

## Prerequisites

- Python 3.11+
- A GitHub **fine-grained Personal Access Token** with the `read:user` and `public_repo` permissions (or `repo`, if private repos should be counted too)
  → create one at https://github.com/settings/tokens?type=beta

## Setup

```bash
git clone https://github.com/Haroon-labs/HaroonAbdul-Ali.git
cd HaroonAbdul-Ali
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env` — this is the only file with a secret in it:

```
PAT_TOKEN=<your-token>
```

## Customizing the profile

Everything else — name, contact info, photos, and the neofetch info panel — lives in **`profile.env`**, committed to the repo (none of it is sensitive; it's the same data the rendered README already shows publicly):

```
BIRTH_DATE=25.12.2000

FULL_NAME=Your Name
CONTACT_EMAIL=you@example.com
LINKEDIN_URL=https://www.linkedin.com/in/your-profile/
PHOTO_LIGHT=white.png
PHOTO_DARK=dark.png
NEOFETCH_HOST=profile

INFO_OS=Windows 11, macOS, Linux
INFO_HOST=Your Company GmbH
INFO_KERNEL=Your Job Title
INFO_IDE=VSCode, IDEA, Cursor
INFO_LANGUAGES_PROGRAMMING=Python, Java
INFO_LANGUAGES_REAL=German, English
INFO_HOBBIES_TECHNICAL=LLM Fine-tuning, Software development
INFO_HOBBIES_SPORTS=Fitness, Jogging, Cycling, Swimming
```

If you fork this repo for yourself, just edit the values in `profile.env` directly and commit — no GitHub repository variables to configure, since both local runs and the GitHub Actions workflow read this same file straight out of the checked-out repo. `PHOTO_LIGHT`/`PHOTO_DARK` are filenames relative to the repo root; drop your own images in and point these at them. `NEOFETCH_HOST` is just the "host" half of the `login@host` header in the stats panel (cosmetic).

## Running locally

```bash
python main.py
```

This fetches real live data from the GitHub API, writes it to `stats.json`, and regenerates `README.md`.

**To test layout/text only, without real API calls:** `python readme_generator.py` re-reads the last saved `stats.json` (no new API call). Handy for quick previews of formatting changes.

## Automation

`.github/workflows/stats.yml` runs:
- on every push to `main`
- daily at midnight UTC (cron)
- manually via "Run workflow" in the Actions tab

The action uses the repository secret `PAT_TOKEN` (Settings → Secrets and variables → Actions → Secrets tab — the only thing that needs configuring in GitHub) and automatically commits `README.md` if anything changed. Everything in `profile.env` is picked up automatically since it's already checked out with the rest of the repo.

## Where to make changes

| Goal | File |
|---|---|
| Name, contact info, photos, info panel content | [profile.env](profile.env) |
| Layout/markup of the profile card | [readme_generator.py](readme_generator.py) |
| GraphQL queries to the GitHub API | [github_queries.py](github_queries.py) |
| API client / rate-limit handling | [github_client.py](github_client.py) |
| Local cache for commit history | [cache.py](cache.py) |

**Don't edit directly:** `README.md` and `stats.json` are generated files — changes to them get overwritten on the next run. Change `profile.env` (content) or `readme_generator.py` (layout) and regenerate.

## Known pitfalls

- If you test `readme_generator.py` locally and then commit, make sure `stats.json` is current (`python main.py` instead of just `readme_generator.py`) — otherwise stale numbers end up in the commit, which the action then overwrites shortly after.
- The action runs automatically after a push; a `git pull` before your next commit avoids merge conflicts in `README.md`.
- **Adding a new env var to `readme_generator.py`?** If it's non-sensitive, add it to `profile.env` (and `.env.example`'s comment, if worth documenting) — it just works locally and in CI with no further setup. Only genuinely sensitive values (tokens, keys) belong in `.env`/the repository Secrets tab instead.
