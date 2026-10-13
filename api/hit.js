// Visit logger for the internal visitor report. Each page view becomes one private blob that the
// ops box collects every hour and deletes. Nothing is shown to the visitor.
// Interest events (tapped email, opened chat...) also ping Alex straight from here, because the
// collector now runs hourly: Vercel Blob gives Hobby 2,000 "advanced operations" a month and a
// 10 minute poll spends 4,320 of them on list() alone, which suspended the store on 2026-10-10.
import { put } from "@vercel/blob";

const EVENTS = new Set(["email", "whatsapp", "phone", "wechat", "quote_cta", "form_start", "form_sent", "chat_open"]);
const SAID = { email: "tapped our email", whatsapp: "tapped WhatsApp", phone: "tapped a phone number", wechat: "tapped WeChat",
  quote_cta: "clicked Request a quotation", form_start: "started the inquiry form", form_sent: "sent the inquiry form", chat_open: "opened the chat" };
const ok = () => new Response(null, { status: 204, headers: { "cache-control": "no-store" } });
const BOT = /bot|crawl|spider|slurp|headless|lighthouse|preview|facebookexternalhit|embedly|python|curl|wget/i;

export async function POST(request) {
  let b;
  try { b = JSON.parse(await request.text()); } catch { return ok(); }
  const ua = request.headers.get("user-agent") || "";
  if (BOT.test(ua)) return ok();
  const clip = (v, n) => String(v || "").slice(0, n);
  const hit = {
    t: new Date().toISOString(),
    ip: (request.headers.get("x-forwarded-for") || "").split(",")[0].trim(),
    cc: request.headers.get("x-vercel-ip-country") || "",
    city: decodeURIComponent(request.headers.get("x-vercel-ip-city") || ""),
    p: clip(b.p, 120), s: /^[a-z0-9]{6,16}$/.test(b.s || "") ? b.s : "",
    r: /^[a-z0-9]{4,16}$/.test(b.r || "") ? b.r : "",
    ref: clip(b.ref, 80), lang: b.lang === "zh" ? "zh" : "en", ua: clip(ua, 200),
  };
  // Interest events (tapped email, started the inquiry form, opened chat...) ride the same queue.
  if (EVENTS.has(b.e)) hit.e = b.e;
  if (!hit.ip || !hit.p) return ok();
  try {
    await put(`hylex-hits/${Date.now()}.json`, JSON.stringify(hit), { access: "private", addRandomSuffix: true, contentType: "application/json" });
  } catch (e) {
    // Never let the visitor see it, but never lose it in silence either: this shows in the function log.
    console.error("hit blob write failed:", e && e.message);
  }
  // Someone acting on the site is worth knowing now, not at the top of the hour. The hourly
  // collector still sends the full session afterwards (pages read, network, referrer).
  if (hit.e && process.env.TG_TOKEN && process.env.TG_CHAT) {
    const where = [hit.city, hit.cc].filter(Boolean).join(", ");
    const text = `🔥 [HYLEX SITE] Visitor ${SAID[hit.e]}\n${where ? where + " · " : ""}on ${hit.p}${hit.r ? "\nTagged link: " + hit.r : ""}`;
    try {
      await fetch(`https://api.telegram.org/bot${process.env.TG_TOKEN}/sendMessage`, {
        method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({ chat_id: process.env.TG_CHAT, text, disable_web_page_preview: true }),
      });
    } catch (e) { console.error("hit ping failed:", e && e.message); }
  }
  return ok();
}
