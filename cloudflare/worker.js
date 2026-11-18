/**
 * Cloudflare Worker cho Where Money Sleeps (TRACKING-PLAN.md §3–§4, AC-34, AC-35, AC-55, AC-56, AC-68, AC-82)
 * - Cùng origin với Static Assets (dist/site).
 * - Endpoint nhận beacon: POST /api/p (tránh danh sách EasyPrivacy).
 * - Endpoint /api/feedback: trả 410 Gone rõ ràng (R23/R29 — 0 lưu PII/email trên D1).
 * - Route HTML chính (/, /index.html, /prototype.html): dùng HTMLRewriter gắn OpenGraph/Twitter động theo ?story=&lang=.
 * - Không đọc bất kỳ header định danh hay địa chỉ mạng nào; luôn trả 204 No Content ở /api/p.
 */

const SITE_ORIGIN = "https://wheremoneysleeps.duyslab.icu";

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

const HTML_SECURITY_HEADERS = {
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "X-Frame-Options": "DENY",
  "Content-Security-Policy":
    "default-src 'self'; img-src 'self' data: blob: https://i.ytimg.com; media-src 'self' blob:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; script-src 'self' 'unsafe-inline'; connect-src 'self'; frame-src https://www.youtube-nocookie.com https://www.youtube.com; object-src 'none'; base-uri 'none'"
};

const SEO_CATALOG = {
  landing: {
    vi: {
      title: "Đêm nay, tiền của bạn đang ngủ ở đâu? — Where Money Sleeps",
      desc: "Từ tin báo ghi có tới sổ sách ngân hàng: giải mã đường đi thật của dòng tiền và bút toán kép Thông tư 99/2025/TT-BTC (song ngữ VI ⇄ EN).",
      imgAlt: "Where Money Sleeps — Mặt cắt đường đi của dòng tiền và sổ kế toán"
    },
    en: {
      title: "Where Does Your Money Sleep Tonight? — Where Money Sleeps",
      desc: "From the bank alert to double-entry ledgers: trace real settlement rails and Circular 99/2025/TT-BTC bookkeeping (unofficial summary, bilingual VI ⇄ EN).",
      imgAlt: "Where Money Sleeps — Cross-section of payment settlement rails and ledgers"
    }
  },
  stories: {
    card: {
      vi: {
        title: "Đêm nay, 10 triệu bạn vừa quẹt thẻ đang ngủ ở đâu? — Where Money Sleeps",
        desc: "Một bữa liên hoan, năm bên đứng sau cú chạm thẻ, và 220.000 đồng chưa từng biến mất.",
        imgAlt: "Đêm nay, 10 triệu bạn vừa quẹt thẻ đang ngủ ở đâu?"
      },
      en: {
        title: "You just tapped 10 million at dinner. Where is that money sleeping tonight? — Where Money Sleeps",
        desc: "One group dinner, five houses on one street, and 220,000 dong that never vanished. (Unofficial summary of Circular 99/2025/TT-BTC.)",
        imgAlt: "You just tapped 10 million at dinner. Where is that money sleeping tonight?"
      }
    },
    pay: {
      vi: {
        title: "Vì sao công ty bảo bạn mở tài khoản nhận lương ở đúng một ngân hàng? — Where Money Sleeps",
        desc: "15 triệu lương vừa báo về, nhưng không đồng nào thật sự chảy vào tài khoản ngay lúc đó. Con số trên màn hình lại là món nợ ngân hàng đang nợ ngược lại bạn.",
        imgAlt: "Vì sao công ty bảo bạn mở tài khoản nhận lương ở đúng một ngân hàng?"
      },
      en: {
        title: "Why does your company tell you to open an account at one specific bank? — Where Money Sleeps",
        desc: "Payday lands without a single dong leaving the building. And your balance turns out to be a debt. (Unofficial summary of Circular 99/2025/TT-BTC.)",
        imgAlt: "Why does your company tell you to open an account at one specific bank?"
      }
    },
    install: {
      vi: {
        title: "Mua điện thoại 12 triệu trả góp 0%: ai đang trả tiền lãi? — Where Money Sleeps",
        desc: "Chiếc máy 12 triệu (ví dụ), tờ rơi ghi 0%, và 600.000 đồng cửa hàng chịu cắt lại ngay sau quầy thu ngân.",
        imgAlt: "Mua điện thoại 12 triệu trả góp 0%: ai đang trả tiền lãi?"
      },
      en: {
        title: "Buying a 12M phone on 0% installment: who actually pays the interest? — Where Money Sleeps",
        desc: "A 12,000,000 VND smartphone, a bright 0% counter flyer, and the 600,000 VND slice the shop quietly gives up behind the register. (Unofficial summary of Circular 99/2025/TT-BTC.)",
        imgAlt: "Buying a 12M phone on 0% installment: who actually pays the interest?"
      }
    },
    minpay: {
      vi: {
        title: "Sao kê 10 triệu, trả tối thiểu 5% (500.000 đồng): vì sao kỳ sau vẫn bị cộng 592.500 đồng tiền lãi? — Where Money Sleeps",
        desc: "Chạm thẻ 10 triệu đầu kỳ (ví dụ), trả đúng hạn 500.000 đồng ở Ngày 45, và đồng hồ tính lãi lặng lẽ quay ngược về Ngày 01.",
        imgAlt: "Sao kê 10 triệu, trả tối thiểu 5% (500.000 đồng): vì sao kỳ sau vẫn bị cộng 592.500 đồng tiền lãi?"
      },
      en: {
        title: "Paying the 5% minimum (500,000 VND) on a 10M card bill: why does 592,500 VND in interest land next month? — Where Money Sleeps",
        desc: "A Day 01 swipe, an on-time 500,000 VND minimum payment on Day 45, and a silent interest clock that rewinds straight back to Day 01. (Unofficial summary of Circular 99/2025/TT-BTC.)",
        imgAlt: "Paying the 5% minimum (500,000 VND) on a 10M card bill: why does 592,500 VND in interest land next month?"
      }
    },
    qr: {
      vi: {
        title: "Quét QR trả 50 nghìn: vì sao quán nhận đủ ngay, không mất 2,2% phí như quẹt thẻ? — Where Money Sleeps",
        desc: "Tấm bảng mica trên quầy gỗ, tiếng loa báo tiền sau 3 giây, và hai chiều tiền đi ngược nhau giữa quét mã (Push) với quẹt thẻ (Pull).",
        imgAlt: "Quét QR trả 50 nghìn: vì sao quán nhận đủ ngay, không mất 2,2% phí như quẹt thẻ?"
      },
      en: {
        title: "Scanning a 50K QR for coffee: why does the shop get 100% in 3 seconds, dodging 2.2% card fees? — Where Money Sleeps",
        desc: "A plastic QR square on a wooden counter, a small speaker announcing 50,000 VND in three seconds, and why pushing your own cash beats pulling from a credit line. (Unofficial summary of Circular 99/2025/TT-BTC.)",
        imgAlt: "Scanning a 50K QR for coffee: why does the shop get 100% in 3 seconds, dodging 2.2% card fees?"
      }
    },
    profitcash: {
      vi: {
        title: "Chốt sổ lãi ròng 2 tỷ nhưng TK 112 chỉ còn 50 triệu: sao công ty có lãi vẫn hết tiền trả lương? — Where Money Sleeps",
        desc: "Chiều 31 tháng 12, hai tờ giấy đặt cạnh nhau trên bàn: báo cáo ghi lãi ròng 2 tỷ đồng, sao kê ngân hàng còn đúng 50 triệu — vì 3,45 tỷ đang nằm yên trong giấy hẹn nợ (TK 131) và trên kệ kho (TK 156).",
        imgAlt: "Chốt sổ lãi ròng 2 tỷ nhưng TK 112 chỉ còn 50 triệu: sao công ty có lãi vẫn hết tiền trả lương?"
      },
      en: {
        title: "Booking 2B net profit with 50M cash left: why does a profitable firm run short of payroll cash? — Where Money Sleeps",
        desc: "At 4:00 p.m. on December 31, the closed income statement reads 2 billion VND profit while Account 112 holds just 50 million—because 3.45 billion sits inside unpaid customer invoices (Account 131) and warehouse shelves (Account 156). (Unofficial summary of Circular 99/2025/TT-BTC.)",
        imgAlt: "Booking 2B net profit with 50M cash left: why does a profitable firm run short of payroll cash?"
      }
    },
    offus: {
      vi: {
        title: "Chuyển khoản 20 triệu cùng và khác ngân hàng: cùng reo sau 3 giây, sao tiền thật đi hai đường? — Where Money Sleeps",
        desc: "Hai lệnh 20 triệu cùng báo thành công sau 3 giây. Một lệnh chỉ sửa hai dòng số dư trong cùng toà nhà; lệnh kia cần tiền cọc bảo chứng và phiên bù trừ 30 tỷ cuối ngày tại Ngân hàng Trung ương.",
        imgAlt: "Chuyển khoản 20 triệu cùng và khác ngân hàng: cùng reo sau 3 giây, sao tiền thật đi hai đường?"
      },
      en: {
        title: "20 Million to the Same Bank vs. Another Bank: Both Chime in 3 Seconds, So Why Do Reserves Go Two Ways? — Where Money Sleeps",
        desc: "Two 20-million-dong transfers chime after 3 seconds. One edits two lines in a single ledger; the other taps pledged collateral and waits for a 30-billion-dong net settlement at the central bank. (Unofficial summary of Circular 99/2025/TT-BTC.)",
        imgAlt: "20 Million to the Same Bank vs. Another Bank: Both Chime in 3 Seconds, So Why Do Reserves Go Two Ways?"
      }
    }
  }
};

let isolateDay = "";
let isolateWrites = 0;

export function resolveSeoMeta(urlInput) {
  const urlObj = urlInput instanceof URL ? urlInput : new URL(String(urlInput || SITE_ORIGIN));
  const rawLang = (urlObj.searchParams.get("lang") || "").toLowerCase();
  const lang = rawLang === "en" ? "en" : "vi";
  const rawStory = (urlObj.searchParams.get("story") || "").toLowerCase();
  const isStory = Boolean(rawStory && Object.prototype.hasOwnProperty.call(SEO_CATALOG.stories, rawStory));
  const slug = isStory ? rawStory : "landing";
  const entry = isStory ? SEO_CATALOG.stories[slug][lang] : SEO_CATALOG.landing[lang];
  const canonicalUrl = isStory
    ? `${SITE_ORIGIN}/?story=${encodeURIComponent(slug)}&lang=${lang}`
    : (lang === "en" ? `${SITE_ORIGIN}/?lang=en` : `${SITE_ORIGIN}/`);
  const imageUrl = `${SITE_ORIGIN}/public/brand/${isStory ? slug : "card"}-fig-1.jpg`;
  return {
    lang,
    isStory,
    slug,
    title: entry.title,
    desc: entry.desc,
    imageAlt: entry.imgAlt,
    canonicalUrl,
    altViUrl: isStory ? `${SITE_ORIGIN}/?story=${encodeURIComponent(slug)}&lang=vi` : `${SITE_ORIGIN}/?lang=vi`,
    altEnUrl: isStory ? `${SITE_ORIGIN}/?story=${encodeURIComponent(slug)}&lang=en` : `${SITE_ORIGIN}/?lang=en`,
    altDefaultUrl: isStory ? `${SITE_ORIGIN}/?story=${encodeURIComponent(slug)}` : `${SITE_ORIGIN}/`,
    imageUrl,
    locale: lang === "en" ? "en_US" : "vi_VN",
    altLocale: lang === "en" ? "vi_VN" : "en_US"
  };
}

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

function applyHtmlSeoRewriter(resp, urlObj) {
  const meta = resolveSeoMeta(urlObj);
  const setAttr = (attr, val) => ({
    element(el) {
      el.setAttribute(attr, val);
    }
  });
  return new HTMLRewriter()
    .on("html", setAttr("lang", meta.lang))
    .on("title", {
      element(el) {
        el.setInnerContent(meta.title);
      }
    })
    .on("#metaDesc", setAttr("content", meta.desc))
    .on("#canonicalLink", setAttr("href", meta.canonicalUrl))
    .on("#hreflangVi", setAttr("href", meta.altViUrl))
    .on("#hreflangEn", setAttr("href", meta.altEnUrl))
    .on("#hreflangDefault", setAttr("href", meta.altDefaultUrl))
    .on("#ogType", setAttr("content", meta.isStory ? "article" : "website"))
    .on("#ogLocale", setAttr("content", meta.locale))
    .on("#ogLocaleAlt", setAttr("content", meta.altLocale))
    .on("#ogTitle", setAttr("content", meta.title))
    .on("#ogDesc", setAttr("content", meta.desc))
    .on("#ogUrl", setAttr("content", meta.canonicalUrl))
    .on("#ogImage", setAttr("content", meta.imageUrl))
    .on("#ogImageAlt", setAttr("content", meta.imageAlt))
    .on("#twTitle", setAttr("content", meta.title))
    .on("#twDesc", setAttr("content", meta.desc))
    .on("#twImage", setAttr("content", meta.imageUrl))
    .transform(resp);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/feedback") {
      return new Response('{"ok":false,"reason":"mailto_only"}', {
        status: 410,
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          "Cache-Control": "no-store"
        }
      });
    }

    if (url.pathname === "/api/p") {
      if (request.method !== "POST") {
        return new Response(null, { status: 204 });
      }
      try {
        const origin = request.headers.get("Origin") || "";
        if (origin) {
          try {
            const originHost = new URL(origin).hostname;
            if (
              originHost !== "wheremoneysleeps.duyslab.icu" &&
              originHost !== "localhost" &&
              originHost !== "127.0.0.1"
            ) {
              return new Response(null, { status: 204 });
            }
          } catch {
            return new Response(null, { status: 204 });
          }
        }
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
      const assetResp = await env.ASSETS.fetch(request);
      const isMainEntry = url.pathname === "/" || url.pathname === "/index.html" || url.pathname === "/prototype.html";
      if (!isMainEntry || assetResp.status !== 200) {
        return assetResp;
      }
      const headers = new Headers(assetResp.headers);
      for (const [hk, hv] of Object.entries(HTML_SECURITY_HEADERS)) {
        headers.set(hk, hv);
      }
      const securedResp = new Response(assetResp.body, {
        status: assetResp.status,
        statusText: assetResp.statusText,
        headers
      });
      const ct = headers.get("Content-Type") || "";
      if (request.method === "GET" && typeof HTMLRewriter === "function" && ct.includes("text/html")) {
        return applyHtmlSeoRewriter(securedResp, url);
      }
      return securedResp;
    }
    return new Response("Not Found", { status: 404 });
  }
};
