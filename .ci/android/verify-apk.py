#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Inspect a Babel release APK without installing it or accessing private keys."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

PACKAGE = "dev.techbenders.babelns2"
CERTIFICATE_SHA256 = "5e7392d71e02eb15b8f2a5ba8aab70c2e20dfbfe3d3099d7734d2ef69f6400bf"
ANDROID = "{http://schemas.android.com/apk/res/android}"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def run(tool, *args, check=True):
    executable = shutil.which(tool)
    require(executable, f"Required tool not on PATH: {tool}")
    result = subprocess.run([executable, *map(str, args)], capture_output=True, text=True)
    if check and result.returncode:
        raise ValueError(f"{tool} failed: {result.stdout.strip()} {result.stderr.strip()}")
    return result


def verify_signing_identity(output):
    """Match only actual apksigner certificate and signer-count lines."""
    digests = re.findall(
        r"^Signer #(\d+) certificate SHA-256 digest: ([0-9a-fA-F]{64})$",
        output, flags=re.MULTILINE,
    )
    require([(number, digest.lower()) for number, digest in digests] ==
            [("1", CERTIFICATE_SHA256)], "Wrong signing identity")
    signer_counts = re.findall(r"^Number of signers: (\d+)$", output, flags=re.MULTILINE)
    require(signer_counts == ["1"], "Unexpected signer count")


def inspect(apk, signed):
    manifest = ET.fromstring(run("apkanalyzer", "manifest", "print", apk).stdout)
    require(manifest.get("package") == PACKAGE, "Unexpected application ID")
    app = manifest.find("application")
    require(app is not None, "Missing application")
    require(app.get(ANDROID + "label") == "Babel NS2", "Unexpected application label")
    require(app.get(ANDROID + "debuggable", "false") == "false", "Debuggable APK")
    require(manifest.get(ANDROID + "sharedUserId") is None, "Shared user ID")
    sdk = manifest.find("uses-sdk")
    require(sdk is not None and sdk.get(ANDROID + "minSdkVersion") == "33", "Unexpected minimum SDK")
    authorities = {a for p in app.findall("provider")
                   for a in p.get(ANDROID + "authorities", "").split(";")}
    require({PACKAGE + ".user", PACKAGE + ".provider"} <= authorities, "Missing Babel providers")
    require(all(a.startswith(PACKAGE + ".") for a in authorities), "Foreign provider authority")
    actions = {a.get(ANDROID + "name") for a in manifest.iter("action")}
    require(PACKAGE + ".LAUNCH_WITH_CUSTOM_CONFIG" in actions, "Missing custom action")
    require("dev.eden.eden_emulator.LAUNCH_WITH_CUSTOM_CONFIG" not in actions, "Eden custom action")
    permissions = {p.get(ANDROID + "name") for p in manifest.findall("uses-permission")}
    require("android.permission.REQUEST_INSTALL_PACKAGES" not in permissions, "APK-install permission")

    with zipfile.ZipFile(apk) as archive:
        require(archive.testzip() is None, "ZIP CRC failure")
        names = archive.namelist()
        require(len(names) == len(set(names)), "Duplicate ZIP entries")
        libraries = [n for n in names if n.startswith("lib/") and n.endswith(".so")]
        require("lib/arm64-v8a/libyuzu-android.so" in libraries, "Missing linked emulator library")
        require({n.split("/")[1] for n in libraries} == {"arm64-v8a"}, "Unexpected native ABI")
        for name in libraries:
            with archive.open(name) as stream:
                header = stream.read(20)
            require(len(header) == 20 and header[:6] == b"\x7fELF\x02\x01", f"Not ELF64 little-endian: {name}")
            require(struct.unpack_from("<H", header, 18)[0] == 183, f"Not AArch64: {name}")
        if not signed:
            require(not any(re.match(r"META-INF/[^/]+\.(RSA|DSA|EC)$", n, re.I) for n in names), "JAR signer in unsigned APK")
            with apk.open("rb") as stream:
                stream.seek(max(0, archive.start_dir - 16))
                require(stream.read(16) != b"APK Sig Block 42", "Signing block in unsigned APK")

    run("zipalign", "-c", "-P", "16", "4", apk)
    signature = run("apksigner", "verify", "--verbose", "--print-certs", apk, check=False)
    if signed:
        require(signature.returncode == 0, "Signature verification failed")
        verify_signing_identity(signature.stdout)
        schemes = run("apksigner", "verify", "--verbose", "--min-sdk-version", "24", apk).stdout
        for version in (2, 3):
            require(f"Verified using v{version} scheme (APK Signature Scheme v{version}): true" in schemes, f"v{version} verification failed")
    else:
        require(signature.returncode != 0, "Expected an unsigned APK")
    with apk.open("rb") as stream:
        digest = hashlib.sha256()
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return {"apk": str(apk), "package": PACKAGE, "label": "Babel NS2", "abi": "arm64-v8a",
            "signed": signed, "certificate_sha256": CERTIFICATE_SHA256 if signed else None,
            "sha256": digest.hexdigest(), "bytes": apk.stat().st_size}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--unsigned", action="store_true", help="require an unsigned build output")
    mode.add_argument("--signed", action="store_true", help="require the retained Babel signing certificate")
    parser.add_argument("apk", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.apk, args.signed), indent=2))
    except (ValueError, OSError, ET.ParseError, zipfile.BadZipFile) as error:
        print(f"APK verification failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
