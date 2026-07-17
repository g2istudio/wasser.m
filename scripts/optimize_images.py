#!/usr/bin/env python3
"""Create WebP variants for oversized raster assets and update site references."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
TEXT_EXTENSIONS = {".html", ".js", ".json", ".xml", ".css"}


def main():
    replacements = {}
    for source in ASSETS.rglob("*"):
        if source.suffix.lower() not in {".png", ".jpg", ".jpeg"} or source.stat().st_size <= 500_000:
            continue
        target = source.with_suffix(".webp")
        with Image.open(source) as image:
            image = ImageOps.exif_transpose(image)
            if max(image.size) > 1800:
                image.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
            image.save(target, "WEBP", quality=82, method=6)
        old = source.relative_to(ROOT).as_posix()
        new = target.relative_to(ROOT).as_posix()
        replacements[old] = new
        replacements["../" + old] = "../" + new
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS or ".git" in path.parts:
            continue
        text = path.read_text()
        changed = text
        for old, new in replacements.items():
            changed = changed.replace(old, new)
        if changed != text:
            path.write_text(changed)
    for old, new in sorted(replacements.items()):
        if not old.startswith("../"):
            print(f"{old} -> {new}")


if __name__ == "__main__":
    main()
