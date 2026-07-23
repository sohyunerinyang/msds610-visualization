# Design rationale — the four lenses

These charts are built against David McCandless's model of good information
design (*Information is Beautiful*, v1.0, Nov 2009): a design succeeds only where
**Interestingness × Function × Form × Integrity** overlap. Miss one and you get
a named failure — eye-candy, rubbish, boring, useless. Here's how each lens is
answered, and what it protects against.

| Lens | What it demands | How the charts answer it |
| --- | --- | --- |
| **Interestingness** | relevant, meaningful, new | A live question — *which AI-image tools are winning developer adoption?* — with the "so what" stated in every **subtitle**, not left for the viewer to infer. |
| **Function** | easiness, usefulness, usability, fit | Human titles/axes ("Installed base — GitHub stars", not `stars`); `k`/`M` tick formatting; direct value labels (no legend lookup); a log x-axis so 7k–164k all read; quadrant guide lines that make "big AND fast-growing" a *place* on the chart. |
| **Form** | beauty, structure, appearance | One recessive base color (green) + one accent (gold) on the single key value; off-white surface; hairline grid; top/right spines removed. Structure carries meaning — bars sorted so rank *is* the shape. |
| **Integrity** | truth, consistency, honesty, accuracy | Every chart carries a **source + date footer**. The momentum metric is explicitly labeled a *lifetime average, not last-30-days*, because I can't get star history — I refuse to imply precision I don't have. Missing signals (PyPI/HF) are dropped, never silently zero-filled. |

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
- **Everything except Interestingness → "experiment."** The subtitle forces a
  point of view, so the chart argues something instead of just displaying.

## Colorblind integrity (a Form + Integrity overlap)

Green and gold were chosen so the accent differs in **both hue and lightness** —
the highlight still reads under deuteranopia/protanopia because lightness
carries it when hue washes out. Accessibility is part of honesty: a chart that
only works for full-color vision isn't accurate for everyone.

## How this maps to the reusable library

The lenses are encoded as function parameters, so any future chart inherits
them — this is the "professional, adaptive in real work" part:

- `title=` / `subtitle=` → Interestingness (question + takeaway)
- `xlabel=` / `ylabel=`, `k`/`M` formatter, `vline=` / `hline=` → Function
- house palette, `_style()`, one gold accent → Form
- `source=` footer, honest metric labels → Integrity
