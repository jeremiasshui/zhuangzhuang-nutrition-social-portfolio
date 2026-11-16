# Claim Ledger

這是成品能不能使用具體事實的唯一索引。品牌資料來自 2026-09-18 對官網與 Threads 的調查（references/v1-seed/research.md），標 VERIFIED 並註明範圍；「官網自述」不等於第三方驗證或品牌內部確認。

| Claim ID | Claim | Status | Source | Checked | Expiry / Recheck rule |
|---|---|---|---|---|---|
| BRAND-001 | 品牌核心主張：把減重放回日常、外食與聚餐可被納入計畫 | VERIFIED | BGG-OFFICIAL／BGG-THREADS 抓取 2026-09-18（references/v1-seed/research.md）；範圍＝官網公開主張，非品牌內部確認 | 2026-09-18 | 對外使用前或 30 天後重查 |
| BRAND-002 | 「放縱是計畫的一部分，不是失敗」可作為底層訊息 | VERIFIED | BGG-OFFICIAL／BGG-THREADS 抓取 2026-09-18（references/v1-seed/research.md）；範圍＝官網公開主張，非品牌內部確認 | 2026-09-18 | 對外使用前或 30 天後重查 |
| BRAND-003 | 品牌主張不教學員秤食物（營養師原話：「我真的沒在教大家秤食物，減肥要融入生活才能長久」） | VERIFIED | BGG-IG story-02；範圍＝品牌公開主張 | 2026-09-18 | 對外使用前確認仍為現行說法 |
| OFFER-003 | 課程使用「344 份量」與「自檢表」等工具 | HYPOTHESIS | BGG-IG story-01 學員對話提及，定義未取得 | 2026-09-18 | 需品牌方說明 |
| FOUNDER-001 | 創辦人營養師資格／學歷／NASM 等資訊 | VERIFIED | BGG-OFFICIAL／BGG-THREADS 抓取 2026-09-18（references/v1-seed/research.md）；範圍＝官網自述 | 2026-09-18 | 對外使用前或 30 天後重查 |
| METRIC-001 | Threads 追蹤數（v1 記 54,900） | VERIFIED | BGG-OFFICIAL／BGG-THREADS 抓取 2026-09-18（references/v1-seed/research.md）；同日同業研究亦記 54.9K | 2026-09-18 | 每次使用前刷新 |
| METRIC-002 | 陪伴學員數（v1 記 1,000+） | VERIFIED | BGG-OFFICIAL／BGG-THREADS 抓取 2026-09-18（references/v1-seed/research.md）；範圍＝官網自述數字 | 2026-09-18 | 每次使用前刷新 |
| METRIC-003 | 報名人次（v1 記 2,500+） | VERIFIED | BGG-OFFICIAL／BGG-THREADS 抓取 2026-09-18（references/v1-seed/research.md）；範圍＝官網自述數字 | 2026-09-18 | 每次使用前刷新 |
| METRIC-004 | 滿意度（v1 記 4.9/5） | VERIFIED | BGG-OFFICIAL／BGG-THREADS 抓取 2026-09-18（references/v1-seed/research.md）；範圍＝官網自述數字 | 2026-09-18 | 每次使用前刷新 |
| CASE-001 | 任何學員公斤數、期間、職業、照片 | BLOCKED | v1 案例摘要 | 2026-09-18 | 需來源一致＋授權 |
| OFFER-001 | 課程五階段流程 | VERIFIED | BGG-OFFICIAL／BGG-THREADS 抓取 2026-09-18（references/v1-seed/research.md）（〈壯壯營養師是誰〉文章） | 2026-09-18 | 對外使用前確認流程仍一致 |
| OFFER-002 | 價格、時長、影片數、退款、諮詢次數 | BLOCKED | v1 明列缺資料 | 2026-09-18 | 需品牌方提供 |
| OFFER-004 | 品牌提供一對一免費諮詢（線上會議），會後以表單蒐集回饋（兩題 1–5 分評分＋開放題＋是否加入大師班） | VERIFIED | BGG-IG story-04；另見 research.md（Fillout 表單預約） | 2026-09-18 | 對外使用前確認仍免費 |
| OFFER-005 | 諮詢不只由創辦人執行，至少還有一位團隊營養師 | VERIFIED | BGG-IG story-04 回饋提及其他營養師姓名 | 2026-09-18 | 人數未取得 |
| NUTRITION-001 | 任何具體份量、時程、生理機制 | BLOCKED | 無單一永久來源 | — | 每個 asset 建 claim card |
| NUTRITION-002 | 臺灣「國民飲食指標」建議每日鈉攝取量限制在 2400 mg（約 6 g 食鹽）以下 | VERIFIED | HPA-DRIS-8 鈉章 p.11 | 2026-09-18 | 第九版 DRIs 發布時重查 |
| NUTRITION-003 | 冷凍小香腸每 100 g 含鈉 722 mg | VERIFIED | TFDA-FOOD-DB | 2026-09-18 | 資料庫改版時重查；僅限此樣品 |
| NUTRITION-004 | 培根每 100 g 含鈉 610 mg | VERIFIED | TFDA-FOOD-DB | 2026-09-18 | 資料庫改版時重查；僅限此樣品 |
| NUTRITION-005 | 冷凍貢丸每 100 g 含鈉 580 mg | VERIFIED | TFDA-FOOD-DB | 2026-09-18 | 資料庫改版時重查；僅限此樣品 |
| LEGAL-001 | 廣告／薦證／營養師執業法規解釋 | BLOCKED | 需查現行法規 | — | 每個高風險 asset 重查 |

## 新增格式

`CLAIM-ID | 一句可被驗證的 claim | VERIFIED/USER_CONFIRMED/IMPORTED/HYPOTHESIS/BLOCKED | source | checked date | expiry/recheck`

一個 claim 只能有一個清楚主張。不要把「A、B、C 所以 D」混成同一列。
