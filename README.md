# Hylex Energy Consulting — Website

Live at https://www.hylexenergy.com

Hylex is positioned as an integrated industrial project solution provider, organized around five capabilities: Engineering, Procurement, Fabrication, Oilfield Solutions, and Project Intelligence. Each has its own page; Procurement and Project Intelligence name and link to their live branded products (Fabflow Control, ScopePlex), while Engineering/Fabrication/Oilfield Solutions describe Hylex's own capability without naming the underlying manufacturing partners.

## Files
- `index.html` — homepage/hub, no build step
- `engineering.html`, `procurement.html`, `fabrication.html`, `oilfield.html`, `project-intelligence.html` — the five capability pages
- `about.html`, `contact.html` — company pages
- `assets/styles.css` — shared stylesheet (linked from every page)
- `assets/nav.js` — mobile nav toggle + dropdown behavior
- `assets/img/` — real photography extracted from source decks (Hylex, USP, Fabflow, AMGAIN)
- `usp-logo.png`, `fabflow-logo.png` — legacy logo assets (fabflow-logo still referenced; usp-logo currently unused since Fabrication no longer names USP)
- `vercel.json` — enables clean URLs (`/fabrication` instead of `/fabrication.html`)

## How deployment works
- GitHub repo: **https://github.com/hyperalexie/hylex-energy-site** (source of truth)
- Vercel project: **hylex-energy-site** (team: Alex Mac's projects) — auto-deploys on every push to `main`
- Domains: hylexenergy.com (308 → www) and www.hylexenergy.com
- DNS at GoDaddy: `A @ → 216.198.79.1`, `CNAME www → f519a66ac934c0df.vercel-dns-017.com`
  (MX/SPF for Microsoft 365 email untouched)

## Editing
Open this folder in VS Code, edit the relevant `.html` file (styles live in `assets/styles.css`, shared across all pages), then:
```bash
git add -A && git commit -m "update site" && git push
```
Vercel deploys automatically in ~30 seconds.

## TODO
- Contact form (`contact.html`) currently posts to a placeholder Formspree endpoint (`YOUR_FORM_ID`) — sign up free at formspree.io, create a form, and replace the placeholder in the form's `action` attribute before relying on it.
- Analytics not yet wired up on the marketing site itself (separate from ScopePlex's in-app analytics) — decide on PostHog/GA4/Plausible if desired.
