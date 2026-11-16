# CI、分支/PR 流程、Claude Code 在 Actions 裡跑：三方來源實務整理

整理日期：2026-09-18。只收三種來源：Will 保哥本人部落格（blog.miniasp.com）、高見龍本人教材與部落格（gitbook.tw、kaochenlong.com）、Anthropic 官方文件（code.claude.com/docs、github.com/anthropics/claude-code-action）。每條建議附網址與逐字引用；英文引用後面用括號給一句白話中文。凡是我自己依官方文件組合、或來源只有間接支持的地方，都明確標「研究員組合」或「間接」。

專案情境（判斷適用性的依據）：私人 GitHub 倉庫；四條 `writer/<平台>` 分支各開 PR 到 `main`；CI 跑 `python -m unittest discover -s tests -v` 和 `python scripts/check_copy.py output/`；希望 PR 上由 Claude 自動審文案；使用者是 Claude Max 訂閱，不確定有沒有 API key。現有 workflow 在 `.github/workflows/copy-check.yml`。

---

## 一、GitHub Actions workflow 寫法建議

### 1-1 觸發事件：PR 事件用 `pull_request`，自動化任務用 `push`/`workflow_dispatch`

- Anthropic 官方的 PR 審查範例只掛四種 PR 事件：
  > `on:\n  pull_request:\n    types: [opened, synchronize, ready_for_review, reopened]`
  > — https://code.claude.com/docs/en/github-actions （「Run a skill」段）
- Will 保哥的發行 workflow 用 `main` 分支 push 加手動觸發：
  > 「以下是我完整的 GitHub Actions 設定檔 (`publish.yml`)，該檔案必須放在 Repo 的 `.github/workflows/publish.yml` 路徑，這樣當你的 `main` 分支有新的 commit 或手動觸發 workflow 時，GitHub 就會執行這個設定檔。」
  > 對應 YAML：`on:\n  workflow_dispatch:\n  push:\n    branches:\n      - main`
  > — https://blog.miniasp.com/post/2025/02/07/How-to-use-the-Chrome-Web-Store-Publish-API-to-automate-the-publishing-of-a-Chrome-Extension （2025/02/07）
- Anthropic 提醒觸發事件要涵蓋 Claude 推的 commit：
  > "Check that your CI workflow's triggers include the events Claude's pushes produce, such as `push` or `pull_request`"（確認 CI 的觸發事件包含 Claude 推送會產生的事件）
  > — https://code.claude.com/docs/en/github-actions （Troubleshooting）

### 1-2 permissions 最小權限

- Anthropic：
  > "Grant the workflow only the permissions it needs, and review Claude's changes before merging."（只給 workflow 需要的權限，合併前檢查 Claude 的改動）
  > — https://code.claude.com/docs/en/github-actions （Best practices）
- Anthropic 的唯讀審查範例權限只有：
  > `permissions:\n  contents: read\n  pull-requests: read\n  issues: read\n  id-token: write`
  > — https://code.claude.com/docs/en/github-actions （「Run a skill」段）
- claude-code-action 安全文件：
  > "If you need `'*'`, scope workflow `permissions:` to the minimum required"（若真的要開放所有 bot，把 workflow 權限縮到最小）
  > — https://github.com/anthropics/claude-code-action/blob/main/docs/security.md
- Will 保哥的 workflow 因為要建 Release，才給 `contents: write`，並說明要先開 token 權限：
  > 「你必須先啟用 `secrets.GITHUB_TOKEN` 的權限，設定的步驟如下：」
  > — https://blog.miniasp.com/post/2025/02/07/How-to-use-the-Chrome-Web-Store-Publish-API-to-automate-the-publishing-of-a-Chrome-Extension
- 適用判斷：我們的測試與檢查腳本只讀檔，`contents: read` 已足夠（現有 copy-check.yml 就是這樣）。Claude 審查 job 若要留 PR 留言，依官方範例另開 `pull-requests: write` 或改走 inline-comment MCP 工具（見第三節）。

### 1-3 Python 版本設定與快取

- 三個來源都沒有 Python 專用的 setup-python / pip 快取寫法（見第五節）。可參考的是 Will 保哥對 Node 的做法（`actions/setup-node@v4` 加 `node-version: '20'`），同一篇網址如上。
- 執行平台：Will 保哥建議 Linux runner，因為內建壓縮工具：
  > 整理自原文（非逐字）：使用 `ubuntu-latest` 而不是 `windows-latest`，因為 Linux 內建 `zip`/`unzip` 方便壓縮解壓。
  > — https://blog.miniasp.com/post/2023/03/25/Improve-GitHub-Actions-workflow-by-archive-files-before-upload-artifact （2023/03/25）

### 1-4 Artifact（工作產物）與儲存空間

我們目前不上傳 artifact；若日後要把 `output/` 或審稿報告存成 artifact，Will 保哥兩篇文章的教訓適用：

- 上傳前先打包，時間大幅下降：
  > 「在 CI 的 `actions/upload-artifact@v2` 這個步驟花費了超級大量的時間上傳 `node_modules` 資料夾中的檔案」；改成先壓縮後 「整體 CI/CD 的時間直接從 `26m 34s` 降到 `8m 58s`」
  > — https://blog.miniasp.com/post/2023/03/25/Improve-GitHub-Actions-workflow-by-archive-files-before-upload-artifact
- 私人倉庫有儲存額度，會直接擋上傳：
  > 錯誤訊息原文 "Artifact storage quota has been hit. Unable to upload any new artifacts."；作者建議「刪除超過 14 天的所有 artifacts 與 workflow runs」
  > — https://blog.miniasp.com/post/2025/08/28/How-to-solve-the-issue-of-running-out-of-Artifact-storage-in-GitHub-Actions （2025/08/28）

### 1-5 失敗訊息呈現

- 三個來源都沒有談 GitHub Actions 的 `::error::` 註解或失敗訊息格式（見第五節）。
- 唯一相關：Anthropic 說 Claude 可以讀 CI 結果，前提是給 `actions: read`：
  > "Yes! Claude can access GitHub Actions workflow runs, job logs, and test results on the PR where it's tagged. To enable this: 1. Add `actions: read` permission to your workflow"（Claude 可讀該 PR 的 workflow 執行、job 日誌與測試結果，要先加 `actions: read`）
  > — https://github.com/anthropics/claude-code-action/blob/main/docs/faq.md

### 1-6 Required status check（必過檢查）與 Claude 審查的關係

- 三個來源都沒有教怎麼在 GitHub 設 required status check（見第五節）。
- 但 Anthropic 明說託管版 Code Review 不會擋合併：
  > "The check run always completes with a neutral conclusion so it never blocks merging through branch protection rules."（檢查結果一律「中性」，不會透過分支保護擋合併）
  > — https://code.claude.com/docs/en/code-review
- 推論（研究員）：真正該設成必過的是我們自己的 `copy-check` job；Claude 審稿當「建議」，不當「閘門」，符合官方設計取向。

### 1-7 成本與失控防護

- Anthropic：
  > "Set `--max-turns` in `claude_args` to limit iterations" / "Set workflow-level timeouts to avoid runaway jobs" / "Use GitHub's concurrency controls to limit parallel runs"（限制回合數、設 workflow 逾時、用 concurrency 限制同時執行）
  > "Keep your `CLAUDE.md` concise, since Claude reads it on every run"（CLAUDE.md 保持精簡，每次執行都會讀）
  > — https://code.claude.com/docs/en/github-actions （Manage costs）

---

## 二、分支與 PR 流程建議

### 2-1 分支很便宜，流程要全隊一致

- 高見龍：
  > 「重點是 Flow 是要讓整個開發團隊看的，要讓所有人都遵守同一套流程」
  > — https://gitbook.tw/chapters/gitflow/using-git-flow
- 高見龍對 Git Flow 五種分支的定義（master 放「穩定、隨時可上線的版本」，develop 是「所有開發的基礎分支」）：
  > 「主要是用來放穩定、隨時可上線的版本」；「所有開發的基礎分支」；「這幾年來也陸續有其它優秀的開發流程，例如 GitHub Flow、Gitlab Flow 等流程」
  > — https://gitbook.tw/chapters/gitflow/why-need-git-flow
- 適用判斷：我們的 `main` 對應「隨時可上線」；四條 `writer/<平台>` 對應 feature 分支。不需要 develop/release/hotfix，高見龍自己也說 GitHub Flow 等更簡單的流程已出現。

### 2-2 分支命名

- 高見龍教材用 `feature/`、`hotfix/` 這類前綴（Git Flow 工具自動加），但沒有給硬性命名規範（見第五節）。
- Will 保哥的 worktree 範例用 `hotfix/v2.0-bug` 這種「類型/描述」格式：
  > `git worktree add -b hotfix/v2.0-bug ../MyRepo-master master`
  > — https://blog.miniasp.com/post/2023/10/29/git-worktree-manage-multiple-working-directories （2023/10/29）
- Anthropic 建議把分支命名規範寫進 CLAUDE.md：
  > 表格「✅ Include」欄：`Repository etiquette (branch naming, PR conventions)`（倉庫禮節：分支命名、PR 慣例）
  > — https://code.claude.com/docs/en/best-practices （Write an effective CLAUDE.md）
- 適用判斷：`writer/<平台>` 已符合「類型/描述」格式；要做的是把它寫進 CLAUDE.md。

### 2-3 多分支並行：用 git worktree 而不是一直切換

- Will 保哥：
  > 「同時開啟不同分支的程式碼做開發，所以你並不想要經常的切換分支」；「兩個工作目錄只共用一組本地儲存庫」
  > — https://blog.miniasp.com/post/2023/10/29/git-worktree-manage-multiple-working-directories
- 適用判斷：四個寫手代理平行寫作，正是這個場景。

### 2-4 PR 的目的：讓 main 隨時可上線

- 高見龍：
  > 「負責管理這個專案的人收到 PR 後，進行 Code Review 並確認無誤後便可進行合併，這樣一來可讓這個產品分支處於隨時都是可上線的狀態。」
  > — https://gitbook.tw/chapters/github/pull-request
- 高見龍實際收作業的做法（PR 進指定分支、他整理後合併）：
  > 「請同學完成作業後，發送 PR 到該分支」；「我會使用 rebase 方式整理分支並合併到 master 分支」
  > — https://kaochenlong.com/2017/12/12/use-github-for-homework （2017/12/12）
  > 同文列出退件條件（整理自原文，非逐字）：放錯目錄、一個 PR 裡 commit 太多、測試沒過、commit 訊息無意義、有衝突未解。

### 2-5 PR 大小與 commit 整理

- 高見龍：一個 PR 裡 commit 太多是退件理由（同上 kaochenlong.com 文章，非逐字）。
- 高見龍教把瑣碎 commit 合成一個：
  > 「太過「瑣碎」」的 commit「會讓 Commit 看起來更乾淨一些」（合併後）；操作是在 `git rebase -i` 把 `pick` 改成 `squash`，「最後一行的 `27f6ed6` 會跟前一個 Commit `2bab3e7` 進行合併」
  > — https://gitbook.tw/chapters/rewrite-history/merge-multiple-commits-to-one-commit
- Will 保哥的 commit 訊息慣例：
  > 「我在我公司已經有很多專案採用 Conventional Commits 風格來寫 Git 提交訊息」
  > — https://blog.miniasp.com/post/2024/12/27/GitHub-Copilot-Cookbook-Define-Custom-Instructions-for-Generating-Git-Commit-Messages （2024/12/27）

### 2-6 rebase 還是 merge

- 高見龍的原則：本地整理用 rebase，推出去的別 rebase。
  > 「使用 Rebase 分支來整理完再推出去」；「Rebase 等於是修改歷史，修改已經推出去的歷史可能會對其它人帶來困擾」；「對於已經推出去的內容，非必要的話請盡量不要使用 Rebase」
  > — https://gitbook.tw/chapters/branch/merge-with-rebase
- 拉更新時可用 `git pull --rebase` 避免多餘的合併 commit：
  > 「為了合併而產生的這個 Commit 本身並沒有什麼問題，但如果你不想要這個額外的 Commit，可考慮使用 Rebase 方式」
  > — https://gitbook.tw/chapters/github/pull-from-github
- 推不上去時先拉再推，不要強推：
  > 「這段訊息的意思是線上版本的內容比你電腦裡這份還要新，所以 Git 不讓你推上去。」；「因為你電腦裡的內容是比較舊的，所以你應該先拉一份線上版本的回來更新，然後再推一次」；（對 force push）「雖然這樣一定會成功，但接下來你就要去面對 Sherly，跟她解釋為什麼你把她的進度蓋掉了。」
  > — https://gitbook.tw/chapters/github/fail-to-push
- 快轉合併 vs 保留「小耳朵」（merge commit）：
  > 「非快轉模式合併的好處是可以完整保留分支的樣子，但如果你不是很介意這件事的話其實也就沒必要硬要做出小耳朵囉。」
  > — https://gitbook.tw/chapters/branch/merge-commit
- 適用判斷：`writer/<平台>` 分支各只有一個寫手在動，rebase 到最新 `main` 再推是安全的；`main` 永遠不 rebase、不 force push。GitHub 上「Squash and merge」還是「Merge」：高見龍沒直接談 GitHub 的合併按鈕選項（見第五節）；他自己的作法是「rebase 整理後合併到 master」。

### 2-7 保護 main 與 review 規則

- 三個來源都沒有逐步教 GitHub 分支保護設定（見第五節）。
- 有依據的原則：PR 要 review 後才合併（高見龍 2-4）；CI 通過是硬條件（高見龍退件條件「測試沒過」）；Claude 的審查是建議不是閘門（Anthropic 1-6）；合併前人要看 Claude 的改動（Anthropic 1-2）。

---

## 三、Claude Code 在 Actions 裡跑

### 3-1 兩條路：託管版 Code Review vs 自架 claude-code-action

- 託管版 Code Review 只給 Team/Enterprise，Max 用不到：
  > "Code Review is in research preview, available for Team and Enterprise subscriptions."
  > "Code Review usage is billed separately through usage credits and does not count against your plan's included usage."（另外用 usage credits 計費）
  > — https://code.claude.com/docs/en/code-review
- 所以我們走 claude-code-action（自己寫 workflow）：
  > "To run Claude in your own CI infrastructure instead of this managed service, see GitHub Actions"
  > — 同上

### 3-2 安裝步驟

- 快速安裝：
  > "Quick setup: run `/install-github-app` from Claude Code. Claude Code installs the GitHub App, adds your authentication secret, and prepares the workflow pull request for you"
  > "For either path, you need admin access to the repository."（兩種方式都需要倉庫 admin）
  > "Before you start, install the GitHub CLI and authenticate it with `gh auth login`."
  > "Otherwise, choose between creating a long-lived token with your Claude subscription and pasting in an API key"（沒有 API key 時，可選「用訂閱建立長效 token」）
  > "Claude Code saves the credential as a repository secret, named `ANTHROPIC_API_KEY` for an API key or `CLAUDE_CODE_OAUTH_TOKEN` for a subscription token."
  > — https://code.claude.com/docs/en/github-actions （Quick setup）
- 手動安裝三步：
  > 1. "Install the Claude GitHub App to your repository." 2. "Add one of the following secrets to your repository" 3. "Copy examples/claude.yml into your repository's `.github/workflows/` directory. ... If you added `CLAUDE_CODE_OAUTH_TOKEN` instead, change the workflow's `anthropic_api_key` line to `claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}`."
  > — 同上（Manual setup）
- GitHub App 用到的三個權限：
  > "Contents: read and write, so Claude can modify repository files / Issues: read and write, so Claude can respond to issues / Pull requests: read and write, so Claude can create PRs and push changes"
  > — 同上
- 安裝 App 時無法只勾一部分權限：
  > "When you install the app, you accept its full permission set. GitHub doesn't let you accept a subset."
  > — 同上（GitHub App permissions）

### 3-3 憑證：訂閱制（Max）能用，怎麼產生 token

- 訂閱制可用，明文列出 Pro/Max/Team/Enterprise：
  > "`CLAUDE_CODE_OAUTH_TOKEN`: an OAuth token that authenticates with your Claude subscription, available on Pro, Max, Team, and Enterprise plans. Generate one by running `claude setup-token` locally."
  > — https://code.claude.com/docs/en/github-actions
  > "This token authenticates with your Claude subscription and requires a Pro, Max, Team, or Enterprise plan."
  > — https://code.claude.com/docs/en/authentication （Generate a long-lived token）
- 怎麼產生、有效期、不會自動存：
  > "For CI pipelines, scripts, or other environments where interactive browser login isn't available, generate a one-year OAuth token with `claude setup-token`"（一年期）
  > "The command opens the same browser authorization flow as `/login`, and the token prints to the terminal after you approve access in the browser. It does not save the token anywhere; copy it and set it as the `CLAUDE_CODE_OAUTH_TOKEN` environment variable wherever you want to authenticate"
  > — 同上
- 用訂閱 token 跑，帳算在訂閱額度而不是 API 帳單：
  > "If you authenticate with an OAuth token, runs use your Claude subscription instead of API billing."
  > — https://code.claude.com/docs/en/github-actions （Manage costs）
- token 綁個人訂閱；多人共用倉庫官方建議改 API key（我們是單人私倉，不受影響）：
  > "For a secret shared across repositories, authenticate with an API key from the Claude Console rather than an OAuth token, since an OAuth token is tied to the subscription of the person who ran `claude setup-token`."
  > — 同上（Set up for an organization）
- 憑證絕不能寫進檔案：
  > "Never commit API keys or OAuth tokens directly to your repository. Always store them as GitHub Secrets and reference them in workflows"
  > — 同上（Protect your credentials）
- 若改用 `claude -p` 自己寫步驟：不能加 `--bare`，因為 bare mode 不讀訂閱 token：
  > "Bare mode does not read `CLAUDE_CODE_OAUTH_TOKEN`. If your script passes `--bare`, authenticate with `ANTHROPIC_API_KEY` or an `apiKeyHelper` instead."
  > — https://code.claude.com/docs/en/authentication
  > "In bare mode, Claude Code never reads OAuth credentials or the system keychain."
  > — https://code.claude.com/docs/en/headless
- 憑證選用順序（`CLAUDE_CODE_OAUTH_TOKEN` 是第 5 順位，比 `/login` 高、比 `ANTHROPIC_API_KEY` 低）：
  > "5. `CLAUDE_CODE_OAUTH_TOKEN` environment variable. A long-lived OAuth token generated by `claude setup-token`. Use this for CI pipelines and scripts where browser login isn't available."
  > — https://code.claude.com/docs/en/authentication （Authentication precedence）

### 3-4 觸發方式與兩種模式

- 互動模式（等 `@claude`）vs 自動化模式（有 `prompt` 就直接跑）：
  > "Interactive mode: when the workflow provides no `prompt` input, Claude waits for the trigger phrase, `@claude` by default"
  > "Automation mode: when the workflow provides a `prompt` input, Claude runs without waiting for a mention ... By default, results appear in the workflow run log rather than a comment."
  > — https://code.claude.com/docs/en/github-actions
- 誰能觸發（防止 bot 迴圈）：
  > "Write access: on issue and pull request events, the triggering user must have write access to the repository."
  > "Human actor: on every event, the Claude Code GitHub Action rejects a bot actor unless you list it in `allowed_bots`, which keeps bots from triggering Claude in a loop."
  > — 同上（Who can trigger runs）
- 自動審查會跳過的 PR：
  > "Claude skips draft and closed pull requests, pull requests it judges not to need a review, such as automated or trivial ones, and pull requests that already have a comment from Claude."
  > — 同上（Run a skill）
- 純文字 prompt 預設沒有 shell/GitHub 工具，要自己開：
  > "For a plain-text prompt, Claude has no shell or GitHub API access until you grant the tools the prompt needs, with `--allowedTools` in `claude_args`"
  > — 同上（Run on a schedule）
- 安全文件：不要把不可信的 ref 直接 checkout 到工作目錄根（我們是同倉庫分支，風險低，但原則要知道）：
  > "Do not check out an untrusted ref into the workspace root before this action."
  > — https://github.com/anthropics/claude-code-action/blob/main/docs/security.md

### 3-5 官方逐字 workflow 範例（PR 自動審查）

出處：https://code.claude.com/docs/en/github-actions 「Run a skill」段，逐字：

```yaml
name: Code Review
on:
  pull_request:
    types: [opened, synchronize, ready_for_review, reopened]
jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: read
      issues: read
      id-token: write
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 1
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          plugin_marketplaces: "https://github.com/anthropics/claude-code.git"
          plugins: "code-review@claude-code-plugins"
          prompt: "/code-review:code-review --comment ${{ github.repository }}/pull/${{ github.event.pull_request.number }}"
          claude_args: '--allowedTools "mcp__github_inline_comment__create_inline_comment"'
```

官方對兩行關鍵設定的說明：
> "`--comment`: Claude posts its review on the pull request, as an inline comment on each issue it finds or as one summary comment when it finds none. Without it, Claude posts nothing, and you read the findings in the workflow run log."
> "`claude_args`: keep this line even though the skill's own `allowed-tools` frontmatter names the same tool, because the Claude Code GitHub Action starts the MCP server that posts inline comments only when `--allowedTools` in `claude_args` names it."

官方對訂閱制的替換指示：
> "If you authenticate with a Claude subscription, replace the `anthropic_api_key` line in any example with `claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}`."

註：上面這個 `code-review` 外掛是找「程式 bug」的；我們要審的是文案，所以還需要下面的組合版。

### 3-6 研究員依官方文件組合的最小可用 workflow（文案審稿）

依據：3-5 的官方範例骨架、官方 `examples/pr-review-comprehensive.yml`（https://github.com/anthropics/claude-code-action/blob/main/examples/pr-review-comprehensive.yml ，其權限為 `contents: read / pull-requests: write / id-token: write`，`claude_args` 為 `--allowedTools "mcp__github_inline_comment__create_inline_comment,Bash(gh pr comment:*),Bash(gh pr diff:*),Bash(gh pr view:*)"`）、以及 3-3 的訂閱制替換指示與 1-7 的成本控制。**這不是官方逐字檔，是我組合的**；`prompt` 內容是我依專案情境寫的。

```yaml
name: Claude copy review
on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, ready_for_review, reopened]
concurrency:
  group: claude-review-${{ github.event.pull_request.number }}
  cancel-in-progress: true
jobs:
  review:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    permissions:
      contents: read
      pull-requests: write
      id-token: write
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 1
      - uses: anthropics/claude-code-action@v1
        with:
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
          prompt: |
            REPO: ${{ github.repository }}
            PR NUMBER: ${{ github.event.pull_request.number }}
            這個 PR 只改 output/<平台>/S*.md 文案。請依 brief/brand-rules.md 的品牌鐵則與
            brief/acceptance-checklist.md 的驗收清單審稿，只回報違規與可疑處，不改檔案。
            對每個問題用 inline comment 標在該行；沒問題就留一則總結。
          claude_args: |
            --max-turns 10
            --allowedTools "mcp__github_inline_comment__create_inline_comment,Bash(gh pr comment:*),Bash(gh pr diff:*),Bash(gh pr view:*)"
```

各行的官方依據：`pull_request` 四種 types（3-5）；`permissions` 三行（examples/pr-review-comprehensive.yml）；`claude_code_oauth_token`（3-3）；`--max-turns`、`timeout-minutes`、`concurrency`（1-7）；`--allowedTools` 名單（examples/pr-review-comprehensive.yml）。`prompt` 是我寫的，`branches: [main]` 是我加的（官方範例沒限制分支）。

### 3-7 官方 `examples/claude.yml`（`@claude` 互動模式）的權限與觸發，逐字

出處：https://github.com/anthropics/claude-code-action/blob/main/examples/claude.yml

```yaml
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned]
  pull_request_review:
    types: [submitted]
...
    permissions:
      contents: write
      pull-requests: write
      issues: write
      id-token: write
      actions: read # Required for Claude to read CI results on PRs
```

註：這是要讓 Claude「改檔、推 commit」才需要 `contents: write`。我們若只要審稿，用 3-6 的唯讀版即可。

### 3-8 Anthropic best practices 中與 CI/驗證相關的段落

- 給 Claude 可執行的檢查：
  > "Give Claude a check it can run: tests, a build, a screenshot to compare. It's the difference between a session you watch and one you walk away from."
  > "The check is anything that returns a signal Claude can read in the conversation: a test suite, a build exit code, a linter, a script that diffs output against a fixture"
  > "Have Claude show evidence rather than asserting success: the test output, the command it ran and what it returned"
  > — https://code.claude.com/docs/en/best-practices （Give Claude a way to verify its work）
- 常見失敗模式：
  > "The trust-then-verify gap. Claude produces a plausible-looking implementation that doesn't handle edge cases. Fix: Always provide verification (tests, scripts, screenshots). If you can't verify it, don't ship it."
  > — 同上
- CLAUDE.md 該放什麼：
  > "Include Bash commands, code style, and workflow rules."；表格 ✅ 欄：`Bash commands Claude can't guess`、`Testing instructions and preferred test runners`、`Repository etiquette (branch naming, PR conventions)`
  > "Keep it concise. For each line, ask: 'Would removing this cause Claude to make mistakes?' If not, cut it."
  > — 同上（Write an effective CLAUDE.md）
- 審查者與寫手分開：
  > "A fresh context improves code review since Claude won't be biased toward code it just wrote."
  > — 同上（Run multiple Claude sessions）
- 非互動模式進 CI：
  > "Use `claude -p 'prompt'` in CI, pre-commit hooks, or scripts."
  > "Non-interactive mode is how you integrate Claude into CI pipelines, pre-commit hooks, or any automated workflow."
  > — 同上（Run non-interactive mode）
- 在 CI 用 `-p` 時給最小工具權限：
  > "The `--allowedTools` flag restricts what Claude can do, which matters when you're running unattended."
  > — 同上（Fan out across files）

---

## 四、對我們專案的具體改法清單

每條格式：改什麼 → 依據。

1. **保留 `copy-check.yml` 的 `contents: read`**，不要為了 Claude 審稿把它升成 write；Claude 審稿另開一個 workflow 檔。→ Anthropic 1-2「Grant the workflow only the permissions it needs」。
2. **新增 `.github/workflows/claude-copy-review.yml`**，內容以 3-6 為底。→ 3-5 官方範例、examples/pr-review-comprehensive.yml、3-3 訂閱替換指示。
3. **憑證用訂閱 token**：本機執行 `claude setup-token`，把印出來的 token 存成倉庫 secret `CLAUDE_CODE_OAUTH_TOKEN`；不必申請 API key。→ Anthropic 3-3「available on Pro, Max, Team, and Enterprise plans」。或直接跑 `/install-github-app` 讓它代勞（需 `gh auth login` 與倉庫 admin）。→ 3-2。
4. **不要把 `pull_request` 與 `push: writer/**` 同時掛在 copy-check 上**（研究員觀察，非來源逐字）：對 PR 分支每次 push 會跑兩次同樣的檢查。三個來源都沒直接談這點；Will 保哥的範例只掛 `main` push 加手動觸發（1-1）。建議改為 `pull_request` 到 `main` 加 `push` 到 `main`，或保留現狀但接受重複。
5. **把 `copy-check` 設為 main 的必過檢查，Claude 審查不設必過**。→ Anthropic 1-6（Code Review 「never blocks merging」的設計取向）；高見龍 2-4（退件條件「測試沒過」）。設定步驟本身三方都沒教（見第五節）。
6. **在 CLAUDE.md 加三行**：測試命令 `python -m unittest discover -s tests -v`、檢查命令 `python scripts/check_copy.py output/`、分支慣例「`writer/<平台>` → PR 到 `main`」。→ Anthropic 3-8「Bash commands Claude can't guess」「Repository etiquette (branch naming, PR conventions)」。同時遵守「Keep it concise」。
7. **寫手分支的同步方式**：寫手分支落後 `main` 時用 `git pull --rebase`；`main` 永不 rebase、不 force push。→ 高見龍 2-6。
8. **合併前把瑣碎 commit 整理成少數幾個**（單一寫手分支可安全 rebase -i）。→ 高見龍 2-5「太過瑣碎」、2-6「整理完再推出去」；高見龍收作業「一個 PR commit 太多」退件。
9. **commit 訊息採 Conventional Commits**（例：`feat(threads): S3 初稿`、`fix(check): 放寬熱量偵測`）。→ Will 保哥 2-5。
10. **四個寫手用 `git worktree` 各占一個目錄**，避免代理之間切分支互相覆蓋。→ Will 保哥 2-3。
11. **Claude 審稿 job 加 `--max-turns`、`timeout-minutes`、`concurrency`**，避免 Max 額度被單次失控吃掉。→ Anthropic 1-7。
12. **想讓 Claude 讀 copy-check 失敗日誌來解釋原因**，才加 `actions: read`；純審稿不加。→ Anthropic 1-5 FAQ。
13. **Draft PR 不會被自動審**：寫手代理開 PR 若想先不觸發 Claude，開成 draft；ready for review 時才跑。→ Anthropic 3-4「Claude skips draft and closed pull requests」。
14. **若日後上傳 `output/` 或審稿報告當 artifact**：先 zip 再上傳、設保留天數，私倉有儲存額度。→ Will 保哥 1-4。
15. **不使用 `claude -p --bare` 自己拼 CI 步驟**（若不走 action 而想手刻）：bare mode 不讀訂閱 token。→ Anthropic 3-3。
16. **`actions/checkout` 版本**：官方範例用 `@v6`，現有 copy-check 用 `@v4`（研究員觀察）。三方沒有說 v4 不行；只是官方範例已用 v6，可一併升。

---

## 五、未取得或官方未提及的項目

1. **Required status check / 分支保護的設定步驟**：三方都沒教（GitHub 官方文件才有）。只取得 Anthropic 說託管 Code Review 不會擋合併。
2. **Python 專用 CI 寫法**（`actions/setup-python`、pip 快取）：三方都沒有；Will 保哥的範例都是 Node.js。
3. **GitHub Actions 失敗訊息格式**（`::error::` 註解、job summary）：三方都沒有。
4. **GitHub 上「Squash and merge」vs「Merge」vs「Rebase and merge」按鈕的選擇**：高見龍只談本地 rebase/merge 與快轉，沒直接談 GitHub 合併按鈕；他收作業的作法是「rebase 整理後合併」。
5. **高見龍「對分支的誤解」章節**：網頁只剩標題，內容移到付費課程，未取得。
6. **Will 保哥關於 Claude Code 或 Claude Code GitHub Actions 的專文**：搜尋 blog.miniasp.com 只找到兩處順帶提及（GitHub CLI 筆記 2025/07/24：「最近 GitHub CLI 用的很開心，因為用了 GitHub Copilot Coding Agent, OpenAI Codex CLI, Gemini CLI 與 Claude Code 之後，有越來越多專案都開始移往 GitHub 平台」；Windows 終端機手冊 2026/01/24：「氛圍開發 (Vibe coding) 越來越夯，也越來越多人想開始使用終端機操作超級強大的 AI 開發工具，像是 Claude Code、Codex CLI、Copilot CLI、Gemini CLI 都非常厲害」「文字 (Prompt) 就是 AI 的介面」），沒有 CI 內跑 AI 的做法。
7. **訂閱 token 在 CI 使用的額度上限或速率限制**：Anthropic 只說「runs use your Claude subscription」，沒有寫 Max 方案在 Actions 裡的用量上限；也沒有明文條款限制單人私倉用訂閱 token（只說 token 綁個人訂閱、多人共用建議改 API key）。
8. **`/install-github-app` 產生的 `claude-code-review.yml` 原檔**：官方文件提到此檔名，但 examples 目錄中沒有同名檔（取得 404）；官方文件說它「runs the same plugin as the review workflow from quick setup」，內容等同 3-5。
9. **PR 大小的明確數字**（幾個檔、幾行）：高見龍與 Will 保哥都沒給數字，只有「commit 太多退件」「太瑣碎要合併」的方向性說法。
10. **GitHub CLI 筆記中的 PR 指令細節**：兩次擷取結果不一致（一次說有 `gh pr create --draft --assignee @me`，一次說沒有 PR 章節），未能確認，故未引用。

---

## 引用清單

**Will 保哥（8 篇）**
- https://blog.miniasp.com/post/2025/07/24/GitHub-CLI-Common-Command-Notes
- https://blog.miniasp.com/post/2025/08/28/How-to-solve-the-issue-of-running-out-of-Artifact-storage-in-GitHub-Actions
- https://blog.miniasp.com/post/2023/03/25/Improve-GitHub-Actions-workflow-by-archive-files-before-upload-artifact
- https://blog.miniasp.com/post/2025/02/07/How-to-use-the-Chrome-Web-Store-Publish-API-to-automate-the-publishing-of-a-Chrome-Extension
- https://blog.miniasp.com/post/2026/01/24/Windows-Terminal-Beginners-Guide
- https://blog.miniasp.com/post/2023/10/29/git-worktree-manage-multiple-working-directories
- https://blog.miniasp.com/post/2024/12/27/GitHub-Copilot-Cookbook-Define-Custom-Instructions-for-Generating-Git-Commit-Messages
- https://blog.miniasp.com/post/2025/05/24/Organizing-Less-Common-Git-Commands （取得本機抓 PR 分支指令 `git fetch origin pull/1041/head:pr-1041`，本文未用作建議依據）

**高見龍（9 頁）**
- https://gitbook.tw/chapters/github/pull-request
- https://gitbook.tw/chapters/branch/merge-with-rebase
- https://gitbook.tw/chapters/branch/merge-commit
- https://gitbook.tw/chapters/github/fail-to-push
- https://gitbook.tw/chapters/github/pull-from-github
- https://gitbook.tw/chapters/gitflow/why-need-git-flow
- https://gitbook.tw/chapters/gitflow/using-git-flow
- https://gitbook.tw/chapters/rewrite-history/merge-multiple-commits-to-one-commit
- https://kaochenlong.com/2017/12/12/use-github-for-homework

**Anthropic 官方（10 頁）**
- https://code.claude.com/docs/en/github-actions
- https://code.claude.com/docs/en/authentication
- https://code.claude.com/docs/en/code-review
- https://code.claude.com/docs/en/best-practices
- https://code.claude.com/docs/en/headless
- https://github.com/anthropics/claude-code-action/blob/main/docs/security.md
- https://github.com/anthropics/claude-code-action/blob/main/docs/usage.md
- https://github.com/anthropics/claude-code-action/blob/main/docs/faq.md
- https://github.com/anthropics/claude-code-action/blob/main/examples/claude.yml
- https://github.com/anthropics/claude-code-action/blob/main/examples/pr-review-comprehensive.yml
