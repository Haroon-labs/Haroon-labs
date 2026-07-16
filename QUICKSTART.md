# Quick Start Guide

## Setup (one-time)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env with your GitHub token
cp .env.example .env
# Edit .env and add your fine-grained PAT from https://github.com/settings/tokens?type=beta
```

## Generate Your Profile Card

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

## Embed in Your Profile README

In your GitHub profile's `README.md`:

```markdown
# Hi, I'm Your Name

<img src="profile.svg" width="900" alt="GitHub Profile Stats">

Check out my work...
```

Then commit `profile.svg` to your profile repo.

## GitHub Actions (Auto-Update)

The workflow runs daily, fetches fresh stats, regenerates `profile.svg`, and commits it back.

See `.github/workflows/stats.yml` for setup.

## Customization

### ASCII Art Width
```python
converter = ASCIIConverter(width=80)  # Default 70
```

### SVG Theme
```python
renderer = SVGRenderer(
    bg_color="#0d1117",      # Dark theme
    text_color="#c9d1d9"
)
```

### Stat Labels & Format
Edit the `stat_lines` list in `svg_renderer.py` to customize which stats are shown.
