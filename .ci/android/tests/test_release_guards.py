#!/usr/bin/env python3
"""Targeted regressions for the Babel release verification and build wrapper."""

import importlib.util
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest

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


class BuildFailureTests(unittest.TestCase):
    def run_build(self, shell, gradle_status, verifier_status):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script = root / ".ci/android/build.sh"
            script.parent.mkdir(parents=True)
            shutil.copyfile(BUILD, script)
            script.chmod(0o755)
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
