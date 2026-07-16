"""Main entry point for GitHub profile stats generator."""

import os
import json
import sys
from dotenv import load_dotenv
from github_client import GitHubClient
from cache import StatsCache
from ascii_converter import ASCIIConverter
from svg_renderer import SVGRenderer


def main(image_path: str = None, generate_svg: bool = True):
    """
    Fetch GitHub stats and optionally generate profile SVG.

    Args:
        image_path: Path to profile image (for ASCII conversion)
        generate_svg: Whether to render SVG after fetching stats
    """
    load_dotenv()

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not set")

    print("[*] Fetching GitHub profile statistics...")

    cache = StatsCache(".stats_cache.json")
    client = GitHubClient(token, cache)

    # Get all stats
    stats = client.get_all_stats()

    # Pretty print results
    print("\n[OK] GitHub Profile Stats:")
    print(f"  Login: {stats['login']}")
    print(f"  Followers: {stats['follower_count']}")
    print(f"  Repos: {stats['total_repos']}")
    print(f"  Stars: {stats['total_stars']}")
    print(f"  Commits: {stats['total_commits']}")
    print(f"  Lines Added: {stats['total_additions']:,}")
    print(f"  Lines Deleted: {stats['total_deletions']:,}")
    print(f"  Net LOC: {stats['total_additions'] - stats['total_deletions']:,}")

    # Save stats to JSON
    with open("stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    print("\n[STATS] Stats saved to stats.json")

    # Convert image to ASCII art if provided
    if image_path and os.path.exists(image_path):
        print(f"\n[ART] Converting image to ASCII art...")
        converter = ASCIIConverter(width=70)
        ascii_art = converter.convert_to_file(image_path, "ascii_art.txt")
        print(f"   ({len(ascii_art.split(chr(10)))} lines, 70 chars wide)")
    else:
        ascii_art = None

    # Generate SVG if image was converted
    if generate_svg and ascii_art:
        print("\n[SVG] Rendering SVG profile card...")
        renderer = SVGRenderer()
        renderer.render(stats, ascii_art, output_path="profile.svg")
        print("   [OK] Ready to embed in README!")

    return stats


if __name__ == "__main__":
    # Check if image path provided as argument
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    main(image_path=image_path)
