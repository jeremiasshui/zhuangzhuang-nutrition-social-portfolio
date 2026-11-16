# Evaluation

## Copy scorecard（只作診斷，不用總分掩蓋 BLOCKED）

- Brand fit: PASS/FIX
- Audience specificity: PASS/FIX
- Single message: PASS/FIX
- Hook/first screen: PASS/FIX
- Concrete action: PASS/FIX
- Platform fit: PASS/FIX
- CTA fit: PASS/FIX
- Claims: PASS/FIX/BLOCKED
- 角色語境 SPIN／價值邏輯 FABE／語意節奏 GAVE／品牌人格落款／語意結構／問句與信任落點: PASS/FIX（標準見 `references/landing-page-aiseo-method.md`）

## Golden tests

`examples/good-threads.md`：合格結構。  
`examples/bad-guarantee.md`：必須被 deterministic guardrail 擋。  
`examples/bad-double-cta.md`：必須被 CTA 檢查擋。

## Human override

Reviewer 的 PASS 不是絕對真值。若人推翻 reviewer，記在 `memory/learning/failed-patterns.md` 或 reviewer agent memory；有重複模式再修規則。
