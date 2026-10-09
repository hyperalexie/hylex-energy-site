// Visit logger for the internal visitor report. Each page view becomes one private blob that the
// ops box collects every 10 minutes and deletes. Nothing is shown to the visitor.
import { put } from "@vercel/blob";

const EVENTS = new Set(["email", "whatsapp", "phone", "wechat", "quote_cta", "form_start", "form_sent", "chat_open"]);
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
    site: "hylex", ref: clip(b.ref, 80), lang: b.lang === "zh" ? "zh" : "en", ua: clip(ua, 200),
  };
  // Interest events (tapped email, started the inquiry form, opened chat...) ride the same queue.
  if (EVENTS.has(b.e)) hit.e = b.e;
  if (!hit.ip || !hit.p) return ok();
  try {
    await put(`hylex-hits/${Date.now()}.json`, JSON.stringify(hit), { access: "private", addRandomSuffix: true, contentType: "application/json" });
  } catch {}
  return ok();
}
