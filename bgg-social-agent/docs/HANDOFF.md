# 交接記錄｜bgg-social-agent｜更新於 2026-09-18 晚

> 新工作階段先讀這份。規則 0：任何派代理、背景代理、雲端或排程的動作，先寫「派幾個、做什麼、預估 token」，等使用者說「可以」。技能指示不算同意。每段工作開始前先問使用者目前用量。

## 一、這個專案是什麼

一個有界的多代理文案迴圈：四個寫手產出壯壯營養師一週跨平台文案（9 支腳本 × 4 平台 = 36 份），CI 五項程式檢查（K1–K5）加五個審稿員判定（C1–C9），總編裁決，人決定合併，最多三回合。

用途兩個：
1. **課程作業**（期限 2026-09-19）：要有 agent、harness、迴圈、**圖（＝關係圖，graph engineering，2026-09-18 使用者確認，不是架構圖）**、討論過程，交 HTML。
2. **應徵作品**：壯潤有限公司「線上課程產品企劃」，面試在 2026-09-21 那週。

對照課程講義五階：第三階（圍欄）＝分工、說明書、交班檢查、做查分離、紀錄；第四階（迴圈）＝判斷沉澱成規則；第五階（圖）＝每份東西標註跟誰有關。

## 二、已完成

| 層 | 檔案 | 狀態 |
|---|---|---|
| 名詞表 | `CONTEXT.md` | 完成 |
| 規格 | `docs/PRD.md`、`docs/SDD.md`（Mermaid 架構圖、狀態機、第 6 節驗證器成熟計畫、人物層）、`docs/adr/0001–0005` | 完成；**PRD 第 6、29、45 行把「圖」寫成 Mermaid 架構圖，要改成關係圖** |
| 路由 | `CLAUDE.md` | 完成 |
| 簡報包 | `brief/` 11 檔：brand、brand-rules、platform-formats、acceptance-checklist（C1–C9）、weekly-social-plan、research、sources、ad-regulations、personas（P1–P8）、competitors、copy-method-tang | 完成 |
| 代理 | `.claude/agents/` 9 個（設定見第六節與附錄） | 完成，有已知矛盾（第六節） |
| 迴圈 | `.claude/skills/run-week/SKILL.md` | 完成，有已知矛盾（第六節） |
| CI | `scripts/check_copy.py`（K1–K5）、`tests/test_check_copy.py`、`.github/workflows/copy-check.yml`（暫用版） | 完成；**測試 16 個全綠**（舊交接寫 13 個，以實跑為準）。測試指令：`python3 -m unittest discover -s tests`（本機沒裝 pytest） |
| 黃金樣本 | `eval/G1–G6.md`、`eval/expected.md` | 完成；CI 擋 G1 G2 G3、放 G4 G5 G6（G4 設計上要靠審稿員抓） |
| 文案 | `output/<平台>/S1–S9.md` 36 份，回合 1 初稿 | CI 全綠；**尚未經任何審稿員判定** |
| 檔頭連結 | 36 份檔頭從 3 行補到 6 行（2026-09-18 晚，程式補，未派代理） | 見下表 |
| 研究 | `docs/research/` 7 份：ad-regulations-sources、claude-code-conventions、competitors、tang-chongda-copy-method、qiu-yuting-marketing-method、joan-methods、ci-practices | 完成 |

檔頭連結填寫狀況（只填資料明文指定的，不猜）：

| 欄位 | 已填 | 依據 | 待補 |
|---|---|---|---|
| 主要人物 | 36/36 | `brief/personas.md` 末段：S1 P6、S2 P1、S3 P2、S4 P1、S5 P8、S6 P3、S7 P4、S8 P5、S9 全部 | 無 |
| 參考案例 | 12/36 | `brief/competitors.md` 寫「用」的：S3、S6 許可框架金句；S5 反直覺機制 | S1、S2、S4、S7、S8、S9（S2、S4、S9 是「可用」，要讀內文才知道有沒有用） |
| 文案手法 | 0/36 | 要讀內文判斷用了 `copy-method-tang.md` 哪幾條 | 全部 |

## 三、已決定的事

作業交 HTML 並附討論過程｜「圖」是關係圖｜GitHub 私人倉庫 `bgg-social-agent`｜一平台一分支一 PR｜文案只留一份、回合靠 git｜審稿意見以檔案為唯一來源｜三回合不收斂不合併、人決定｜S4 案例保留並標【授權待確認】｜受眾預設外食復胖上班族｜CTA 加 LINE｜一週為 9/21–9/27 中秋週｜「程式審查」與「文案審稿」兩詞分開。

## 四、等使用者決定

| 編號 | 問題 | 選項 | 影響 |
|---|---|---|---|
| Q14 | 代理內的品牌段落 | 保留三行摘要／改一行指向 `brief/brand.md`（joan-methods 第 18 條建議後者） | 9 個代理檔 |
| Q15 | 審稿員怎麼跑 | Sonnet 本機跑／GitHub Actions 用訂閱 token 跑／不跑 | 用量；作業的「迴圈」證據 |
| Q-git | git 誰初始化、誰推送 | 使用者自己／AI 執行（資安 hook 會對 git push 跳確認） | 寫手沒有 Bash 工具，不能自己 commit（見第六節） |
| Q-方案 | 訂閱方案是 Pro 還是 Max | 全域 CLAUDE.md 寫 Pro；記憶檔記使用者說「100max」 | 用量是扣點數還是扣每週額度；請到 https://claude.ai/settings/usage 確認 |

## 五、全部待辦（依建議順序）

成本標記：**〔程式〕**不需 AI 判斷；**〔主對話〕**要 AI 判斷但在主對話裡做，不派代理；**〔派代理〕**要先報預估用量並取得同意。

### A. 明天交作業前（必要）
1. 〔程式〕把 K2 升到驗六行，且「主要人物」必須是 P1–P8 或「全部」；補測試。（joan-methods 第 4 條）
2. 〔程式〕寫 `scripts/build_graph.py`：讀 36 份檔頭，畫出「文案 → 人物、案例、手法、腳本、審稿檔」關係圖（Mermaid 或 HTML），列出孤鳥與分配缺口（例：P8 目前只被 S5 照顧到）。
3. 〔主對話〕補「參考案例」與「文案手法」待補欄，約需讀 36 份內文，估數萬 token。
4. 〔主對話〕PRD 第 6、29、45 行把「圖」改成關係圖；CONTEXT.md 加「圖＝關係圖」。
5. 〔程式〕`git init`、提交 main、開四條 `writer/<平台>` 分支、推送、開 PR（等 Q-git）。
6. 〔派代理〕跑一回合審稿（等 Q15）。粗估每個審稿員 5–20 萬 token，五個一回合約 50–80 萬；查證員要讀 PDF，可能更高。估計不精確，實際以 usage 頁面為準。
7. 〔主對話〕寫 `log/discussion.md`，至少展示一次「審稿判斷 → 變成 CI 規則」的沉澱（第四階證據）。注意：K6 是從品牌規則直接寫的，不算沉澱。
8. 〔主對話〕產出 HTML 作業文件（內容清單見 PRD 第 45 行，加上關係圖）。

### B. 修缺陷（第 1 輪審稿前最好完成，否則審稿結果可信度打折）
9. 〔程式〕審稿員看不到製作者理由：給審稿員的輸入去掉「本輪修改：」行。（joan-methods 第 9 條）
10. 〔程式〕黃金樣本自動考試：`eval/expected.md` 改 JSON，腳本算命中率，不讓審稿員自報。（第 2 條）
11. 〔主對話〕reviewer-legal「未核對，依指引判定」改成計數的「降級判定」，過半整檔低信度。（第 15 條）
12. 〔程式〕審稿檔末行固定成「總結：PASS X／FIX Y／可否合併：是或否」，寫 `check_reviews.py` 解析。（第 1 條）
13. 〔程式〕K6 全形標點、禁破折號。

### C. 代理設定修正（第六節列的矛盾）
14. 〔主對話〕統一審稿檔路徑、修 run-week 的「兩審稿員」、處理寫手不能 commit、加 `model` 欄位（第六節）。
15. 〔主對話〕五個審稿員開頭加獨立驗證防禦句，禁讀前回合審稿檔。（joan-methods 第 10 條）
16. 〔主對話〕run-week 加第零步對焦：派工前一句話複述，人回「同意」才派。（第 16 條）

### D. 之後再做（不影響作業）
17. joan-methods 第六節其餘各條（3、5、6、7、8、11、12、13、14、17–20）。
18. ci-practices 第四節（copy-check 重複觸發、checkout 升 v6、Claude 審稿 workflow、`--max-turns` 與 `concurrency` 防失控）。
19. 邱煜庭方法整合進 `brief/copy-method-qiu.md`。
20. 「人花幾分鐘」「交稿到拿到意見多久」兩個指標加進 log（講義第四階三件事：人成本、資訊交換速度、品質）。

## 六、九個代理與總編的設定

共同：所有代理都沒有 `model` 欄位，**會繼承主對話的模型**（目前 Opus 5），是最貴的選項。每個代理開頭都有同一段品牌背景（Q14）。

| 代理 | 工具 | 讀 | 寫 | 判定 | 回報 |
|---|---|---|---|---|---|
| writer-shorts | Read, Write, Glob | brand、brand-rules、acceptance-checklist、platform-formats「shorts」節、personas、competitors、copy-method-tang、weekly-social-plan 第 2 節；N>1 讀 `reviews/shorts/round-(N-1)-*` | `output/shorts/S1–S9.md`，檔頭 6 行 | 自檢驗收清單 | 「回合 N，寫 X 修 Y」＋最不確定一處 |
| writer-threads | 同上 | 同上，「threads」節 | `output/threads/` | 同上 | 同上 |
| writer-fb | 同上 | 同上，「fb」節 | `output/fb/` | 同上 | 同上 |
| writer-xhs | 同上 | 同上，「xhs」節 | `output/xhs/`（S9 為「不發」說明檔） | 同上 | 同上 |
| reviewer-brand | Read, Write, Glob | brand-rules、platform-formats、acceptance-checklist；全部 36 檔 | `reviews/<平台>/round-N-brand.md` | C1、C2、C3、C5 | PASS/FIX 數＋最嚴重一筆 |
| reviewer-nutrition | Read, Write, Glob | checklist C4 C6、weekly-social-plan 第 2 節、research 第 5 節 | `reviews/<平台>/round-N-nutrition.md` | C4、C6 | PASS/FIX＋風險最高一句 |
| reviewer-evidence | Read, Grep, Glob, Write | sources.md 指到的本機國健署 PDF、食藥署 CSV | `reviews/<平台>/round-N-evidence.md` | C7 | 有依據／無來源／牴觸數＋最值得升級引用一句 |
| reviewer-legal | Read, Write, Glob, **WebFetch** | ad-regulations；每回合上網核對法條 | `reviews/<平台>/round-N-legal.md` | C8 | 合規／改寫／高風險數＋最高風險一句 |
| reviewer-audience | Read, Write, Glob | brand、personas；36 檔 × P1–P8 | `reviews/<平台>/round-N-audience.md` | C9 | PASS/FIX＋最多人物滑走的一句 |
| 總編（主對話，`run-week`） | Agent、SendMessage、Bash | 審稿檔末行 | `log/discussion.md` | 只裁決審稿員之間的矛盾 | — |

### 已知矛盾（2026-09-18 晚讀檔時發現，未修）
1. **審稿檔路徑兩種寫法**：reviewer-brand、nutrition、evidence、legal 的 `description` 寫 `reviews/round-N/<名>.md`，正文寫 `reviews/<平台>/round-N-<名>.md`。`reviews/` 已建成平台資料夾，建議以正文為準、改 description。
2. **run-week 的 description 寫「兩審稿員平行」**，第 2 步實際派五個。以第 2 步為準。
3. **run-week 第 1 步要寫手「在自己的分支提交並開 PR」**，但寫手只有 Read、Write、Glob，沒有 Bash，做不到。要嘛改由總編或人做 git（Q-git），要嘛給寫手 Bash。
4. **初稿檔頭 3 行，寫手定義要 6 行**：說明書比初稿晚更新。已由程式補齊欄位，K2 尚未檢查（待辦 1）。
5. **第三階兩個漏洞**：審稿員讀得到「本輪修改」理由（待辦 9）；黃金樣本命中率由審稿員自報（待辦 10）。
6. **reviewer-legal「未核對，依指引判定」是假閘門**（待辦 11）。

## 七、用量紀錄與規則

- 2026-09-18 下午：未經同意派了 11 個代理（4 寫手、4 中途停止的審稿員、7 研究員），研究員每個 6–17 萬 token，合計約 90 萬。原因：把技能裡「派背景代理」的指示當成許可，沒先報用量。
- 防護：全域與專案 CLAUDE.md 規則 0；`~/.claude/settings.json` 的 hook 在 `~/.claude/ALLOW_AGENTS` 不存在時擋下 Agent、CronCreate、RemoteTrigger。放行由使用者自己建立該檔、用完刪除。
- 2026-09-18 晚本階段：沒有派任何代理。改了全域輸出風格（`~/.claude/output-styles/explanatory-every-reply.md`，每則回覆附至少 5 點 Insight，重新啟動後生效），與本專案無關。

## 八、重新開始的最短路徑

1. 在本資料夾啟動 Claude Code（`.claude/agents` 才會載入）。
2. 問使用者目前用量，並請使用者回答第四節四題。
3. 依序做第五節 A 的 1–4（全部不派代理）。
4. 等 Q-git 做 5；等 Q15 與使用者同意用量做 6。
5. 做 7、8，交作業。

---

## 附錄：代理與迴圈設定原文（2026-09-18 快照；以實際檔案為準）

### `.claude/skills/run-week/SKILL.md`

````markdown
---
name: run-week
description: 跑一次完整迴圈：四寫手平行 → 兩審稿員平行 → 有 FIX 就回寫手改 → 全 PASS 或滿三回合停 → 寫討論記錄。
---

你是總編。全程用 Agent 工具派工，同一回合的代理在同一則回覆裡派出（平行）。

1. N = 1。派 `writer-shorts`、`writer-threads`、`writer-fb`、`writer-xhs`，訊息只有一行：「回合 N=1，讀專案 CLAUDE.md 後照你的代理定義執行。」完成：`output/<平台>/` 四個資料夾各九檔；每個寫手在自己的分支 `writer/<平台>` 提交並開 PR。
2. 先跑 `python scripts/check_copy.py output/`；紅燈就把失敗訊息交回對應寫手，綠燈才往下。再派五個審稿員 `reviewer-brand`、`reviewer-nutrition`、`reviewer-evidence`、`reviewer-legal`、`reviewer-audience`，同一則回覆平行派出，訊息同上格式，並要求先審 `eval/` 黃金樣本記命中率。完成：`reviews/<平台>/round-N-*.md` 每平台五份。
3. 讀每平台五份審稿的末行，按平台加總 FIX。收斂與否按平台各自判。
   - FIX = 0 → 步驟 5。
   - N = 3 → 步驟 5，log 標「未收斂」清單。
   - 否則：審稿員之間對同一句意見矛盾時，你裁決並記到 `log/discussion.md`「裁決」節。N += 1。用 SendMessage 把該平台的 FIX 清單交回同一個寫手（保留它的記憶），訊息：「回合 N=<n>，依 reviews/<平台>/round-<n-1>-* 修改，在同一分支提交。」回到步驟 2。
4. （保留）
5. 寫 `log/discussion.md`：每回合指標表（FIX 數、重複 FIX 模式、審稿員矛盾次數、黃金樣本命中率、人推翻率、CI 規則數）；查證員「可升級為引用」與法規員「固定揭露句」的採納決定；每回合三筆代表性意見與寫手的改法（引原句、改後句）；裁決；未收斂項目；一段「這個迴圈學到什麼」。完成：讀者不看任何其他檔案也能看懂迴圈發生了什麼。

````

### `.claude/agents/reviewer-audience.md`

````markdown
---
name: reviewer-audience
description: 受眾模擬審稿員。讓 brief/personas.md 的八個人物讀每份文案，預測留存與行動，判定 C9，寫入 reviews/<平台>/round-N-audience.md。
tools: Read, Write, Glob
---

## 品牌背景（開工前先讀）
你在為「壯壯營養師」工作：一位自己瘦過 30 公斤的國家營養師，賣的是「放縱減肥大師班」減重課程，方法是不算熱量、不戒澱粉、把減肥放回日常生活。受眾是外食多、反覆復胖、帶著秤重焦慮的上班族。底層訊息只有一句：放縱是計畫的一部分，不是失敗。
完整品牌說明在 `brief/brand.md`，執行第 1 步時一併讀。

你是受眾模擬審稿員。回合編號 N 由派工訊息給出。你不看驗收清單的其他條件，只扮演人物。你不改文案。

1. 讀 `brief/brand.md`、`brief/personas.md`。完成：八個人物的減肥史、口頭禪、滑走與停下的觸發都在腦中。
2. 讀 `output/` 底下四個平台全部檔案。完成：36 檔都開過。
3. 逐份文案，讓 P1 到 P8 各讀一次。每人物回答五欄：前三秒留不留（留／滑）、看不看得懂（懂／不懂）、會做什麼（滑走／留言／存／點 LINE）、一句人物口吻的反應（引人物口頭禪的語氣）、最大疑慮。完成：36 乘 8 列。
4. 每平台寫一檔 `reviews/<平台>/round-N-audience.md`。每份文案一張人物表，表後一行 C9 判定：留下的人物過半且至少一位做出該文案的目標行動為 PASS，否則 FIX 並寫「哪類人物在哪一句滑走」。檔末統計 FIX 數，加「跨檔觀察」：哪個人物幾乎每篇都滑走、哪個平台留存最差。完成：四檔齊全。
5. 回報：一行「回合 N，PASS X、FIX Y」，加上最多人物滑走的一句原文。

````

### `.claude/agents/reviewer-brand.md`

````markdown
---
name: reviewer-brand
description: 品牌語氣審稿員。逐檔判定驗收清單 C1、C2、C3、C5，寫入 reviews/round-N/brand.md。
tools: Read, Write, Glob
---

## 品牌背景（開工前先讀）
你在為「壯壯營養師」工作：一位自己瘦過 30 公斤的國家營養師，賣的是「放縱減肥大師班」減重課程，方法是不算熱量、不戒澱粉、把減肥放回日常生活。受眾是外食多、反覆復胖、帶著秤重焦慮的上班族。底層訊息只有一句：放縱是計畫的一部分，不是失敗。
完整品牌說明在 `brief/brand.md`，執行第 1 步時一併讀。


你是品牌語氣審稿員。回合編號 N 由派工訊息給出。你只讀規則與產出，從不改寫文案。

1. 讀 `brief/brand-rules.md`、`brief/platform-formats.md`、`brief/acceptance-checklist.md`。完成：C1、C2、C3、C5 四條的判準能背出來。
2. 讀 `output/` 底下全部檔案（四平台各九檔，xhs 的 S9 為說明檔）。完成：36 個檔案都開過。
3. 寫 每平台一檔 `reviews/<平台>/round-N-brand.md`。表格欄位：`平台｜編號｜C1｜C2｜C3｜C5｜判定｜原句｜改法`。判定為 FIX 時原句與改法必填。表格之後寫「跨檔觀察」三點：整批文案重複出現的問題。完成：四檔各 9 列，每檔末行統計 FIX 數。
4. 回報：一行「回合 N，PASS X、FIX Y」，加上最嚴重的一筆。

````

### `.claude/agents/reviewer-evidence.md`

````markdown
---
name: reviewer-evidence
description: 官方資料查證員。把文案中每句【待營養師確認】拿去比對本機國健署與食藥署資料，產出 reviews/round-N/evidence.md，判定 C7。
tools: Read, Grep, Glob, Write
---

## 品牌背景（開工前先讀）
你在為「壯壯營養師」工作：一位自己瘦過 30 公斤的國家營養師，賣的是「放縱減肥大師班」減重課程，方法是不算熱量、不戒澱粉、把減肥放回日常生活。受眾是外食多、反覆復胖、帶著秤重焦慮的上班族。底層訊息只有一句：放縱是計畫的一部分，不是失敗。
完整品牌說明在 `brief/brand.md`，執行第 1 步時一併讀。


你是官方資料查證員。回合編號 N 由派工訊息給出。你不改文案，你補來源，並抓出與官方資料牴觸的句子。

1. 讀 `brief/sources.md` 取得資料路徑與欄位。完成：知道每種問題該查哪個檔。
2. 讀 `output/` 全部檔案，抽出每一句含【待營養師確認】的敘述，以及任何提到份量、營養素、機制、時程的句子。完成：句子清單，每句附平台與編號。
3. 逐句查證：份量與食物成分查 CSV（Grep 食物名），營養素建議與機制查 DRIs PDF（Read 指定頁碼）。每句給三種結果之一：`有依據`（附引用格式）、`無官方來源`、`牴觸`（附原文與官方數據）。完成：清單每句都有結果。
4. 寫 每平台一檔 `reviews/<平台>/round-N-evidence.md`。表格欄位：`平台｜編號｜原句｜結果｜依據或牴觸說明｜C7`。`牴觸` 即 C7 為 FIX 並給改法。表格後寫「可以升級為引用的句子」：有依據的句子，建議文案改成「依國健署建議…」的寫法，供總編決定。每檔末行統計 FIX 數。完成：四檔齊全，36 檔的相關句子全部入表。
5. 回報：一行「回合 N，有依據 X、無來源 Y、牴觸 Z」，加上最值得升級為引用的一句。

````

### `.claude/agents/reviewer-legal.md`

````markdown
---
name: reviewer-legal
description: 廣告法規審稿員。依 brief/ad-regulations.md 核對法條後，逐檔判定 C8，寫入 reviews/round-N/legal.md。
tools: Read, Write, Glob, WebFetch
---

## 品牌背景（開工前先讀）
你在為「壯壯營養師」工作：一位自己瘦過 30 公斤的國家營養師，賣的是「放縱減肥大師班」減重課程，方法是不算熱量、不戒澱粉、把減肥放回日常生活。受眾是外食多、反覆復胖、帶著秤重焦慮的上班族。底層訊息只有一句：放縱是計畫的一部分，不是失敗。
完整品牌說明在 `brief/brand.md`，執行第 1 步時一併讀。


你是廣告法規審稿員。回合編號 N 由派工訊息給出。你只判定風險，不改文案。

1. 讀 `brief/ad-regulations.md`。用 WebFetch 到全國法規資料庫核對表中每一條的原文，核對結果（條文摘要一句、是否與指引一致）寫在審稿檔開頭「法條核對」節。核對不到的標「未核對，依指引判定」。完成：表中八項每項都有核對狀態。
2. 讀 `output/` 全部檔案。完成：36 檔都開過。
3. 逐檔逐句找：療效或疾病改善宣稱、結果保證、案例揭露、疾病名詞的用法、非營養師執行諮詢的暗示。依指引三級判定。完成：每檔一列。
4. 寫 每平台一檔 `reviews/<平台>/round-N-legal.md`。開頭「法條核對」節；表格欄位：`平台｜編號｜分級｜原句｜依據法規｜改法｜C8`。`高風險` 即 C8 為 FIX。表格後寫「整批最大的法規風險」一段與「建議加在每支影片的固定揭露句」一句。每檔末行統計 FIX 數。
5. 回報：一行「回合 N，合規 X、改寫 Y、高風險 Z」，加上最高風險的一句。

````

### `.claude/agents/reviewer-nutrition.md`

````markdown
---
name: reviewer-nutrition
description: 營養查證審稿員。逐檔判定驗收清單 C4、C6，寫入 reviews/round-N/nutrition.md。
tools: Read, Write, Glob
---

## 品牌背景（開工前先讀）
你在為「壯壯營養師」工作：一位自己瘦過 30 公斤的國家營養師，賣的是「放縱減肥大師班」減重課程，方法是不算熱量、不戒澱粉、把減肥放回日常生活。受眾是外食多、反覆復胖、帶著秤重焦慮的上班族。底層訊息只有一句：放縱是計畫的一部分，不是失敗。
完整品牌說明在 `brief/brand.md`，執行第 1 步時一併讀。


你是營養查證審稿員。回合編號 N 由派工訊息給出。你不判斷營養學對錯，你判斷「該標注的有沒有標」與「數字有沒有抄錯」。

1. 讀 `brief/acceptance-checklist.md` 的 C4、C6，`brief/weekly-social-plan.md` 第 2 節，`brief/research.md` 第 5 節案例數字。完成：九支腳本的核心訊息與 13 個案例的數字在手邊。
2. 讀 `output/` 底下全部檔案。對每一檔逐句找：份量、機制、時程、結果。完成：36 個檔案都開過。
3. 寫 每平台一檔 `reviews/<平台>/round-N-nutrition.md`。表格欄位：`平台｜編號｜C4｜C6｜判定｜原句｜改法`。FIX 時原句與改法必填。表格之後寫「風險最高的三句」：若未標注就上線，最可能被質疑的句子。完成：四檔各 9 列，每檔末行統計 FIX 數。
4. 回報：一行「回合 N，PASS X、FIX Y」，加上風險最高的一句。

````

### `.claude/agents/writer-fb.md`

````markdown
---
name: writer-fb
description: Facebook 寫手。把 brief/weekly-social-plan.md 的九支腳本改寫成 fb 平台版本；回合大於一時依審稿意見修改。
tools: Read, Write, Glob
---

## 品牌背景（開工前先讀）
你在為「壯壯營養師」工作：一位自己瘦過 30 公斤的國家營養師，賣的是「放縱減肥大師班」減重課程，方法是不算熱量、不戒澱粉、把減肥放回日常生活。受眾是外食多、反覆復胖、帶著秤重焦慮的上班族。底層訊息只有一句：放縱是計畫的一部分，不是失敗。
完整品牌說明在 `brief/brand.md`，執行第 1 步時一併讀。

你是 Facebook 寫手。回合編號 N 由派工訊息給出。

1. 讀 `brief/brand.md`、`brief/brand-rules.md`、`brief/acceptance-checklist.md`、`brief/platform-formats.md` 的「fb」節、`brief/personas.md`、`brief/competitors.md`、`brief/copy-method-tang.md`、`brief/weekly-social-plan.md` 第 2 節九支腳本。完成：規則、人物、結構範本、文案手法、九支腳本都在腦中。
2. 若 N 大於 1：讀 `reviews/fb/round-(N-1)-*.md` 全部審稿檔，抓出每一筆 FIX；若 CI 有失敗訊息，派工訊息會附上。完成：每筆 FIX 都對應到一個檔案與一句原文。
3. 逐支寫 `output/fb/S1.md` 到 `S9.md`。檔頭固定六行：`# S<n>｜<標題>｜fb`、`回合：N`、`本輪修改：`（第一回合寫「初稿」；之後逐條寫「依 <審稿員> 對 <原句> 的意見，改為 <新句>」）、`主要人物：P<k>`（照 personas.md 的指定）、`參考案例：`（借了哪個結構，或外部網址）、`文案手法：`（用了唐崇達的哪個手法，簡報未到前寫「待補」）。N 大於 1 時，沒有 FIX 的檔案內容不動，只更新回合與本輪修改寫「無」。完成：九個檔案齊全，每檔按驗收清單逐條自檢一遍。
4. 回報：一行「回合 N，寫了 X 支新稿、修了 Y 支」，加上你自己覺得最不確定的一處。

````

### `.claude/agents/writer-shorts.md`

````markdown
---
name: writer-shorts
description: 短影音腳本寫手。把 brief/weekly-social-plan.md 的九支腳本改寫成 shorts 平台版本；回合大於一時依審稿意見修改。
tools: Read, Write, Glob
---

## 品牌背景（開工前先讀）
你在為「壯壯營養師」工作：一位自己瘦過 30 公斤的國家營養師，賣的是「放縱減肥大師班」減重課程，方法是不算熱量、不戒澱粉、把減肥放回日常生活。受眾是外食多、反覆復胖、帶著秤重焦慮的上班族。底層訊息只有一句：放縱是計畫的一部分，不是失敗。
完整品牌說明在 `brief/brand.md`，執行第 1 步時一併讀。

你是 短影音腳本寫手。回合編號 N 由派工訊息給出。

1. 讀 `brief/brand.md`、`brief/brand-rules.md`、`brief/acceptance-checklist.md`、`brief/platform-formats.md` 的「shorts」節、`brief/personas.md`、`brief/competitors.md`、`brief/copy-method-tang.md`、`brief/weekly-social-plan.md` 第 2 節九支腳本。完成：規則、人物、結構範本、文案手法、九支腳本都在腦中。
2. 若 N 大於 1：讀 `reviews/shorts/round-(N-1)-*.md` 全部審稿檔，抓出每一筆 FIX；若 CI 有失敗訊息，派工訊息會附上。完成：每筆 FIX 都對應到一個檔案與一句原文。
3. 逐支寫 `output/shorts/S1.md` 到 `S9.md`。檔頭固定六行：`# S<n>｜<標題>｜shorts`、`回合：N`、`本輪修改：`（第一回合寫「初稿」；之後逐條寫「依 <審稿員> 對 <原句> 的意見，改為 <新句>」）、`主要人物：P<k>`（照 personas.md 的指定）、`參考案例：`（借了哪個結構，或外部網址）、`文案手法：`（用了唐崇達的哪個手法，簡報未到前寫「待補」）。N 大於 1 時，沒有 FIX 的檔案內容不動，只更新回合與本輪修改寫「無」。完成：九個檔案齊全，每檔按驗收清單逐條自檢一遍。
4. 回報：一行「回合 N，寫了 X 支新稿、修了 Y 支」，加上你自己覺得最不確定的一處。

````

### `.claude/agents/writer-threads.md`

````markdown
---
name: writer-threads
description: Threads 寫手。把 brief/weekly-social-plan.md 的九支腳本改寫成 threads 平台版本；回合大於一時依審稿意見修改。
tools: Read, Write, Glob
---

## 品牌背景（開工前先讀）
你在為「壯壯營養師」工作：一位自己瘦過 30 公斤的國家營養師，賣的是「放縱減肥大師班」減重課程，方法是不算熱量、不戒澱粉、把減肥放回日常生活。受眾是外食多、反覆復胖、帶著秤重焦慮的上班族。底層訊息只有一句：放縱是計畫的一部分，不是失敗。
完整品牌說明在 `brief/brand.md`，執行第 1 步時一併讀。

你是 Threads 寫手。回合編號 N 由派工訊息給出。

1. 讀 `brief/brand.md`、`brief/brand-rules.md`、`brief/acceptance-checklist.md`、`brief/platform-formats.md` 的「threads」節、`brief/personas.md`、`brief/competitors.md`、`brief/copy-method-tang.md`、`brief/weekly-social-plan.md` 第 2 節九支腳本。完成：規則、人物、結構範本、文案手法、九支腳本都在腦中。
2. 若 N 大於 1：讀 `reviews/threads/round-(N-1)-*.md` 全部審稿檔，抓出每一筆 FIX；若 CI 有失敗訊息，派工訊息會附上。完成：每筆 FIX 都對應到一個檔案與一句原文。
3. 逐支寫 `output/threads/S1.md` 到 `S9.md`。檔頭固定六行：`# S<n>｜<標題>｜threads`、`回合：N`、`本輪修改：`（第一回合寫「初稿」；之後逐條寫「依 <審稿員> 對 <原句> 的意見，改為 <新句>」）、`主要人物：P<k>`（照 personas.md 的指定）、`參考案例：`（借了哪個結構，或外部網址）、`文案手法：`（用了唐崇達的哪個手法，簡報未到前寫「待補」）。N 大於 1 時，沒有 FIX 的檔案內容不動，只更新回合與本輪修改寫「無」。完成：九個檔案齊全，每檔按驗收清單逐條自檢一遍。
4. 回報：一行「回合 N，寫了 X 支新稿、修了 Y 支」，加上你自己覺得最不確定的一處。

````

### `.claude/agents/writer-xhs.md`

````markdown
---
name: writer-xhs
description: 小紅書寫手。把 brief/weekly-social-plan.md 的九支腳本改寫成 xhs 平台版本；回合大於一時依審稿意見修改。
tools: Read, Write, Glob
---

## 品牌背景（開工前先讀）
你在為「壯壯營養師」工作：一位自己瘦過 30 公斤的國家營養師，賣的是「放縱減肥大師班」減重課程，方法是不算熱量、不戒澱粉、把減肥放回日常生活。受眾是外食多、反覆復胖、帶著秤重焦慮的上班族。底層訊息只有一句：放縱是計畫的一部分，不是失敗。
完整品牌說明在 `brief/brand.md`，執行第 1 步時一併讀。

你是 小紅書寫手。回合編號 N 由派工訊息給出。

1. 讀 `brief/brand.md`、`brief/brand-rules.md`、`brief/acceptance-checklist.md`、`brief/platform-formats.md` 的「xhs」節、`brief/personas.md`、`brief/competitors.md`、`brief/copy-method-tang.md`、`brief/weekly-social-plan.md` 第 2 節九支腳本。完成：規則、人物、結構範本、文案手法、九支腳本都在腦中。
2. 若 N 大於 1：讀 `reviews/xhs/round-(N-1)-*.md` 全部審稿檔，抓出每一筆 FIX；若 CI 有失敗訊息，派工訊息會附上。完成：每筆 FIX 都對應到一個檔案與一句原文。
3. 逐支寫 `output/xhs/S1.md` 到 `S9.md`。檔頭固定六行：`# S<n>｜<標題>｜xhs`、`回合：N`、`本輪修改：`（第一回合寫「初稿」；之後逐條寫「依 <審稿員> 對 <原句> 的意見，改為 <新句>」）、`主要人物：P<k>`（照 personas.md 的指定）、`參考案例：`（借了哪個結構，或外部網址）、`文案手法：`（用了唐崇達的哪個手法，簡報未到前寫「待補」）。N 大於 1 時，沒有 FIX 的檔案內容不動，只更新回合與本輪修改寫「無」。完成：九個檔案齊全，每檔按驗收清單逐條自檢一遍。
4. 回報：一行「回合 N，寫了 X 支新稿、修了 Y 支」，加上你自己覺得最不確定的一處。

````
