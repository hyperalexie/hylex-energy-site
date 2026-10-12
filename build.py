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
/* ---- dropdown nav ---- */
nav .nd{position:relative}
@media(min-width:900px){nav .nd>a{display:inline-flex;align-items:center;height:72px}}
nav .dd{display:none;position:absolute;left:-18px;top:66px;min-width:256px;background:#fff;border:1px solid var(--line);box-shadow:0 14px 30px rgba(0,0,0,.08);padding:8px 0}
nav .dd a{display:block;padding:10px 18px;font-size:15px;color:var(--ink)}
nav .dd a:hover{background:var(--soft);color:var(--green-d)}
@media(min-width:900px){nav .nd:hover .dd,nav .nd:focus-within .dd{display:block}}
nav a.on{color:var(--green-d);font-weight:600}
@media(max-width:899px){
header.open nav .nd{display:block;border-top:1px solid var(--line)}
header.open nav .nd>a{display:block;padding:15px 0;font-size:16px;color:var(--ink);font-weight:600;border:0}
header.open nav .dd{display:block;position:static;min-width:0;border:0;box-shadow:none;padding:0 0 10px}
header.open nav .dd a{padding:9px 0 9px 14px;font-size:15px;color:var(--mute);border:0}
}
/* ---- home hero over photo ---- */
.phero{position:relative;background:var(--ink);overflow:hidden}
.phero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.42}
.phero .wrap{position:relative;padding:72px 20px 64px;color:#fff}
@media(min-width:900px){.phero .wrap{padding:118px 40px 108px}}
.phero .eb{color:#5fd99a}
.phero h1{font-size:clamp(30px,4.2vw,50px);margin:14px 0 18px;max-width:880px;color:#fff}
.phero p{font-size:18px;color:#d7dcdf;max-width:680px;margin:0 0 30px}
.phero .btn{border-color:#fff;color:#fff}.phero .btn.p{background:var(--green);border-color:var(--green)}
/* ---- inner page banner ---- */
.pb{border-bottom:1px solid var(--line);background:var(--soft);padding:40px 0 38px}
@media(min-width:900px){.pb{padding:56px 0 52px}}
.pb h1{font-size:clamp(28px,3.6vw,42px);margin:10px 0 14px;max-width:860px}
.pb p{font-size:18px;color:#39424a;max-width:740px;margin:0}
.crumb{font-size:13px;color:var(--mute)}.crumb a{color:var(--mute)}.crumb a:hover{color:var(--green-d)}
/* ---- key figures ---- */
.kpi{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);margin-top:4px}
@media(min-width:700px){.kpi{grid-template-columns:1fr 1fr}}
@media(min-width:1000px){.kpi.k4{grid-template-columns:repeat(4,1fr)}.kpi.k3{grid-template-columns:repeat(3,1fr)}}
.kpi div{background:#fff;padding:24px}
.kpi b{display:block;font-size:clamp(22px,2.4vw,28px);letter-spacing:-.02em;margin-bottom:6px}
.kpi span{font-size:14px;color:var(--mute);line-height:1.5;display:block}
/* ---- doors / cards ---- */
.doors{display:grid;gap:1px;background:var(--line);border:1px solid var(--line)}
@media(min-width:900px){.doors{grid-template-columns:1fr 1fr}}
.door{background:#fff;padding:30px 28px;display:flex;flex-direction:column}
.door h3{font-size:clamp(20px,2.2vw,24px);margin:10px 0 12px}
.door p{color:#39424a;font-size:16px;margin:0 0 18px;flex:1}
.door .lk{display:flex;flex-wrap:wrap;gap:10px}
.door .lk a{font-weight:600;font-size:15px;color:var(--green-d);border-bottom:2px solid var(--line);padding-bottom:3px}
.door .lk a:hover{border-color:var(--green)}
/* ---- photo cards ---- */
.pcards{display:grid;gap:22px}
@media(min-width:700px){.pcards{grid-template-columns:1fr 1fr}}
@media(min-width:1000px){.pcards.p3{grid-template-columns:repeat(3,1fr)}}
.pcards figure{margin:0;border:1px solid var(--line);background:#fff;display:flex;flex-direction:column}
.pcards img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.pcards figcaption{padding:18px 20px 20px}
.pcards figcaption b{display:block;font-size:18px;margin-bottom:6px}
.pcards figcaption p{margin:0;font-size:15px;color:var(--mute)}
.pcards figcaption ul{margin:10px 0 0;padding-left:18px;font-size:15px;color:var(--mute)}
.pcards figcaption li{padding:2px 0}
/* ---- split: photo beside text ---- */
.split{display:grid;gap:30px;align-items:center}
@media(min-width:900px){.split{grid-template-columns:1fr 1fr}.split.rev>div:first-child{order:2}}
.split img{width:100%;height:auto;display:block;border:1px solid var(--line)}
.split h2{margin-bottom:14px}
.split p{font-size:17px;color:#39424a}
/* ---- screenshots ---- */
.shots{display:grid;gap:26px;margin-top:8px}
@media(min-width:900px){.shots{grid-template-columns:1fr 1fr}.shots figure.wide{grid-column:1/-1}}
.shots figure{margin:0;border:1px solid var(--line);background:var(--soft)}
.shots img{display:block;width:100%;height:auto;border-bottom:1px solid var(--line)}
.shots figcaption{padding:14px 18px;font-size:14px;color:var(--mute)}
.shots figcaption b{display:block;color:var(--ink);font-size:16px;margin-bottom:4px;font-weight:600}
/* ---- numbered / detail list ---- */
.nlist{display:grid;gap:1px;background:var(--line);border:1px solid var(--line)}
.nlist div{background:#fff;padding:22px 24px;display:grid;gap:4px 18px}
@media(min-width:800px){.nlist div{grid-template-columns:200px 1fr;align-items:baseline}}
.nlist b{font-size:16px}.nlist p{margin:0;color:var(--mute);font-size:15px}
.nlist ul{margin:0;padding-left:18px;color:var(--mute);font-size:15px}.nlist li{padding:2px 0}
/* ---- tag grid ---- */
.tags{display:grid;gap:1px;background:var(--line);border:1px solid var(--line)}
@media(min-width:600px){.tags{grid-template-columns:1fr 1fr}}
@media(min-width:900px){.tags{grid-template-columns:repeat(3,1fr)}}
.tags div{background:#fff;padding:20px 22px;font-weight:600;font-size:16px}
.tags span{display:block;font-weight:400;font-size:14px;color:var(--mute);margin-top:4px}
/* ---- shared bits ---- */
.codes{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:baseline;margin-top:26px;padding:14px 18px;background:var(--soft);border-left:3px solid var(--green);font-size:14px}
.codes span{color:var(--mute)}.codes b{font-weight:600;letter-spacing:.01em}
.aig{display:grid;gap:34px}@media(min-width:900px){.aig{grid-template-columns:1fr 1fr;align-items:start}}
.aip{font-size:17px;color:#39424a}
ul.cv{list-style:none;margin:0;padding:0;background:var(--ink);color:#fff}
ul.cv li{padding:13px 20px;border-top:1px solid #2b3236;font-size:15px}ul.cv li:first-child{border-top:0}
/* ---- dark cta band ---- */
.end h2{font-size:clamp(24px,2.8vw,32px)}
.end .wrap{display:grid;gap:22px}@media(min-width:900px){.end .wrap{grid-template-columns:1.4fr 1fr;align-items:center}}
.end p{color:#aeb6bb;margin:10px 0 0}
.end .cta{display:flex;flex-wrap:wrap;gap:12px}@media(min-width:900px){.end .cta{justify-content:flex-end}}
.end .btn{border-color:#fff;color:#fff}.end .btn.p{background:var(--green);border-color:var(--green);color:#fff}
/* ---- footer columns ---- */
footer{border-top:1px solid var(--line);padding:46px 0 34px;font-size:14px;color:var(--mute)}
footer .wrap{display:block}
footer .fg{display:grid;gap:26px}@media(min-width:800px){footer .fg{grid-template-columns:repeat(4,1fr)}}
footer b{display:block;color:var(--ink);font-size:13px;letter-spacing:.06em;text-transform:uppercase;margin-bottom:10px}
footer a{display:block;padding:4px 0;color:var(--mute)}footer a:hover{color:var(--green-d)}
footer span{display:block;padding:4px 0}
footer .fb{margin-top:30px;padding-top:18px;border-top:1px solid var(--line);display:flex;flex-wrap:wrap;gap:8px 18px;justify-content:space-between}
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
    ("About", "about.html", []),
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
            '<a href="index.html"><img src="hylex-logo.png" alt="Hylex Energy Consulting"></a>'
            f'<nav>{items}</nav>'
            '<div class="hr"><a class="btn p" href="contact.html">Send an enquiry</a>'
            '<button type="button" class="burger" aria-label="Menu" aria-expanded="false"><i></i><i></i><i></i></button>'
            '</div></div></header>')


FOOTER = f"""<footer><div class="wrap"><div class="fg">
<div><b>What we do</b><a href="services.html">Fabrication programs</a><a href="engineering.html">Engineering</a><a href="procurement.html">Procurement</a><a href="digital.html">Project controls</a></div>
<div><b>Capability</b><a href="capability.html">Fabrication scope</a><a href="capability.html#qa">Quality and inspection</a><a href="capability.html#sectors">Sectors</a></div>
<div><b>Global network</b><a href="hub-china.html">China hub</a><a href="hub-vietnam.html">Vietnam hub</a><a href="hub-mexico.html">Mexico hub</a><a href="network.html#houston">Houston</a></div>
<div><b>Contact</b><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:+16099170633">{TEL_US}</a><a href="tel:+8618322780729">{TEL_CN}</a><span>Energy Corridor, Houston TX</span><span>Tianjin, China</span></div>
</div><div class="fb"><span>© 2026 Hylex Energy Consulting</span><span>Driving projects from concept to commissioning</span></div></div></footer>"""


def end_band(h2, p, primary=("Send an enquiry", "contact.html"),
             secondary=("Book a call", f"mailto:{EMAIL}?subject=Call%20request")):
    return (f'<section class="end"><div class="wrap"><div><h2>{e(h2)}</h2><p>{e(p)}</p></div>'
            f'<div class="cta"><a class="btn p" href="{primary[1]}">{e(primary[0])}</a>'
            f'<a class="btn" href="{secondary[1]}">{e(secondary[0])}</a></div></div></section>')


OG = f"{SITE}/og-card.png"


def page(fn, title, desc, body, active, ld=None):
    url = f"{SITE}/" + ("" if fn == "index.html" else fn.replace(".html", ""))
    ldj = "".join(f'<script type="application/ld+json">{json.dumps(x, separators=(",", ":"))}</script>' for x in (ld or []))
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="/img-icon-32.png"><link rel="icon" type="image/png" sizes="48x48" href="/img-icon-48.png"><link rel="icon" type="image/png" sizes="192x192" href="/img-icon-192.png"><link rel="apple-touch-icon" href="/img-icon-180.png">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Hylex Energy Consulting">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{OG}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{OG}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{BASE_CSS}{EXTRA_CSS}</style></head>
<body>
{ldj}
{header(active)}
{body}
{FOOTER}
{TAIL}</body></html>"""
    open(fn, "w").write(doc)
    return url


def banner(crumb, h1, p, eyebrow):
    return (f'<section class="pb"><div class="wrap"><div class="crumb">{" · ".join(crumb)}</div>'
            f'<div class="eb" style="margin-top:14px">{e(eyebrow)}</div>'
            f'<h1>{e(h1)}</h1><p>{e(p)}</p></div></section>')


def kpis(pairs, cls="k4"):
    return f'<div class="kpi {cls}">' + "".join(
        f"<div><b>{e(b)}</b><span>{e(s)}</span></div>" for b, s in pairs) + "</div>"


CODES = ('<div class="codes"><span>Fabricated and tested to</span>'
         '<b>ASME · API · PED · EN · ISO · NORSOK M-501 · ISO 12944</b></div>')


# ---------------------------------------------------------------- pages
def home():
    body = f"""<section class="phero"><img src="img-yard.jpg" alt="Fabrication yard with pipe racks and modules under assembly">
<div class="wrap"><div class="eb">Hylex Energy Consulting</div>
<h1>Global fabrication, procurement, engineering and project delivery</h1>
<p>We take complete ownership of the fabrication execution process for EPC companies and asset owners, from shop readiness and sourcing through QA, NDE, FAT and logistics, delivered through hubs in China, Vietnam and Mexico.</p>
<div class="cta"><a class="btn p" href="contact.html">Send an enquiry</a><a class="btn" href="services.html">What we do</a></div></div></section>

<section class="s"><div class="wrap"><div class="eb">Comprehensive services</div><h2>One partner, complete project lifecycle support</h2>
<div class="doors">
<div class="door"><div class="eb">01 · Engineering and design</div><h3>Fabrication ready execution</h3>
<p>Detailed shop drawings, 3D models, clash checks and datasheets, from FEED through as built.</p>
<div class="lk"><a href="engineering.html">Engineering ›</a></div></div>
<div class="door"><div class="eb">02 · Procurement</div><h3>Global sourcing under one owner</h3>
<p>Vendor qualification, audits, commercial negotiation, expediting and logistics coordination across China, Vietnam and Mexico.</p>
<div class="lk"><a href="procurement.html">Procurement ›</a></div></div>
<div class="door"><div class="eb">03 · Fabrication delivery</div><h3>Pipe spools to complete modules</h3>
<p>Pipe spooling, pressure vessels, structural steel, platework and turnkey skid systems through a network of qualified workshops.</p>
<div class="lk"><a href="capability.html">Capability ›</a><a href="network.html">The hubs ›</a></div></div>
<div class="door"><div class="eb">04 · Project controls</div><h3>Progress you can see</h3>
<p>Real time weld inch tracking, fabrication dashboards, NDE reporting, material traceability and digital manufacturing record books.</p>
<div class="lk"><a href="digital.html">Project controls ›</a></div></div>
</div></div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="eb">Scale</div><h2>What the network delivers</h2>
{kpis([("250,000+", "Dia-inches of pipe spooling per month across the workshops"),
       ("50,000+", "Tons a year of structural steel and platework"),
       ("8 m / 150 mm", "Vessel diameter and wall thickness, single units over 300 tons"),
       ("1,000+ tons", "Pre assembled modules up to 32 m in length")])}
<p style="margin-top:24px"><a class="btn" href="capability.html">Full fabrication scope</a></p></div></section>

<section class="s"><div class="wrap"><div class="eb">Global presence</div><h2>Hubs across North America and Asia</h2>
<p class="aip" style="max-width:720px;margin:0 0 28px">Houston holds the client interface, the engineering coordination and the procurement. The fabrication hubs carry the capacity, the yards and the load out.</p>
<div class="pcards p3">
<figure><img src="img-hub-china.jpg" alt="China fabrication and engineering hub" loading="lazy"><figcaption><b>China</b><p>Full fabrication capability, heavy yard and mega module assembly, procurement and engineering support.</p></figcaption></figure>
<figure><img src="img-hub-vietnam.jpg" alt="Vietnam fabrication hub yard and jetty" loading="lazy"><figcaption><b>Vietnam</b><p>Heavy structural fabrication, modular assembly and a private jetty with deep sea load out. Tariff resilient.</p></figcaption></figure>
<figure><img src="img-hub-mexico.jpg" alt="Mexico fabrication facility at Monterrey" loading="lazy"><figcaption><b>Mexico</b><p>Monterrey pipe spooling and industrial coating, 1.5 hours from the Texas border, inside USMCA.</p></figcaption></figure>
</div>
<p style="margin-top:24px"><a class="btn" href="network.html">The global network</a></p></div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="eb">Why it matters</div><h2>Fabrication stops being your problem to manage</h2>
<div class="tags">
<div>Zero internal burden<span>No procurement, inspection or fabrication specialists needed on your staff.</span></div>
<div>Single point accountability<span>One team owns cost, schedule, quality and compliance.</span></div>
<div>Faster mobilisation<span>Projects launch without procurement delays or technical onboarding.</span></div>
</div>
{CODES}</div></section>

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
                body, "services.html")


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
                body, "engineering.html")


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
                body, "procurement.html")


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
                body, "capability.html")


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
        name="Vietnam", title="Vietnam fabrication and engineering hub", img="img-hub-vietnam.jpg",
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
<figure><img src="img-hub-vietnam.jpg" alt="Vietnam fabrication hub" loading="lazy"><figcaption><b>Vietnam</b><p>Heavy structural and modular assembly on a 195,000 m² yard with a 312 m private jetty. Tariff resilient.</p><p style="margin-top:10px"><a href="hub-vietnam.html" style="color:var(--green-d);font-weight:600">Vietnam hub ›</a></p></figcaption></figure>
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
        "Fabrication reported by piece and by weight, from the shop's own records. The same systems run our estimating and our enquiry desk, and we set them up for fabricators, distributors and procurement teams.", "Project controls and digital")}

<section class="s"><div class="wrap"><div class="eb">What you get</div><h2>Five things that take the manual work out of a program</h2>
<table><tbody>
<tr><td>Enquiry intake</td><td>Inbound enquiries read, drawings sorted, scope summarised and filed to the job before anyone opens the mail</td></tr>
<tr><td>Take off and estimating</td><td>Every sheet of a bid package read, spools and components counted and weighed, priced against real cost history</td></tr>
<tr><td>Progress and weld inch tracking</td><td>Fit up, welding and final check recorded by piece and by kilogram, from the shop's own workbooks</td></tr>
<tr><td>NDE and documentation</td><td>Inspection results, material traceability and a digital manufacturing record book built as the work happens</td></tr>
<tr><td>Reporting</td><td>Pipeline, deadlines and progress in one daily brief instead of four spreadsheets</td></tr>
</tbody></table></div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="eb">In use</div><h2>Running systems, not screenshots of a demo</h2>
<p class="aip" style="max-width:720px;margin:0 0 26px">Three views from a working installation. Customer names and commercial figures are masked.</p>
<div class="shots">
<figure class="wide"><img src="img-sys-takeoff.jpg" alt="Bid package take off with spools counted, weighed and typed against the piping class" loading="lazy">
<figcaption><b>Take off from a bid package</b>A 69 page drawing set read sheet by sheet. Every spool typed, counted and weighed against the piping class, with the conflicts raised before pricing.</figcaption></figure>
<figure><img src="img-sys-shopfloor.jpg" alt="Shop floor progress tracker by piece and by weight" loading="lazy">
<figcaption><b>Shop floor</b>Progress by piece and by kilogram, fit up through final check, read from the shop's own workbooks.</figcaption></figure>
<figure><img src="img-sys-pipeline.jpg" alt="Enquiry pipeline board tied to the mail threads" loading="lazy">
<figcaption><b>Enquiry pipeline</b>Every enquiry on one board, updated from the mailbox rather than by hand, with first reply time on each card.</figcaption></figure>
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
          ("Send a package", "contact.html"), ("Ask about a setup", f"mailto:{EMAIL}?subject=Project%20controls"))}"""
    return page("digital.html", "Project controls and digital | Hylex Energy Consulting",
                "Weld inch tracking, fabrication dashboards, NDE reporting, digital manufacturing record books, and bid package take off and estimating systems set up on your own server.",
                body, "digital.html")


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
            hub("china"), hub("vietnam"), hub("mexico"), digital(), about(), contact()]
    urls += insights()
    notfound()

    open("sitemap.xml", "w").write(
        '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls) + "</urlset>\n")
    open("sitemap.txt", "w").write("\n".join(urls) + "\n")

    names = sorted({u.rsplit("/", 1)[-1] for u in urls if u.rsplit("/", 1)[-1]})
    keep = names + ["index", "404", "hylex-logo", "favicon", "img-", "og-card", "robots", "sitemap",
                    "api/", r"[0-9a-f]{32}\.txt"]
    cfg = {"cleanUrls": True,
           "redirects": [{"source": "/((?!" + "|".join(keep) + ").+)", "destination": "/", "permanent": False}]}
    open("vercel.json", "w").write(json.dumps(cfg, indent=2) + "\n")
    print("pages", len(urls) + 1)
    for u in urls:
        print("  ", u)


if __name__ == "__main__":
    main()
