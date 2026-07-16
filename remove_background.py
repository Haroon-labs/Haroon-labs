"""Remove background from profile image."""

from PIL import Image
from rembg import remove


def remove_background(input_path="profile.png", output_path="profile.png"):
    """
    Remove background from image using rembg.

    Args:
        input_path: Path to input image
        output_path: Path to save processed image
    """
    print(f"[*] Removing background from {input_path}...")

    # Load image
    input_image = Image.open(input_path)

    # Remove background
    output_image = remove(input_image)

    # Save with transparency
    output_image.save(output_path)

    print(f"[OK] Background removed! Saved to {output_path}")
    print(f"   Image size: {output_image.size}")
    print(f"   Format: PNG (transparent background)")


if __name__ == "__main__":
    remove_background()
