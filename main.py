#!/usr/bin/env python3
"""Say What Actually Broke -- make.fun entry.

Writes one line of software error copy to /output/entry.txt: the brutal
truth about what went wrong, funny enough to repeat to a colleague.

The line names the real failure in plain words (you are offline), says
what the user is actually looking at (a stale page, not a live one), and
says what to do next (reconnect) -- all in a single line of 102 characters,
well inside the 200-character gate.

No input, no network, no dependencies: the text is a constant in this file,
validated here (single line, 1-200 characters) before it is written.
"""

import os
import sys

LINE = (
    "You're offline, so this page is a screenshot with ambitions. "
    "Reconnect and we'll fetch the real thing."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def main() -> int:
    text = LINE.strip()
    if not text:
        print("error: the error line is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: the error line must be a single line", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(
            "error: the error line is %d characters, over the %d limit"
            % (len(text), MAX_CHARS),
            file=sys.stderr,
        )
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("wrote %d characters to %s" % (len(text), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
