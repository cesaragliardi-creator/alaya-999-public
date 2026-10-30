#!/usr/bin/env python3
"""One-time public archive request for the ALAYA-999 GitHub Pages home.

This is a best-effort PUBLIC web page capture through Internet Archive's
Save Page Now. It never accesses private memory or uses a credential.
Acceptance is NOT evidence of successful capture: an archive URL or status
must be independently checked before any milestone is marked complete.
"""
from __future__ import annotations
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

PUBLIC_URL = "https://cesaragliardi-creator.github.io/alaya-999-public/"
ENDPOINT = "https://web.archive.org/save/" + PUBLIC_URL
REPORT_PATH = Path("dist/wayback-public-page-request.json")


def main() -> int:
    report = {
        "schema": "alaya-999-wayback-request-v1",
        "requested_utc": datetime.now(timezone.utc).isoformat(),
        "target": PUBLIC_URL,
        "status": "unverified",
        "archived_capture_verified": False,
        "privacy": "Only public homepage; no private memory, Google Drive or private GitHub.",
        "warning": "Save Page Now archives a single page; it is not a full bundle mirror.",
    }
    try:
        req = Request(ENDPOINT, headers={
            "User-Agent": "ALAYA-999-public-preservation/1.0 (+https://github.com/cesaragliardi-creator/alaya-999-public)",
            "Accept": "text/html,application/json,*/*",
        })
        with urlopen(req, timeout=48) as response:
            final_url = response.geturl()
            status = response.status
            _ = response.read(2048)
        report["http_status"] = status
        report["response_url"] = final_url
        if re.match(r"^https://web\.archive\.org/web/\d{14}/https://cesaragliardi-creator\.github\.io/alaya-999-public/?$", final_url):
            report["status"] = "capture_url_received"
            report["capture_url"] = final_url
        else:
            report["status"] = "submitted_but_not_verified"
        print("WAYBACK_REQUEST_STATUS=" + report["status"])
        print("WAYBACK_RESPONSE_URL=" + final_url)
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        report["status"] = "request_failed"
        report["error"] = str(exc)[:300]
        print("WAYBACK_REQUEST_FAILED=" + str(exc), file=sys.stderr)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if report["status"] == "capture_url_received" else 1


if __name__ == "__main__":
    raise SystemExit(main())
