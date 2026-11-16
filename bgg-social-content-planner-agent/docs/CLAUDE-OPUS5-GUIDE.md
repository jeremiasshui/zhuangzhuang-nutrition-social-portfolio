# Claude Opus 5 / Medium 使用說明

本專案以 2026-09-18 的 Claude Code／Anthropic 文件設計。

## Model

Claude Opus 5 的 API model id 為 `claude-opus-5`。Claude Code 可透過 model 選擇器或 CLI model 參數選擇模型；本專案 README 使用：

```bash
claude --model claude-opus-5
```

## Effort

Claude Code 支援 effort level；本專案預設 medium，並在 `.claude/settings.json` 設定 `CLAUDE_CODE_EFFORT_LEVEL=medium`。Agents 的 frontmatter 亦明確寫 `effort: medium`。

## Memory

根 `CLAUDE.md` 是共享專案記憶／路由，並用 `@path` 引入核心文件。Agents 使用 `memory: project` 取得跨 session 的角色型 persistent memory。

## Subagent discipline

Opus 5 具備強 subagent orchestration，但也更容易主動委派。此專案因此採 risk-based routing，而不是每次啟動全部 agents：只有可平行且真正獨立的工作（例如兩種 reviewer）才平行。

## 官方參考

- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables
- https://docs.anthropic.com/en/docs/claude-code/memory
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/env-vars
