// Website inquiry form -> Telegram (Alex), plus a copy in the private lead log (blob leads/, drained by the ops box).
import { put } from "@vercel/blob";
const MAX_FILE = 4 * 1024 * 1024;
const FIELDS = [
  ["type", "Type"], ["call_date", "Call date"], ["call_time", "Call time"], ["tz", "Time zone"], ["platform", "Platform"],
  ["name", "Name"], ["company", "Company"], ["email", "Email"], ["phone", "Phone"], ["country", "Country"],
  ["scope", "Scope"], ["code", "Code / material"], ["quantity", "Quantity"], ["deadline", "Offer needed by"], ["delivery", "Delivery required by"], ["link", "Files link"], ["message", "Message"],
];
const esc = (s) => String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c]);
const json = (status, body) => new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json" } });

async function tg(method, body) {
  const r = await fetch(`https://api.telegram.org/bot${process.env.TG_TOKEN}/${method}`, { method: "POST", body });
  if (!r.ok) throw new Error(`telegram ${method} ${r.status} ${await r.text()}`);
}

const ZH = {
  "Could not read the form.": "无法读取表单。",
  "Please give your name, a valid email and a short description.": "请填写姓名、有效邮箱和简要需求描述。",
  "Attachment is over 4 MB. Your message was received; please email the drawings.": "附件超过4 MB。您的询价已收到，请通过邮件发送图纸。",
  "We could not send your inquiry. Please email amac@hylexenergy.com.": "询价发送失败，请发邮件至 amac@hylexenergy.com。",
  "Your message was received, but the attachment did not go through. Please email it to amac@hylexenergy.com.": "您的询价已收到，但附件未能上传，请发邮件至 amac@hylexenergy.com。",
};

export async function POST(request) {
  let form;
  try { form = await request.formData(); } catch { return json(400, { ok: false, error: "Could not read the form." }); }
  const zh = form.get("lang") === "zh";
  const fail = (status, msg) => json(status, { ok: false, error: zh ? ZH[msg] || msg : msg });
  if (form.get("website")) return json(200, { ok: true }); // honeypot: bots fill hidden fields
  const v = (k) => String(form.get(k) || "").trim().slice(0, 2000);
  const call = v("type") === "Call";
  if (!v("name") || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v("email")) || (!call && !v("message")) || (call && (!v("call_date") || !v("call_time"))))
    return fail(400, "Please give your name, a valid email and a short description.");

  const lines = FIELDS.filter(([k]) => v(k)).map(([k, label]) => `<b>${label}:</b> ${esc(v(k))}`);
  const text = `${call ? "📞 <b>[HYLEX] hylexenergy.com call request" : v("type") === "Chat" ? "💬 <b>[HYLEX] hylexenergy.com chat question" : "🌐 <b>[HYLEX] hylexenergy.com inquiry"}${zh ? " (中文站)" : ""}</b>\n\n${lines.join("\n")}`.slice(0, 4000);
  const rec = { kind: "inquiry", site: "hylex", t: new Date().toISOString(), lang: zh ? "zh" : "en", ip: (request.headers.get("x-forwarded-for") || "").split(",")[0].trim(),
    cc: request.headers.get("x-vercel-ip-country") || "", city: decodeURIComponent(request.headers.get("x-vercel-ip-city") || ""), s: v("s").slice(0, 16), r: v("r").slice(0, 16),
    file: (form.get("file") && form.get("file").name) || "" };
  for (const [k] of FIELDS) if (v(k)) rec[k] = v(k);
  let saved = false;
  try { await put(`hylex-leads/${Date.now()}.json`, JSON.stringify(rec), { access: "private", addRandomSuffix: true, contentType: "application/json" }); saved = true; } catch (e) { console.error(e); }
  // The message and the attachment are sent separately; a failed attachment must not report the message as lost.
  try {
    const m = new FormData();
    m.set("chat_id", process.env.TG_CHAT); m.set("text", text); m.set("parse_mode", "HTML");
    await tg("sendMessage", m);
  } catch (e) {
    console.error(e);
    if (saved) { // kept in the lead log; flag it so the ops box pings Alex from there
      try { await put(`hylex-leads/${Date.now()}.json`, JSON.stringify({ ...rec, kind: "inquiry_unsent" }), { access: "private", addRandomSuffix: true, contentType: "application/json" }); } catch {}
      return json(200, { ok: true });
    }
    return fail(502, "We could not send your inquiry. Please email amac@hylexenergy.com.");
  }
  const partial = (msg) => json(200, { ok: true, partial: true, error: zh ? ZH[msg] || msg : msg });
  const file = form.get("file");
  if (file && typeof file === "object" && file.size > 0) {
    if (file.size > MAX_FILE) return partial("Attachment is over 4 MB. Your message was received; please email the drawings.");
    try {
      const d = new FormData();
      d.set("chat_id", process.env.TG_CHAT);
      d.set("caption", `Attachment from ${v("name")} (${v("company") || v("email")})`.slice(0, 1000));
      d.set("document", file, file.name || "attachment");
      await tg("sendDocument", d);
    } catch (e) {
      console.error(e);
      return partial("Your message was received, but the attachment did not go through. Please email it to amac@hylexenergy.com.");
    }
  }
  return json(200, { ok: true });
}
