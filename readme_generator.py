"""Generate README with dynamic GitHub stats."""

import json
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from xml.sax.saxutils import escape as xml_escape


def calculate_age(birth_date_str: str) -> str:
    """Calculate age from birth date string (DD.MM.YYYY format)."""
    try:
        birth_date = datetime.strptime(birth_date_str.strip(), "%d.%m.%Y")
        today = datetime.now()
        age = relativedelta(today, birth_date)
        return f"{age.years} years, {age.months} months, {age.days} days"
    except Exception as e:
        print(f"[ERROR] Could not parse birth date: {e}")
        return "N/A"


def format_line(label: str, value: str, width: int = 90, display_value: str = None) -> str:
    """Format label and value with dots, value right-aligned at end of line.

    If value is markdown (e.g. a link) whose rendered width differs from its
    raw length, pass the rendered text via display_value so dot-padding stays aligned.
    """
    label_with_colon = f"{label}:"
    visible_value = display_value if display_value is not None else value

    # Calculate dots to fill the space
    # Total width = label + dots + value (all aligned)
    available = width - len(label_with_colon) - len(visible_value)
    dots = "." * max(1, available)

    return f"{label_with_colon}{dots} {value}"


def _svg_row(y: int, label: str, value: str, canvas_width: int,
             dot_start: int = 185, char_width: float = 7.6, gap: int = 8) -> str:
    """Render one SVG row: label flush left, value flush right via text-anchor="end"
    (pixel-exact regardless of value length), with a dot leader stretched via
    textLength to fill the space in between.
    """
    right_edge = canvas_width - 2
    value_str = str(value)
    value_width_est = len(value_str) * char_width
    dot_end = max(dot_start, right_edge - value_width_est - gap)
    dot_span = max(0, dot_end - dot_start)
    n_dots = max(3, int(dot_span / 6))

    parts = [f'<text x="0" y="{y}" class="fg">{xml_escape(label)}:</text>']
    if dot_span > 4:
        dots = "." * n_dots
        parts.append(
            f'<text x="{dot_start}" y="{y}" textLength="{dot_span:.0f}" '
            f'lengthAdjust="spacingAndGlyphs" class="dots">{dots}</text>'
        )
    parts.append(f'<text x="{right_edge}" y="{y}" text-anchor="end" class="fg">{xml_escape(value_str)}</text>')
    return "\n".join(parts)


def build_stats_svg(header: str, info_rows: list, github_rows: list, canvas_width: int = 620) -> str:
    """Build the neofetch-style stats panel as an SVG.

    SVG text is positioned with exact coordinates (text-anchor="end" for values),
    so alignment to the right edge is exact regardless of font substitution or
    value length - unlike the HTML/character-counting approach, which GitHub's
    markdown sanitizer and inconsistent font rendering kept breaking.
    """
    row_h = 22
    y = 20
    lines = []

    def add_section_header(text: str):
        nonlocal y
        lines.append(f'<text x="0" y="{y}" class="strong">{xml_escape(text)}</text>')
        y += 8
        lines.append(f'<line x1="0" y1="{y}" x2="{canvas_width - 2}" y2="{y}" class="rule"/>')
        y += row_h

    def add_row(label: str, value: str):
        nonlocal y
        lines.append(_svg_row(y, label, value, canvas_width))
        y += row_h

    def add_gap():
        nonlocal y
        y += 14

    add_section_header(header)
    for label, value in info_rows:
        add_row(label, value)

    add_gap()
    add_section_header("GitHub Stats")
    for label, value in github_rows:
        add_row(label, value)

    height = y + 6

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_width} {height}" width="{canvas_width}" height="{height}">
<style>
text {{ font-family: 'Courier New', Consolas, monospace; font-size: 13px; }}
.fg {{ fill: #59636e; }}
.strong {{ fill: #1f2328; font-weight: bold; font-size: 14px; }}
.rule {{ stroke: #d1d9e0; stroke-width: 1; }}
.dots {{ fill: #59636e; opacity: 0.55; }}
@media (prefers-color-scheme: dark) {{
  .fg {{ fill: #9198a1; }}
  .strong {{ fill: #f0f6fc; }}
  .rule {{ stroke: #3d444d; }}
  .dots {{ fill: #9198a1; }}
}}
</style>
{chr(10).join(lines)}
</svg>
"""


def generate_readme(stats_file="stats.json", output_file="README.md", svg_file="stats.svg"):
    """
    Generate README with photo and stats side-by-side.

    Args:
        stats_file: Path to stats.json
        output_file: Path to output README.md
        svg_file: Path to the generated stats SVG (info panel + GitHub stats)
    """

    # Load environment variables
    load_dotenv()
    birth_date = os.getenv("BIRTH_DATE") or "25.12.2000"
    uptime = calculate_age(birth_date)

    # Load stats
    with open(stats_file, "r") as f:
        stats = json.load(f)

    login = stats.get("login") or "haroon"
    header = f"{login.lower()}@Abdul-Ali"
    rule = '<hr style="border: none; border-top: 1px solid var(--color-border-default); margin: 2px 0 6px 0;">'

    info_rows = [
        ("OS", os.getenv("INFO_OS") or "Windows 11, macOS, Linux"),
        ("Uptime", uptime),
        ("Host", os.getenv("INFO_HOST") or "C&A GmbH & Co. KG"),
        ("Kernel", os.getenv("INFO_KERNEL") or "Software Development Apprentice"),
        ("IDE", os.getenv("INFO_IDE") or "VSCode, IDEA, Cursor"),
        ("Languages.Programming", os.getenv("INFO_LANGUAGES_PROGRAMMING") or "Python, Java"),
        ("Languages.Real", os.getenv("INFO_LANGUAGES_REAL") or "German, English, Persian"),
        ("Hobbies.Technical", os.getenv("INFO_HOBBIES_TECHNICAL") or "LLM Fine-tuning, Software development"),
        ("Hobbies.Sports/Fitness", os.getenv("INFO_HOBBIES_SPORTS") or "Fitness, Jogging, Cycling, Swimming"),
    ]
    github_rows = [
        ("Repos", f'{stats["total_repos"]} | Stars {stats["total_stars"]} | Followers {stats["follower_count"]}'),
        ("Commits", f'{stats["total_commits"]:,}'),
        ("Lines of Code", f'{stats["total_additions"]:,} (+{stats["total_additions"]:,}, -{stats["total_deletions"]:,})'),
    ]

    # Write the stats panel as SVG (exact right-edge alignment, immune to GitHub's HTML sanitizer)
    svg_content = build_stats_svg(header, info_rows, github_rows)
    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(svg_content)

    # Build README content with theme-aware card
    readme_content = f"""# Haroon Abdul-Ali

<div style="border: 1px solid var(--color-border-default); border-radius: 12px; padding: 20px; background-color: var(--color-canvas-subtle);">
<table style="width: 100%; border: none;">
<tr>
<td width="35%" valign="bottom" style="padding-right: 20px; border: none;">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="dark.png">
  <img src="white.png" alt="Haroon Abdul-Ali" style="width: 100%; max-width: 250px; height: auto; border-radius: 8px;">
</picture>

</td>
<td width="65%" valign="top" style="border: none;">

<img src="{svg_file}" alt="{header} stats" style="width: 100%; display: block;">

<div style="font-family: 'Courier New', monospace; font-size: 12px; line-height: 1.3; color: var(--color-fg-muted); margin-top: 6px;">
<b>Contact</b>
{rule}
{format_line('Email.Personal', '<a href="mailto:haroon.aa.dev@gmail.com">haroon.aa.dev@gmail.com</a>', 100, display_value='haroon.aa.dev@gmail.com')}
<br>{format_line('LinkedIn', '<a href="https://www.linkedin.com/in/aa-haroon/">Haroon Abdul-Ali</a>', 116, display_value='Haroon Abdul-Ali')}
</div>

</td>
</tr>
</table>
</div>

---

## About

Software developer passionate about building elegant solutions at the intersection of web technologies, AI, and automation. Exploring the cutting edge of LLMs, network architecture, and creative coding.
<br>**Currently exploring:** GraphQL APIs • Modern Python • Machine Learning • Open Source Development • JavaScript • React
"""

    # Write README
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"[OK] README generated with SVG stats panel:")
    print(f"   Repos: {stats['total_repos']}")
    print(f"   Stars: {stats['total_stars']}")
    print(f"   Commits: {stats['total_commits']:,}")
    print(f"   Followers: {stats['follower_count']}")
    print(f"   Lines of Code: {stats['total_additions']:,}")


if __name__ == "__main__":
    generate_readme()
