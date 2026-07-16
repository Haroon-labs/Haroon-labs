"""Generate README with dynamic GitHub stats."""

import json


def generate_readme(stats_file="stats.json", output_file="README.md"):
    """
    Generate README with photo and stats side-by-side.

    Args:
        stats_file: Path to stats.json
        output_file: Path to output README.md
    """

    # Load stats
    with open(stats_file, "r") as f:
        stats = json.load(f)

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
<td width="65%" valign="top" style="font-family: 'Courier New', monospace; font-size: 12px; line-height: 1.8; color: var(--color-fg-muted);">

OS.......................................... Windows 11, macOS Sequoia, Linux (Fedora)
<br>Uptime...................................... 21 years, 11 months, 15 days
<br>Host........................................ ThinkPad X1 Carbon • Arch Linux GmbH & Co. KG
<br>Kernel...................................... Software Development Apprentice | Prompt Engineer
<br>IDE......................................... VSCode, Cursor, Zsh, Neovim

<br>Languages.Programming...................... Python, JavaScript, TypeScript, Java
<br>Languages.Computer......................... SQL, HTML, CSS, JSON, Markdown
<br>Languages.Real............................. German, English, Arabic

<br>Hobbies.Technical.......................... LLM Fine-tuning, Network Security
<br>Hobbies.Creative........................... Analog Photography, Guitar

<br>Email.Personal............................. haroon.aa.dev@gmail.com
<br>LinkedIn................................... Haroon Abdul-Ali
<br>Discord.................................... haroon.aa

<br>Repos...................................... {stats['total_repos']} | Stars {stats['total_stars']} | Followers {stats['follower_count']}
<br>Commits.................................... {stats['total_commits']:,}
<br>Lines of Code.............................. {stats['total_additions']:,} (+{stats['total_additions']:,}, -{stats['total_deletions']:,})

</td>
</tr>
</table>
</div>

---

## About

Full-stack developer passionate about building elegant solutions at the intersection of web technologies, AI, and automation. Exploring the cutting edge of LLMs, network architecture, and creative coding.

**Currently exploring:** GraphQL APIs • Modern Python • Machine Learning • Open Source Development

---

## Let's Connect

Reach out on [LinkedIn](https://linkedin.com/in/HaroonAbdul-Ali) or email for collaborations, questions, or just to chat about tech.
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
