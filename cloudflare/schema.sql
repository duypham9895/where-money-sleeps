-- Cloudflare D1 Schema cho Where Money Sleeps (TRACKING-PLAN.md §4 & §2.4, QĐ 31, QĐ 32, AC-80)
-- Không lưu IP, User-Agent, cookie, hay định danh người dùng; chỉ cộng gộp theo ngày (UTC YYYY-MM-DD).

CREATE TABLE IF NOT EXISTS counts (
  day TEXT NOT NULL,
  event TEXT NOT NULL,
  d1 TEXT NOT NULL,
  d2 TEXT NOT NULL,
  n INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (day, event, d1, d2)
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS quarantined_days (
  day TEXT NOT NULL PRIMARY KEY,
  reason TEXT NOT NULL,
  added_at TEXT NOT NULL
) WITHOUT ROWID;
