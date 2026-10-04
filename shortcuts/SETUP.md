# iPhone Shortcuts setup (5 minutes)

## A. Create the shortcut  ("Daily Wallpaper")

Shortcuts app -> **+** -> name it `Daily Wallpaper`, then add these actions in order:

1. **Current Date**
2. **Format Date** -> Date Format: *Custom* -> `yyyyMMddHHmm`
   (this becomes a throw-away number that stops iOS/GitHub from serving a cached old image)
3. **Text** -> paste your URL, then tap the end and insert the *Formatted Date* variable:
   `https://raw.githubusercontent.com/YOUR_USER/YOUR_REPO/main/output/wallpaper.png?v=`**[Formatted Date]**
4. **Get Contents of URL** -> input: the Text from step 3 (Method: GET)
5. **Set Wallpaper** -> input: *Contents of URL*
   - Tap the **>** arrow to expand the options
   - Choose **Lock Screen** (or Lock Screen and Home Screen)
   - Turn **Show Preview** OFF   <- required, otherwise it asks every time

Tap **Play** once. Your wallpaper should change. If it works manually, the automation will work.

## B. Schedule it for 6:00 AM

1. Shortcuts -> **Automation** tab -> **+** -> **Time of Day**
2. Time **6:00 AM**, Repeat **Daily**
3. Next -> **Add Action** -> **Run Shortcut** -> pick `Daily Wallpaper`
4. Next -> set **Run Immediately** (not "Run After Confirmation")
5. Turn **Notify When Run** OFF -> Done

## C. Reliability tips

- Settings -> Notifications -> Shortcuts: turning banners off hides the "automation ran" banner.
- Keep the iPhone with data/Wi-Fi at 6 AM (it must download the image).
- If an automation ever doesn't fire, open Shortcuts -> Automation and confirm it's still enabled.

## D. Using the iCloud Drive route instead (Option B / Windows laptop)

Replace steps 1-4 with:
1. **Get File** -> *Service:* iCloud Drive -> path `Wallpaper/wallpaper.png` -> turn **Show Document Picker** OFF
2. **Set Wallpaper** as in step 5 above.

Note: this only works if the laptop actually generated and synced the file before 6 AM.

## E. Fallback if "Set Wallpaper" misbehaves on your iOS version

Replace step 5 with **Save to Photo Album** -> album `Challenge`, then set your lock screen
to **Photo Shuffle** using only that album. Less clean, but needs no wallpaper action.
