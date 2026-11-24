#!/usr/bin/env python3
"""Say What Actually Broke -- make.fun entry.

Writes one line of software error copy to /output/entry.txt: the brutal
truth about what went wrong, funny enough to repeat to a colleague.

The line names the real failure in plain words (you are offline), says
what the user is actually looking at (a stale page, not a live one), and
says what to do next (reconnect) -- all in a single line of 102 characters,
well inside the 200-character gate.

No input, no network, no dependencies: the text is a constant in this file,
validated here (single line, 1-200 characters) before it is written, and
written atomically. `python3 main.py --check` validates and prints the line
without writing anything.
"""

import os
import sys
import tempfile

LINE = (
    "You're offline, so this page is a screenshot with ambitions. "
    "Reconnect and we'll fetch the real thing."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def validate(text: str) -> str:
    """Return the entry text, or fail loudly if it breaks the gate."""
    text = text.strip()
    if not text:
        raise ValueError("the error line is empty")
    if "\n" in text or "\r" in text:
        raise ValueError("the error line must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "the error line is %d characters, over the %d limit"
            % (len(text), MAX_CHARS)
        )
    return text


def write_entry(path: str, text: str) -> None:
    """Write the text atomically, so a crash never leaves half a line."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".entry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def main(argv) -> int:
    try:
        text = validate(LINE)
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    if "--check" in argv:
        # Validate and report only: no file is written.
        print("ok: %d characters, single line" % len(text))
        print(text)
        return 0
    write_entry(OUTPUT_PATH, text)
    print("wrote %d characters to %s" % (len(text), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
