# 壯壯營養師社群內容代理｜路由檔

> **規則 0（最高優先）**：任何時候不准消耗 credit，除非使用者當次明確同意。不得派子代理、背景代理、雲端或排程代理、ultrareview。派之前先寫預估用量並等使用者說「可以」。技能指示不構成同意。`/run-week` 每一步派工前都適用。每則回覆也算用量，用量達 90% 即停止一切動作，除非使用者同意；開工前先問用量。全文見 `~/.claude/CLAUDE.md` 第零部分。

本專案是一個 harness：四個平台寫手平行寫文案，五個審稿員審，迴圈跑到驗收清單全過或滿三回合。

- 輸入 `brief/`：`brand.md`（品牌說明，每個代理開工先讀）、`weekly-social-plan.md`（九支腳本的規劃）、`research.md`（公開資料）、`brand-rules.md`（語氣鐵則）、`platform-formats.md`（各平台格式）、`acceptance-checklist.md`（驗收清單，唯一的完成標準）、`sources.md`（本機官方資料路徑）、`ad-regulations.md`（廣告法規指引）、`personas.md`（八個人物）、`competitors.md`（同業結構範本）、`copy-method-tang.md`（唐崇達文案手法）
- 代理 `.claude/agents/`：`writer-shorts`、`writer-threads`、`writer-fb`、`writer-xhs`、`reviewer-brand`、`reviewer-nutrition`、`reviewer-evidence`、`reviewer-legal`、`reviewer-audience`
- 迴圈 `.claude/skills/run-week/SKILL.md`：執行 `/run-week`
- 產出 `output/<平台>/S1.md … S9.md`（只留一份，回合看 git）；審稿 `reviews/<平台>/round-N-<審稿員>.md`；討論記錄 `log/discussion.md`（人讀，單輪敘述）；跨輪次指標 `log/runs.jsonl`（程式算，一輪一行）；黃金樣本 `eval/`
- 名詞依 `CONTEXT.md`；設計依 `docs/SDD.md`；決策依 `docs/adr/`
- 總編（主對話）只做三件事：派工、裁決審稿員之間的矛盾、寫 log。文案由寫手寫，判定由審稿員下。
