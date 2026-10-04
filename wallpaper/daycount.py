"""Challenge-day maths. Day 1 == start_date."""
from __future__ import annotations

from datetime import date


def parse_date(s: str) -> date:
    return date.fromisoformat(s)


def current_day(start: date, today: date) -> int:
    """(today - start) + 1. Can be <1 before the start, >total after the end."""
    return (today - start).days + 1
