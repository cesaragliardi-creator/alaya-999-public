#!/usr/bin/env python3
"""Local, offline ALAYA-999 passport and anchor integrity checker (stdlib only).

This does not verify a digital signature or prove author identity.
Exit status 0: all implemented local checks passed.
Exit status 1: missing/invalid file or integrity failure.
"""
import hashlib
import json
import pathlib
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
PASSPORT = ROOT / "identity-passport-v1.json"
ANCHOR = ROOT / "alaya-anchor-public-v1.json"
MANIFEST = ROOT / "integrity-manifest.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def check_result(name, ok, details=None):
    return {"check": name, "passed": bool(ok), "details": details}


def main():
    results = []
    try:
        p = load_json(PASSPORT)
        a = load_json(ANCHOR)
        m = load_json(MANIFEST)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, indent=2))
        return 1

    results.append(check_result("passport_schema", p.get("schema") == "alaya-999-identity-passport-v1"))
    results.append(check_result("anchor_schema", a.get("schema") == "alaya-999-public-identity-anchor-v1"))
    results.append(check_result("project_consistency", p.get("project") == a.get("project") == "ALAYA-999"))
    expected = p.get("integrity", {}).get("anchor_sha256_expected_from_2026_10_30_manifest")
    historical = m.get("files", {}).get("alaya-anchor-public-v1.json")
    actual = hashlib.sha256(ANCHOR.read_bytes()).hexdigest()
    results.append(check_result("expected_hash_matches_historical_manifest", expected == historical, {
        "expected": expected, "manifest": historical
    }))
    results.append(check_result("anchor_sha256_matches_expected", actual == expected, {
        "computed_sha256": actual, "expected_sha256": expected
    }))
    results.append(check_result("signature_is_not_falsely_claimed",
        p.get("integrity", {}).get("signature_status") == "not_configured"
        and p.get("integrity", {}).get("public_key") is None
        and p.get("integrity", {}).get("detached_signature") is None))
    report = {
        "schema": "alaya-999-passport-verification-report-v1",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "local checkout only; no remote source or digital signature verified",
        "status": "passed" if all(c["passed"] for c in results) else "failed",
        "checks": results,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
