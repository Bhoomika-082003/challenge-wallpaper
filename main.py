#!/usr/bin/env python3
"""Generate today's challenge wallpaper.

  python main.py                         -> output/wallpaper.png (stable name)
  python main.py --date 2026-12-01       -> pretend it's that date (testing)
  python main.py --theme beige
  python main.py --preview               -> output/preview_<theme>.png for every theme
"""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from wallpaper.config import ROOT, load_config, today_in_tz
from wallpaper.daycount import current_day, parse_date
from wallpaper.renderer import render
from wallpaper.themes import THEMES


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", help="path to config.toml")
    ap.add_argument("--date", help="override today's date (YYYY-MM-DD)")
    ap.add_argument("--theme", help="override theme for this run")
    ap.add_argument("--out", help="output file (default output/wallpaper.png)")
    ap.add_argument("--archive", action="store_true", help="also keep output/archive/day-XXX.png")
    ap.add_argument("--preview", action="store_true", help="render every built-in theme")
    args = ap.parse_args()

    cfg = load_config(args.config)
    ch = cfg["challenge"]
    today: date = parse_date(args.date) if args.date else today_in_tz(ch["timezone"])
    day = current_day(parse_date(ch["start_date"]), today)
    out_dir = ROOT / "output"
    out_dir.mkdir(exist_ok=True)

    if args.preview:
        for name in list(THEMES) + list(cfg.get("themes", {})):
            p = out_dir / f"preview_{name}.png"
            render(cfg, today, name).save(p)
            print("wrote", p)
        return

    img = render(cfg, today, args.theme)
    out = Path(args.out) if args.out else out_dir / "wallpaper.png"
    img.save(out, optimize=True)
    (out_dir / "day.txt").write_text(str(day))      # used by the CI commit message
    print(f"{today} -> DAY {day} -> {out}")

    if args.archive:
        arch = out_dir / "archive"
        arch.mkdir(exist_ok=True)
        img.save(arch / f"day-{day:03d}.png", optimize=True)


if __name__ == "__main__":
    main()
