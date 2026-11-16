"""把整個專案（規格、代理、迴圈、CI、驗證、產出、研究）原文收進一份 HTML，交給其他人或模型重新規劃。
用法：python3 scripts/build_dossier.py  → export/project-dossier.html"""
from pathlib import Path
from html import escape
import os, re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "export" / "project-dossier.html"

# (區塊標題, 說明, glob 清單)；順序即閱讀順序
GROUPS = [
    ("交接與路由", "目前狀態、待辦、已知矛盾、給 Claude Code 的路由檔。", ["docs/HANDOFF.md", "CLAUDE.md", "CONTEXT.md"]),
    ("PRD 需求", "要做什麼、為什麼、驗收。", ["docs/PRD.md"]),
    ("SDD 設計", "架構、狀態機、驗證器成熟計畫、人物層。", ["docs/SDD.md"]),
    ("ADR 決策紀錄", "五個架構決策與理由。", ["docs/adr/*.md"]),
    ("迴圈 Loop", "總編（主對話）跑一週的步驟。", [".claude/skills/**/*.md"]),
    ("代理設定", "四個寫手、五個審稿員的工作說明書。", [".claude/agents/*.md"]),
    ("簡報包 brief", "所有代理的輸入資料。", ["brief/*.md"]),
    ("CI 程式檢查", "K1–K5 檢查程式、測試、GitHub Actions。", ["scripts/check_copy.py", "tests/*.py", ".github/workflows/*"]),
    ("驗證 黃金樣本", "已知答案的考題，用來量審稿員準不準。", ["eval/*.md"]),
    ("寫手產出：shorts", "writer-shorts 製作的九支腳本（回合 1 初稿）。", ["output/shorts/*.md"]),
    ("寫手產出：threads", "writer-threads 製作的九份。", ["output/threads/*.md"]),
    ("寫手產出：fb", "writer-fb 製作的九份。", ["output/fb/*.md"]),
    ("寫手產出：xhs", "writer-xhs 製作的九份（S9 為不發說明）。", ["output/xhs/*.md"]),
    ("研究員產出", "七個研究代理寫的研究筆記。", ["docs/research/*.md"]),
    ("更早的規劃 bgg-course-plan", "專案開始前寫在同層資料夾 bgg-course-plan/ 的草稿；2026-09-18 比對過，與 brief/ 同名檔逐字相同。", ["../bgg-course-plan/*.md"]),
    ("其他", "", [".gitignore", "scripts/build_dossier.py"]),
]

AGENTS = [
    ("writer-shorts", "寫手", "output/shorts/S1–S9.md", "9 份，CI 通過，未審"),
    ("writer-threads", "寫手", "output/threads/S1–S9.md", "9 份，CI 通過，未審"),
    ("writer-fb", "寫手", "output/fb/S1–S9.md", "9 份，CI 通過，未審"),
    ("writer-xhs", "寫手", "output/xhs/S1–S9.md", "9 份（S9 不發），CI 通過，未審"),
    ("reviewer-brand", "審稿員 C1 C2 C3 C5", "reviews/<平台>/round-N-brand.md", "無產出（曾啟動，中途停止）"),
    ("reviewer-nutrition", "審稿員 C4 C6", "reviews/<平台>/round-N-nutrition.md", "無產出（曾啟動，中途停止）"),
    ("reviewer-evidence", "審稿員 C7", "reviews/<平台>/round-N-evidence.md", "無產出"),
    ("reviewer-legal", "審稿員 C8", "reviews/<平台>/round-N-legal.md", "無產出"),
    ("reviewer-audience", "審稿員 C9", "reviews/<平台>/round-N-audience.md", "無產出"),
    ("研究員 ×7", "一次性研究", "docs/research/*.md", "7 份"),
    ("總編（主對話）", "派工、裁決、寫紀錄", "log/discussion.md", "尚未產出"),
]


def collect():
    seen, groups = set(), []
    for title, note, pats in GROUPS:
        files = []
        for pat in pats:
            base, pat = (ROOT.parent, pat[3:]) if pat.startswith("../") else (ROOT, pat)
            for p in sorted(base.glob(pat)):
                if p.is_file() and p not in seen:
                    seen.add(p); files.append(p)
        groups.append((title, note, files))
    return groups


def slug(s):
    return "f-" + re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")


def mermaid_blocks(md):
    return re.findall(r"```mermaid\n(.*?)```", md, flags=re.S)


def build():
    groups = collect()
    total = sum(len(f) for _, _, f in groups)
    sdd = (ROOT / "docs/SDD.md").read_text(encoding="utf-8")
    diagrams = "".join(f'<div class="scroll"><pre class="mermaid">{escape(m)}</pre></div>' for m in mermaid_blocks(sdd))
    loop = (ROOT / ".claude/skills/run-week/SKILL.md").read_text(encoding="utf-8")
    steps = "".join(f"<li>{escape(l[2:].strip())}</li>" for l in loop.splitlines() if re.match(r"^\d\.", l))

    agent_rows = "".join(
        f"<tr><td><code>{escape(a)}</code></td><td>{escape(r)}</td><td><code>{escape(o)}</code></td><td>{escape(s)}</td></tr>"
        for a, r, o, s in AGENTS)
    toc = "".join(f'<li><a href="#{slug(t)}">{escape(t)}</a> <span class="n">{len(f)}</span></li>' for t, _, f in groups)

    sections = []
    for title, note, files in groups:
        items = []
        for p in files:
            rel = Path(os.path.relpath(p, ROOT)).as_posix()
            text = p.read_text(encoding="utf-8")
            items.append(
                f'<details id="{slug(rel)}"><summary><code>{escape(rel)}</code>'
                f'<span class="n">{len(text.splitlines())} 行</span></summary>'
                f'<div class="scroll"><pre>{escape(text)}</pre></div></details>')
        sections.append(
            f'<section id="{slug(title)}"><h2>{escape(title)}</h2>'
            f'<p class="note">{escape(note)}</p>{"".join(items)}</section>')

    empty = '<p class="note">以下資料夾目前是空的：<code>reviews/fb</code>、<code>reviews/shorts</code>、<code>reviews/threads</code>、<code>reviews/xhs</code>、<code>log/</code>。審稿員從未完成一回合，所以沒有審稿檔與討論紀錄。</p>'

    html = f"""<title>bgg-social-agent 全貌</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;600;800&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{--bg:#F6F7F3;--ink:#1D231F;--muted:#5A655D;--accent:#2E6A4E;--rule:#DCE1DA;--code:#ECEFE9;--warn:#8A5A12;--warnbg:#FBF1DF}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#121614;--ink:#E3E8E3;--muted:#9AA59C;--accent:#80C2A1;--rule:#2A312C;--code:#1A201C;--warn:#E7B869;--warnbg:#2A2317}}}}
:root[data-theme="dark"]{{--bg:#121614;--ink:#E3E8E3;--muted:#9AA59C;--accent:#80C2A1;--rule:#2A312C;--code:#1A201C;--warn:#E7B869;--warnbg:#2A2317}}
body{{background:var(--bg);color:var(--ink);font:15px/1.7 "Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif}}
.wrap{{max-width:60rem;margin:0 auto;padding-inline:16px;padding-block:32px 64px;display:grid;gap:40px}}
h1{{font-size:1.9rem;font-weight:800;line-height:1.25;margin:0;text-wrap:balance}}
h2{{font-size:1.25rem;font-weight:800;margin:0 0 4px;padding-top:12px;border-top:2px solid var(--ink);text-wrap:balance}}
.eyebrow{{font:500 .75rem/1 "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin:0 0 8px}}
.lede{{color:var(--muted);max-width:65ch;margin:8px 0 0}}
.note{{color:var(--muted);margin:0 0 12px;max-width:65ch}}
.warn{{background:var(--warnbg);color:var(--ink);border-left:3px solid var(--warn);padding:12px 16px;max-width:65ch}}
code,pre,.n{{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace}}
code{{font-size:.85em}}
.scroll{{overflow-x:auto}}
pre{{background:var(--code);margin:0;padding:14px 16px;font-size:.8rem;line-height:1.6;white-space:pre-wrap;word-break:break-word;tab-size:4}}
pre.mermaid{{white-space:pre;background:transparent}}
table{{border-collapse:collapse;width:100%;font-size:.88rem}}
th,td{{text-align:left;padding:8px 10px;border-bottom:1px solid var(--rule);vertical-align:top}}
th{{font-weight:600;color:var(--muted)}}
ol.toc{{columns:2 16rem;margin:0;padding-left:1.4em}}
ol.toc li{{break-inside:avoid;padding:2px 0}}
a{{color:var(--accent)}}
a:focus-visible,summary:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.n{{color:var(--muted);font-size:.75rem;margin-left:8px;font-variant-numeric:tabular-nums}}
details{{border-bottom:1px solid var(--rule)}}
summary{{cursor:pointer;padding:10px 0;display:flex;flex-wrap:wrap;align-items:baseline;gap:4px}}
details[open] summary{{color:var(--accent)}}
details pre{{margin-bottom:12px}}
ol.steps{{margin:0;padding-left:1.4em;max-width:65ch}}
</style>
<main class="wrap">
<header>
<p class="eyebrow">專案全貌 · 2026-09-18 快照 · {total} 個檔案原文</p>
<h1>bgg-social-agent：壯壯營養師一週跨平台文案的多代理系統</h1>
<p class="lede">四個寫手 × 九支腳本 = 36 份文案；CI 五項程式檢查（K1–K5）；五個審稿員判定驗收清單 C1–C9；總編裁決；人決定合併；最多三回合。本頁收錄每個檔案的完整原文，供重新規劃使用。</p>
</header>

<section>
<h2>給重新規劃者</h2>
<div class="warn"><p style="margin:0">目前狀態：規格、代理、CI、36 份初稿都已完成；<b>審稿員從未跑完一回合</b>，所以沒有審稿檔、沒有討論紀錄、迴圈實際上沒有轉過。已知矛盾與全部待辦在「交接與路由 → docs/HANDOFF.md」第五、六節。作業要求的「圖」是關係圖（graph engineering），不是架構圖；PRD 仍寫成架構圖。</p></div>
</section>

<section>
<h2>工作流程</h2>
<p class="note">迴圈步驟，原文來自 <code>.claude/skills/run-week/SKILL.md</code>：</p>
<ol class="steps">{steps}</ol>
<p class="note" style="margin-top:16px">架構圖與狀態機，原文來自 <code>docs/SDD.md</code>：</p>
{diagrams}
</section>

<section>
<h2>每個代理製作的內容</h2>
<div class="scroll"><table>
<thead><tr><th>代理</th><th>角色</th><th>產出位置</th><th>實際產出</th></tr></thead>
<tbody>{agent_rows}</tbody></table></div>
{empty}
</section>

<section>
<h2>目錄</h2>
<ol class="toc">{toc}</ol>
</section>

{"".join(sections)}
</main>
"""
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)}：{total} 檔，{len(html.encode())//1024} KB")


if __name__ == "__main__":
    build()
