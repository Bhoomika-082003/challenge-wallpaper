"""Config loading + small helpers shared by the whole project."""
from __future__ import annotations

import tomllib
from datetime import date
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent

# Device presets (pixels, portrait). Wallpapers are cropped/scaled by iOS to fit,
# so the Pro Max size works well on every modern iPhone.
DEVICES = {
    "iphone_pro_max": (1290, 2796),   # 14/15/16 Plus & Pro Max class
    "iphone_pro":     (1179, 2556),   # 14/15/16 Pro class
    "iphone_16_pro":  (1206, 2622),
    "iphone_se":      (750, 1334),
}


def load_config(path: str | Path | None = None) -> dict:
    """Read config.toml and fill in defaults."""
    path = Path(path) if path else ROOT / "config.toml"
    with open(path, "rb") as fh:
        cfg = tomllib.load(fh)

    cfg.setdefault("challenge", {})
    cfg.setdefault("display", {})
    cfg.setdefault("layout", {})
    cfg.setdefault("habits", {})
    cfg.setdefault("quote", {})
    cfg.setdefault("weight", {})

    ch = cfg["challenge"]
    ch.setdefault("total_days", 365)
    ch.setdefault("timezone", "UTC")

    d = cfg["display"]
    d.setdefault("theme", "black")
    d.setdefault("safe_top", 0.27)
    d.setdefault("safe_bottom", 0.10)
    if "width" not in d or "height" not in d:
        d["width"], d["height"] = DEVICES.get(d.get("device", "iphone_pro_max"), DEVICES["iphone_pro_max"])

    lay = cfg["layout"]
    lay.setdefault("top", ["day", "progress"])
    lay.setdefault("middle", ["habits"])
    lay.setdefault("bottom", ["quote"])
    return cfg


def today_in_tz(tz_name: str) -> date:
    """'Today' in the user's own time zone (matters when running on a UTC server)."""
    from datetime import datetime
    return datetime.now(ZoneInfo(tz_name)).date()
