---
name: learn-results
description: 從發布後的內容數據萃取可重複學習，更新 learning memory，不讓單一爆文污染核心品牌規則。
---

參數 `$ARGUMENTS` 是成效檔、數據或使用者觀察。

1. 讀 `memory/learning/performance.csv` schema。
2. 匯入或追加資料；不杜撰缺少的指標。
3. 以同平台、同內容類型、同 funnel stage 優先比較，不把不同分母直接比高低。
4. 找：hook、主題、persona、CTA、格式的重複模式。
5. 樣本不足時只寫 `candidate learning`；達升級門檻才寫 `validated-learnings.md`。
6. 記錄反例與失效模式到 `failed-patterns.md`。
7. 只「提議」更新 project/core，不自動覆蓋。使用者或總編確認後才升級。
