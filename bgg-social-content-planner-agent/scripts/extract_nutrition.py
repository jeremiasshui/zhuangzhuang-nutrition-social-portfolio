"""把本機營養資料庫中本專案需要的部分抽到 data/nutrition/（純本機執行，不用 AI）。

用法：~/.venvs/nutrition/bin/python scripts/extract_nutrition.py [--src <nutrition_data 路徑>]
來源對照見 references/local-sources.md。
"""
from pathlib import Path
import argparse, csv, logging

logging.getLogger('pypdf').setLevel(logging.ERROR)  # 字型警告不影響中文抽取

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SRC = '/mnt/c/Users/User/Desktop/nutrition-knowledge/nutrition_data'

# 選題會用到的食物（中秋、聚餐、外食、超商、甜食）。要加題目就加關鍵字。
FOOD_KEYWORDS = [
    '月餅', '蛋黃酥', '綠豆椪', '鳳梨酥', '文旦', '柚',
    '香腸', '培根', '貢丸', '烤肉', '雞腿', '豆干', '蝦', '玉米', '地瓜', '吐司',
    '青椒', '香菇', '茭白筍', '白飯', '飯糰', '茶葉蛋', '奶茶', '珍珠', '啤酒', '火鍋',
]
TFDA_COLS = ['整合編號', '食品分類', '樣品名稱', '俗名', '內容物描述', '每單位重', '廢棄率',
             '熱量(kcal)', '粗蛋白(g)', '粗脂肪(g)', '飽和脂肪(g)', '總碳水化合物(g)',
             '糖質總量(g)', '膳食纖維(g)', '鈉(mg)', '鉀(mg)']


def extract_pdfs(src: Path, out: Path):
    from pypdf import PdfReader
    rows = []
    for sub in ['dris_8th', 'dris_9th_draft']:
        for pdf in sorted((src / 'tw_hpa' / sub).glob('*.pdf')):
            reader = PdfReader(str(pdf))
            parts = [f'# {pdf.name}\n# 來源：國民健康署（本機副本 tw_hpa/{sub}）\n']
            for i, page in enumerate(reader.pages, 1):
                parts.append(f'\n=== p.{i} ===\n{page.extract_text() or ""}')
            text = ''.join(parts)
            dest = out / 'hpa' / sub / (pdf.stem + '.txt')
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(text, encoding='utf-8')
            rows.append((sub, pdf.name, len(reader.pages), len(text)))
    return rows


def extract_tfda(src: Path, out: Path):
    with open(src / 'tw_fda_food_nutrition' / '20_2_wide.csv', encoding='utf-8-sig') as f:
        data = list(csv.DictReader(f))
    hits, counts = [], {}
    for kw in FOOD_KEYWORDS:
        matched = [r for r in data if kw in r['樣品名稱'] or kw in (r['俗名'] or '')]
        counts[kw] = len(matched)
        hits += [{'關鍵字': kw, **{c: r.get(c, '') for c in TFDA_COLS}} for r in matched]
    dest = out / 'tfda_subset.csv'
    with open(dest, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['關鍵字'] + TFDA_COLS)
        w.writeheader()
        w.writerows(hits)
    return counts, len(hits)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default=DEFAULT_SRC)
    ap.add_argument('--out', default=str(ROOT / 'data' / 'nutrition'))
    a = ap.parse_args()
    src, out = Path(a.src), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for sub, name, pages, chars in extract_pdfs(src, out):
        print(f'HPA {sub} | {name} | {pages} 頁 | {chars} 字')
    counts, total = extract_tfda(src, out)
    print(f'TFDA 子集 {total} 列：' + '、'.join(f'{k}{v}' for k, v in counts.items()))


if __name__ == '__main__':
    main()
