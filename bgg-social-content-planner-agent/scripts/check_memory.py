from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]

def main():
    fails=[]
    required=[
        'memory/00_INDEX.md',
        'memory/core/00-brand-core.md',
        'memory/core/01-role-and-success.md',
        'memory/core/02-audience.md',
        'memory/core/03-content-strategy.md',
        'memory/core/04-platforms.md',
        'memory/core/05-claims-and-risk.md',
        'memory/core/06-production-quality.md',
        'memory/project/source-registry.md',
        'memory/project/claim-ledger.md',
        'memory/project/feedback-ledger.md',
        'memory/project/audience-language-bank.md',
        'memory/project/reference-case-library.md',
        'memory/project/hook-pattern-library.md',
        'memory/working/current-week.md',
        'memory/working/research-radar.md',
        'memory/working/9-video-board.md',
        'memory/learning/experiment-log.md',
    ]
    for r in required:
        if not (ROOT/r).exists():
            fails.append(f'missing {r}')

    ledger_path=ROOT/'memory/project/claim-ledger.md'
    if ledger_path.exists():
        ledger=ledger_path.read_text(encoding='utf-8')
        valid={'VERIFIED','USER_CONFIRMED','IMPORTED','HYPOTHESIS','BLOCKED'}
        for line in ledger.splitlines():
            if line.startswith('|') and re.search(r'\|\s*(?:BRAND|FOUNDER|METRIC|CASE|OFFER|NUTRITION|LEGAL)-', line):
                if not any(f'| {s} |' in line for s in valid):
                    fails.append('invalid/missing claim status: '+line)

    for p in (ROOT/'memory').rglob('*.md'):
        t=p.read_text(encoding='utf-8')
        if '/mnt/c/Users/' in t or re.search(r'[A-Za-z]:\\Users\\', t):
            fails.append(f'machine-specific path in memory: {p.relative_to(ROOT)}')

    if fails:
        print('\n'.join('FAIL: '+x for x in fails))
        return 1
    print('OK')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
