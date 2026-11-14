#!/usr/bin/env python3
"""Targeted regressions for the Babel release verification and build wrapper."""

import importlib.util
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock
import zipfile

ROOT = Path(__file__).resolve().parents[3]
VERIFY = ROOT / ".ci/android/verify-apk.py"
BUILD = ROOT / ".ci/android/build.sh"
spec = importlib.util.spec_from_file_location("babel_verify_apk", VERIFY)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class SigningIdentityTests(unittest.TestCase):
    def test_valid_single_signer(self):
        verifier.verify_signing_identity(
            "Number of signers: 1\n"
            f"Signer #1 certificate SHA-256 digest: {verifier.CERTIFICATE_SHA256}\n"
        )

    def test_spoofed_digest_in_subject_is_rejected(self):
        output = (
            "Number of signers: 1\n"
            "Signer #1 certificate SHA-256 digest: " + "a" * 64 + "\n"
            "Signer #1 certificate DN: CN=Signer #1 certificate SHA-256 digest: "
            + verifier.CERTIFICATE_SHA256 + "\n"
        )
        with self.assertRaisesRegex(ValueError, "Wrong signing identity"):
            verifier.verify_signing_identity(output)

    def test_twelve_signers_not_one(self):
        output = (
            "Number of signers: 12\n"
            f"Signer #1 certificate SHA-256 digest: {verifier.CERTIFICATE_SHA256}\n"
        )
        with self.assertRaisesRegex(ValueError, "Unexpected signer count"):
            verifier.verify_signing_identity(output)

    def test_duplicate_digest_lines_rejected(self):
        line = f"Signer #1 certificate SHA-256 digest: {verifier.CERTIFICATE_SHA256}\n"
        with self.assertRaisesRegex(ValueError, "Wrong signing identity"):
            verifier.verify_signing_identity("Number of signers: 1\n" + line + line)


class ZipValidationTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.apk = Path(tmp.name) / "test.apk"

    def inspect(self):
        manifest = f"""<manifest xmlns:android="http://schemas.android.com/apk/res/android"
            package="{verifier.PACKAGE}">
            <uses-sdk android:minSdkVersion="33"/>
            <application android:label="Babel NS2">
                <provider android:authorities="{verifier.PACKAGE}.user"/>
                <provider android:authorities="{verifier.PACKAGE}.provider"/>
                <activity><intent-filter>
                    <action android:name="{verifier.PACKAGE}.LAUNCH_WITH_CUSTOM_CONFIG"/>
                </intent-filter></activity>
            </application>
        </manifest>"""
        results = [
            subprocess.CompletedProcess("apkanalyzer", 0, stdout=manifest),
            subprocess.CompletedProcess("zipalign", 0),
            subprocess.CompletedProcess("apksigner", 1),
        ]
        with mock.patch.object(verifier, "run", side_effect=results):
            return verifier.inspect(self.apk, signed=False)

    def write_apk(self, archive):
        header = bytearray(20)
        header[:6] = b"\x7fELF\x02\x01"
        header[18:20] = (183).to_bytes(2, "little")
        archive.writestr("AndroidManifest.xml", b"stubbed manifest")
        archive.writestr("lib/arm64-v8a/libyuzu-android.so", header)

    def test_duplicate_zip_entries_rejected(self):
        with zipfile.ZipFile(self.apk, "w") as archive:
            self.write_apk(archive)
            with self.assertWarnsRegex(UserWarning, "Duplicate name"):
                archive.writestr("AndroidManifest.xml", b"duplicate manifest")
        with self.assertRaisesRegex(ValueError, "^Duplicate ZIP entries$"):
            self.inspect()

    def test_malformed_zip_rejected(self):
        self.apk.write_bytes(b"not a ZIP archive")
        with self.assertRaises(zipfile.BadZipFile):
            self.inspect()

    def test_valid_zip_passes(self):
        with zipfile.ZipFile(self.apk, "w") as archive:
            self.write_apk(archive)
        result = self.inspect()
        self.assertFalse(result["signed"])
        self.assertEqual(result["bytes"], self.apk.stat().st_size)


class BuildFailureTests(unittest.TestCase):
    def run_build(self, shell, gradle_status, verifier_status):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script = root / ".ci/android/build.sh"
            script.parent.mkdir(parents=True)
            shutil.copy(BUILD, script)
            checker = root / ".ci/android/verify-apk.py"
            checker.write_text(f"import sys\nsys.exit({verifier_status})\n")
            gradle = root / "src/android/gradlew"
            gradle.parent.mkdir(parents=True)
            gradle.write_text(f"#!/bin/sh\nexit {gradle_status}\n")
            gradle.chmod(0o755)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            for tool in ("java", "apkanalyzer", "apksigner", "zipalign", "glslangValidator"):
                stub = bin_dir / tool
                stub.write_text("#!/bin/sh\nexit 0\n")
                stub.chmod(0o755)
            env = os.environ.copy()
            env["PATH"] = str(bin_dir) + os.pathsep + env["PATH"]
            env.pop("BABEL_KEYSTORE_FILE", None)
            argv = ([str(script)] if shell is None else [shell, str(script)])
            result = subprocess.run(
                argv + ["-t", "babel", "-b", "Release"],
                cwd=root, env=env, capture_output=True, text=True,
            )
            return result.returncode

    def test_failed_gradle_never_reports_success(self):
        for shell in (None, "sh", "bash"):
            with self.subTest(shell=shell):
                self.assertNotEqual(self.run_build(shell, 1, 0), 0)

    def test_failed_verifier_never_reports_success(self):
        for shell in (None, "sh", "bash"):
            with self.subTest(shell=shell):
                self.assertNotEqual(self.run_build(shell, 0, 1), 0)

    def test_successful_stub_flow(self):
        for shell in (None, "sh", "bash"):
            with self.subTest(shell=shell):
                self.assertEqual(self.run_build(shell, 0, 0), 0)


if __name__ == "__main__":
    unittest.main()
