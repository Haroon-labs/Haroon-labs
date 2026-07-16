"""Render GitHub profile (ASCII art + info) into SVG."""

import json
from pathlib import Path
from typing import Dict


class SVGRenderer:
    """Renders GitHub profile with ASCII art + info into SVG (dark + light modes)."""

    DARK_MODE = {
        "bg": "#0d1117",
        "text": "#c9d1d9",
    }

    LIGHT_MODE = {
        "bg": "#ffffff",
        "text": "#24292e",
    }

    def __init__(self):
        """Initialize renderer."""
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

    def _build_profile_lines(self, stats: Dict) -> list:
        """Build profile info lines from stats."""
        return [
            "Haroon Abdul-Ali",
            "",
            "OS:............................. Windows 11, Linux",
            "Uptime:......................... Always Learning",
            "Host:........................... Digital Future Lab",
            "Kernel:......................... Growth-Oriented",
            "IDEs:........................... VS Code, Neovim",
            "",
            f"Languages.Programming:.......... Python, JavaScript, TypeScript",
            f"Languages.Computer:............ HTML, CSS, SQL, Markdown",
            f"Languages.Real:................ English, German",
            "",
            f"Hobbies.Software:.............. Web Dev, AI/ML, Open Source",
            f"Hobbies.Hardware:.............. Tech, Automation, IoT",
            "",
            "Contact",
            "Email.Personal:................ haroonabdulali.w@gmail.com",
            "LinkedIn:...................... HaroonAbdul-Ali",
            "Discord:........................ [your handle]",
            "",
            "GitHub Stats",
            f"Repos: {stats['total_repos']} | Stars: {stats['total_stars']} | Commits: {stats['total_commits']:,}",
        ]

    def _create_profile_svg(
        self, ascii_lines: list, profile_lines: list, colors: Dict
    ) -> str:
        """
        Create SVG with ASCII art + profile info side-by-side.

        Args:
            ascii_lines: List of ASCII art lines
            profile_lines: List of profile info lines
            colors: Dict with 'bg' and 'text' colors

        Returns:
            SVG content string
        """
        ascii_width = 70
        char_width = 6.6  # pixels per character in monospace
        spacing = 2

        svg_text_elements = []
        max_lines = max(len(ascii_lines), len(profile_lines))

        for i in range(max_lines):
            y = 50 + (i * self.line_height)

            ascii_part = ascii_lines[i] if i < len(ascii_lines) else " " * ascii_width
            ascii_part = ascii_part.ljust(ascii_width)
            ascii_escaped = self._escape_svg_text(ascii_part)

            info_part = profile_lines[i] if i < len(profile_lines) else ""
            info_escaped = self._escape_svg_text(info_part)

            # ASCII art
            svg_text_elements.append(
                f'  <text x="20" y="{y}" font-family="{self.font_family}" '
                f'font-size="{self.font_size}" fill="{colors["text"]}" '
                f'xml:space="preserve">{ascii_escaped}</text>'
            )

            # Profile info
            if info_part:
                info_x = 20 + int(ascii_width * char_width) + 15
                svg_text_elements.append(
                    f'  <text x="{info_x}" y="{y}" font-family="{self.font_family}" '
                    f'font-size="{self.font_size}" fill="{colors["text"]}">{info_escaped}</text>'
                )

        svg_height = 50 + (max_lines * self.line_height) + 30
        svg_width = 20 + int(ascii_width * char_width) + 15 + 350

        svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      text {{ white-space: pre; }}
    </style>
  </defs>
  <rect width="{svg_width}" height="{svg_height}" fill="{colors['bg']}"/>
{''.join([f'  {line}' + chr(10) for line in svg_text_elements])}
</svg>
"""
        return svg_content.strip()

    def render(
        self,
        stats: Dict,
        ascii_art: str,
        output_dark: str = "dark_mode.svg",
        output_light: str = "light_mode.svg",
    ) -> None:
        """
        Render profile SVG in both dark and light modes.

        Args:
            stats: Stats dict from main.py
            ascii_art: ASCII art string (newline-separated)
            output_dark: Path to dark mode SVG
            output_light: Path to light mode SVG
        """
        ascii_lines = ascii_art.strip().split("\n")
        profile_lines = self._build_profile_lines(stats)

        # Dark mode
        dark_svg = self._create_profile_svg(ascii_lines, profile_lines, self.DARK_MODE)
        with open(output_dark, "w", encoding="utf-8") as f:
            f.write(dark_svg)
        print(f"[OK] Dark mode SVG: {output_dark}")

        # Light mode
        light_svg = self._create_profile_svg(ascii_lines, profile_lines, self.LIGHT_MODE)
        with open(output_light, "w", encoding="utf-8") as f:
            f.write(light_svg)
        print(f"[OK] Light mode SVG: {output_light}")

    def render_from_files(
        self,
        stats_json: str = "stats.json",
        ascii_txt: str = "ascii_art.txt",
        output_dark: str = "dark_mode.svg",
        output_light: str = "light_mode.svg",
    ) -> None:
        """
        Render SVG from JSON and text files.

        Args:
            stats_json: Path to stats.json from main.py
            ascii_txt: Path to ascii_art.txt from ascii_converter.py
            output_dark: Path to dark mode SVG
            output_light: Path to light mode SVG
        """
        with open(stats_json, "r") as f:
            stats = json.load(f)

        with open(ascii_txt, "r") as f:
            ascii_art = f.read()

        self.render(stats, ascii_art, output_dark, output_light)
