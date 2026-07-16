"""Render GitHub profile with ASCII art + info side-by-side."""

import json


def render_profile(ascii_file="ascii_art.txt", stats_file="stats.json", output_file="profile_text.md"):
    """
    Render ASCII art + profile info side-by-side.

    Args:
        ascii_file: Path to ASCII art file
        stats_file: Path to stats JSON file
        output_file: Output markdown file
    """

    # Load ASCII art
    with open(ascii_file, "r") as f:
        ascii_lines = f.read().strip().split("\n")

    # Load stats
    with open(stats_file, "r") as f:
        stats = json.load(f)

    # Profile info lines
    info_lines = [
        f"Haroon Abdul-Ali",
        f"",
        f"OS:............................. Windows 11, Linux",
        f"Uptime:......................... Always Learning",
        f"Host:........................... Digital Future Lab",
        f"Kernel:......................... Growth-Oriented",
        f"IDEs:........................... VS Code, Neovim",
        f"",
        f"Languages.Programming:.......... Python, JavaScript, TypeScript",
        f"Languages.Computer:............ HTML, CSS, SQL, Markdown",
        f"Languages.Real:................ English, German",
        f"",
        f"Hobbies.Software:.............. Web Dev, AI/ML, Open Source",
        f"Hobbies.Hardware:.............. Tech, Automation, IoT",
        f"",
        f"Contact",
        f"Email.Personal:................ haroonabdulali.w@gmail.com",
        f"LinkedIn:...................... HaroonAbdul-Ali",
        f"Discord:........................ [your handle]",
        f"",
        f"GitHub Stats",
        f"Repos: {stats['total_repos']} | Stars: {stats['total_stars']} | Commits: {stats['total_commits']:,}",
    ]

    # Combine ASCII art (left) with info (right)
    ascii_width = 70
    spacing = 2

    output = []
    max_lines = max(len(ascii_lines), len(info_lines))

    for i in range(max_lines):
        ascii_part = ascii_lines[i] if i < len(ascii_lines) else " " * ascii_width
        # Ensure ascii_part is exactly ascii_width chars
        ascii_part = ascii_part.ljust(ascii_width)

        info_part = info_lines[i] if i < len(info_lines) else ""

        line = ascii_part + (" " * spacing) + info_part
        output.append(line)

    # Write to file
    result = "\n".join(output)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"[OK] Profile rendered to {output_file}")
    return result


if __name__ == "__main__":
    render_profile()
