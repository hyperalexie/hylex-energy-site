# hylexenergy.com, award standard rebuild

Alex, 2026-10-13: "品質標準以 awwwards、webby awards、FWA 獲得獎項的程度為目標，透過自我檢查，反覆自行提升品質，直到達到該品質標準為止。"

## Baseline measured 2026-10-13
- Jury rubric (Awwwards): Design 40, Usability 30, Creativity 20, Content 10. SOTD ~8.0.
- Self score today: ~5.5. Usability and content pass, design and creativity fail.
- Named failures: raster logo with swoosh clipping "Energy"; Inter only, no display face;
  every section the same centred container and rhythm; zero motion; unedited photos in rounded
  cards, mixed colour temperature; default energy green.
- Strength to protect: 321 KB, 10 requests, TTFB 77 ms, FCP 308 ms. Award winners ship 4 to 8 MB.

## The idea
The program line. One continuous hairline route through the site, FEED to commissioning and
Houston to Tianjin to Vietnam to Monterrey. Scroll advances along it. Art direction is engineering
drawing: hairline grid, mono annotations over duotone industrial photography, program data as
decoration. True to what Hylex sells (weld inch tracking, program visibility).

## Phases
1. Design system: vector logo redraw, display face + Inter, colour, 8pt grid, motion tokens
2. Home rebuilt on the idea
3. Global network page as the interactive route map (the FWA piece)
4. Remaining 15 pages onto the system
5. Motion pass: scroll choreography, page transitions, prefers-reduced-motion fallback
6. Gates: Lighthouse 95+, CLS < 0.05, AA contrast, 390 phone, Safari + Firefox, SEO parity

## Self check loop
Playwright captures every page at 1440/1024/390, full page + 6 scroll stops + scroll video.
Score each page against the jury rubric into `award-ledger/`. Rework anything under 8.0.
A fresh reviewer agent that did not build it scores the same screenshots blind.
Benchmark against current SOTD winners. Loop until three clean rounds, no gate failing.

## Constraints
- Motion layers on top of static HTML. Enquiry path never behind an animation. 800 KB budget.
- Stays on build.py + plain HTML/CSS, no framework.
- Hylex content only. Never mixes with USP.

## Open with Alex
- Logo: original vector, or I redraw the mark.
- Quality bar only, or actual paid submission with a jury page. Assuming quality bar.

## Progress
- 2026-10-13 Phase 1 + 2 done, commit 060dfc5, STAGED NOT DEPLOYED.
  New token set in parts/base.css, Archivo + IBM Plex Mono, motion layer in parts/tail.html,
  home rebuilt in build.py. Self score 5.5 -> ~7.5.
  Gates: no overflow 18 pages x 1440/390, AA contrast on every pair (--faint darkened to #697572),
  0 missing alt, 0 unlabelled buttons, FCP 0.33s, no-JS safe.
  Alex rejected all 8 logo concepts ("maybe E2 but didn't like any of them, work on website and
  original logo first"). Original hylex-logo.png kept in the header. Revisit the mark later.
  Remaining: phase 3 interactive hub map, phase 4 the other 17 pages art directed, phase 5 motion
  pass, phase 6 the blind reviewer scoring loop.
- 2026-10-13 Alex: "why design is so close to USP? and why the black and white photo?" then
  "I meant those little words, even the font is similar". He was right. Commit 14000e0:
  Bricolage Grotesque + Instrument Sans replace Archivo + IBM Plex Mono (USP runs Inter);
  every letterspaced uppercase mono label removed site wide; home hero is no longer a photo,
  it opens on the network sheet + seven station lifecycle line on light paper; hub photos
  restored to colour with a common grade. RULE: Hylex must never share USP's visual
  architecture, not just its palette. USP leads on product photography, Hylex leads on the
  program. Still staged, not deployed.
- 2026-10-13 Alex on the photo question: "we don't really need real shop photo right? We are not
  locked in in shops....." He is right and it is a positioning rule, not a preference. Hylex does
  not own yards, so a yard photo in the hero claims one, which is USP's claim. That was the real
  root of the resemblance. RULE: Hylex leads on the program (network, lifecycle, record book,
  weld inch tracking, dashboards), never on shop photography. Photos are evidence on the network
  and capability pages, never the identity. This also voids the earlier request for 2400px photos.
- 2026-10-13 Alex rejected Bricolage Grotesque ("hell no"), left the replacement to me. Commit
  d59ab9f: Barlow Semi Condensed display + Barlow text, chosen from six candidates rendered at
  headline scale. Geist and Familjen Grotesk ruled out as too close to Inter (USP's face).
- 2026-10-13 First blind scoring round. My self score 7.4, blind reviewer 6.4
  (Design 6.5 / Usability 7.3 / Creativity 4.5 / Content 7.5). Creativity is the binding
  constraint: "nothing here is invented", layout reads as a well executed template default.
  LESSON: self scores run ~1.0 high, always run the blind reviewer before quoting a number.
  It caught Alpha ECC branding on the Vietnam quay. Audited every photo at 3x: img-hub-vietnam.jpg
  and img-yard.jpg both carried another fabricator's name, both deleted (commit 203a2f5).
  Also fixed: the 01-07 rail orphaned its dots when it wrapped on phone.
  OPEN: the hero has no signature moment. Proposal is to let the seven step program line drive
  the hero rather than sit under it. Put to Alex, awaiting his call.

## 2026-10-13, round 2: the traveller

Alex asked for 8.5 plain average. Round 1 of the rebuilt hero scored **7.33 and 7.80** from two
independent blind jurors (up from 6.4). Both named the same three faults and both were right.

**The device.** Every fabricated piece carries a traveller: a sheet that follows the steel station
to station and is stamped at each one. Hylex does not own the steel in the photograph, it owns the
sheet. So the sheet runs the hero: seven stations down the left, each stamping its real deliverable
(ITP, IFC, MTR, WPS, NDE, DFT, MDR) on load. Claim in the middle, work as evidence on the right.
A juror's words: "the rare B2B page where the idea and the business model are the same object."

**Faults found and fixed**
- Two hub photos were deck thumbnails rendered at ~5x. Root cause was general: the HTML `height`
  attribute was overriding `aspect-ratio` on every `.pcards img` site wide, forcing 372x600 boxes.
  Fixed with `height:auto`. No sharper hub source exists in the deck, so the home page now runs one
  sharp photograph (img-structural.jpg, 16.565 T stencilled on the web) beside three hard facts.
- The traveller was spent by section 02. Stations are links now, each code spells itself out in the
  row (`title=` does not exist on touch), and the page closes on the record book: the MDR contents
  at handover, stamped station by station.
- Three competing 01-0n sequences (stations, section counters, network rows). Now one: a number
  means a station. The fixed `.prog` scroll bar was removed, it was a progress bar wearing the
  idea's name and every template has it.

**Still open, needs Alex**
- Zero named proof: no client, no project, no reference. Biggest content gap, cannot be invented.
- `+1 (609) 917-0633` is a New Jersey area code on a page arguing "Houston decides".

**Lesson, again.** Self-scores run about a point high. Two independent blind jurors disagreed with
each other by 0.5, so run two, average them, and never quote your own number.

## 2026-10-13, rounds 3 and 4

Four blind jurors across four builds: **6.4 → 7.33 / 7.80 → 7.4 → 7.4**. The score stopped
moving because the remaining gap is not craft.

**Alex killed the seven station traveller**, in his words "the 7 station is really meaningless
to me", and he is right: FEED, drawings, procurement, fabrication, NDE, coating, load out is
what every fabricator does. The sheet frame stays; its contents are now the burden transfer,
the five things that leave the client's desk, each stamped HYLEX.

**Bugs the jury found that the gates did not.** Worth remembering, because every one of them
is a class of thing the overflow, contrast and alt gates cannot see:
- `backdrop-filter` on `header` made it the containing block for its own `position:fixed`
  drawer, so the mobile menu opened as a 48px sliver. The site was unusable on a phone.
- The drawer media query stopped at 999px while the burger ran to 1139px.
- A translucent header let the dark sections' own copy read through it.
- Tabbing out of the open drawer walked into the page behind it; `main` was not inert.
- `parts/tail.html` was copied from USP and never rewritten, so the Hylex chat answered
  with USP's distribution catalogue, in English and Chinese, triggered by the word "scope",
  which is Hylex's own call to action.
- An HTML `height` attribute beat CSS `aspect-ratio`, upscaling 376x212 thumbnails ~5x.
- Content contradicted itself across pages: four shops vs three, 3,000 t as a ceiling on two
  pages and a floor on two others, a PQR claim that fails ASME IX, and a capacity disclaimer
  that existed on the home page but not in `llms.txt` or the `FAQPage` JSON-LD, which are
  the surfaces a machine actually quotes.

**The ceiling.** Every juror puts 8.5 behind the same two things: one device carried the whole
length of the page, and one real delivered program, even anonymised. Without the case study
the ceiling is about 8.1. Both are now with Alex.

**Process lesson.** Run the juror against the live build, not screenshots, and do not edit the
repo while one is reviewing. Two of four rounds were partly wasted scoring a page that had
already changed underneath them.
