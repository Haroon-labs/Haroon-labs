"""Remove background from profile image."""

from PIL import Image
from rembg import remove


def remove_background(input_path="profile.png", output_path="profile.png", bg_color=(20, 20, 20)):
    """
    Remove background from image and add dark background.

    Args:
        input_path: Path to input image
        output_path: Path to save processed image
        bg_color: RGB tuple for background color (default: dark gray)
    """
    print(f"[*] Removing background from {input_path}...")

    # Load image
    input_image = Image.open(input_path)

    # Remove background (creates RGBA with transparency)
    output_image = remove(input_image)

    # Create dark background image
    bg_image = Image.new("RGB", output_image.size, bg_color)

    # Paste the image with transparency onto the dark background
    bg_image.paste(output_image, mask=output_image.split()[3] if output_image.mode == "RGBA" else None)

    # Convert back to RGB and save
    bg_image.save(output_path)

    print(f"[OK] Background removed and replaced! Saved to {output_path}")
    print(f"   Image size: {bg_image.size}")
    print(f"   Background color: RGB{bg_color}")
    print(f"   Format: PNG (dark background)")


if __name__ == "__main__":
    remove_background()
