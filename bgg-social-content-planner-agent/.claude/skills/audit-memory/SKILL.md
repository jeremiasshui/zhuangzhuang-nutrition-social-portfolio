---
name: audit-memory
description: 檢查 Memory 是否過時、重複、衝突、把假設當事實，並提出最小化修正。
---

1. 讀 `memory/00_INDEX.md` 與四層 memory。
2. 找：過期日期、IMPORTED 被當 VERIFIED、BLOCKED 卻出現在 core、同一事實多版本、working 沒清理、learning 沒樣本數。
3. 執行 `python scripts/check_memory.py`。
4. 輸出 `reviews/memory-audit-YYYY-MM-DD.md`：Critical / Update / Archive / Keep。
5. 可以自動修格式與明顯重複；核心語意變更只提議，不自行改。
