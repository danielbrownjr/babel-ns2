# Babel NS2 development documentation

Babel is an independent downstream distribution of Eden NS2, initially concentrating on Android ARM64 and Snapdragon/Adreno compatibility. Start with the [project README](../README.md), [upstream lineage and integration policy](UPSTREAM.md), and [branding provenance](branding/README.md).

## Android and NS2 work

- [Android build guide](build/Android.md) - Babel unsigned ARM64 release workflow and APK verification; signing and device acceptance remain separate
- [Eden NS2 experimental work log](ns2/NOTES.md) - historical upstream evidence, **not Babel Android compatibility results**
- [General build instructions](Build.md) - primarily upstream
- [Dependencies](Deps.md), [CMake options](Options.md), and [cross compilation](CrossCompile.md) - inherited technical references
- [Platform caveats](Caveats.md), [debugging](Debug.md), and [driver bugs](DriverBugs.md)

## Engineering references

- [Development guidelines](Development.md)
- [Design overview](DesignOverview.md)
- [Dynarmic](dynarmic/README.md)
- [HOS kernel](HosKernel.md)
- [Settings](Settings.md)
- [CPM utilities](CPMUtil.md)

## Policies and contributor information

- [Contribution guidelines](../CONTRIBUTING.md)
- [AI assistance policy](policies/AI.md)
- [Coding guidelines](policies/Coding.md)
- [Agent instructions](../AGENTS.md)

## Inherited documentation

The [upstream Eden README](README.upstream.md) and [user handbook](user/README.md) are retained for technical context and original contributor credit. References to Eden's releases, community, services, and performance claims apply to Eden unless independently verified for Babel. Do not treat them as Babel support or distribution channels.
