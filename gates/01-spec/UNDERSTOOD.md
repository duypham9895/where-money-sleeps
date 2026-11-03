---
status: fail
stage: 01-spec
date: 2026-10-24
owner: pm
blocked_on:
  - "Duy đo iPhone + Android thật (~30 phút): Zalo giữ #sync không · mở WebView hay trình duyệt · input type=file chạy không · localStorage sống trong WebView không"
  - "Duy đọc hợp đồng lao động Ringkas (điều khoản IP + không cạnh tranh)"
  - "Agent ke-toan-reviewer chạy thử 1 bài mẫu + card; đo thời gian Duy đọc báo cáo và ký (QĐ 36)"
---

# UNDERSTOOD — S1 Spec

**Phòng sở hữu stage: PM** (cùng Data · Legal · Writer, chạy song song). Quy tắc 11.

## Trích NGUYÊN VĂN từ ONE-PAGER

<grounding>
"Không đăng thứ chưa ai duyệt."
"Ra mắt khi lối vào đã duyệt xong; GĐ01/02/05 lên dần."
"S1 phải định nghĩa cách chống trùng."
</grounding>

## Kể lại bằng chữ của tôi

S0 đã quyết sản phẩm là gì. S1 phải biến mười lăm quyết định đó thành những câu có thể kiểm:
một người lạ cầm PRD này có xây đúng thứ Duy muốn mà không phải hỏi lại ai không.

Chỗ khó của S1 không nằm ở việc viết thêm, mà ở việc viết đúng ranh giới. Đây là một site dạy
tiền cho người chưa từng học tiền, nên mỗi câu trong spec về con số, về thuật ngữ, về thứ được
phép đăng đều là một lời hứa với người đọc rằng điều họ sắp tin là đúng. Spec mơ hồ ở đây không
làm ra một tính năng xấu; nó làm ra một bài học sai mà người học không có cách nào tự phát hiện.

## Stage của tôi phục vụ điều đó thế nào

1. **PRD** nói *cái gì* và *vì sao*, dừng trước *làm thế nào* — khuôn của `/ecc:plan-prd`.
2. **ACCEPTANCE** biến từng lời hứa thành phép kiểm PASS/FAIL, ghi rõ phép nào máy kiểm được và
   phép nào chỉ người kiểm được.
3. **Data** định nghĩa thước đo proxy và cách chống trùng — điều ONE-PAGER giao thẳng cho S1.
4. **Legal** chốt những gì S0 để mở: bộ đếm, trích văn bản luật, redact Hermanson, câu AI.
5. **Không giả vờ chốt** khi ba điều kiện của Duy (iPhone/Android · hợp đồng Ringkas · kế toán)
   chưa xong: viết nháp được, duyệt thì chưa.

## Chưa xác minh được

- Câu "S1 phải biến mười lăm quyết định đó thành những câu có thể kiểm" viết khi gói S0 được coi là 15 quyết định; Brief nay có **16** (QĐ 16 thêm sau APPROVE S0), và QĐ 16 có thuộc gói S0 đã duyệt không là câu chưa giải (PRD T3 Δ21).
- ONE-PAGER (`gates/ONE-PAGER.md`) vẫn `draft` và cũ hơn `PRD.md` (vibe-check [2]): ba câu trích ở trên khớp bản ONE-PAGER hiện tại, nhưng bản đó chưa được Duy duyệt lại sau QĐ 15, 16.
- Mục 5 "không giả vờ chốt": ba điều kiện (đo iPhone/Android · hợp đồng Ringkas · kế toán) chưa điều kiện nào xong ở ngày viết.
- Bản này là của một phiên Claude. Same vendor, same priors — no external verifier ran.

## Đổi ở vòng sửa 2026-10-24

- Thêm frontmatter (`status: fail`, `blocked_on` giống PRD/ACCEPTANCE) và mục "Chưa xác minh được". Không đổi chữ nào khác. Lý do: review S1 (consistency N11).
