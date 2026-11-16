# Memory Audit｜2026-09-18

執行者：主對話（未派 subagent）｜依 `.claude/skills/audit-memory/SKILL.md`

## 自動檢查結果

| 檢查 | 結果 |
|---|---|
| `python3 scripts/check_memory.py` | OK |
| `python3 -m unittest discover -s tests` | 3/3 通過 |
| `check_asset.py examples/*` | good 通過；bad-guarantee、bad-double-cta 被正確擋下 |
| docs／skills 提到的檔案路徑 | 全部存在（`<task-id>` 佔位路徑除外） |

注意：以上檢查只驗證格式與關鍵字，**不驗證事實**，也抓不到「檔案沒被載入」這類設計問題。

---

## Critical（會讓系統產生錯誤結果）

### C1｜`USER_CONFIRMED` 的定義被放寬了
`BRAND-001`、`BRAND-002` 標 `USER_CONFIRMED`，來源是「使用者提供 v1 品牌文件」。但 v1 是**應徵者自己整理的公開資料**，不是品牌方提供。依 `05-claims-and-risk.md` 的定義，`USER_CONFIRMED` 應指「使用者／品牌方明確提供」的事實。
- 風險：作品集裡把「我推論的品牌主張」包裝成「品牌已確認」，面試官一問就會被問倒。
- 提議（語意變更，未自行修改）：這兩條改為 `IMPORTED`，來源寫 `BGG-OFFICIAL 公開頁面（2026-09-18 快照）`；等入職或面試時由品牌方確認後再升級。`00-brand-core.md` 開頭也應加一句「由公開資料推論，尚未經品牌方確認」。

### C2｜品牌語氣檔沒有被載入
`memory/core/01-voice.md` 不在 `CLAUDE.md` 的 `@` 載入清單裡，也不在 `00_INDEX.md` 裡。語氣規則（避免語彙、Good／Bad pattern）很可能從未進入寫稿上下文。
- 已修：`00_INDEX.md` 補上（格式修正）。
- 提議：`CLAUDE.md`「每次啟動必讀」加入 `@memory/core/01-voice.md`。（CLAUDE.md 修改會觸發資安 hook 詢問，使用者睡覺中，所以留待確認）

### C3｜v1／v2 兩套 agent 並存，路由不一致
| 流程 | 使用的 agent |
|---|---|
| v1 通用文案 `/write-copy`、`/plan-campaign` | strategist、researcher、writer、copy-editor、claims-reviewer |
| v2 短影音 `/research-radar`、`/plan-9-videos`、`/write-script`… | audience-researcher、reference-researcher、scriptwriter、platform-adapter、production-qa、performance-analyst（加上共用的 strategist、claims-reviewer、copy-editor） |

`CLAUDE.md` 只列 8 個 agent、8 個指令；`writer`、`researcher`、`/write-copy`、`/plan-campaign`、`/learn-results` 沒被列出。功能都還能用，但使用者看不出何時該用哪一套。
- 提議：`CLAUDE.md` 的 Agents 段落改成上表兩欄，並補上三個漏列的指令。**不刪任何 agent**（保留原功能）。

### C4｜與使用者全域規則 0 衝突
多個 skill 寫「派 X agent／平行派」，但使用者全域 hook 會擋下 Agent 工具，除非使用者當次同意。
- 提議：`CLAUDE.md` 加一條「本機規則：派任何 subagent 前，列出數量、用途、預估 token，等使用者同意；未同意時，由主對話讀該 agent 定義後自行扮演該角色」。這樣 skill 流程不變，只是執行者不同。

---

## Update（要更新／修正）

| # | 問題 | 處理 |
|---|---|---|
| U1 | `claim-ledger` 的 METRIC-001 一列放四個數字，違反 ledger 自訂的「一列一個主張」 | **已修**：拆成 METRIC-001～004，狀態都維持 IMPORTED（未改語意） |
| U2 | `data/performance.csv` 與 `memory/learning/performance.csv` 欄位不同（前者有 topic/format/avg_watch_pct/profile_actions；後者有 content_pillar/persona/impressions/completion_rate/clicks） | **CONFLICT**，已記在 decision-log，未擇一。建議：`data/` 當原始匯入，`memory/learning/` 當清理後的長期紀錄，並統一欄位名 |
| U3 | `docs/MEMORY-DESIGN.md` 列出不存在的 `working/active-script.md` | **已修**：改成實際存在的 `current-brief.md` |
| U4 | `00_INDEX.md` 漏列 `core/01-voice.md`、`project/00-content-strategy.md`、`project/copy-methods.md`、`working/current-brief.md`、`working/research-notes.md` | **已修** |
| U5 | 職缺原文（JD）不在專案裡；`01-role-and-success.md`、`JD-MAPPING.md` 都是轉述 | 需使用者補上 JD 原文並登記到 `source-registry` |
| U6 | 兩個 LINE 識別不一致：`brand-rules.md` 用 `lin.ee/z8FXY7v`，`research.md` 用 `@270kdgxf` | 可能是同一帳號，需查證後寫入 ledger（OFFER 或 CTA 類） |
| U7 | `sources.md` 寫死本機路徑 `/mnt/c/Users/User/Desktop/...`；`check_memory.py` 只掃 `memory/`，所以沒抓到 | v1 快照不改；新增 source-registry 的「LOCAL-NUTRITION-DATA」登記時只寫邏輯名稱 |
| U8 | `ad-regulations.md` 指向 `docs/research/ad-regulations-sources.md`，`personas.md` 指向 `docs/research/competitors.md`、ADR-0005，這些 v1 檔案都沒帶進 v2 | 法規條文需在 LEGAL claim 真正使用前重查 |
| U9 | `MANIFEST.md` 寫 109 個檔案，把 `.pytest_cache`、`__pycache__` 也算進去 | 低優先，下次產生 manifest 時排除 |

## Archive（保留但不當現況）

- `references/v1-seed/weekly-social-plan.md`：中秋週企劃是**歷史範例**，其中 S4（烘焙師 94.1→79kg）屬 CASE-001 BLOCKED；S3「代謝下降、掉髮」、S5「荷爾蒙影響脂肪代謝」、S6「八成是水、三天」都是未查證的營養機制／時程（NUTRITION-001 BLOCKED）。
- `references/v1-seed/brand-rules.md`：「每句接【待營養師確認】」與 v2 writer 規則（公開正文不放內部標籤）衝突，**以 v2 為準**（較新、有測試覆蓋）。
- `references/v1-seed/platform-formats.md`：字數規格可參考，但 v2 `core/04-platforms.md` 優先。

## Keep（狀態良好）

- 四層 memory 架構與升級規則（MEMORY-DESIGN）
- claim 狀態五分類、Copy safety hierarchy
- `check_asset.py` 與三個黃金範例
- `tang-copy-method.md`：每條都有一手來源網址，未取得者明列，可直接當方法參考
- 空白的 working／learning／ledger 表格：正確，代表還沒開始第一週

---

## 資訊分類（使用者要求的四類）

### 1. 已確認品牌事實
**嚴格來說：目前沒有任何一條是品牌方確認過的。** 最接近的是「官網公開寫出的主張」，可以用「官網寫道…」的句型引用，但狀態應為 IMPORTED：
- 品牌名「壯壯營養師」、公司壯潤有限公司、官網 dietitianbgg.com
- 產品線三項：放縱減肥大師班、放縱減肥導師聯盟、一對一諮詢
- 方法主張：不精算熱量、不要求餐餐原型、外食澱粉吃飽、不吃產品不吃藥
- 官網聲明不保證每月減幾公斤

### 2. 需要重新研究的動態資訊（使用前必刷新）
- Threads 追蹤數（v1 記 54,900）
- 陪伴學員 1,000+、報名 2,500+、8 週週期、滿意度 4.9/5
- Threads 高互動貼文數字（「碳水吃太少怎麼睡都不飽」18.7K 讚／5K 分享）
- 課程五階段流程是否仍一致
- LINE 帳號（兩個識別碼）
- 2026 中秋連假日期與天數（v1 寫 9/25–27；2025 年起教師節 9/28 可能也放假，2026-09-28 是週一，**需查證是否變成四天連假**）
- 部落格文章清單（v1 記 9 篇）
- 競品帳號與參考案例（`reference-case-library` 目前是空的）

### 3. 尚未確認、不可直接使用
- 任何學員公斤數、期間、職業、照片（CASE-001）
- 價格、時長、影片數、退款、諮詢次數（OFFER-002）
- 任何份量、時程、生理機制（NUTRITION-001），包括 v1 的「八成是水」「三天再量」「不吃晚餐代謝下降」
- 法規解釋（LEGAL-001）
- 創辦人學歷、證照、體重歷程（FOUNDER-001，IMPORTED，對外使用前刷新）
- 8 個 persona 的細節（是寫作代理，不是真實受眾資料）
- 受眾原句：`audience-language-bank` 是空的，v1 的「真實用語」來自官網案例，沒有逐條來源

### 4. 可以直接用於作品集的內容
- 工作流程設計：RUNBOOK、JD-MAPPING、MEMORY-DESIGN、SDD 的風險路由
- 治理機制：claim ledger 五狀態、feedback ledger、升級門檻
- 自動檢查：`check_asset.py`＋測試＋黃金範例（可現場 demo）
- 模板：topic-scorecard、short-video-script、platform-matrix、performance-review
- `tang-copy-method.md` 的方法整理（附一手來源）
- v1 中秋企劃：**只能當「v1 → v2 我怎麼改進」的對照素材**，不能當成品展示

## 本次修改（皆已記入 `memory/working/decision-log.md`）
1. `memory/00_INDEX.md`：補列 5 個漏列檔案
2. `memory/project/claim-ledger.md`：METRIC-001 拆為 001–004
3. `docs/MEMORY-DESIGN.md`：`active-script.md` → `current-brief.md`

## 待使用者確認的提議
- C1 BRAND-001/002 降為 IMPORTED
- C2 CLAUDE.md 載入 01-voice.md
- C3 CLAUDE.md 補齊 agent／指令對照
- C4 CLAUDE.md 加入 subagent 需同意規則
- U2 兩份 performance.csv 如何統一

## 追加｜2026-09-18 晚（使用者提供 JD 後）
- C1–C4 已套用（見 decision-log）。U5 已解決：JD 原文存 `references/jd-2026-09-18.md`。
- 新增：本機營養資料庫登記（source-registry＋`references/local-sources.md`）、demand-path 選題法、`memory/working/content-calendar.md`（JD 三「內容行事曆」原本缺）。
- 仍待決定：U2 performance.csv 統一。

## 更正｜品牌資料狀態
上方「1. 已確認品牌事實：嚴格來說沒有」過於保守。research.md 是 2026-09-18 對官網與 Threads 的一手調查，已將相關 claim 升為 VERIFIED（範圍：官網自述）。仍需品牌方確認才能升 USER_CONFIRMED。U8 已解決：competitors.md、ad-regulations-sources.md 已補回 references/v1-seed/。
