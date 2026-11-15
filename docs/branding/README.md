# Babel NS2 branding: identity, assets, and provenance

## Identity

**Project:** Babel NS2  
**Tagline:** *In defiance of the Christian God.*  
**Positioning:** independently maintained Android-first downstream distribution of Eden NS2  
**Visual direction:** Tower of Babel / ziggurat architecture, gold lettering and details, warm sunset colors, and researched cuneiform.

The Babel identity must be visually distinct from the Eden name, icon, and promotional assets. Preserve technical lineage and legal notices rather than using branding to imply original authorship of upstream code.

## Approved source artwork

The approved originals come from the [Babel NS2 branding folder in the personal Techbenders Drive](https://drive.google.com/drive/folders/16vHwwmSgtzQSRIqy7tp0HkHkNbraLjO5), under the Babel NS2 project folder. Byte-identical copies are tracked in [`docs/branding/assets/`](assets/). Git blob SHA-1 identifiers were checked against the retrieved originals at import.

| Source asset | Intended use |
| --- | --- |
| [`babel-ns2-branding-board-updated.png`](assets/babel-ns2-branding-board-updated.png) | Reference board and visual style |
| [`social-banner-cuneiform-master.png`](assets/social-banner-cuneiform-master.png) | Full-resolution banner master including cuneiform |
| [`github-social-preview-1280x640.png`](assets/github-social-preview-1280x640.png) | Social-preview artwork |
| [`github-social-preview-upload-under-1MB.jpg`](assets/github-social-preview-upload-under-1MB.jpg) | Size-constrained GitHub social-preview upload |

The archived subfolder contains earlier versions; do not silently replace approved current files with archived alternatives.

## Cuneiform handling

The cuneiform treatment was deliberately researched during artwork development. **Preserve the approved glyph composition and placement.** Do not substitute decorative pseudo-cuneiform or assert an alternative transcription based on visual impression alone.

The research notes, specific sign-by-sign transcription, and scholarly source list are not yet recorded in this repository. This document therefore does not claim an independently verified translation. If philological documentation is added later, record the exact intended text, Unicode/sign references, sources, and any editorial uncertainty separately from visual artwork.

## Usage rules

- The approved corrected Android icon package is integrated in the app resources. See [Android icon integration and validation](android-icons/INTEGRATION.md) for source provenance, resource mapping, checks, and remaining device/build gates.
- The social banner belongs in repository/social presentation, not embedded indiscriminately throughout UI and docs.
- Do not imply GitHub's repository social-preview **setting** has been changed simply because an image exists in Drive or in Git.
- Preserve source artwork; derive optimized exports non-destructively and record filenames, dimensions, and intended destinations.
- Keep upstream copyright and license notices intact; asset ownership and licensing terms should be established before distributing artwork inside an APK or repository release.

## M0 boundary

This guide records identity and provenance. Android icon resources now have their own [integration record](android-icons/INTEGRATION.md); this does **not** establish APK, signing, launcher/device behavior, or Odin 3 launch acceptance.
