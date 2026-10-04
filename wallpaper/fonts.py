"""Font discovery. Looks in assets/fonts first, then common OS locations.

Drop Inter-*.ttf and NotoSansKR*.ttf (both free, OFL licence) into assets/fonts/
for the nicest look. Otherwise Windows' Segoe UI / Malgun Gothic are used.
"""
from __future__ import annotations

import glob
from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

ROOT = Path(__file__).resolve().parent.parent

CANDIDATES = {
    "bold": [
        "assets/fonts/Inter*Bold*.ttf", "assets/fonts/Inter*SemiBold*.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf",
        "/usr/share/fonts/truetype/inter/Inter*Bold*.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ],
    "regular": [
        "assets/fonts/Inter*Regular*.ttf", "assets/fonts/Inter*.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ],
    "light": [
        "assets/fonts/Inter*Light*.ttf", "assets/fonts/Inter*Regular*.ttf",
        r"C:\Windows\Fonts\segoeuil.ttf", r"C:\Windows\Fonts\segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
    "korean": [
        "assets/fonts/NotoSansKR*.ttf", "assets/fonts/NotoSansKR*.otf",
        r"C:\Windows\Fonts\malgun.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    ],
}


@lru_cache(maxsize=None)
def _resolve(role: str) -> str | None:
    for pattern in CANDIDATES[role]:
        full = pattern if Path(pattern).is_absolute() or pattern[1:2] == ":" else str(ROOT / pattern)
        hits = sorted(glob.glob(full))
        if hits:
            return hits[0]
    return None


@lru_cache(maxsize=None)
def get_font(role: str, size: int) -> ImageFont.FreeTypeFont:
    path = _resolve(role)
    if path is None:
        print(f"[warn] no '{role}' font found - using Pillow default. See README (fonts).")
        return ImageFont.load_default(size)
    return ImageFont.truetype(path, size)
