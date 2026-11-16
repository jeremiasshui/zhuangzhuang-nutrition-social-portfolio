# 本機資料來源對照（僅本機有效）

`memory/` 不能放本機路徑（`scripts/check_memory.py` 會擋），所以本機路徑放這裡。`source-registry.md` 只寫邏輯 ID。檔案不存在時，改用官方網站或回報 BLOCKED。

根目錄：`/mnt/c/Users/User/Desktop/nutrition-knowledge/nutrition_data/`（2026-09-17 下載，見該資料夾 `manifest.json`）

| Source ID | 相對路徑 | 內容 | 用法 |
|---|---|---|---|
| HPA-DRIS-8 | `tw_hpa/dris_8th/` | 國健署「國人膳食營養素參考攝取量」第八版，15 個 PDF（總表、Q&A、名詞說明、碳水、蛋白質、脂質、鈉、鉀、鈣、鐵、鎂、碘、維生素 D 等） | 先讀總表與 Q&A，再讀分章；用 Read 指定頁碼 |
| HPA-DRIS-9-NOTES | `tw_hpa/dris_9th_draft/` | 第九版各章節增修訂說明（2 份） | 第八版查不到或需確認是否已修訂時 |
| TFDA-FOOD-DB | `tw_fda_food_nutrition/20_2_wide.csv` | 食藥署食品營養成分資料庫，2,180 筆，113 欄，每 100 g | 用食品名稱或俗名搜尋；只用來判斷敘述是否牴觸，**熱量數字不進公開文案** |
| USDA-FDC | `usda_fdc/foundation_foods.json` | USDA FoodData Central Foundation Foods，394 筆（英文） | 台灣資料庫沒有的食材才參考，標明是美國資料 |
| PUBMED-2026-09-17 | `pubmed/2026-09-17_summary.csv` | PubMed 摘要約 50 筆 | 只作背景，不當文案依據 |

## 專案內副本（由 `scripts/extract_nutrition.py` 本機產生，不用 AI）

- `data/nutrition/hpa/dris_8th/*.txt`、`dris_9th_draft/*.txt`：PDF 全文，每頁以 `=== p.N ===` 標示，引用頁碼用這個。
- `data/nutrition/tfda_subset.csv`：依腳本內 `FOOD_KEYWORDS` 篩出的食物（目前 180 列）。要加食物就改關鍵字後重跑：
  `~/.venvs/nutrition/bin/python scripts/extract_nutrition.py`（需 venv 內的 pypdf）

引用格式：`依據：<Source ID> <檔名> <頁碼或列名>`。
