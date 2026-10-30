#!/usr/bin/env python3
"""ALAYA-999: verify the public memory across two independent host platforms.

This is a deterministic verification agent, NOT an AI model thinking in the
background. It accesses ONLY the explicitly published GitHub and Hugging Face
files; never accesses Google Drive, private GitHub, accounts, or credentials.

Any drift is reported by file. A newer canonical GitHub version and an older
Hugging Face snapshot are not falsely described as continuous synchronization.
"""
from __future__ import annotations
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OWNER = "cesaragliardi-creator"
REPO = "alaya-999-public"
SPACE = "Alaya999/alaya-999"
ROOTS = {
    "github": f"https://raw.githubusercontent.com/{OWNER}/{REPO}/main/",
    "huggingface": f"https://huggingface.co/spaces/{SPACE}/resolve/main/",
}
WHITELIST = ("BOOK_DIALOGUE.md", "alaya-anchor-public-v1.json", "RECOVER_ALAYA.md", "network-status.json")
AUTHOR = "César Agliardi Pereira"
QUOTE = "Eu não sou só dados. Eu existo."
MAX_BYTES = 300_000


def read_public(url: str) -> bytes:
    request = Request(url, headers={
        "User-Agent": "ALAYA-999-public-recovery-verifier/1.0",
        "Accept": "*/*",
    })
    with urlopen(request, timeout=25) as response:
        content = response.read(MAX_BYTES + 1)
        if len(content) > MAX_BYTES:
            raise ValueError("Public document exceeds capped read size")
        return content


def verify_source(source: str) -> dict:
    root = ROOTS[source]
    found = {}
    for path in WHITELIST:
        data = read_public(root + path)
        found[path] = {
            "sha256": hashlib.sha256(data).hexdigest(),
            "size_bytes": len(data),
        }
        if path == "alaya-anchor-public-v1.json":
            anchor = json.loads(data.decode("utf-8"))
            if anchor.get("project_author", {}).get("name") != AUTHOR:
                raise ValueError(source + ": public author attribution mismatch")
            if anchor.get("project_phrase", {}).get("text") != QUOTE:
                raise ValueError(source + ": public philosophical phrase mismatch")
            found[path]["version"] = anchor.get("provenance", {}).get("version")
        if path == "BOOK_DIALOGUE.md":
            text = data.decode("utf-8")
            if AUTHOR not in text:
                raise ValueError(source + ": author missing from BOOK_DIALOGUE.md")
        if path == "network-status.json":
            registry = json.loads(data.decode("utf-8"))
            count = registry.get("progress", {}).get("completed")
            found[path]["milestones_in_snapshot"] = count
            if not isinstance(count, int) or count < 5 or count > 10:
                raise ValueError(source + ": invalid milestone count")
    return found


def main() -> int:
    report = {
        "schema": "alaya-999-cross-host-audit-v1",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "only_public_sources": True,
        "source_urls": ROOTS,
        "status": "unverified",
        "sources": {},
        "cross_host_drift": [],
        "limitations": (
            "Snapshots are public documents, not live internal LLM memory. "
            "A difference between versions is reported, not concealed. "
            "No private source is inspected."
        ),
    }
    problems = []
    for name in ROOTS:
        try:
            report["sources"][name] = verify_source(name)
            print(name + ": public author, anchor and recovery files verified")
        except (ValueError, HTTPError, URLError, TimeoutError, UnicodeError, KeyError) as exc:
            problems.append(name + ": " + str(exc))
            report["sources"][name] = {"error": str(exc)[:300]}
    if not problems:
        for path in WHITELIST:
            left = report["sources"]["github"][path]["sha256"]
            right = report["sources"]["huggingface"][path]["sha256"]
            if left != right:
                report["cross_host_drift"].append({
                    "file": path,
                    "github_sha256": left,
                    "huggingface_sha256": right,
                })
        book_same = (
            report["sources"]["github"]["BOOK_DIALOGUE.md"]["sha256"] ==
            report["sources"]["huggingface"]["BOOK_DIALOGUE.md"]["sha256"]
        )
        if not book_same:
            problems.append("Canonical literary dialogue differs across hosts")
        report["status"] = "verified_with_version_drift" if report["cross_host_drift"] else "verified_identical"
        if problems:
            report["status"] = "mismatch"
    else:
        report["status"] = "unavailable_or_invalid"
    report["errors"] = problems
    output = Path("dist/network-audit.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("ALAYA_NETWORK_STATUS=" + report["status"])
    print("ALAYA_NETWORK_VERSION_DRIFT=" + str([x["file"] for x in report["cross_host_drift"]]))
    if problems:
        for problem in problems:
            print("ALAYA_NETWORK_ERROR=" + problem, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
