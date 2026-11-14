# Babel NS2 Android launcher icon resource package

Reference: user-circled Babel NS2 logo from the 2026-11-14 branding-board screenshot. This is a faithful **vector redraw**, not a byte-identical extraction from the original Techbenders Drive master. The approved source artwork should be used for an exact-match production export if available.

## Contents
- `source/launcher-master.svg` and `source/launcher-1024.png`: full-color legacy launcher master.
- `source/adaptive-foreground.svg` / `adaptive-foreground-1024.png`: sunset plus ziggurat on a transparent 1024-square canvas, centered in the adaptive safe zone.
- `source/adaptive-background.svg` / `adaptive-background-1024.png`: dark navy background.
- `source/themed-monochrome.svg` / `themed-monochrome-1024.png`: white silhouette on alpha for Android themed icons.
- `app/src/main/res/mipmap-{mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi}/`: legacy launcher sizes and round variants.
- `app/src/main/res/mipmap-anydpi-v26/`: Android 8+ adaptive XML definitions with Android 13+ monochrome layer.
- `app/src/main/res/drawable-nodpi/`: adaptive source layers.
- `play-store-512.png`: 512-square Play Store graphic candidate.

## Integration
1. Copy the `app/src/main/res/` contents into the Android app module's corresponding resource directory, checking for existing icon customizations before replacement.
2. Confirm `<application android:icon="@mipmap/ic_launcher" android:roundIcon="@mipmap/ic_launcher_round">` in `AndroidManifest.xml` where appropriate.
3. Preview circle, squircle, and themed treatments on a real device/emulator. Confirm the exact icon appearance and app packaging before merge.

**Status:** Rendered and file-verified assets only. No repository changes, Android compilation, emulator checks, or GitHub PR have been performed.
