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

    # Calculate net LOC
    net_loc = stats["total_additions"] - stats["total_deletions"]

    # Build README content
    readme_content = f"""# Haroon Abdul-Ali

<table>
<tr>
<td width="40%">

![Haroon Abdul-Ali](profile.png)

</td>
<td width="60%">

<pre style="color: #c9d1d9; background: transparent; font-family: 'Courier New', monospace; line-height: 1.6;">
<span style="color: #58a6ff;">haroon@abdul-ali</span>

<span style="color: #ffa657;">OS:</span>............................ Windows 11, macOS Sequoia, Linux (Fedora)
<span style="color: #ffa657;">Uptime:</span>........................ 21 years, 11 months, 15 days
<span style="color: #ffa657;">Host:</span>.......................... ThinkPad X1 Carbon • Arch Linux GmbH & Co. KG
<span style="color: #ffa657;">Kernel:</span>........................ Software Development Apprentice | Prompt Engineer
<span style="color: #ffa657;">IDE:</span>........................... VSCode, Cursor, Zsh, Neovim

<span style="color: #ffa657;">Languages.Programming:</span>....... Python, JavaScript, TypeScript, Java
<span style="color: #ffa657;">Languages.Computer:</span>.......... SQL, HTML, CSS, JSON, Markdown
<span style="color: #ffa657;">Languages.Real:</span>.............. German, English, Arabic

<span style="color: #ffa657;">Hobbies.Technical:</span>........... LLM Fine-tuning, Network Security
<span style="color: #ffa657;">Hobbies.Creative:</span>............ Analog Photography, Guitar

<span style="color: #ffa657;">Contact</span>
<span style="color: #ffa657;">Email.Personal:</span>.............. <span style="color: #58a6ff;">haroon.aa.dev@gmail.com</span>
<span style="color: #ffa657;">LinkedIn:</span>..................... <span style="color: #58a6ff;">Haroon Abdul-Ali</span>
<span style="color: #ffa657;">Discord:</span>....................... <span style="color: #58a6ff;">haroon.aa</span>

<span style="color: #ffa657;">GitHub Stats</span>
<span style="color: #ffa657;">Repos:</span>........................ <span style="color: #58a6ff;">{stats['total_repos']}</span> | <span style="color: #ffa657;">Stars:</span> <span style="color: #58a6ff;">{stats['total_stars']}</span> | <span style="color: #ffa657;">Followers:</span> <span style="color: #58a6ff;">{stats['follower_count']}</span>
<span style="color: #ffa657;">Commits:</span>....................... <span style="color: #58a6ff;">{stats['total_commits']:,}</span>
<span style="color: #ffa657;">Lines of Code on GitHub:</span>.... <span style="color: #58a6ff;">{stats['total_additions']:,}</span> (+<span style="color: #79c0ff;">{stats['total_additions']:,}</span>, -<span style="color: #f85149;">{stats['total_deletions']:,}</span>)
</pre>

</td>
</tr>
</table>

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

    print(f"[OK] README generated with stats:")
    print(f"   Repos: {stats['total_repos']}")
    print(f"   Stars: {stats['total_stars']}")
    print(f"   Commits: {stats['total_commits']:,}")
    print(f"   Followers: {stats['follower_count']}")
    print(f"   Lines of Code: {stats['total_additions']:,}")


if __name__ == "__main__":
    generate_readme()
