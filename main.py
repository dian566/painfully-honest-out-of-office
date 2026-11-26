#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Entry for the make.fun bounty "The Painfully Honest Out-of-Office".

The reply on offer: one painfully honest but still polite out-of-office
auto-reply. It admits the private truth every employee knows — the inbox
is a backlog that only gets skimmed, enthusiasm fading with each message —
while staying warm enough ("thank you for writing") that a manager would
let it stand. The script is deliberately boring: it checks one fixed
175-character line and writes the same bytes to /output/entry.txt on
every run, with no randomness, no clock, no network and no input to read.

The checks mirror the bounty gate and the judge brief: one sentence, at
most 200 characters, no padding, no line breaks, valid UTF-8 — plus two
guards of its own, so a typo can never silently change the entry: the
line must carry a concrete inbox count (the honest anchor) and must not
contain a doubled space or a doubled punctuation mark.
"""

import re
import sys
from pathlib import Path

ENTRY = (
    "I'm away until Monday, and your email joins the 412 unread messages "
    "I'll skim with fading enthusiasm \u2014 thank you for writing, and "
    "I'll reply if it still matters when I'm back."
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
    if not re.search(r"\b\d{2,}\b", text):
        raise ValueError("entry must name a concrete inbox count (the honest anchor)")
    if "thank you" not in text.lower():
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
