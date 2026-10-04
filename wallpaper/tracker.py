"""Habit log helpers (data/habit_log.json).

Format:  { "2026-10-05": {"No Sugar": true, "Workout": false}, ... }
Edit the file by hand today; later a Shortcut / web form can write to it.
"""
from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

from .config import ROOT

LOG_PATH = ROOT / "data" / "habit_log.json"


def load_log(path: Path = LOG_PATH) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}


def is_done(log: dict, day: date, habit: str) -> bool:
    return bool(log.get(day.isoformat(), {}).get(habit, False))


def streak(log: dict, habit: str, today: date) -> int:
    """Consecutive completed days. Today not being done yet doesn't break it."""
    d = today if is_done(log, today, habit) else today - timedelta(days=1)
    n = 0
    while is_done(log, d, habit):
        n += 1
        d -= timedelta(days=1)
    return n
