# Editorial Review｜2026-09-21 跨平台版本（repurpose-content）

- Reviewer: copy-editor（由主對話扮演，未派 subagent；寫作者與審查者是同一個模型，獨立性有限）
- Date: 2026-09-19
- 範圍：照 board 的 Platform priority，每支第二平台各一版。S6 Threads 另見 `reviews/2026-09-21-S6-threads-editorial_V1.0_20260919.md`。
- Claims：除 S5 FB 版（意思有增加，補審見 `reviews/2026-09-21-S5-claims_V1.0_20260919.md` 追加段）外，核心意思未改，不重開 claims review。

## 判定矩陣

| Check | S1 Threads | S2 Threads | S3 小紅書 | S4 小紅書 | S5 FB | S6 FB | S7 FB | S8 Threads | S9 Threads |
|---|---|---|---|---|---|---|---|---|---|
| Hook | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Single message | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Brand | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Audience | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Platform | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| CTA | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Claims | 同原稿 HC | 同原稿 HC | PASS | 同原稿 HC | 暫不可用 | PASS | 同原稿 HC | PASS | 同原稿 HC |
| SPIN | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| FABE | PASS | PASS | PASS | PASS | FIX（空格） | N/A | PASS | PASS | PASS |
| GAVE | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 品牌落款 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 語意結構 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 問句／信任落點 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | FIX（已補）① | PASS |

HC＝HUMAN_CHECK，與原稿同一個待確認項，營養師確認原稿後跨平台版一併適用。GAVE 四項合併一欄，9 版均無 FIX。

## FIX 細節

| # | Asset | Original | Reason | 結果 |
|---|---|---|---|---|
| ① | S8 Threads | 結尾問「你心裡的那句話怎麼說」，未說明回覆區怎麼處理 | 問自責的話，回覆區可能出現情緒低落或疑似飲食困擾的內容 | 已加發布備註：只回應接住情緒的話、不給飲食處方、必要時引導專業協助，回覆措辭由品牌方決定 |
| ② | S5 FB | 「簡短的回饋表，讓我們知道聊得有沒有幫助」 | 長度與目的沒有來源 | 已改為「我們會請你填一份回饋表。」 |
| ③ | S5 FB | 「正在治療的疾病」 | check_asset 療效語規則擋下 | 改為「正在看醫師、有疾病需要照顧」 |

## 跨平台一致性檢查

- 9 版的核心句都跟原稿一樣（「換，不是禁」「不是重來，是回來」「給它一個位置」等），沒有新增原稿沒有的營養說法。
- S4 小紅書的數字、樣品限定語（「資料庫樣品數值」「冷凍小香腸」）、來源都跟原稿相同，同一張卡上沒有拆開。
- 同日的 S8、S9 Threads 結尾問句不同（心裡的話／今天的晚餐），回覆不會重疊。
- S6 三個平台（短影音、Threads、FB）選項一字不差，回覆可以合併統計。
- S6 短影音版已加「每一個都不用躲」（使用者 2026-09-19「全部都做」），editorial ④ 結案。

`scripts/check_asset.py`：9 版全部 OK（S5 FB 第一次 FAIL「醫療療效語」，改寫後 OK）。
