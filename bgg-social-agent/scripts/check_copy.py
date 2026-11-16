"""CI 檢查：程式能確定判斷的五項。介面：check_dir(root) -> Report。規格：docs/SDD.md §9。"""
from dataclasses import dataclass, field
from pathlib import Path
import re, sys

PLATFORMS = ("shorts", "threads", "fb", "xhs")
EXPECTED = {f"S{i}.md" for i in range(1, 10)}
TITLE_RE = re.compile(r"^# (S[1-9])｜.+｜(shorts|threads|fb|xhs)$")
LIMITS = {"shorts": 260, "threads": 300, "fb": 400, "xhs": 300}
SHORTS_SEGMENTS = ("開場", "主體", "重點整理", "行動引導")
ANNOTATION_RE = re.compile(r"【[^】]*】")

def sections(body: str) -> dict:
    """把「## 標題」切成 {標題: 內容}；標題前的文字放在 ''。"""
    out, key = {"": []}, ""
    for ln in body.splitlines():
        if ln.startswith("## "):
            key = ln[3:].strip(); out.setdefault(key, [])
        else:
            out[key].append(ln)
    return {k: "\n".join(v) for k, v in out.items()}

def counted_text(platform: str, body: str) -> str:
    sec = sections(body)
    if platform == "shorts":
        picked = [v for k, v in sec.items() if any(k.startswith(s) for s in SHORTS_SEGMENTS)]
    elif platform == "xhs":
        picked = [v for k, v in sec.items() if k.startswith("正文")]
    else:
        picked = [body]
    text = ANNOTATION_RE.sub("", "\n".join(picked))
    return re.sub(r"\s+", "", text)

GUARDRAILS = (("保證", "含「保證」"), ("大卡", "含熱量數字「大卡」"), ("kcal", "含熱量數字「kcal」"), ("保健食品", "含「保健食品」"))

def split_header(text: str):
    """檔頭 = 開頭到第一個空行；正文 = 之後全部。"""
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.strip() == "":
            return lines[:i], "\n".join(lines[i + 1:])
    return lines, ""

@dataclass
class Failure:
    platform: str
    script: str
    rule: str
    message: str

@dataclass
class Report:
    failures: list = field(default_factory=list)
    @property
    def ok(self) -> bool:
        return not self.failures

def check_dir(root: Path) -> Report:
    rep = Report()
    for p in PLATFORMS:
        d = root / p
        names = {f.name for f in d.glob("S*.md")} if d.exists() else set()
        missing, extra = sorted(EXPECTED - names), sorted(names - EXPECTED)
        if missing or extra:
            rep.failures.append(Failure(p, "-", "K1", f"缺 {missing} 多 {extra}"))
        for name in sorted(names & EXPECTED):
            rep.failures += check_file(p, name[:-3], (d / name).read_text(encoding="utf-8"))
    return rep

def check_file(platform: str, script: str, text: str) -> list:
    out = []
    lines = text.splitlines()
    m = TITLE_RE.match(lines[0] if lines else "")
    if not m or m.group(1) != script or m.group(2) != platform:
        out.append(Failure(platform, script, "K2", "第 1 行須為「# S<n>｜標題｜<平台>」且編號與平台相符"))
    if len(lines) < 2 or not lines[1].startswith("回合："):
        out.append(Failure(platform, script, "K2", "第 2 行須以「回合：」開頭"))
    if len(lines) < 3 or not lines[2].startswith("本輪修改："):
        out.append(Failure(platform, script, "K2", "第 3 行須以「本輪修改：」開頭"))
    _, body = split_header(text)
    low = body.lower()
    for word, msg in GUARDRAILS:
        if word.lower() in low:
            out.append(Failure(platform, script, "K3", msg))
    if re.search(r"藥[^。\n]*推薦|推薦[^。\n]*藥", body):
        out.append(Failure(platform, script, "K3", "同句含「藥」與「推薦」"))
    n = len(counted_text(platform, body))
    if n > LIMITS[platform]:
        out.append(Failure(platform, script, "K4", f"正文 {n} 字，上限 {LIMITS[platform]}"))
    links = body.count("lin.ee")
    if links > 1:
        out.append(Failure(platform, script, "K5", f"LINE 連結出現 {links} 次"))
    if links >= 1 and "留言" in body:
        out.append(Failure(platform, script, "K5", "同時有留言引導與 LINE 連結"))
    return out

def main(argv):
    root = Path(argv[1] if len(argv) > 1 else "output")
    rep = check_dir(root)
    for f in rep.failures:
        print(f"[{f.rule}] {f.platform}/{f.script}: {f.message}")
    print("OK" if rep.ok else f"FAIL {len(rep.failures)}")
    return 0 if rep.ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv))
