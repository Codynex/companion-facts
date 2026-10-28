# companion-facts — daily Bible fact cards

This repository feeds the **Facts** reels in Joy's personal study companion app (Flutter, Android).
The app downloads `facts.json` from `main` (raw.githubusercontent.com) about every 6 hours and on app open.
Joy is one of Jehovah's Witnesses; the cards support his personal Bible study.

## The daily job

Each run:

1. **Fix flagged cards first.** Read open issues titled `Fix: <id>`
   (`gh issue list --repo Codynex/companion-facts --state open`). For each:
   - If the card is in `facts.json`, correct it there.
   - If the id is in `built_in_ids.txt` (a card built into the app), add a corrected entry with the
     same id to `facts.json` — a feed entry with the same id replaces the built-in card.
   - If it can't be fixed confidently, add the id to `"removed"` instead.
   - Comment on the issue with what changed, then close it.
2. **Add 7 new cards** with `"added"` set to today's date (Asia/Kolkata).
3. Run `python3 scripts/validate.py`; fix anything it reports.
4. Commit to `main` with a message like `Add 7 facts, fix 1 (2026-10-29)` and push.

## Writing a card

```json
{
  "id": "good_samaritan",            // lowercase_with_underscores, never reused
  "cat": "parable",                  // character | prophecy | prophet | law | principle | parable | miracle
  "scene": "desert",                 // dawn | sea | desert | egypt | field | city | sower | stars
  "book": 42, "chapter": 10,         // book number 1–66 and a chapter that exists (opens in the app)
  "title":  {"en": "...", "ta": "..."},
  "text":   {"en": "...", "ta": "..."},   // 1–3 sentences, under ~420 characters
  "lesson": {"en": "...", "ta": "..."},   // one practical sentence
  "ref":    {"en": "Luke 10:29-37", "ta": "லூக்கா 10:29-37"},
  "added": "2026-10-28"
}
```

Rules:

- **Accuracy first.** Only state what the cited verses actually say. No speculation, no added details, no legends.
- **Own words only.** Never copy wording from jw.org, the New World Translation or any publication. Short, plain retellings.
- **Respectful, in harmony with what Joy believes.** Use "Jehovah" for God's name. Keep lessons practical and
  in line with Bible principles; avoid doctrinal claims beyond what the verse plainly says.
  Dates, where needed, follow the chronology in *Insight on the Scriptures* (e.g. 607 B.C.E., 539 B.C.E., 29 C.E.).
- **Tamil**: natural, everyday Tamil as Tamil Witnesses speak it (யெகோவா, கடவுளுடைய அரசாங்கம், ஞானஸ்நானம், சபை).
  Book names as in `built-in` cards (e.g. ஆதியாகமம், மத்தேயு). Use கி.மு./கி.பி. for dates.
- **No repeats.** Check every existing id and title in `facts.json` and `built_in_ids.txt`; don't retell a story
  already covered unless it's a clearly different angle.
- **Variety.** Rotate through all seven categories over the week. Prefer people, events and teachings not yet covered —
  minor characters, lesser-known laws, parables, miracles, fulfilled prophecies, practical principles.
- Pick a `scene` that fits: sea (water, boats, storms), desert (wilderness, night, tents), egypt (Egypt, Nile),
  field (farming, harvest, shepherds), city (cities, kings, temples, prisons), sower (growth, teaching),
  stars (night, visions, prophecy), dawn (hope, prayer, new beginnings).

Character cards whose id matches a character in the app (e.g. `noah`, `ruth`, `daniel`) also unlock that
character in the app's collection — reuse those exact ids only for the first card about that person.
