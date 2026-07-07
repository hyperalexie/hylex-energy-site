This is a handoff prompt — paste everything below into a fresh Claude Code session opened at this project folder.

---

# Design polish pass: Hylex Energy Consulting website

## Context

This is a static marketing site (no build step, no framework — plain HTML/CSS/JS) for Hylex Energy Consulting, positioned as "an integrated industrial project solution provider" organized around five capabilities. It was functionally built and shipped over two prior sessions, and now needs a **design-focused polish pass** — the content, structure, and copy are correct and should NOT be rewritten; this pass is about how it *looks*.

Read `README.md` first for file structure and deployment details.

## Site map

- `index.html` — homepage hub (hero, 5-capability grid, global presence, why-Hylex, contact teaser)
- `engineering.html`, `procurement.html`, `fabrication.html` — capability pages describing Hylex's own capability/capacity (do NOT name the underlying manufacturing partners — this is deliberate, see "Do not touch" below)
- `oilfield.html` — short hub linking to two sub-pages:
  - `oilfield-equipment.html` (water treatment tech)
  - `oilfield-parts.html` (dissolvable bridge plug products)
- `project-intelligence.html` — **ScopePlex mini-site**, intentionally a completely separate design system (see below)
- `about.html`, `contact.html` — company pages
- `assets/styles.css` — shared stylesheet for all pages except `project-intelligence.html`
- `assets/nav.js` — mobile nav toggle
- `assets/img/` — real photography extracted from company decks and partner websites (not stock photos — see "Do not touch")

## Three things to work on

### 1. General visual polish
Typography rhythm, spacing consistency, color balance, and imagery treatment across all 9 shared-design-system pages (everything except `project-intelligence.html`). Current palette: `--green:#00A651`, `--orange:#F0A24B`, `--ink:#111417`, `--dark:#15181c`, `--gray:#5a6470`, backgrounds `--bg:#fff` / `--bg-soft:#f5f8f6`. Look for: inconsistent vertical spacing between sections, card padding/shadow inconsistencies, whether the orange/green swash graphic in hero sections still feels intentional at every viewport, and whether the numbered-badge/stats/hub-card components (`.step`, `.stat`, `.hub-card` in `assets/styles.css`) feel like one coherent system or ad-hoc.

### 2. Known weak spots to specifically address
- On `fabrication.html`, the "Core Business" grid has 2 cards with real photos (Steel Fabrication, Pipe Spools, Pressure Vessel) and 2 cards with **no image** ("Miscellaneous Steel Products", "Project Engineering & Management") — these currently look visually orphaned next to their photographed siblings. No matching stock/extracted photo exists for these two; decide whether to source one, use an icon/illustration treatment instead, or redesign the grid so text-only cards don't look like a downgrade.
- The homepage's 5-capability grid: 4 cards have real photos, the 5th (Project Intelligence/ScopePlex) intentionally uses a dark branded chip instead — confirm this reads as an intentional design choice rather than an inconsistency, or propose a better way to visually unify the 5th card with its siblings.
- `fabrication.html`'s world-map image (`assets/img/fabrication-world-map.jpg`) is a cropped screenshot from a PDF deck — it has real text labels that become illegible on mobile (this is currently accepted because the hub-card content below it duplicates the same info in readable text, but check whether a lighter-weight custom map treatment would look more native to the web than an embedded PDF crop).
- Nav "Capabilities" dropdown currently lists Engineering / Procurement / Fabrication / Oilfield Solutions (+ indented Equipment / Parts sub-links) / Project Intelligence as plain text links in a basic dropdown menu — consider whether this needs icons, descriptions, or a richer mega-menu treatment given it's now 7 destinations deep.

### 3. Design system audit across the now-10-page site
Since pages were built incrementally across sessions, check for drift: are `.card`, `.hub-card`, `.stat`, `.cert-badge` etc. used consistently everywhere they logically apply, or did later pages invent slightly different one-off patterns for the same kind of content? Is heading hierarchy (`.sec-kicker` → `h2` → `.sec-sub`) applied uniformly? Are button variants (`.btn`, `.btn.ghost`, `.btn.orange`) used correctly per their intended meaning (primary/secondary/partner-CTA) everywhere, or did any page reach for the wrong variant?

## Do not touch

- **Copy/content**: the text is deliberate and reviewed by the client (Alex) across multiple rounds — don't rewrite headlines, body copy, or restructure sections unless a design change genuinely requires new copy length (in which case ask first, don't invent new claims).
- **The company-name-omission rule**: Engineering, Fabrication, and Oilfield Solutions pages deliberately never name the third-party manufacturers behind them (Feverfield, USP, AMGAIN) — they describe capability/capacity only. Procurement (Fabflow Control) and Project Intelligence (ScopePlex) deliberately DO name their brand and link out to the live product sites (fabflowcontrol.com, scopeplex.app) with a dedicated "Visit" CTA button. Do not add or remove naming on either side of this rule without checking with the user first — it was an explicit, repeated decision.
- **`project-intelligence.html`'s separate design system**: this page intentionally does NOT use `assets/styles.css`. It has its own self-contained `<style>` block matching the real design language of the live scopeplex.app (DM Sans + Newsreader italic serif accent + JetBrains Mono, cream `#FAFAF7` background, amber `#D97706` accent, dark `#111111` section). Polish this page's *own* system independently — don't merge it into the shared Hylex CSS or make it look like the rest of the site. If scopeplex.app's real design has evolved since this was built, feel free to re-check it live and update to match.
- **Mobile touch targets**: every interactive element site-wide was just brought up to a 44px minimum tap target (nav, footer, inline links). Any new/changed component must preserve this — check via `getBoundingClientRect().height >= 44` on real elements, don't just eyeball it.
- **Real imagery only**: all photos in `assets/img/` were deliberately extracted from actual company PDF decks (Hylex, USP, Fabflow, AMGAIN — still present in the project root, gitignored) or downloaded directly from fabflowcontrol.com's live site. Do not replace these with generic stock photography. If more imagery is needed, extract it from the same source decks (PyMuPDF works well for precise crops) rather than sourcing new stock images.
- **No build step**: stay plain HTML/CSS/JS. Don't introduce a framework, bundler, or preprocessor.

## Verification

Use gstack (`~/.claude/skills/gstack/browse/dist/browse`, or your preferred browser automation) to visually check every page you touch at both 375px (mobile) and 1280px (desktop), and re-run a touch-target audit (querySelectorAll('a, button') + getBoundingClientRect) on any page where you changed interactive elements. Take real screenshots before claiming a change looks better — don't assert improvement without visual evidence.
