# HTML format

One HTML file per invocation. Tailwind and Mermaid both come from CDNs. Mermaid handles graph-shaped diagrams (sequences, data flow, dependencies); hand-built divs and inline SVG handle everything else. Mix the two: leaning on Mermaid for everything looks generic.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{one-line topic}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* small custom layer for what Tailwind doesn't cover: dashed seams, arrow heads */
      .seam { stroke-dasharray: 4 4; }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-10">
      <header>{{topic as a heading, one sentence under it}}</header>
      <section>{{the visual}}</section>
    </main>
  </body>
</html>
```

The only scripts are the Tailwind CDN and the Mermaid ESM import. The page is otherwise static.

## Rendering each sketch shape

The inline shapes in `SKILL.md` each have an HTML counterpart. Pick by the same rule: the shape that matches the point.

- **Pseudocode / whole code block** → `<pre>` inside a `rounded-lg border bg-white p-4 font-mono text-sm` card. Color the one or two lines that carry the point with a `bg-emerald-50` span.
- **Call tree / component tree** → nested boxes. Each node is a bordered `div` with its label; children sit inside with `ml-6 mt-2`. File paths and hooks go in `text-xs font-mono text-slate-500` beside the label. Give the node that answers the question a thick dark border; leave the rest thin.
- **File tree** → a `<pre>` mono tree with the `├──` characters, comments in `text-slate-500`.
- **Diff** → line by line: added lines `bg-emerald-50 text-emerald-900`, removed lines `bg-red-50 text-red-900 line-through`, unchanged lines plain. Keep the `+`/`-` gutter so it still reads as a diff.
- **Sequence / data flow / dependency graph** → Mermaid in `<pre class="mermaid">`, wrapped in a white card so it sits in the page rather than parachuted in. Use `classDef` to color the edge or node that matters.
- **Before / after, state comparison, layout comparison** → two columns, `grid md:grid-cols-2 gap-6`, each column a card with a small uppercase label (`Before`, `After`, or the state name). Columns stack on mobile.
- **Infographic** → the comparison grid plus stat tiles: `text-3xl font-semibold` number, `text-xs uppercase tracking-wider` caption.
- **Short slide deck** → one `<section>` per point, `min-h-screen snap-start flex items-center`, inside a `snap-y snap-mandatory overflow-y-scroll h-screen` container. One visual and one sentence per slide. Order the slides in the order the point unfolds.

## Style

Two modes, chosen by topic:

- **The product's own UI** (a screen, a component, a layout): reuse the product's tokens. Read them from the repo first (Tailwind config, CSS variables, theme files) and put the same colors, type scale, spacing, and component shapes on the page. Real labels, real data, so the visual reads as the product.
- **Everything else** (algorithms, call flow, file layout, architecture): editorial. `bg-stone-50` page, `text-slate-900` body, one accent (emerald or indigo), red for the problem, amber for a warning. Generous whitespace. Serif headings (`font-serif`) fit well with stone/slate.

Both modes:

- Diagrams around 320px tall, so side-by-side pairs fit without scrolling.
- Labels inside diagrams in `text-xs uppercase tracking-wider`, so they read as schematic, not as UI.
- `max-w-5xl mx-auto px-6`, and every multi-column layout collapses to one column below `md:`.
- Prose is sparse. If a diagram needs a paragraph to be understood, redraw the diagram.
