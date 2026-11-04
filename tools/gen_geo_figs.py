# -*- coding: utf-8 -*-
"""几何第一批（m2-01 五篇 + m2-02 收尾四篇）配图生成器。

纪律（CLAUDE.md）：
- SVG 是 XML：所有文本经 esc() 转义，禁止裸 < > &
- width/height 与 viewBox 严格一致
- 图内文字与正文数字严格一致（alt / caption / SVG 内三方对齐）
"""
import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "content" / "media"

DARK = "#1f2937"
GREY = "#6b7280"
GREYM = "#9ca3af"
BLUE = "#2563eb"
BLUEF = "#dbeafe"
GRN = "#16a34a"
GRNF = "#dcfce7"
RED = "#dc2626"
REDF = "#fee2e2"
YEL = "#b45309"
YELF = "#fef3c7"
PURP = "#7c3aed"
PURPF = "#ede9fe"


def esc(s):
    return (str(s).replace("&", "&amp;")
            .replace("<", "&lt;").replace(">", "&gt;"))


class Fig:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.buf = []

    def line(self, x1, y1, x2, y2, color=DARK, width=2.0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.buf.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"{d}/>')

    def poly(self, pts, fill="none", stroke=DARK, width=2.0, dash=None):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.buf.append(
            f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{width}" stroke-linejoin="round"{d}/>')

    def circle(self, x, y, r, fill="none", stroke=DARK, width=1.5):
        self.buf.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{width}"/>')

    def dot(self, x, y, color=DARK, r=3.5):
        self.buf.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" '
            f'stroke="{color}" stroke-width="1"/>')

    def text(self, x, y, s, size=12, color=DARK, anchor="start", weight=None):
        w = f' font-weight="{weight}"' if weight else ""
        self.buf.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}" font-family="Noto Sans SC, PingFang SC, '
            f'Microsoft YaHei, sans-serif"{w}>{esc(s)}</text>')

    def arc(self, cx, cy, r, a1, a2, color=DARK, width=1.6, dash=None,
            span_pass=None):
        """以 (cx,cy) 为圆心、半径 r 的圆弧，从屏幕角 a1 画到 a2（度，0=东，90=南）。
        默认走劣弧（<180°）；span_pass='cw' 或 'ccw' 指定跨越方向（用于大角）。"""
        a1r, a2r = math.radians(a1), math.radians(a2)
        x1, y1 = cx + r * math.cos(a1r), cy + r * math.sin(a1r)
        x2, y2 = cx + r * math.cos(a2r), cy + r * math.sin(a2r)
        if span_pass is None:
            # 取两侧夹角中较小的一个：diff 落在 [-180,180)，符号决定绕行方向
            diff = ((a2 - a1 + 180) % 360) - 180
            sweep = 1 if diff >= 0 else 0
            large = 0
        else:
            sweep = 1 if span_pass == "cw" else 0
            large = 0
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.buf.append(
            f'<path d="M {x1:.1f} {y1:.1f} A {r} {r} 0 {large} {sweep} '
            f'{x2:.1f} {y2:.1f}" fill="none" stroke="{color}" '
            f'stroke-width="{width}"{d}/>')

    def arrow_head(self, x, y, dx, dy, color=DARK, size=9):
        """在 (x,y) 处画箭头，指向 (dx,dy) 单位方向。"""
        ang = math.atan2(dy, dx)
        a1 = ang + math.radians(152)
        a2 = ang - math.radians(152)
        p1 = (x + size * math.cos(a1), y + size * math.sin(a1))
        p2 = (x + size * math.cos(a2), y + size * math.sin(a2))
        self.poly([(x, y), p1, p2], fill=color, stroke=color, width=1)

    def arrow_line(self, x1, y1, x2, y2, color=DARK, width=2.0, dash=None):
        self.line(x1, y1, x2, y2, color, width, dash)
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy)
        self.arrow_head(x2, y2, dx / n, dy / n, color)

    def right_angle(self, vx, vy, d1, d2, size=11, color=DARK):
        """在顶点 (vx,vy) 画直角符号，两边方向为屏幕角 d1、d2。"""
        p1 = (vx + size * math.cos(math.radians(d1)),
              vy + size * math.sin(math.radians(d1)))
        p2 = (vx + size * math.cos(math.radians(d2)),
              vy + size * math.sin(math.radians(d2)))
        pc = (p1[0] + p2[0] - vx, p1[1] + p2[1] - vy)
        self.poly([p1, pc, p2], fill="none", stroke=color, width=1.4)

    def tick(self, x1, y1, x2, y2, n=1, color=DARK, size=6):
        """线段中点的相等记号（垂直小短线，可重复 n 次）。"""
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        n_ = math.hypot(dx, dy)
        ux, uy = -dy / n_, dx / n_
        for i in range(n):
            off = (i - (n - 1) / 2) * 6
            cx, cy = mx + ux * 0, my + uy * 0
            sx, sy = cx + ux * 0 + dx / n_ * 0, cy
            a = (mx + ux * 0 + (i - (n - 1) / 2) * 5 * (dx / n_),
                 my + (i - (n - 1) / 2) * 5 * (dy / n_))
            self.line(a[0] - ux * size / 2, a[1] - uy * size / 2,
                      a[0] + ux * size / 2, a[1] + uy * size / 2, color, 1.8)

    def chevron(self, x, y, color=DARK, size=7):
        """平行线的 > 记号。"""
        self.buf.append(
            f'<path d="M {x:.1f} {y - size / 2:.1f} L {x + size:.1f} {y:.1f} '
            f'L {x:.1f} {y + size / 2:.1f}" fill="none" stroke="{color}" '
            f'stroke-width="1.6"/>')

    def save(self, name):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" '
               f'height="{self.h}" viewBox="0 0 {self.w} {self.h}">'
               f'<rect width="{self.w}" height="{self.h}" fill="#ffffff"/>'
               + "".join(self.buf) + "</svg>")
        (OUT / name).write_text(svg, encoding="utf-8")
        print("saved", name)


def fig_lines():
    f = Fig(760, 300)
    rows = [
        ("直线", 70, "无端点，两方无限延伸", "记作直线 AB（两个大写字母）"),
        ("射线", 150, "一个端点，向一方无限延伸", "端点写在前：射线 OA"),
        ("线段", 230, "两个端点，可以度量长度", "记作线段 AB，AB = BA"),
    ]
    for name, y, desc, note in rows:
        f.text(56, y + 5, name, 14, DARK, weight="bold")
        if name == "直线":
            f.line(150, y, 340, y, DARK, 2.2)
            f.arrow_head(150, y, -1, 0, DARK)
            f.arrow_head(340, y, 1, 0, DARK)
            f.dot(200, y); f.dot(300, y)
            f.text(200, y + 22, "A", 13, DARK, anchor="middle")
            f.text(300, y + 22, "B", 13, DARK, anchor="middle")
        elif name == "射线":
            f.dot(170, y)
            f.line(170, y, 340, y, DARK, 2.2)
            f.arrow_head(340, y, 1, 0, DARK)
            f.dot(285, y)
            f.text(163, y + 22, "O", 13, DARK, anchor="middle")
            f.text(285, y - 12, "A", 13, DARK, anchor="middle")
        else:
            f.dot(170, y); f.dot(340, y)
            f.line(170, y, 340, y, DARK, 2.2)
            f.tick(170, y, 340, y, 1)
            f.text(163, y + 22, "A", 13, DARK, anchor="middle")
            f.text(347, y + 22, "B", 13, DARK, anchor="middle")
        f.text(392, y - 2, desc, 13, DARK)
        f.text(392, y + 20, note, 12, GREY)
    f.text(392, 66, "", 12, GREY)
    f.save("lines-basic.svg")


def fig_angle():
    f = Fig(760, 300)
    O = (230, 250)
    r = 185
    aA, aB, aC = 215, 285, 250
    A = (O[0] + r * math.cos(math.radians(aA)), O[1] + r * math.sin(math.radians(aA)))
    B = (O[0] + r * math.cos(math.radians(aB)), O[1] + r * math.sin(math.radians(aB)))
    C = (O[0] + r * math.cos(math.radians(aC)), O[1] + r * math.sin(math.radians(aC)))
    f.line(O[0], O[1], A[0], A[1], DARK, 2.2)
    f.line(O[0], O[1], B[0], B[1], DARK, 2.2)
    f.line(O[0], O[1], C[0], C[1], RED, 2.2)
    for p, name, off in [(O, "O", (-14, 16)), (A, "A", (-16, -6)),
                         (B, "B", (6, -8)), (C, "C", (0, -12))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.arc(O[0], O[1], 46, aA, aC, BLUE, 1.8)
    f.arc(O[0], O[1], 46, aC, aB, GRN, 1.8)
    for adeg, lab, col in [(232.5, "35°", BLUE), (267.5, "35°", GRN)]:
        lx = O[0] + 66 * math.cos(math.radians(adeg))
        ly = O[1] + 66 * math.sin(math.radians(adeg))
        f.text(lx, ly, lab, 12, col, anchor="middle")
    f.arc(O[0], O[1], 112, aA, aB, GREY, 1.2, dash="4 3")
    f.text(O[0] + 134 * math.cos(math.radians(240)),
           O[1] + 134 * math.sin(math.radians(240)),
           "70°", 12, GREY, anchor="middle")
    f.text(230, 286, "OC 平分 ∠AOB：∠AOC = ∠COB = 35°", 13, DARK, anchor="middle")
    # 右侧说明
    f.text(560, 120, "把 ∠AOB 沿 OC 对折，", 13, DARK, anchor="middle")
    f.text(560, 146, "OA 与 OB 完全重合。", 13, DARK, anchor="middle")
    f.text(560, 184, "折痕 OC 就是角平分线：", 12, GREY, anchor="middle")
    f.text(560, 208, "分出的两个角都等于原角的一半。", 12, GREY, anchor="middle")
    f.save("angle-bisector.svg")


def fig_parallel():
    f = Fig(760, 340)
    # 左：对顶角
    O = (180, 172)
    f.text(180, 36, "① 相交：对顶角", 14, DARK, anchor="middle", weight="bold")
    f.line(40, 82, 320, 262, DARK, 2.2)
    f.line(40, 262, 320, 82, DARK, 2.2)
    f.dot(*O)
    f.text(174, 190, "O", 12, DARK, anchor="end")
    d1 = math.degrees(math.atan2(82 - 262, 40 - 320))   # l2 上行方向
    f.arc(O[0], O[1], 34, 212.7, 327.3, RED, 1.8)
    f.text(O[0], O[1] - 54, "∠1", 12, RED, anchor="middle")
    f.arc(O[0], O[1], 34, 32.7, 147.3, RED, 1.8)
    f.text(O[0], O[1] + 56, "∠3", 12, RED, anchor="middle")
    f.arc(O[0], O[1], 24, 327.3, 32.7, BLUE, 1.8)
    f.text(O[0] + 44, O[1] + 4, "∠2", 12, BLUE, anchor="middle")
    f.arc(O[0], O[1], 24, 147.3, 212.7, BLUE, 1.8)
    f.text(O[0] - 44, O[1] + 4, "∠4", 12, BLUE, anchor="middle")
    f.text(180, 316, "对顶角相等：∠1 = ∠3，∠2 = ∠4", 13, DARK, anchor="middle")
    # 右：三线八角
    f.text(575, 36, "② 平行：三线八角", 14, DARK, anchor="middle", weight="bold")
    f.line(410, 105, 740, 105, DARK, 2.2)
    f.line(410, 235, 740, 235, DARK, 2.2)
    f.line(460, 50, 710, 290, GREY, 2.0)
    f.chevron(700, 105, PURP, 8)
    f.chevron(688, 105, PURP, 8)
    f.chevron(700, 235, PURP, 8)
    f.chevron(688, 235, PURP, 8)
    P = (517.3, 105)
    Q = (652.7, 235)
    f.dot(*P); f.dot(*Q)
    f.text(505, 92, "P", 12, DARK, anchor="middle")
    f.text(640, 224, "Q", 12, DARK, anchor="middle")
    # 同位角（红）：两条线的左上角
    f.arc(P[0], P[1], 26, 180, 223.8, RED, 1.8)
    f.text(P[0] - 44, P[1] - 24, "1", 12, RED, anchor="middle")
    f.arc(Q[0], Q[1], 26, 180, 223.8, RED, 1.8)
    f.text(Q[0] - 44, Q[1] - 24, "1", 12, RED, anchor="middle")
    # 内错角（绿）：P 南侧大角 / Q 北侧大角
    f.arc(P[0], P[1], 34, 50, 170, GRN, 1.8)
    f.text(P[0] - 10, P[1] + 50, "2", 12, GRN, anchor="middle")
    f.arc(Q[0], Q[1], 34, 230, 350, GRN, 1.8)
    f.text(Q[0] + 14, Q[1] - 52, "2", 12, GRN, anchor="middle")
    # 同旁内角（蓝）：P 右下小角 / Q 东侧小角
    f.arc(P[0], P[1], 16, 2, 40, BLUE, 1.8)
    f.text(P[0] + 30, P[1] + 14, "3", 12, BLUE, anchor="middle")
    f.arc(Q[0], Q[1], 16, 300, 356, BLUE, 1.8)
    f.text(Q[0] + 34, Q[1] - 26, "3", 12, BLUE, anchor="middle")
    f.text(575, 316, "a∥b：红=同位角，绿=内错角，蓝=同旁内角", 13, DARK, anchor="middle")
    f.save("parallel-angles.svg")


def fig_counterexample():
    f = Fig(760, 300)
    # 左：真命题
    f.text(180, 36, "真命题：对顶角相等", 14, DARK, anchor="middle", weight="bold")
    O = (180, 165)
    f.line(60, 75, 300, 255, DARK, 2.2)
    f.line(60, 255, 300, 75, DARK, 2.2)
    f.dot(*O)
    f.arc(O[0], O[1], 30, 212.7, 327.3, RED, 1.8)
    f.text(O[0], O[1] - 48, "∠1", 12, RED, anchor="middle")
    f.arc(O[0], O[1], 30, 32.7, 147.3, RED, 1.8)
    f.text(O[0], O[1] + 50, "∠3", 12, RED, anchor="middle")
    f.text(180, 292, "∠1 = ∠3（可由补角推导）", 12, DARK, anchor="middle")
    # 右：假命题的反例
    f.text(550, 36, "假命题：相等的角是对顶角", 14, DARK, anchor="middle", weight="bold")
    O2 = (540, 240)
    aA, aB, aC = 210, 270, 240
    r = 130
    A = (O2[0] + r * math.cos(math.radians(aA)), O2[1] + r * math.sin(math.radians(aA)))
    B = (O2[0] + r * math.cos(math.radians(aB)), O2[1] + r * math.sin(math.radians(aB)))
    C = (O2[0] + r * math.cos(math.radians(aC)), O2[1] + r * math.sin(math.radians(aC)))
    f.line(O2[0], O2[1], A[0], A[1], DARK, 2.2)
    f.line(O2[0], O2[1], B[0], B[1], DARK, 2.2)
    f.line(O2[0], O2[1], C[0], C[1], GRN, 2.2)
    for p, name, off in [(O2, "O", (12, 18)), (A, "A", (-12, 0)),
                         (B, "B", (10, -6)), (C, "C", (0, -10))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.arc(O2[0], O2[1], 34, aA, aC, GRN, 1.8)
    f.arc(O2[0], O2[1], 34, aC, aB, GRN, 1.8)
    for rr, adeg in ((58, 225), (76, 255)):
        lx = O2[0] + rr * math.cos(math.radians(adeg))
        ly = O2[1] + rr * math.sin(math.radians(adeg))
        f.text(lx, ly, "30°", 12, GRN, anchor="middle")
    f.text(560, 292, "反例：∠AOC = ∠BOC = 30°，但不是对顶角", 12, DARK, anchor="middle")
    f.save("counterexample.svg")


def fig_construction():
    f = Fig(760, 380)
    f.text(380, 28, "作线段 AB 的垂直平分线", 14, DARK, anchor="middle", weight="bold")
    A = (280, 200)
    B = (480, 200)
    r = 150
    C = (380, 200 - 111.8)
    D = (380, 200 + 111.8)
    # 作图弧（虚线）：圆心 A、B，半径 r
    f.arc(A[0], A[1], r, -48.2, -100, GREY, 1.4, dash="5 4")
    f.arc(B[0], B[1], r, -131.8, -80, GREY, 1.4, dash="5 4")
    f.arc(A[0], A[1], r, 48.2, 100, GREY, 1.4, dash="5 4")
    f.arc(B[0], B[1], r, 131.8, 80, GREY, 1.4, dash="5 4")
    # 线段与垂直平分线
    f.line(A[0], A[1], B[0], B[1], DARK, 2.2)
    f.line(C[0], C[1], D[0], D[1], RED, 2.2)
    for p, name, off in [(A, "A", (-12, 20)), (B, "B", (12, 20)),
                         (C, "C", (-16, -6)), (D, "D", (14, 4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    M = (380, 200)
    f.right_angle(M[0], M[1], 0, 90, 10, DARK)
    f.text(394, 186, "M（中点）", 12, DARK)
    # 左侧说明
    f.text(40, 150, "以 A、B 为圆心，", 12, DARK)
    f.text(40, 172, "等长半径（大于 AB 一半）", 12, DARK)
    f.text(40, 194, "画弧，两弧交于 C、D。", 12, DARK)
    f.text(40, 230, "CA=CB、DA=DB", 12, RED, weight="bold")
    f.text(40, 252, "（同一半径），", 12, GREY)
    f.text(40, 274, "CD 就是垂直平分线。", 12, DARK)
    f.save("perp-bisector-construction.svg")


def fig_models():
    f = Fig(760, 480)
    # ① 平移型
    f.text(128, 36, "① 平移型", 14, DARK, anchor="middle", weight="bold")
    t1 = [(30, 330), (150, 330), (90, 190)]
    t2 = [(125, 225), (245, 225), (185, 120)]
    for (a, b) in zip(t1, t2):
        f.line(a[0], a[1], b[0], b[1], GREYM, 1.4, dash="4 3")
    f.poly(t1, GRNF, GRN, 2.0)
    f.poly(t2, BLUEF, BLUE, 2.0)
    f.tick(t1[0][0], t1[0][1], t1[2][0], t1[2][1], 1, DARK)
    f.tick(t2[0][0], t2[0][1], t2[2][0], t2[2][1], 1, DARK)
    f.tick(t1[1][0], t1[1][1], t1[2][0], t1[2][1], 2, DARK)
    f.tick(t2[1][0], t2[1][1], t2[2][0], t2[2][1], 2, DARK)
    f.arrow_line(92, 306, 148, 244, GREY, 1.6)
    f.text(128, 430, "对应点连线", 12, GREY, anchor="middle")
    f.text(128, 452, "平行且相等", 12, GREY, anchor="middle")
    # ② 旋转型（手拉手）
    f.text(380, 36, "② 旋转型（手拉手）", 14, DARK, anchor="middle", weight="bold")
    O = (380, 250)
    A = (286, 216)
    B = (397, 152)
    C = (478, 233)
    D = (414, 344)
    for p, name, off in [(O, "O", (-14, 4)), (A, "A", (-12, -4)),
                         (B, "B", (12, -10)), (C, "C", (14, -2)),
                         (D, "D", (12, 12))]:
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.line(A[0], A[1], B[0], B[1], BLUE, 2.0)
    f.line(C[0], C[1], D[0], D[1], GRN, 2.0)
    f.line(O[0], O[1], A[0], A[1], BLUE, 2.0)
    f.line(O[0], O[1], B[0], B[1], BLUE, 2.0)
    f.line(O[0], O[1], C[0], C[1], GRN, 2.0)
    f.line(O[0], O[1], D[0], D[1], GRN, 2.0)
    f.line(A[0], A[1], C[0], C[1], RED, 1.8, dash="6 4")
    f.line(B[0], B[1], D[0], D[1], RED, 1.8, dash="6 4")
    for p in (O, A, B, C, D):
        f.dot(p[0], p[1])
    f.tick(O[0], O[1], A[0], A[1], 1, DARK)
    f.tick(O[0], O[1], B[0], B[1], 1, DARK)
    f.tick(O[0], O[1], C[0], C[1], 2, DARK)
    f.tick(O[0], O[1], D[0], D[1], 2, DARK)
    f.arc(O[0], O[1], 26, 200, 280, YEL, 1.8)
    f.arc(O[0], O[1], 26, 350, 70, YEL, 1.8)
    f.text(O[0] - 36, O[1] - 62, "∠1", 11, YEL, anchor="middle")
    f.text(O[0] + 58, O[1] + 62, "∠1", 11, YEL, anchor="middle")
    f.text(380, 430, "OA=OB、OC=OD、∠AOB=∠COD", 12, DARK, anchor="middle")
    f.text(380, 452, "→ SAS → △AOC≌△BOD → AC=BD", 12, RED, anchor="middle")
    # ③ 一线三等角（90° 特例：一线三垂直）
    f.text(635, 36, "③ 一线三等角", 14, DARK, anchor="middle", weight="bold")
    Bv = (560, 340)
    Dv = (635, 340)
    Cv = (710, 340)
    Av = (560, 265)
    Ev = (710, 265)
    f.line(Bv[0], Bv[1], Cv[0], Cv[1], DARK, 2.2)
    f.poly([Bv, Av, Dv], GRNF, GRN, 2.0)
    f.poly([Dv, Ev, Cv], BLUEF, BLUE, 2.0)
    f.line(Dv[0], Dv[1], Av[0], Av[1], GRN, 2.0)
    f.line(Dv[0], Dv[1], Ev[0], Ev[1], BLUE, 2.0)
    f.line(Cv[0], Cv[1], Ev[0], Ev[1], BLUE, 2.0)
    f.right_angle(Bv[0], Bv[1], 0, 270, 10, DARK)
    f.right_angle(Dv[0], Dv[1], 225, 315, 10, DARK)
    f.right_angle(Cv[0], Cv[1], 180, 270, 10, DARK)
    for p, name, off in [(Bv, "B", (-12, 18)), (Dv, "D", (0, 18)),
                         (Cv, "C", (12, 18)), (Av, "A", (-12, -4)),
                         (Ev, "E", (12, -4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(635, 430, "∠B = ∠ADE = ∠C（图为 90° 特例）", 12, DARK, anchor="middle")
    f.text(635, 452, "配 AB = DC → ASA → △ABD≌△DEC", 12, RED, anchor="middle")
    f.save("congruent-models.svg")


def fig_isosceles():
    f = Fig(760, 340)
    A = (380, 60)
    B = (230, 290)
    C = (530, 290)
    M = (380, 290)
    f.poly([A, B, C], "none", DARK, 2.2)
    f.line(A[0], A[1], M[0], M[1], RED, 2.2)
    for p, name, off in [(A, "A", (0, -12)), (B, "B", (-14, 16)),
                         (C, "C", (14, 16)), (M, "D", (0, 18))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    # 腰相等记号
    f.tick(A[0], A[1], B[0], B[1], 1, DARK)
    f.tick(A[0], A[1], C[0], C[1], 1, DARK)
    # 底边两段相等
    f.tick(B[0], B[1], M[0], M[1], 2, DARK)
    f.tick(M[0], M[1], C[0], C[1], 2, DARK)
    # 底角相等弧
    aB = math.degrees(math.atan2(A[1] - B[1], A[0] - B[0]))
    f.arc(B[0], B[1], 34, 0, aB, RED, 1.8)
    f.text(B[0] + 52, B[1] - 18, "∠B", 11, RED, anchor="middle")
    aC = math.degrees(math.atan2(A[1] - C[1], A[0] - C[0]))
    f.arc(C[0], C[1], 34, 180, aC, RED, 1.8)
    f.text(C[0] - 52, C[1] - 18, "∠C", 11, RED, anchor="middle")
    # 顶角被 AD 平分
    aAB = math.degrees(math.atan2(B[1] - A[1], B[0] - A[0]))
    aAC = math.degrees(math.atan2(C[1] - A[1], C[0] - A[0]))
    f.arc(A[0], A[1], 40, aAC, 90, BLUE, 1.8)
    f.arc(A[0], A[1], 40, 90, aAB, BLUE, 1.8)
    f.right_angle(M[0], M[1], 180, 270, 10, DARK)
    f.text(300, 330, "AB = AC（腰）", 12, DARK, anchor="middle")
    f.text(470, 330, "∠B = ∠C（等边对等角）", 12, RED, anchor="middle")
    f.text(380, 330, "", 12, DARK)
    f.text(380, 314, "", 12, DARK)
    f.text(620, 175, "AD 一人三职：", 13, DARK, anchor="middle", weight="bold")
    f.text(620, 200, "顶角平分线（蓝弧）", 12, BLUE, anchor="middle")
    f.text(620, 224, "底边中线（双记号）", 12, GRN, anchor="middle")
    f.text(620, 248, "底边上的高（直角记号）", 12, DARK, anchor="middle")
    f.save("isosceles-three-in-one.svg")


def fig_pythagoras():
    f = Fig(760, 340)
    f.text(380, 28, "勾股定理的拼图证明（四个全等的直角三角形）", 14, DARK,
           anchor="middle", weight="bold")
    ox, oy = 268, 50
    S = 224
    a, b = 96, 128
    outer = [(ox, oy), (ox + S, oy), (ox + S, oy + S), (ox, oy + S)]
    inner = [(ox + a, oy), (ox + S, oy + a), (ox + b, oy + S), (ox, oy + b)]
    t1 = [(ox, oy), (ox + a, oy), (ox, oy + b)]
    t2 = [(ox + a, oy), (ox + S, oy), (ox + S, oy + a)]
    t3 = [(ox + S, oy + a), (ox + S, oy + S), (ox + b, oy + S)]
    t4 = [(ox + b, oy + S), (ox, oy + S), (ox, oy + b)]
    for t, fill in [(t1, GRNF), (t2, BLUEF), (t3, GRNF), (t4, BLUEF)]:
        f.poly(t, fill, DARK, 1.6)
    f.poly(inner, YELF, YEL, 2.2)
    f.poly(outer, "none", DARK, 2.5)
    # 直角记号
    f.right_angle(ox, oy, 0, 90, 10)
    f.right_angle(ox + S, oy, 180, 90, 10)
    f.right_angle(ox + S, oy + S, 180, 270, 10)
    f.right_angle(ox, oy + S, 0, 270, 10)
    # 边长标注
    f.text(ox + a / 2, oy - 8, "a", 13, DARK, anchor="middle")
    f.text(ox + a + b / 2, oy - 8, "b", 13, DARK, anchor="middle")
    f.text(ox - 12, oy + b / 2, "b", 13, DARK, anchor="end")
    f.text(ox - 12, oy + b + a / 2, "a", 13, DARK, anchor="end")
    f.text(ox + S + 12, oy + a / 2, "a", 13, DARK)
    f.text(ox + S + 12, oy + a + b / 2, "b", 13, DARK)
    f.text(ox + b / 2, oy + S + 20, "b", 13, DARK, anchor="middle")
    f.text(ox + b + a / 2, oy + S + 20, "a", 13, DARK, anchor="middle")
    # 内部正方形标注
    f.text(ox + a + 46, oy + a - 18, "c", 13, RED, weight="bold")
    f.text((inner[0][0] + inner[1][0] + inner[2][0] + inner[3][0]) / 4,
           (inner[0][1] + inner[1][1] + inner[2][1] + inner[3][1]) / 4 + 6,
           "c²", 16, RED, anchor="middle", weight="bold")
    # 左侧推导
    f.text(30, 110, "(a+b)² = 4×½ab + c²", 14, DARK, weight="bold")
    f.text(30, 140, "展开：a²+2ab+b² = 2ab+c²", 12, GREY)
    f.text(30, 170, "得 a²+b² = c²", 14, RED, weight="bold")
    f.text(30, 210, "大正方形边长 a+b；", 12, GREY)
    f.text(30, 232, "四个三角形全等；", 12, GREY)
    f.text(30, 254, "中间是边长 c 的正方形。", 12, GREY)
    f.save("pythagoras-square.svg")


def fig_midline():
    f = Fig(760, 340)
    A = (300, 42)
    B = (150, 292)
    C = (610, 292)
    D = (225, 167)
    E = (455, 167)
    F = (380, 292)
    f.poly([A, D, E], GRNF, GRN, 1.8)
    f.poly([B, D, F], BLUEF, BLUE, 1.8)
    f.poly([D, E, F], YELF, YEL, 1.8)
    f.poly([E, C, F], PURPF, PURP, 1.8)
    f.poly([A, B, C], "none", DARK, 2.2)
    f.line(D[0], D[1], E[0], E[1], RED, 2.5)
    for p, name, off in [(A, "A", (0, -12)), (B, "B", (-14, 18)),
                         (C, "C", (14, 18)), (D, "D", (-14, -6)),
                         (E, "E", (14, -6)), (F, "F", (0, 20))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    # 中点记号
    f.tick(A[0], A[1], D[0], D[1], 1, DARK)
    f.tick(D[0], D[1], B[0], B[1], 1, DARK)
    f.tick(A[0], A[1], E[0], E[1], 1, DARK)
    f.tick(E[0], E[1], C[0], C[1], 1, DARK)
    f.tick(B[0], B[1], F[0], F[1], 1, DARK)
    f.tick(F[0], F[1], C[0], C[1], 1, DARK)
    f.text(340, 152, "DE（中位线）", 12, RED, anchor="middle")
    f.text(380, 332, "DE∥BC 且 DE=½BC；三条中位线把三角形分成 4 个全等的小三角形",
           12, DARK, anchor="middle")
    f.save("triangle-midline.svg")




# ============ 几何第二批（m2-03 四边形 4 篇） ============

def fig_polygon():
    f = Fig(760, 340)
    # ① 左：五边形拆三角形
    f.text(200, 40, "① 内角和：拆三角形", 14, DARK, anchor="middle", weight="bold")
    cx, cy, R = 200, 185, 110
    ang = [-90, -18, 54, 126, 198]
    V = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a)))
         for a in ang]
    A, B, C, D, E = V
    f.poly([A, B, C], GRNF, GRN, 1.8)
    f.poly([A, C, D], BLUEF, BLUE, 1.8)
    f.poly([A, D, E], YELF, YEL, 1.8)
    f.poly(V, "none", DARK, 2.2)
    f.line(A[0], A[1], C[0], C[1], RED, 2.2)
    f.line(A[0], A[1], D[0], D[1], RED, 2.2)
    for p, name, off in [(A, "A", (0, -12)), (B, "B", (14, 4)),
                         (C, "C", (12, 18)), (D, "D", (-10, 18)),
                         (E, "E", (-14, 4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(200, 316, "从 A 出发的 2 条对角线，分成 3 个三角形", 12, DARK, anchor="middle")
    f.text(200, 336, "内角和 = 3×180° = 540°", 13, RED, anchor="middle", weight="bold")
    # ② 右：正五边形外角和
    f.text(580, 40, "② 外角和：走一圈", 14, DARK, anchor="middle", weight="bold")
    cx2, cy2, R2 = 580, 178, 80
    W = [(cx2 + R2 * math.cos(math.radians(a)), cy2 + R2 * math.sin(math.radians(a)))
         for a in ang]
    f.poly(W, "none", DARK, 2.2)
    for i in range(5):
        Vi, Vn, Vp = W[i], W[(i + 1) % 5], W[(i - 1) % 5]
        t_in = math.degrees(math.atan2(Vi[1] - Vp[1], Vi[0] - Vp[0]))
        t_out = math.degrees(math.atan2(Vn[1] - Vi[1], Vn[0] - Vi[0]))
        f.arc(Vi[0], Vi[1], 18, t_in, t_out, RED, 1.8)
        if i in (1, 3):
            ex = Vi[0] + 34 * math.cos(math.radians(t_in))
            ey = Vi[1] + 34 * math.sin(math.radians(t_in))
            f.line(Vi[0], Vi[1], ex, ey, GREY, 1.4, dash="5 4")
            mid = (t_in + t_out) / 2
            lx = Vi[0] + 48 * math.cos(math.radians(mid))
            ly = Vi[1] + 48 * math.sin(math.radians(mid))
            f.text(lx, ly, "72°", 12, RED, anchor="middle")
    f.text(580, 316, "每个外角 72°（沿边走，每个顶点转一次）", 12, DARK, anchor="middle")
    f.text(580, 336, "外角和 = 5×72° = 360°，与边数无关", 13, RED,
           anchor="middle", weight="bold")
    f.save("polygon-interior.svg")


def fig_parallelogram():
    f = Fig(760, 360)
    # ① 左：性质三件套
    f.text(210, 40, "① 性质三件套", 14, DARK, anchor="middle", weight="bold")
    A, B, C, D = (120, 90), (360, 90), (300, 270), (60, 270)
    O = (210, 180)
    f.poly([A, B, C, D], "none", DARK, 2.2)
    f.line(A[0], A[1], C[0], C[1], GREY, 1.6)
    f.line(B[0], B[1], D[0], D[1], GREY, 1.6)
    # 对边平行记号（紫色）与相等记号
    f.chevron(250, 90, PURP, 8)
    f.chevron(190, 270, PURP, 8)
    f.tick(A[0], A[1], B[0], B[1], 1, DARK)
    f.tick(C[0], C[1], D[0], D[1], 1, DARK)
    f.tick(A[0], A[1], D[0], D[1], 2, DARK)
    f.tick(B[0], B[1], C[0], C[1], 2, DARK)
    # 对角线互相平分记号
    f.tick(A[0], A[1], O[0], O[1], 3, DARK)
    f.tick(O[0], O[1], C[0], C[1], 3, DARK)
    f.tick(B[0], B[1], O[0], O[1], 4, DARK)
    f.tick(O[0], O[1], D[0], D[1], 4, DARK)
    # 对角相等弧
    aAD = math.degrees(math.atan2(D[1] - A[1], D[0] - A[0]))
    f.arc(A[0], A[1], 22, 0, aAD, RED, 2.0)
    aCB = math.degrees(math.atan2(B[1] - C[1], B[0] - C[0]))
    f.arc(C[0], C[1], 22, 180, aCB, RED, 2.0)
    f.arc(B[0], B[1], 22, 180, aAD, BLUE, 2.0)
    f.arc(D[0], D[1], 22, 0, aCB, BLUE, 2.0)
    for p, name, off in [(A, "A", (-10, -6)), (B, "B", (10, -6)),
                         (C, "C", (12, 18)), (D, "D", (-12, 18)),
                         (O, "O", (12, 4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(210, 320, "红弧：∠A=∠C；蓝弧：∠B=∠D（邻角互补）", 12, DARK,
           anchor="middle")
    f.text(210, 342, "对边平行且相等，对角线互相平分", 12, DARK, anchor="middle")
    # ② 右：沿对角线拆成两个全等三角形
    f.text(590, 40, "② 拆开看：两个全等三角形", 14, DARK, anchor="middle", weight="bold")
    A2, B2, C2, D2 = (480, 110), (700, 110), (660, 280), (440, 280)
    f.poly([A2, B2, C2], GRNF, GRN, 1.8)
    f.poly([A2, C2, D2], BLUEF, BLUE, 1.8)
    f.line(A2[0], A2[1], C2[0], C2[1], DARK, 1.8)
    f.line(A2[0], A2[1], B2[0], B2[1], DARK, 2.0)
    f.line(B2[0], B2[1], C2[0], C2[1], DARK, 2.0)
    f.line(C2[0], C2[1], D2[0], D2[1], DARK, 2.0)
    f.line(D2[0], D2[1], A2[0], A2[1], DARK, 2.0)
    # 内错角弧：AD 截 AC（绿），AB 截 AC（蓝）
    aA2C2 = math.degrees(math.atan2(C2[1] - A2[1], C2[0] - A2[0]))
    aA2D2 = math.degrees(math.atan2(D2[1] - A2[1], D2[0] - A2[0]))
    f.arc(A2[0], A2[1], 22, aA2C2, aA2D2, GRN, 1.8)
    f.arc(A2[0], A2[1], 22, 0, aA2C2, BLUE, 1.8)
    aC2A2 = aA2C2 + 180
    aC2B2 = math.degrees(math.atan2(B2[1] - C2[1], B2[0] - C2[0]))
    aC2D2 = math.degrees(math.atan2(D2[1] - C2[1], D2[0] - C2[0]))
    f.arc(C2[0], C2[1], 22, aC2B2, aC2A2, GRN, 1.8)
    f.arc(C2[0], C2[1], 22, aC2D2, aC2A2, BLUE, 1.8)
    f.text(560, 304, "同色弧＝一对内错角", 12, DARK, anchor="middle")
    for p, name, off in [(A2, "A", (-12, -6)), (B2, "B", (10, -6)),
                         (C2, "C", (12, 18)), (D2, "D", (-12, 18))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(590, 336, "AB∥DC、AD∥BC → 内错角相等 + 公共边 AC", 12, DARK,
           anchor="middle")
    f.text(590, 356, "→ ASA → 两个三角形全等 → 对边相等", 12, RED,
           anchor="middle", weight="bold")
    f.save("parallelogram-properties.svg")


def fig_special():
    f = Fig(760, 380)
    # ① 矩形
    f.text(140, 52, "① 矩形：加直角", 14, DARK, anchor="middle", weight="bold")
    A, B, C, D = (50, 120), (230, 120), (230, 260), (50, 260)
    O = (140, 190)
    f.poly([A, B, C, D], "none", DARK, 2.2)
    f.line(A[0], A[1], C[0], C[1], GREY, 1.6)
    f.line(B[0], B[1], D[0], D[1], GREY, 1.6)
    f.right_angle(A[0], A[1], 0, 90, 9, DARK)
    f.right_angle(B[0], B[1], 180, 90, 9, DARK)
    f.right_angle(C[0], C[1], 180, 270, 9, DARK)
    f.right_angle(D[0], D[1], 0, 270, 9, DARK)
    for p, q in [(A, O), (B, O), (C, O), (D, O)]:
        f.tick(p[0], p[1], q[0], q[1], 1, DARK)
    for p, name, off in [(A, "A", (-16, -10)), (B, "B", (16, -10)),
                         (C, "C", (16, 20)), (D, "D", (-16, 20)),
                         (O, "O", (14, -6))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(140, 316, "对角线相等且互相平分", 12, DARK, anchor="middle")
    f.text(140, 338, "OA=OB=OC=OD", 13, RED, anchor="middle", weight="bold")
    # ② 菱形
    f.text(380, 52, "② 菱形：邻边相等", 14, DARK, anchor="middle", weight="bold")
    A2, B2, C2, D2 = (380, 100), (480, 190), (380, 280), (280, 190)
    O2 = (380, 190)
    f.poly([A2, B2, C2, D2], "none", DARK, 2.2)
    f.line(A2[0], A2[1], C2[0], C2[1], GREY, 1.6)
    f.line(B2[0], B2[1], D2[0], D2[1], GREY, 1.6)
    f.right_angle(O2[0], O2[1], 90, 180, 9, DARK)
    for s, e in [(A2, B2), (B2, C2), (C2, D2), (D2, A2)]:
        f.tick(s[0], s[1], e[0], e[1], 1, DARK)
    f.tick(A2[0], A2[1], O2[0], O2[1], 2, DARK)
    f.tick(O2[0], O2[1], C2[0], C2[1], 2, DARK)
    f.tick(B2[0], B2[1], O2[0], O2[1], 3, DARK)
    f.tick(O2[0], O2[1], D2[0], D2[1], 3, DARK)
    for p, name, off in [(A2, "A", (0, -12)), (B2, "B", (16, 4)),
                         (C2, "C", (0, 22)), (D2, "D", (-16, 4)),
                         (O2, "O", (12, -8))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(400, 146, "d1/2", 11, GREY)
    f.text(430, 184, "d2/2", 11, GREY)
    f.text(380, 316, "对角线互相垂直平分、平分对角", 12, DARK, anchor="middle")
    f.text(380, 338, "面积 = 1/2 × d1 × d2", 13, RED, anchor="middle", weight="bold")
    # ③ 正方形
    f.text(620, 52, "③ 正方形：两样都加", 14, DARK, anchor="middle", weight="bold")
    A3, B3, C3, D3 = (540, 130), (700, 130), (700, 290), (540, 290)
    O3 = (620, 210)
    f.poly([A3, B3, C3, D3], "none", DARK, 2.2)
    f.line(A3[0], A3[1], C3[0], C3[1], GREY, 1.6)
    f.line(B3[0], B3[1], D3[0], D3[1], GREY, 1.6)
    f.right_angle(O3[0], O3[1], 90, 180, 9, DARK)
    for p, q in [(A3, O3), (B3, O3), (C3, O3), (D3, O3)]:
        f.tick(p[0], p[1], q[0], q[1], 1, DARK)
    for p, name, off in [(A3, "A", (-16, -10)), (B3, "B", (16, -10)),
                         (C3, "C", (16, 20)), (D3, "D", (-16, 20)),
                         (O3, "O", (14, -6))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(620, 316, "对角线相等 + 互相垂直平分", 12, DARK, anchor="middle")
    f.text(620, 338, "正方形 = 矩形 ∩ 菱形", 13, RED, anchor="middle", weight="bold")
    f.save("special-quadrilaterals.svg")


def fig_trapezoid():
    f = Fig(760, 380)
    # ① 左：等腰梯形平移一腰
    f.text(230, 40, "① 等腰梯形：平移一腰", 14, DARK, anchor="middle", weight="bold")
    A, B, C, D = (140, 110), (320, 110), (370, 280), (90, 280)
    E = (190, 280)  # A + (C - B)，AE ∥ BC
    f.poly([A, B, C, E], BLUEF, BLUE, 1.6)
    f.poly([A, D, E], GRNF, GRN, 1.6)
    f.poly([A, B, C, D], "none", DARK, 2.2)
    f.line(A[0], A[1], E[0], E[1], RED, 2.2, dash="7 4")
    # 腰相等记号 + 平行记号
    f.tick(A[0], A[1], D[0], D[1], 1, DARK)
    f.tick(B[0], B[1], C[0], C[1], 1, DARK)
    f.chevron(215, 150, PURP, 7)
    f.chevron(348, 195, PURP, 7)
    # 等腰三角形 ADE 底角弧
    aDA = math.degrees(math.atan2(A[1] - D[1], A[0] - D[0]))
    f.arc(D[0], D[1], 22, 0, aDA, GRN, 1.8)
    aEA = math.degrees(math.atan2(A[1] - E[1], A[0] - E[0]))
    f.arc(E[0], E[1], 22, 180, aEA, GRN, 1.8)
    f.text(D[0] + 46, D[1] - 26, "∠ADE", 11, GRN, anchor="middle")
    f.text(E[0] + 52, E[1] - 26, "∠AED", 11, GRN, anchor="middle")
    for p, name, off in [(A, "A", (-12, -4)), (B, "B", (10, -4)),
                         (C, "C", (14, 18)), (D, "D", (-12, 18)),
                         (E, "E", (0, 20))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(230, 322, "AE∥BC：拆成平行四边形 ABCE + 等腰 △ADE", 12, DARK,
           anchor="middle")
    f.text(230, 346, "AD=AE=BC → ∠ADE=∠AED", 12, RED, anchor="middle", weight="bold")
    # ② 右：中点四边形
    f.text(575, 40, "② 中点四边形：连中点", 14, DARK, anchor="middle", weight="bold")
    A2, B2, C2, D2 = (450, 100), (700, 120), (660, 300), (470, 280)
    f.line(A2[0], A2[1], C2[0], C2[1], GREY, 1.6, dash="6 4")
    f.line(B2[0], B2[1], D2[0], D2[1], GREY, 1.6, dash="6 4")
    E2 = ((A2[0] + B2[0]) / 2, (A2[1] + B2[1]) / 2)
    F2 = ((B2[0] + C2[0]) / 2, (B2[1] + C2[1]) / 2)
    G2 = ((C2[0] + D2[0]) / 2, (C2[1] + D2[1]) / 2)
    H2 = ((D2[0] + A2[0]) / 2, (D2[1] + A2[1]) / 2)
    f.poly([E2, F2, G2, H2], YELF, YEL, 2.0)
    f.poly([A2, B2, C2, D2], "none", DARK, 2.2)
    for s, e in [(A2, E2), (E2, B2), (B2, F2), (F2, C2),
                 (C2, G2), (G2, D2), (D2, H2), (H2, A2)]:
        f.tick(s[0], s[1], e[0], e[1], 1, GREY, size=5)
    for p, name, off in [(A2, "A", (-14, -6)), (B2, "B", (14, -6)),
                         (C2, "C", (14, 18)), (D2, "D", (-14, 18)),
                         (E2, "E", (0, -10)), (F2, "F", (16, 4)),
                         (G2, "G", (0, 22)), (H2, "H", (-16, 4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(575, 322, "EF、HG 都是中位线：平行于 AC 且等于 AC 的一半", 12, DARK,
           anchor="middle")
    f.text(575, 346, "同理 EH、FG 平行于 BD → EFGH 是平行四边形", 12, RED,
           anchor="middle", weight="bold")
    f.save("trapezoid-midpoints.svg")


if __name__ == "__main__":
    fig_lines()
    fig_angle()
    fig_parallel()
    fig_counterexample()
    fig_construction()
    fig_models()
    fig_isosceles()
    fig_pythagoras()
    fig_midline()
    fig_polygon()
    fig_parallelogram()
    fig_special()
    fig_trapezoid()


# ============ 几何第三批（m2-04 圆 6 篇） ============

def fig_circle_perp():
    f = Fig(760, 360)
    # ① 垂径定理
    f.text(190, 40, "① 垂径定理：连圆心，作垂线", 14, DARK, anchor="middle", weight="bold")
    O, R = (190, 175), 110
    half = math.sqrt(110**2 - 50**2)
    A, B = (190 - half, 225), (190 + half, 225)
    D, C = (190, 225), (190, 285)
    f.circle(O[0], O[1], R, "none", DARK, 2.2)
    f.line(A[0], A[1], B[0], B[1], DARK, 2.2)
    f.line(O[0], O[1], C[0], C[1], RED, 2.2)
    f.line(O[0], O[1], A[0], A[1], GREY, 1.4)
    f.text(128, 196, "R", 11, GREY)
    aA = math.degrees(math.atan2(A[1] - O[1], A[0] - O[0]))
    aB = math.degrees(math.atan2(B[1] - O[1], B[0] - O[0]))
    f.arc(O[0], O[1], R, aB, aA, RED, 3.2)
    f.right_angle(D[0], D[1], -90, 180, 9)
    f.tick(A[0], A[1], D[0], D[1], 1, DARK)
    f.tick(D[0], D[1], B[0], B[1], 1, DARK)
    f.text(204, 196, "d", 12, RED)
    f.text(141, 245, "a/2", 12, DARK, anchor="middle")
    for p, name, off in [(O, "O", (12, 4)), (A, "A", (-16, 0)), (B, "B", (16, 0)),
                         (D, "D", (-14, 18)), (C, "C", (14, 4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(190, 316, "OD⊥AB → AD=DB，OD 平分弧 AB", 12, DARK, anchor="middle")
    f.text(190, 341, "R²=d²+(a/2)²（勾股）", 13, RED, anchor="middle", weight="bold")
    # ② 拱桥
    f.text(600, 40, "② 拱桥：矢高与半径", 14, DARK, anchor="middle", weight="bold")
    O2, R2 = (600, 155), 100
    half2 = math.sqrt(R2**2 - 75**2)
    A2, B2 = (600 - half2, 230), (600 + half2, 230)
    aA2 = math.degrees(math.atan2(A2[1] - O2[1], A2[0] - O2[0]))
    aB2 = math.degrees(math.atan2(B2[1] - O2[1], B2[0] - O2[0]))
    arch = [(600 + R2 * math.cos(math.radians(a)),
             155 + R2 * math.sin(math.radians(a)))
            for a in [aA2 + i * 3 for i in range(int((aB2 + 360 - aA2) / 3) + 1)]]
    f.poly(arch, "none", DARK, 2.4)
    f.line(505, 230, 715, 230, DARK, 2.2)
    f.line(O2[0], O2[1], 600, 55, GREY, 1.4)
    f.text(588, 104, "R", 11, GREY)
    f.line(O2[0], O2[1], 600, 230, GREY, 1.4, dash="5 4")
    f.right_angle(600, 230, -90, 180, 9)
    f.arrow_line(575, 230, 575, 58, RED, 1.8)
    f.text(560, 150, "h", 12, RED)
    f.arrow_line(A2[0], 254, B2[0], 254, GREY, 1.6)
    f.text(600, 276, "a（跨度）", 12, GREY, anchor="middle")
    for p, name, off in [(O2, "O", (12, 4)), ((600, 230), "M", (12, 4)),
                         (A2, "", (0, 0)), (B2, "", (0, 0))]:
        if name:
            f.dot(p[0], p[1])
            f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.dot(A2[0], A2[1]); f.dot(B2[0], B2[1])
    f.text(600, 316, "R² = (a/2)² + (R−h)²", 13, RED, anchor="middle", weight="bold")
    f.text(600, 341, "圆心到桥面 = R−h（垂足是跨度中点）", 12, DARK, anchor="middle")
    f.save("circle-perpendicular.svg")


def fig_central_inscribed():
    f = Fig(760, 380)
    # ① 圆心角与圆周角
    f.text(200, 36, "① 圆周角 = 圆心角的一半", 14, DARK, anchor="middle", weight="bold")
    O, R = (200, 195), 120
    A = (200 + R * math.cos(math.radians(140)), 195 + R * math.sin(math.radians(140)))
    B = (200 + R * math.cos(math.radians(40)), 195 + R * math.sin(math.radians(40)))
    C = (200, 75)
    f.circle(O[0], O[1], R, "none", DARK, 2.0)
    f.arc(O[0], O[1], R, 40, 140, RED, 3.2)
    f.line(O[0], O[1], A[0], A[1], DARK, 2.0)
    f.line(O[0], O[1], B[0], B[1], DARK, 2.0)
    f.line(C[0], C[1], A[0], A[1], BLUE, 2.2)
    f.line(C[0], C[1], B[0], B[1], BLUE, 2.2)
    f.arc(O[0], O[1], 26, 40, 140, RED, 2.0)
    f.text(200, 239, "100°", 12, RED, anchor="middle")
    aCA = math.degrees(math.atan2(A[1] - C[1], A[0] - C[0]))
    aCB = math.degrees(math.atan2(B[1] - C[1], B[0] - C[0]))
    f.arc(C[0], C[1], 30, aCB, aCA, BLUE, 2.0)
    f.text(200, 122, "50°", 12, BLUE, anchor="middle")
    f.text(200, 331, "弧 AB", 11, RED, anchor="middle")
    for p, name, off in [(O, "O", (12, 4)), (A, "A", (-14, 18)), (B, "B", (14, 18)),
                         (C, "C", (0, -12))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(200, 355, "∠AOB=100°（圆心角），∠ACB=50°（圆周角）", 12, DARK, anchor="middle")
    # ② 直径所对的圆周角
    f.text(600, 36, "② 直径所对的圆周角是直角", 14, DARK, anchor="middle", weight="bold")
    O2, R2 = (600, 190), 110
    A2, B2 = (490, 190), (710, 190)
    C2, D2 = (600, 80), (600, 300)
    f.circle(O2[0], O2[1], R2, "none", DARK, 2.0)
    f.line(A2[0], A2[1], B2[0], B2[1], DARK, 3.0)
    for P in (C2, D2):
        f.line(P[0], P[1], A2[0], A2[1], BLUE, 2.0)
        f.line(P[0], P[1], B2[0], B2[1], BLUE, 2.0)
    f.right_angle(C2[0], C2[1], 45, 135, 9)
    f.right_angle(D2[0], D2[1], 225, 315, 9)
    for p, name, off in [(O2, "O", (10, -12)), (A2, "A", (-16, -8)), (B2, "B", (16, -8)),
                         (C2, "C", (0, -12)), (D2, "D", (0, 20))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(600, 340, "AB 是直径 → ∠ACB=∠ADB=90°", 12, DARK, anchor="middle")
    f.text(600, 362, "90° 圆周角反过来锁定直径", 13, RED, anchor="middle", weight="bold")
    f.save("central-inscribed.svg")


def fig_circle_position():
    f = Fig(760, 400)
    f.text(380, 26, "① 点与圆：比较 OP 与半径 r", 14, DARK, anchor="middle", weight="bold")
    # 三个点位置场景
    for cx, px, verdict in [(130, 155, "d<r：点在圆内"), (380, 425, "d=r：点在圆上"),
                            (630, 700, "d>r：点在圆外")]:
        f.circle(cx, 120, 45, "none", DARK, 1.8)
        f.line(cx, 120, px, 120, GREY, 1.4, dash="5 4")
        f.dot(cx, 120)
        f.text(cx + 8, 112, "O", 12, DARK)
        f.dot(px, 120, RED)
        f.text(px + 9, 108, "P", 12, RED)
        f.text(cx, 186, verdict, 12, DARK, anchor="middle")
        f.text((cx + px) / 2, 132, "d", 11, GREY, anchor="middle")
    f.text(380, 212, "② 直线与圆：比较圆心距 d 与半径 r", 14, DARK, anchor="middle", weight="bold")
    # 相交
    f.circle(130, 318, 42, "none", DARK, 1.8)
    f.line(85, 343, 175, 343, DARK, 2.2)
    f.line(130, 318, 130, 343, GREY, 1.4, dash="5 4")
    f.text(138, 334, "d", 11, GREY)
    for x in (130 - math.sqrt(42**2 - 25**2), 130 + math.sqrt(42**2 - 25**2)):
        f.dot(x, 343, RED, 2.6)
    f.dot(130, 318)
    f.text(138, 310, "O", 12, DARK)
    f.text(130, 382, "d<r：相交（两个公共点）", 12, DARK, anchor="middle")
    # 相切
    f.circle(380, 318, 42, "none", DARK, 1.8)
    f.line(335, 276, 425, 276, DARK, 2.2)
    f.line(380, 318, 380, 276, GREY, 1.4, dash="5 4")
    f.text(388, 296, "d", 11, GREY)
    f.right_angle(380, 276, -90, 180, 8)
    f.dot(380, 276, RED)
    f.dot(380, 318)
    f.text(388, 310, "O", 12, DARK)
    f.text(380, 382, "d=r：相切（一个公共点）", 12, DARK, anchor="middle")
    # 相离
    f.circle(630, 318, 42, "none", DARK, 1.8)
    f.line(585, 254, 675, 254, DARK, 2.2)
    f.line(630, 318, 630, 254, GREY, 1.4, dash="5 4")
    f.text(638, 282, "d", 11, GREY)
    f.dot(630, 318)
    f.text(638, 310, "O", 12, DARK)
    f.text(630, 382, "d>r：相离（无公共点）", 12, DARK, anchor="middle")
    f.save("circle-position.svg")


def fig_tangent():
    f = Fig(760, 390)
    # ① 切线性质
    f.text(200, 36, "① 切线：恰一个公共点，垂直于半径", 14, DARK, anchor="middle", weight="bold")
    O, R = (190, 190), 95
    f.circle(O[0], O[1], R, "none", DARK, 2.0)
    f.line(75, 285, 305, 285, DARK, 2.4)
    f.line(190, 190, 190, 285, RED, 2.2)
    f.right_angle(190, 285, -90, 0, 10)
    f.text(146, 240, "半径", 11, RED)
    f.line(100, 80, 280, 130, GREY, 1.5, dash="6 4")
    f.dot(165.5, 98.2, GREY, 2.6)
    f.dot(258.3, 124.0, GREY, 2.6)
    f.text(284, 105, "割线", 11, GREY)
    for p, name, off in [(O, "O", (12, 4)), ((190, 285), "C", (10, 20)),
                         ((75, 285), "A", (-12, -12)), ((305, 285), "B", (12, -12))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(200, 352, "切线 AB ⊥ 半径 OC；割线（虚线）有两个公共点", 12, DARK, anchor="middle")
    # ② 切线长定理
    f.text(570, 36, "② 切线长定理：PA=PB，OP 平分 ∠APB", 14, DARK, anchor="middle", weight="bold")
    O2, R2, P = (560, 240), 80, (560, 70)
    pa = math.sqrt(170**2 - 80**2)
    th = math.degrees(math.acos(80 / 170))
    A = (560 + 80 * math.cos(math.radians(-90 + th)), 240 + 80 * math.sin(math.radians(-90 + th)))
    B = (560 + 80 * math.cos(math.radians(-90 - th)), 240 + 80 * math.sin(math.radians(-90 - th)))
    f.circle(O2[0], O2[1], R2, "none", DARK, 2.0)
    f.line(P[0], P[1], A[0], A[1], DARK, 2.2)
    f.line(P[0], P[1], B[0], B[1], DARK, 2.2)
    f.line(O2[0], O2[1], A[0], A[1], BLUE, 1.8)
    f.line(O2[0], O2[1], B[0], B[1], BLUE, 1.8)
    f.line(P[0], P[1], O2[0], O2[1], RED, 2.0, dash="6 4")
    aPtoA = math.degrees(math.atan2(A[1] - P[1], A[0] - P[0]))
    aPtoB = math.degrees(math.atan2(B[1] - P[1], B[0] - P[0]))
    f.arc(P[0], P[1], 24, aPtoA, 90, GRN, 1.8)
    f.arc(P[0], P[1], 24, 90, aPtoB, GRN, 1.8)
    aAtoO = math.degrees(math.atan2(O2[1] - A[1], O2[0] - A[0]))
    aAtoP = math.degrees(math.atan2(P[1] - A[1], P[0] - A[0]))
    f.right_angle(A[0], A[1], aAtoO, aAtoP, 9)
    aBtoO = math.degrees(math.atan2(O2[1] - B[1], O2[0] - B[0]))
    aBtoP = math.degrees(math.atan2(P[1] - B[1], P[0] - B[0]))
    f.right_angle(B[0], B[1], aBtoO, aBtoP, 9)
    f.tick(P[0], P[1], A[0], A[1], 1, DARK)
    f.tick(P[0], P[1], B[0], B[1], 1, DARK)
    f.text(520, 106, "平分", 11, GRN, anchor="middle")
    for p, name, off in [(P, "P", (0, -14)), (O2, "O", (12, 4)),
                         (A, "A", (18, 6)), (B, "B", (-18, 6))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(570, 352, "∠OAP=∠OBP=90°；∠AOB+∠APB=180°", 12, DARK, anchor="middle")
    f.text(570, 374, "HL 全等：△OAP≌△OBP", 13, RED, anchor="middle", weight="bold")
    f.save("tangent-lines.svg")


def fig_arc_cone():
    f = Fig(760, 380)
    # ① 扇形
    f.text(190, 34, "① 扇形：n° 占整圆的 n/360", 14, DARK, anchor="middle", weight="bold")
    O, R = (190, 205), 110
    arcpts = [(190 + R * math.cos(math.radians(a)), 205 + R * math.sin(math.radians(a)))
              for a in range(30, 151, 5)]
    f.poly([O] + arcpts + [O], YELF, DARK, 1.6)
    f.arc(O[0], O[1], R, 30, 150, RED, 3.0)
    A, B = arcpts[0], arcpts[-1]
    f.line(O[0], O[1], A[0], A[1], DARK, 2.2)
    f.line(O[0], O[1], B[0], B[1], DARK, 2.2)
    f.arc(O[0], O[1], 26, 30, 150, DARK, 1.6)
    f.text(190, 249, "n°", 12, DARK, anchor="middle")
    f.text(238, 214, "R", 11, GREY)
    f.text(190, 334, "l（弧长）", 12, RED, anchor="middle")
    for p, name, off in [(O, "O", (12, 4)), (A, "A", (16, 4)), (B, "B", (-16, 4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(190, 358, "l=nπR/180　S=nπR²/360=½lR", 12, RED, anchor="middle", weight="bold")
    # ② 圆锥与展开
    f.text(600, 34, "② 圆锥：侧面展开是扇形", 14, DARK, anchor="middle", weight="bold")
    V, base, rx, ry = (460, 90), (460, 280), 65, 13
    f.line(V[0], V[1], base[0] - rx, base[1], DARK, 2.2)
    f.line(V[0], V[1], base[0] + rx, base[1], DARK, 2.2)
    ell = [(460 + rx * math.cos(math.radians(a)), 280 + ry * math.sin(math.radians(a)))
           for a in range(0, 360, 6)]
    f.poly(ell, "none", DARK, 1.8)
    f.line(V[0], V[1], base[0], base[1], GREY, 1.4, dash="5 4")
    f.text(468, 188, "h", 12, GREY)
    f.line(base[0], base[1], base[0] + rx, base[1], GREY, 1.6)
    f.text(492, 298, "r", 12, GREY)
    f.right_angle(460, 280, -90, 0, 8)
    f.text(516, 170, "l（母线）", 11, DARK, anchor="middle")
    for p, name, off in [(V, "V", (0, -12)), (base, "O", (10, 4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    # 展开扇形
    O2, R2 = (665, 250), 85
    pts = [(665 + R2 * math.cos(math.radians(a)), 250 + R2 * math.sin(math.radians(a)))
           for a in range(120, 241, 5)]
    f.poly([O2] + pts + [O2], YELF, DARK, 1.6)
    f.arc(O2[0], O2[1], R2, 120, 240, RED, 3.0)
    E1, E2 = pts[0], pts[-1]
    f.line(O2[0], O2[1], E1[0], E1[1], DARK, 2.0)
    f.line(O2[0], O2[1], E2[0], E2[1], DARK, 2.0)
    f.arc(O2[0], O2[1], 26, 120, 240, DARK, 1.6)
    f.text(620, 250, "θ", 12, DARK, anchor="middle")
    f.text(560, 306, "2πr", 12, RED, anchor="middle")
    f.text(640, 206, "l", 11, DARK, anchor="middle")
    f.arrow_line(540, 250, 573, 250, RED, 1.8)
    f.text(554, 220, "剪开摊平", 11, RED, anchor="middle")
    for p, name, off in [(O2, "O", (12, 4)), (E1, "", (0, 0)), (E2, "", (0, 0))]:
        if name:
            f.dot(p[0], p[1])
            f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(600, 336, "母线 l → 扇形半径；底面周长 2πr → 扇形弧长", 12, DARK, anchor="middle")
    f.text(600, 360, "S侧=πrl；θ=360°·r/l", 12, RED, anchor="middle", weight="bold")
    f.save("arc-sector-cone.svg")


def fig_regular_poly():
    f = Fig(760, 380)
    # ① 正六边形
    f.text(200, 30, "① 正六边形：两圆同心，R=a", 14, DARK, anchor="middle", weight="bold")
    O, R = (200, 190), 95
    V = [(200 + R * math.cos(math.radians(a)), 190 + R * math.sin(math.radians(a)))
         for a in (-90, -30, 30, 90, 150, 210)]
    A, B, C = V[0], V[1], V[2]
    f.circle(O[0], O[1], R, "none", DARK, 1.8)
    rin = R * math.sqrt(3) / 2
    inner = [(200 + rin * math.cos(math.radians(a)), 190 + rin * math.sin(math.radians(a)))
             for a in range(0, 360, 5)]
    f.poly(inner, "none", GREY, 1.4, dash="5 4")
    f.poly(V, "none", DARK, 2.2)
    f.line(O[0], O[1], B[0], B[1], RED, 2.0)
    f.text(258, 132, "R", 11, RED)
    M = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    f.line(O[0], O[1], M[0], M[1], GREY, 1.6, dash="5 4")
    f.right_angle(M[0], M[1], 120, 210, 8)
    f.text(210, 152, "r", 11, GREY)
    f.text(231, 100, "a/2", 11, DARK, anchor="middle")
    f.arc(O[0], O[1], 32, -30, 30, PURP, 2.0)
    f.text(246, 190, "60°", 12, PURP, anchor="middle")
    for p, name, off in [(O, "O", (12, 4)), (A, "A", (0, -12)), (B, "B", (16, 0)),
                         (C, "C", (16, 8))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(200, 330, "中心角 60°=外角；边心距 r=√3/2·R", 12, DARK, anchor="middle")
    f.text(200, 354, "R²=r²+(a/2)²；S=½×周长×r", 12, RED, anchor="middle", weight="bold")
    # ② 正方形
    f.text(600, 30, "② 正方形：对角线即直径", 14, DARK, anchor="middle", weight="bold")
    O2, R2 = (600, 190), 80
    S = [(600 + R2 * math.cos(math.radians(a)), 190 + R2 * math.sin(math.radians(a)))
         for a in (225, 315, 45, 135)]
    A2, B2, C2, D2 = S[3], S[2], S[1], S[0]
    f.circle(O2[0], O2[1], R2, "none", DARK, 1.8)
    f.poly(S, "none", DARK, 2.2)
    f.line(A2[0], A2[1], C2[0], C2[1], GREY, 1.4)
    f.line(B2[0], B2[1], D2[0], D2[1], GREY, 1.4)
    f.text(600, 100, "2R=√2·a", 11, GREY, anchor="middle")
    f.line(O2[0], O2[1], C2[0], C2[1], GREY, 1.6, dash="5 4")
    f.right_angle(C2[0], C2[1], 180, 90, 8)
    f.text(626, 178, "r=a/2", 11, GREY, anchor="middle")
    f.text(600, 288, "a", 12, DARK, anchor="middle")
    for p, name, off in [(O2, "O", (0, -20)), (A2, "A", (-14, -8)), (B2, "B", (14, -8)),
                         (C2, "C", (14, 20)), (D2, "D", (-14, 20))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(600, 330, "对角线=2R=√2·a，边心距 r=a/2", 12, DARK, anchor="middle")
    f.text(600, 354, "面积=½×周长×r=a²", 12, RED, anchor="middle", weight="bold")
    f.save("regular-polygon.svg")


if __name__ == "__main__":
    fig_circle_perp()
    fig_central_inscribed()
    fig_circle_position()
    fig_tangent()
    fig_arc_cone()
    fig_regular_poly()
