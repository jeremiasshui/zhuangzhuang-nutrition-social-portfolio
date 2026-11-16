---
name: plan-campaign
description: 把商業目標轉成一週／一月內容計畫；先規劃，不一次把所有文案都生成。
---

參數 `$ARGUMENTS` 是 campaign 需求。

1. 讀 core memory 與 current content strategy。
2. 派 strategist 建 campaign brief；若涉及節日、競品、當期趨勢或數據，平行派 researcher 做只讀 research。
3. 建立 `plans/<campaign-id>.md`，內容至少有：目標、受眾、JTBD、期間、主軸、content pillars 配比、funnel 配比、平台角色、每個 asset 的一句 brief、CTA、主要 KPI、需查證 claim。
4. 每個 asset 都要能回答：「為什麼現在發」「對誰」「只想改變哪個認知／行為」。
5. 不在此 skill 自動生成全部成品。使用者要開始寫時，再逐個或小批次呼叫 `/write-copy`，避免一次 30 篇造成品質漂移。
