# Android: Babel NS2 release workflow

This preserves the Android build and external signing procedure used on
2026-11-14. It uses the existing Gradle/CMake project, not a replacement build
system. The reproducible target is `babelRelease`: `dev.techbenders.babelns2`,
label **Babel NS2**, ARM64 only, minimum Android API 33. Upstream Mainline remains
`dev.eden.eden_emulator`; the Java/Kotlin namespace and JNI symbols stay unchanged.

## Source and prerequisites

The original successful build was based on
`34ae209250c41fdd185ea1a04e12e32f31802ea2` **plus five uncommitted packaging
files**. There is no single historical commit SHA for that complete input.
[The evidence record](android-release-evidence.json) contains those five file
hashes, exact command, versions, artifact hashes and report links. This branch
preserves those files byte-for-byte. The original icons were used in that APK.

For a clean checkout while this PR is pending:

```sh
git clone https://github.com/danielbrownjr/babel-ns2.git
cd babel-ns2
git switch --track origin/build/android-release-workflow
```

Inspect the actual branch/head before building. `main` at the recorded baseline
has no Babel flavor; neither does branding PR #1 by itself. There are no Git
submodules or `.gitmodules` at that baseline. Native vendored sources are in-tree;
Gradle/Maven and CPM fetch additional dependencies over the network. See
[CPMUtil](../CPMUtil.md). Do not substitute unrelated desktop build dependencies.

The successful host was Ubuntu **26.04.1 LTS**, **x86_64**, four logical CPUs,
with a user-local toolchain. Ubuntu 24.04 is the existing hosted workflow's runner,
not the verified local host. Required tools must already be provisioned; this
workflow does not install packages, accept licenses, change shell startup files,
configure the NAS, or access a device.

| Component | Recorded version / role |
| --- | --- |
| Java | Eclipse Temurin JDK 17.0.21+9, including `java` and `keytool` |
| Gradle | 8.13, downloaded by the checked-in wrapper |
| Android Gradle Plugin / Kotlin plugin | 8.9.1 / 1.9.20, selected by existing Gradle files |
| SDK platform | `platforms;android-36`, revision 2 |
| SDK build tools | 35.0.0 and 36.0.0 installed; 36.0.0 used for explicit APK inspection/signing |
| NDK | `28.2.13676358` / r28c, Clang 19.0.1 |
| CMake / Ninja | SDK CMake 3.31.5 / its Ninja 1.10.2 |
| Android command-line tools | 23.0, delegating to Android CLI 1.1.16919734 |
| Platform tools | 37.0.1; not needed to install anything during a build |
| Shader tools | glslang 16.2.0 and SPIR-V tools 2026.1 |
| Other host tools | Git, Python 3.8+, tar/ZIP utilities; existing make/GCC/G++/pkg-config were available |

The exact historical Gradle-resolved build-tools selection was not separately
logged; having SDK 36 inspection tools does not prove Gradle used that binary.
No separate Vulkan SDK installation was used for this Android build. Target
Vulkan headers, libraries and other bundled dependencies come through the existing
CMake/CPM configuration; host shader tools must be on `PATH`. Optional missing
RenderDoc support was not a fatal error.

Set `JAVA_HOME` to JDK 17 and `ANDROID_HOME` to your SDK. Set `ANDROID_SDK_ROOT`
consistently if present. Add the JDK `bin`, installed command-line-tools `bin`,
SDK `build-tools/36.0.0`, SDK `cmake/3.31.5/bin`, and host shader-tool directories
to `PATH`. SDK licenses and packages must be ready before building. The historical
package-manager invocation selected:

```sh
sdkmanager --sdk_root="$ANDROID_HOME" \
  'platform-tools' 'platforms;android-36' \
  'build-tools;35.0.0' 'build-tools;36.0.0' \
  'ndk;28.2.13676358' 'cmake;3.31.5'
```

This is a provisioning reference, not a step performed automatically by the
build script. `sdkmanager --licenses` was also invoked historically; tools 23
reported that option unnecessary. `sdkmanager` now emits a delegation/deprecation
notice; `android sdk list` was used to inspect the installed packages. The original
installation was outside the repository, with verified vendor downloads and
user-local extraction of the shader/ZIP tools. Its machine-specific activation
script is intentionally not a checkout prerequisite.

## Build an unsigned Babel release

From the repository root:

```sh
.ci/android/build.sh -t babel -b Release
```

The Babel branch of the existing script runs the historically successful command:

```sh
cd src/android
CMAKE_BUILD_PARALLEL_LEVEL=2 ./gradlew :app:assembleBabelRelease \
  --no-daemon --max-workers=2 --console=plain --stacktrace \
  '-Dorg.gradle.jvmargs=-Xmx4g -XX:MaxMetaspaceSize=1g -Dfile.encoding=UTF-8'
```

It then runs the unsigned APK verifier. It does not build an AAB, decode an
upstream keystore, run an installer, or sign an APK. `BABEL_KEYSTORE_FILE` must be
unset for this path; a configured signing key fails before Gradle starts. Babel
rejects nightly, debug, ccache and custom-CMake modes in this preserved wrapper;
use a separately reviewed direct Gradle invocation for other configurations.
**Do not pass `-r`: the legacy script uses that flag to enable upstream updates.**
Other script targets (`standard`, `legacy`, `optimized`, `chromeos`) retain their
existing APK/AAB path and behavior; `--help` describes the actual options.

Expected unsigned output, relative to the repository root:

```text
src/android/app/build/outputs/apk/babel/release/app-babel-release-unsigned.apk
src/android/app/build/outputs/apk/babel/release/output-metadata.json
```

No debug or unrelated signing identity is accepted as a Babel release. The
Gradle Babel flavor has no release-key fallback, disables the native updater and
startup update checks, and removes the install-packages permission through its
manifest overlay. Debug build types still exist for development and use the
inherited debug signing configuration; they are not this release workflow.

AGP shared native compilation under `RelWithDebInfo` while packaging the Android
`babelRelease` variant. Do not interpret that native directory name as a debug
APK: inspect generated `BuildConfig`, merged manifest and the actual output.
The Android build includes NS2 services, Ampere shader translation, ARM64 NCE,
Vulkan renderer and the linked `libyuzu-android.so`.

## Verify output without installation

```sh
python3 .ci/android/verify-apk.py --unsigned \
  src/android/app/build/outputs/apk/babel/release/app-babel-release-unsigned.apk
python3 .ci/android/verify-apk.py --signed /path/to/returned-signed.apk
```

Python uses only the standard library and calls `apkanalyzer`, `zipalign` and
`apksigner` from `PATH`. It checks ZIP CRC, package/label/API, non-debuggable status,
provider authorities and custom action, absence of shared UID/install permission,
linked ARM64 ELF libraries, ZIP alignment and explicit signed/unsigned status.
Signed mode requires the retained Babel certificate fingerprint below and verifies
v2/v3; an unsigned APK, debug signer or unrelated release key fails signed mode.
It prints SHA-256, size and inspected identity; no keys are accessed.

Inspect Gradle's `app/build/outputs/logs/manifest-merger-babel-release-report.txt`
and manifests under `app/build/intermediates` if resource or manifest checks fail.
A build error or signature failure is not installation acceptance.

## External NAS signing (requires separate authorization)

The dedicated Babel PKCS12 key remains on the NAS, alias `babelns2`, RSA-4096,
subject `CN=Babel NS2`, 10,000-day certificate validity. Its certificate SHA-256 is:

```text
5e7392d71e02eb15b8f2a5ba8aab70c2e20dfbfe3d3099d7734d2ef69f6400bf
```

Keep the existing identity. Do not regenerate it, substitute TLS keys or debug
keys, copy it into this checkout, or upload it with artifacts. The private signing
directory and key/password files were protected as 0700/0600. An independently
verified off-NAS recovery backup was not established by the original session.

The historical process was: inspect the existing NAS access and tools; stage the
unsigned APK, checksum-verified JDK 17 archive and SDK 36 `apksigner.jar`; verify
input hashes on the NAS; sign there; export only the public certificate; return
APK/certificate/signing metadata; verify hashes, signatures and unchanged ZIP
payload on the development host. The NAS used a user-local JDK, not a new Docker
service. Tool staging and one-time key generation were manually orchestrated;
the saved local helper was pinned to the original APK's version/hash and is not
a generic new-build command. This PR does not repeat staging or key generation.

For an authorized signing operation, an operator with the existing protected
paths can use this mechanism **on the NAS**, with placeholders resolved privately:

```sh
java -jar "$APKSIGNER_JAR" sign \
  --ks "$EXISTING_BABEL_KEYSTORE" --ks-key-alias babelns2 \
  --ks-pass "file:$PROTECTED_PASSWORD_FILE" \
  --v1-signing-enabled false --v2-signing-enabled true \
  --v3-signing-enabled true --v4-signing-enabled false \
  --debuggable-apk-permitted false --out "$NEW_SIGNED_APK" "$UNSIGNED_APK"
java -jar "$APKSIGNER_JAR" verify --verbose --print-certs "$NEW_SIGNED_APK"
java -jar "$APKSIGNER_JAR" verify --verbose --min-sdk-version 24 "$NEW_SIGNED_APK"
```

Use a new output filename, verify the unsigned input hash before signing, and
compare the returned artifact with the NAS result. For this PKCS12 key, let the
key password default to the store password: passing the same single-line password
file twice caused an EOF failure in the first attempt. Do not put the password
itself in arguments, logs or documentation. The extra verifier minimum-API option
exercises v2 as well as v3; it does not lower the APK's actual minimum API 33.
Direct Gradle signing inputs (`BABEL_KEYSTORE_FILE`, `BABEL_KEYSTORE_PASS`,
`BABEL_KEY_ALIAS`, optional `BABEL_KEY_PASS`) remain supported, but were not the
historically used process and are deliberately excluded from the wrapper.

## Evidence, warnings and scope

The [recorded signed APK](https://drive.google.com/file/d/1paoMbxBuSR5hPOoZO2RlCnHRPOcaz_ej/view),
[original report](https://drive.google.com/file/d/1Uq08Hc84anoDZExl54_WMt0PZtivKvBz/view),
and [checksums](https://drive.google.com/file/d/1QaGrjD3uoGgtmYd2zbm8YGe2SNufjJY0/view)
were uploaded and downloaded with byte equality checks. Future authorized Babel
artifact/report delivery uses the existing
[Babel-NS2 folder](https://drive.google.com/drive/folders/1pAPSHrcF9uXdAyVkypuM5OVREr0O-KDn).
The user subsequently reported Odin 3 installation and expected initial startup.
That is historical, user-reported physical evidence; no game dump/boot, captured
device log or device validation of a later source commit follows from it.

Recorded warnings include Gradle/AGP/CMake deprecations, deprecated BuildConfig and
ApplicationVariant/ktlint APIs, SDK XML version mismatch, unused `YUZU_USE_CPM`,
native signedness/format/BUILD_ID-redefinition warnings, deprecated Android APIs
and Kotlin nullable-type warnings. Gradle reports incompatibility with Gradle 9.0.
These were not silently repaired or suppressed. No bit-for-bit reproducibility is
claimed: version codes are time-derived and Maven/CPM transitive inputs are not
fully locked. Git version strings alone did not identify the uncommitted source.

The existing `.github/workflows/android.yml` builds Mainline, not Babel, on pushes.
It was not changed or manually dispatched. At initial inspection there were no
runs. Checkout/setup-java/setup-gradle/upload-artifact v4 action metadata selects
Node 20; deprecation/runtime acceptance needs inspection on an authorized run and
is unresolved. A green job alone would not establish clean CI or merge readiness.

[Branding PR #1](https://github.com/danielbrownjr/babel-ns2/pull/1) at
`4d9959f60f04d13c4aa9a799ffd80b72cdd26ac9` changes icons, branding and project
policies/docs, not these five packaging files. This branch imports none of its
artwork or commits. The resource paths remain the existing launcher references,
so the two diffs do not overlap; combined-head resource/device acceptance must
still be recorded separately. Installing, signing, publishing and merging require
separate authorization; this build helper performs none of them.
