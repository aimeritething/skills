---
name: terminal-diagrams
description: Draw a colored blueprint schematic inline in the chat reply — bar chart, small table, flow, or nested-box diagram. Use when an answer hinges on comparing quantities, a pipeline/flow, a cost/latency breakdown, or nested structure, or when the user asks for a diagram or chart in the terminal. Not for documents, PRs, mermaid, or image requests.
---

# Terminal Diagrams

Markdown tables and mermaid don't render as visuals in a terminal. This
skill draws colored blueprint schematics directly in the chat reply:
`scripts/frame.py` builds every frame so alignment is never hand-counted,
and the output is pasted verbatim into the reply **outside any fence** —
Claude Code's markdown renderer consumes the backticks and stars, leaving
accent-colored runs and bold with no visible syntax.

Chat-only: pasted anywhere else (a file, PR, doc) the markup degrades into
literal backticks — documents get a markdown table or mermaid instead. If
Bash is unavailable, answer in prose; the markup is not hand-buildable.

## Workflow

1. **Draft content rows only** — the text inside the frame, columns
   aligned with spaces. Wrap each run to color in `backticks` and each
   run to bold in **stars**; both are zero-width in the final render. A
   line of exactly `---` becomes a spaced-dash separator; an empty line a
   blank row.
   - Backticks go tightly around visible characters (`` `████` ``), never
     around padding — the script owns all padding.
   - Two colored runs need at least one space between them.
2. **Pipe through the script** (in this skill's directory):

   ```bash
   python3 <skill-dir>/scripts/frame.py --title "CI TIME" <<'EOF'
   **build**    `██████████`   210
   tests    `█████`         96
   `deploy`   `██`            42
   EOF
   ```

   It adds the `┌ ┐ └ ┘` frame, the centered accent `[ TITLE ]` band,
   margins, and line-end hard breaks; width fits the content exactly
   (`--width N` forces a total width). Every multi-space run is hidden
   inside a codespan so markdown preserves the alignment.
3. **Paste the output verbatim, directly into the reply as prose — NOT
   inside a code fence** (a fence would show the backticks literally).
   The output is width-checked by the script: one call, done. Never
   re-count, re-verify, or write your own checker.

## The palette

The renderer offers exactly three layers (raw ANSI is stripped; hues
follow the user's theme):

- `backticks` → the theme accent color. Best on `█` bars, key values,
  status words — and the script itself spends it on the `[ TITLE ]` band
  and inner-box corners.
- **stars** → bold. Best on the row the reader should see first.
- Everything else renders in the default foreground — labels and borders
  stay plain so the colored runs pop.

## Content rules

- **Single-width characters only**: ASCII plus `▁▂▃▄▅▆▇█ ▶ ◀ ┌ ┐ └ ┘`.
  CJK, emoji, and tabs are double-width or variable in most terminal
  fonts and destroy alignment — if the conversation is in Chinese, keep
  labels inside the diagram in English/ASCII and explain them in the
  surrounding prose (在图外用中文解释).
- **Tables**: text columns left-aligned, numeric columns right-aligned on
  a fixed column, ≥3 spaces between columns — alignment does the
  separating. A `---` separator under the header and above any Total row.
- **Sparse is the style**: dashes spaced (`- - -`), never solid runs.
  Keep content within ~56 columns so the frame stays ≤64 — wider risks
  wrapping in split terminals.

## Visual language

Examples below show the rendered shape with the markup stripped so it is
visible here; real output comes from the script and carries the markup.

**Bar charts** — horizontal `█` bars (accent) scaled to the longest
value, value right-aligned after the bar:

```
┌ - - - - -   [ CI TIME BY STAGE ]  - - - - - - ┐
|                                               |
|   build      ██████████████████████   210s    |
|   typecheck  ████████████             118s    |
|   tests      ██████████                96s    |
|   install    ████                      42s    |
|                                               |
└ - - - - - - - - - - - - - - - - - - - - - - - ┘
```

**Tables** — header, separator, rows, bolded Total:

```
┌ - -   [ CI PIPELINE COST ]  - - - ┐
|                                   |
|   Stage          Time     Share   |
|   - - - - - - - - - - - - - - -   |
|   install         42s        8%   |
|   build          210s       42%   |
|   - - - - - - - - - - - - - - -   |
|   Total          ~8m       100%   |
|                                   |
└ - - - - - - - - - - - - - - - - - ┘
```

**Flows** — dashed arrows `- - - - ▶` between stages; labels go on the
line *below* the thing they name, aligned to its starting column. Tiny
bar glyphs (`▂▃▂▄▂`, accent) can stand in for "a quantity":

```
┌ - - - - -   [ AI IS AN AMPLIFIER ]  - - - - - - ┐
|                                                 |
|   ▂▃▂▄▂  - - - - ▶  AI  - - - - ▶  ▄▆▄█▆▄       |
|   your taste                       amplified    |
|                                                 |
└ - - - - - - - - - - - - - - - - - - - - - - - - ┘
```

Stack multi-stage pipelines vertically with a `|` / `▼` spine when they
don't fit on one line — never exceed the frame width.

**Nested boxes** — `--box` builds an inner box whose `┌ ┐ └ ┘` corners
render accent, dashes inset to align with the sides. Build the innermost
box first, prefix/indent its lines (a `◀ - ▶` run marks a gap or inset),
feed the result to the next `--box`, and finally to the main call; a
formula or takeaway line sits below the boxes, terms vertically aligned:

```
┌ - - - - -  [ NESTED RADII ]   - - - - - ┐
|                                         |
|   ┌  - - - - - - - - - - - - - - -  ┐   |
|   |   outer   16px                  |   |
|   |         ┌  - - - - - - - -  ┐   |   |
|   |   ◀ - ▶ |   inner   12px    |   |   |
|   |         └  - - - - - - - -  ┘   |   |
|   |   inset    4px                  |   |
|   └  - - - - - - - - - - - - - - -  ┘   |
|                                         |
|      inner = outer - inset              |
|      12px  =  16px -   4px              |
|                                         |
└ - - - - - - - - - - - - - - - - - - - - ┘
```

## When NOT to use this

- Plain prose answers, one-liners, code explanations — a frame with
  nothing structural inside is noise, not polish.
- The user asks for mermaid, an image, or a markdown table — give them
  that format.
- Inside source files, commit messages, or docs — markdown table or
  mermaid there.

The diagram supplements the answer, it doesn't replace it: lead with the
direct answer in prose, drop the schematic where it sharpens
understanding, and keep it to one or two frames per response.
