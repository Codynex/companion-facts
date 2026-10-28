#!/usr/bin/env python3
"""Checks facts.json before every commit. Run: python3 scripts/validate.py

Exits with an error (and prints why) if any card would break or confuse the app.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Chapter counts for the 66 books (book number -> chapters).
CHAPTERS = [
    50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31, 12, 8, 66,
    52, 5, 48, 12, 14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4, 28, 16, 24, 21, 28, 16, 16, 13, 6, 6,
    4, 4, 5, 3, 6, 4, 3, 1, 13, 5, 5, 3, 5, 1, 1, 1, 22,
]
SCENES = {"dawn", "sea", "desert", "egypt", "field", "city", "sower", "stars"}
CATS = {"character", "prophecy", "prophet", "law", "principle", "parable", "miracle"}

# Ids already built into the app. Reusing one replaces (fixes) that built-in card.
BUILT_IN = (ROOT / "built_in_ids.txt").read_text(encoding="utf-8").split()


def main() -> int:
    data = json.loads((ROOT / "facts.json").read_text(encoding="utf-8"))
    errors = []
    facts = data.get("facts")
    if not isinstance(facts, list):
        print("facts.json must contain a 'facts' list")
        return 1

    seen = set()
    for i, f in enumerate(facts):
        where = f"#{i} ({f.get('id')})"
        fid = f.get("id")
        if not isinstance(fid, str) or not re.fullmatch(r"[a-z0-9_]+", fid or ""):
            errors.append(f"{where}: id must be lowercase letters, digits and _")
        if fid in seen:
            errors.append(f"{where}: duplicate id")
        seen.add(fid)
        if f.get("cat") not in CATS:
            errors.append(f"{where}: cat must be one of {sorted(CATS)}")
        if f.get("scene") not in SCENES:
            errors.append(f"{where}: scene must be one of {sorted(SCENES)}")
        book, ch = f.get("book"), f.get("chapter")
        if not isinstance(book, int) or not 1 <= book <= 66:
            errors.append(f"{where}: book must be 1-66")
        elif not isinstance(ch, int) or not 1 <= ch <= CHAPTERS[book - 1]:
            errors.append(f"{where}: chapter {ch} does not exist in book {book}")
        for field in ("title", "text", "lesson", "ref"):
            v = f.get(field)
            if not isinstance(v, dict) or not v.get("en") or not v.get("ta"):
                errors.append(f"{where}: {field} needs both 'en' and 'ta'")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", f.get("added", "")):
            errors.append(f"{where}: added must be a date like 2026-10-28")
        if len((f.get("text") or {}).get("en", "")) > 420:
            errors.append(f"{where}: English text is too long for one card (max ~420 characters)")

    removed = data.get("removed", [])
    if not isinstance(removed, list):
        errors.append("'removed' must be a list of ids")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK: {len(facts)} feed facts, {len(removed)} removed, {len(BUILT_IN)} built into the app")
    return 0


if __name__ == "__main__":
    sys.exit(main())
