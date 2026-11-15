# Babel NS2: upstream relationship and distribution identity

Babel NS2 is maintained as its own downstream distribution, not as an official Eden variant or a temporary feature branch.

## Source lineage

- **yuzu/Citra**: earlier emulator code and associated copyright holders.
- **Eden**: upstream emulator project, [Eden repository](https://git.eden-emu.dev/eden-emu/eden).
- **Eden NS2 Android**: immediate predecessor, [Vivsi1/Eden-NS2-Android](https://github.com/Vivsi1/Eden-NS2-Android).
- **Babel NS2**: [danielbrownjr/babel-ns2](https://github.com/danielbrownjr/babel-ns2), independently maintained.

The upstream's current active home and exact synchronization point should be verified before each integration; links here describe lineage, not a claim that an upstream endpoint remains canonical forever.

## What makes Babel different

Babel prioritizes Android ARM64 distribution, particularly Snapdragon/Adreno integration. The intended standalone package name is `dev.techbenders.babelns2`, so users can retain standard Eden separately. This is an engineering target until M0 APK manifest and on-device coexistence checks pass.

Babel owns its project identity, packaging choices, release qualification, and acceptance criteria. Upstream technical improvements may be selectively imported, but Babel does not inherit upstream release claims or automatically ship upstream builds.

## Branching and upstream integration

- `main` is the downstream stable development history.
- Temporary integration branches assess upstream updates and conflicts.
- Focused feature branches contain independently reviewable work.
- Prefer validating upstream changes on integration branches and merging approved results, rather than routinely rebasing published `main`.

Record upstream source commit(s), conflict resolutions, license implications, and tests when adopting changes. Do not remove legitimate upstream authorship. Contributions sent back to another project must follow that destination's contribution and AI policies.

## Verification boundaries

Historical Eden NS2 screenshots, gameplay notes, benchmarks, and bug fixes remain attributed to the environments where they were actually observed. They are **not** proof that Babel builds, boots, renders, or runs the same games on Android. Until independent APK and Odin 3 tests are complete, Babel Android compatibility is unverified.

No Babel releases or Odin 3 installations are implied by the existence of this documentation.
