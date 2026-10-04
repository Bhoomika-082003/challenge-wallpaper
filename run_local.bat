@echo off
REM Local (laptop) alternative: generate the image into your iCloud Drive folder.
REM 1. Edit OUT below to your iCloud Drive path (iCloud for Windows must be installed).
REM 2. Schedule this file with Windows Task Scheduler (see README, "Option B").
set OUT=%USERPROFILE%\iCloudDrive\Wallpaper\wallpaper.png
cd /d "%~dp0"
python main.py --out "%OUT%"
