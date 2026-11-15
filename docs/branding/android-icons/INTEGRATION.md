# Corrected Android icon integration

## Provenance and preserved sources

Imported on 2026-11-14 from the user-supplied **Babel-NS2-repo-ready.zip**
(attachment filename `1-Babel-NS2-repo-ready.zip`). Archive SHA-256:

```text
f405fbb09e6020eec1a64e98f2a7187faba066fa20c381de44cf41a3fb8ae731
```

This is the approved corrected 26-file package: gold ziggurat, complete circular
orange-to-purple striped sunset, and dark background. All 26 packaged files are
imported byte-for-byte, including four SVGs and 18 PNGs. No artwork was regenerated.
The package describes its source as a vector redraw; it is not an extraction from
the original Drive master. The originals in [`../assets/`](../assets/) and their
researched cuneiform remain unchanged.

[`README.md`](README.md) and [`manifest.json`](manifest.json) are preserved package
records. The README's integration steps and pre-integration status describe the
supplied package, not the current repository state; this document records the
integration. Manifest paths beginning `app/` map to repository `src/android/app/`;
all other paths are relative to this directory. Its 25 entries cover every supplied
file except the manifest itself, with verified byte counts and SHA-256 hashes.

## Android resources

- `src/android/app/src/main/res/mipmap-{mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi}/`
  contains square and round legacy PNGs at 48, 72, 96, 144, and 192 pixels.
- `mipmap-anydpi-v26/ic_launcher.xml` and `ic_launcher_round.xml` reference the
  background, foreground, and themed monochrome PNGs in `drawable-nodpi/`.
  Each adaptive layer is 1024 × 1024 pixels, byte-identical to its source PNG here.
- Existing manifest references `@mipmap/ic_launcher` and
  `@mipmap/ic_launcher_round` are unchanged. Package IDs, flavors, signing, labels,
  and splash artwork are outside this change.
- Removed the old `drawable/ic_launcher_foreground.png` to avoid competing
  resources with the same name, and removed `values/colors.xml`, which contained
  only the now-unused old launcher background color.
- `source/` preserves the SVG/PNG masters. `play-store-512.png` is retained as
  supplied, without publishing it.

The upstream [`tools/update-icons.sh`](../../../tools/update-icons.sh) generates
Eden artwork and overwrites launcher resources. It is not a regeneration procedure
for this Babel package; do not run it to refresh these icons.

## Validation

These results apply to the commit containing this integration; PR #1 records the
exact SHA after commit and push.

**Archive and static checks:** ZIP CRC checks passed; 26 unique safe paths; all 25
manifest entries matched their supplied bytes and hashes. All 18 PNGs decoded with
valid PNG chunk CRCs and expected dimensions; all four SVGs and both adaptive XMLs
parsed. `git diff --check` flags one supplied trailing space in each of the two
color SVGs; these source bytes are deliberately preserved to retain package hashes.
Runtime adaptive PNGs equal their corresponding source exports. The
manifest references resolve, and approved original branding files are unchanged.

**Visual inspection / static simulation:** inspected the full-color master,
adaptive foreground, all square/round legacy sizes at 48–192 px, and static circle,
squircle, rounded-square, and themed previews. The complete sunset and tower are
retained. Previews use the central 72/108 of each adaptive canvas. Every nonzero
alpha pixel lies within the central 66/108-diameter safe circle: maximum distance
from canvas center is 304.96 px for the color foreground and 298.06 px for monochrome,
below the 312.89 px safe radius. These are static geometry checks, not launcher or
animation tests on Android.

**Android resource compilation/linking:** existing Android SDK build-tools 36.0.0,
AAPT2 `2.20-13193326`, and platform `android-36` successfully compiled and linked all
15 launcher resource files with an isolated validation manifest using the existing
application icon references. Compiled adaptive XML resolves all three layers,
including monochrome.

**Project resource build:** existing JDK 17.0.21+9, Gradle wrapper 8.13, AGP 8.9.1,
SDK platform 36, and configured NDK 28.2.13676358:

```sh
cd src/android
# JAVA_HOME and ANDROID_HOME point to the existing local JDK and SDK.
./gradlew :app:processMainlineReleaseResources --offline --no-daemon \
  --console=plain -Pandroid.builder.sdkDownload=false
```

Passed: 15 executed tasks, including Mainline Release resource merging, manifest
processing, and resource linking. Existing warnings: deprecated BuildConfig option,
`ApplicationVariant`, ktlint `disabledRules`, Gradle features incompatible with
Gradle 9, and SDK XML version 4 read by tooling supporting version 3. No dependencies
or host software were installed.

**Remaining acceptance gates:** full APK/native compilation, emulator/device
installation, actual launcher masking/themed behavior, animation, signing, and
physical-device acceptance were not performed. Local resource success is not a
clean hosted-CI or merge-readiness claim. Any unresolved hosted Node.js runtime
warnings remain blockers to that claim. No manual hosted workflow dispatch,
release, APK publication, or merge is part of this import.
