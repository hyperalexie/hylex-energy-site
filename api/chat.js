// Live website chat relayed through a dedicated Telegram bot (ChenUSPWebChat_bot).
// POST: visitor message -> Telegram to Alex, tagged #<session>. GET: Alex's swipe-replies for a session after message id `after`.
// No database: pending replies are read from Telegram getUpdates; updates older than 30 min are confirmed away.
import { put } from "@vercel/blob";
const API = (m) => `https://api.telegram.org/bot${process.env.WEBCHAT_TOKEN}/${m}`;
const ADMIN = () => String(process.env.ADMIN_CHAT);
const json = (status, body) => new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });
const esc = (s) => String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c]);
const validSession = (s) => /^[a-z0-9]{6,12}$/.test(s || "");

export async function POST(request) {
  let b;
  try { b = await request.json(); } catch { return json(400, { ok: false }); }
  const s = String(b.s || ""), text = String(b.text || "").trim().slice(0, 1500);
  if (!validSession(s) || !text || b.website) return json(400, { ok: false });
  const who = [b.name, b.email].filter(Boolean).map((x) => esc(String(x).slice(0, 120))).join(" · ");
  const page = esc(String(b.page || "").slice(0, 120));
  const head = `💬 <b>[HYLEX] Website chat</b> #${s}${b.lang === "zh" ? " (中文站)" : ""}${who ? "\n" + who : ""}${page ? "\n<i>" + page + "</i>" : ""}`;
  try {
    await put(`hylex-leads/${Date.now()}.json`, JSON.stringify({ kind: "chat", site: "hylex", t: new Date().toISOString(), s, text, email: String(b.email || "").slice(0, 120), name: String(b.name || "").slice(0, 120),
      page: String(b.page || "").slice(0, 120), lang: b.lang === "zh" ? "zh" : "en", ip: (request.headers.get("x-forwarded-for") || "").split(",")[0].trim(),
      cc: request.headers.get("x-vercel-ip-country") || "", city: decodeURIComponent(request.headers.get("x-vercel-ip-city") || "") }), { access: "private", addRandomSuffix: true, contentType: "application/json" });
  } catch {}
  const r = await fetch(API("sendMessage"), {
    method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ chat_id: ADMIN(), text: `${head}\n\n${esc(text)}\n\n↩️ Swipe-reply to answer`, parse_mode: "HTML" }),
  });
  return json(r.ok ? 200 : 502, { ok: r.ok });
}

export async function GET(request) {
  const u = new URL(request.url);
  const s = u.searchParams.get("s"), after = Number(u.searchParams.get("after") || 0), since = Number(u.searchParams.get("since") || 0);
  if (!validSession(s)) return json(400, { ok: false });
  const r = await fetch(API("getUpdates") + "?allowed_updates=%5B%22message%22%5D&limit=100");
  const d = await r.json().catch(() => ({ result: [] }));
  const now = Math.floor(Date.now() / 1000);
  const ups = d.result || [];
  const old = ups.filter((x) => (x.message?.date || 0) < now - 1800).map((x) => x.update_id);
  if (old.length) fetch(API("getUpdates") + `?offset=${Math.max(...old) + 1}&limit=1`).catch(() => {});
  const replies = ups.map((x) => x.message).filter((m) => m && String(m.chat?.id) === ADMIN() && m.text && m.message_id > after && m.date > since &&
    m.reply_to_message?.text?.includes(`#${s}`)).sort((a, b) => a.message_id - b.message_id).map((m) => ({ id: m.message_id, t: m.text, d: m.date }));
  return json(200, { ok: true, replies, now });
}
