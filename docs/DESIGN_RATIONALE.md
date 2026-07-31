# Design rationale — the four lenses

These charts are built against David McCandless's model of good information
design (*Information is Beautiful*, v1.0, Nov 2009): a design succeeds only where
**Interestingness × Function × Form × Integrity** overlap. Miss one and you get
a named failure — eye-candy, rubbish, boring, useless. Here's how each lens is
answered, and what it protects against.

| Lens | What it demands | How the charts answer it |
| --- | --- | --- |
| **Interestingness** | relevant, meaningful, new | A live question — *which AI-image tools are winning developer adoption?* The gold accent answers it at a glance; the "so what" is delivered in the README and the video narration. |
| **Function** | easiness, usefulness, usability, fit | Titles derive from friendly column names; `k`/`M` tick formatting; direct value labels (no legend lookup); the plot is centered with symmetric margins; bubbles are sized large enough to read. |
| **Form** | beauty, structure, appearance | One recessive base color (green) + one accent (gold) on the single key value; off-white surface; hairline grid; top/right spines removed. In `radial_bar`, color *and* length both encode magnitude. |
| **Integrity** | truth, consistency, honesty, accuracy | The momentum metric is a *lifetime average, not last-30-days* — stated in the README and narration, because star history isn't available and I refuse to imply precision I don't have. Missing signals (PyPI/HF) are dropped, never silently zero-filled. Attribution is kept off-chart only to honor the "smallest API" rule — never to hide it. |

## The failure modes each choice avoids

McCandless names what you get when a lens is missing. The design is a set of
defenses against those:

- **Form without Integrity → "eye-candy."** The gold accent is powerful, so it
  is *reserved* for the one true key value (leader / median). It never
  decorates.
- **Function without Form → "useless / boring."** The data is real and usable,
  but the recessive chrome and single accent keep it from being a grey wall of
  bars.
- **Interestingness without Integrity → "rubbish."** A hot topic tempts
  overclaiming. The honest "lifetime average" caveat keeps the momentum story
  truthful.
- **Everything except Interestingness → "experiment."** The title + gold accent
  force a point of view, so the chart argues something instead of just displaying.

## Colorblind integrity (a Form + Integrity overlap)

Green and gold were chosen so the accent differs in **both hue and lightness** —
the highlight still reads under deuteranopia/protanopia because lightness
carries it when hue washes out. Accessibility is part of honesty: a chart that
only works for full-color vision isn't accurate for everyone.

## How this maps to the reusable library

The lenses are baked into tiny functions (per the "design the smallest API"
rule) rather than exposed as many optional parameters:

- `highlight=` + gold accent → Interestingness (points at the answer)
- auto titles from column names, `k`/`M` formatter, big readable bubbles,
  centered layout → Function
- house palette, `_style()`, one gold accent → Form
- honest metric labels in README + narration → Integrity
