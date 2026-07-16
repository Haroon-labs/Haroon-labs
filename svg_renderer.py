"""Render GitHub stats + ASCII art into an SVG profile card."""

import json
from pathlib import Path
from typing import Dict, List


class SVGRenderer:
    """Renders GitHub stats and ASCII art into an SVG profile card."""

    def __init__(self, bg_color: str = "#0d1117", text_color: str = "#c9d1d9"):
        """
        Initialize renderer.

        Args:
            bg_color: SVG background color (GitHub dark theme)
            text_color: Text color
        """
        self.bg_color = bg_color
        self.text_color = text_color
        self.font_family = "Courier New, monospace"
        self.font_size = 11
        self.line_height = 14

    def _escape_svg_text(self, text: str) -> str:
        """Escape special XML characters."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
        )

    def _create_ascii_block(
        self, ascii_art: str, x_offset: int = 20
    ) -> tuple[str, int]:
        """
        Create SVG text element for ASCII art.

        Args:
            ascii_art: ASCII art string (newline-separated)
            x_offset: X position of ASCII block

        Returns:
            (SVG text element, width in pixels)
        """
        lines = ascii_art.strip().split("\n")
        max_width = max(len(line) for line in lines) if lines else 0

        svg_lines = []
        for i, line in enumerate(lines):
            y = 50 + (i * self.line_height)
            escaped_line = self._escape_svg_text(line)
            svg_lines.append(
                f'  <text x="{x_offset}" y="{y}" font-family="{self.font_family}" '
                f'font-size="{self.font_size}" fill="{self.text_color}" '
                f'xml:space="preserve">{escaped_line}</text>'
            )

        width = max_width * 6.6  # ~6.6px per char in monospace

        return "\n".join(svg_lines), int(width)

    def _format_stat(self, label: str, value: str, max_label_width: int = 20) -> str:
        """
        Format a stat line with dot-padding alignment.

        Args:
            label: Stat label (e.g., "Commits")
            value: Stat value (e.g., "2,116")
            max_label_width: Width to pad label to

        Returns:
            Formatted string with dots (e.g., "Commits........2,116")
        """
        dots_count = max_label_width - len(label)
        dots = "." * dots_count
        return f"{label}{dots}{value}"

    def _create_stats_block(
        self, stats: Dict, x_offset: int = 20
    ) -> str:
        """
        Create SVG text elements for GitHub stats.

        Args:
            stats: Stats dict from main.py
            x_offset: X position of stats block

        Returns:
            SVG text elements
        """
        # Format stats with nice alignment
        stat_lines = [
            ("User", stats.get("login", "N/A")),
            ("Followers", f"{stats.get('follower_count', 0):,}"),
            ("Repositories", f"{stats.get('total_repos', 0)}"),
            ("Stars Received", f"{stats.get('total_stars', 0):,}"),
            ("", ""),  # Spacer
            ("Commits", f"{stats.get('total_commits', 0):,}"),
            ("Lines Added", f"+{stats.get('total_additions', 0):,}"),
            ("Lines Deleted", f"-{stats.get('total_deletions', 0):,}"),
            ("Net LOC", f"{stats.get('total_additions', 0) - stats.get('total_deletions', 0):,}"),
        ]

        svg_lines = []
        for i, (label, value) in enumerate(stat_lines):
            y = 50 + (i * self.line_height)
            if label:  # Skip spacer lines
                formatted = self._format_stat(label, value)
                escaped = self._escape_svg_text(formatted)
                svg_lines.append(
                    f'  <text x="{x_offset}" y="{y}" font-family="{self.font_family}" '
                    f'font-size="{self.font_size}" fill="{self.text_color}">{escaped}</text>'
                )
            else:
                # Spacer line (empty text)
                svg_lines.append(
                    f'  <text x="{x_offset}" y="{y}" font-family="{self.font_family}" '
                    f'font-size="{self.font_size}" fill="{self.text_color}"> </text>'
                )

        return "\n".join(svg_lines)

    def render(
        self,
        stats: Dict,
        ascii_art: str,
        output_path: str = "profile.svg",
    ) -> None:
        """
        Render GitHub stats + ASCII art into SVG.

        Args:
            stats: Stats dict from main.py
            ascii_art: ASCII art string (newline-separated)
            output_path: Path to output SVG file
        """
        # Generate ASCII block
        ascii_svg, ascii_width = self._create_ascii_block(ascii_art, x_offset=20)

        # Generate stats block (positioned to the right of ASCII)
        stats_x = 20 + ascii_width + 40  # 40px padding between blocks
        stats_svg = self._create_stats_block(stats, x_offset=int(stats_x))

        # Calculate SVG dimensions
        ascii_lines = ascii_art.strip().split("\n")
        svg_height = max(
            50 + (len(ascii_lines) * self.line_height),
            50 + (9 * self.line_height),  # Stats height
        )
        svg_width = int(stats_x) + 300  # 300px for stats block

        # Build SVG
        svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{svg_width}" height="{int(svg_height)}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      text {{ white-space: pre; }}
    </style>
  </defs>
  <!-- Background -->
  <rect width="{svg_width}" height="{int(svg_height)}" fill="{self.bg_color}"/>

  <!-- ASCII Art (Left) -->
{ascii_svg}

  <!-- Stats (Right) -->
{stats_svg}
</svg>
"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg_content)

        print(f"[OK] SVG rendered to {output_path} ({svg_width}x{int(svg_height)}px)")

    def render_from_files(
        self,
        stats_json: str = "stats.json",
        ascii_txt: str = "ascii_art.txt",
        output_path: str = "profile.svg",
    ) -> None:
        """
        Render SVG from JSON and text files.

        Args:
            stats_json: Path to stats.json from main.py
            ascii_txt: Path to ascii_art.txt from ascii_converter.py
            output_path: Path to output SVG file
        """
        # Load stats
        with open(stats_json, "r") as f:
            stats = json.load(f)

        # Load ASCII art
        with open(ascii_txt, "r") as f:
            ascii_art = f.read()

        self.render(stats, ascii_art, output_path)
