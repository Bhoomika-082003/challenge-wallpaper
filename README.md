# Auto-Updating iPhone Challenge Wallpaper

Shows `DAY 1 ... DAY 365`, your habit checklist and a message on your iPhone wallpaper,
updated every morning with no manual work. 100% free.

```
challenge-wallpaper/
├── config.toml               <- edit this: start date, theme, habits, layout
├── main.py                   <- command line entry point
├── requirements.txt
├── run_local.bat             <- Windows/iCloud route (Option B)
├── wallpaper/
│   ├── config.py             <- loads config, device sizes, timezone
│   ├── daycount.py           <- (today - start) + 1
│   ├── themes.py             <- black / beige / purple (+ custom in config)
│   ├── fonts.py              <- finds fonts on Windows / Linux / assets
│   ├── widgets.py            <- day, progress, habits, quote, korean, weight
│   ├── tracker.py            <- habit log + streak maths
│   └── renderer.py           <- layout engine, draws the PNG
├── data/
│   ├── quotes.json           <- quote-of-the-day pool
│   ├── korean_words.json     <- 오늘의 단어 pool
│   └── habit_log.json        <- per-day habit ticks (tracked mode)
├── assets/fonts/             <- optional: Inter + Noto Sans KR
├── output/wallpaper.png      <- always the latest image (stable filename)
├── shortcuts/SETUP.md        <- iPhone setup
└── .github/workflows/daily.yml   <- free daily automation in the cloud
```

## How it works (recommended architecture)

```
GitHub Actions (cron, free)  ->  Python + Pillow makes PNG  ->  committed to repo
                                                                      |
iPhone Shortcut @ 6:00 AM  ->  downloads the PNG by URL  ->  Set Wallpaper
```

Why this beats the alternatives: the laptop doesn't need to be on, there is no server to
maintain, and the iPhone only needs one stable URL. Python/Pillow is the simplest renderer
(Option A). HTML rendering needs a headless browser; a native app needs a paid developer
account to install long-term.

## Install (about 15 minutes)

### 1. Test locally on Windows
1. Install Python 3.11+ from python.org (tick "Add to PATH").
2. In this folder: `pip install -r requirements.txt`
3. Edit `config.toml` (start date, theme, habits).
4. `python main.py --preview` -> open `output/preview_*.png` and pick a theme.
5. `python main.py --date 2026-12-01` to test any day, including `DAY 365`.

### 2. Fonts (optional but recommended)
Windows already has Segoe UI and Malgun Gothic (Korean), so it works out of the box. For a
more premium look, download **Inter** and **Noto Sans KR** (both free, OFL licence) and put
`Inter-Bold.ttf`, `Inter-Regular.ttf`, `Inter-Light.ttf`, `NotoSansKR-*.ttf` in `assets/fonts/`.
Commit them so the cloud build uses the same fonts.

### 3. Option A (recommended): GitHub Actions
1. Create a free GitHub account and a **public** repository, push this folder to it.
   (Public is required for the simple raw URL; the image holds nothing sensitive.)
2. Repo -> Settings -> Actions -> General -> Workflow permissions -> **Read and write**.
3. Edit the cron line in `.github/workflows/daily.yml` (UTC!) so it runs about an hour before 6 AM your time.
4. Actions tab -> **Daily wallpaper** -> **Run workflow** once to test.
5. Your URL is `https://raw.githubusercontent.com/USER/REPO/main/output/wallpaper.png`
6. Follow `shortcuts/SETUP.md`.

### 4. Option B: laptop + iCloud Drive (no GitHub)
1. Install **iCloud for Windows**, make a folder `Wallpaper` in iCloud Drive.
2. Edit the path in `run_local.bat`.
3. Task Scheduler -> Create Basic Task -> Daily 5:30 AM -> Start a program -> `run_local.bat`
   (tick "Run task as soon as possible after a scheduled start is missed" and "Wake the computer").
4. Use section D of `shortcuts/SETUP.md`.
Downside: the laptop must be on/asleep-but-wakeable and synced by 6 AM.

## Customising

| I want to...               | Do this |
|----------------------------|---------|
| Change theme               | `config.toml` -> `[display] theme = "beige"` |
| Own colours                | add a `[themes.mine]` block (see the commented example) |
| Change habits              | edit `[habits] items` |
| Daily random quote         | `[quote] mode = "daily"` and edit `data/quotes.json` |
| Add Korean word            | put `"korean"` into a `[layout]` list (e.g. `middle = ["habits", "korean"]`) |
| Add weight line            | fill `[weight]`, add `"weight"` to `[layout]` |
| Move things under the clock| adjust `safe_top` |
| Other iPhone size          | `[display] device = "iphone_pro"` or set `width`/`height` |

Layout note: on the lock screen iOS draws the clock in the top ~25% and buttons at the
bottom, so content sits between them. If you use it as a home-screen wallpaper, lower `safe_top`.

## Edge cases handled
- Before the start date it shows `STARTS IN N`; after day 365 it shows `COMPLETE`.
- "Today" uses your configured time zone, not the server's.
- Same quote all day (seeded by date), so reruns don't change the picture.

## Known limits
- GitHub's raw URL is cached for a few minutes; the Shortcut adds a `?v=` timestamp to avoid stale images.
- GitHub scheduled runs can start a few minutes late (hence building an hour early), and GitHub may
  pause schedules on repos with no activity for 60 days; the daily commit normally counts as activity,
  but check the Actions tab if the image ever stops changing.
- iOS can occasionally delay or skip personal automations; open the Shortcuts app and run it manually if so.

## Scalability roadmap

1. **Habit tracking** (already scaffolded): set `[habits] mode = "tracked"`. Today it reads
   `data/habit_log.json`. Next step: an iPhone Shortcut that appends today's ticks to that file
   (via the GitHub API with a token, or a tiny free form), so unchecked habits show as empty rings and
   streaks (`7d`) appear automatically.
2. **Streak widgets**: `tracker.streak()` already computes them; add a `Streaks` class in `widgets.py`.
3. **Weight tracking**: store a `data/weight.csv` and plot a sparkline widget; keep it in a **private** repo
   (or the iCloud route) because the raw-URL approach needs a public repo.
4. **More content**: add a class to `widgets.py`, register it in `WIDGETS`, reference it in `[layout]`.
5. **Home vs lock screen**: render two files (`--out` plus a second config) and use two Shortcut actions.
6. **Archive**: `python main.py --archive` keeps `output/archive/day-047.png` for a year-end collage.
