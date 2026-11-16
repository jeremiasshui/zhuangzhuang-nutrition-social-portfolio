# PRD｜BGG Social Content Planner Agent

版本：3.0｜2026-09-18

## Problem

社群內容企劃不是單點「寫文案」。真正工作鏈包含：研究受眾、觀察平台與同業、規劃題目、撰寫可拍攝腳本、跨平台轉譯、交接剪輯、品質確認、整理數據，再把結果帶回下一輪內容。若 AI 只負責生成文案，無法證明應徵者具備職缺要求的完整判斷力。

## Goal

建立一套 Claude Code 可執行的社群內容企劃工作台，讓使用者能模擬並展示完整職務流程，同時保留品牌／營養專業的人為決策與可追溯性。

## Primary user

- 應徵「社群內容企劃」者。
- 入職後可延伸為實際內容營運工作台。

## Functional requirements

1. Weekly research radar：平台趨勢、競品案例、留言／FAQ、受眾真實語言。
2. Topic scoring：受眾張力、品牌適配、證據狀態、平台適配、時效性、轉換路徑。
3. Weekly 9-video content board。
4. Shoot-ready short-form script。
5. Cross-platform transformation matrix。
6. Production handoff and QA。
7. Claims review for nutrition / health facts。
8. Performance analysis by topic / hook / platform / CTA。
9. Supervisor & nutritionist feedback ledger。
10. Versioned memory and source provenance。

## Non-goals

- 自動發布社群。
- 自動取代營養師確認。
- 只以觀看數判斷內容好壞。
- 把所有平台文案做成同一份文字的長短版。
- 把一次主管修改直接寫成永久品牌規則。

## Success criteria

- 能在 10 分鐘 demo 內走完「研究 → 選題 → 腳本 → 平台轉譯 → QA → 成效回饋」的縮小版閉環。
- 每個選題可回答 audience / problem / hook / evidence / platform / CTA。
- 每份腳本可直接交給拍攝者理解。
- 高風險營養 claim 有來源狀態。
- 每次主管／營養師回饋可追溯。
- 成效報告最後必須產生下一輪可測試假設。
