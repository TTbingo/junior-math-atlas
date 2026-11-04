# -*- coding: utf-8 -*-
"""生成「方程与不等式」数形结合配图 8 张 → content/media/

所有文本统一经 esc() 转义：SVG 是 XML，文本里的裸 < > & 会导致整图解析失败。
图上的数字必须与对应知识点正文严格一致（见各函数 docstring）。
"""
import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "content" / "media"

DARK = "#2d3748"; BLUE = "#2b6cb0"; BLUEF = "#ebf4ff"
YEL = "#b7791f"; YELF = "#fefcbf"
GRN = "#2f855a"; GRNF = "#f0fff4"
RED = "#c53030"; GREY = "#4a5568"; GREYL = "#edf2f7"
GREYM = "#a0aec0"; WHITE = "#ffffff"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Fig:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.parts = [f'<rect width="{w}" height="{h}" fill="{WHITE}"/>']

    def svg(self, label):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'width="{self.w}" height="{self.h}" role="img" aria-label="{esc(label)}">')
        return head + "".join(self.parts) + "</svg>"

    def rect(self, x, y, w, h, fill, stroke, sw=1.5, dash=None, rx=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        r = f' rx="{rx}"' if rx is not None else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
                          f'stroke="{stroke}" stroke-width="{sw}"{d}{r}/>')

    def line(self, x1, y1, x2, y2, stroke, sw=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
                          f'stroke-width="{sw}"{d}/>')

    def circle(self, cx, cy, r, fill, stroke, sw=1.5):
        self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" '
                          f'stroke-width="{sw}"/>')

    def poly(self, pts, fill):
        p = " ".join(f"{x},{y}" for x, y in pts)
        self.parts.append(f'<polygon points="{p}" fill="{fill}"/>')

    def path(self, d, stroke, sw=2.0, fill="none"):
        self.parts.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, s, size=13, fill=DARK, anchor="middle", weight=None):
        w = f' font-weight="{weight}"' if weight else ""
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}"{w} fill="{fill}" '
                          f'text-anchor="{anchor}">{esc(s)}</text>')

    def arrow_head(self, x, y, dx, dy, fill, size=8):
        n = math.hypot(dx, dy) or 1
        ux, uy = dx / n, dy / n
        px, py = -uy, ux
        p1 = (x, y)
        p2 = (x - ux * size + px * size * 0.6, y - uy * size + py * size * 0.6)
        p3 = (x - ux * size - px * size * 0.6, y - uy * size - py * size * 0.6)
        self.poly([p1, p2, p3], fill)

    def save(self, name, label):
        (OUT / name).write_text(self.svg(label), encoding="utf-8", newline="\n")
        print("ok", name)


# ---------------------------------------------------------------- 通用部件

def balance(f, cx, yb, pan_w=76):
    """天平：横梁 + 两盘 + 支架。盘面在 yb+24，物品底边贴 yb+24。"""
    f.line(cx - 70, yb, cx + 70, yb, DARK, 3)
    for sx in (-70, 70):
        f.line(cx + sx, yb, cx + sx, yb + 28, GREY, 1.2)
    f.rect(cx - 70 - pan_w / 2, yb + 28, pan_w, 18, GREYL, GREY, 1.5, rx=3)
    f.rect(cx + 70 - pan_w / 2, yb + 28, pan_w, 18, GREYL, GREY, 1.5, rx=3)
    f.poly([(cx, yb + 2), (cx - 12, yb + 44), (cx + 12, yb + 44)], DARK)
    f.line(cx - 22, yb + 44, cx + 22, yb + 44, DARK, 3)


def weight(f, cx, cy, r=4.5):
    f.circle(cx, cy, r, GREYM, GREY, 1)


# ---------------------------------------------------------------- 图 1：天平

def fig_balance():
    """m1-02-01 一元一次方程。对齐正文实验：左盘物体+3砝码 vs 右盘5砝码。"""
    f = Fig(560, 300)
    # 天平①
    balance(f, 170, 50)
    f.rect(70, 66, 14, 12, YELF, YEL, 1.8)          # 未知重量的物体
    for x in (96, 108, 120):
        weight(f, x, 73.5)
    for x in (216, 228, 240, 252, 264):
        weight(f, x, 73.5)
    f.text(170, 124, "x + 3 = 5", 15, RED, weight="600")
    # 竖箭头
    f.line(170, 136, 170, 164, BLUE, 2)
    f.arrow_head(170, 172, 0, 1, BLUE)
    f.text(184, 156, "两边同拿走 3 个砝码", 12, GREY, anchor="start")
    # 天平②
    balance(f, 170, 180)
    f.rect(70, 196, 14, 12, YELF, YEL, 1.8)
    for x in (232, 248):
        weight(f, x, 203.5)
    f.text(170, 254, "x = 2", 15, RED, weight="600")
    # 右侧：两种记法对照
    f.rect(320, 60, 215, 200, WHITE, GREYM, 1.5, rx=8)
    f.text(427, 88, "同一个动作，两种记法", 13, DARK, weight="600")
    f.text(427, 120, "x + 3 = 5", 14, RED, weight="600")
    f.text(427, 146, "两边同减 3", 12, GREY)
    f.text(427, 172, "x = 5 − 3", 13, DARK)
    f.text(427, 204, "x = 2", 14, RED, weight="600")
    f.text(427, 234, "「移项变号」", 12, GREY)
    f.text(427, 250, "就是两边同减的速记", 12, GREY)
    f.save("balance-scale.svg",
           "上下两架天平：第一架左盘物体加三个砝码对右盘五个砝码，两边同时拿走三个砝码后仍平衡，"
           "第二架左盘只剩物体、右盘两个砝码；右侧写出 x 加 3 等于 5 变形到 x 等于 2 的两种记法")


# ---------------------------------------------------------------- 图 2：双天平

def fig_two_balance():
    """m1-02-02 二元一次方程组。对齐正文：3大+2小=400，2大+3小=350。"""
    f = Fig(560, 260)
    # 图例
    f.circle(70, 22, 8, BLUEF, BLUE, 1.8)
    f.text(88, 26, "大球", 12, GREY, anchor="start")
    f.circle(140, 22, 5.5, GRNF, GRN, 1.8)
    f.text(154, 26, "小球", 12, GREY, anchor="start")

    def items(cx, yb, xs_big, xs_small):
        for dx in xs_big:
            f.circle(cx + dx, yb + 20, 8, BLUEF, BLUE, 1.8)
        for dx in xs_small:
            f.circle(cx + dx, yb + 22.5, 5.5, GRNF, GRN, 1.8)

    def block(cx, yb, s):
        f.rect(cx + 44, yb + 12, 52, 16, GREYL, GREY, 1.5, rx=2)
        f.text(cx + 70, yb + 24, s, 11, DARK)

    # 天平① 3 大 + 2 小
    balance(f, 170, 45, pan_w=92)
    items(170, 45, (-106, -89, -72), (-56, -44))
    block(170, 45, "400 克")
    f.text(170, 108, "① 3 个大球 + 2 个小球 = 400 克", 13, DARK)
    # 天平② 2 大 + 3 小
    balance(f, 170, 165, pan_w=92)
    items(170, 165, (-104, -86), (-68, -57, -46))
    block(170, 165, "350 克")
    f.text(170, 228, "② 2 个大球 + 3 个小球 = 350 克", 13, DARK)
    # 结果面板
    f.rect(385, 55, 160, 180, WHITE, GREYM, 1.5, rx=8)
    f.text(465, 80, "把 ① 的两边", 12, GREY)
    f.text(465, 98, "分别减去 ② 的两边", 12, GREY)
    f.text(465, 126, "(3−2) 个大球", 13)
    f.text(465, 146, "(2−3) 个小球", 13)
    f.text(465, 166, "400 − 350 克", 13)
    f.text(465, 194, "1 大 − 1 小 = 50 克", 13, RED, weight="600")
    f.text(465, 220, "大球比小球重 50 克", 12, DARK)
    # 引导箭头
    f.line(268, 75, 378, 100, GREYM, 1.5)
    f.arrow_head(382, 101, 1, 0.25, GREYM)
    f.line(268, 195, 378, 195, GREYM, 1.5)
    f.arrow_head(382, 195, 1, 0, GREYM)
    f.save("two-balance.svg",
           "两个天平上下排列：三个大球加两个小球对四百克，两个大球加三个小球对三百五十克，"
           "两次读数相减得一个大球减一个小球等于五十克")


# ---------------------------------------------------------------- 图 3：配方法

def fig_completing_square():
    """m1-02-03 一元二次方程。对齐正文：x²+6x=7 补 9 → (x+3)²=16。"""
    f = Fig(560, 300)
    # 左：缺角 L 形
    f.text(120, 36, "x² + 6x：一个缺角的 L 形", 14, DARK, weight="600")
    f.rect(40, 80, 160, 160, "none", GREYM, 1.2, dash="5 4")
    f.rect(40, 80, 100, 100, BLUEF, BLUE, 1.5)
    f.text(90, 135, "x²", 15, BLUE)
    f.rect(140, 80, 60, 100, YELF, YEL, 1.5)
    f.text(170, 135, "3x", 13, YEL)
    f.rect(40, 180, 100, 60, YELF, YEL, 1.5)
    f.text(90, 213, "3x", 13, YEL)
    f.rect(140, 180, 60, 60, "none", RED, 1.5, dash="4 3")
    f.text(170, 214, "9", 14, RED)
    f.text(90, 74, "x", 12, GREY)
    f.text(170, 74, "3", 12, GREY)
    f.text(32, 134, "x", 12, GREY)
    f.text(32, 214, "3", 12, GREY)
    f.text(120, 270, "x² + 6x = 7", 14, RED, weight="600")
    # 中：箭头
    f.line(214, 160, 308, 160, RED, 2)
    f.arrow_head(316, 160, 1, 0, RED)
    f.text(260, 146, "补上 9", 12, RED)
    # 右：完整大正方形
    f.text(410, 36, "补上 9：恰好拼成边长 x + 3", 14, DARK, weight="600")
    f.rect(330, 80, 160, 160, "none", DARK, 2)
    f.rect(330, 80, 100, 100, BLUEF, BLUE, 1.5)
    f.text(380, 135, "x²", 15, BLUE)
    f.rect(430, 80, 60, 100, YELF, YEL, 1.5)
    f.text(460, 135, "3x", 13, YEL)
    f.rect(330, 180, 100, 60, YELF, YEL, 1.5)
    f.text(380, 213, "3x", 13, YEL)
    f.rect(430, 180, 60, 60, GRNF, GRN, 1.5)
    f.text(460, 214, "9", 14, GRN)
    f.text(380, 74, "x", 12, GREY)
    f.text(460, 74, "3", 12, GREY)
    f.text(322, 134, "x", 12, GREY)
    f.text(322, 214, "3", 12, GREY)
    f.text(410, 270, "(x+3)² = x² + 6x + 9 = 16", 13, RED, weight="600")
    f.save("completing-square.svg",
           "左边 L 形由 x 平方正方形和两条 3x 长条组成缺一角，右边补上 3 乘 3 的角拼成边长 x 加 3 的大正方形，"
           "方程由 x 平方加 6x 等于 7 变为 x 加 3 的平方等于 16")


# ---------------------------------------------------------------- 图 4：韦达数轴

def fig_vieta():
    """m1-02-04 判别式与韦达。三情形：同正 / 异号 / 同负。"""
    f = Fig(560, 245)
    px = lambda v: 70 + 40 * (v + 4)   # -4..4 → 70..390
    rows = [
        (70, "x² − 5x + 6 = 0", (2, 3),
         ("x₁x₂ = 6 > 0：同侧", "x₁+x₂ = 5 > 0：同正")),
        (140, "x² + x − 6 = 0", (-3, 2),
         ("x₁x₂ = −6 < 0：异侧", "一正一负，看和的符号")),
        (210, "x² + 5x + 6 = 0", (-3, -2),
         ("x₁x₂ = 6 > 0：同侧", "x₁+x₂ = −5 < 0：同负")),
    ]
    for y, eq, roots, note in rows:
        f.text(70, y - 22, eq, 13, DARK, anchor="start")
        f.line(70, y, 390, y, GREY, 1.5)
        for v in range(-4, 5):
            tall = 5 if v == 0 else 4
            f.line(px(v), y - tall, px(v), y + tall, GREY, 1.2)
            f.text(px(v), y + 18, str(v), 11, GREY)
        f.text(402, y - 4, note[0], 12, BLUE, anchor="start")
        f.text(402, y + 16, note[1], 12, DARK, anchor="start")
        f.circle(px(roots[0]), y, 5, BLUE, BLUE, 1)
        f.circle(px(roots[1]), y, 5, BLUE, BLUE, 1)
        f.text(px(roots[0]), y - 12, "x₁", 12, BLUE)
        f.text(px(roots[1]), y - 12, "x₂", 12, BLUE)
    f.save("vieta-numberline.svg",
           "三条数轴各标出一个一元二次方程的两个根：第一条两根都在零右侧，第二条两根分居零两侧，"
           "第三条两根都在零左侧，右侧文字说明积与和的符号怎样决定两根位置")


# ---------------------------------------------------------------- 图 5：乘负翻折

def fig_flip():
    """m1-02-06 不等式。对齐正文实验：2、3、4 翻折到 −2、−3、−4。"""
    f = Fig(560, 258)
    px = lambda v: 280 + 40 * v        # -5..5 → 80..480
    f.text(280, 22, "乘以 −1：每个点翻到原点对面", 13, DARK, weight="600")
    # 图例
    # 数轴
    y_axis = 140
    f.line(80, y_axis, 480, y_axis, GREY, 1.5)
    for v in range(-5, 6):
        tall = 5 if v == 0 else 4
        f.line(px(v), y_axis - tall, px(v), y_axis + tall, GREY, 1.2)
        f.text(px(v), y_axis + 18, str(v), 11, GREY)
    # 原来的点
    for v in (2, 3, 4):
        f.circle(px(v), 95, 5, BLUE, BLUE, 1)
        f.text(px(v), 114, str(v), 12, BLUE)
    # 翻折后的点
    for v in (-2, -3, -4):
        f.circle(px(v), 185, 5, RED, RED, 1)
        f.text(px(v), 203, str(v), 12, RED)
    # 翻折曲线（都经过原点上方，体现关于原点对称）
    curves = [((360, 101), (340, 60), (220, 60), (203, 176)),
              ((400, 101), (370, 48), (190, 48), (161, 176)),
              ((440, 101), (400, 36), (160, 36), (119, 176))]
    for p0, c1, c2, p3 in curves:
        f.path(f"M {p0[0]} {p0[1]} C {c1[0]} {c1[1]}, {c2[0]} {c2[1]}, {p3[0]} {p3[1]}", RED, 1.6)
        f.arrow_head(p3[0], p3[1], p3[0] - c2[0], p3[1] - c2[1], RED, 7)
    f.text(280, 220, "蓝点 = 乘 −1 前的点，红点 = 翻折后的点，箭头 = 关于原点对称", 12, GREY)
    f.text(280, 242, "乘 −1 前从左到右：2 < 3 < 4；乘 −1 后从左到右：−4 < −3 < −2 —— 顺序整个反过来", 12, DARK)
    f.save("flip-numberline.svg",
           "一条数轴，上方 2、3、4 三个蓝点经曲线连到下方负二、负三、负四三个红点，"
           "曲线经过原点附近，下方注明乘负一前后从左到右的顺序完全相反")


# ---------------------------------------------------------------- 图 6：解集数轴

def fig_solution():
    """m1-02-06 例 2。对齐例题：2x−1>3 与 x−3≤1 → 2<x≤4。"""
    f = Fig(560, 265)
    px = lambda v: 120 + 58 * v         # 0..5 → 120..410
    rows = [
        (60, "① 2x − 1 > 3，解得 x > 2", BLUE, "open"),
        (130, "② x − 3 ≤ 1，解得 x ≤ 4", GRN, "closed"),
        (200, "同一条数轴上取重叠：2 < x ≤ 4", RED, "both"),
    ]
    for y, label, color, kind in rows:
        f.text(120, y - 18, label, 13, color if kind == "both" else DARK,
               anchor="start", weight="600" if kind == "both" else None)
        f.line(120, y, 410, y, GREY, 1.5)
        for v in range(0, 6):
            f.line(px(v), y - 4, px(v), y + 4, GREY, 1.2)
            f.text(px(v), y + 18, str(v), 11, GREY)
        if kind == "open":
            f.line(px(2), y, 404, y, BLUE, 4)
            f.arrow_head(414, y, 1, 0, BLUE, 10)
            f.circle(px(2), y, 5, WHITE, BLUE, 2)
        elif kind == "closed":
            f.line(126, y, px(4), y, GRN, 4)
            f.arrow_head(116, y, -1, 0, GRN, 10)
            f.circle(px(4), y, 5, GRN, GRN, 1.5)
        else:
            f.line(px(2), y, px(4), y, RED, 4.5)
            f.circle(px(2), y, 5, WHITE, RED, 2)
            f.circle(px(4), y, 5, RED, RED, 1.5)
    f.text(265, 246, "空心 = 取不到，实心 = 取得到；重叠段照抄两头的开闭", 12, GREY)
    f.save("solution-numberline.svg",
           "三条上下对齐的数轴：第一条在 2 处空心圆向右粗线表示 x 大于 2，第二条在 4 处实心圆向左粗线表示 "
           "x 小于等于 4，第三条画出重叠部分，从 2 空心到 4 实心")


# ---------------------------------------------------------------- 图 7：行程线段

def fig_motion():
    """m1-02-07 例 1 相遇 + 通用追及。对齐例 1：60 千米、2(x+10)+2x=60。"""
    f = Fig(560, 300)
    # 上幅：相遇（同一条路上相向而行）
    f.text(280, 28, "相遇：两人走的路程之和 = 全程", 14, DARK, weight="600")
    f.circle(70, 75, 4.5, DARK, DARK, 1)
    f.text(70, 60, "A", 12, DARK)
    f.circle(510, 75, 4.5, DARK, DARK, 1)
    f.text(510, 60, "B", 12, DARK)
    f.circle(310, 75, 4.5, RED, RED, 1)
    f.text(310, 60, "相遇点", 12, RED)
    f.line(78, 75, 296, 75, BLUE, 2.5)
    f.arrow_head(302, 75, 1, 0, BLUE)
    f.text(185, 57, "甲：2(x+10) 千米", 12, BLUE)
    f.line(502, 75, 324, 75, GRN, 2.5)
    f.arrow_head(318, 75, -1, 0, GRN)
    f.text(415, 57, "乙：2x 千米", 12, GRN)
    f.line(70, 95, 510, 95, GREY, 1)
    f.line(70, 89, 70, 101, GREY, 1)
    f.line(510, 89, 510, 101, GREY, 1)
    f.text(280, 113, "全程 60 千米", 12, GREY)
    f.text(280, 140, "2(x+10) + 2x = 60", 13, RED, weight="600")
    # 下幅：追及（两条车道，同一终点）
    f.text(280, 172, "追及：快者多走的路 = 原来领先的差距", 14, DARK, weight="600")
    f.line(446, 190, 446, 248, GREYM, 1.2, dash="3 3")
    f.text(452, 184, "追上点", 12, RED)
    # 乙在上道
    f.circle(250, 202, 4.5, GRN, GRN, 1)
    f.text(250, 191, "乙", 12, GRN)
    f.line(258, 202, 430, 202, GRN, 2.5)
    f.arrow_head(438, 202, 1, 0, GRN)
    f.text(350, 192, "乙：v₂t", 12, GRN)
    # 甲在下道
    f.circle(70, 238, 4.5, BLUE, BLUE, 1)
    f.text(70, 227, "甲", 12, BLUE)
    f.line(78, 238, 430, 238, BLUE, 2.5)
    f.arrow_head(438, 238, 1, 0, BLUE)
    f.text(300, 228, "甲：v₁t", 12, BLUE)
    # 领先差距括号
    f.line(70, 258, 250, 258, GREY, 1)
    f.line(70, 252, 70, 264, GREY, 1)
    f.line(250, 252, 250, 264, GREY, 1)
    f.text(160, 276, "乙领先 s₀", 12, GREY)
    f.text(450, 276, "v₁t = s₀ + v₂t", 13, RED, weight="600")
    f.save("motion-diagram.svg",
           "上下两幅线段图：上幅 A、B 两地相距 60 千米两人相向而行中途相遇，两段路程相加等于全程；"
           "下幅两条车道，乙在前领先一段距离，甲在后追到同一终点，甲走的路程等于乙走的路程加领先的差距")


# ---------------------------------------------------------------- 图 8：整数解

def fig_integer():
    """m1-02-08 不等式应用。对齐正文 why：租车 4≤x≤6，可行 x=4,5,6。"""
    f = Fig(560, 215)
    px = lambda v: 130 + 55 * v          # 0..6 → 130..460
    f.text(295, 26, "解集是一整段，可行的只有整数点", 14, DARK, weight="600")
    f.text(468, 78, "x（大巴数）", 12, GREY, anchor="start")
    y = 95
    f.line(130, y, 460, y, GREY, 1.5)
    for v in range(0, 7):
        f.line(px(v), y - 4, px(v), y + 4, GREY, 1.2)
        f.text(px(v), y + 18, str(v), 11, GREY)
    f.text(122, y + 4, "解集：", 12, BLUE, anchor="end")
    f.line(px(4), y, px(6), y, BLUE, 4.5)
    f.circle(px(4), y, 5, BLUE, BLUE, 1.5)
    f.circle(px(6), y, 5, BLUE, BLUE, 1.5)
    # 整数点行
    y2 = 150
    f.text(122, y2 + 4, "整数点：", 12, GREY, anchor="end")
    for v in range(0, 7):
        if 4 <= v <= 6:
            f.circle(px(v), y2, 4.5, RED, RED, 1.5)
        else:
            f.circle(px(v), y2, 4.5, WHITE, GREYM, 1.5)
    f.text(px(5), y2 + 20, "x = 4、5、6", 12, RED)
    f.text(295, 196, "不等式的解集是连续的，但方案数是整数——必须把整段筛成点", 12, GREY)
    f.save("integer-solutions.svg",
           "一条 0 到 6 的数轴：上方从 4 到 6 画粗线段表示解集，下方一行圆点中 4、5、6 为实心红点表示可行方案，"
           "0 到 3 为空心灰点不可行")


if __name__ == "__main__":
    fig_balance()
    fig_two_balance()
    fig_completing_square()
    fig_vieta()
    fig_flip()
    fig_solution()
    fig_motion()
    fig_integer()
    print("全部生成完毕 →", OUT)
