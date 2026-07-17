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

Fill in `.env`:

```
PAT_TOKEN=<your-token>
BIRTH_DATE=YOUR_BIRTH_DATE
```

`.env` is gitignored and will **never** be committed.

### Customizing the info panel

Everything shown in the info panel (OS, host, kernel, IDE, languages, hobbies) comes from environment variables, each with a sensible default — so a fresh clone works out of the box, and you only need to override what you want to change:

```
INFO_OS=Windows 11, macOS, Linux
INFO_HOST=Your Company GmbH
INFO_KERNEL=Your Job Title
INFO_IDE=VSCode, IDEA, Cursor
INFO_LANGUAGES_PROGRAMMING=Python, Java
INFO_LANGUAGES_REAL=German, English
INFO_HOBBIES_TECHNICAL=LLM Fine-tuning, Software development
INFO_HOBBIES_SPORTS=Fitness, Jogging, Cycling, Swimming
```

See `.env.example` for the full list. If you fork this repo for yourself, set these in `.env` (local) and as repository **variables** (Settings → Secrets and variables → Actions → Variables tab — not Secrets, since this isn't sensitive data) so the automated workflow picks them up too, instead of editing `readme_generator.py`.

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

The action uses the repository secret `PAT_TOKEN` (Settings → Secrets and variables → Actions) and automatically commits `README.md` if anything changed.

## Where to make changes

| Goal | File |
|---|---|
| Layout/text of the profile card (OS, host, languages, hobbies, dot alignment) | [readme_generator.py](readme_generator.py) |
| GraphQL queries to the GitHub API | [github_queries.py](github_queries.py) |
| API client / rate-limit handling | [github_client.py](github_client.py) |
| Local cache for commit history | [cache.py](cache.py) |

**Don't edit directly:** `README.md` and `stats.json` are generated files — changes to them get overwritten on the next run. Always change `readme_generator.py` and regenerate.

## Known pitfalls

- If you test `readme_generator.py` locally and then commit, make sure `stats.json` is current (`python main.py` instead of just `readme_generator.py`) — otherwise stale numbers end up in the commit, which the action then overwrites shortly after.
- The action runs automatically after a push; a `git pull` before your next commit avoids merge conflicts in `README.md`.
