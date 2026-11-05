"""图文匹配审计：SVG 里实际画了什么 vs alt/caption 声称画了什么。"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
POINTS = ROOT / "content" / "points"
MEDIA = ROOT / "content" / "media"

# SVG 里可能出现的标签：点名字母（可带撇）、数字/角度、带单位文本
TOKEN = re.compile(r"[A-Z][A-Za-z′'′]?|\d+(?:\.\d+)?|min|max|=[^<\"]{1,6}")

rows = []
for f in sorted(POINTS.glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    for m in d.get("media", []):
        svg = MEDIA / m["file"]
        if not svg.exists():
            continue
        src = svg.read_text(encoding="utf-8")
        labels = [t.strip() for t in re.findall(r">([^<>]{1,24})</text>", src) if t.strip()]
        alt = m.get("alt", "")
        cap = m.get("caption", "")
        # alt/caption 中「明确声称画出的」数字与坐标
        nums = set(re.findall(r"-?\d+(?:\.\d+)?", alt + " " + cap))
        svg_text = " ".join(labels)
        svg_nums = set(re.findall(r"-?\d+(?:\.\d+)?", svg_text))
        missing = sorted(n for n in nums if n not in svg_nums)
        # alt 中提到的点名（形如 A(3，2) 或 “点 A”）
        pt_names = set(re.findall(r"([A-Z])[(（]", alt))
        miss_pt = sorted(p for p in pt_names if p not in svg_text)
        # 图里画了但 alt 完全没提的数字（可能多画了内容）
        rows.append({
            "pid": d["id"], "file": m["file"], "labels": labels,
            "missing_nums": missing, "missing_pts": miss_pt,
            "alt_len": len(alt),
        })

print(f"{'文件':<34}{'标签数':>6}{'alt缺数字':>12}{'alt缺点名':>12}")
print("-" * 70)
flag = 0
for r in rows:
    if r["missing_nums"] or r["missing_pts"]:
        flag += 1
        print(f"{r['file']:<34}{len(r['labels']):>6}{str(r['missing_nums']):>12}{str(r['missing_pts']):>12}")
print(f"\n共 {len(rows)} 张配图，alt 声称的内容在图里找不到对应标注的：{flag} 张")

# 汇总：图里所有文字标签，检查是否有明显压字（同一坐标重复标签）
print("\n=== 各图文本标签清单 ===")
for r in rows:
    print(f"{r['file']:<34}{r['labels']}")
