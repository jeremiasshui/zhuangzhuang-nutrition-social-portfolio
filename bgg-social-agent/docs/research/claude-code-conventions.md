# Claude Code 自訂代理、技能及設定慣例

根據官方文件整理的 Claude Code 五大問題答案。

---

## 1. 專案層級自訂子代理定義檔的 Frontmatter 欄位

**檔案位置：** `.claude/agents/<name>.md`

**支援的 Frontmatter 欄位：**

| 欄位名稱 | 必要 | 說明 |
|---------|------|------|
| `name` | 是 | 唯一識別碼，使用小寫字母和連字號 |
| `description` | 是 | 何時應委派給此子代理 |
| `tools` | 否 | 子代理可使用的工具列表 |
| `disallowedTools` | 否 | 要禁用的工具 |
| `model` | 否 | 子代理使用的模型（sonnet、opus、haiku、fable、完整 ID 或 inherit） |
| `permissionMode` | 否 | 權限模式（default、acceptEdits、auto、dontAsk、bypassPermissions、plan 或 manual） |
| `maxTurns` | 否 | 最大代理循環數 |
| `skills` | 否 | 啟動時預加載的技能 |
| `mcpServers` | 否 | 此子代理可用的 MCP 伺服器 |
| `hooks` | 否 | 此子代理的生命週期鉤子 |
| `memory` | 否 | 持久化記憶範圍（user、project 或 local） |
| `background` | 否 | 設為 true 子代理在背景執行 |
| `omitClaudeMd` | 否 | 設為 true 跳過 CLAUDE.md 檔案 |
| `effort` | 否 | 工作強度等級（low、medium、high、xhigh、max） |
| `isolation` | 否 | 隔離模式，設為 worktree 使用 git worktree |
| `color` | 否 | 顯示顏色（red、blue、green、yellow、purple、orange、pink、cyan） |
| `initialPrompt` | 否 | 當代理為主工作階段時自動提交的首個提示 |
| `experimental` | 否 | 實驗性選項映射 |

**tools 欄位的工具名稱格式：**

- **精確工具名稱：** tools: Read, Grep, Glob, Bash
- **MCP 伺服器模式：** tools: Read, mcp__github, mcp__slack
- **Agent 生成限制：** tools: Agent(worker, researcher), Read, Bash
- **禁用列表：** disallowedTools: Write, Edit, mcp__*

**Glob 工具合法性：** 是。Glob 是官方合法的內建工具名稱，用於根據模式匹配搜尋檔案。

**來源：** https://code.claude.com/docs/en/sub-agents.md

---

## 2. Agent 工具中的 subagent_type 參數與子代理載入時機

**subagent_type 參數填寫方式：**

呼叫 Agent 工具派出自訂代理時，subagent_type 要填寫該子代理定義文件的 name 欄位值。例如子代理檔案 .claude/agents/code-reviewer.md 的 name: code-reviewer，則 subagent_type 應填 code-reviewer。

若省略 subagent_type 且專案中不存在 general-purpose 子代理，呼叫會失敗並要求指定。

**子代理載入時機：**

子代理會從以下位置被發現（優先順序如下）：

1. **組織管理設定**（全組織範圍）
2. **--agents CLI 旗標**（當前工作階段）
3. **.claude/agents/**（當前專案）
4. **~/.claude/agents/**（所有專案 - 使用者層級）
5. **插件的 agents/ 目錄**（插件已啟用）

**工作目錄的影響：**

- Claude Code 會監視 .claude/agents/ 和 ~/.claude/agents/ 目錄在工作階段中的變化
- **新增 agents 目錄：** 需要重啟以開始監視
- **編輯現有檔案：** 在數秒內被偵測，無需重啟
- **--add-dir 資料夾中的檔案：** 不被監視，變更後需要重啟

工作目錄會影響優先順序（項目 3 優先於項目 4），但不影響是否載入——只要在支援的位置，子代理就會被發現。

**來源：** https://code.claude.com/docs/en/sub-agents.md

---

## 3. 專案層級技能的 Frontmatter 必要欄位與叫用行為

**檔案位置：** `.claude/skills/<skill-name>/SKILL.md`

**Frontmatter 必要欄位：** 官方文件未強制要求任何欄位。

**強烈推薦欄位：**

- description — Claude 用此決定何時自動載入技能

**其他常用欄位（非必要）：**

- name — 技能的顯示標籤（個人/專案技能時，命令名稱由目錄名決定）
- arguments — 技能接受的參數
- visibility — 控制誰可叫用（預設公開）

**使用者用 /<name> 叫用時的行為：**

1. 技能按目錄名稱命名：
   - ~/.claude/skills/deploy-staging/SKILL.md → /deploy-staging
   - .claude/skills/my-skill/SKILL.md → /my-skill
   - 嵌套技能：apps/web/.claude/skills/deploy/SKILL.md → /apps/web:deploy
   - 插件技能：my-plugin/skills/review/SKILL.md → /my-plugin:review

2. Claude Code 執行 SKILL.md 中的內容，可包含：
   - Shell 指令碼
   - 互動式指令
   - 基於工具的工作流程
   - 自訂邏輯

3. 技能載入位置優先順序：
   - 專案技能（.claude/skills/）
   - 使用者技能（~/.claude/skills/）
   - 嵌套技能（子目錄）
   - 插件技能

**來源：** https://code.claude.com/docs/en/skills.md

---

## 4. 子代理間通信與 Agent Teams 機制

**預設行為：** 子代理預設無法相互傳訊息。

**官方機制 — Agent Teams：**

是的，有官方的「agent teams」機制支援子代理團隊協作與相互溝通。

**啟用方式：**

Agent Teams 預設禁用。需在 settings.json 或環境變數中設定：

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

或在命令列：
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude
```

**主要功能：**

1. **直接訊息傳遞** — 團隊成員可彼此直接傳訊息，無須透過主工作階段轉發
2. **共享工作列表** — 有 Task 工具的代理可聲明和完成任務
3. **自我協調** — 團隊成員在共享任務列表上獨立工作
4. **獨立上下文** — 每個團隊成員有自己的上下文視窗
5. **生命週期鉤子** — TeammateIdle、TaskCreated、TaskCompleted 等

**子代理 vs Agent Teams 的區別：**

| 特性 | 子代理 | Agent Teams |
|-----|--------|-----------|
| **通信** | 結果回傳給主代理 | 團隊成員直接互相訊息 |
| **協調** | 主代理管理所有工作 | 透過共享任務列表自我協調 |
| **Token 成本** | 較低 | 較高（每個成員獨立） |

**團隊成員名稱與召喚：**

- 主代理為每個團隊成員指定名稱
- 可使用 @teammate-name 格式直接傳訊息
- 可透過 SendMessage 工具在代理之間傳訊息

**限制：**

- 目前實驗性功能，有已知限制
- 工作階段恢復時不會恢復內嵌式團隊成員
- 非互動式模式（-p 旗標）不啟用團隊
- 一個工作階段只能有一個團隊

**來源：** https://code.claude.com/docs/en/agent-teams.md

---

## 5. Claude Code 對 CLAUDE.md 的載入規則

**載入規則 — 完整優先順序：**

Claude Code 按以下順序載入 CLAUDE.md 檔案（從最廣泛到最具體）：

1. **組織管理原則 CLAUDE.md**
   - macOS: /Library/Application Support/ClaudeCode/CLAUDE.md
   - Linux/WSL: /etc/claude-code/CLAUDE.md
   - Windows: C:\Program Files\ClaudeCode\CLAUDE.md

2. **使用者層級 CLAUDE.md** — ~/.claude/CLAUDE.md（所有專案）

3. **專案層級 CLAUDE.md** — ./CLAUDE.md 或 ./.claude/CLAUDE.md

4. **本機層級 CLAUDE.md** — ./CLAUDE.local.md（個人偏好，加入 .gitignore）

**層級合併方式：**

- 所有發現的檔案被串接入上下文，而非相互覆蓋
- 目錄樹中的內容按檔案系統根目錄向下至工作目錄順序組織
- 範例：在 foo/bar/ 啟動 Claude，載入順序為 foo/CLAUDE.md → foo/CLAUDE.local.md → foo/bar/CLAUDE.md → foo/bar/CLAUDE.local.md
- 距離工作目錄越近的指令最後讀取（優先級更高）

**子目錄 CLAUDE.md 的載入時機：**

- **根目錄及上級：** 在工作階段啟動時即時載入
- **子目錄：** 按需載入——當 Claude 讀取那些子目錄中的檔案時才載入

**工作目錄的影響：**

- 工作目錄決定向上搜索的起點和向下搜索的範圍
- 若在 foo/bar/ 啟動，會搜索 foo/bar/ 及其上級；若子目錄中有 CLAUDE.md 會在訪問時載入

**其他載入方式：**

1. **@path 匯入** — CLAUDE.md 可用 @path/to/file 語法匯入其他檔案
2. **.claude/rules/** — 路徑特定規則可用 paths 欄位只在匹配檔案時載入
3. **--add-dir 旗標** — 需設環境變數 CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 才會加載額外目錄的 CLAUDE.md

**排除特定 CLAUDE.md：**

使用 claudeMdExcludes 設定跳過不相關的檔案：

```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/path/to/other-team/.claude/rules/**"
  ]
}
```

**來源：** https://code.claude.com/docs/en/memory.md

---

## 摘要

本文檔涵蓋 Claude Code 自訂代理、技能與設定的五項核心慣例，包括子代理定義的 13 個 Frontmatter 欄位、tools 欄位格式（支援 Glob）、subagent_type 參數用法、技能無必要欄位但推薦 description、Agent Teams 的官方協作機制（需啟用環境變數），以及 CLAUDE.md 的分層加載規則（工作目錄優先級、子目錄按需加載、支援匯入與路徑規則）。
