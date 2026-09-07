#!/usr/bin/env python3
"""
update.py — AI-Assisted Game Dev Framework
Run from the repo root after dropping SESSION_END.zip there.

What it does:
  - Unpacks SESSION_END.zip
  - Writes each updated repo file to the repo root, overwriting existing files
  - Appends session_summary.txt to SESSION_LOG.csv
  - Deletes SESSION_END.zip if everything succeeded

What it does NOT do:
  - Commit anything
  - Populate git_commit_hash (Claude Code does that after the first commit)
  - Touch any file not included in the zip
"""

import sys
import zipfile
from pathlib import Path

ZIP_NAME = "SESSION_END.zip"
SUMMARY_FILE = "session_summary.txt"
SESSION_LOG = "SESSION_LOG.csv"
REPO_ROOT = Path(__file__).parent


def main():
    zip_path = REPO_ROOT / ZIP_NAME

    # Step 1 — Check zip exists
    if not zip_path.exists():
        print(f"ERROR: {ZIP_NAME} not found in repo root ({REPO_ROOT})")
        print("Drop SESSION_END.zip in the repo root and try again.")
        sys.exit(1)

    written = []
    warnings = []

    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()

        # Step 4 (early) — Confirm session_summary.txt is present before touching anything
        if SUMMARY_FILE not in names:
            print(f"ERROR: {SUMMARY_FILE} not found in {ZIP_NAME}.")
            print("The zip may be malformed. No files were written.")
            sys.exit(1)

        # Step 3 — Extract repo files
        for name in names:
            if name == SUMMARY_FILE:
                continue

            dest = REPO_ROOT / name

            if not dest.exists():
                warnings.append(name)

            dest.write_bytes(zf.read(name))
            written.append(name)

        # Step 5 — Append session_summary.txt to SESSION_LOG.csv
        summary_row = zf.read(SUMMARY_FILE).decode("utf-8").strip()

    session_log_path = REPO_ROOT / SESSION_LOG
    with session_log_path.open("a", encoding="utf-8") as log:
        log.write(f"\n{summary_row}")

    # Step 6 — Delete the zip (only reached if everything above succeeded)
    zip_path.unlink()

    # Step 7 — Print summary
    print()
    print("=== update.py complete ===")
    print()

    if written:
        print("Files written:")
        for name in written:
            tag = " (WARNING: new file — was not in repo)" if name in warnings else ""
            print(f"  {name}{tag}")

    print()
    print(f"SESSION_LOG.csv updated.")
    print(f"{ZIP_NAME} deleted.")
    print()
    print("Next step: Claude Code reviews the git diff and handles the commit.")


if __name__ == "__main__":
    main()
