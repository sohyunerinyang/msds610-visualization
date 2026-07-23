# 2-minute video script — simple-eda / The AI Image-Gen Tool Race

Target: ~2:00. Record to Zoom cloud, turn OFF the passcode, and **test the link
in an incognito window before submitting** (this is the #1 thing graders check).

---

## 0:00–0:25 — Install, import, README  *(requirement #1)*

> "Hi, I'm Sohyun. This is **simple-eda**, a small pandas + matplotlib library I
> built for fast, good-looking exploratory analysis. Let me show it working."

- Terminal: `pip install -e .`
- Then: `python -c "import simple_eda as eda; print(eda.__all__)"`
- Scroll the **README** — pause on the function tables and the "Aesthetic
  choices" section.

> "One dependency idea drives the whole look: spend your one bright color on the
> number that matters."

## 0:25–1:20 — My two favorite charts  *(requirement #2 — aesthetics)*

> "I pointed it at a real question: **which open-source AI image-generation tools
> are winning developer adoption?** I pulled live GitHub data for eight tools."

**Chart 1 — `examples/01_radial.png` (radial bar):**
> "This is `radial_bar` — the race as a circular bar chart. Length *and* color
> both encode stars, so the biggest tools read instantly; the modern leader,
> ComfyUI, is pulled out in gold. Green and gold differ in both hue and
> brightness, so the highlight still reads for colorblind viewers."

**Chart 2 — `examples/02_market_map.png` (bubble market map):**
> "This is `bubble` as a *market map*: installed base on the x-axis, log scale;
> momentum — stars per day since launch — on the y; and bubble size is forks,
> a proxy for contributor pull. Top-right is 'big and still growing fast.'
> **ComfyUI**, in gold, is the modern leader: nearly the mindshare of A1111 but
> far younger. That's the kind of one-slide read a GTM or product team acts on."

## 1:20–1:50 — Two problems I hit  *(requirement #3)*

> "**Problem one: encoding three variables without clutter.** A plain scatter
> shows two. I scaled bubble *area* to a third (forks) and split the plane with
> median guide lines, so 'big and fast-growing' becomes a place on the chart —
> readable, not a wall of dots."

> "**Problem two: the metrics weren't comparable and some were missing.** Stars,
> PyPI downloads, and Hugging Face downloads live on totally different scales,
> and not every tool publishes all three. So I standardized on one signal every
> tool exposes — GitHub — and derived a lifetime velocity from it, rather than
> faking a composite that would quietly treat missing data as zero."

## 1:50–2:00 — Close

> "So: a real, installable library, a real dataset, and charts designed to make
> one number obvious. The fetch script re-pulls the data monthly, so this stays
> current. Thanks for watching."

---

## LinkedIn caption (post the two PNGs)

> Which open-source AI image tools are actually winning developer adoption?
>
> I built a small Python library (pandas + matplotlib) and pointed it at live
> GitHub data for 8 generative-image tools. Two takeaways:
>
> 📊 A1111 WebUI still leads on raw mindshare (164K★), but…
> 🚀 ComfyUI is the momentum story — nearly the same following in half the time.
>
> Design principle I stuck to: spend ONE bright color on the number that matters,
> and keep everything else quiet. (Green + gold — go Dons 💚💛)
>
> Data refreshes monthly, so this is a living tracker. Code + charts in comments.
>
> #dataviz #python #generativeAI #productanalytics #gtm
