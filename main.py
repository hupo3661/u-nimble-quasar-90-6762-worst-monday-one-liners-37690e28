#!/usr/bin/env python3
"""Worst Monday One-Liners - write one funny line to /output/entry.txt.

The entry itself is a single sentence: Monday arrives before the first
coffee, so the narrator files a bug report against the calendar and asks
for a rollback to Sunday. The joke works because it treats an ordinary,
dreaded weekday exactly like a broken software release: something went
live too early, somebody should have caught it in review, and the only
sensible fix is to revert to the last known good day.

This module is deliberately small and deterministic:

* No randomness, no network access and no clock are involved, so every
  run produces byte-for-byte the same output file.
* The line is validated before anything is written, and the file is
  read back and compared after writing, so a bad line or a failed
  write can never pass silently.
* The output path defaults to ``/output/entry.txt`` and can be
  overridden with the ``OUTPUT_PATH`` environment variable, which is
  how the grading harness points the entry at its own output folder.

Usage::

    python3 main.py
    OUTPUT_PATH=/tmp/entry.txt python3 main.py

Exit status is 0 on success. Any validation or write problem stops
the program with a clear message on standard error and a non-zero
exit status.
"""

import os
import sys

# The entry line. This exact text is the submission: it must not be
# edited, reworded, re-punctuated or re-wrapped. Everything else in
# this file exists only to check it and to deliver it unchanged.
LINE = "Monday hit before my first coffee, so I filed a bug report against the calendar and asked it to roll back to Sunday."

# The competition limit for this bounty, in characters.
LIMIT = 140

# Where the line goes when OUTPUT_PATH is not set.
DEFAULT_OUTPUT_PATH = "/output/entry.txt"

# The only encoding the entry ever uses.
ENCODING = "utf-8"


def check_non_empty(line: str) -> None:
    """Reject a line that is empty or contains only whitespace.

    An empty entry is not a joke and not a submission, so fail loudly
    instead of writing an empty file that looks like success.
    """
    if not line.strip():
        raise SystemExit("Invalid line: entry must be non-empty.")


def check_no_surrounding_whitespace(line: str) -> None:
    """Reject leading or trailing whitespace around the line.

    Stray spaces would change the submitted text without changing
    what a reader sees, so the check keeps the file byte-identical
    to the LINE constant above.
    """
    if line != line.strip():
        raise SystemExit(
            "Invalid line: entry must not have leading or trailing whitespace."
        )


def check_length(line: str) -> None:
    """Reject a line longer than the competition limit.

    The limit counts every character, including spaces and the final
    full stop, so the check measures ``len(line)`` directly.
    """
    if len(line) > LIMIT:
        raise SystemExit(
            f"Invalid line: {len(line)} characters, over the {LIMIT} limit."
        )


def check_single_line(line: str) -> None:
    """Reject any newline or carriage return inside the line.

    The bounty asks for one line. An embedded newline would split
    the entry into two lines in the output file, so both ``\\n`` and
    ``\\r`` are refused.
    """
    if "\n" in line or "\r" in line:
        raise SystemExit(
            "Invalid line: entry must be a single line with no newline characters."
        )


def check_printable_text(line: str) -> None:
    """Reject control characters other than the ones already refused.

    The line is plain printable English text. A stray control
    character (a tab, a bell, an escape) would be invisible in most
    editors but would still be part of the submission, so the check
    refuses every character that is not printable.
    """
    for character in line:
        if not character.isprintable():
            raise SystemExit(
                "Invalid line: entry must contain only printable characters."
            )


def check_ends_with_full_stop(line: str) -> None:
    """Require the line to end with a full stop.

    The entry is one complete sentence, and the full stop is part of
    its rhythm: the request to roll back to Sunday lands as a flat,
    formal demand rather than a trailing thought.
    """
    if not line.endswith("."):
        raise SystemExit(
            "Invalid line: entry must end with a full stop."
        )


def check_no_double_spaces(line: str) -> None:
    """Reject two spaces in a row inside the line.

    A doubled space is almost always a typo, and it would spend two
    of the 140 characters on nothing. The entry line is written with
    single spaces throughout, so this check guards the exact text
    against an accidental extra space during any future edit.
    """
    if "  " in line:
        raise SystemExit(
            "Invalid line: entry must not contain two spaces in a row."
        )


def validate(line: str) -> None:
    """Run every entry check, in a fixed order.

    The checks are split into small functions so that a failure names
    exactly which rule broke, instead of hiding behind one large
    conditional. The order is deliberate: emptiness first, then shape
    (whitespace, length, single line), then content (printable text
    and the closing full stop).
    """
    check_non_empty(line)
    check_no_surrounding_whitespace(line)
    check_length(line)
    check_single_line(line)
    check_printable_text(line)
    check_ends_with_full_stop(line)
    check_no_double_spaces(line)


def describe_line(line: str) -> dict:
    """Summarise the line for the run report printed on success.

    Returns the character count, the word count and how many
    characters of the limit are still unused. Nothing here changes
    the line; it only measures it for the human running the script.
    """
    return {
        "characters": len(line),
        "words": len(line.split()),
        "characters_remaining": LIMIT - len(line),
    }


def resolve_output_path() -> str:
    """Decide where the entry file goes.

    ``OUTPUT_PATH`` wins when it is set to a non-empty value; an
    empty value falls back to the default instead of failing on an
    empty path. A ``~`` at the start is expanded so a home-relative
    path works as a user would expect.
    """
    override = os.environ.get("OUTPUT_PATH", "")
    if override.strip():
        return os.path.expanduser(override)
    return DEFAULT_OUTPUT_PATH


def ensure_parent_directory(output_path: str) -> None:
    """Create the output folder if it does not exist yet.

    The grading harness may point at a fresh ``/output`` folder, so
    the parent directory is created (including any missing parents)
    rather than assuming it is already there.
    """
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def write_entry(line: str, output_path: str) -> None:
    """Write the line to the output file, exactly as given.

    The file is written as UTF-8 with no trailing newline appended:
    the submitted text is the line and nothing else. Writing through
    a single ``write`` call keeps the operation atomic enough for a
    one-line file and avoids any chance of a half-written line.
    """
    with open(output_path, "w", encoding=ENCODING) as handle:
        handle.write(line)


def verify_written_file(line: str, output_path: str) -> None:
    """Read the file back and confirm it matches the line exactly.

    A write that silently truncated or altered the text would be
    worse than a crash, because the wrong entry would look submitted.
    The read-back comparison turns that silent failure into a loud
    one, with the mismatch reported instead of ignored.
    """
    with open(output_path, encoding=ENCODING) as handle:
        written = handle.read()
    if written != line:
        raise SystemExit(
            "Write verification failed: entry file content does not match the line."
        )


def report_success(line: str, output_path: str) -> None:
    """Print a short human-readable summary of the successful run.

    The summary names the output file and the line's size, so a
    runner can confirm at a glance that the right file was written
    and that the line fits its limit, without opening the file.
    """
    summary = describe_line(line)
    print(f"Wrote {summary['characters']} characters "
          f"({summary['words']} words) to {output_path}; "
          f"{summary['characters_remaining']} characters of the "
          f"{LIMIT}-character limit remain unused.")


def main() -> int:
    """Validate the line, write it out, verify it and report success.

    Returns 0 on success. Validation and verification failures raise
    ``SystemExit`` with a message, which Python turns into a non-zero
    exit status, so a failing entry never pretends to have worked.
    """
    validate(LINE)
    output_path = resolve_output_path()
    ensure_parent_directory(output_path)
    write_entry(LINE, output_path)
    verify_written_file(LINE, output_path)
    report_success(LINE, output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
