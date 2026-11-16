#!/usr/bin/env python3
"""
nutrition_sources_downloader.py
下載健康與營養的官方開放資料，並用 manifest.json 記錄每個檔案的來源、雜湊值與檢查時間。
重複執行時，內容沒變的檔案會標示為 unchanged，不會重複覆寫。

來源：
  1. 食藥署「食品營養成分資料集」（政府資料開放平臺 dataset 8543）
  2. 國健署 DRIs 第八版、第九版草案頁面上的 PDF
  3. USDA FoodData Central（Foundation Foods，需要免費 API key）
  4. PubMed 最新文獻（依關鍵字，不需金鑰）

自動下載失敗的項目，會列在 nutrition_data/manual_download_list.md，方便手動補抓。
"""
import csv
import hashlib
import io
import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("缺少套件，請先執行：pip install requests beautifulsoup4")

# ===================== 設定區（可自行修改） =====================
OUT = Path(__file__).resolve().parent / "nutrition_data"

# PubMed 查詢式：預設抓近一年「減重 + 飲食」的論文
PUBMED_QUERY = '("weight loss"[Title/Abstract] AND diet[Title/Abstract]) AND "last 1 year"[dp]'
PUBMED_MAX = 50

# USDA API key：建議用環境變數設定，不要寫死在檔案裡
USDA_API_KEY = os.environ.get("USDA_API_KEY", "")
USDA_MAX_PAGES = 5  # 每頁 200 筆

DATA_GOV_TW_DATASETS = {
    "tw_fda_food_nutrition": "8543",  # 食品營養成分資料集
}

HPA_PAGES = {
    "dris_8th": "https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=4248&pid=12285",
    "dris_9th_draft": "https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=129&pid=19883",
}

DELAY_SECONDS = 2  # 每次請求間隔，避免對官方網站造成負擔
HEADERS = {"User-Agent": "Mozilla/5.0 (personal nutrition research downloader)"}
# ===============================================================

session = requests.Session()
session.headers.update(HEADERS)
MANIFEST_PATH = OUT / "manifest.json"
manifest = {}
failures = []  # (項目, 手動下載網址, 原因)


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get(url, **kwargs):
    time.sleep(DELAY_SECONDS)
    r = session.get(url, timeout=120, **kwargs)
    r.raise_for_status()
    return r


def filename_from(response, url, fallback):
    cd = response.headers.get("Content-Disposition", "")
    m = re.search(r"filename\*?=(?:UTF-8'')?\"?([^\";]+)", cd, re.I)
    if m:
        return unquote(m.group(1))
    tail = unquote(Path(urlparse(url).path).name)
    return tail if "." in tail else fallback


def save_bytes(rel_path, content, source_url):
    rel_path = str(rel_path)
    path = OUT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(content).hexdigest()
    old = manifest.get(rel_path)
    if old and old.get("sha256") == digest and path.exists():
        status = "unchanged"
    else:
        path.write_bytes(content)
        status = "updated" if old else "new"
    manifest[rel_path] = {
        "source_url": source_url,
        "sha256": digest,
        "bytes": len(content),
        "checked_at": now(),
        "status": status,
    }
    print(f"  [{status}] {rel_path}")


# ---------- 1. 政府資料開放平臺 ----------
def download_data_gov_tw():
    print("\n[1] 政府資料開放平臺")
    for name, ds_id in DATA_GOV_TW_DATASETS.items():
        page = f"https://data.gov.tw/dataset/{ds_id}"
        api = f"https://data.gov.tw/api/v2/rest/dataset/{ds_id}"
        try:
            meta = get(api).json()
        except Exception as e:
            failures.append((name, page, f"讀取資料集資訊失敗：{e}"))
            continue
        text = json.dumps(meta, ensure_ascii=False, indent=2)
        save_bytes(f"{name}/metadata.json", text.encode("utf-8"), api)
        candidates = {
            u for u in re.findall(r"https?://[^\s\"'<>\\]+", text)
            if re.search(r"export|download|\.zip|\.csv|\.json$", u, re.I)
            and "api/v2" not in u
        }
        if not candidates:
            failures.append((name, page, "資料集資訊中找不到下載連結"))
        for i, u in enumerate(sorted(candidates), 1):
            try:
                r = get(u)
                fname = filename_from(r, u, f"resource_{i}.bin")
                save_bytes(f"{name}/{fname}", r.content, u)
            except Exception as e:
                failures.append((name, page, f"{u} 下載失敗：{e}"))


# ---------- 2. 國健署 PDF ----------
def download_hpa():
    print("\n[2] 國民健康署 PDF")
    for name, page in HPA_PAGES.items():
        try:
            html = get(page).text
        except Exception as e:
            failures.append((name, page, f"頁面讀取失敗：{e}"))
            continue
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if re.search(r"\.pdf|File/Attach|/Upload/|GetFile\.ashx", href, re.I):
                links.append(urljoin(page, href))
        links = list(dict.fromkeys(links))
        got = 0
        for i, link in enumerate(links, 1):
            try:
                r = get(link)
                is_pdf = "pdf" in r.headers.get("Content-Type", "").lower() or link.lower().endswith(".pdf")
                if not is_pdf:
                    continue
                fname = filename_from(r, link, f"file_{i}.pdf")
                save_bytes(f"tw_hpa/{name}/{fname}", r.content, link)
                got += 1
            except Exception as e:
                failures.append((name, link, f"下載失敗：{e}"))
        if got == 0:
            failures.append((name, page, "頁面上沒有抓到 PDF，請手動下載"))


# ---------- 3. USDA FoodData Central ----------
def download_usda():
    print("\n[3] USDA FoodData Central")
    if not USDA_API_KEY:
        failures.append(("usda_fdc", "https://fdc.nal.usda.gov/api-key-signup",
                         "未設定 USDA_API_KEY，已略過（申請免費金鑰後再執行）"))
        print("  未設定 USDA_API_KEY，略過")
        return
    endpoint = "https://api.nal.usda.gov/fdc/v1/foods/list"
    foods = []
    for p in range(1, USDA_MAX_PAGES + 1):
        try:
            batch = get(endpoint, params={
                "dataType": "Foundation", "pageSize": 200,
                "pageNumber": p, "api_key": USDA_API_KEY,
            }).json()
        except Exception as e:
            failures.append(("usda_fdc", "https://fdc.nal.usda.gov/download-datasets", f"第 {p} 頁失敗：{e}"))
            break
        if not batch:
            break
        foods.extend(batch)
    if foods:
        # 紀錄中的網址不含 API key，避免金鑰外洩
        save_bytes("usda_fdc/foundation_foods.json",
                   json.dumps(foods, ensure_ascii=False, indent=2).encode("utf-8"),
                   endpoint + "?dataType=Foundation")


# ---------- 4. PubMed ----------
def download_pubmed():
    print("\n[4] PubMed")
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    common = {"db": "pubmed", "tool": "nutrition_downloader"}
    try:
        ids = get(base + "esearch.fcgi", params={
            **common, "term": PUBMED_QUERY, "retmax": PUBMED_MAX,
            "retmode": "json", "sort": "pub_date",
        }).json()["esearchresult"]["idlist"]
        if not ids:
            print("  沒有符合的文獻")
            return
        xml_bytes = get(base + "efetch.fcgi", params={
            **common, "id": ",".join(ids), "retmode": "xml",
        }).content
    except Exception as e:
        failures.append(("pubmed", "https://pubmed.ncbi.nlm.nih.gov/", f"查詢失敗：{e}"))
        return

    today = datetime.now().strftime("%Y-%m-%d")
    save_bytes(f"pubmed/{today}_raw.xml", xml_bytes, base + "efetch.fcgi")

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["PMID", "年份", "期刊", "標題", "摘要", "連結"])
    for art in ET.fromstring(xml_bytes).findall(".//PubmedArticle"):
        pmid = art.findtext(".//PMID", "")
        title_el = art.find(".//ArticleTitle")
        title = "".join(title_el.itertext()) if title_el is not None else ""
        abstract = " ".join("".join(t.itertext()) for t in art.findall(".//AbstractText"))
        journal = art.findtext(".//Journal/Title", "")
        year = art.findtext(".//PubDate/Year") or art.findtext(".//PubDate/MedlineDate") or ""
        writer.writerow([pmid, year, journal, title, abstract,
                         f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"])
    # utf-8-sig 讓 Excel 正確顯示中文欄位名稱
    save_bytes(f"pubmed/{today}_summary.csv", buf.getvalue().encode("utf-8-sig"), PUBMED_QUERY)


def main():
    global manifest
    OUT.mkdir(parents=True, exist_ok=True)
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    for step in (download_data_gov_tw, download_hpa, download_usda, download_pubmed):
        try:
            step()
        except Exception as e:  # 單一來源出錯不影響其他來源
            failures.append((step.__name__, "", f"未預期錯誤：{e}"))

    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [f"# 需要手動下載的項目（{now()}）", ""]
    if failures:
        lines += [f"- **{n}**：{r}\n  - {u}" for n, u, r in failures]
    else:
        lines.append("全部自動下載成功，沒有需要手動處理的項目。")
    (OUT / "manual_download_list.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"\n完成。檔案位置：{OUT}")
    print(f"成功記錄 {len(manifest)} 個檔案；需要手動處理 {len(failures)} 項。")
    if failures:
        print("請打開 nutrition_data/manual_download_list.md 查看。")


if __name__ == "__main__":
    main()
