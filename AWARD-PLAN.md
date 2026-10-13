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
