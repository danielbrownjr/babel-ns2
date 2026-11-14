# Contributing to Babel NS2

Babel NS2 is an independent downstream Android-first distribution of Eden NS2. Contributions here are directed to **Babel**, not automatically to Eden or any other upstream project.

## Before contributing

- Read [Babel's project identity and current status](README.md) and [upstream relationship](docs/UPSTREAM.md).
- Follow the [coding guidelines](docs/policies/Coding.md), [AI assistance policy](docs/policies/AI.md), and [repository agent instructions](AGENTS.md).
- Retain copyright, SPDX, license, and third-party notices from upstream or contributed work.
- Avoid unrelated core refactors during focused Android packaging work.

## Scope and evidence

The immediate milestone is a separately installable Android ARM64 application with package-specific storage, providers, and updater behavior. Please distinguish source inspection from a compiled APK, and a compiled APK from successful testing on real hardware.

When reporting a problem, include the exact commit, variant, device/driver if relevant, reproduction steps, and sanitized logs. Do not upload firmware, cryptographic keys, game dumps, personal data, or credentials.

## Contributions and proposals

Use this repository's [issues](https://github.com/danielbrownjr/babel-ns2/issues) for Babel-specific bugs and feature proposals. Keep pull requests focused and explain verification performed and remaining gaps. Work on feature branches; integration of upstream changes should be reviewed independently before reaching Babel `main`.

Contributions to Eden or the Eden NS2 Android project must follow **their own** current policies and submission process. Babel's AI policy does not override policies of external destinations.

Babel has no advertised donation program, official community chat, or release channel in this document. Historical Eden contact and donation links in inherited documentation are **Eden's**, not Babel's.

## Licensing

Contributions must be compatible with the repository's GPL and relevant component licenses. Preserve legitimate attribution and include license/source information for imported code and assets.
