#!/usr/bin/env python3
"""Generate insights.html + insight-<slug>.html from posts.json using index.html's head, header and footer. Run before each deploy."""
import json, html, re, datetime
idx = open('index.html').read()
head = idx[:idx.index('<body>')]
header = idx[idx.index('<header>'):idx.index('</header>') + 9].replace('href="#', 'href="index.html#')
footer = idx[idx.index('<footer>'):idx.index('</footer>') + 9]
tail = idx[idx.index('<button type="button" class="chatb"'):idx.index('</body>')]
posts = sorted(json.load(open('posts.json')), key=lambda p: p['date'], reverse=True)
e = html.escape
def page(fn, title, desc, body):
    h = re.sub(r'<title>.*?</title>', f'<title>{e(title)}</title>', head, 1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc)}">', h, 1)
    h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="https://www.hylexenergy.com/{fn.replace(".html", "")}">', h, 1)
    open(fn, 'w').write(h + '<body>\n' + header + body + footer + tail + '</body></html>')
cards = ''.join(f'<a class="ic" href="insight-{p["slug"]}.html"><div class="eb">{p["date"]}</div><h3>{e(p["title"])}</h3><p>{e(p["summary"])}</p><span>Read ›</span></a>' for p in posts)
css = '<style>.ig{display:grid;gap:18px}@media(min-width:800px){.ig{grid-template-columns:1fr 1fr}}.ic{display:block;border:1px solid var(--line);border-top:3px solid var(--green);background:var(--soft);padding:24px}.ic h3{font-size:22px;margin:8px 0 10px}.ic p{color:var(--mute);margin:0 0 12px}.ic span{font-weight:600;color:var(--green-d)}.art p{font-size:18px;line-height:1.75;color:#2a3135;max-width:760px}</style>'
page('insights.html', 'Insights | Hylex Energy Consulting', 'Notes on sourcing fabricated equipment from Asia, landed pricing, bid packages and AI for industrial sales desks.',
     css + f'<section class="s"><div class="wrap"><div class="eb">Insights</div><h2>Notes from the procurement desk</h2><div class="ig">{cards}</div></div></section>')
for p in posts:
    body = ''.join(f'<p>{e(x)}</p>' for x in p['body'])
    page(f'insight-{p["slug"]}.html', f'{p["title"]} | Hylex Energy Consulting', p['summary'],
         css + f'<section class="s"><div class="wrap art"><div class="eb">Insights · {p["date"]}</div><h2>{e(p["title"])}</h2><p style="color:var(--mute)">{e(p["summary"])}</p>{body}<p><a class="btn p" href="index.html#enquiry">Send us your scope</a> <a class="btn" href="insights.html">All insights</a></p></div></section>')
urls = ['', 'insights'] + [f'insight-{p["slug"]}' for p in posts]
today = datetime.date.today().isoformat()
open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>https://www.hylexenergy.com/{u}</loc><lastmod>{today}</lastmod></url>' for u in urls) + '</urlset>\n')
open('sitemap.txt', 'w').write('\n'.join(f'https://www.hylexenergy.com/{u}' for u in urls) + '\n')
print('pages', len(urls))
