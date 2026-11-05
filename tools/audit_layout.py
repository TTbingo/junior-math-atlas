"""方位一致性审计：把 SVG 里每个文本标注按左右半区归类，
与 alt/caption 中「左…右…」描述声称的内容比对。"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
POINTS = ROOT / "content" / "points"
MEDIA = ROOT / "content" / "media"

TEXT_RE = re.compile(r"<text[^>]*?x=\"([\d.\-]+)\"[^>]*?y=\"([\d.\-]+)\"[^>]*?>([^<]*)</text>")


def halves(svg_path):
    src = svg_path.read_text(encoding="utf-8")
    m = re.search(r"width=\"([\d.]+)\"", src)
    W = float(m.group(1)) if m else 680.0
    left, right = [], []
    for x, y, t in TEXT_RE.findall(src):
        t = t.strip()
        if not t:
            continue
        (left if float(x) < W / 2 else right).append(t)
    return W, left, right


def keywords(seg):
    """从 alt 的左右描述片段里抽出点名/关键词（连写如 ABCDE 拆成单个字母）"""
    ks = set()
    for tok in re.findall(r"[A-Z][A-Za-z′']*", seg):
        if len(tok) == 1:
            ks.add(tok)
        else:
            # 连写点名：拆成字母（撇号保留在前一个字母上）
            for i, ch in enumerate(tok):
                if ch.isupper():
                    ks.add(ch + ("′" if i + 1 < len(tok) and tok[i + 1] == "′" else ""))
    return ks


def split_lr(alt):
    """按「左图：」「右图：」「①…②…」这类明确标记切分左右两段"""
    m = re.search(r"(左图|左)[：:]\s*(.*?)(?=右图|右[：:])", alt, re.S)
    n = re.search(r"(右图|右)[：:]\s*(.*)$", alt, re.S)
    if m and n:
        return m.group(2), n.group(2)
    return None, None


out = []
for f in sorted(POINTS.glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    for m in d.get("media", []):
        alt = m.get("alt", "")
        if not re.search(r"左|右", alt):
            continue
        p = MEDIA / m["file"]
        if not p.exists():
            continue
        W, L, R = halves(p)
        seg_l, seg_r = split_lr(alt)
        if seg_l is None:
            continue
        kl, kr = keywords(seg_l), keywords(seg_r)
        sl = " ".join(L)
        sr = " ".join(R)
        miss_l = sorted(k for k in kl if k not in sl)
        miss_r = sorted(k for k in kr if k not in sr)
        out.append((d["id"], m["file"], miss_l, miss_r, len(L), len(R), seg_l[:60], seg_r[:60]))

print(f"{'篇目':<36}{'图':<30}{'左半区缺':<18}{'右半区缺'}")
print("-" * 110)
flag = 0
for pid, f, ml, mr, nl, nr, sl, sr in out:
    if ml or mr:
        flag += 1
        print(f"{pid:<36}{f:<30}{str(ml):<18}{str(mr)}")
        print(f"    左描述: {sl}")
        print(f"    右描述: {sr}")
print(f"\n共 {len(out)} 张含左右描述的图，声称内容在对应半区找不到的：{flag} 张")
