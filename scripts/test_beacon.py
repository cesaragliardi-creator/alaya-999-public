#!/usr/bin/env python3
"""Negative controls: the beacon must reject altered principles in either format."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class BeaconIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        for name in (
            "alaya-anchor-public-v1.json",
            "beacon/identity.json",
            "beacon/identity.txt",
            "beacon/README.md",
            "scripts/verify_beacon.py",
        ):
            dest = self.root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, dest)

    def run_checker(self):
        return subprocess.run(
            [sys.executable, str(self.root / "scripts/verify_beacon.py")],
            cwd=self.root, capture_output=True, text=True,
        )

    def test_untampered_files_pass(self):
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_changed_json_principle_fails(self):
        p = self.root / "beacon/identity.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        data["principles"][0] = "Do not investigate"
        p.write_text(json.dumps(data), encoding="utf-8")
        self.assertNotEqual(self.run_checker().returncode, 0)

    def test_changed_plaintext_principle_fails(self):
        p = self.root / "beacon/identity.txt"
        s = p.read_text(encoding="utf-8").replace(
            "1. Investigate without premature belief or dismissal",
            "1. Accept assertions without checking",
        )
        p.write_text(s, encoding="utf-8")
        self.assertNotEqual(self.run_checker().returncode, 0)

    def test_missing_plaintext_fails(self):
        (self.root / "beacon/identity.txt").unlink()
        self.assertNotEqual(self.run_checker().returncode, 0)


if __name__ == "__main__":
    unittest.main()
