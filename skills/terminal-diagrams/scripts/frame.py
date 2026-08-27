#!/usr/bin/env python3
"""Build a perfectly aligned, colored blueprint frame for chat replies.

Usage (build a frame):
    python3 frame.py --title "CI TIME BY STAGE" <<'EOF'
    build      `██████████████████████`   210s
    tests      `██████████`                96s
    EOF

The output is prose-mode markdown: paste it VERBATIM into the reply,
outside any fence. Markdown consumes the `backticks` (theme accent color)
and **stars** (bold); every multi-space run is hidden inside a codespan so
alignment survives markdown's whitespace collapsing; every line but the
last ends with a two-space hard break.

Frame style: exact-fit width (slack split evenly), solid | sides on every
row including blanks, uncolored ┌ ┐ └ ┘ corners, accent [ TITLE ] band
with a 2-space gap on each side.

Modes:
    --box       build an inner box from stdin rows: accent ┌ ┐ └ ┘
                corners aligned with the | sides, dashes inset two
                columns. Output is raw content rows — indent/prefix them
                as needed and paste them into the main call's stdin.
    --check     read a finished diagram, verify one display width
    --width N   force total width, rounded up to odd

Content conventions (main call and --box):
    `run` -> accent    **run** -> bold    both zero-width in the render
    ---   -> spaced-dash separator        empty line -> blank padded row
Backticks go tightly around visible characters, never around padding.
"""
import argparse
import sys
import unicodedata

MARGIN = 3
GAP = 2  # spaces between the [ TITLE ] band and the border dashes


def dw(s: str) -> int:
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in s)


def vw(s: str) -> int:
    """Visible width: backticks and ** are consumed by markdown."""
    return dw(s.replace("`", "").replace("**", ""))


def dashes(n: int) -> str:
    return ("- " * n)[:n]


def prose_wrap(line: str) -> str:
    """Wrap every run of 2+ plain spaces in a codespan (codespan interiors
    are preserved verbatim by markdown and spaces have no glyph, so the
    coloring is invisible). Keeps one plain space next to an existing
    codespan so backtick runs never touch."""
    out, i, n = [], 0, len(line)
    while i < n:
        c = line[i]
        if c == "`":
            j = line.find("`", i + 1)
            j = n - 1 if j == -1 else j
            out.append(line[i:j + 1])
            i = j + 1
            continue
        if c == " ":
            j = i
            while j < n and line[j] == " ":
                j += 1
            run = j - i
            if run >= 2:
                lk = 1 if i > 0 and line[i - 1] == "`" else 0
                rk = 1 if j < n and line[j] == "`" else 0
                core = run - lk - rk
                if core >= 1:
                    out.append(" " * lk + "`" + " " * core + "`" + " " * rk)
                else:
                    out.append(" " * run)  # both sides touch codespans
            else:
                out.append(" " * run)
            i = j
            continue
        out.append(c)
        i += 1
    return "".join(out)


def layout(rows, width, title_need=0):
    """Exact-fit total width (odd, never truncating), symmetric left pad."""
    content_max = max((vw(r) for r in rows if r.strip() and r != "---"), default=0)
    need = content_max + 2 * MARGIN + 2
    total = max(width or 0, need, title_need)
    total += 1 - total % 2
    lpad = MARGIN + (total - need) // 2
    return content_max, total, lpad


def body_rows(rows, content_max, inner, lpad):
    def row(s=""):
        return "|" + " " * lpad + s + " " * (inner - lpad - vw(s)) + "|"
    out = []
    for r in rows:
        if r == "---":
            out.append(row(dashes(content_max)))
        elif not r.strip():
            out.append(row())
        else:
            out.append(row(r))
    return out, row


def build_frame(rows, title=None, width=None):
    t = f"[ {title} ]" if title else ""
    content_max, total, lpad = layout(rows, width, dw(t) + 2 * GAP + 12 if title else 0)
    inner = total - 2
    top = "┌ " + dashes(total - 4) + " ┐"
    if title:
        seg = dw(t) + 2 * GAP
        s = (total - seg) // 2
        top = top[:s] + " " * GAP + "`" + t + "`" + " " * GAP + top[s + seg:]
    body, row = body_rows(rows, content_max, inner, lpad)
    out = [top, row()] + body + [row(), "└ " + dashes(total - 4) + " ┘"]
    out = [prose_wrap(l) for l in out]
    return [l + "  " if k < len(out) - 1 else l for k, l in enumerate(out)]


def build_box(rows, width=None):
    content_max, total, lpad = layout(rows, width)
    inner = total - 2
    body, _ = body_rows(rows, content_max, inner, lpad)
    top = "`┌`" + "  " + dashes(total - 6) + "  " + "`┐`"
    bot = "`└`" + "  " + dashes(total - 6) + "  " + "`┘`"
    return [top] + body + [bot]


def check(lines):
    lines = [l.rstrip() for l in lines if l.strip()]
    widths = {}
    for i, l in enumerate(lines, 1):
        widths.setdefault(vw(l), []).append(i)
    if len(widths) == 1:
        print(f"OK: {len(lines)} lines, width {next(iter(widths))}")
        return 0
    print("MISALIGNED:")
    for w, idxs in sorted(widths.items()):
        print(f"  width {w}: lines {idxs}")
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title")
    ap.add_argument("--width", type=int)
    ap.add_argument("--box", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    rows = [l.rstrip() for l in sys.stdin.read().rstrip("\n").splitlines()]
    if args.check:
        sys.exit(check(rows))
    out = build_box(rows, args.width) if args.box else build_frame(rows, args.title, args.width)
    print("\n".join(out))
    bad = {vw(l.rstrip()) for l in out}
    if len(bad) != 1:
        print(f"INTERNAL WIDTH ERROR: {sorted(bad)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
