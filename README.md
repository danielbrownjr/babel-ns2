# Babel NS2

**In defiance of the Christian God.**

Babel NS2 is an independently maintained, downstream distribution of [Eden NS2](https://github.com/Vivsi1/Eden-NS2-Android), initially focused on **Android ARM64** and Snapdragon/Adreno devices. It is not a rename of the official Eden application, an official Eden release, or a branch awaiting upstream acceptance.

Babel intends to incorporate selected upstream improvements while controlling its own Android application identity, packaging, release decisions, and project direction. The original Eden installation and its user data must remain untouched.

> **Development status (November 2026):** Babel's independent Android APK, package isolation, and device startup are still being developed. No verified Babel APK or successful AYN Odin 3 execution is claimed here. The screenshots and game compatibility observations inherited from Eden NS2 are **upstream evidence, not Babel Android test results**.

## Relationship and provenance

The code lineage is **yuzu/Citra → Eden → Eden NS2 Android → Babel NS2**. Babel's immediate source was [Vivsi1/Eden-NS2-Android](https://github.com/Vivsi1/Eden-NS2-Android). The broader [Eden project](https://git.eden-emu.dev/eden-emu/eden) and its predecessors retain credit for their respective work. Upstream code, documentation, notices, and license obligations are not rebranded as original Babel work.

Babel will maintain its own `main` branch and review selected upstream updates on integration branches. See [upstream and distribution policy](docs/UPSTREAM.md) and the original [upstream README](docs/README.upstream.md).

## Android direction

| | Babel NS2 | Eden / Eden NS2 |
| --- | --- | --- |
| Project governance | Independent downstream maintenance | Separate upstream projects and maintainers |
| Intended Android application ID | `dev.techbenders.babelns2` (M0 target, not yet verified in an APK) | Existing Eden package ID(s), unchanged by Babel's plans |
| Branding | Babel name and Tower of Babel identity | Retains Eden's own identity |
| Packaging and release | Babel-controlled, once validated | Upstream-controlled |
| Current device verification | Not yet established | Do not infer from Babel or vice versa |

**M0 priority:** produce a valid ARM64 Android APK that installs alongside an existing Eden installation without replacing it or importing its preferences, saves, firmware, or caches. See the [Android build notes](docs/build/Android.md), which still include inherited upstream instructions and are not yet a verified Babel build procedure.

## Branding

Babel's approved direction uses a monumental Tower of Babel / ziggurat motif, sunset palette, gold typography, and researched cuneiform artwork. The visual identity is distinct from Eden. The tagline is a project statement, not a claim about emulator capabilities or religious affiliation.

Read the [branding assets and provenance guide](docs/branding/README.md) before modifying artwork. The approved source files are currently in the project Drive and are not automatically bundled into an APK.

## Compatibility and evidence

The inherited [Eden NS2 work log](docs/ns2/NOTES.md) records prior Switch 2 experiments and limitations. Those experiments must **not** be presented as Babel-on-Android results. Babel-specific compatibility claims require reproducible logs and hardware validation.

No commercial games, keys, firmware, or copyrighted game content are distributed with Babel. Users must provide lawfully obtained material where applicable.

## Contributing and documentation

- [Babel contribution guidelines](CONTRIBUTING.md)
- [Development documentation](docs/README.md)
- [AI assistance policy](docs/policies/AI.md)
- [Coding guidelines](docs/policies/Coding.md)

## License and independence

The repository retains [GPL-3.0-or-later licensing and notices](LICENSE.txt) alongside applicable file-level and third-party notices. Babel is **not affiliated with or endorsed by Eden, Vivsi1, Nintendo, or their contributors**. Fork independence does not erase upstream authorship or license requirements.
