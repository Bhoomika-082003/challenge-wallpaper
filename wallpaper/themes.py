"""Colour themes. Add your own here or under [themes.name] in config.toml."""
from __future__ import annotations

Color = tuple[int, int, int]

THEMES: dict[str, dict[str, Color]] = {
    "black": dict(
        bg_top=(0, 0, 0), bg_bottom=(0, 0, 0),
        fg=(255, 255, 255), muted=(140, 140, 140),
        accent=(255, 255, 255), track=(42, 42, 42),
    ),
    "beige": dict(
        bg_top=(238, 230, 216), bg_bottom=(221, 210, 192),
        fg=(38, 33, 28), muted=(122, 111, 98),
        accent=(38, 33, 28), track=(204, 192, 173),
    ),
    "purple": dict(
        bg_top=(38, 18, 62), bg_bottom=(12, 5, 24),
        fg=(245, 239, 255), muted=(166, 148, 198),
        accent=(204, 172, 255), track=(68, 45, 100),
    ),
}


def _hex(h: str) -> Color:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def get_theme(name: str, cfg: dict) -> dict[str, Color]:
    """Built-in themes first, then custom ones from config.toml."""
    custom = cfg.get("themes", {})
    if name in custom:
        base = dict(THEMES["black"])
        base.update({k: _hex(v) for k, v in custom[name].items()})
        return base
    if name not in THEMES:
        raise SystemExit(f"Unknown theme '{name}'. Choose from: {', '.join(list(THEMES) + list(custom))}")
    return THEMES[name]
