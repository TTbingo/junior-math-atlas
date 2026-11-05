"""全站内容审计：结构、引用、图文、TeX 纪律。只报事实，不做修复。"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
POINTS = ROOT / "content" / "points"
MEDIA = ROOT / "content" / "media"

SECTIONS = ["explanation", "scenarios", "cautions", "why", "method",
            "examples", "inferences", "pitfalls", "intuition", "related"]

SCENES = {"图形设计", "测量与工程", "竞技与游戏", "生活优化", "物理情境",
          "行程与速度", "销售与利润", "数据调查", "方案选择", "金融与增长"}

issues = []


def add(level, pid, msg):
    issues.append((level, pid, msg))


docs = {}
for f in sorted(POINTS.glob("*.json")):
    try:
        docs[f.stem] = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        add("ERR", f.stem, f"JSON 解析失败: {e}")

ids = set()
for pid, d in docs.items():
    ids.add(d.get("id"))

# ---------- 1. 结构 ----------
for pid, d in docs.items():
    if d.get("id") != pid:
        add("ERR", pid, f"id 与文件名不一致: {d.get('id')}")
    if d.get("schema") != 1:
        add("WARN", pid, f"schema={d.get('schema')}")
    if d.get("segment") != 4:
        add("ERR", pid, f"segment={d.get('segment')}（合法值只有 4）")
    miss = [s for s in SECTIONS if s not in d.get("sections", {})]
    if miss:
        add("ERR", pid, f"缺板块: {miss}")
        continue
    s = d["sections"]
    why = s["why"]
    for k in ("steps", "experiment"):
        if k not in why:
            add("ERR", pid, f"why 缺 {k}")
    if not why.get("steps"):
        add("ERR", pid, "why.steps 为空")
    # diagram 可为空（无配图篇目），但非空时必须指向 media 里的 id

# ---------- 2. 引用闭环 ----------
pending_related = []   # 指向尚未写作篇目的边，记录下来供后续批次核对
for pid, d in docs.items():
    s = d["sections"]
    pre = d.get("prerequisites", [])
    for p in pre:
        if p not in ids:
            pending_related.append((pid, "prerequisites", p))
    # related 目标必须存在；指向未写篇目的边会被 build 静默跳过（不算错，但是内容债）
    for r in s.get("related", []):
        if r.get("id") not in ids:
            pending_related.append((pid, "related", r.get("id")))
        if not r.get("note"):
            add("WARN", pid, f"related {r.get('id')} 缺 note")
    # 前置不得同时出现在 related（体检规则，复核）
    rel_ids = {r.get("id") for r in s.get("related", [])}
    dup = rel_ids & set(pre)
    if dup:
        add("ERR", pid, f"related 里写了前置: {dup}")

# 前置无环
def has_cycle():
    color = {}
    stack = []

    def dfs(u):
        color[u] = 1
        stack.append(u)
        for v in docs[u].get("prerequisites", []):
            if v not in docs:
                continue
            if color.get(v) == 1:
                add("ERR", u, f"前置成环: {' -> '.join(stack[stack.index(v):] + [v])}")
                return True
            if color.get(v) is None and dfs(v):
                return True
        stack.pop()
        color[u] = 2
        return False

    for n in docs:
        if color.get(n) is None:
            if dfs(n):
                return True
    return False


has_cycle()

# ---------- 2b. 前置顺序倒挂 ----------
def order_key(pid):
    m = re.match(r"m(\d)-(\d\d)-(\d\d)", pid)
    return tuple(int(x) for x in m.groups()) if m else (9, 99, 99)


for pid, d in docs.items():
    for p in d.get("prerequisites", []):
        if p in docs and order_key(p) > order_key(pid):
            add("ERR", pid, f"前置倒挂（前置比本文靠后）: {p}")

# ---------- 3. 媒体 ----------
media_owner = {}
for pid, d in docs.items():
    s = d["sections"]
    media = d.get("media", [])
    figids = {m.get("id") for m in media}
    if s["why"].get("diagram") and s["why"]["diagram"] not in figids:
        add("ERR", pid, f"why.diagram={s['why'].get('diagram')} 不在 media 里")
    # 有 media 却没挂进 why 也无妨（可能只挂在例题），但既没挂 why 也没挂例题才警示
    ex_figids = {f for e in s["examples"] for f in (e.get("media") or [])}
    if media and not s["why"].get("diagram"):
        orphan = [m.get("id") for m in media if m.get("id") not in ex_figids]
        if orphan:
            add("WARN", pid, f"图 {orphan} 既未挂 why.diagram 也未挂例题，只能靠兜底插入")
    for m in media:
        f = m.get("file")
        if not (MEDIA / f).exists():
            add("ERR", pid, f"配图文件缺失: {f}")
        else:
            media_owner.setdefault(f, []).append(pid)
        for k in ("id", "alt", "caption", "width", "height"):
            if not m.get(k):
                add("ERR", pid, f"media {f} 缺 {k}")
    # 正文引用的「图 N」是否超出 media 数量
    blob = json.dumps(s, ensure_ascii=False)
    figs = {int(x) for x in re.findall(r"图\s*(\d+)", blob)}
    if figs and max(figs) > len(media):
        add("ERR", pid, f"正文提到图 {sorted(figs)}，但只有 {len(media)} 张配图")

for f, owners in media_owner.items():
    if len(owners) > 1:
        add("WARN", owners[0], f"配图被多篇共用: {f} <- {owners}")

# ---------- 4. 例题与场景 ----------
for pid, d in docs.items():
    exs = d["sections"]["examples"]
    if not exs:
        add("ERR", pid, "无例题")
        continue
    scenes = []
    for e in exs:
        if e.get("scene") not in SCENES:
            add("ERR", pid, f"{e.get('id')} scene 非法: {e.get('scene')}")
        scenes.append(e.get("scene"))
        for k in ("id", "scene", "context", "question", "solution", "answer"):
            if not e.get(k):
                add("ERR", pid, f"{e.get('id')} 缺 {k}")
        for k in e:
            if k not in ("id", "scene", "context", "question", "solution", "answer", "media"):
                add("WARN", pid, f"{e.get('id')} 有额外字段 {k}")
    if len(set(scenes)) != len(scenes):
        add("WARN", pid, f"同篇例题场景重复: {scenes}")

# ---------- 4b. 陷阱块字段完整性 ----------
# 注：假陷阱（wrong 说的其实是对的）无法靠措辞或片段比对可靠检出——
# 实测「wrong 与 right 共享数学片段」规则 23 条命中全为误报（共享的多是题设片段而非结论），
# 因此不设自动判定，改为人工复核（见 CLAUDE.md 规则 31）。
for pid, d in docs.items():
    for i, pf in enumerate(d["sections"].get("pitfalls", [])):
        if not pf.get("right") or not pf.get("why") or not pf.get("wrong"):
            add("ERR", pid, f"pitfalls[{i}] 缺 wrong/why/right")

# ---------- 5. TeX 纪律 ----------
def walk(o, path=""):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, f"{path}.{k}")


for pid, d in docs.items():
    for path, txt in walk(d["sections"]):
        # 解码后出现「三个及以上」反斜杠一定是写多了（\\ 本身是 cases/array 的换行，合法）
        if "\\\\\\" in txt:
            add("ERR", pid, f"{path} 含三连反斜杠")
        # 缺一对 $ 的粗判
        if txt.count("$") % 2:
            add("ERR", pid, f"{path} $ 未配对: {txt[:60]}")
        # 裸露 TeX 命令（不在 $ 内）
        stripped = re.sub(r"\$[^$]*\$", "", txt)
        bad = re.findall(r"\\(frac|times|cdot|circ|angle|triangle|sqrt|perp|parallel|geqslant|leqslant|tfrac|overrightarrow)", stripped)
        if bad:
            add("ERR", pid, f"{path} $ 外有 TeX 命令: {set(bad)}")

# ---------- 输出 ----------
by_level = {"ERR": [], "WARN": []}
for lv, pid, msg in issues:
    by_level[lv].append((pid, msg))

print(f"审计 {len(docs)} 篇 / {len(media_owner)} 张配图")
print(f"ERR {len(by_level['ERR'])} 条 | WARN {len(by_level['WARN'])} 条")
for pid, msg in by_level["ERR"]:
    print(f"[ERR ] {pid}  {msg}")
for pid, msg in by_level["WARN"]:
    print(f"[WARN] {pid}  {msg}")

print(f"\n待写篇目引用（不是错，是内容债，写作时须核对 id 拼写）：{len(pending_related)} 条")
from collections import Counter
targets = Counter(t for _, _, t in pending_related)
for t, n in targets.most_common():
    srcs = [s for s, k, tt in pending_related if tt == t]
    print(f"  {t}  <- {len(srcs)} 处: {', '.join(srcs)}")
