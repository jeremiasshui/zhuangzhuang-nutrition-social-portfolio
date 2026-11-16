# Source Registry

> 本表把附件 v1 的來源整理成「可追蹤來源」，不代表 2026-09-18 之後永久有效。使用前依 claim 類型判斷是否需要重新確認。

| ID | 類型 | 來源 | 用途 | 時效 | 狀態 |
|---|---|---|---|---|---|
| BGG-OFFICIAL | 品牌一手 | https://dietitianbgg.com | 品牌、產品、FAQ、文章、案例 | 中 | VERIFIED（2026-09-18 抓取，`references/v1-seed/research.md`） |
| BGG-THREADS | 品牌一手社群 | Threads @dietitian_bgg | 語氣、近期內容、社群案例 | 高 | VERIFIED（2026-09-18 抓取）；互動數字每次使用前刷新 |
| BGG-IG | 品牌一手社群（使用者提供截圖） | `references/ig-screenshots/bgg-ig-story-01.jpg`～`-04.jpg`（限時動態；截圖日期未知，對話與前後照日期 11–4 月） | 學員語言、品牌語氣、限動格式 | 高 | VERIFIED（截圖內容）；學員數字與照片屬 CASE-001，不可轉用 |
| COMPETITORS-2026-09 | 同業一手頁面 | `references/v1-seed/competitors.md`（8 家，2026-09-18 抓取） | 參考案例、差異化 | 高 | VERIFIED（抓取當日）；IG／TikTok 未取得 |
| LEGAL-SOURCES-2026-09 | 政府法規原文 | `references/v1-seed/ad-regulations-sources.md`（v1 逐字抄錄） | 廣告／薦證／營養師法 | 高 | 抄錄於 2026-09-18；高風險內容仍重查現行條文 |
| HPA | 政府 | 國民健康署官方資料 | DRIs、健康教育 | 中 | 需逐 claim 驗證 |
| TFDA | 政府 | 食藥署官方資料 | 食品營養成分、廣告規範 | 中 | 需逐 claim 驗證 |
| LAW | 政府 | 全國法規資料庫 | 法規條文 | 高 | 每次高風險內容重查 |
| FTC | 政府 | 公平交易委員會 | 薦證、廣告 | 高 | 每次高風險內容重查 |
| TANG | 一手／課程 | `references/tang-copy-method.md` | 文案技巧 | 低 | IMPORTED / 方法參考 |
| JD-2026-09 | 使用者提供 | `references/jd-2026-09-18.md`（職缺原文逐字） | 職務範圍、JD mapping | 低 | USER_CONFIRMED（職缺內容） |
| METHOD-DEMAND-PATH | 使用者提供 | `references/demand-path-method.md` | 人×場景×問題選題法 | 低 | 方法參考 |
| METHOD-AISEO-LANDING | 使用者提供 | `references/landing-page-aiseo-method.md` | 內容審查標準：SPIN／FABE／GAVE／品牌落款／語意結構 | 中 | 審查標準（使用者指定） |
| HPA-DRIS-8 | 政府（本機副本） | 見 `references/local-sources.md` | 國人膳食營養素參考攝取量第八版 | 中 | 需逐 claim 驗證 |
| HPA-DRIS-9-NOTES | 政府（本機副本） | 見 `references/local-sources.md` | 第九版增修訂說明 | 中 | 需逐 claim 驗證 |
| TFDA-FOOD-DB | 政府（本機副本） | 見 `references/local-sources.md` | 食品營養成分，每 100 g | 中 | 需逐 claim 驗證；熱量不進公開文案 |
| USDA-FDC | 外國政府（本機副本） | 見 `references/local-sources.md` | 台灣資料缺漏時參考 | 中 | 背景 |
| PUBMED-2026-09-17 | 研究摘要（本機副本） | 見 `references/local-sources.md` | 背景知識 | 高 | 背景，不當文案依據 |

## Source priority

品牌當前內部文件／使用者提供 > 官方一手來源 > 品牌官網 > 原始研究／論文 > 專業二手來源 > 媒體 > 社群評論。

## Research write-back

researcher 查完一個 claim 後，新增或更新 `claim-ledger.md`：claim、來源、日期、適用範圍、狀態、expiry。不要只把 URL 丟在 `research-notes.md`。
