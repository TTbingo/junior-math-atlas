"""把正文里的裸知识点 ID（m2-05-02）换成知识点名称 + 跳转链接。

做法分两步：
1) 内容层：把裸 ID 换成 [[m2-05-02]] 标记（保留机器可读性，便于校验与再次替换）
2) 渲染层：build.py 的 md_inline 把 [[id]] 转成 <a href="...">知识点名</a>

替换规则按 ID 周围的上下文分类处理，不同句式用不同的连接词：
- 「（m2-01-03）」→「（相交线与平行线）」
- 「到 m2-04-06 再展开」→「到「相交线与平行线」再展开」
- 「学了 m2-02-02 再回看」→「学了「全等三角形」再回看」
- 「m2-03-02 判定②」→「平行四边形的判定②」
- 「m2-01-03 的结论」→「「相交线与平行线」的结论」
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
C = ROOT / "content" / "points"

PAT = re.compile(r"\bm[123]-\d{2}-\d{2}\b")
SKIP = re.compile(r"\.related\[\d+\]\.id$")

# id → 标题
TITLES = {}
for f in sorted(C.glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    TITLES[d["id"]] = d["title"]

# ── 上下文规则表：按顺序尝试，命中即用 ──
# 每条规则：(正则, 替换模板)。{id} {title} 为占位。
RULES = [
    # 「（m2-01-03）」这类纯括注
    (re.compile(r"（\s*(m[123]-\d{2}-\d{2})\s*）"), "（@@@ID@@@）"),
    # 「到 m2-04-06 再展开」「在 m2-02-05」等：ID 前有介词
    (re.compile(r"(到|在|加|按|依|据|用|见|自|从)(m[123]-\d{2}-\d{2})\b"), "\1@@@ID@@@"),
    # 「学了 m2-02-02 再回看」「m2-02-05 已证」「m2-03-02 判定②」
    (re.compile(r"\b(m[123]-\d{2}-\d{2})\b"), "@@@ID@@@"),
]


def convert(text):
    """把一段文本里的裸 ID 转成 [[id]] 标记。

    一次性扫描：按优先级找最长的匹配区间，命中的 ID 用 \x01 占位，
    最后统一还原成 [[id]]。避免多轮替换互相包裹。
    """
    # 先把已有的 [[id]] 保护起来，保证脚本可重复运行
    protected = []

    def _stash(m):
        protected.append(m.group(0))
        return f"@@@PROT{len(protected)-1}@@@"

    text = re.sub(r"\[\[m[123]-\d{2}-\d{2}\]\]", _stash, text)

    best = {}   # 起始位置 -> (结束位置, 替换文本)
    for pat, rep in RULES:
        for m in pat.finditer(text):
            s0, e0 = m.span()
            if any(not (e0 <= bs or s0 >= be) for bs, (be, _r) in best.items()):
                continue  # 与已命中的区间重叠，保留先命中的（规则按优先级）
            gid = m.group(len(m.groups()))
            best[s0] = (e0, rep.replace("@@@ID@@@", f"[[{gid}]]"))
    if not best:
        # 没有新命中，但仍需还原受保护的标记
        for i, mk in enumerate(protected):
            text = text.replace(f"@@@PROT{i}@@@", mk)
        return text
    out = []
    pos = 0
    for s0 in sorted(best):
        if s0 < pos:
            continue
        e0, rep = best[s0]
        out.append(text[pos:s0])
        out.append(rep)
        pos = e0
    out.append(text[pos:])
    res = "".join(out)
    # 还原受保护的标记
    for i, mk in enumerate(protected):
        res = res.replace(f"@@@PROT{i}@@@", mk)
    return res


def main():
    """只处理 sections 里的正文文本。

    绝不能碰 id / slug / media.file / related[].id 这些数据字段——
    它们是构建系统的键，改了会直接把站点改坏。
    """
    total = 0
    touched = {}
    for f in sorted(C.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        n = 0

        def walk(o):
            """就地替换字符串；related 的 note 走文本，id 保持原样。"""
            nonlocal n
            if isinstance(o, str):
                new = convert(o)
                if new != o:
                    n += 1
                return new
            if isinstance(o, list):
                return [walk(v) for v in o]
            if isinstance(o, dict):
                return {k: walk(v) for k, v in o.items()}
            return o

        secs = d["sections"]
        new_secs = {}
        for k, v in secs.items():
            if k == "related":
                # related 的 id 是数据键，只处理 note
                new_secs[k] = [
                    {**r, "note": convert(r.get("note", ""))} for r in v
                ]
            else:
                new_secs[k] = walk(v)
        d["sections"] = new_secs

        if n:
            # 断言：数据字段没被动过
            assert d["id"].startswith(("m1-", "m2-", "m3-")), f"id 被改坏: {d['id']}"
            assert "/" not in d["slug"], f"slug 被改坏: {d['slug']}"
            for mm in d.get("media", []):
                assert mm["file"].endswith(".svg"), f"media.file 被改坏: {mm['file']}"
            f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
            touched[d["id"]] = n
            total += n
    print(f"替换 {total} 处，涉及 {len(touched)} 篇")
    for k, v in sorted(touched.items(), key=lambda x: -x[1])[:12]:
        print(f"  {k:<42}{v} 处")
    if len(touched) > 12:
        print(f"  …其余 {len(touched)-12} 篇各 1-2 处")


if __name__ == "__main__":
    main()
