"""
Dedupe extracted skills JSON files.

Keeps only the newest file per resume ID (based on timestamp in filename)
and moves older files to an archive directory. Safe by default with a
`--dry-run` option.

Usage:
    python scripts/dedupe_extracted_skills.py --path data/extracted_skills --archive-dir data/extracted_skills/archive --dry-run
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from datetime import datetime
from typing import Dict, List, Tuple


TIMESTAMP_RE = re.compile(r"(?P<resume_id>.+?)_skills_(?P<ts>\d{8}_\d{6})\.json$", re.IGNORECASE)


def parse_args():
    p = argparse.ArgumentParser(description="Dedupe extracted_skills JSON files")
    p.add_argument("--path", default="data/extracted_skills", help="Directory with extracted skill files")
    p.add_argument("--archive-dir", default=None, help="Directory to move older files into (default: <path>/archive)")
    p.add_argument("--dry-run", action="store_true", help="Show actions without moving files")
    p.add_argument("--delete-old", action="store_true", help="Permanently delete older files instead of archiving (use with caution)")
    return p.parse_args()


def extract_resume_id_and_ts(filename: str) -> Tuple[str | None, datetime | None]:
    m = TIMESTAMP_RE.search(filename)
    if m:
        resume_id = m.group("resume_id")
        ts_str = m.group("ts")
        try:
            ts = datetime.strptime(ts_str, "%Y%m%d_%H%M%S")
            return resume_id, ts
        except Exception:
            return resume_id, None

    # Not matching pattern — return Nones
    return None, None


def scan_directory(path: str) -> Dict[str, List[Tuple[datetime | None, str]]]:
    by_resume: Dict[str, List[Tuple[datetime | None, str]]] = {}

    for name in os.listdir(path):
        full = os.path.join(path, name)
        if not os.path.isfile(full):
            continue

        resume_id, ts = extract_resume_id_and_ts(name)

        # If no resume_id from filename, attempt to read JSON `resume_id` field
        if resume_id is None:
            try:
                with open(full, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                    rid = data.get("resume_id")
                    if rid:
                        resume_id = rid
            except Exception:
                pass

        # Final fallback: use filename as resume id (so each file treated separately)
        if resume_id is None:
            resume_id = name

        by_resume.setdefault(resume_id, []).append((ts, full))

    return by_resume


def choose_newest(entries: List[Tuple[datetime | None, str]]) -> Tuple[Tuple[datetime | None, str], List[Tuple[datetime | None, str]]]:
    # Choose the entry with the latest timestamp; if timestamps missing, use file mtime
    best = None
    best_ts = None

    resolved: List[Tuple[datetime, str]] = []
    for ts, path in entries:
        if ts is None:
            mtime = datetime.fromtimestamp(os.path.getmtime(path))
            resolved.append((mtime, path))
        else:
            resolved.append((ts, path))

    resolved.sort(key=lambda x: x[0], reverse=True)
    newest = resolved[0]
    others = resolved[1:]

    # convert back to original tuple form (datetime, path)
    return (newest, others)


def main():
    args = parse_args()
    base_path = args.path
    archive_dir = args.archive_dir or os.path.join(base_path, "archive")

    if not os.path.isdir(base_path):
        print(f"Path not found: {base_path}")
        return

    os.makedirs(archive_dir, exist_ok=True)

    grouped = scan_directory(base_path)

    total_kept = 0
    total_moved = 0
    actions: List[str] = []

    for resume_id, entries in grouped.items():
        if len(entries) <= 1:
            total_kept += len(entries)
            continue

        newest, others = choose_newest(entries)
        total_kept += 1

        # newest is a tuple (datetime, path)
        kept_path = newest[1]
        for ts, path in others:
            rel_name = os.path.basename(path)
            dest = os.path.join(archive_dir, rel_name)
            if args.dry_run:
                actions.append(f"Would move: {path} -> {dest}")
            else:
                if args.delete_old:
                    os.remove(path)
                    actions.append(f"Deleted: {path}")
                else:
                    shutil.move(path, dest)
                    actions.append(f"Moved: {path} -> {dest}")
                total_moved += 1

    # Summary
    print("Dedupe summary:")
    print(f"  Files scanned groups: {len(grouped)}")
    print(f"  Kept files: {total_kept}")
    print(f"  Older files moved/deleted: {total_moved}")

    if args.dry_run:
        print("\nDry-run actions:")
        for a in actions:
            print("  ", a)


if __name__ == "__main__":
    main()
