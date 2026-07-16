"""Convert images to ASCII art with grayscale character mapping."""

import os
from typing import Tuple


class ASCIIConverter:
    """Converts images to ASCII art using brightness-mapped characters."""

    # Characters mapped from darkest to lightest (by visual density)
    ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ","]

    def __init__(self, width: int = 70):
        """
        Initialize converter.

        Args:
            width: Width of ASCII output in characters
        """
        self.width = width
        self.height = None
        self._check_imports()

    def _check_imports(self) -> None:
        """Check for required image libraries."""
        try:
            import numpy as np
            self.np = np
            self.use_numpy = True
        except ImportError:
            self.use_numpy = False
            try:
                from PIL import Image
                self.Image = Image
            except ImportError:
                raise ImportError(
                    "ASCII conversion requires PIL/Pillow or numpy. "
                    "Install with: pip install Pillow  (or numpy)"
                )

    def _convert_with_numpy(self, image_path: str) -> Tuple[list, int, int]:
        """Convert image using numpy + imageio."""
        try:
            import imageio
        except ImportError:
            raise ImportError(
                "numpy-based conversion requires imageio. "
                "Install with: pip install imageio"
            )

        img = imageio.imread(image_path)

        # Convert to grayscale
        if len(img.shape) == 3:  # RGB/RGBA
            if img.shape[2] == 4:  # RGBA
                img = img[:, :, :3]
            gray = (0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]).astype('uint8')
        else:
            gray = img

        # Resize
        aspect_ratio = gray.shape[0] / gray.shape[1]
        new_height = int(self.width * aspect_ratio * 0.55)

        # Simple resize by sampling
        step_x = gray.shape[1] // self.width
        step_y = gray.shape[0] // new_height
        resized = gray[::step_y, ::step_x][:new_height, :self.width]

        return resized, resized.shape[0], resized.shape[1]

    def _convert_with_pil(self, image_path: str) -> Tuple[list, int, int]:
        """Convert image using PIL/Pillow."""
        img = self.Image.open(image_path)

        # Convert to grayscale
        gray = img.convert("L")

        # Resize maintaining aspect ratio
        aspect_ratio = gray.height / gray.width
        new_height = int(self.width * aspect_ratio * 0.55)
        gray = gray.resize((self.width, new_height))

        pixels = list(gray.getdata())
        return pixels, new_height, self.width

    def _pixels_to_ascii(self, pixels, height: int, width: int) -> str:
        """Convert pixels to ASCII string."""
        ascii_str = ""
        for i, pixel in enumerate(pixels):
            if i > 0 and i % width == 0:
                ascii_str += "\n"

            # Map brightness to ASCII char
            char_index = (pixel * len(self.ASCII_CHARS)) // 256
            char_index = min(char_index, len(self.ASCII_CHARS) - 1)
            ascii_str += self.ASCII_CHARS[char_index]

        return ascii_str

    def convert(self, image_path: str) -> str:
        """
        Convert image file to ASCII art.

        Args:
            image_path: Path to input image

        Returns:
            ASCII art as string (newline-separated)
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        try:
            if self.use_numpy:
                pixels, height, width = self._convert_with_numpy(image_path)
                # Flatten numpy array
                pixels = pixels.flatten().tolist()
            else:
                pixels, height, width = self._convert_with_pil(image_path)
        except Exception as e:
            raise RuntimeError(f"Failed to convert image: {e}")

        ascii_str = self._pixels_to_ascii(pixels, height, width)
        return ascii_str

    def convert_to_file(self, image_path: str, output_path: str = "ascii_art.txt") -> str:
        """
        Convert image to ASCII and save to file.

        Args:
            image_path: Path to input image
            output_path: Path to output text file

        Returns:
            ASCII art string
        """
        ascii_art = self.convert(image_path)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ascii_art)
        print(f"[OK] ASCII art saved to {output_path}")
        return ascii_art
