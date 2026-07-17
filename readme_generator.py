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
<td width="65%" valign="top" style="font-family: 'Courier New', monospace; font-size: 12px; line-height: 1.3; color: var(--color-fg-muted);">
<b>{header}</b>
{rule}
{format_line('OS', 'Windows 11, macOS, Linux', 90)}
<br>{format_line('Uptime', uptime, 90)}
<br>{format_line('Host', 'C&A GmbH & Co. KG', 90)}
<br>{format_line('Kernel', 'Software Development Apprentice | Software Engineering', 90)}
<br>{format_line('IDE', 'VSCode, IDEA, Cursor', 90)}
<br>{format_line('Languages.Programming', 'Python, Java, (JavaScript)', 90)}
<br>{format_line('Languages.Real', 'German, English, Persian', 90)}
<br>{format_line('Hobbies.Technical', 'LLM Fine-tuning, Software development', 90)}
<br>{format_line('Hobbies.Sports/Fitness', 'Fitness, Jogging, Cycling, Swimming', 90)}
<br><br><b>Contact</b>
{rule}
{format_line('Email.Personal', '<a href="mailto:haroon.aa.dev@gmail.com">haroon.aa.dev@gmail.com</a>', 90, display_value='haroon.aa.dev@gmail.com')}
<br>{format_line('LinkedIn', '<a href="https://www.linkedin.com/in/aa-haroon/">Haroon Abdul-Ali</a>', 90, display_value='Haroon Abdul-Ali')}
<br><br><b>GitHub Stats</b>
{rule}
{format_line('Repos', f'{stats["total_repos"]} | Stars {stats["total_stars"]} | Followers {stats["follower_count"]}', 90)}
<br>{format_line('Commits', f'{stats["total_commits"]:,}', 90)}
<br>{format_line('Lines of Code', f'{stats["total_additions"]:,} (+{stats["total_additions"]:,}, -{stats["total_deletions"]:,})', 90)}
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
