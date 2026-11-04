#!/usr/bin/env python3
"""Checks quiz.json before every commit. Run: python3 scripts/validate_quiz.py"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODES = {"who", "book", "basics"}


def main() -> int:
    data = json.loads((ROOT / "quiz.json").read_text(encoding="utf-8"))
    qs = data.get("questions")
    if not isinstance(qs, list):
        print("quiz.json must contain a 'questions' list")
        return 1
    errors, seen = [], set()
    for i, q in enumerate(qs):
        where = f"#{i} ({q.get('id')})"
        qid = q.get("id")
        if not isinstance(qid, str) or not re.fullmatch(r"q_[a-z0-9_]+", qid):
            errors.append(f"{where}: id must look like q_lowercase_words")
        if qid in seen:
            errors.append(f"{where}: duplicate id")
        seen.add(qid)
        if q.get("mode") not in MODES:
            errors.append(f"{where}: mode must be one of {sorted(MODES)}")
        if not (isinstance(q.get("q"), dict) and q["q"].get("en") and q["q"].get("ta")):
            errors.append(f"{where}: q needs 'en' and 'ta'")
        opts = q.get("options")
        if not isinstance(opts, list) or len(opts) != 4 or not all(isinstance(o, dict) and o.get("en") and o.get("ta") for o in opts):
            errors.append(f"{where}: needs exactly 4 options, each with 'en' and 'ta'")
        elif len({o["en"] for o in opts}) != 4:
            errors.append(f"{where}: options must be different")
        if not isinstance(q.get("answer"), int) or not 0 <= q["answer"] <= 3:
            errors.append(f"{where}: answer must be 0-3")
        if not q.get("ref"):
            errors.append(f"{where}: ref (scripture) is required")
        src = q.get("src", "")
        if not (src.startswith("https://wol.jw.org/") or src.startswith("https://www.jw.org/")):
            errors.append(f"{where}: src must be a wol.jw.org or www.jw.org link")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", q.get("added", "")):
            errors.append(f"{where}: added must be a date like 2026-11-04")
    if not isinstance(data.get("removed", []), list):
        errors.append("'removed' must be a list of ids")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK: {len(qs)} quiz questions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
