# Migration from attached v1

## 保留

- `CLAUDE.md` 作為專案路由。
- `.claude/agents/` 與 `.claude/skills/` 的 Claude Code native 結構。
- writer 與 reviewer 分離。
- deterministic CI / tests。
- 黃金反例、來源查證、法規與營養風險意識。
- v1 的品牌、persona、唐崇達研究做為 seed knowledge。

## 重做

1. **Memory**：v1 的 `brief/` 混了永久品牌、單週中秋、假設、即時數字。v2 分成 core/project/working/learning。
2. **Routing**：v1 每輪固定 4 writer + 5 reviewer；v2 按 risk 啟動，避免 Opus 5 過度派代理。
3. **Claims**：v1 依「待營養師確認」文字標籤；v2 加正式 claim ledger，舊資料預設 IMPORTED。
4. **Audience**：v1 要八 persona 過半都留下；v2 改成 Primary Persona 優先，避免文案為討好所有人而失焦。
5. **Convergence**：v1 最多三輪；v2 最多兩輪，仍有 BLOCKED 就交人，防止模型為過關而編造。
6. **Learning loop**：v1 有討論 log，但沒有明確發布數據升級政策；v2 建 performance → learning → project/core promotion。
7. **Portability**：v1 evidence agent 指向特定 Windows `/mnt/c/Users/...`；v2 使用 source registry，不綁機器路徑。

## 舊檔案如何使用

v1 `brief/research.md`、`brand.md`、`personas.md`、`copy-method-tang.md` 都可以當 seed；但只有品牌方明確確認的長期規則進 core，動態數字與案例進 claim ledger，週計畫只當 examples。
