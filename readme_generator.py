"""Generate README with dynamic GitHub stats."""

import json


def generate_readme(stats_file="stats.json", output_file="README.md"):
    """
    Generate README with dynamic stats from stats.json.

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

<div style="font-family: 'Courier New', monospace; font-size: 13px; line-height: 1.6; margin-bottom: 20px;">

<div style="color: var(--color-accent-fg); font-size: 14px; font-weight: 600; margin-bottom: 12px;">haroon@abdul-ali</div>

<div style="color: var(--color-fg-muted);">
<span style="color: var(--color-accent-fg);">OS:</span> Windows 11, macOS Sequoia, Linux (Fedora)
<br><span style="color: var(--color-accent-fg);">Uptime:</span> 21 years, 11 months, 15 days
<br><span style="color: var(--color-accent-fg);">Host:</span> ThinkPad X1 Carbon • Arch Linux GmbH & Co. KG
<br><span style="color: var(--color-accent-fg);">Kernel:</span> Software Development Apprentice | Prompt Engineer
<br><span style="color: var(--color-accent-fg);">IDE:</span> VSCode, Cursor, Zsh, Neovim
</div>

<div style="margin-top: 12px; color: var(--color-fg-muted);">
<span style="color: var(--color-accent-fg);">Languages.Programming:</span> Python, JavaScript, TypeScript, Java
<br><span style="color: var(--color-accent-fg);">Languages.Computer:</span> SQL, HTML, CSS, JSON, Markdown
<br><span style="color: var(--color-accent-fg);">Languages.Real:</span> German, English, Arabic
</div>

<div style="margin-top: 12px; color: var(--color-fg-muted);">
<span style="color: var(--color-accent-fg);">Hobbies.Technical:</span> LLM Fine-tuning, Network Security
<br><span style="color: var(--color-accent-fg);">Hobbies.Creative:</span> Analog Photography, Guitar
</div>

<div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--color-border-default); color: var(--color-fg-muted);">
<div style="color: var(--color-fg-default); font-weight: 500; margin-bottom: 8px;">Contact</div>
<span style="color: var(--color-accent-fg);">Email.Personal:</span> <span style="color: var(--color-accent-fg);">haroon.aa.dev@gmail.com</span>
<br><span style="color: var(--color-accent-fg);">LinkedIn:</span> Haroon Abdul-Ali
<br><span style="color: var(--color-accent-fg);">Discord:</span> haroon.aa
</div>

<div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--color-border-default); color: var(--color-fg-muted);">
<div style="color: var(--color-fg-default); font-weight: 500; margin-bottom: 8px;">GitHub Stats</div>
<span style="color: var(--color-accent-fg);">Repos:</span> {stats['total_repos']} | <span style="color: var(--color-accent-fg);">Stars:</span> {stats['total_stars']} | <span style="color: var(--color-accent-fg);">Followers:</span> {stats['follower_count']}
<br><span style="color: var(--color-accent-fg);">Commits:</span> {stats['total_commits']:,}
<br><span style="color: var(--color-accent-fg);">Lines of Code on GitHub:</span> {stats['total_additions']:,} (+{stats['total_additions']:,}, -{stats['total_deletions']:,})
</div>

</div>

<div style="text-align: center; margin-top: 20px;">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="dark.png">
  <img src="white.png" alt="Haroon Abdul-Ali" style="max-width: 100%; height: auto; border-radius: 8px;">
</picture>

</div>

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
