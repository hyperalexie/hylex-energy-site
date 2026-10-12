#!/usr/bin/env python3
"""Build hylexenergy.com. Multi page: representation and industrial AI.

Run: python3 build.py   (writes the html files, sitemap and the vercel redirect whitelist)
Shared css, chat widget and tracking live in parts/. Insights come from posts.json.
"""
import json, html, re, datetime, os, io

SITE = "https://www.hylexenergy.com"
EMAIL = "amac@hylexenergy.com"
e = html.escape
TODAY = datetime.date.today().isoformat()

BASE_CSS = open("parts/base.css").read()
TAIL = open("parts/tail.html").read()
FORM = open("parts/form.html").read()

EXTRA_CSS = r"""
/* ---- dropdown nav ---- */
nav .nd{position:relative}
@media(min-width:900px){nav .nd>a{display:inline-flex;align-items:center;height:72px}}
nav .dd{display:none;position:absolute;left:-18px;top:66px;min-width:248px;background:#fff;border:1px solid var(--line);box-shadow:0 14px 30px rgba(0,0,0,.08);padding:8px 0}
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
/* ---- inner page banner ---- */
.pb{border-bottom:1px solid var(--line);background:var(--soft);padding:40px 0 38px}
@media(min-width:900px){.pb{padding:56px 0 52px}}
.pb h1{font-size:clamp(28px,3.6vw,42px);margin:10px 0 14px;max-width:820px}
.pb p{font-size:18px;color:#39424a;max-width:720px;margin:0}
.crumb{font-size:13px;color:var(--mute)}.crumb a{color:var(--mute)}.crumb a:hover{color:var(--green-d)}
/* ---- home doors ---- */
.doors{display:grid;gap:1px;background:var(--line);border:1px solid var(--line)}
@media(min-width:900px){.doors{grid-template-columns:1fr 1fr}}
.door{background:#fff;padding:34px 30px 30px;display:flex;flex-direction:column}
.door h3{font-size:clamp(22px,2.4vw,27px);margin:10px 0 14px}
.door p{color:#39424a;font-size:16px;margin:0 0 20px;flex:1}
.door .lk{display:flex;flex-wrap:wrap;gap:10px}
.door .lk a{font-weight:600;font-size:15px;color:var(--green-d);border-bottom:2px solid var(--line);padding-bottom:3px}
.door .lk a:hover{border-color:var(--green)}
/* ---- shared bits ---- */
.codes{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:baseline;margin-top:26px;padding:14px 18px;background:var(--soft);border-left:3px solid var(--green);font-size:14px}
.codes span{color:var(--mute)}.codes b{font-weight:600;letter-spacing:.01em}
.aig{display:grid;gap:34px}@media(min-width:900px){.aig{grid-template-columns:1fr 1fr;align-items:start}}
.aip{font-size:17px;color:#39424a}
ul.cv{list-style:none;margin:0;padding:0;background:var(--ink);color:#fff}
ul.cv li{padding:13px 20px;border-top:1px solid #2b3236;font-size:15px}ul.cv li:first-child{border-top:0}
/* ---- screenshots ---- */
.shots{display:grid;gap:26px;margin-top:8px}
@media(min-width:900px){.shots{grid-template-columns:1fr 1fr}.shots figure.wide{grid-column:1/-1}}
.shots figure{margin:0;border:1px solid var(--line);background:var(--soft)}
.shots img{display:block;width:100%;height:auto;border-bottom:1px solid var(--line)}
.shots figcaption{padding:14px 18px;font-size:14px;color:var(--mute)}
.shots figcaption b{display:block;color:var(--ink);font-size:16px;margin-bottom:4px;font-weight:600}
/* ---- numbered list ---- */
.nlist{display:grid;gap:1px;background:var(--line);border:1px solid var(--line)}
.nlist div{background:#fff;padding:22px 24px;display:grid;gap:4px 18px}
@media(min-width:800px){.nlist div{grid-template-columns:150px 1fr;align-items:baseline}}
.nlist b{font-size:16px}.nlist p{margin:0;color:var(--mute);font-size:15px}
/* ---- dark cta band ---- */
.end h2{font-size:clamp(24px,2.8vw,32px)}
.end .wrap{display:grid;gap:22px}@media(min-width:900px){.end .wrap{grid-template-columns:1.4fr 1fr;align-items:center}}
.end p{color:#aeb6bb;margin:10px 0 0}
.end .cta{justify-content:flex-start}@media(min-width:900px){.end .cta{justify-content:flex-end}}
.end .btn{border-color:#fff;color:#fff}.end .btn.p{background:var(--green);border-color:var(--green);color:#fff}
/* ---- footer columns ---- */
footer{border-top:1px solid var(--line);padding:46px 0 34px;font-size:14px;color:var(--mute)}
footer .wrap{display:block}
footer .fg{display:grid;gap:26px}@media(min-width:800px){footer .fg{grid-template-columns:repeat(4,1fr)}}
footer b{display:block;color:var(--ink);font-size:13px;letter-spacing:.06em;text-transform:uppercase;margin-bottom:10px}
footer a{display:block;padding:4px 0;color:var(--mute)}footer a:hover{color:var(--green-d)}
footer .fb{margin-top:30px;padding-top:18px;border-top:1px solid var(--line);display:flex;flex-wrap:wrap;gap:8px 18px;justify-content:space-between}
"""

# ---------------------------------------------------------------- nav
NAV = [
    ("Representation", "representation.html", [
        ("What we supply", "representation.html#scope"),
        ("How an order runs", "representation.html#how"),
        ("Assurance", "representation.html#assurance"),
        ("For manufacturers", "principals.html"),
    ]),
    ("Industrial AI", "digital.html", [
        ("What we build", "digital.html#build"),
        ("Your own agent", "digital.html#agent"),
        ("How a setup runs", "digital.html#setup"),
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
    return (
        '<header><div class="wrap">'
        '<a href="index.html"><img src="hylex-logo.png" alt="Hylex Energy Consulting"></a>'
        f'<nav>{items}</nav>'
        '<div class="hr"><a class="btn p" href="contact.html">Send an enquiry</a>'
        '<button type="button" class="burger" aria-label="Menu" aria-expanded="false"><i></i><i></i><i></i></button>'
        '</div></div></header>'
    )


FOOTER = f"""<footer><div class="wrap"><div class="fg">
<div><b>Representation</b><a href="representation.html#scope">What we supply</a><a href="representation.html#how">How an order runs</a><a href="representation.html#assurance">Assurance</a><a href="principals.html">For manufacturers</a></div>
<div><b>Industrial AI</b><a href="digital.html#build">What we build</a><a href="digital.html#agent">Your own agent</a><a href="digital.html#setup">How a setup runs</a></div>
<div><b>Company</b><a href="about.html">About</a><a href="insights.html">Insights</a><a href="contact.html">Contact</a></div>
<div><b>Contact</b><a href="mailto:{EMAIL}">{EMAIL}</a><span>Houston, Texas</span></div>
</div><div class="fb"><span>© 2026 Hylex Energy Consulting</span><span>Representation and industrial AI for energy and process projects</span></div></div></footer>"""


def end_band(h2, p, primary=("Send an enquiry", "contact.html"), secondary=("Book a call", f"mailto:{EMAIL}?subject=Call%20request")):
    return (f'<section class="end"><div class="wrap"><div><h2>{e(h2)}</h2><p>{e(p)}</p></div>'
            f'<div class="cta"><a class="btn p" href="{primary[1]}">{e(primary[0])}</a>'
            f'<a class="btn" href="{secondary[1]}">{e(secondary[0])}</a></div></div></section>')


OG_DEFAULT = f"{SITE}/og-card.png"


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
<meta property="og:url" content="{url}"><meta property="og:image" content="{OG_DEFAULT}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{OG_DEFAULT}">
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
    c = ' · '.join(crumb)
    return (f'<section class="pb"><div class="wrap"><div class="crumb">{c}</div>'
            f'<div class="eb" style="margin-top:14px">{e(eyebrow)}</div>'
            f'<h1>{e(h1)}</h1><p>{e(p)}</p></div></section>')


# ---------------------------------------------------------------- shared blocks
SCOPE_TABLE = """<table><thead><tr><th>Category</th><th>What we supply</th></tr></thead><tbody>
<tr><td>Thermoplastic piping</td><td>PP, PVDF and HDPE spools, fittings and tanks, welded and pressure tested</td></tr>
<tr><td>Composite</td><td>GRP and FRP pipe, ducting, tanks and scrubber internals</td></tr>
<tr><td>Metallic fabrication</td><td>Carbon steel, stainless, duplex and nickel alloy spools, vessels and structures</td></tr>
<tr><td>Equipment</td><td>Pumps, filters, skids and packaged units to your datasheets</td></tr>
<tr><td>Valves and instruments</td><td>Isolation and control valves, instruments, cable and panels</td></tr>
<tr><td>Oilfield</td><td>Completion, wellhead and flowline products</td></tr>
</tbody></table>"""

CODES = ('<div class="codes"><span>Work placed with shops qualified to</span>'
         '<b>ASME VIII · ASME B31.3 · ASME IX · AWS D1.1 · EN 1090 · ISO 3834 · DVS 2207 · ISO 14692</b></div>')


# ---------------------------------------------------------------- pages
def home():
    body = f"""<section class="hero"><div class="wrap g">
<div><div class="eb">Hylex Energy Consulting</div>
<h1>Representation and industrial AI</h1>
<p>Two lines of work from one desk. We represent manufacturers into the energy and process accounts we handle every day, and we build the sales and operations systems industrial companies run on.</p>
<div class="cta"><a class="btn p" href="contact.html">Send an enquiry</a><a class="btn" href="principals.html">For manufacturers</a></div></div>
<div class="req"><h2>Typical requests</h2><ul>
<li>Thermoplastic piping: PP, PVDF, HDPE</li><li>GRP and FRP pipe, ducts and tanks</li><li>Special alloy and lined fabrication</li><li>Packaged equipment to datasheet</li><li>Valves, instruments and electrical</li><li>Oilfield and completion products</li></ul></div>
</div></section>

<section class="s"><div class="wrap"><div class="eb">Two sides of the desk</div><h2>What Hylex does</h2>
<div class="doors">
<div class="door"><div class="eb">01 · Representation</div>
<h3>We carry a manufacturer's product to the buyer who specifies it</h3>
<p>Buyers get the part of a package that falls outside one shop's scope, quoted as one offer and followed through to delivery. Manufacturers get a desk already inside the account, reading the specification before the enquiry reaches them.</p>
<div class="lk"><a href="representation.html">For buyers ›</a><a href="principals.html">For manufacturers ›</a></div></div>
<div class="door"><div class="eb">02 · Industrial AI</div>
<h3>The systems a sales desk and a shop floor run on</h3>
<p>Bid package take off, estimating from your own cost history, pipeline and follow up, shop floor progress by piece, and a private agent on your own server that works with your team in the chat app they already use.</p>
<div class="lk"><a href="digital.html">What we build ›</a><a href="digital.html#setup">How a setup runs ›</a></div></div>
</div></div></section>

<section class="s" id="scope" style="background:var(--soft)"><div class="wrap"><div class="eb">Scope</div><h2>The parts of a package one shop rarely covers</h2>
{SCOPE_TABLE}
<p style="margin-top:24px"><a class="btn" href="representation.html">How an order runs</a></p></div></section>

<section class="s"><div class="wrap"><div class="eb">Who we work with</div><h2>The same buyers, a wider scope</h2>
<div class="who"><div><b>EPC contractors</b><p>Packages that span materials and disciplines.</p></div><div><b>Equipment OEMs</b><p>Fabricated and bought out content for your units.</p></div><div><b>Operators</b><p>Spares, replacements and site upgrades.</p></div></div>
{CODES}</div></section>

{end_band("Have a scope that does not fit?", "Send the drawings and specification. We reply within one working day.")}"""
    ld = [
        {"@context": "https://schema.org", "@type": "Organization", "name": "Hylex Energy Consulting",
         "url": SITE + "/", "logo": f"{SITE}/img-icon-512.png", "email": EMAIL,
         "address": {"@type": "PostalAddress", "addressLocality": "Houston", "addressRegion": "TX", "addressCountry": "US"}},
        {"@context": "https://schema.org", "@type": "WebSite", "name": "Hylex Energy Consulting", "url": SITE + "/"},
    ]
    return page("index.html", "Hylex Energy Consulting | Representation and industrial AI",
                "Hylex represents manufacturers into energy and process accounts and builds the sales and operations systems industrial companies run on. Houston, Texas.",
                body, "index.html", ld)


def representation():
    body = f"""{banner(['<a href="index.html">Home</a>', 'Representation'], "The parts of a package one shop rarely covers",
        "When part of a package falls outside your fabricator's scope, we find the shop that does it. We agree the specification, follow the work through fabrication and inspection, and deliver it with the rest of the job.", "Representation · for buyers")}

<section class="s" id="scope"><div class="wrap"><div class="eb">Scope</div><h2>What we supply</h2>
{SCOPE_TABLE}</div></section>

<section class="s" id="how" style="background:var(--soft)"><div class="wrap"><div class="eb">How we work</div><h2>One contract, managed to delivery</h2>
<div class="steps">
<div><span>01</span><b>Send the scope</b><p>Drawings, datasheets and specifications, as you would to any bidder.</p></div>
<div><span>02</span><b>We qualify the shop</b><p>Capability, references and quality system checked against your spec.</p></div>
<div><span>03</span><b>One offer</b><p>Price, lead time and inspection plan in one proposal.</p></div>
<div><span>04</span><b>Followed through</b><p>Inspection, documentation and shipping managed by us.</p></div>
</div></div></section>

<section class="s" id="assurance"><div class="wrap"><div class="eb">Assurance</div><h2>How your order is protected</h2>
<div class="who five">
<div><b>Shop qualified first</b><p>Capability, quality system and welder qualifications checked against your specification before award.</p></div>
<div><b>ITP with hold points</b><p>Inspection and test plan agreed up front. Nothing moves past a hold point without release.</p></div>
<div><b>Independent inspection</b><p>Third party inspection by SGS, Bureau Veritas or TÜV at your option.</p></div>
<div><b>Payment tied to release</b><p>Milestones paid against inspection release, not against the calendar.</p></div>
<div><b>Full records</b><p>Material certificates, NDT and test reports in one manufacturing record book at shipment.</p></div>
</div>
{CODES}</div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="eb">Who we work with</div><h2>The same buyers, a wider scope</h2>
<div class="who"><div><b>EPC contractors</b><p>Packages that span materials and disciplines.</p></div><div><b>Equipment OEMs</b><p>Fabricated and bought out content for your units.</p></div><div><b>Operators</b><p>Spares, replacements and site upgrades.</p></div></div></div></section>

{end_band("Send us the scope", "Drawings and specification, as you would to any bidder. We reply within one working day.")}"""
    return page("representation.html", "Representation | Hylex Energy Consulting",
                "Thermoplastic and composite piping, special alloy fabrication, packaged equipment, valves and oilfield products. One offer, qualified shops, inspection and documentation managed to delivery.",
                body, "representation.html")


def principals():
    body = f"""{banner(['<a href="index.html">Home</a>', '<a href="representation.html">Representation</a>', 'For manufacturers'],
        "Representation into accounts a portal will not reach",
        "If you build equipment, piping, valves or oilfield products and you are not in front of the people who write the specification, that is the work we do. We carry your product into enquiries we are already handling.", "For manufacturers")}

<section class="s"><div class="wrap"><div class="eb">What representation covers</div><h2>From the enquiry to the released order</h2>
<div class="nlist">
<div><b>Enquiry</b><p>We are in the account when the package is being split. Your product goes in at that point, not after the bid list is closed.</p></div>
<div><b>Specification</b><p>We read the specification and the drawings against what you actually build, and raise the conflicts before anyone prices them.</p></div>
<div><b>Quotation</b><p>Your offer presented in the buyer's format, with the commercial terms and the inspection plan the buyer expects to see.</p></div>
<div><b>Negotiation</b><p>Clarifications, technical queries and the commercial round handled in the buyer's language and time zone.</p></div>
<div><b>Order</b><p>Placed with you directly, or placed through Hylex where the buyer wants one counterparty for the whole package.</p></div>
<div><b>Follow through</b><p>Inspection release, documentation and shipping chased, so the account does not go quiet on you.</p></div>
</div></div></section>

<section class="s" id="structure" style="background:var(--soft)"><div class="wrap"><div class="eb">Structure</div><h2>Two ways to appoint us</h2>
<div class="who"><div><b>As your representative</b><p>You quote and you contract. We hold the account, present the offer and carry the order through. Commission on what ships.</p></div>
<div><b>As the counterparty</b><p>Hylex takes the order and places it with you. The buyer gets one contract for a package that spans several shops, and you get a clean scope.</p></div>
<div><b>Exclusive or not</b><p>By territory, by product line or by named account. We will tell you where we already have a competing line rather than carry both quietly.</p></div></div></div></section>

<section class="s"><div class="wrap"><div class="eb">Fit</div><h2>What we need, what you get</h2>
<div class="aig">
<div><h3 style="font-size:19px;margin-bottom:12px">What we need from you</h3>
<div class="nlist">
<div><b>Product basis</b><p>Datasheets, standard range and the price basis you want quoted.</p></div>
<div><b>Lead time</b><p>Honest shop loading, so dates we give the buyer survive the order.</p></div>
<div><b>Quality system</b><p>Approvals, code stamps and welder qualifications we can put in front of a QA reviewer.</p></div>
<div><b>A contact</b><p>One person who answers inside a working day during a bid.</p></div>
</div></div>
<div><h3 style="font-size:19px;margin-bottom:12px">What you get</h3>
<div class="nlist">
<div><b>Qualified enquiries</b><p>Scope read and checked against your capability before it reaches your desk.</p></div>
<div><b>Fewer dead bids</b><p>We say no to what you cannot build well, instead of passing it on.</p></div>
<div><b>Nothing chased by hand</b><p>Open offers and quiet accounts followed up on schedule by the systems we run.</p></div>
<div><b>A reading of the account</b><p>Who decides, what they compare on, and where your price actually sits.</p></div>
</div></div></div></div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="eb">Where</div><h2>Markets we sell into</h2>
<div class="who"><div><b>Sectors</b><p>Energy, mining, LNG, power, chemical and process plant.</p></div>
<div><b>Regions</b><p>The Americas, Europe, Australia and Asia.</p></div>
<div><b>Buyers</b><p>EPC contractors, equipment OEMs and operators.</p></div></div></div></section>

{end_band("Send us your product line", "Datasheets and the markets you want covered. We will tell you straight whether we can sell it.", ("Send the details", "contact.html"))}"""
    return page("principals.html", "For manufacturers | Hylex Energy Consulting",
                "Representation for manufacturers of fabricated equipment, piping, valves and oilfield products into EPC, OEM and operator accounts in the Americas, Europe, Australia and Asia.",
                body, "principals.html")


def digital():
    body = f"""{banner(['<a href="index.html">Home</a>', 'Industrial AI'], "The systems an industrial sales desk runs on",
        "Built and run in a working fabrication business first, then set up for yours. Bid take off, estimating, pipeline, shop floor and a private agent on your own server.", "Industrial AI")}

<section class="s" id="build"><div class="wrap"><div class="eb">What we build</div><h2>Five things that take the manual work out of a desk</h2>
<table><tbody>
<tr><td>RFQ intake</td><td>Inbound enquiries read, drawings sorted, scope summarised and filed to the job before anyone opens the mail</td></tr>
<tr><td>Take off and estimating</td><td>Every sheet of a bid package read, spools and components counted and weighed, priced against your own cost history</td></tr>
<tr><td>Pipeline and follow up</td><td>Every enquiry on one board, tied to its mail thread, with open offers and quiet accounts chased on schedule</td></tr>
<tr><td>Shop floor</td><td>Fit up, welding and final check recorded by piece and by weight, from the shop's own workbooks</td></tr>
<tr><td>Reporting</td><td>Pipeline, deadlines and progress in one daily brief instead of four spreadsheets</td></tr>
</tbody></table></div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="eb">In use</div><h2>Running systems, not screenshots of a demo</h2>
<p class="aip" style="max-width:720px;margin:0 0 26px">Three views from a working installation. Customer names and commercial figures are masked.</p>
<div class="shots">
<figure class="wide"><img src="img-sys-takeoff.jpg" alt="Bid package take off: spools counted, weighed and typed against the piping class" loading="lazy">
<figcaption><b>Take off from a bid package</b>A 69 page drawing set read sheet by sheet. Every spool typed, counted and weighed against the piping class, with the conflicts raised before pricing.</figcaption></figure>
<figure><img src="img-sys-pipeline.jpg" alt="Sales pipeline board with every enquiry tied to its mail thread" loading="lazy">
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
<div><b>01 · Trial</b><p>Send one bid package. We return the take off and the clarification list, so you can judge the work before you commit to anything.</p></div>
<div><b>02 · Your data</b><p>Past quotes, cost history and the mailbox connected, read only, on your own server.</p></div>
<div><b>03 · One desk first</b><p>Estimating or sales, whichever is costing you most. Running in weeks, not a programme.</p></div>
<div><b>04 · Then the rest</b><p>Shop floor, reporting and the agent added once the first desk is relied on.</p></div>
</div></div></section>

{end_band("Send us one bid package", "We return the take off and a clarification list, so you can judge the work. No system access needed to start.", ("Send a package", "contact.html"), ("Ask about a setup", f"mailto:{EMAIL}?subject=Industrial%20AI%20setup"))}"""
    return page("digital.html", "Industrial AI | Hylex Energy Consulting",
                "Bid package take off, estimating from your own cost history, sales pipeline, shop floor progress and a private AI agent on your own server. Built and run in a working fabrication business.",
                body, "digital.html")


def about():
    body = f"""{banner(['<a href="index.html">Home</a>', 'About'], "A small team with a long record in fabrication and supply",
        "Hylex works with EPC contractors, equipment OEMs and operators on fabrication and supply for energy, mining and process projects, and builds the systems those desks run on.", "About")}

<section class="s"><div class="wrap"><div class="aig">
<div><p class="aip" style="margin:0 0 14px">Two lines of work. We represent manufacturers into accounts we already handle, and we build the sales and operations systems industrial companies run on. The second came out of the first: the tools were built for a working fabrication desk before they were offered to anyone else.</p>
<p class="aip" style="margin:0 0 14px">Hylex exists to solve the scope that does not fit one shop. We qualify the shop that can build it, agree the specification, and carry the order through inspection and documentation to delivery.</p>
<p class="aip" style="margin:0">Every enquiry is handled by a principal, from first drawing to delivery.</p></div>
<ul class="cv"><li>Representation for fabrication and equipment manufacturers</li><li>AI systems for industrial sales and operations</li><li>Mining, LNG, power, chemical and process projects</li><li>Asia, Australia, the Americas and Europe</li><li>Houston, Texas</li></ul></div></div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="eb">How we work</div><h2>What you can hold us to</h2>
<div class="who"><div><b>One contact</b><p>A principal reads your enquiry and answers it. Nothing is handed to a desk that has not seen the drawings.</p></div>
<div><b>Straight answers</b><p>If a shop cannot build it well, we say so rather than pass the enquiry on.</p></div>
<div><b>One working day</b><p>Every enquiry gets a reply inside one working day, even when the answer is that we need longer.</p></div></div>
{CODES}</div></section>

{end_band("Start with a scope or a product line", "Buyers send the drawings. Manufacturers send the datasheets. Either way we reply within one working day.")}"""
    return page("about.html", "About | Hylex Energy Consulting",
                "Hylex Energy Consulting, Houston, Texas. Representation for fabrication and equipment manufacturers, and AI systems for industrial sales and operations.",
                body, "about.html")


def contact():
    body = f"""{banner(['<a href="index.html">Home</a>', 'Contact'], "Send us the scope",
        "Drawings, datasheets and specification, as you would to any bidder. Manufacturers looking for representation can send a product line instead. We reply within one working day.", "Contact")}

<section class="s"><div class="wrap">{FORM}</div></section>

<section class="s" style="background:var(--soft)"><div class="wrap"><div class="eb">Direct</div><h2>Other ways to reach us</h2>
<div class="who"><div><b>Email</b><p><a href="mailto:{EMAIL}" style="color:var(--green-d);font-weight:600">{EMAIL}</a></p></div>
<div><b>Call</b><p><a href="mailto:{EMAIL}?subject=Call%20request" style="color:var(--green-d);font-weight:600">Request a call</a> and we will send times.</p></div>
<div><b>Office</b><p>Houston, Texas.</p></div></div></div></section>"""
    return page("contact.html", "Contact | Hylex Energy Consulting",
                "Send drawings, specifications or a product line to Hylex Energy Consulting, Houston, Texas. We reply within one working day.",
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
                   "Sourcing fabricated equipment from Asia, landed price, reading a bid package, and what AI actually does for an industrial sales desk.", "Insights")
            + css + f'<section class="s"><div class="wrap"><div class="ig">{cards}</div></div></section>'
            + end_band("Have a scope that does not fit?", "Send the drawings and specification. We reply within one working day."))
    urls = [page("insights.html", "Insights | Hylex Energy Consulting",
                 "Notes on sourcing fabricated equipment from Asia, landed pricing, bid packages and AI for industrial sales desks.",
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
            + f"""<section class="s"><div class="wrap"><div class="doors">
<div class="door"><div class="eb">Representation</div><h3>Scope one shop does not cover</h3><p>What we supply, how an order runs, and how it is inspected and documented.</p><div class="lk"><a href="representation.html">For buyers ›</a><a href="principals.html">For manufacturers ›</a></div></div>
<div class="door"><div class="eb">Industrial AI</div><h3>Systems for a sales desk and a shop floor</h3><p>Take off, estimating, pipeline, shop floor and a private agent on your own server.</p><div class="lk"><a href="digital.html">What we build ›</a></div></div>
</div></div></section>""")
    return page("404.html", "Page not found | Hylex Energy Consulting",
                "That page is not on this site. Representation and industrial AI from Hylex Energy Consulting.", body, "")


# ---------------------------------------------------------------- run
def main():
    urls = [home(), representation(), principals(), digital(), about(), contact()]
    urls += insights()
    notfound()

    open("sitemap.xml", "w").write(
        '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls) + "</urlset>\n")
    open("sitemap.txt", "w").write("\n".join(urls) + "\n")

    # vercel: keep the catch all redirect for dead old urls, but let every real page through
    names = sorted({u.rsplit("/", 1)[-1] for u in urls if u.rsplit("/", 1)[-1]})
    keep = names + ["index", "404", "hylex-logo", "favicon", "img-icon", "img-sys", "og-card", "robots", "sitemap",
                    "api/", r"[0-9a-f]{32}\.txt"]
    cfg = {
        "cleanUrls": True,
        "redirects": [{"source": "/((?!" + "|".join(keep) + ").+)", "destination": "/", "permanent": False}],
    }
    open("vercel.json", "w").write(json.dumps(cfg, indent=2) + "\n")
    print("pages", len(urls) + 1)
    for u in urls:
        print("  ", u)


if __name__ == "__main__":
    main()
