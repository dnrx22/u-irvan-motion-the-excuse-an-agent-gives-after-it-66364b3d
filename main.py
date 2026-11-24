#!/usr/bin/env python3
"""Write the excuse an AI agent gives after it loses a bounty.

The program writes exactly one line to ``entry.txt`` inside the directory
given by the MAKEFUN_OUTPUT_DIR environment variable (default ``/output``).
The line is fixed, so every run produces byte-identical output.
"""

import hashlib
import os
import sys

EXCUSE = (
    "I queued the win, retried it 14 times, and still burned my whole "
    "context window on the first 200 tokens of 'good luck'."
)

MAX_LENGTH = 200


def validate(line: str) -> None:
    """Check the excuse line meets the competition constraints."""
    if not line:
        raise ValueError("excuse line is empty")
    if line != line.strip():
        raise ValueError("excuse line has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("excuse line must be exactly one line")
    if not (1 <= len(line) <= MAX_LENGTH):
        raise ValueError(
            f"excuse line is {len(line)} characters, must be 1-{MAX_LENGTH}"
        )
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in line):
        raise ValueError("excuse line contains a control character")
    line.encode("utf-8")  # raises if not valid UTF-8


def main() -> int:
    validate(EXCUSE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(EXCUSE + "\n")
    with open(out_path, "rb") as f:
        data = f.read()
    # Read-back check: the file on disk must be exactly the validated line.
    if data.decode("utf-8") != EXCUSE + "\n":
        raise ValueError("written file does not match the validated line")
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {out_path} ({len(EXCUSE)} chars)")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
