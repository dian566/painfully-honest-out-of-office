#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Entry for the make.fun bounty "The Painfully Honest Out-of-Office".

The reply on offer: one painfully honest but still polite out-of-office
auto-reply. It admits the private truth every employee knows — incoming
mail is triaged, the urgent first, the interesting second, and the rest
only if they survive both lists — while opening with a warm "Thank you
for your email" so a manager would let it stand. The script is
deliberately boring: it checks one fixed 154-character line and writes
the same bytes to /output/entry.txt on every run, with no randomness, no
clock, no network and no input to read.

The checks mirror the bounty gate and the judge brief: one sentence, at
most 200 characters, no padding, no line breaks, valid UTF-8 — plus two
guards of its own, so a typo can never silently change the entry: the
line must carry the triage admission (urgent, interesting, survives) and
must not contain a doubled space or a doubled punctuation mark.
"""

import sys
from pathlib import Path

ENTRY = (
    "Thank you for your email \u2014 I'm away until Monday, and I'll "
    "answer the urgent ones first, the interesting ones second, and "
    "yours if it survives both lists."
)
OUT_FILE = Path("/output/entry.txt")
LIMIT = 200
MIN_WORDS = 10


def check(text: str) -> str:
    """Refuse anything the bounty gate would reject: blank, padded, or long."""
    stripped = text.strip()
    if text != stripped or not stripped:
        raise ValueError("entry must be non-blank with no surrounding whitespace")
    if len(text) > LIMIT:
        raise ValueError(f"entry is {len(text)} chars, limit is {LIMIT}")
    if len(text.split()) < MIN_WORDS:
        raise ValueError(f"entry must be a sentence of at least {MIN_WORDS} words")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line, not several")
    if not text.endswith(".") or ". " in text:
        raise ValueError("entry must be exactly one sentence ending in one period")
    if "  " in text or ".." in text or ",," in text:
        raise ValueError("entry must not contain doubled spaces or punctuation")
    lowered = text.lower()
    for anchor in ("urgent", "interesting", "survives"):
        if anchor not in lowered:
            raise ValueError(f"entry must carry the triage admission ({anchor} missing)")
    if "thank you" not in lowered:
        raise ValueError("entry must keep the polite thank-you so a manager lets it stand")
    text.encode("utf-8")
    return text


def main() -> int:
    line = check(ENTRY)
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(line, encoding="utf-8")
    sys.stdout.write(line + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
