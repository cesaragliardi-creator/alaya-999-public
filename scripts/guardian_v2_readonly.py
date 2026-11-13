#!/usr/bin/env python3
"""ALAYA-999 Guardian v2: read-only public SHA-256 audit."""
import argparse
import datetime as dt
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO = "cesaragliardi-creator/alaya-999-public"
BASE = "https://raw.githubusercontent.com/" + REPO + "/"
HEADERS = {"User-Agent": "alaya999-guardian-v2/0.1"}

def download(ref, path):
    parts = [urllib.parse.quote(p, safe="") for p in path.split("/")]
    url = BASE + urllib.parse.quote(ref, safe="") + "/" + "/".join(parts)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.read()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", default="main", help="Branch or immutable commit SHA")
    parser.add_argument("--out", default="dist/guardian-v2-report.json")
    args = parser.parse_args()
    report = {"schema": "alaya-999-guardian-v2-report-v1",
              "checked_at": dt.datetime.now(dt.timezone.utc).isoformat(),
              "repository": REPO, "ref": args.ref,
              "reference_is_immutable": len(args.ref) == 40 and all(c in "0123456789abcdef" for c in args.ref.lower()),
              "note": "Manifest hashes are claims from the selected ref, not an independent trust anchor.",
              "files": [], "counts": {}}
    try:
        raw = download(args.ref, "integrity-manifest.json")
        report["manifest_sha256"] = hashlib.sha256(raw).hexdigest()
        manifest = json.loads(raw)
        entries = manifest["files"]
        if not isinstance(entries, dict):
            raise ValueError("Manifest files is not an object")
        for path, expected in sorted(entries.items()):
            entry = {"path": path, "expected_sha256": expected}
            if (not isinstance(path, str) or path.startswith("/") or ".." in path.split("/")
                    or not isinstance(expected, str) or len(expected) != 64
                    or any(c not in "0123456789abcdef" for c in expected.lower())):
                entry["status"] = "invalid_manifest_entry"
            else:
                try:
                    data = download(args.ref, path)
                    entry["actual_sha256"] = hashlib.sha256(data).hexdigest()
                    entry["status"] = "match" if entry["actual_sha256"] == expected else "mismatch"
                except urllib.error.HTTPError as e:
                    entry["status"] = "missing" if e.code == 404 else "error"
                    entry["http_status"] = e.code
                except (urllib.error.URLError, TimeoutError, OSError) as e:
                    entry["status"] = "error"
                    entry["error_type"] = type(e).__name__
            report["files"].append(entry)
            report["counts"][entry["status"]] = report["counts"].get(entry["status"], 0) + 1
    except (ValueError, KeyError, json.JSONDecodeError, urllib.error.URLError, OSError) as e:
        report["fatal_error"] = type(e).__name__ + ": " + str(e)[:200]
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"counts": report["counts"], "fatal_error": report.get("fatal_error"), "report": str(output)}))
    return 1 if report.get("fatal_error") or any(k != "match" for k in report["counts"]) else 0

if __name__ == "__main__":
    raise SystemExit(main())
