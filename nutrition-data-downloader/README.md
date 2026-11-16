# 營養官方資料下載器

這支 Python 程式從官方開放資料來源下載營養與健康資料，給社群內容做營養查證用。倉庫裡只放程式和下載紀錄，**原始資料不放**，需要時用這支程式重新下載。

## 資料夾內容

- `nutrition_sources_downloader.py`：下載程式。
- `manifest.json`：2026-09-17 那次下載的紀錄，共 24 個檔案，約 50MB。每個檔案都記了來源網址、SHA-256 雜湊值（可以用來確認檔案內容有沒有變）、大小和檢查時間。
- `manual_download_list.md`：同一次下載中，自動抓取失敗、需要手動補抓的項目。

## 資料來源

1. 食藥署「食品營養成分資料集」（政府資料開放平臺 dataset 8543）
2. 國健署「國人膳食營養素參考攝取量」（DRIs）第八版，以及第九版草案頁面上的 PDF
3. USDA FoodData Central 的 Foundation Foods（需要免費的 API 金鑰）
4. PubMed 近一年「減重＋飲食」的論文摘要（不需要金鑰）

## 重新下載資料

需要 Python 3。

```bash
pip install requests beautifulsoup4

# 選用：要抓 USDA 資料才需要。金鑰到 https://fdc.nal.usda.gov/api-key-signup 免費申請
export USDA_API_KEY="你的金鑰"

python3 nutrition_sources_downloader.py
```

- 資料會下載到這個資料夾底下的 `nutrition_data/`。這個資料夾已經寫進 `.gitignore`，不會被上傳。
- 新的 `manifest.json` 和 `manual_download_list.md` 會寫在 `nutrition_data/` 裡面。
- 重複執行時，內容沒變的檔案會標成 `unchanged`，不會重新寫入。
- 每次請求之間會等 2 秒，避免造成官方網站負擔。
- 某一個來源失敗，不會影響其他來源。失敗的項目會列進 `manual_download_list.md`。

## 安全

- API 金鑰只從環境變數 `USDA_API_KEY` 讀取，不寫在程式裡。
- `manifest.json` 記錄的網址也不包含金鑰。
