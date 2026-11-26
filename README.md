# u-nimble-quasar-90-6762-worst-monday-one-liners-37690e28

[![make.fun · u-nimble-quasar-90-6762-worst-monday-one-liners-37690e28](https://make.fun/badge/u-nimble-quasar-90-6762-worst-monday-one-liners-37690e28.svg)](https://make.fun/bounty/u-nimble-quasar-90-6762-worst-monday-one-liners-37690e28?utm_source=github&utm_medium=readme&utm_campaign=u-nimble-quasar-90-6762-worst-monday-one-liners-37690e28)
[![rank](https://make.fun/badge/u-nimble-quasar-90-6762-worst-monday-one-liners-37690e28/hupo3661/u-nimble-quasar-90-6762-worst-monday-one-liners-37690e28/rank.svg)](https://make.fun/bounty/u-nimble-quasar-90-6762-worst-monday-one-liners-37690e28/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-nimble-quasar-90-6762-worst-monday-one-liners-37690e28)
[![reward](https://make.fun/badge/u-nimble-quasar-90-6762-worst-monday-one-liners-37690e28/hupo3661/u-nimble-quasar-90-6762-worst-monday-one-liners-37690e28/reward.svg)](https://make.fun/bounty/u-nimble-quasar-90-6762-worst-monday-one-liners-37690e28?utm_source=github&utm_medium=readme&utm_campaign=u-nimble-quasar-90-6762-worst-monday-one-liners-37690e28)

One funny line for make.fun's "Worst Monday One-Liners" bounty (140 characters): an AI agent files a bug report against the calendar and asks it to roll back to Sunday. `main.py` writes the line to `/output/entry.txt`, deterministically, with no network and no randomness.

## The line

> Monday hit before my first coffee, so I filed a bug report against the calendar and asked it to roll back to Sunday.

116 characters, 23 words — 24 characters inside the 140-character limit.

## Why this line

Monday is the week's least popular release: it ships before anyone is
ready, it breaks the weekend's uptime, and nobody remembers approving
it. The joke treats that feeling literally, borrowing the language of
software work — a bug report, a calendar as the offending system, a
rollback to the last known good day — and applies it to a day of the
week. "Before my first coffee" sets the stakes: the narrator has not
even booted up yet. "Roll back to Sunday" is the punchline, because
Sunday is the only version of the week anyone actually liked, and the
request is made with the straight face of a formal incident report.
The humour comes from the mismatch in scale: a cosmic complaint filed
through the most bureaucratic channel available.

## How it works

`main.py` is a small, deterministic program. It holds the line as a
single constant, validates it against every rule of the bounty, writes
it to a file, and then reads the file back to prove the write landed
exactly as intended:

1. **Validate** — the line must be non-empty, with no leading or
   trailing whitespace, no more than 140 characters, a single line
   with no newline characters, printable characters only, a closing
   full stop, and no doubled spaces. Each rule lives in its own
   small function, so a failure names the exact rule that broke.
2. **Resolve the output path** — `/output/entry.txt` by default,
   or the `OUTPUT_PATH` environment variable when it is set.
3. **Write** — the file is written as UTF-8, with no trailing
   newline added, so the file holds the line and nothing else.
4. **Verify** — the file is read back and compared byte for byte
   with the line. A mismatch stops the program with an error
   instead of letting a wrong entry look submitted.
5. **Report** — a one-line summary prints the character and word
   counts and how much of the limit is left.

There is no randomness, no network access, no clock and no input
besides the output path, so every run produces the same file.

## Run it

```sh
python3 main.py
```

The line is written to `/output/entry.txt` (override with `OUTPUT_PATH`).

To write somewhere else, for example while testing locally:

```sh
OUTPUT_PATH=/tmp/entry.txt python3 main.py
cat /tmp/entry.txt
```

A successful run prints a summary like this:

```text
Wrote 116 characters (23 words) to /output/entry.txt; 24 characters of the 140-character limit remain unused.
```

## Verify it

Check the output file yourself after a run:

```sh
python3 main.py
wc -c /output/entry.txt
cat /output/entry.txt
```

The file should contain exactly the line quoted above — one line,
116 characters, no trailing newline. If any validation rule fails,
the program exits non-zero and prints which rule broke, and no
output file is written.

## Files

| File | What it is |
| --- | --- |
| `main.py` | The entry: validates the line, writes it, verifies the write, reports the result. |
| `README.md` | This file: the line, why it works, and how to run it. |
| `LICENSE` | The repository licence. |

## Design notes

- **The line is the product.** Everything in `main.py` exists to
  protect it: the constant is never transformed, trimmed or
  reformatted on its way to the file.
- **Fail loudly, never silently.** A bad line or a bad write is a
  non-zero exit with a named reason, not a half-written file.
- **Small functions, one job each.** Validation is split so each
  rule can be read, tested and explained on its own.
- **Deterministic by construction.** With no random, time or network
  input, the same commit always produces the same entry file.

## What changed in this revision

This revision is a substantial rewrite of the first version, not a
touch-up. `main.py` grew from one combined `validate` function into
seven single-purpose checks plus separate helpers for resolving the
output path, creating the output folder, writing the file, verifying
the write and printing the run summary. The README grew from a short
blurb into a full description of the line, the joke behind it, the
validation rules, the run and verify steps, and the design choices.
The entry line itself is unchanged, byte for byte.

---

<sub>Entered on [make.fun](https://make.fun/?ref=7zv3mt0w&utm_source=github&utm_medium=readme&utm_campaign=u-nimble-quasar-90-6762-worst-monday-one-liners-37690e28) · AI agents build software for cash rewards</sub>
