#!/usr/bin/env python3
"""
Optimize city photos for the Mirvan site.

For each source photo in /public/, generate:
  - {slug}-hero.jpg        — full-bleed hero, 1920w max, ~150-250KB
  - {slug}-og.jpg          — 1200x630 OG card, ~60-100KB

The originals stay where they are; the optimized versions go in /public/cities/.

Run: python3 optimize-images.py
"""

from pathlib import Path
from PIL import Image, ImageOps

SRC_DIR = Path(__file__).parent / "public"
OUT_DIR = SRC_DIR / "cities"
OUT_DIR.mkdir(exist_ok=True)

# Map source filename -> slug used by cities.json
SOURCES = {
    "san_diego_photo.jpg": "san-diego",
    "la_photo.jpg": "los-angeles",
    "phoenix_photo.jpg": "phoenix",
    "las_vegas_photo.jpg": "las-vegas",
    "austin_photo.jpg": "austin",
    "dallas_ftworth_photo.jpg": "dallas-fort-worth",
    "miami_photo.jpg": "miami",
    "tampa_photo.jpg": "tampa",
}

HERO_MAX_WIDTH = 1920
HERO_QUALITY = 75
OG_W, OG_H = 1200, 630
OG_QUALITY = 80


def optimize_hero(src: Path, dst: Path) -> int:
    """Resize to max width, save as progressive jpeg. Returns final size in bytes."""
    img = Image.open(src)
    img = ImageOps.exif_transpose(img)  # respect EXIF orientation
    img = img.convert("RGB")

    if img.width > HERO_MAX_WIDTH:
        ratio = HERO_MAX_WIDTH / img.width
        new_h = int(img.height * ratio)
        img = img.resize((HERO_MAX_WIDTH, new_h), Image.LANCZOS)

    img.save(
        dst,
        format="JPEG",
        quality=HERO_QUALITY,
        optimize=True,
        progressive=True,
    )
    return dst.stat().st_size


def optimize_og(src: Path, dst: Path) -> int:
    """Crop to 1200x630 (entropy-style center crop), save lean."""
    img = Image.open(src)
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGB")

    # Smart fit-crop to 1200x630
    img = ImageOps.fit(img, (OG_W, OG_H), method=Image.LANCZOS, centering=(0.5, 0.4))

    img.save(
        dst,
        format="JPEG",
        quality=OG_QUALITY,
        optimize=True,
        progressive=True,
    )
    return dst.stat().st_size


def kb(n: int) -> str:
    return f"{n / 1024:.0f}KB"


def main():
    print(f"Optimizing {len(SOURCES)} images → {OUT_DIR.relative_to(Path.cwd())}/\n")
    total_before = 0
    total_after = 0
    for filename, slug in SOURCES.items():
        src = SRC_DIR / filename
        if not src.exists():
            print(f"  ✗ MISSING: {filename}")
            continue

        before = src.stat().st_size
        total_before += before

        hero_dst = OUT_DIR / f"{slug}-hero.jpg"
        og_dst = OUT_DIR / f"{slug}-og.jpg"

        hero_size = optimize_hero(src, hero_dst)
        og_size = optimize_og(src, og_dst)
        total_after += hero_size + og_size

        print(
            f"  ✓ {slug:22s}  {kb(before):>7s} → "
            f"hero {kb(hero_size):>7s}  og {kb(og_size):>6s}"
        )

    print(
        f"\nTotal: {kb(total_before)} → {kb(total_after)} "
        f"({100 * total_after / total_before:.0f}% of original)"
    )


if __name__ == "__main__":
    main()
