#!/usr/bin/env python3
"""Build hylexenergy.com.

Positioning and all figures come from Alex's capability deck (Hylex.pdf, 12 Oct 2026):
global fabrication, procurement, engineering and project delivery for EPCs and owners,
run from Houston through the China, Vietnam and Mexico hubs.

Run: python3 build.py   (writes the html, sitemap and the vercel redirect whitelist)
Shared css, chat widget, tracking and the enquiry form live in parts/. Posts in posts.json.
"""
import json, html, datetime

SITE = "https://www.hylexenergy.com"
EMAIL = "amac@hylexenergy.com"
TEL_US = "+1 (609) 917-0633"
TEL_CN = "+86 183 2278 0729"
e = html.escape
TODAY = datetime.date.today().isoformat()

BASE_CSS = open("parts/base.css").read()
TAIL = open("parts/tail.html").read()
FORM = open("parts/form.html").read()

EXTRA_CSS = r"""
/* ============ home hero: the program traveller ============ */
.xh2{background:var(--paper);border-bottom:1px solid var(--line);position:relative;overflow:hidden}
.xh2::before{content:"";position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(52% 62% at 93% 2%,rgba(0,196,106,.06),transparent 70%)}
.xh2 .wrap{padding-top:clamp(28px,3.4vw,50px);padding-bottom:0}
.xh2 .top{font-size:14.5px;color:var(--faint);display:flex;gap:8px 22px;flex-wrap:wrap;align-items:center}
.xh2 .top b{color:var(--green-t);font-weight:500;display:inline-flex;align-items:center;gap:8px}
.xh2 .top b::before{content:"";width:7px;height:7px;background:var(--green);
  animation:pulse 2.8s var(--e2) infinite}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.3;transform:scale(.6)}}
/* three zones: the traveller runs the hero, the claim sits beside it, the work is evidence */
.hg{display:grid;gap:clamp(24px,2.8vw,38px);margin-top:clamp(18px,2vw,28px);align-items:start}
@media(min-width:1080px){
  .hg{grid-template-columns:208px minmax(0,1.18fr) minmax(0,.76fr);gap:0;align-items:stretch;
    margin-top:clamp(24px,2.5vw,36px)}
  .hcopy{order:2;padding:2px clamp(28px,3vw,50px) clamp(46px,4.4vw,70px);border-right:1px solid var(--line)}
  .trav{order:1}
  .hpic{order:3;padding:0 0 clamp(46px,4.4vw,70px) clamp(28px,3vw,50px)}
  .hpic .hshot{height:100%;aspect-ratio:auto;min-height:420px}
}
.xh2 h1{font-family:var(--d);font-size:clamp(37px,3.65vw,53px);line-height:1.03;letter-spacing:-.02em;
  margin:0;max-width:16ch}
.xh2 h1 em{font-style:normal;display:block;color:var(--faint)}
.xh2 .sub{margin:clamp(17px,1.8vw,25px) 0 0;max-width:47ch;font-size:clamp(16.5px,1.25vw,18.5px);
  line-height:1.6;color:var(--body)}
.xh2 .cta{margin:clamp(23px,2.3vw,31px) 0 0}
/* the work is evidence, never the identity of the page */
.hshot{position:relative;overflow:hidden;background:var(--paper-3);width:100%;margin:0;aspect-ratio:4/5}
.hshot img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
  filter:saturate(.94) contrast(1.05);transform:scale(1.03);transition:transform 2.4s var(--e)}
.xh2.in .hshot img{transform:scale(1)}
.hshot figcaption{position:absolute;left:0;right:0;bottom:0;padding:15px 17px;color:#fff;
  font-size:13.5px;line-height:1.35;background:linear-gradient(0deg,rgba(11,15,16,.86),transparent)}
@media(max-width:1079px){.hshot{aspect-ratio:16/10}}
@media(max-width:767px){.hshot figcaption{padding-right:74px}}
.sheet{border:1px solid var(--line);background:#fff}
.sheet .hd{display:flex;justify-content:space-between;align-items:center;gap:12px;
  padding:14px 18px;border-bottom:1px solid var(--line);font-size:14px;color:var(--faint)}
.sheet .hd b{color:var(--ink);font-weight:500}
.sheet ol{list-style:none;margin:0;padding:6px 20px 18px;position:relative;counter-reset:st}
@media(min-width:900px){.sheet ol{display:grid;grid-template-columns:1fr 1fr;column-gap:40px;padding-bottom:22px}
.sheet ol::before,.sheet ol::after{display:none}
.sheet li+li{border-top:0}
.sheet li:nth-child(n+3){border-top:1px solid var(--line)}}
.sheet ol::before{content:"";position:absolute;left:25px;top:25px;bottom:30px;width:1px;background:var(--line-2)}
.sheet ol::after{content:"";position:absolute;left:25px;top:24px;width:1px;background:var(--green);
  height:0;transition:height 1.5s var(--e) .3s}
section.s.in .sheet ol::after{height:calc(100% - 54px)}
.sheet li{position:relative;padding:15px 0 15px 46px}
.sheet li+li{border-top:1px solid var(--line)}
.sheet li::before{content:"";position:absolute;left:21px;top:21px;width:9px;height:9px;background:var(--green);
  opacity:0;transform:scale(.3);transition:opacity .5s var(--e),transform .5s var(--e)}
section.s.in .sheet li:nth-child(1)::before{opacity:1;transform:scale(1);transition-delay:.45s}
section.s.in .sheet li:nth-child(2)::before{opacity:1;transform:scale(1);transition-delay:.75s}
section.s.in .sheet li:nth-child(3)::before{opacity:1;transform:scale(1);transition-delay:1.05s}
section.s.in .sheet li:nth-child(4)::before{opacity:1;transform:scale(1);transition-delay:1.35s}
.sheet i{display:block;font-style:normal;font-size:13.5px;color:var(--faint);margin-bottom:5px}
.sheet b{display:block;font-size:17.5px;font-weight:600;letter-spacing:-.01em;color:var(--ink);margin-bottom:4px}
.sheet span{display:block;font-size:14.5px;line-height:1.45;color:var(--mute)}
/* ============ the traveller ============================================
   Every fabricated piece carries a traveller: a sheet that follows the steel
   from station to station and is stamped at each one. Hylex does not own the
   steel in the photograph, it owns the sheet. So the sheet runs the page.
   Stations stamp themselves once, fast. No JS, no prefers-reduced-motion:
   everything is already stamped, nothing is hidden. */
.trav{position:relative;border-top:1px solid var(--ink);padding-top:0}
@media(min-width:1080px){.trav{border-top:0;border-right:1px solid var(--line);padding:2px 26px 70px 0}}
.tvh{display:flex;justify-content:space-between;gap:10px;align-items:baseline;
  padding:13px 0 15px;font-size:13px;color:var(--faint)}
.tvh b{font-weight:600;color:var(--ink);font-size:13.5px}
@media(min-width:1080px){.tvh{display:block;padding:0 0 19px}.tvh span{display:block;margin-top:4px}}
.trav ol{list-style:none;margin:0;padding:0;position:relative}
.trav ol::before{content:"";position:absolute;left:3px;top:11px;bottom:16px;width:1px;background:var(--line-2)}
.trav ol::after{content:"";position:absolute;left:3px;top:11px;width:1px;background:var(--green);
  height:calc(100% - 27px)}
.js .trav ol::after{height:0;transition:height 1.05s var(--e2) .08s}
.js .xh2.in .trav ol::after{height:calc(100% - 27px)}
.trav li{position:relative;padding:0 0 clamp(13px,1.45vw,19px) 22px;
  display:grid;grid-template-columns:minmax(0,1fr) auto;gap:0 10px;align-items:center}
.trav li::before{content:"";position:absolute;left:0;top:10px;width:7px;height:7px;border-radius:50%;
  background:var(--green)}
.js .trav li::before{opacity:0;transform:scale(.2);transition:opacity .3s,transform .34s var(--e)}
.js .xh2.in .trav li::before{opacity:1;transform:scale(1)}
.trav i{grid-column:1;font-style:normal;font-size:12px;color:var(--faint);display:block;line-height:1}
.trav b{grid-column:1;display:block;font-size:14.5px;font-weight:600;color:var(--ink);
  line-height:1.22;letter-spacing:-.005em;margin-top:4px}
/* the stamp: lands like a rubber stamp on paper, once */
.trav .sk{grid-column:2;grid-row:1/3;align-self:center;justify-self:end;
  font-size:11px;font-weight:700;letter-spacing:.03em;color:var(--green-t);
  border:1.5px solid var(--green);padding:4px 6px;line-height:1;white-space:nowrap;
  transform:rotate(-1.5deg)}
.js .trav .sk{opacity:0;transform:scale(1.85) rotate(-8deg);
  transition:opacity .2s var(--e2),transform .28s var(--e2)}
.js .xh2.in .trav .sk{opacity:1;transform:scale(1) rotate(-1.5deg)}
.js .xh2.in .trav li:nth-child(1) .sk,.js .xh2.in .trav li:nth-child(1)::before{transition-delay:.20s}
.js .xh2.in .trav li:nth-child(2) .sk,.js .xh2.in .trav li:nth-child(2)::before{transition-delay:.33s}
.js .xh2.in .trav li:nth-child(3) .sk,.js .xh2.in .trav li:nth-child(3)::before{transition-delay:.46s}
.js .xh2.in .trav li:nth-child(4) .sk,.js .xh2.in .trav li:nth-child(4)::before{transition-delay:.59s}
.js .xh2.in .trav li:nth-child(5) .sk,.js .xh2.in .trav li:nth-child(5)::before{transition-delay:.72s}
.js .xh2.in .trav li:nth-child(6) .sk,.js .xh2.in .trav li:nth-child(6)::before{transition-delay:.85s}
.js .xh2.in .trav li:nth-child(7) .sk,.js .xh2.in .trav li:nth-child(7)::before{transition-delay:.98s}
.tvf{border-top:1px solid var(--line);padding-top:13px;font-size:12.5px;line-height:1.45;color:var(--faint)}
@media(max-width:1079px){.trav{padding-bottom:4px}}
/* ============ footer title block ============ */
.tblock{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--line-dk);
  border-left:1px solid var(--line-dk);margin-bottom:clamp(38px,4.2vw,60px)}
@media(min-width:900px){.tblock{grid-template-columns:repeat(4,1fr)}}
.tblock div{padding:13px 15px;border-right:1px solid var(--line-dk);border-bottom:1px solid var(--line-dk)}
.tblock i{font-style:normal;display:block;font-size:12px;color:rgba(255,255,255,.42);margin-bottom:5px}
.tblock b{display:block;margin:0;font-size:13.5px;font-weight:600;color:#fff;line-height:1.3}
/* ============ dark data band ============ */
.dark-s{background:var(--ink);color:#fff;padding:clamp(64px,8vw,116px) 0;border-bottom:0}
.dark-s h2{color:#fff}
.dark-s .eb{color:var(--green)}
.dark-s .eb::before{color:rgba(255,255,255,.4)}
.dark-s .lead{color:rgba(255,255,255,.66)}
.dark-s .kpi{border-color:var(--line-dk)}
.dark-s .kpi div{border-color:var(--line-dk)}
.dark-s .kpi b{color:#fff;font-size:clamp(34px,3.7vw,54px)}
.dark-s .kpi span{color:rgba(255,255,255,.55)}
.dark-s .btn{border-color:rgba(255,255,255,.4);color:#fff}
.dark-s .btn::before{background:#fff}.dark-s .btn:hover{color:var(--ink)}
/* ============ dropdown nav ============ */
nav .nd{position:relative}
/* ============ inner page banner eyebrow has no counter ============ */
.pb .eb::before{content:none}
.xh .eb::before,.end .eb::before{content:none}
"""


# ---------------------------------------------------------------- nav
NAV = [
    ("What we do", "services.html", [
        ("Fabrication programs", "services.html"),
        ("Engineering", "engineering.html"),
        ("Procurement", "procurement.html"),
        ("Project controls", "digital.html"),
    ]),
    ("Capability", "capability.html", [
        ("Fabrication scope", "capability.html"),
        ("Quality and inspection", "capability.html#qa"),
        ("Sectors", "capability.html#sectors"),
    ]),
    ("Global network", "network.html", [
        ("Overview", "network.html"),
        ("China hub", "hub-china.html"),
        ("Vietnam hub", "hub-vietnam.html"),
        ("Mexico hub", "hub-mexico.html"),
        ("Houston", "network.html#houston"),
    ]),
    ("Industrial AI", "industrial-ai.html", []),
    ("About", "about.html", [
        ("Company", "about.html"),
        ("FAQ", "faq.html"),
    ]),
    ("Insights", "insights.html", []),
    ("Contact", "contact.html", []),
]


def header(active):
    items = ""
    for label, href, subs in NAV:
        on = ' class="on"' if href == active or any(s[1].split("#")[0] == active for s in subs) else ""
        if subs:
            dd = "".join(f'<a href="{h}">{e(t)}</a>' for t, h in subs)
            items += f'<div class="nd"><a href="{href}"{on}>{e(label)}</a><div class="dd">{dd}</div></div>'
        else:
            items += f'<div class="nd"><a href="{href}"{on}>{e(label)}</a></div>'
    return ('<header><div class="wrap">'
            '<a class="logo" href="index.html"><img src="hylex-logo.png" alt="Hylex Energy Consulting" width="300" height="88"></a>'
            f'<nav>{items}</nav>'
            '<div class="hr"><a class="btn p" href="contact.html">Send an enquiry</a>'
            '<button type="button" class="burger" aria-label="Menu" aria-expanded="false"><i></i><i></i><i></i></button>'
            '</div></div></header>')


FOOTER = f"""<footer><div class="wrap"><div class="tblock">
<div><i>Program owner</i><b>Hylex Energy Consulting</b></div>
<div><i>Head office</i><b>Energy Corridor, Houston, Texas</b></div>
<div><i>Scope</i><b>Engineering · Procurement · Fabrication · Controls</b></div>
<div><i>Fabrication hubs</i><b>China · Vietnam · Mexico</b></div>
</div><div class="fg">
<div><b>What we do</b><a href="services.html">Fabrication programs</a><a href="engineering.html">Engineering</a><a href="procurement.html">Procurement</a><a href="digital.html">Project controls</a></div>
<div><b>Capability</b><a href="capability.html">Fabrication scope</a><a href="capability.html#qa">Quality and inspection</a><a href="capability.html#sectors">Sectors</a><a href="faq.html">FAQ</a></div>
<div><b>Global network</b><a href="hub-china.html">China hub</a><a href="hub-vietnam.html">Vietnam hub</a><a href="hub-mexico.html">Mexico hub</a><a href="network.html#houston">Houston</a><a href="industrial-ai.html">Industrial AI</a></div>
<div><b>Contact</b><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:+16099170633">{TEL_US}</a><a href="tel:+8618322780729">{TEL_CN}</a><span>Energy Corridor, Houston TX</span><span>Tianjin, China</span></div>
</div><div class="fb"><span>© 2026 Hylex Energy Consulting</span><span>Driving projects from concept to commissioning</span></div></div></footer>"""


def end_band(h2, p, primary=("Send an enquiry", "contact.html"),
             secondary=("Book a call", f"mailto:{EMAIL}?subject=Call%20request")):
    return (f'<section class="end"><div class="wrap"><div><h2>{e(h2)}</h2><p>{e(p)}</p></div>'
            f'<div class="cta"><a class="btn p" href="{primary[1]}">{e(primary[0])}</a>'
            f'<a class="btn" href="{secondary[1]}">{e(secondary[0])}</a></div></div></section>')


OG = f"{SITE}/og-card.png"

# breadcrumb trails: filename -> [(name, path)], last entry is the page itself
TRAILS = {
    "services.html": [("Home", "/"), ("What we do", "/services")],
    "engineering.html": [("Home", "/"), ("What we do", "/services"), ("Engineering", "/engineering")],
    "procurement.html": [("Home", "/"), ("What we do", "/services"), ("Procurement", "/procurement")],
    "digital.html": [("Home", "/"), ("What we do", "/services"), ("Project controls", "/digital")],
    "capability.html": [("Home", "/"), ("Capability", "/capability")],
    "network.html": [("Home", "/"), ("Global network", "/network")],
    "hub-china.html": [("Home", "/"), ("Global network", "/network"), ("China hub", "/hub-china")],
    "hub-vietnam.html": [("Home", "/"), ("Global network", "/network"), ("Vietnam hub", "/hub-vietnam")],
    "hub-mexico.html": [("Home", "/"), ("Global network", "/network"), ("Mexico hub", "/hub-mexico")],
    "industrial-ai.html": [("Home", "/"), ("Industrial AI", "/industrial-ai")],
    "about.html": [("Home", "/"), ("About", "/about")],
    "contact.html": [("Home", "/"), ("Contact", "/contact")],
    "faq.html": [("Home", "/"), ("FAQ", "/faq")],
    "insights.html": [("Home", "/"), ("Insights", "/insights")],
}


def breadcrumb_ld(fn):
    t = TRAILS.get(fn)
    if not t:
        return None
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
                                for i, (n, u) in enumerate(t)]}


def service_ld(name, desc, path):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "description": desc,
            "serviceType": name, "url": SITE + path,
            "provider": {"@type": "Organization", "name": "Hylex Energy Consulting", "url": SITE + "/"},
            "areaServed": [{"@type": "Country", "name": c} for c in
                           ("United States", "Mexico", "China", "Vietnam", "Australia")]}



PAGE_INDEX = []


def page(fn, title, desc, body, active, ld=None):
    url = f"{SITE}/" + ("" if fn == "index.html" else fn.replace(".html", ""))
    if fn != "404.html":
        PAGE_INDEX.append((title, desc, url))
    blocks = list(ld or [])
    bc = breadcrumb_ld(fn)
    if bc:
        blocks.append(bc)
    ldj = "".join(f'<script type="application/ld+json">{json.dumps(x, separators=(",", ":"))}</script>' for x in blocks)
    doc = f"""<!doctype html>
<html lang="en"><head><script>document.documentElement.className="js"</script><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="/img-icon-32.png"><link rel="icon" type="image/png" sizes="48x48" href="/img-icon-48.png"><link rel="icon" type="image/png" sizes="192x192" href="/img-icon-192.png"><link rel="apple-touch-icon" href="/img-icon-180.png">
<link rel="canonical" href="{url}">
<meta name="google-site-verification" content="5lLqt_MN86aVO2VkLGsd1zxDl5vYC9yxgDOhDw3d26c">
<meta property="og:type" content="website"><meta property="og:site_name" content="Hylex Energy Consulting">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{OG}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{OG}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=Barlow+Semi+Condensed:wght@600;700&display=swap" rel="stylesheet">
<style>{BASE_CSS}{EXTRA_CSS}</style></head>
<body>
{ldj}
{header(active)}
{body}
{FOOTER}
{TAIL}
<script defer src="/_vercel/speed-insights/script.js"></script>
</body></html>"""
    open(fn, "w").write(doc)
    return url


def banner(crumb, h1, p, eyebrow):
    return (f'<section class="pb"><div class="wrap"><div class="crumb">{" · ".join(crumb)}</div>'
            f'<div class="eb" style="margin-top:14px">{e(eyebrow)}</div>'
            f'<h1>{e(h1)}</h1><p>{e(p)}</p></div></section>')


def kpis(pairs, cls="k4"):
    return f'<div class="kpi {cls}">' + "".join(
        f"<div><b>{e(b)}</b><span>{e(s)}</span></div>" for b, s in pairs) + "</div>"


LLMS_HEAD = f"""# Hylex Energy Consulting

> Global fabrication, procurement, engineering and project delivery for EPC companies and asset owners. Hylex takes ownership of the fabrication execution process from shop readiness and sourcing through QA, NDE, FAT and logistics, delivered through fabrication and engineering hubs in China, Vietnam and Mexico, with headquarters in the Energy Corridor, Houston, Texas.

## Key facts
- Four services: engineering and design, global procurement, fabrication delivery, project controls and lifecycle reporting
- Houston holds the client interface, engineering coordination, procurement and QA; the hubs hold the capacity, the yards and the load out
- Pipe spooling over 250,000 dia-inches a month across the workshops
- Structural steel and platework over 50,000 tons a year
- Pressure vessels and columns to 8 m diameter and 150 mm wall, single units over 300 tons
- Pre assembled modules over 1,000 tons and up to 32 m long
- Over 16,000 m2 of surface preparation and coating, including TSA, FBE, epoxy and galvanizing
- Over 500 prequalified manufacturers and OEMs; strategic sourcing saves 20 to 40 percent against local procurement
- Fabricated and tested to ASME, API, PED, EN, ISO, NORSOK M-501 and ISO 12944
- China hub: over 200,000 dia-inches a month, over 40,000 tons a year structural, modules to 3,000 tons
- Vietnam hub: 195,000 m2 yard, 31,000 m2 covered workshops, 260 t gantry cranes, 312 m private jetty with 10,000 DWT load out
- Mexico hub: Monterrey, 4,000 to 5,000 spools a month, 34,000 factored dia-inches a week, 11 hectare yard, 100,000 sq ft coating facility, inside USMCA
- Sectors: chemical, LNG terminals, downstream, power, mining and semiconductor
- Separate line of work: industrial AI systems for estimating, sales pipeline, shop floor tracking and a private agent on the client's own server
- Every enquiry is handled by a principal, answered within one working day

"""

CODES = ('<div class="codes"><span>Fabricated and tested to</span>'
         '<b>ASME · API · PED · EN · ISO · NORSOK M-501 · ISO 12944</b></div>')


# ---------------------------------------------------------------- pages
def home():
    body = f"""<section class="xh2"><div class="wrap">
<div class="top"><b>Four locations, one program</b><span>Houston, China, Vietnam, Mexico</span></div>
<div class="hg">
<div class="hcopy">
<h1>We run the fabrication program.<em>You run the project.</em></h1>
<p class="sub">Hylex takes complete ownership of fabrication execution for EPC companies and asset owners. Engineering, global procurement, fabrication and project controls, under one owner from concept to commissioning.</p>
<div class="cta"><a class="btn p" href="contact.html"><span>Send us the scope</span></a><a class="btn" href="services.html"><span>What we do</span></a></div>
{CODES}
</div>
<div class="trav" aria-label="The program traveller, FEED to load out">
<div class="tvh"><b>Program traveller</b><span>FEED to load out</span></div>
<ol>
<li><i>01 · ITP</i><b>FEED and design</b><span class="sk" title="Inspection and test plan agreed">ITP</span></li>
<li><i>02 · IFC</i><b>Shop drawings</b><span class="sk" title="Issued for construction">IFC</span></li>
<li><i>03 · MTR</i><b>Procurement</b><span class="sk" title="Material test reports held">MTR</span></li>
<li><i>04 · WPS</i><b>Fabrication</b><span class="sk" title="Weld procedures qualified">WPS</span></li>
<li><i>05 · NDE</i><b>NDE and FAT</b><span class="sk" title="Examination and test reports">NDE</span></li>
<li><i>06 · DFT</i><b>Coating</b><span class="sk" title="Film thickness records">DFT</span></li>
<li><i>07 · MDR</i><b>Load out</b><span class="sk" title="Manufacturing record book">MDR</span></li>
</ol>
<p class="tvf">Seven stations. One owner. You hold the record book, not the coordination.</p>
</div>
<div class="hpic"><figure class="hshot"><img src="img-piperacks.jpg" alt="Galvanised pipe racks and spools laid out in the fabrication shop" fetchpriority="high" width="784" height="980"><figcaption>Pipe racks and spools, shop assembled</figcaption></figure></div>
</div>
</div></section>

<section class="s"><div class="wrap"><div class="eb">What we do</div><h2>One partner, the whole lifecycle</h2>
<p class="lead">Four disciplines under one owner, so nothing falls between a designer, a buyer and a workshop.</p>
<div class="doors">
<div class="door"><div class="eb">Stations 01 to 02 · <b>Engineering and design</b></div><h3>Fabrication ready execution</h3>
<p>Detailed shop drawings, 3D models, clash checks and datasheets, from FEED through as built.</p>
<div class="lk"><a href="engineering.html">Engineering</a></div></div>
<div class="door"><div class="eb">Station 03 · <b>Procurement</b></div><h3>Global sourcing under one owner</h3>
<p>Vendor qualification, audits, commercial negotiation, expediting and logistics coordination across China, Vietnam and Mexico.</p>
<div class="lk"><a href="procurement.html">Procurement</a></div></div>
<div class="door"><div class="eb">Stations 04 to 06 · <b>Fabrication delivery</b></div><h3>Pipe spools to complete modules</h3>
<p>Pipe spooling, pressure vessels, structural steel, platework and turnkey skid systems through a network of qualified workshops.</p>
<div class="lk"><a href="capability.html">Capability</a><a href="network.html">The hubs</a></div></div>
<div class="door"><div class="eb">Station 07 · <b>Project controls</b></div><h3>Progress you can see</h3>
<p>Real time weld inch tracking, fabrication dashboards, NDE reporting, material traceability and digital manufacturing record books.</p>
<div class="lk"><a href="digital.html">Project controls</a></div></div>
</div></div></section>

<section class="s dark-s"><div class="wrap"><div class="eb">Scale</div><h2>What the network delivers</h2>
<p class="lead">Capacity held across the hubs, available to one program without you qualifying a single workshop.</p>
{kpis([("250,000+", "Dia-inches of pipe spooling per month across the workshops"),
       ("50,000+", "Tons a year of structural steel and platework"),
       ("8 m / 150 mm", "Vessel diameter and wall thickness, single units over 300 tons"),
       ("1,000+ tons", "Pre assembled modules up to 32 m in length")])}
<div class="cta" style="margin-top:38px"><a class="btn" href="capability.html"><span>Full fabrication scope</span></a></div></div></section>

<section class="s"><div class="wrap"><div class="eb">Global network</div><h2>Houston decides. The hubs build.</h2>
<p class="lead">Houston holds the client interface, the engineering coordination and the procurement. The fabrication hubs carry the capacity, the yards and the load out.</p>
<div class="sheet" style="margin-bottom:clamp(30px,3.4vw,46px)"><div class="hd"><b>The network</b><span>Who does what, and where</span></div>
<ol>
<li><i>01 · Houston, Texas</i><b>The interface</b><span>Client contact, engineering coordination, procurement and QA.</span></li>
<li><i>02 · China</i><b>Heavy fabrication</b><span>Full capability, mega module assembly, engineering support.</span></li>
<li><i>03 · Vietnam</i><b>Yard and jetty</b><span>Heavy structural, modular assembly, deep sea load out.</span></li>
<li><i>04 · Mexico</i><b>Nearshore</b><span>Monterrey spooling and coating, inside USMCA.</span></li>
</ol></div>
<div class="pcards p3">
<figure><div class="im"><img src="img-hub-china.jpg" alt="China fabrication and engineering hub" loading="lazy" width="800" height="600"></div><figcaption><b>China</b><p>Full fabrication capability, heavy yard and mega module assembly, procurement and engineering support.</p></figcaption></figure>
<figure><div class="im"><img src="img-structural.jpg" alt="Heavy structural module fabricated for load out" loading="lazy" width="800" height="600"></div><figcaption><b>Vietnam</b><p>Heavy structural fabrication, modular assembly and a private jetty with deep sea load out. Tariff resilient.</p></figcaption></figure>
<figure><div class="im"><img src="img-hub-mexico.jpg" alt="Mexico fabrication facility at Monterrey" loading="lazy" width="800" height="600"></div><figcaption><b>Mexico</b><p>Monterrey pipe spooling and industrial coating, 1.5 hours from the Texas border, inside USMCA.</p></figcaption></figure>
</div>
<div class="cta" style="margin-top:38px"><a class="btn" href="network.html"><span>The global network</span></a></div></div></section>

<section class="s"><div class="wrap"><div class="eb">Why it matters</div><h2>Fabrication stops being your problem to manage</h2>
<div class="tags">
<div>Zero internal burden<span>No procurement, inspection or fabrication specialists needed on your staff.</span></div>
<div>Single point accountability<span>One team owns cost, schedule, quality and compliance.</span></div>
<div>Faster mobilisation<span>Projects launch without procurement delays or technical onboarding.</span></div>
</div></div></section>

{end_band("Send us the scope", "Drawings, datasheets and specification. We reply within one working day.")}"""
    ld = [
        {"@context": "https://schema.org", "@type": "Organization", "name": "Hylex Energy Consulting",
         "url": SITE + "/", "logo": f"{SITE}/img-icon-512.png", "email": EMAIL, "telephone": TEL_US,
         "address": {"@type": "PostalAddress", "streetAddress": "Energy Corridor",
                     "addressLocality": "Houston", "addressRegion": "TX", "addressCountry": "US"},
         "description": "Global fabrication, procurement, engineering and project delivery for EPC companies and asset owners."},
        {"@context": "https://schema.org", "@type": "WebSite", "name": "Hylex Energy Consulting", "url": SITE + "/"},
    ]
    return page("index.html", "Hylex Energy Consulting | Global fabrication, procurement and project delivery",
                "End to end fabrication program management for EPC companies and asset owners. Engineering, global procurement, fabrication and project controls through hubs in China, Vietnam and Mexico.",
                body, "index.html", ld)


def services():
    body = f"""{banner(['<a href="index.html">Home</a>', 'What we do'], "Full fabrication management",
        "Hylex takes complete ownership of the fabrication execution process from day one, so your procurement and project teams can stay on strategy while we carry the technical, commercial and operational load.", "What we do")}

<section class="s"><div class="wrap"><div class="eb">The four parts</div><h2>What we take on</h2>
<div class="nlist">
<div><b>Fabrication program management</b><ul><li>End to end oversight from shop readiness and sourcing to QA, NDE, FAT and logistics</li><li>Every interface managed between your engineering team, the fabricators, the inspectors and the freight forwarders</li></ul></div>
<div><b>Procurement and vendor ownership</b><ul><li>Single point of accountability for supplier selection, qualification, contracting and expediting</li><li>Your procurement team does not have to run the RFPs or the audits</li></ul></div>
<div><b>Technical and QA oversight</b><ul><li>Fabrication technical reviews, WPS and PQR qualification, inspection regimes and document control</li><li>Handled by our own subject matter experts, not handed back to the shop to mark its own work</li></ul></div>
<div><b>Project controls and lifecycle reporting</b><ul><li>Progress dashboards, weld inch tracking, NDE reporting and material traceability</li><li>Complete digital manufacturing record books and as built data at handover</li></ul></div>
</div></div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="split">
<div><div class="eb">Houston</div><h2>North American governance over Asian capacity</h2>
<p>The Houston office holds early engagement and feasibility, multi discipline design oversight, vendor prequalification and material strategy, a single point of contact for milestone reporting and change management, and QA and NDE coordination including third party audits.</p>
<p><a class="btn" href="network.html#houston">The Houston hub</a></p></div>
<div><img src="img-shopfloor.jpg" alt="Fabrication workshop floor with assemblies in progress" loading="lazy"></div>
</div></div></section>

<section class="s"><div class="wrap"><div class="eb">Why it matters</div><h2>What changes for your team</h2>
<div class="tags">
<div>Zero internal burden<span>No procurement, inspection or fabrication specialists on staff.</span></div>
<div>Single point accountability<span>One team owns cost, schedule, quality and compliance.</span></div>
<div>Faster mobilisation<span>No procurement delay, no staffing gap, no technical onboarding.</span></div>
<div>Optimised outcomes<span>A qualified global network instead of whoever is already on the approved list.</span></div>
<div>Predictable reporting<span>One progress picture, not four spreadsheets from three shops.</span></div>
<div>Clean handover<span>Digital record books, as built data and maintenance packages at completion.</span></div>
</div></div></section>

{end_band("Put a scope in front of us", "Send the drawings and the specification. We come back with the execution plan, not just a price.")}"""
    return page("services.html", "What we do | Hylex Energy Consulting",
                "Fabrication program management, procurement and vendor ownership, technical and QA oversight, and project controls for EPC companies and asset owners.",
                body, "services.html", [service_ld("Fabrication program management", "End to end management of fabrication execution for EPC companies and asset owners, from shop readiness and sourcing to QA, NDE, FAT and logistics.", "/services")])


def engineering():
    body = f"""{banner(['<a href="index.html">Home</a>', '<a href="services.html">What we do</a>', 'Engineering'],
        "Engineering that bridges design and the shop floor",
        "A full spectrum of engineering services that turn complex project requirements into buildable, optimised and cost effective solutions, from front end studies through detailed design to as built.", "Engineering")}

<section class="s"><div class="wrap"><div class="eb">Core capabilities</div><h2>From FEED to as built</h2>
<div class="nlist">
<div><b>Front end design</b><ul><li>Feasibility studies, conceptual layouts and early cost modelling to de risk decisions before fabrication</li><li>Process flow diagrams, P&amp;IDs and basis of design aligned to your objectives</li></ul></div>
<div><b>3D modelling</b><ul><li>Full plant modelling with clash detection and routing optimisation</li><li>PDMS, SmartPlant and E3D, with digital twin integration</li></ul></div>
<div><b>Detailed design</b><ul><li>Piping isometrics, structural fabrication drawings, equipment layouts and installation schematics</li><li>Build ready documentation tied into the procurement and fabrication workflow</li></ul></div>
<div><b>Process, mechanical and structural</b><ul><li>Pressure vessel and heat exchanger design to ASME, EN and PED</li><li>Modularisation, skid layout engineering and structural calculations optimised for transport</li></ul></div>
<div><b>As built and lifecycle</b><ul><li>Red line integration, as built documentation and predictive maintenance data</li><li>Continuing support for modifications, upgrades and expansion</li></ul></div>
</div></div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="split rev">
<div><div class="eb">Process technology</div><h2>Separation and water treatment packages</h2>
<p>Through a specialist engineering partner we supply proprietary process systems with a field record across offshore platforms, FPSOs and onshore facilities.</p>
<div class="nlist" style="margin-top:20px">
<div><b>Dehydration</b><p>Removes over 85 percent of water from production streams under 50 percent water cut, taking oil in water below 30 mg/L. Compact, with no moving parts.</p></div>
<div><b>Hydrocyclone and CFU</b><p>Hydrocyclone takes oil in water from under 1000 mg/L to under 100 mg/L. Compact flotation takes it below 30 mg/L.</p></div>
<div><b>Ultrafiltration</b><p>Removes particulates and organics from 0.002 to 0.1 micron, ten times the anti fouling performance of conventional membranes, Class A1 water for reinjection.</p></div>
<div><b>Biofilm wastewater</b><p>Up to 99 percent media fill with no clogging, for high COD and high turbidity streams offshore and in petrochemical plants.</p></div>
</div></div>
<div><img src="img-processunit.jpg" alt="Process package under assembly in the workshop" loading="lazy"></div>
</div></div></section>

{end_band("Send the drawings", "Feasibility, detailed design, or a package that needs engineering before anyone can build it.")}"""
    return page("engineering.html", "Engineering | Hylex Energy Consulting",
                "FEED, 3D modelling and digital twin, detailed design and shop drawings, pressure vessel and structural engineering to ASME, EN and PED, plus proprietary separation and water treatment packages.",
                body, "engineering.html", [service_ld("Engineering and design", "FEED, 3D modelling, detailed design and shop drawings, pressure vessel and structural engineering to ASME, EN and PED.", "/engineering")])


def procurement():
    body = f"""{banner(['<a href="index.html">Home</a>', '<a href="services.html">What we do</a>', 'Procurement'],
        "Global sourcing without the procurement overhead",
        "Comprehensive sourcing across China, Vietnam, Mexico and other manufacturing regions, so every project has the right materials and equipment, on time, on budget and compliant with international standards.", "Procurement")}

<section class="s"><div class="wrap">
{kpis([("500+", "Prequalified manufacturers and OEMs across piping, structural, mechanical, E&I and specialty equipment"),
       ("20 to 40%", "Cost saving against local procurement through strategic sourcing"),
       ("3 regions", "China, Vietnam and Mexico, so tariff and trade exposure is not single sourced")], "k3")}
</div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="eb">What it covers</div><h2>End to end supply chain management</h2>
<div class="nlist">
<div><b>Full lifecycle sourcing</b><ul><li>Material requisition through delivery and documentation</li><li>Vendor qualification, auditing, commercial negotiation and compliance verification</li><li>Expediting, inspection coordination and logistics planning in one managed process</li></ul></div>
<div><b>Regional specialisation</b><ul><li>China: cost effective high volume manufacturing and short lead times</li><li>Vietnam: tariff resilient sourcing with competitive labour and logistics</li><li>Mexico: nearshore supply for USMCA projects with less customs complexity</li></ul></div>
<div><b>Cost and risk</b><ul><li>Multi region options reduce tariff exposure, trade disruption and single source dependency</li><li>Prequalified vendor base compliant with ASME, API, PED and IEC</li><li>Direct relationships with steel mills, foundries, valve and instrumentation suppliers</li></ul></div>
<div><b>Logistics and delivery</b><ul><li>Global transport, export packing, sea freight planning and delivery scheduling</li><li>Shipment tracking and customs documentation so the package does not sit at the port</li></ul></div>
</div></div></section>

<section class="s"><div class="wrap"><div class="split">
<div><div class="eb">Delivered</div><h2>The scope arrives as one consignment, not six</h2>
<p>Packing, freight and documentation are planned with the fabrication schedule rather than after it. One party is answerable for what lands on your site and when.</p>
<p><a class="btn" href="contact.html">Send a material list</a></p></div>
<div><img src="img-logistics.jpg" alt="Container vessel loaded for export" loading="lazy"></div>
</div></div></section>

{end_band("Send a material list or a vendor scope", "We come back with sourcing options by region, with the cost and the lead time against each.")}"""
    return page("procurement.html", "Procurement | Hylex Energy Consulting",
                "Global sourcing with vendor qualification, audits, expediting and logistics. Over 500 prequalified manufacturers across China, Vietnam and Mexico, compliant to ASME, API, PED and IEC.",
                body, "procurement.html", [service_ld("Global procurement and sourcing", "Vendor qualification, audits, commercial negotiation, expediting and logistics across China, Vietnam and Mexico.", "/procurement")])


def capability():
    body = f"""{banner(['<a href="index.html">Home</a>', 'Capability'], "Overall fabrication capability",
        "Fully integrated fabrication through a network of specialised facilities across China, Vietnam and Mexico, from piping and pressure vessels to modular units and complete process packages.", "Capability")}

<section class="s"><div class="wrap">
{kpis([("250,000+", "Dia-inches of pipe spooling per month"),
       ("50,000+", "Tons a year, structural steel and platework"),
       ("300+ tons", "Single unit vessel weight, up to 8 m diameter and 150 mm wall"),
       ("16,000+ m²", "Surface preparation and coating facilities")])}
</div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="eb">Scope</div><h2>What the workshops build</h2>
<div class="pcards">
<figure><img src="img-piperacks.jpg" alt="Pipe spools racked after fabrication" loading="lazy"><figcaption><b>Pipe spooling and piping systems</b><ul><li>Over 250,000 dia-inches a month across multiple workshops</li><li>CNC cutting and beveling, automated welding, hydrotesting</li><li>Digital traceability on every spool</li></ul></figcaption></figure>
<figure><img src="img-structural.jpg" alt="Structural steel frame fabricated and painted" loading="lazy"><figcaption><b>Structural steel and platework</b><ul><li>Over 50,000 tons a year of pipe racks, structures and platforms</li><li>Heavy frameworks and large assembly bays</li><li>Load out quays for mega module construction</li></ul></figcaption></figure>
<figure><img src="img-vessels.jpg" alt="Row of pressure vessels completed in the workshop" loading="lazy"><figcaption><b>Pressure vessels, exchangers and columns</b><ul><li>Diameters to 8 m, wall thickness to 150 mm</li><li>Single unit weights over 300 tons</li><li>Built to ASME, PED, API and EN</li></ul></figcaption></figure>
<figure><img src="img-skid.jpg" alt="Packaged process skid complete with piping and instruments" loading="lazy"><figcaption><b>Modular skids and turnkey units</b><ul><li>Pre assembled modules over 1,000 tons and 32 m long</li><li>Mechanical, piping, E&amp;I and coating integrated</li><li>Delivered plug and play</li></ul></figcaption></figure>
<figure><img src="img-column.jpg" alt="Large diameter column under welding" loading="lazy"><figcaption><b>Specialised materials</b><ul><li>Stainless, duplex, super duplex and clad materials</li><li>Surface engineering including TSA, FBE, epoxy and galvanizing</li><li>Coating to ISO 12944 and NORSOK M-501</li></ul></figcaption></figure>
<figure><img src="img-platework.jpg" alt="Access platform and handrail assembly" loading="lazy"><figcaption><b>Platework and secondary steel</b><ul><li>Access platforms, handrails, gratings and ladders</li><li>Pipe supports, guides, anchors, shoes and trunnions</li><li>Engineered to the process and load case</li></ul></figcaption></figure>
</div></div></section>

<section class="s" id="qa"><div class="wrap"><div class="split rev">
<div><div class="eb">Quality</div><h2>Integrated QA, QC and digital project control</h2>
<p>Comprehensive inspection and test plans, non destructive examination covering VT, MT, PT, RT, UT and PMI, factory acceptance testing and complete documentation packages.</p>
<p>Progress is reported as real time weld inch tracking and fabrication dashboards, and the manufacturing record book is delivered digitally.</p>
<p><a class="btn" href="digital.html">How progress is reported</a></p>
{CODES}</div>
<div><img src="img-welder.jpg" alt="Welder working on a pipe spool" loading="lazy"></div>
</div></div></section>

<section class="s" id="sectors" style="background:var(--soft)"><div class="wrap"><div class="eb">Sectors</div><h2>Where the work goes</h2>
<div class="tags">
<div>Chemical<span>Process plant, reactors and utilities.</span></div>
<div>LNG terminals<span>Cryogenic piping, modules and storage support steel.</span></div>
<div>Downstream<span>Refinery units, exchangers and pipe racks.</span></div>
<div>Power<span>Boiler steel, ducting and balance of plant.</span></div>
<div>Mining<span>Processing structures, chutes, tanks and platework.</span></div>
<div>Semiconductor<span>High purity piping, skids and clean utility packages.</span></div>
</div></div></section>

{end_band("Send a fabrication scope", "Drawings, line lists or an equipment schedule. We come back with capacity, route and lead time.")}"""
    return page("capability.html", "Fabrication capability | Hylex Energy Consulting",
                "Pipe spooling over 250,000 dia-inches a month, 50,000 tons a year of structural steel, pressure vessels to 8 m diameter, modules over 1,000 tons, with integrated QA, NDE and digital reporting.",
                body, "capability.html", [service_ld("Fabrication delivery", "Pipe spooling, pressure vessels, structural steel, platework and turnkey modular skid systems.", "/capability")])


HUBS = {
    "china": dict(
        name="China", title="China fabrication and engineering hub", img="img-hub-china.jpg",
        lead="China is the backbone of the delivery platform, combining fabrication capacity, heavy engineering and modularisation at a scale and flexibility that is hard to match elsewhere.",
        kpi=[("200,000+", "Dia-inches of pipe spooling per month"),
             ("40,000+", "Tons a year of structural steel and platework"),
             ("3,000+ tons", "Pre assembled module weight"),
             ("30 to 50%", "Cost saving against Western markets")],
        blocks=[
            ("Pipe spooling and piping", ["Automated cutting, welding and hydrotesting", "Full digital traceability on every spool"]),
            ("Vessels and exchangers", ["Diameter to 8 m, wall thickness to 150 mm, single units over 300 tons", "ASME, PED and API certified fabrication and testing"]),
            ("Structural and platework", ["Large scale pipe racks, modules and steel frameworks", "Annual output over 40,000 tons"]),
            ("Modular skids and packages", ["Integrated piping, mechanical, E&amp;I, insulation and coatings", "Pre assembled, tested and loaded out complete"]),
            ("Heavy yard assembly", ["One of the largest heavy industrial assembly yards in Asia", "Pre assembly before shipment cuts site labour and installation schedule"]),
            ("Sourcing and supply chain", ["Access to steel mills, component OEMs and raw material suppliers", "Mature domestic ecosystem with supplier redundancy"]),
        ],
        desc="China fabrication and engineering hub: over 200,000 dia-inches of pipe spooling a month, 40,000 tons a year of structural steel, vessels to 8 m diameter and modules over 3,000 tons."),
    "vietnam": dict(
        name="Vietnam", title="Vietnam fabrication and engineering hub", img="img-structural.jpg",
        lead="Vietnam covers heavy structural fabrication, modular assembly and integrated process units, with deep water load out and a trade position that gives EPCs an alternative to China based supply.",
        kpi=[("195,000 m²", "Total yard area, 136,000 m² outdoor fabrication and laydown"),
             ("31,000 m²", "Covered workshops, with 6,884 m² assembly bays at 22 m hook height"),
             ("260 t", "Heavy lift gantry crane capacity"),
             ("312 m", "Private jetty, 10,000 DWT load out, 20 t/m² quay bearing")],
        blocks=[
            ("Production capacity", ["Structural steel over 20,000 tons a year", "Pipe spooling over 180,000 dia-inches a year", "Process skids and modular units, over 60 units a year"]),
            ("Integrated facilities", ["Machining, cutting, rolling, cap forming and hot induction bending", "Dedicated blasting, painting and coating halls to ISO 12944 and NORSOK M-501", "Pressure vessel fabrication, piping, outfitting and pre dressing"]),
            ("Logistics and load out", ["Direct deep sea access from the private jetty", "Heavy haul SPMT handling and sea fastening engineering"]),
            ("Trade position", ["Favourable trade status with North America, Europe and Australia", "Lets EPCs diversify sourcing and reduce trade exposure without losing cost position"]),
        ],
        desc="Vietnam fabrication hub: 195,000 m² yard, 312 m private jetty, 260 t gantry cranes, over 20,000 tons a year of structural steel and 180,000 dia-inches of pipe spooling."),
    "mexico": dict(
        name="Mexico", title="Mexico fabrication and engineering hub", img="img-hub-mexico.jpg",
        lead="Monterrey gives North American projects pipe spooling and industrial coating capacity an hour and a half from the Texas border, inside USMCA, with direct port and rail connections.",
        kpi=[("4,000 to 5,000", "Spools a month on a single shift"),
             ("34,000", "Factored dia-inches a week of welding throughput"),
             ("11 hectares", "Total yard area, 29,700 m² covered production space"),
             ("100,000 sq ft", "Coating facility with four blasting booths")],
        blocks=[
            ("Pipe spool fabrication", ["CNC cutting and beveling, multi process and automated welding", "Spoolgen detailing and SAM material tracking and allocation", "NDE and heat treatment services", "Real time spool tracking and data analytics"]),
            ("Blasting and coating", ["Ultra high solids and liquid coatings, thermal spray aluminium", "Climate controlled blasting and painting environments", "7,400 m² painting area, 3,350 m² weekly painting output"]),
            ("Structural pipe supports", ["Shop attached and field supports, guides, anchors, shoes, trunnions, base plates and dummy legs", "Engineered to the specific process and load requirement"]),
            ("Trade and workforce", ["USMCA tariff and customs advantage for North American projects", "Direct port and rail connections for rapid export", "Licensed and accredited local workforce"]),
        ],
        desc="Mexico fabrication hub at Monterrey: 4,000 to 5,000 spools a month, 34,000 factored dia-inches a week, an 11 hectare yard and a 100,000 sq ft coating facility, inside USMCA."),
}


def hub(key):
    h = HUBS[key]
    blocks = "".join(f'<div><b>{e(t)}</b><ul>' + "".join(f"<li>{x}</li>" for x in items) + "</ul></div>"
                     for t, items in h["blocks"])
    body = f"""{banner(['<a href="index.html">Home</a>', '<a href="network.html">Global network</a>', h["name"]],
        h["title"], h["lead"], "Fabrication hub")}

<section class="s"><div class="wrap">{kpis(h["kpi"])}</div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="eb">Capabilities</div><h2>What the hub covers</h2>
<div class="nlist">{blocks}</div>
{CODES}</div></section>

<section class="s"><div class="wrap"><div class="split">
<div><div class="eb">In the network</div><h2>One program, routed to the right yard</h2>
<p>Scope is placed where the capacity, the trade position and the schedule fit, and the whole package still reports to one team in Houston. The other hubs cover what this one does not.</p>
<p><a class="btn" href="network.html">The global network</a></p></div>
<div><img src="{h['img']}" alt="{e(h['title'])}" loading="lazy"></div>
</div></div></section>

{end_band("Send a scope for " + h["name"], "Drawings, line lists or an equipment schedule. We come back with capacity, route and lead time.")}"""
    return page(f"hub-{key}.html", f"{h['title']} | Hylex Energy Consulting", h["desc"], body, f"hub-{key}.html")


def network():
    body = f"""{banner(['<a href="index.html">Home</a>', 'Global network'], "Hubs across North America and Asia",
        "Houston holds the client interface, the engineering coordination and the procurement. The fabrication hubs in China, Vietnam and Mexico carry the capacity, the yards and the load out.", "Global presence")}

<section class="s" id="houston"><div class="wrap"><div class="split">
<div><div class="eb">Houston, Texas</div><h2>Headquarters and global support hub</h2>
<p>The Houston office brings North American standards, project governance and client facing support to fabrication delivered on the other side of the world.</p>
<div class="nlist" style="margin-top:20px">
<div><b>Front end development</b><p>Early engagement, feasibility studies and cost modelling to de risk decisions before fabrication starts.</p></div>
<div><b>Engineering coordination</b><p>Multi discipline design oversight, 3D model integration and technical alignment with your requirements.</p></div>
<div><b>Procurement intelligence</b><p>Vendor prequalification, material strategy and commercial negotiation run by a dedicated procurement team.</p></div>
<div><b>Client interface</b><p>A single point of contact for project tracking, milestone reporting, document control and change management.</p></div>
<div><b>QA and inspection</b><p>QA specialists and NDE coordination, including third party audits and regulatory liaison.</p></div>
</div></div>
<div><img src="img-skid.jpg" alt="Completed process skid ready for despatch" loading="lazy"></div>
</div></div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="eb">Fabrication hubs</div><h2>Three routes for one scope</h2>
<div class="pcards p3">
<figure><img src="img-hub-china.jpg" alt="China fabrication and engineering hub" loading="lazy"><figcaption><b>China</b><p>Full fabrication, heavy yard and mega module assembly. Over 200,000 dia-inches a month and modules to 3,000 tons.</p><p style="margin-top:10px"><a href="hub-china.html" style="color:var(--green-d);font-weight:600">China hub ›</a></p></figcaption></figure>
<figure><img src="img-structural.jpg" alt="Heavy structural module fabricated for load out" loading="lazy"><figcaption><b>Vietnam</b><p>Heavy structural and modular assembly on a 195,000 m² yard with a 312 m private jetty. Tariff resilient.</p><p style="margin-top:10px"><a href="hub-vietnam.html" style="color:var(--green-d);font-weight:600">Vietnam hub ›</a></p></figcaption></figure>
<figure><img src="img-hub-mexico.jpg" alt="Mexico fabrication hub at Monterrey" loading="lazy"><figcaption><b>Mexico</b><p>Monterrey spooling and coating, 1.5 hours from the Texas border, inside USMCA. Nearshore for North America.</p><p style="margin-top:10px"><a href="hub-mexico.html" style="color:var(--green-d);font-weight:600">Mexico hub ›</a></p></figcaption></figure>
</div></div></section>

<section class="s"><div class="wrap"><div class="eb">Why three</div><h2>Routing is part of the engineering</h2>
<div class="tags">
<div>Tariff exposure<span>Multi region options, so one trade decision does not reprice the package.</span></div>
<div>Schedule<span>Capacity found where the yard is free, not where the enquiry happened to land.</span></div>
<div>Load out<span>Deep water jetty for modules, nearshore rail and road for North American spools.</span></div>
</div></div></section>

{end_band("Not sure which hub fits?", "Send the scope. Routing, capacity and lead time come back with the offer.")}"""
    return page("network.html", "Global network | Hylex Energy Consulting",
                "Houston headquarters with fabrication and engineering hubs in China, Vietnam and Mexico. Capacity, yards, load out and trade position for EPC and owner projects.",
                body, "network.html")


def digital():
    body = f"""{banner(['<a href="index.html">Home</a>', '<a href="services.html">What we do</a>', 'Project controls'],
        "Progress you can see, not progress you are told about",
        "Fabrication reported by piece and by weight, out of the shop's own records, so a program running in three countries reads as one picture rather than four spreadsheets.", "Project controls")}

<section class="s"><div class="wrap"><div class="eb">What you get</div><h2>What is reported, and where it comes from</h2>
<table><tbody>
<tr><td>Progress and weld inch tracking</td><td>Fit up, welding and final check recorded by piece and by kilogram, read from the shop's own workbooks rather than a percentage someone types in</td></tr>
<tr><td>Take off and quantities</td><td>Every sheet of the package read, spools and components counted, weighed and typed against the piping class, with conflicts raised before anyone prices them</td></tr>
<tr><td>NDE and inspection</td><td>Inspection results, hold point releases and repair rates tracked against the ITP as the work happens</td></tr>
<tr><td>Material traceability</td><td>Heat numbers, certificates and release notes tied to the piece, not filed separately and reconciled at the end</td></tr>
<tr><td>Documentation</td><td>A digital manufacturing record book that is built through the job and handed over complete, not assembled in the last week</td></tr>
<tr><td>Reporting</td><td>One progress picture across every hub, with the deadlines and the exceptions, in a brief you can forward</td></tr>
</tbody></table></div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="eb">In use</div><h2>Running systems, not screenshots of a demo</h2>
<p class="aip" style="max-width:720px;margin:0 0 26px">Three views from a working installation. Customer names and commercial figures are masked.</p>
<div class="shots">
<figure class="wide"><img src="img-sys-takeoff.jpg" alt="Bid package take off with spools counted, weighed and typed against the piping class" loading="lazy">
<figcaption><b>Take off from a bid package</b>A 69 page drawing set read sheet by sheet. Every spool typed, counted and weighed against the piping class, with the conflicts raised before pricing.</figcaption></figure>
<figure><img src="img-sys-shopfloor.jpg" alt="Shop floor progress tracker by piece and by weight" loading="lazy">
<figcaption><b>Shop floor</b>Progress by piece and by kilogram, fit up through final check, read from the shop's own workbooks.</figcaption></figure>
<figure><img src="img-sys-pipeline.jpg" alt="Enquiry and package board tied to the mail threads" loading="lazy">
<figcaption><b>Package tracking</b>Every package on one board, updated from the correspondence rather than by hand, with the response time on each.</figcaption></figure>
</div></div></section>

<section class="s" id="how"><div class="wrap"><div class="eb">How it works</div><h2>Why the numbers hold up</h2>
<div class="steps" style="margin-top:8px">
<div><span>01</span><b>From the shop, not about it</b><p>Figures come out of the workbooks the shop already keeps, so reporting does not depend on anyone writing a status email.</p></div>
<div><span>02</span><b>By piece and by weight</b><p>Percent complete is derived from pieces and kilograms through each gate, which is hard to flatter.</p></div>
<div><span>03</span><b>Exceptions first</b><p>What is late, what failed inspection and what is waiting on a decision, ahead of what went fine.</p></div>
<div><span>04</span><b>One picture</b><p>Three hubs, one report. You do not reconcile three formats to find out where the program stands.</p></div>
</div></div></section>

{end_band("Ask for a sample progress report", "We will show you what the weekly looks like on a live package, with the names taken out.",
          ("Send an enquiry", "contact.html"), ("Ask for a sample", f"mailto:{EMAIL}?subject=Sample%20progress%20report"))}"""
    return page("digital.html", "Project controls | Hylex Energy Consulting",
                "Weld inch tracking, progress by piece and by weight from the shop's own records, NDE and inspection against the ITP, material traceability and a digital manufacturing record book.",
                body, "digital.html", [service_ld("Project controls and reporting", "Weld inch tracking, progress by piece and weight, NDE against the ITP, material traceability and digital manufacturing record books.", "/digital")])


def industrial_ai():
    body = f"""{banner(['<a href="index.html">Home</a>', 'Industrial AI'], "The systems an industrial desk runs on",
        "A separate line of work. We build and run the estimating, sales and shop floor systems behind our own fabrication programs, and we set the same systems up for fabricators, suppliers and distributors on their own servers.", "Industrial AI")}

<section class="s"><div class="wrap"><div class="eb">What we build</div><h2>Five things that take the manual work out of a desk</h2>
<table><tbody>
<tr><td>RFQ intake</td><td>Inbound enquiries read, drawings sorted, scope summarised and filed to the job before anyone opens the mail</td></tr>
<tr><td>Take off and estimating</td><td>Every sheet of a bid package read, spools and components counted and weighed, priced against your own past quotes and costs</td></tr>
<tr><td>Pipeline and follow up</td><td>Every enquiry on one board, tied to its mail thread, with open offers and quiet accounts chased on schedule</td></tr>
<tr><td>Shop floor</td><td>Fit up, welding and final check recorded by piece and by weight, from the shop's own workbooks</td></tr>
<tr><td>Reporting</td><td>Pipeline, deadlines and progress in one daily brief instead of four spreadsheets</td></tr>
</tbody></table></div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="eb">In use</div><h2>Running systems, not screenshots of a demo</h2>
<p class="aip" style="max-width:720px;margin:0 0 26px">Three views from a working installation. Customer names and commercial figures are masked.</p>
<div class="shots">
<figure class="wide"><img src="img-sys-takeoff.jpg" alt="Bid package take off with spools counted, weighed and typed against the piping class" loading="lazy">
<figcaption><b>Take off from a bid package</b>A 69 page drawing set read sheet by sheet. Every spool typed, counted and weighed against the piping class, with the conflicts raised before pricing.</figcaption></figure>
<figure><img src="img-sys-pipeline.jpg" alt="Sales pipeline board tied to the mail threads" loading="lazy">
<figcaption><b>Pipeline</b>Every enquiry on one board, updated from the mailbox rather than by hand, with first reply time on each card.</figcaption></figure>
<figure><img src="img-sys-shopfloor.jpg" alt="Shop floor progress tracker by piece and by weight" loading="lazy">
<figcaption><b>Shop floor</b>Progress by piece and by kilogram, fit up through final check, read from the shop's own workbooks.</figcaption></figure>
</div></div></section>

<section class="s" id="agent"><div class="wrap"><div class="eb">AI agent</div><h2>Your own operations agent: server, model, messaging</h2>
<p class="aip" style="max-width:760px">A private agent that lives on your server, reads your systems, and works with your team in the chat app they already use.</p>
<div class="steps" style="margin-top:28px">
<div><span>01</span><b>Private server</b><p>Your cloud account and your data. Read only links to the mailbox, file server, ERP or MES. Scheduled jobs, backups and a watchdog.</p></div>
<div><span>02</span><b>Model with tools</b><p>Reads drawings, enquiries and spreadsheets. Takes off bills of material, drafts proposals, remembers your rules and decisions.</p></div>
<div><span>03</span><b>In your chat app</b><p>Telegram, WhatsApp or Teams. It answers what came in overnight and drafts the clarification list for you to send.</p></div>
<div><span>04</span><b>Human approval</b><p>Nothing goes to a client without a person releasing it. Separate brains per company, no data mixing.</p></div>
</div></div></section>

<section class="s" id="setup" style="background:var(--soft)"><div class="wrap"><div class="eb">How a setup runs</div><h2>From one bid package to a working desk</h2>
<div class="nlist">
<div><b>01 · Trial</b><p>Send one bid package. We return the take off and the clarification list, so you can judge the work before committing to anything.</p></div>
<div><b>02 · Your data</b><p>Past quotes, cost history and the mailbox connected, read only, on your own server.</p></div>
<div><b>03 · One desk first</b><p>Estimating or sales, whichever is costing you most. Running in weeks, not a programme.</p></div>
<div><b>04 · Then the rest</b><p>Shop floor, reporting and the agent added once the first desk is relied on.</p></div>
</div></div></section>

{end_band("Send us one bid package", "We return the take off and a clarification list, so you can judge the work. No system access needed to start.",
          ("Send a package", "contact.html"), ("Ask about a setup", f"mailto:{EMAIL}?subject=Industrial%20AI%20setup"))}"""
    return page("industrial-ai.html", "Industrial AI | Hylex Energy Consulting",
                "Estimating and take off, sales pipeline, shop floor tracking and a private AI agent on your own server, set up for fabricators, suppliers and distributors.",
                body, "industrial-ai.html", [service_ld("Industrial AI systems", "Estimating and take off, sales pipeline, shop floor tracking and a private AI agent, set up for fabricators, suppliers and distributors.", "/industrial-ai")])


def about():
    body = f"""{banner(['<a href="index.html">Home</a>', 'About'], "Fabrication as a managed program, not a purchase order",
        "Hylex Energy Consulting provides end to end project execution support for complex industrial developments, through a global fabrication network, strategic procurement and engineering run out of Houston.", "About")}

<section class="s"><div class="wrap"><div class="aig">
<div><p class="aip" style="margin:0 0 14px">We work with EPC companies and asset owners on fabrication and supply for energy, mining and process projects. Hylex takes complete ownership of fabrication execution from day one, acting as an embedded extension of your organisation.</p>
<p class="aip" style="margin:0 0 14px">That removes the need for in house subject matter experts, vendor management overhead, and the coordination cost that sits between an engineering team and four workshops in three countries.</p>
<p class="aip" style="margin:0">Every enquiry is handled by a principal, from first drawing to delivery.</p></div>
<ul class="cv"><li>Fabrication program management for EPCs and owners</li><li>Engineering, procurement and project controls</li><li>Hubs in China, Vietnam and Mexico</li><li>Chemical, LNG, downstream, power, mining and semiconductor</li><li>Energy Corridor, Houston TX</li></ul></div></div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="eb">How we work</div><h2>What you can hold us to</h2>
<div class="tags">
<div>One contact<span>A principal reads your enquiry and answers it. Nothing is handed to a desk that has not seen the drawings.</span></div>
<div>Straight answers<span>If a shop cannot build it well, we say so rather than route it anyway.</span></div>
<div>One working day<span>Every enquiry gets a reply inside one working day, even when the answer is that we need longer.</span></div>
</div>
{CODES}</div></section>

{end_band("Let us build the future together", "Developing a project, optimising a fabrication strategy, or exploring global sourcing. Send the scope.")}"""
    return page("about.html", "About | Hylex Energy Consulting",
                "Hylex Energy Consulting, Energy Corridor, Houston TX. End to end fabrication program management for EPC companies and asset owners through a global fabrication network.",
                body, "about.html")


def contact():
    body = f"""{banner(['<a href="index.html">Home</a>', 'Contact'], "Let us build the future together",
        "Whether you are developing a world scale energy project, optimising fabrication strategy or exploring global sourcing, send the scope and we reply within one working day.", "Contact")}

<section class="s"><div class="wrap">{FORM}</div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="eb">Direct</div><h2>Other ways to reach us</h2>
<div class="tags">
<div>Email<span><a href="mailto:{EMAIL}" style="color:var(--green-d);font-weight:600">{EMAIL}</a></span></div>
<div>United States<span><a href="tel:+16099170633" style="color:var(--green-d);font-weight:600">{TEL_US}</a><br>Energy Corridor, Houston TX</span></div>
<div>China<span><a href="tel:+8618322780729" style="color:var(--green-d);font-weight:600">{TEL_CN}</a><br>Tianjin</span></div>
</div></div></section>"""
    return page("contact.html", "Contact | Hylex Energy Consulting",
                "Contact Hylex Energy Consulting. Energy Corridor, Houston TX and Tianjin, China. Send drawings, specifications or a material list and we reply within one working day.",
                body, "contact.html")


FAQ = [
    ("What does Hylex do?",
     "We manage fabrication execution end to end for EPC companies and asset owners: engineering, global procurement, fabrication, QA and NDE oversight, documentation and logistics. Houston holds the client interface and the fabrication hubs in China, Vietnam and Mexico carry the capacity."),
    ("Which codes and standards do you build to?",
     "ASME, API, PED, EN and ISO, with coating to ISO 12944 and NORSOK M-501. Pressure equipment is fabricated and tested to ASME, PED and API, and the shop is qualified against your specification before award."),
    ("How is quality controlled?",
     "An inspection and test plan with hold points is agreed up front. Non destructive examination covers VT, MT, PT, RT, UT and PMI, factory acceptance testing is witnessed, third party inspection is available at your option, and a complete digital manufacturing record book is delivered at handover."),
    ("What can the network fabricate?",
     "Pipe spooling at over 250,000 dia-inches a month, structural steel and platework at over 50,000 tons a year, pressure vessels and columns to 8 m diameter and 150 mm wall thickness with single unit weights over 300 tons, and pre assembled modules over 1,000 tons and 32 m long."),
    ("Where do you ship from?",
     "China and Vietnam by sea, including a 312 m private jetty with 10,000 DWT load out and 20 t/m² quay bearing at the Vietnam yard. Mexico serves North American projects by road and rail from Monterrey, an hour and a half from the Texas border."),
    ("How do you deal with tariffs and trade risk?",
     "By sourcing across three regions rather than one. Vietnam carries favourable trade status with North America, Europe and Australia, Mexico sits inside USMCA, and China gives volume and lead time. A trade decision in one region does not reprice the whole package."),
    ("How do I know what progress is real?",
     "Progress is reported by piece and by kilogram from the shop's own workbooks, not as a percentage someone types into a status email. Weld inch tracking, NDE results against the ITP and material traceability are reported in one picture across every hub."),
    ("What do you need in order to quote?",
     "Drawings, datasheets, line lists or an equipment schedule, the specification, and the delivery location and date. If part of that is missing we will tell you what is needed rather than price around it."),
    ("How quickly do you reply?",
     "Within one working day, even when the answer is that we need longer to price it properly."),
]


def faq_page():
    rows = "".join(f'<div><b>{e(q)}</b><p>{e(a)}</p></div>' for q, a in FAQ)
    body = f"""{banner(['<a href="index.html">Home</a>', 'FAQ'], "Questions buyers ask first",
        "What we do, which codes we build to, how quality is controlled, where the work ships from and what we need in order to quote.", "FAQ")}

<section class="s"><div class="wrap"><div class="nlist">{rows}</div>
{CODES}</div></section>

{end_band("Still have a question?", "Send it with the drawings and we will answer both inside one working day.")}"""
    ld = [{"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q,
                           "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]
    return page("faq.html", "FAQ | Hylex Energy Consulting",
                "Codes and standards, quality control and ITP, fabrication capacity, shipping and load out, tariff and trade risk, and what Hylex needs in order to quote.",
                body, "faq.html", ld)


def insights():
    posts = sorted(json.load(open("posts.json")), key=lambda p: p["date"], reverse=True)
    css = ('<style>.ig{display:grid;gap:18px}@media(min-width:800px){.ig{grid-template-columns:1fr 1fr}}'
           '.ic{display:block;border:1px solid var(--line);border-top:3px solid var(--green);background:var(--soft);padding:24px}'
           '.ic h3{font-size:22px;margin:8px 0 10px}.ic p{color:var(--mute);margin:0 0 12px}.ic span{font-weight:600;color:var(--green-d)}'
           '.art p{font-size:18px;line-height:1.75;color:#2a3135;max-width:760px}</style>')
    cards = "".join(
        f'<a class="ic" href="insight-{p["slug"]}.html"><div class="eb">{p["date"]}</div>'
        f'<h3>{e(p["title"])}</h3><p>{e(p["summary"])}</p><span>Read ›</span></a>' for p in posts)
    body = (banner(['<a href="index.html">Home</a>', 'Insights'], "Notes from the desk",
                   "Sourcing fabricated equipment from Asia, landed price, reading a bid package, and what the project control systems actually do.", "Insights")
            + css + f'<section class="s"><div class="wrap"><div class="ig">{cards}</div></div></section>'
            + end_band("Have a scope to place?", "Send the drawings and specification. We reply within one working day."))
    urls = [page("insights.html", "Insights | Hylex Energy Consulting",
                 "Notes on sourcing fabricated equipment from Asia, landed pricing, bid packages and project control systems.",
                 body, "insights.html")]
    for p in posts:
        art = "".join(f"<p>{e(x)}</p>" for x in p["body"])
        pb = (banner(['<a href="index.html">Home</a>', '<a href="insights.html">Insights</a>', e(p["date"])],
                     p["title"], p["summary"], "Insights")
              + css + f'<section class="s"><div class="wrap art">{art}'
              f'<p style="margin-top:28px"><a class="btn p" href="contact.html">Send us your scope</a> '
              f'<a class="btn" href="insights.html">All insights</a></p></div></section>')
        urls.append(page(f'insight-{p["slug"]}.html', f'{p["title"]} | Hylex Energy Consulting', p["summary"],
                         pb, "insights.html"))
    return urls


def notfound():
    body = (banner(['<a href="index.html">Home</a>', 'Not found'], "That page is not here",
                   "The link may be from an older version of this site. The sections below cover everything on it.", "404")
            + """<section class="s"><div class="wrap"><div class="doors">
<div class="door"><div class="eb">What we do</div><h3>Fabrication managed end to end</h3><p>Engineering, procurement, fabrication delivery and project controls for EPCs and owners.</p><div class="lk"><a href="services.html">What we do ›</a><a href="capability.html">Capability ›</a></div></div>
<div class="door"><div class="eb">Global network</div><h3>China, Vietnam and Mexico</h3><p>Three fabrication hubs and a Houston headquarters holding the client interface.</p><div class="lk"><a href="network.html">The network ›</a><a href="contact.html">Contact ›</a></div></div>
</div></div></section>""")
    return page("404.html", "Page not found | Hylex Energy Consulting",
                "That page is not on this site. Global fabrication, procurement and project delivery from Hylex Energy Consulting.", body, "")


# ---------------------------------------------------------------- run
def main():
    urls = [home(), services(), engineering(), procurement(), capability(), network(),
            hub("china"), hub("vietnam"), hub("mexico"), digital(), industrial_ai(), about(), faq_page(), contact()]
    urls += insights()
    notfound()

    open("sitemap.xml", "w").write(
        '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls) + "</urlset>\n")
    open("sitemap.txt", "w").write("\n".join(urls) + "\n")

    open("llms.txt", "w").write(LLMS_HEAD + "\n## Pages\n" + "".join(
        f"- [{t}]({u}): {d}\n" for t, d, u in PAGE_INDEX) + "\n## Contact\n"
        f"- Email {EMAIL}\n- United States {TEL_US}, Energy Corridor, Houston TX\n- China {TEL_CN}, Tianjin\n")

    names = sorted({u.rsplit("/", 1)[-1] for u in urls if u.rsplit("/", 1)[-1]})
    keep = names + ["index", "404", "hylex-logo", "favicon", "img-", "og-card", "robots", "sitemap",
                    "llms", "_vercel", "api/", r"[0-9a-f]{32}\.txt"]
    csp = ("default-src 'self'; img-src 'self' data:; "
           "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
           "font-src 'self' https://fonts.gstatic.com; "
           "script-src 'self' 'unsafe-inline'; "
           "connect-src 'self' https://*.vercel-insights.com; "
           "frame-ancestors 'self'; base-uri 'self'; form-action 'self'")
    cfg = {
        "cleanUrls": True,
        "headers": [
            {"source": "/(.*)", "headers": [
                {"key": "X-Content-Type-Options", "value": "nosniff"},
                {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
                {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
                {"key": "Strict-Transport-Security", "value": "max-age=31536000"},
                {"key": "Content-Security-Policy", "value": csp},
            ]},
            {"source": "/(img-.*|hylex-logo.png|og-card.png|favicon.ico)", "headers": [
                {"key": "Cache-Control", "value": "public, max-age=2592000"}]},
            {"source": "/sitemap.xml", "headers": [
                {"key": "Content-Type", "value": "text/xml; charset=utf-8"},
                {"key": "Content-Disposition", "value": "inline"}]},
            {"source": "/llms.txt", "headers": [
                {"key": "Content-Type", "value": "text/plain; charset=utf-8"}]},
        ],
        "redirects": [{"source": "/((?!" + "|".join(keep) + ").+)", "destination": "/", "permanent": False}],
    }
    open("vercel.json", "w").write(json.dumps(cfg, indent=2) + "\n")
    print("pages", len(urls) + 1)
    for u in urls:
        print("  ", u)


if __name__ == "__main__":
    main()
