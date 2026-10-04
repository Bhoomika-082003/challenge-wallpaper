"""Widgets = self-contained blocks (day header, habits, quote ...).

Every widget exposes:
    height(ctx) -> int          how many pixels it needs
    draw(ctx, y)  -> None       paint itself starting at vertical position y

To add a feature: write a class here, register it in WIDGETS, then add its
name to [layout] in config.toml. Nothing else needs to change.
"""
from __future__ import annotations

import json
import random

from . import tracker
from .config import ROOT


# ----------------------------------------------------------------- helpers
def _line_h(font) -> int:
    asc, desc = font.getmetrics()
    return asc + desc


def _spaced_width(font, text: str, tracking: int) -> float:
    return sum(font.getlength(c) for c in text) + tracking * max(len(text) - 1, 0)


def _draw_spaced(ctx, y, text, font, fill, tracking):
    """Centred text with letter-spacing (Pillow has none built in)."""
    x = (ctx.W - _spaced_width(font, text, tracking)) / 2
    for ch in text:
        ctx.draw.text((x, y), ch, font=font, fill=fill, anchor="la")
        x += font.getlength(ch) + tracking


def _wrap(font, text: str, max_w: int) -> list[str]:
    """Respect manual \\n, and wrap anything wider than max_w."""
    lines: list[str] = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split(" "):
            trial = f"{cur} {word}".strip()
            if font.getlength(trial) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def _load_json(name: str):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


# ----------------------------------------------------------------- widgets
class DayHeader:
    """'DAY 47' - the hero element."""

    def _text(self, ctx) -> str:
        if ctx.day < 1:
            return f"STARTS IN {1 - ctx.day}"
        if ctx.day > ctx.total:
            return "COMPLETE"
        return f"DAY {ctx.day}"

    def _font(self, ctx):
        return ctx.font("bold", 200 if ctx.day >= 1 else 110)

    def height(self, ctx):
        return _line_h(self._font(ctx))

    def draw(self, ctx, y):
        _draw_spaced(ctx, y, self._text(ctx), self._font(ctx), ctx.theme["fg"], ctx.px(10))


class ProgressBar:
    """'47 / 365' + a thin rounded bar."""

    def height(self, ctx):
        return _line_h(ctx.font("regular", 40)) + ctx.px(36) + ctx.px(14)

    def draw(self, ctx, y):
        t = ctx.theme
        shown = min(max(ctx.day, 0), ctx.total)
        font = ctx.font("regular", 40)
        _draw_spaced(ctx, y, f"{shown} / {ctx.total}", font, t["muted"], ctx.px(6))

        bar_w, bar_h = int(ctx.W * 0.62), ctx.px(14)
        x0 = (ctx.W - bar_w) // 2
        y0 = y + _line_h(font) + ctx.px(36)
        r = bar_h // 2
        ctx.draw.rounded_rectangle([x0, y0, x0 + bar_w, y0 + bar_h], r, fill=t["track"])
        fill_w = int(bar_w * shown / ctx.total)
        if fill_w > 0:
            ctx.draw.rounded_rectangle([x0, y0, x0 + max(fill_w, bar_h), y0 + bar_h], r, fill=t["accent"])


class Habits:
    """Checklist. static = all ticked, tracked = reads data/habit_log.json."""
    ROW = 128

    def _items(self, ctx):
        return ctx.cfg["habits"].get("items", [])

    def height(self, ctx):
        n = len(self._items(ctx))
        return max(n - 1, 0) * ctx.px(self.ROW) + ctx.px(70)

    def draw(self, ctx, y):
        t, items = ctx.theme, self._items(ctx)
        if not items:
            return
        tracked = ctx.cfg["habits"].get("mode", "static") == "tracked"
        log = tracker.load_log() if tracked else {}

        font = ctx.font("regular", 54)
        circle = ctx.px(70)
        gap = ctx.px(44)
        block_w = circle + gap + max(int(font.getlength(i)) for i in items)
        x0 = (ctx.W - block_w) // 2

        for i, name in enumerate(items):
            top = y + i * ctx.px(self.ROW)
            done = (not tracked) or tracker.is_done(log, ctx.today, name)
            cx, cy = x0 + circle // 2, top + circle // 2

            if done:
                ctx.draw.ellipse([x0, top, x0 + circle, top + circle], fill=t["accent"])
                # vector check mark (no font glyph needed)
                p = [(cx - circle * .22, cy + circle * .01),
                     (cx - circle * .06, cy + circle * .17),
                     (cx + circle * .24, cy - circle * .15)]
                ctx.draw.line(p, fill=t["bg_top"], width=max(ctx.px(7), 2), joint="curve")
            else:
                ctx.draw.ellipse([x0, top, x0 + circle, top + circle],
                                 outline=t["muted"], width=max(ctx.px(4), 2))

            label_col = t["fg"] if done else t["muted"]
            ctx.draw.text((x0 + circle + gap, cy), name, font=font, fill=label_col, anchor="lm")

            if tracked:
                s = tracker.streak(log, name, ctx.today)
                if s >= 2:
                    tx = x0 + circle + gap + font.getlength(name) + ctx.px(24)
                    ctx.draw.text((tx, cy), f"{s}d", font=ctx.font("regular", 36),
                                  fill=t["muted"], anchor="lm")


class Quote:
    """Bottom message. fixed text, or a deterministic 'quote of the day'."""

    def _lines(self, ctx):
        q = ctx.cfg["quote"]
        if q.get("mode", "fixed") == "daily":
            quotes = _load_json("quotes.json")
            text = random.Random(ctx.today.toordinal()).choice(quotes)  # same all day
        else:
            text = q.get("text", "One decision.\nEvery day.")
        return _wrap(ctx.font("light", 62), text, int(ctx.W * 0.78))

    def height(self, ctx):
        return len(self._lines(ctx)) * int(_line_h(ctx.font("light", 62)) * 1.15)

    def draw(self, ctx, y):
        font = ctx.font("light", 62)
        step = int(_line_h(font) * 1.15)
        for i, line in enumerate(self._lines(ctx)):
            ctx.draw.text((ctx.W / 2, y + i * step), line, font=font,
                          fill=ctx.theme["fg"], anchor="ma")


class KoreanWord:
    """오늘의 단어 - one word per day, cycling through data/korean_words.json."""

    def _word(self, ctx):
        words = _load_json("korean_words.json")
        return words[(max(ctx.day, 1) - 1) % len(words)]

    def height(self, ctx):
        return (_line_h(ctx.font("korean", 38)) + _line_h(ctx.font("korean", 130))
                + _line_h(ctx.font("regular", 40)) * 2 + ctx.px(50))

    def draw(self, ctx, y):
        t, w = ctx.theme, self._word(ctx)
        f_title, f_ko = ctx.font("korean", 38), ctx.font("korean", 130)
        f_sm = ctx.font("regular", 40)
        _draw_spaced(ctx, y, "오늘의 단어", f_title, t["muted"], ctx.px(6))
        y += _line_h(f_title) + ctx.px(10)
        ctx.draw.text((ctx.W / 2, y), w["ko"], font=f_ko, fill=t["fg"], anchor="ma")
        y += _line_h(f_ko) + ctx.px(10)
        ctx.draw.text((ctx.W / 2, y), w["rom"], font=f_sm, fill=t["muted"], anchor="ma")
        y += _line_h(f_sm)
        ctx.draw.text((ctx.W / 2, y), w["en"], font=f_sm, fill=t["fg"], anchor="ma")


class Weight:
    """Current -> target weight. Enable by adding 'weight' to [layout]."""

    def height(self, ctx):
        return _line_h(ctx.font("regular", 56)) + _line_h(ctx.font("regular", 34))

    def draw(self, ctx, y):
        w = ctx.cfg["weight"]
        unit = w.get("unit", "kg")
        f1, f2 = ctx.font("regular", 56), ctx.font("regular", 34)
        ctx.draw.text((ctx.W / 2, y), f'{w.get("current", 0)} → {w.get("target", 0)} {unit}',
                      font=f1, fill=ctx.theme["fg"], anchor="ma")
        _draw_spaced(ctx, y + _line_h(f1), "CURRENT → TARGET", f2, ctx.theme["muted"], ctx.px(4))


# Register new widgets here ------------------------------------------------
WIDGETS = {
    "day": DayHeader(),
    "progress": ProgressBar(),
    "habits": Habits(),
    "quote": Quote(),
    "korean": KoreanWord(),
    "weight": Weight(),
}
