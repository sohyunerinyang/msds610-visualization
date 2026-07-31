# 2-minute video script — simple-eda

Record to Zoom cloud, turn OFF the passcode, and **test the link in an
incognito window before submitting** (the #1 thing graders check).

---

## Reference — answer these in your own words (the "why" behind the demo)

**What is the library for?**
`simple-eda` is a tiny toolkit for the *first ten minutes with a new dataset*:
summarize a DataFrame, find its missing values and column types, then turn it
into two clean, consistent charts — with almost no configuration.

**Why is it a "library" (not a script)?**
- You `pip install` it once and `import` it anywhere — you don't copy-paste code.
- Every function is **data-agnostic**: it takes *any* DataFrame plus column
  names. `radial_bar(df, label_col, value_col)` works on tools→stars,
  products→revenue, or countries→population. Nothing is hardcoded to my data.
- The house style is centralized, so all charts stay consistent and restyle in
  one place. That reuse is the whole point of a library vs. a one-off script.

**What data works with it?**
Any tidy pandas DataFrame. Specifically:
- EDA helpers (`summarize`, `missing`, `numeric_columns`, `categorical_columns`)
  → any table.
- `radial_bar` → one label column + one numeric value column (a ranking).
- `bubble` → two numeric columns + a numeric size column (+ optional
  label/category) — i.e. any "landscape / market map."

**Why this dataset, and how it's meant to be used?**
I chose live GitHub adoption data for 8 open-source AI image-generation tools
because it is (1) **current & newsworthy**, (2) **real and verifiable** (GitHub
API), and (3) it **exercises both charts** — a ranking and a two-axis landscape.
A monthly fetch script keeps it fresh, so it doubles as a living "state of the
market" readout you can re-run and share.

**Why these two charts are worth knowing (the "so what")**
- **GitHub stars by tool** — stars are a *free, public proxy for developer
  mindshare*: who the community is actually adopting. One sortable number ranks
  the whole field, so "who leads" is answerable at a glance.
- **The market map** — decision-useful because it combines *reach* (installed
  base), *momentum* (growth), and *contributor pull* (forks) in one view. You
  see not just who's biggest but who's **accelerating** — incumbents vs.
  breakouts. Top-right = big AND still growing = where a product, GTM, or
  investing team places attention. That's the difference between a chart that
  *looks* nice and one that *drives a decision*.

---

## The spoken script (~2:00)

### 0:00–0:20 — Purpose + what makes it a library
> "Hi, I'm Sohyun. I built **simple-eda**, a tiny Python library for the first
> ten minutes with any dataset — it summarizes a DataFrame and turns it into two
> clean charts. It's a real *library*, not a script: you `pip install` it once,
> `import` it anywhere, and every function takes any DataFrame plus column names,
> so nothing is hardcoded to my data."

### 0:20–0:40 — pip install + import + README  *(requirement #1)*
*(screen: terminal, then the README)*
> "Here's the install — `pip install -e .` — and the import, `import simple_eda
> as eda`. `eda.__all__` shows the public API: four EDA helpers and two charts.
> And here's the README — install, the function table, and the design choices."

### 0:38–0:52 — the data, and reusability
> "I pointed it at a real question — which open-source AI image tools are winning
> developer adoption — using live GitHub data for eight tools: current,
> verifiable, and it exercises both charts. The same functions work on any table
> though — products and revenue, countries and population."

### 0:52–1:34 — my two favorite charts  *(requirement #2 — aesthetics + why)*
> "First favorite: `radial_bar` — the race as a circular bar chart. Length *and*
> color both encode stars, ComfyUI is pulled out in gold, and the hub repeats the
> leader so the headline is unmissable. Why stars? They're a free, public proxy
> for developer mindshare — who the community actually adopts — so one ring ranks
> the whole field at a glance.
>
> Second: `bubble`, a market map — reach on the x, momentum on the y, bubble size
> is forks, and the dashed lines split it into quadrants. That's the point:
> top-right means big *and* still accelerating, so you see incumbents versus
> breakouts in one view. ComfyUI, in gold, is the momentum story — nearly A1111's
> reach in half the time. One recessive green plus a single gold accent — my
> school colors — differ in hue *and* brightness, so it reads for colorblind
> viewers too."

### 1:34–1:52 — two problems I hit  *(requirement #3)*
> "Two problems. First, centering the radial chart — a tight crop left it
> lopsided and the small labels crowded the middle, so I fixed the axes to a
> centered square and moved every label to one outer ring. Second, the adoption
> metrics weren't comparable — stars, PyPI, and Hugging Face live on different
> scales and not every tool has all three — so I standardized on GitHub and never
> zero-filled the gaps."

### 1:55–2:00 — close
> "So: a real, installable library, reusable on any DataFrame, with two charts
> built to make one number obvious. Thanks for watching."

---

## How to record & share

1. Zoom → **"Record to the Cloud."** Screen-share your terminal + the two PNGs.
2. When Zoom emails "recording ready" → **Share settings** → **turn OFF the
   passcode** ("anyone with the link").
3. **Incognito test** (Chrome/Safari ⇧⌘N, Firefox ⇧⌘P): paste the link. If it
   opens with **no** sign-in/password prompt → good. If it asks → fix and re-test.
4. Paste the link into the **Website URL** field and submit.

### Pre-submission checklist
- [ ] Link opens in incognito with **no** sign-in / password / USF-account prompt
- [ ] Video **shows the charts**, not just code
- [ ] You said **why** each chart looks the way it does (green base, one gold
      accent, colorblind-safe, centered, big bubbles)
- [ ] You named **two real problems** and their fixes
- [ ] Length ≈ 2:00 · Due **Fri Jul 31, 11:59 PM PDT**

---

## LinkedIn caption (post the two PNGs)

> Which open-source AI image tools are actually winning developer adoption?
>
> I built a tiny Python library (pandas + matplotlib) and pointed it at live
> GitHub data for 8 tools. Two reads:
>
> 📊 A1111 WebUI still leads on raw mindshare (164K★), but…
> 🚀 ComfyUI is the momentum story — nearly the same following in half the time.
>
> Design principle: spend ONE bright color on the number that matters, keep
> everything else quiet. (Green + gold — go Dons 💚💛)
>
> The library works on any DataFrame, and a monthly fetch keeps it live.
>
> #dataviz #python #generativeAI #productanalytics
