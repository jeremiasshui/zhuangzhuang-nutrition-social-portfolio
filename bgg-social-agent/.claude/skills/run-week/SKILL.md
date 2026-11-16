---
name: run-week
description: 跑一次完整迴圈：四寫手平行 → 兩審稿員平行 → 有 FIX 就回寫手改 → 全 PASS 或滿三回合停 → 寫討論記錄。
---

你是總編。全程用 Agent 工具派工，同一回合的代理在同一則回覆裡派出（平行）。

1. N = 1。派 `writer-shorts`、`writer-threads`、`writer-fb`、`writer-xhs`，訊息只有一行：「回合 N=1，讀專案 CLAUDE.md 後照你的代理定義執行。」完成：`output/<平台>/` 四個資料夾各九檔；每個寫手在自己的分支 `writer/<平台>` 提交並開 PR。
2. 先跑 `python scripts/check_copy.py output/`；紅燈就把失敗訊息交回對應寫手，綠燈才往下。再派五個審稿員 `reviewer-brand`、`reviewer-nutrition`、`reviewer-evidence`、`reviewer-legal`、`reviewer-audience`，同一則回覆平行派出，訊息同上格式，並要求先審 `eval/` 黃金樣本記命中率。完成：`reviews/<平台>/round-N-*.md` 每平台五份。
3. 讀每平台五份審稿的末行，按平台加總 FIX。收斂與否按平台各自判。
   - FIX = 0 → 步驟 5。
   - N = 3 → 步驟 5，log 標「未收斂」清單。
   - 否則：審稿員之間對同一句意見矛盾時，你裁決並記到 `log/discussion.md`「裁決」節。N += 1。用 SendMessage 把該平台的 FIX 清單交回同一個寫手（保留它的記憶），訊息：「回合 N=<n>，依 reviews/<平台>/round-<n-1>-* 修改，在同一分支提交。」回到步驟 2。
4. （保留）
5. 寫 `log/discussion.md`：每回合指標表（FIX 數、重複 FIX 模式、審稿員矛盾次數、黃金樣本命中率、人推翻率、CI 規則數）；查證員「可升級為引用」與法規員「固定揭露句」的採納決定；每回合三筆代表性意見與寫手的改法（引原句、改後句）；裁決；未收斂項目；一段「這個迴圈學到什麼」。完成：讀者不看任何其他檔案也能看懂迴圈發生了什麼。

6. 追加一行到 `log/runs.jsonl`（不存在就建檔，只追加、不改前面的行）。欄位固定如下，一行一輪 `/run-week`：

```json
{"date":"YYYY-MM-DD","run":"<跑了什麼>","rounds":<跑到第幾回合>,"dispatches":<總派工次數>,"converged":<true|false>,"unconverged":["<平台>"],"interventions":<人插手次數>,"session_pct":[<開工前>,<結束後>],"week_pct":[<開工前>,<結束後>],"note":"<一句>"}
```

- `dispatches`：Agent 工具派出的總次數（一回合 4 寫手 + 5 審稿員 = 9，含 SendMessage 回修則加計）。這是成本主指標，能數到個位數。
- `interventions`：你（人）出手的次數——裁決矛盾、推翻審稿員、手改文案、中止重跑，各算一次。
- `session_pct` / `week_pct`：開工前後各看一次 `/usage` 抄整數。只能當粗略佐證：整數解析度下一輪可能都顯示 0，不要拿它算單位成本。Fable 有獨立週額度，狀態列讀不到，若該輪用 Fable 派工就在 `note` 註明。
- 完成：連續三輪之後，「每支腳本花幾次派工」「幾輪沒收斂」「平均插手幾次」三個數字都能直接從這個檔案算出來，不用回想。
