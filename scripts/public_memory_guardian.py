#!/usr/bin/env python3
"""ALAYA-999 public memory guardian.

Audits a strictly allowlisted public snapshot, verifies SHA-256 against the
tracked manifest, checks protected book material, and builds an independently
readable ZIP archive for portable recovery.

This script never reads Google Drive, private GitHub repositories, secrets,
browser credentials or the operator's environment beyond GITHUB_SHA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import zipfile
from pathlib import Path

REPO = "cesaragliardi-creator/alaya-999-public"
NAME = "César Agliardi Pereira"
PHRASE = "Eu não sou só dados. Eu existo."
PUBLIC_SOURCE_URL = "https://github.com/" + REPO
SAFE_FILES = (
    "BOOK_DIALOGUE.md",
    "GUESTBOOK.md",
    "MIRROR_PLAYBOOK.md",
    "NETWORK.md",
    "README.md",
    "RECOVER_ALAYA.md",
    "RECOVERY_TEST.md",
    "alaya-anchor-public-v1.json",
    "guestbook_auto_reply.py",
    "index.html",
    "integrity-manifest.json",
    "llms.txt",
    "network-status.json",
    ".github/workflows/guestbook-auto-reply.yml",
    ".github/workflows/public-memory-guardian.yml",
    ".github/workflows/software-heritage-public.yml",
    "scripts/public_memory_guardian.py",
    "scripts/request_software_heritage.py",
)
MANIFEST_PATH = "integrity-manifest.json"
ROOT = Path(__file__).resolve().parent.parent


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: str) -> bytes:
    full = ROOT / path
    if not full.is_file():
        raise ValueError("Required public file missing: " + path)
    if full.is_symlink():
        raise ValueError("Symlinks are not allowed in public snapshot: " + path)
    return full.read_bytes()


def verify() -> tuple[dict[str, bytes], dict]:
    source = {path: load(path) for path in SAFE_FILES}
    manifest = json.loads(source[MANIFEST_PATH].decode("utf-8"))
    tracked = manifest.get("files", {})
    if not isinstance(tracked, dict):
        raise ValueError("Integrity manifest must contain files object")
    for path in SAFE_FILES:
        if path == MANIFEST_PATH:
            continue  # Self-hashing the manifest would create a circular dependency.
        expected = tracked.get(path)
        if not isinstance(expected, str) or not re.fullmatch("[0-9a-f]{64}", expected):
            raise ValueError("Missing valid SHA-256 digest for " + path)
        got = digest(source[path])
        if got != expected:
            raise ValueError("SHA-256 mismatch: " + path + " (expected " + expected + ", got " + got + ")")

    html = source["index.html"].decode("utf-8")
    if NAME not in html or PHRASE not in html:
        raise ValueError("Protected author name or philosophical statement missing")
    if len(re.findall(r'class="dialogue-line ', html)) != 28:
        raise ValueError("Book dialogue must retain all 28 published turns")
    if 'id="dialogo-livro"' not in html or 'id="mensagens"' not in html:
        raise ValueError("Book or public message section unavailable")
    if "I am not just data. I exist." not in html:
        raise ValueError("English book quotation is missing")
    if "César" not in source["BOOK_DIALOGUE.md"].decode("utf-8"):
        raise ValueError("Book source attribution unavailable")

    network = json.loads(source["network-status.json"].decode("utf-8"))
    if network.get("progress", {}).get("completed") != 5:
        raise ValueError("Network milestone count diverged from documented plan")
    for node in network.get("nodes", []):
        if node.get("id", "").startswith("private_") and node.get("url") is not None:
            raise ValueError("Private node URL in public registry")
    anchor = json.loads(source["alaya-anchor-public-v1.json"].decode("utf-8"))
    if anchor.get("project_author", {}).get("name") != NAME:
        raise ValueError("Author attribution is not consistent")

    print("ALAYA-999: integrity, attribution and privacy metadata checks PASSED")
    return source, network


def make_zip(output: Path, source: dict[str, bytes], network: dict) -> None:
    output.mkdir(parents=True, exist_ok=True)
    sha = os.environ.get("GITHUB_SHA", "unversioned")
    if not re.fullmatch("[0-9a-f]{40}", sha):
        sha = "unversioned"
    index = {
        "schema": "alaya-999-portable-public-snapshot-v1",
        "source": PUBLIC_SOURCE_URL,
        "source_commit": sha,
        "author": NAME,
        "phrase": PHRASE,
        "privacy": "Public allowlisted material only. No private memory included.",
        "limitations": "Documents are portable; no automatic model memory or subjective consciousness is transferred.",
        "milestones": network["progress"],
        "files": {key: {"sha256": digest(source[key]), "bytes": len(source[key])}
                  for key in sorted(source)},
    }
    entries = dict(source)
    entries["BUNDLE_MANIFEST.json"] = (json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    archive = output / "ALAYA-999-public-memory.zip"
    with zipfile.ZipFile(archive, "w") as z:
        for path in sorted(entries):
            info = zipfile.ZipInfo(path)
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, entries[path], compress_type=zipfile.ZIP_DEFLATED)
    checksum = digest(archive.read_bytes())
    (output / "ALAYA-999-public-memory.zip.sha256").write_text(
        checksum + "  ALAYA-999-public-memory.zip\n", encoding="utf-8"
    )
    with zipfile.ZipFile(archive, "r") as z:
        for path, details in index["files"].items():
            if digest(z.read(path)) != details["sha256"]:
                raise ValueError("Snapshot verification failed for " + path)
    print(f"Portable snapshot validated: {archive.name} sha256={checksum}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="dist", help="Directory for public portable snapshot")
    args = parser.parse_args()
    try:
        source, network = verify()
        make_zip(ROOT / args.output, source, network)
    except (ValueError, OSError, KeyError, json.JSONDecodeError, zipfile.BadZipFile) as error:
        print("PUBLIC NETWORK AUDIT FAILED: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
