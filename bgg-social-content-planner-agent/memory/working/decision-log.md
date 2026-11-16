# Decision Log

格式：

## YYYY-MM-DD｜Task ID
- Decision:
- Why:
- Evidence:
- Alternatives rejected:
- Memory impact: none / learning / project / core-proposal
- Conflict / blocker:

## 2026-09-18｜memory-audit-2026-09-18
- Decision: 只做格式修正三項：00_INDEX 補列 5 檔；claim-ledger METRIC-001 拆成 001–004；MEMORY-DESIGN 的 active-script.md 改為實際存在的 current-brief.md。
- Why: 01-voice.md 未被索引，語氣規則可能沒被讀到；ledger 自訂「一列一個主張」；文件指向不存在的檔案。
- Evidence: reviews/memory-audit-2026-09-18.md
- Alternatives rejected: 直接改 CLAUDE.md 與 BRAND 狀態——屬語意變更，依 audit-memory skill 只提議不自改。
- Memory impact: project（僅格式，狀態值未變）
- Conflict / blocker: 見下條

## 2026-09-18｜CONFLICT performance.csv
- Decision: 未擇一，保留兩份。
- Why: data/performance.csv 與 memory/learning/performance.csv 欄位不同（topic/format/avg_watch_pct/profile_actions vs content_pillar/persona/impressions/completion_rate/clicks）。
- Evidence: 兩檔表頭
- Alternatives rejected: 自行合併——需使用者決定哪份是正式 schema。
- Memory impact: none
- Conflict / blocker: CONFLICT，待使用者決定

## 2026-09-18｜JD 與資料源接入
- Decision: (1) 職缺原文逐字存 references/jd-2026-09-18.md；(2) BRAND-001/002 由 USER_CONFIRMED 改 IMPORTED，00-brand-core 註明未經品牌方確認（audit C1，使用者同意）；(3) 本機營養資料庫登記進 source-registry，本機路徑放 references/local-sources.md；(4) 新增 demand-path 方法、模板，接進 research-radar；(5) 新增 content-calendar，接進 plan-9-videos；(6) JD-MAPPING 補 4 列與「JD 六問」對照。
- Why: (1) JD 原文是 mapping 唯一依據；(2) 應徵者整理的公開資料不等於品牌確認；(3) SDD 說 local path 可寫在 source-registry，但 check_memory.py 禁止 memory/ 內出現本機路徑——兩者衝突，採有測試執行的那條，路徑移到 references/；(4) 使用者提供的選題方法；(5) JD 三明列「建立及維護社群內容行事曆」，專案原本沒有。
- Evidence: references/jd-2026-09-18.md、reviews/memory-audit-2026-09-18.md
- Alternatives rejected: 直接展開 125 題主題池——與 plan-campaign「不一次生成」原則衝突，改成 3–5 × 3–5。
- Memory impact: project＋core（僅 brand-core 來源註記，原則內容未改）
- Conflict / blocker: SDD Portability 段與 check_memory.py 的衝突，SDD 待改文字

## 2026-09-18｜CLAUDE.md 路由修正（audit C2–C4）
- Decision: 載入 core/01-voice.md；Agents 段改成兩流程對照表（不刪任何 agent）；加入「派 subagent 前須使用者同意，否則主對話扮演該角色」；主要指令補 /write-copy、/plan-campaign、/learn-results，並指向 JD 原文、demand-path、local-sources。
- Why: 語氣規則原本未被載入；11 個 agent 只列 8 個；使用者全域規則 0 禁止未經同意派 agent。
- Evidence: reviews/memory-audit-2026-09-18.md C2–C4
- Alternatives rejected: 刪除 v1 agents——會移除 /write-copy 功能。
- Memory impact: none（路由檔）
- Conflict / blocker: 無

## 2026-09-18｜加入 Landing Page／AISEO 方法
- Decision: 原文逐字存 references/landing-page-aiseo-method.md；copy-methods 新增第 7 條 SPIN／FABE；source-registry 登記 METHOD-AISEO-LANDING。
- Why: 使用者要求加入；轉換型內容原本缺結構骨架。
- Evidence: 使用者貼文（作者未標示）
- Alternatives rejected: 把「AI 引用率」加進 KPI——JD 明列的是觀看、互動、收藏、分享、LINE；作者主張未驗證，只列為 HYPOTHESIS。GAVE 縮寫原文未定義，不自行補。
- Memory impact: project（方法庫）
- Conflict / blocker: 無

## 2026-09-18｜更正：Landing Page／AISEO 內容改為審查標準
- Decision: 使用者更正「是審查，不是個人觀點」。移除 HYPOTHESIS／作者觀點標記；landing-page-aiseo-method.md 改寫為 7 項審查清單；review-card、EVALUATION、copy-editor 加入這些檢查項。
- Why: 使用者指定為審稿標準。
- Evidence: 使用者 2026-09-18 指示
- Alternatives rejected: 前一條決策「只當方法參考、AI 引用列 HYPOTHESIS」——已被使用者更正，以本條為準。
- Memory impact: project（source-registry、copy-methods）
- Conflict / blocker: GAVE 縮寫定義未取得，審查暫依原文描述

## 2026-09-18｜補上 GAVE 定義
- Decision: GAVE（Grouping／Accentuation／Variation／Elongation）定義與範例寫入 landing-page-aiseo-method.md；審查清單與 review-card 的 GAVE 由 1 列拆成 G／A／V／E 4 列。
- Why: 使用者提供定義，解除前一條的 blocker。
- Evidence: 使用者 2026-09-18 提供
- Alternatives rejected: 同時用 GAVE 改寫所有 skills／agents prompt——超出本次要求，只記為可選項。
- Memory impact: none（references、templates）
- Conflict / blocker: 【】強調與內部標記【待營養師確認】的形式相同，已加註不得混用

## 2026-09-18｜research-radar（本機資料版）
- Decision: 依使用者指示只用本機資料庫、不上網。新增 scripts/extract_nutrition.py（本機抽取 HPA PDF 全文與 TFDA 子集到 data/nutrition/）；venv 安裝 pypdf；產出 radar 18 題（GO 10）；claim-ledger 新增 NUTRITION-002–005（VERIFIED）。
- Why: 使用者要求用免費、不耗用量的方式把資料放進專案；抽取由程式完成，AI 只讀摘要。
- Evidence: memory/working/research-radar.md、data/nutrition/
- Alternatives rejected: 讓 AI 直接讀 PDF——約 1,100 頁，耗用量大；把整個 405 MB 食藥署資料夾複製進專案——只需子集。
- Memory impact: project（claim-ledger 4 列）；working（current-week、radar）
- Conflict / blocker: 受眾語言、趨勢、參考案例無即時來源，全數標 IMPORTED／HYPOTHESIS；連假天數未查證

## 2026-09-18｜更正：品牌調查是當日一手資料
- Decision: 使用者指出品牌已調查過。BRAND-001/002、FOUNDER-001、METRIC-001–004、OFFER-001 由 IMPORTED 升為 VERIFIED（範圍註明「官網自述／公開主張」）；BGG-OFFICIAL、BGG-THREADS 改 VERIFIED；從 bgg-social-agent 複製 competitors.md、ad-regulations-sources.md 到 references/v1-seed/；radar 併入同業趨勢、參考案例、3 個差異化切入點，新增 R19。
- Why: research.md 抓取日期即 2026-09-18，來源為品牌官網與 Threads；先前把「v1」誤當「過時」。competitors.md、ad-regulations-sources.md 是 v2 遷移漏帶的檔案（audit U8）。
- Evidence: references/v1-seed/research.md、competitors.md
- Alternatives rejected: 升為 USER_CONFIRMED——那需要品牌方提供，公開頁面只能是 VERIFIED＋範圍。
- Memory impact: project（claim-ledger、source-registry）
- Conflict / blocker: 品牌 2026-09-17 菜單貼文含大卡數，與「不算熱量」主張衝突，記為內容策略觀察，不寫入 core

## 2026-09-18｜新增品牌定位
- Decision: 新增 memory/project/brand-positioning.md（定位句、拆解、競爭位置、風險、對內容的要求），放 project 層並標 HYPOTHESIS；strategist 與 00-content-strategy 指向它。
- Why: 使用者要求寫品牌定位；定位句是應徵者推論，依 memory/CLAUDE.md 不直接進 core。
- Evidence: research.md、competitors.md、claim-ledger VERIFIED 條目
- Alternatives rejected: 寫進 core/00-brand-core.md——品牌方未確認。
- Memory impact: project
- Conflict / blocker: 無

## 2026-09-18｜併入品牌 IG 限動截圖 2 張
- Decision: 截圖存 references/ig-screenshots/（加入 .gitignore）；學員原句 21 則去識別後寫入 audience-language-bank；參考案例 2 則；claim 新增 BRAND-003（VERIFIED）、OFFER-003（HYPOTHESIS）；定位補「品牌實際說法」與見證揭露風險；radar 新增 R20–R22、Q7–Q8。
- Why: 使用者提供 IG 截圖，補 IG 未取得與受眾語言空缺。
- Evidence: bgg-ig-story-01.jpg、bgg-ig-story-02.jpg
- Alternatives rejected: 把學員數字（腰圍、體重）寫入 ledger 或 language bank——CASE-001 需授權；把「澱粉吃夠就不想吃甜食」「把代謝搞壞」當事實——屬個人經驗與健康宣稱。
- Memory impact: project
- Conflict / blocker: 見證是品牌精選，偏正面；截圖日期未知

## 2026-09-18｜併入 IG 限動 story-03
- Decision: 學員原句 7 則入 language bank；參考案例 1 則；定位補「BA＋感受反饋」固定敘事與「考慮集含減重藥物」；radar 新增 Q9、R23（HOLD）。
- Why: 使用者提供第三張截圖；出現同業調查未涵蓋的競爭選項（猛健樂）。
- Evidence: bgg-ig-story-03.jpg
- Alternatives rejected: 把 R23 排進本週——涉及處方藥與醫療廣告規範，需法規與營養師確認；記錄 18 組前後數字——CASE-001。
- Memory impact: project
- Conflict / blocker: 猛健樂訊號只有 1 則見證，不可推論為普遍現象

## 2026-09-18｜併入 IG 限動 story-04（免費諮詢回饋表）
- Decision: 回饋原句 12 則入 language bank；OFFER-004、OFFER-005 VERIFIED；定位補轉換路徑；radar 新增 Q10、R24（轉換位，與 R14 二選一）；參考案例 1 則。
- Why: 補上「內容 → LINE → 免費諮詢 → 大師班」的轉換路徑，JD 五要求記錄 LINE 與其他導流成果。
- Evidence: bgg-ig-story-04.jpg
- Alternatives rejected: 以截圖 11／23 推算諮詢轉換率——截圖為品牌選取的部分列；記錄諮詢人員姓名——個資。
- Memory impact: project
- Conflict / blocker: 成效表是否加「諮詢預約數」欄，併入 performance.csv CONFLICT 待使用者決定

## 2026-09-19｜plan-9-videos：中秋週 board
- Decision: 9 支＝Reach 3／Trust 2／Action 3／Conversion 1；R01＋R02 合併為 S4；轉換位 R24（使用者決定）；連假照 09/25–27（使用者決定，待查證）；先寫 S1、S4、S8。
- Why: 旅程對應連假前預期焦慮 → 連假中參與 → 最後一天自責高峰；6/9 支對應定位差異；轉換只出現一次、避開連假中。
- Evidence: memory/working/9-video-board.md、research-radar.md、brand-positioning.md
- Alternatives rejected: R05、R19、R08、R14 入備選（理由見 board）；發布時段填 TBD——無帳號數據，不猜。
- Memory impact: working
- Conflict / blocker: S5 需品牌確認諮詢流程；S3、S4 份量說法需營養師

## 2026-09-19｜腳本模板加入分鏡表
- Decision: templates/short-video-script.md 新增 Storyboard 段（7 欄）；write-script 步驟 4、handoff-qa 起點、JD-MAPPING 同步。
- Why: 使用者要求；JD 四「整理腳本、參考案例及素材需求交接給拍攝與剪輯夥伴」。
- Evidence: 使用者 2026-09-19 指示
- Alternatives rejected: 另開獨立分鏡模板——一份腳本兩個檔案，交接易漏。
- Memory impact: none
- Conflict / blocker: 無

## 2026-09-19｜write-script S1／S4／S8
- Decision: 寫完 S1、S4、S8，各含分鏡表，存 `output/2026-09-21-S1.md`、`-S4.md`、`-S8.md`；S4 claims review 存 `reviews/2026-09-21-S4-claims.md`；三支 editorial review 存 `reviews/2026-09-21-S1-S4-S8-editorial.md`。三支只用「收藏」一個 CTA。
- Why: 依 HANDOFF 下一步；scriptwriter、claims-reviewer、copy-editor 由主對話扮演（未派 subagent，使用者指示）。
- Evidence: `python3 scripts/check_asset.py` 三支皆 OK（第一次 S1、S4 因說明文字同時出現「留言」「LINE」被判多重 CTA，改寫說明後通過）。
- Alternatives rejected: S4 沿用 v1「留言烤肉領順序表」——雙重 CTA；S4 寫「加工肉的鈉比你想的多」——3 個樣品不能代表全部，改成限定「資料庫裡的冷凍小香腸」；S8 寫「三天」「禮拜一」——連假天數未查證，改「好幾天」「收假」；S1 在片中提 344 份量——OFFER-003 仍是 HYPOTHESIS。
- Memory impact: working（board 狀態）
- Conflict / blocker: S1「看盤子三件事」、S4「夾取順序」需營養師確認（HUMAN_CHECK）；寫作者與審查者同一模型，獨立性有限；S4 分鏡字幕加粗 5 處，多於審查清單建議的 1–3 處，保留待使用者決定。

## 2026-09-19｜write-script S2／S3／S5／S6／S7／S9
- Decision: 寫完其餘 6 支，各含分鏡表，存 `output/2026-09-21-S2.md`～`-S9.md`；claims review：S3、S5、S9（`reviews/2026-09-21-S*-claims.md`）；editorial 6 支共用矩陣表 `reviews/2026-09-21-S2-S3-S5-S6-S7-S9-editorial.md`。本週 9 支腳本全部 DRAFTED。
- Why: 使用者指示繼續寫其餘 6 支、不派子代理；角色由主對話扮演。
- Evidence: `python3 scripts/check_asset.py` 6 支皆 OK（S3、S9、S5 第一次因說明文字含內部狀態字或「保證」被擋，改寫說明後通過）。
- Alternatives rejected: S5 用回饋表原句當 Hook——屬薦證、LEGAL-001 未確認，改列可刪鏡頭；S5 寫「不會推銷」——回饋表有「是否加入大師班」題，否認可能引人錯誤；S3 沿用 v1「月餅當那一餐的澱粉／一天一顆」——份量等值不可用；S3 封面「3 個步驟」——清單句型；S7 CTA「分享給家裡煮飯的人」——對象就是煮飯的人，改「一起煮中秋飯的人」；S9 寫飢餓／代謝機制——不可用，改用問句。
- Memory impact: working（board 狀態）
- Conflict / blocker: S5 需品牌方填時長、諮詢內容、是否介紹大師班，並確認預約走 LINE 或表單；S1／S7／S9 共用「菜、肉魚蛋豆、飯」待營養師確認；S2「麵換飯」待營養師確認；S9 需對照官網 FAQ「不吃晚餐？」；S1 封面同屬清單句型，待使用者決定是否改；S6 品牌落款弱，待使用者決定。

## 2026-09-19｜repurpose-content：S6 Threads 版
- Decision: 產出 `output/2026-09-21-S6-threads.md`（約 114 字）；三個選項與短影音版相同；每個選項加一句場景；加品牌語氣句「每一個都不用躲」；CTA 為回覆數字＋一句場面；content-calendar 新增 S6-threads 列（09/25）。
- Why: 使用者指示先做 S6 Threads（S6 主平台為 Threads、FB）；platform-adapter 由主對話扮演。
- Evidence: `scripts/check_asset.py` OK；`reviews/2026-09-21-S6-threads-editorial.md` PASS。
- Alternatives rejected: Threads 投票功能——拿不到受眾原話；沿用「這週影片講過了」——Threads 上沒有對應貼文；Hook「中秋最難的不是吃，是那個場面」——互動門檻高。
- Memory impact: working（content-calendar）
- Conflict / blocker: 「每一個都不用躲」回應 editorial ④，短影音版是否同步加入仍待使用者決定；S6 FB 版未做。

## 2026-09-19｜repurpose-content：其餘 8 支第二平台＋S6 FB＋S6 短影音加品牌句
- Decision: 依 board Platform priority 產出 9 版：S1／S2／S8／S9 Threads、S3／S4 小紅書、S5／S6／S7 FB（`output/2026-09-21-S*-{threads,xiaohongshu,fb}.md`）；S6 短影音版加「每一個都不用躲」（round 3，約 22 秒）；content-calendar 新增 9 列，共 19 列。
- Why: 使用者指示「全部都做」（2026-09-19，回報用量 40%）；解讀為「S6 短影音加品牌句」＋「每支 board 指定的第二平台各一版」。platform-adapter 由主對話扮演。
- Evidence: `scripts/check_asset.py` 9 版 OK（S5 FB 第一次因「治療」一詞 FAIL，改寫後 OK）；`reviews/2026-09-21-repurpose-editorial.md`；S5 FB 新增句補審於 `reviews/2026-09-21-S5-claims.md` 追加段。
- Alternatives rejected: 每支做滿 Threads／FB／小紅書三版——使用者未指定，board 只排一個第二平台，做滿約 2.5 倍用量；Threads／FB 版提到「這週影片講過了」——該平台未必有對應貼文；S5 FB 放回饋表原句——薦證未確認。
- Memory impact: working（content-calendar）
- Conflict / blocker: 跨平台版的待確認項與原稿相同；S5 FB 新增「先問醫師」一句待品牌方確認措辭；S8 Threads 回覆區處理方式待品牌方決定。

## 2026-09-19｜handoff-qa：中秋週製作交接包
- Decision: 產出 `output/2026-09-21-production-handoff.md`（handoff 模式；成片尚未交回，QA 模式未執行）。內容：可拍狀態與最晚確認日、依場景合併的拍攝組、道具總表、逐字不可改句、全週禁止加入、字幕粗體、CTA、系列一致性、小紅書圖卡交接、剪後檢查表。content-calendar Production status 更新 11 列。
- Why: 使用者指示；逐支分鏡已在腳本檔，交接包只放跨支整合資訊，避免兩份內容不同步。production-qa 由主對話扮演。
- Evidence: 各腳本 Storyboard 與 Production handoff notes；claims reviews；content-calendar 發布日。
- Alternatives rejected: 每支各出一份交接檔——與腳本內的 handoff notes 重複；逕自把 S1 與 S3 對調發布日——排程屬使用者決定，只列為選項。
- Memory impact: working（content-calendar）
- Conflict / blocker: S1 09/21 發布，營養師需 09/20 前確認，否則建議 S1／S3 對調（待使用者決定）；「最晚要確認」日期為推估（剪輯 1 天）；check_asset 不適用本檔（內部文件，禁止清單本身含禁用字）。

## 2026-09-19｜S1／S3 發布日對調
- Decision: S3（短影音＋小紅書）改 09/21 發布；S1（短影音＋Threads）改 09/23。更新 content-calendar、製作交接包、S6 Fact notes、HANDOFF。
- Why: 使用者決定。S1 需營養師確認「三件事」，09/20 前可能來不及；S3 已可拍。
- Evidence: `output/2026-09-21-production-handoff.md` 第 1 節最晚確認日推估。
- Alternatives rejected: 維持原日期並趕營養師確認——風險在外部回覆速度，無法控制。
- Memory impact: working（content-calendar）
- Conflict / blocker: S3 需 09/20 前拍完並剪好；檔名中的「2026-09-21」是週次 ID（該週週一），不是發布日，未改名。

## 2026-09-19｜S4 粗體減為 2 處；S1 封面改非清單句
- Decision: S4 分鏡／字幕粗體只留「配角」「三成」（原 5 處）；S1 封面由「外食不用秤，問自己 3 件事」改為與 Hook 同句「外食，怎麼可能還帶秤？」。兩支 round 3。
- Why: 使用者決定；回應 editorial 審查（A 重音 1–3 個；本週不用清單句型）。
- Evidence: `reviews/2026-09-21-S1-S4-S8-editorial.md`、`reviews/2026-09-21-S2-S3-S5-S6-S7-S9-editorial.md` 已註記結案；製作交接包第 5 節同步。
- Alternatives rejected: 無。
- Memory impact: none
- Conflict / blocker: 無

## 2026-09-19｜發布前確認清單
- Decision: 產出 `output/2026-09-21-confirmation-checklist.md`：A 給營養師 5 題、B 給品牌方 10 題（可分開寄出，不含內部代號），C 內部追蹤（回覆後要改的檔與鏡號）。
- Why: 使用者要求；把散在各腳本、reviews、HANDOFF 的待確認項合併成對方可直接勾選回覆的格式。
- Evidence: 各 reviews 的 HUMAN_CHECK、claim-ledger recheck 規則、製作交接包最晚確認日。
- Alternatives rejected: 直接寄 reviews 檔——含內部代號，對方難以回答。
- Memory impact: none
- Conflict / blocker: 新增兩題原本未列入待確認：B1 品牌說法是否仍為現行（BRAND-002／003 ledger 規定對外使用前確認；S3 09/21 就會用到）、B2 出鏡人（所有腳本都假設營養師本人出鏡）。

## 2026-09-19｜檔名加版本號與日期
- Decision: 本日產出的 29 個檔（`output/` 21、`reviews/` 8）檔名加 `_V1.0_20260919`（版本在前、日期在後）。版本約定：V1.0＝主對話單一模型扮演各角色產出；V1.1＝同一系統改用 subagent 分工產出，檔名同樣格式。所有持續維護的文件（board、content-calendar、HANDOFF、output、reviews）內的路徑已同步改名。
- Why: 使用者要求，方便辨識同一系統的不同版本。
- Evidence: 改名後逐一檢查所有被引用的 V1.0 路徑都存在；19 份內容檔 check_asset 仍全部 OK。
- Alternatives rejected: 改寫本檔舊條目的路徑——決策紀錄是歷史紀錄，保留當時檔名；需要時把舊檔名加上 `_V1.0_20260919` 即可找到。
- Memory impact: working
- Conflict / blocker: 檔名開頭的 `2026-09-21` 是週次 ID，檔尾的 `20260919` 是產出日期，兩者意思不同。

## 2026-09-19｜V1.1：5 個 subagent 分工做 S1／S4／S8
- Decision: 依使用者同意依序派出 scriptwriter、claims-reviewer、copy-editor、platform-adapter、production-qa，產出 V1.1（`output/2026-09-21-S1／S4／S8_V1.1_20260919.md`、跨平台 3 份、交接包；`reviews/` 查核 3 份＋審稿 1 份）。報告與流程圖、關係圖：`work/agent-run-report_V1.1_20260919.md`。
- Why: 使用者要測試代理分工，並與 V1.0（主對話一人分飾）比較。
- Evidence: 合計 542,619 token、49 步、19.6 分鐘；每個代理固定開銷約 9 萬。獨立審查多找到 4 個問題（含 V1.0 也適用的 P3 受眾定義不符）；V1.1 寫稿代理改動營養師原話，被查核代理抓到。
- Alternatives rejected: 每支每角色各派一個（15 個）——固定開銷 3 倍；合併改寫與交接——使用者選不合成。
- Memory impact: working
- Conflict / blocker: 計畫漏了修稿步驟，交接包列拍攝前必改 15 項；B 方案實際 39.9 萬，超出使用者同意上限約 0.9 萬（已回報）；content-calendar 仍追蹤 V1.0。
