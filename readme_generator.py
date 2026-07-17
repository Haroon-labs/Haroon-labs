"""Generate README with dynamic GitHub stats."""

import json
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv


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


def toc_row(label: str, value: str) -> str:
    """Render a table-of-contents-style row: label flush left, dot leader
    filling the middle, value flush right at the edge of the column.

    Uses a table cell with a long dot string clipped by overflow:hidden
    instead of counting characters, so the leader always reaches the true
    right edge regardless of font, zoom, or embedded HTML (links, etc.).
    """
    return (
        "<tr>"
        f'<td style="white-space: nowrap; overflow: hidden; width: 100%; padding: 0;">{label}:{"." * 250}</td>'
        f'<td style="white-space: nowrap; text-align: right; padding: 0 0 0 6px;">{value}</td>'
        "</tr>"
    )


def generate_readme(stats_file="stats.json", output_file="README.md"):
    """
    Generate README with photo and stats side-by-side.

    Args:
        stats_file: Path to stats.json
        output_file: Path to output README.md
    """

    # Load environment variables
    load_dotenv()
    birth_date = os.getenv("BIRTH_DATE", "25.12.2000")
    uptime = calculate_age(birth_date)

    # Load stats
    with open(stats_file, "r") as f:
        stats = json.load(f)

    login = stats.get("login") or "haroon"
    header = f"{login.lower()}@Abdul-Ali"
    rule = '<hr style="border: none; border-top: 1px solid var(--color-border-default); margin: 2px 0 6px 0;">'

    # Build README content with theme-aware card
    readme_content = f"""# Haroon Abdul-Ali

<div style="border: 1px solid var(--color-border-default); border-radius: 12px; padding: 20px; background-color: var(--color-canvas-subtle);">
<table style="width: 100%;">
<tr>
<td width="35%" valign="bottom" style="padding-right: 20px;">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="dark.png">
  <img src="white.png" alt="Haroon Abdul-Ali" style="width: 100%; max-width: 250px; height: auto; border-radius: 8px;">
</picture>

</td>
<td width="65%" valign="top" style="padding: 0;">
<table style="width: 100%; border-collapse: collapse; font-family: 'Courier New', monospace; font-size: 12px; line-height: 1.3; color: var(--color-fg-muted);">
<tr><td colspan="2"><b>{header}</b></td></tr>
<tr><td colspan="2">{rule}</td></tr>
{toc_row('OS', 'Windows 11, macOS, Linux')}
{toc_row('Uptime', uptime)}
{toc_row('Host', 'C&A GmbH & Co. KG')}
{toc_row('Kernel', 'Software Development Apprentice | Software Engineering')}
{toc_row('IDE', 'VSCode, IDEA, Cursor')}
{toc_row('Languages.Programming', 'Python, Java, (JavaScript)')}
{toc_row('Languages.Real', 'German, English, Persian')}
{toc_row('Hobbies.Technical', 'LLM Fine-tuning, Software development')}
{toc_row('Hobbies.Sports/Fitness', 'Fitness, Jogging, Cycling, Swimming')}
<tr><td colspan="2"><br><b>Contact</b></td></tr>
<tr><td colspan="2">{rule}</td></tr>
{toc_row('Email.Personal', '<a href="mailto:haroon.aa.dev@gmail.com">haroon.aa.dev@gmail.com</a>')}
{toc_row('LinkedIn', '<a href="https://www.linkedin.com/in/aa-haroon/">Haroon Abdul-Ali</a>')}
<tr><td colspan="2"><br><b>GitHub Stats</b></td></tr>
<tr><td colspan="2">{rule}</td></tr>
{toc_row('Repos', f'{stats["total_repos"]} | Stars {stats["total_stars"]} | Followers {stats["follower_count"]}')}
{toc_row('Commits', f'{stats["total_commits"]:,}')}
{toc_row('Lines of Code', f'{stats["total_additions"]:,} (+{stats["total_additions"]:,}, -{stats["total_deletions"]:,})')}
</table>
</td>
</tr>
</table>
</div>

---

## About

Full-stack developer passionate about building elegant solutions at the intersection of web technologies, AI, and automation. Exploring the cutting edge of LLMs, network architecture, and creative coding.
<br>**Currently exploring:** GraphQL APIs • Modern Python • Machine Learning • Open Source Development
"""

    # Write README
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"[OK] README generated with theme-aware card:")
    print(f"   Repos: {stats['total_repos']}")
    print(f"   Stars: {stats['total_stars']}")
    print(f"   Commits: {stats['total_commits']:,}")
    print(f"   Followers: {stats['follower_count']}")
    print(f"   Lines of Code: {stats['total_additions']:,}")


if __name__ == "__main__":
    generate_readme()
