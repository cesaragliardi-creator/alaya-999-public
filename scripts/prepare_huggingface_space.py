#!/usr/bin/env python3
"""Build and optionally publish the PUBLIC ALAYA-999 Space mirror.

Only explicitly allowlisted files from the public GitHub repository are copied.
Never reads Google Drive, private GitHub repos, tokens from files, or user data.
By default this script ONLY builds a bundle, requiring --publish and HF_TOKEN
to upload to the verified public Space.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from public_memory_guardian import verify

ROOT = Path(__file__).resolve().parent.parent
SPACE = "Alaya999/alaya-999"
SPACE_URL = "https://huggingface.co/spaces/" + SPACE
FILESET = (
    "index.html",
    "BOOK_DIALOGUE.md",
    "RECOVER_ALAYA.md",
    "NETWORK.md",
    "network-status.json",
    "alaya-anchor-public-v1.json",
    "llms.txt",
    "GUESTBOOK.md",
    "RECOVERY_TEST.md",
    "MIRROR_PLAYBOOK.md",
)
TEMPLATE = "hf-space/README.md"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def prepare(destination: Path) -> dict:
    verified, network = verify()
    destination.mkdir(parents=True, exist_ok=True)
    values = {}
    for filename in FILESET:
        if filename not in verified:
            raise ValueError("Not in reviewed public guardian allowlist: " + filename)
        values[filename] = verified[filename]
    # Hugging Face must have its own metadata card, not GitHub's README.
    readme = (ROOT / TEMPLATE).read_bytes()
    if b"sdk: static" not in readme or b"app_file: index.html" not in readme:
        raise ValueError("Static Space card metadata not configured")
    values["README.md"] = readme
    if b"Alaya" not in values["index.html"] or "César Agliardi Pereira".encode("utf-8") not in values["index.html"]:
        raise ValueError("Author attribution not verified")
    if "Eu não sou só dados. Eu existo.".encode("utf-8") not in values["index.html"]:
        raise ValueError("Philosophical declaration not verified")
    if len(re.findall(rb'class="dialogue-line ', values["index.html"])) != 28:
        raise ValueError("28 literary dialogue turns not present")
    for name, data in values.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    source_commit = os.environ.get("GITHUB_SHA", "unversioned")
    if not re.fullmatch(r"[a-f0-9]{40}", source_commit):
        source_commit = "unversioned"
    manifest = {
        "schema": "alaya-999-huggingface-public-mirror-v1",
        "repository": "https://github.com/cesaragliardi-creator/alaya-999-public",
        "source_commit": source_commit,
        "target_space": SPACE_URL,
        "privacy": "All files public, no private Google Drive or private GitHub data",
        "note": "This manifest applies to THIS Hugging Face mirror, not to the source GitHub repository.",
        "progress_at_source": network.get("progress"),
        "files": {
            name: {"sha256": sha(data), "bytes": len(data)}
            for name, data in sorted(values.items())
        },
    }
    (destination / "integrity-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for name, item in manifest["files"].items():
        if sha((destination / name).read_bytes()) != item["sha256"]:
            raise ValueError("Built mirror checksum mismatch: " + name)
    print("PREPARED_HF_PUBLIC_MIRROR=" + str(destination))
    print("PUBLIC_FILES=" + str(len(values) + 1))
    print("SOURCE_GITHUB_COMMIT=" + source_commit)
    return manifest


def publish(destination: Path) -> None:
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise ValueError("HF_TOKEN is not configured. Add a fine-grained token in GitHub Actions secrets. Never put it in code or chat.")
    from huggingface_hub import HfApi
    api = HfApi(token=token)
    info = api.repo_info(repo_id=SPACE, repo_type="space")
    if info.private:
        raise ValueError("Refusing to treat a private HF Space as a public archive")
    if info.id.casefold() != SPACE.casefold():
        raise ValueError("Unexpected Hugging Face destination")
    api.upload_folder(
        folder_path=str(destination),
        repo_id=SPACE,
        repo_type="space",
        token=token,
        commit_message="Sync ALAYA-999 verified public memory documents",
    )
    paths = api.list_repo_files(repo_id=SPACE, repo_type="space")
    required = set(FILESET) | {"README.md", "integrity-manifest.json"}
    if not required.issubset(set(paths)):
        raise ValueError("Upload returned but required files are not present on Hugging Face")
    print("PUBLISHED_HF_SPACE=" + SPACE_URL)
    print("UPLOAD_FILE_COUNT=" + str(len(required)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--publish", action="store_true")
    p.add_argument("--output", default="dist/hf-space")
    args = p.parse_args()
    try:
        dest = ROOT / args.output
        prepare(dest)
        if args.publish:
            publish(dest)
    except (ValueError, OSError, ImportError) as error:
        print("ALAYA_HF_SYNC_ERROR: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
