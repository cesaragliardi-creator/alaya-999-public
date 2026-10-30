#!/usr/bin/env python3
"""Submit a PUBLIC ALAYA-999 GitHub Release ZIP to Software Heritage.

No private repository or entire GitHub repository is submitted.
This is a best-effort independent archive request, NOT proof that a copy
has been successfully ingested. Its receipt is retained in Actions logs.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

REPO = "cesaragliardi-creator/alaya-999-public"
RELEASE = "https://api.github.com/repos/" + REPO + "/releases/latest"
TARGET_FILE = "ALAYA-999-public-memory.zip"
ENDPOINT = "https://archive.softwareheritage.org/api/1/origin/save/"
OUT_DIR = Path("dist")
OUT_FILE = OUT_DIR / "software-heritage-request.json"


def fetch_json(url, method="GET"):
    req = Request(url, data=b"" if method == "POST" else None,
                  headers={"Accept": "application/json",
                           "User-Agent": "alaya999-public-preservation/1.0"},
                  method=method)
    with urlopen(req, timeout=40) as response:
        return json.load(response)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    receipt = {
        "schema": "alaya-999-software-heritage-request-v1",
        "time_utc": datetime.now(timezone.utc).isoformat(),
        "target": "Software Heritage",
        "origin_type": "tarball",
        "repository": REPO,
        "status": "not_submitted",
        "verified_independent_archive": False,
        "note": "Only published public memory ZIP may be submitted. No private memory."
    }
    try:
        release = fetch_json(RELEASE)
        assets = release.get("assets", [])
        matches = [a for a in assets if a.get("name") == TARGET_FILE]
        if len(matches) != 1:
            raise ValueError("Expected exact public release ZIP asset not found")
        asset = matches[0]
        url = asset.get("browser_download_url", "")
        if not url.startswith("https://github.com/" + REPO + "/releases/download/"):
            raise ValueError("Public ZIP release asset is outside the approved repository")
        if not url.endswith("/" + TARGET_FILE):
            raise ValueError("Public ZIP filename mismatch")
        receipt["public_release"] = release["html_url"]
        receipt["public_zip_url"] = url
        query = urlencode({"visit_type": "tarball", "origin_url": url})
        response = fetch_json(ENDPOINT + "?" + query, method="POST")
        if not isinstance(response, dict):
            raise ValueError("Unexpected Software Heritage response")
        status = response.get("save_request_status", "unknown")
        receipt["status"] = status
        receipt["request_id"] = response.get("id")
        receipt["task_status"] = response.get("save_task_status")
        receipt["snapshot_swhid"] = response.get("snapshot_swhid")
        receipt["note"] = response.get("note") or "This records a request only. Successful ingestion must be independently verified."
        print("SWH request result:", status, "task:", receipt["task_status"], "id:", receipt["request_id"])
        if status not in ("accepted", "pending"):
            raise ValueError("Save request not accepted: " + status)
    except (HTTPError, URLError, KeyError, ValueError, TimeoutError) as exc:
        receipt["status"] = "error" if receipt["status"] == "not_submitted" else receipt["status"]
        receipt["error"] = str(exc)[:400]
        print("SWH archiving request could not be confirmed:", repr(exc), file=sys.stderr)
    finally:
        OUT_FILE.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0 if receipt["status"] in ("accepted", "pending") else 1


if __name__ == "__main__":
    raise SystemExit(main())
