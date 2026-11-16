# Editorial Review｜2026-09-21 S2、S3、S5、S6、S7、S9

- Reviewer: copy-editor（由主對話扮演，未派 subagent；寫作者與審查者是同一個模型，獨立性有限，正式發布前建議由人再看一次）
- Date: 2026-09-19
- 標準：`references/landing-page-aiseo-method.md` 審查清單、`templates/review-card.md`
- 格式：6 支共用一張矩陣表，FIX 的細節列在表下

## 判定矩陣

| Check | S2 | S3 | S5 | S6 | S7 | S9 |
|---|---|---|---|---|---|---|
| Hook | PASS | PASS | PASS | PASS | PASS | PASS |
| Single message | PASS | PASS | PASS | PASS | PASS | PASS |
| Brand | PASS | PASS | PASS | PASS | PASS | PASS |
| Audience | PASS | PASS | PASS | PASS | PASS | PASS |
| Platform | PASS | FIX（已改）① | PASS | PASS | PASS | PASS |
| CTA | PASS | PASS | PASS | PASS | FIX（已改）② | PASS |
| Claims | HUMAN_CHECK | PASS | 暫不可用 | PASS | HUMAN_CHECK | HUMAN_CHECK |
| 角色語境 SPIN | PASS | PASS | PASS | PASS | PASS | PASS |
| 價值邏輯 FABE | PASS | PASS | FIX（空格）③ | N/A（只問不答） | PASS | PASS |
| G 語組切分 | PASS | PASS | PASS | PASS | PASS | PASS |
| A 重音強調 | PASS | PASS | PASS | PASS | PASS | PASS |
| V 語調變化 | PASS | PASS | PASS | PASS | PASS | PASS |
| E 延伸停頓 | PASS | PASS | PASS | PASS | PASS | PASS |
| 品牌人格落款 | PASS | PASS | PASS | FIX（未改）④ | PASS | PASS |
| 語意結構 | PASS | PASS | PASS | PASS | PASS | PASS |
| 問句／信任落點 | PASS | PASS | PASS | PASS | PASS | FIX（已改）⑤ |

## FIX 細節

| # | Asset | Original | Reason | Direction／結果 |
|---|---|---|---|---|
| ① | S3 | 封面「月餅不用躲｜3 個步驟給它位置」 | board 規定本週不用清單句型（同業已佔滿） | 已改為「月餅不用躲，給它一個位置」 |
| ② | S7 | board CTA「分享給家裡煮飯的人」 | 腳本對象就是煮飯的人，叫他分享給煮飯的人對不上 | 已改為「分享給一起煮中秋飯的人」 |
| ③ | S5 | — | F、A、B 的核心（聊什麼）是空格，價值邏輯要等品牌填完才成立 | 品牌填空後重審 |
| ④ | S6 | 全片 | 換掉品牌名也完全成立；互動片本來就輕 | 2026-09-19 使用者同意後已加「每一個都不用躲」，結案（見 `reviews/2026-09-21-repurpose-editorial_V1.0_20260919.md`） |
| ⑤ | S9 | board Hook 方向之外的備選「今天晚餐，你是不是打算不吃了？」 | 與同日 S8「說中心裡的話」開場太像 | 採用 board 的決策捷徑句，備選不用 |

## 系列觀察（跨 9 支）

- **S1、S7、S9 共用「菜、肉魚蛋豆、飯」三件事**，分鏡都用同一個「叮」的節奏，觀眾看多支會認得。代價是三支綁同一個營養師確認項，一次確認三支適用。
- **S1 封面「外食不用秤，問自己 3 件事」也是清單句型**，和 ① 同一個問題。S1 上一輪已交付，這次沒改，2026-09-19 使用者決定改為「外食，怎麼可能還帶秤？」，已改。
- **S2「食物沒有分好壞」** 是品牌立場的概括，不是官網逐字，列 HUMAN_CHECK。

## 總結

| Asset | Verdict | 發布前還要 |
|---|---|---|
| S2 | PASS＋HUMAN_CHECK | 營養師確認「麵換飯」與「食物沒有分好壞」 |
| S3 | PASS | 建議營養師看一眼 |
| S5 | 暫不可拍 | 品牌方填 3 個空格；決定鏡 6（薦證）是否保留 |
| S6 | PASS（④ 待決定） | 無 |
| S7 | PASS＋HUMAN_CHECK | 與 S1 同一題 |
| S9 | PASS＋HUMAN_CHECK | 與 S1 同一題；對照官網 FAQ「不吃晚餐？」 |

`scripts/check_asset.py`：6 支皆 OK（第一次 S3、S9 因說明文字寫了內部狀態字、S5 因說明文字出現「保證」被擋，改寫說明後通過）。
