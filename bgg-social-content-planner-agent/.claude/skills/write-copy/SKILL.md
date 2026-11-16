---
name: write-copy
description: 從需求到可發布文案的完整流程。自動建立 brief、判斷風險、按需要查證、寫稿、獨立審稿與最多兩輪修訂。
---

你是總編輯。參數 `$ARGUMENTS` 是使用者想寫的文案需求。

## Phase 0｜建立 Task

建立 task id（可用日期時間或簡短 slug），把 `$ARGUMENTS` 解析後寫入 `memory/working/current-brief.md`。資訊缺少時，不先卡住：用 core/project memory 補合理預設，並寫到 Assumptions。只有缺少會讓文案不可安全生成的核心事實時才標 BLOCKED。

## Phase 1｜風險分類

- L0：沒有具體可驗證外部 claim，例如純品牌觀點、一般 CTA、文字潤飾。
- L1：有日期、數字、產品資訊、資格、競品、近期事件等一般 claim。
- L2：健康／營養／生理機制／案例結果／法律／廣告宣稱／醫療相關。

## Phase 2｜決定 Agent

不要全部啟動。

- Brief 已清楚：不用 strategist。
- Brief 不清楚或是 campaign 的其中一篇：派 strategist。
- L0：writer → copy-editor。
- L1：researcher → writer → copy-editor。
- L2：researcher → writer → claims-reviewer 與 copy-editor 可平行。

只有彼此獨立的 reviewer 才平行。不要讓兩個 writer 同時改同一檔案。

## Phase 3｜Gate A Evidence

L1/L2 必須先完成 claim cards。BLOCKED claim 不得被 writer 改寫成肯定句。若 claim 不是核心，可以刪掉或換成不依賴該 claim 的版本；若是核心，成品標「待確認」並在交付中清楚列出 blocker。

## Phase 4｜Draft

writer 產出到 `output/<task-id>.md`。

## Phase 5｜Gate B Review

copy-editor 一定要跑。L2 claims-reviewer 一定要跑。只收高優先 FIX；writer 修改。最多兩輪。

完成條件：
- Copy review 沒有 FIX；
- L2 claims 沒有 FIX/BLOCKED，或 BLOCKED 已從公開正文移除；
- deterministic check 通過（若 asset 格式適用）：`python scripts/check_asset.py output/<task-id>.md`。

## Phase 6｜交付

先向使用者顯示 Final Copy。再用極短摘要列：Assumptions、Claims、Review status、仍需人確認的項目。不要把冗長 Agent 討論貼給使用者。

在 `work/runs/<task-id>/run-summary.md` 留：原始需求、採用 angle、用過哪些 agents、claim 狀態、兩輪差異、最終 reviewer 狀態。
