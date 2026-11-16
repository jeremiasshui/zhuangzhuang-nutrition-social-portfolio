from pathlib import Path
import re, sys

FORBIDDEN = [
    (r"保證", "結果保證"),
    (r"(?:立刻|立即).*(?:瘦|減重)", "速效承諾"),
    (r"(?:根治|治療|治癒)", "醫療療效語"),
    (r"(?:瘦|減)\s*\d+(?:\.\d+)?\s*(?:公斤|kg).*(?:天|週|月)", "固定結果與時程"),
]

def split_frontmatter(text):
    if text.startswith('---\n'):
        end=text.find('\n---\n',4)
        if end!=-1:
            return text[4:end], text[end+5:]
    return '', text

def check(path: Path):
    text=path.read_text(encoding='utf-8')
    meta, body=split_frontmatter(text)
    failures=[]
    for pat,label in FORBIDDEN:
        if re.search(pat, body, re.I|re.S): failures.append(label)
    if '留言' in body and re.search(r'LINE|lin\.ee', body, re.I):
        failures.append('多重 CTA：留言 + LINE')
    # internal statuses should not leak into public copy body
    if re.search(r'\b(?:VERIFIED|IMPORTED|HYPOTHESIS|BLOCKED|USER_CONFIRMED)\b', body):
        failures.append('內部 claim 狀態洩漏到正文')
    if not meta:
        failures.append('缺少 YAML frontmatter')
    else:
        for key in ['task_id:','platform:','persona:','goal:','risk_level:','round:','cta:']:
            if key not in meta: failures.append(f'frontmatter 缺 {key[:-1]}')
    return failures

def main():
    if len(sys.argv)<2:
        print('usage: python scripts/check_asset.py <file>'); return 2
    failures=check(Path(sys.argv[1]))
    if failures:
        for f in failures: print('FAIL:',f)
        return 1
    print('OK')
    return 0

if __name__=='__main__': raise SystemExit(main())
