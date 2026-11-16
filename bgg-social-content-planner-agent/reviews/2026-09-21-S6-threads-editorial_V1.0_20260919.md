# Editorial Review｜2026-09-21-S6-threads

- Reviewer: copy-editor（由主對話扮演，未派 subagent；寫作者與審查者是同一個模型，獨立性有限）
- Date: 2026-09-19
- Asset: `output/2026-09-21-S6-threads_V1.0_20260919.md`（由 `output/2026-09-21-S6_V1.0_20260919.md` 轉譯）
- Claims：核心意思未改、無 claim，依 repurpose-content 步驟 5 不重開 claims review

| Check | Verdict | Original | Reason | Direction |
|---|---|---|---|---|
| Hook | PASS | | 第一行單獨成立 | |
| Single message | PASS | | 只問一件事 | |
| Brand | PASS | | 「每一個都不用躲」 | |
| Audience | PASS | | 三個場景都是連假當下會遇到的 | |
| Platform | PASS | | 短段落、約 114 字、無連結；符合 04-platforms Threads 規則 | |
| CTA | PASS | | 只有回覆 | |
| Claims | PASS | | 無 | |
| 角色語境 SPIN | PASS | | S 連假場合／P 三選一／N 被聽見；互動貼文不要求 I | |
| 價值邏輯 FABE | N/A | | 只問不答 | |
| G 語組切分 | PASS | | 每個選項兩行，一行一意 | |
| A 重音強調 | PASS | | Threads 不支援粗體，以選項編號＋換行做重點 | |
| V 語調變化 | PASS | | 問句 → 陳述 → 問句 | |
| E 延伸停頓 | PASS | | 「但我想先知道」前換段 | |
| 品牌人格落款 | PASS | | 解決短影音版 ④ | |
| 語意結構 | PASS | | 問題、選項、指令三段分明 | |
| 問句／信任落點 | PASS | | 結尾問句承接回覆 | |

## 總結

**PASS**，可發布。`scripts/check_asset.py`：第一次未跑前先改掉發布備註裡的「不加 LINE」（說明文字會觸發多重 CTA 誤判），跑一次 OK。
