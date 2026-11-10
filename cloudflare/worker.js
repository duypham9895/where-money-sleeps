/**
 * Cloudflare Worker cho Where Money Sleeps (TRACKING-PLAN.md §3–§4, AC-34, AC-35, AC-55, AC-56, AC-68, AC-82)
 * - Cùng origin với Static Assets (dist/site).
 * - Endpoint nhận beacon: POST /api/p (tránh danh sách EasyPrivacy).
 * - Không đọc bất kỳ header định danh hay địa chỉ mạng nào; luôn trả 204 No Content.
 * - Kiểm chặt tên event và giá trị thuộc tính theo danh sách cho phép sinh lúc build.
 */

const ALLOWED_LESSONS = new Set([
  "card",
  "pay",
  "install",
  "minpay",
  "qr",
  "profitcash",
  "offus"
]);

const ALLOWED_CARDS = new Set([
  "card-q1.v1",
  "card-q2.v1",
  "pay-q1.v1",
  "pay-q2.v1",
  "install-q1.v1",
  "install-q2.v1",
  "minpay-q1.v1",
  "minpay-q2.v1",
  "qr-q1.v1",
  "qr-q2.v1",
  "profitcash-q1.v1",
  "profitcash-q2.v1",
  "offus-q1.v1",
  "offus-q2.v1"
]);

const ALLOWED_METHODS = new Set(["link", "code"]);
const ALLOWED_SOURCES = new Set(["hosted", "own"]);
const DAILY_WRITE_CAP = 40000;

let isolateDay = "";
let isolateWrites = 0;

export function parseAndValidateBeacon(rawBody) {
  if (typeof rawBody !== "string" || rawBody.length === 0 || rawBody.length > 512) {
    return null;
  }
  let data;
  try {
    data = JSON.parse(rawBody);
  } catch {
    return null;
  }
  if (!data || typeof data !== "object" || Array.isArray(data)) {
    return null;
  }
  const ev = data.event;
  if (ev === "lesson_completed") {
    const lesson = String(data.lesson || "");
    const fromStart = data.from_start;
    if (!ALLOWED_LESSONS.has(lesson) || typeof fromStart !== "boolean") {
      return null;
    }
    return { event: ev, d1: lesson, d2: fromStart ? "true" : "false" };
  }
  if (ev === "card_answered") {
    const card = String(data.card || "");
    const correct = data.correct;
    if (!ALLOWED_CARDS.has(card) || typeof correct !== "boolean") {
      return null;
    }
    return { event: ev, d1: card, d2: correct ? "true" : "false" };
  }
  if (ev === "pdf_opened") {
    const source = String(data.source || "");
    if (!ALLOWED_SOURCES.has(source)) {
      return null;
    }
    return { event: ev, d1: source, d2: "" };
  }
  if (ev === "sync_created" || ev === "progress_restored") {
    const method = String(data.method || "");
    if (!ALLOWED_METHODS.has(method)) {
      return null;
    }
    return { event: ev, d1: method, d2: "" };
  }
  return null;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === "wms.duypham.me") {
      return Response.redirect(`https://money.duypham.me${url.pathname}${url.search}`, 301);
    }

    if (url.pathname === "/api/p") {
      if (request.method !== "POST") {
        return new Response(null, { status: 204 });
      }
      try {
        const raw = await request.text();
        const parsed = parseAndValidateBeacon(raw);
        if (!parsed) {
          return new Response(null, { status: 204 });
        }
        const today = new Date().toISOString().slice(0, 10);
        if (isolateDay !== today) {
          isolateDay = today;
          isolateWrites = 0;
        }
        if (isolateWrites >= DAILY_WRITE_CAP) {
          return new Response(null, { status: 204 });
        }
        isolateWrites += 1;
        if (env && env.DB && typeof env.DB.prepare === "function") {
          await env.DB.prepare(
            "INSERT INTO counts (day, event, d1, d2, n) VALUES (?1, ?2, ?3, ?4, 1) " +
            "ON CONFLICT (day, event, d1, d2) DO UPDATE SET n = n + 1 WHERE n < ?5"
          )
            .bind(today, parsed.event, parsed.d1, parsed.d2, DAILY_WRITE_CAP)
            .run();
        }
      } catch {
        // Bỏ qua lỗi ghi để luôn giữ hợp đồng trả 204
      }
      return new Response(null, { status: 204 });
    }

    if (env && env.ASSETS && typeof env.ASSETS.fetch === "function") {
      return env.ASSETS.fetch(request);
    }
    return new Response("Not Found", { status: 404 });
  }
};
