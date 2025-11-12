import os
import re
from PIL import Image

# --- CONFIG ---
SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg")
CONVERT_TO_JPG = (".jfif", ".jiff", ".jpeg")

def normalize_filename(filename):
    """Normalize to lowercase, remove special chars, collapse dashes/underscores."""
    name, ext = os.path.splitext(filename)
    name = name.lower()
    name = re.sub(r"[^a-z0-9._-]+", "_", name)
    name = re.sub(r"[-_]{2,}", "-", name)
    name = re.sub(r"^[-_]+|[-_]+$", "", name)
    return f"{name}{ext.lower()}"

def convert_to_jpg(src, dst):
    """Convert any nonstandard image (JFIF/JIFF) to JPEG."""
    try:
        with Image.open(src) as im:
            rgb = im.convert("RGB")
            rgb.save(dst, "JPEG")
        print(f"Converted: {src} → {dst}")
        os.remove(src)
    except Exception as e:
        print(f"⚠️ Failed to convert {src}: {e}")

def main():
    for root, _, files in os.walk("."):
        for file in files:
            old_path = os.path.join(root, file)
            if not os.path.isfile(old_path):
                continue

            _, ext = os.path.splitext(file)
            ext_lower = ext.lower()

            # Convert unsupported extensions
            if ext_lower in CONVERT_TO_JPG:
                new_path = os.path.join(root, os.path.splitext(file)[0] + ".jpg")
                convert_to_jpg(old_path, new_path)
                file = os.path.basename(new_path)
                old_path = new_path
                ext_lower = ".jpg"

            # Skip unsupported files entirely
            if ext_lower not in SUPPORTED_EXTENSIONS:
                continue

            new_name = normalize_filename(file)
            new_path = os.path.join(root, new_name)

            if new_path != old_path:
                print(f"Renaming: {file} → {new_name}")
                os.rename(old_path, new_path)

    print("\n✅ Normalization complete.")
    print("Run `git status` to review changes, then commit and push.")

if __name__ == "__main__":
    main()
