"""生成代数「函数」部分的 7 张配图。

全部按数学函数采样出点后连成折线，避免手写坐标造成的形状偏差。
用法：python tools/gen_algebra_figs.py
"""
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "content" / "media"
FONT = "Microsoft YaHei, PingFang SC, sans-serif"
BLUE, GREEN, RED, GRAY, DARK = "#2b6cb0", "#2f855a", "#c53030", "#718096", "#2d3748"


class Plane:
    """像素坐标与数学坐标的换算，一个对象对应一张图的坐标系。"""

    def __init__(self, ox, oy, ux, uy=None):
        self.ox, self.oy, self.ux = ox, oy, ux
        self.uy = ux if uy is None else uy

    def X(self, x):
        return self.ox + x * self.ux

    def Y(self, y):
        return self.oy - y * self.uy

    def axes(self, xmin, xmax, ymin, ymax, xticks=(), yticks=(), xname="x", yname="y"):
        """画两条带箭头的坐标轴，刻度与轴名可选。"""
        out = []
        x0, x1 = self.X(xmin), self.X(xmax)
        y0, y1 = self.Y(ymin), self.Y(ymax)
        out.append(f'<line x1="{x0:.1f}" y1="{self.oy}" x2="{x1:.1f}" y2="{self.oy}" stroke="{DARK}" stroke-width="1.4"/>')
        out.append(f'<polygon points="{x1:.1f},{self.oy} {x1-8:.1f},{self.oy-4} {x1-8:.1f},{self.oy+4}" fill="{DARK}"/>')
        out.append(f'<line x1="{self.ox}" y1="{y0:.1f}" x2="{self.ox}" y2="{y1:.1f}" stroke="{DARK}" stroke-width="1.4"/>')
        out.append(f'<polygon points="{self.ox},{y1:.1f} {self.ox-4},{y1+8:.1f} {self.ox+4},{y1+8:.1f}" fill="{DARK}"/>')
        for t in xticks:
            px = self.X(t)
            out.append(f'<line x1="{px:.1f}" y1="{self.oy-3}" x2="{px:.1f}" y2="{self.oy+3}" stroke="{DARK}" stroke-width="1"/>')
            out.append(f'<text x="{px:.1f}" y="{self.oy+16}" font-size="11" fill="{GRAY}" text-anchor="middle" font-family="{FONT}">{t:g}</text>')
        for t in yticks:
            py = self.Y(t)
            out.append(f'<line x1="{self.ox-3}" y1="{py:.1f}" x2="{self.ox+3}" y2="{py:.1f}" stroke="{DARK}" stroke-width="1"/>')
            out.append(f'<text x="{self.ox-7}" y="{py+4:.1f}" font-size="11" fill="{GRAY}" text-anchor="end" font-family="{FONT}">{t:g}</text>')
        out.append(f'<text x="{x1+2:.1f}" y="{self.oy+18}" font-size="12" fill="{DARK}" font-family="{FONT}">{xname}</text>')
        out.append(f'<text x="{self.ox+8}" y="{y1-2:.1f}" font-size="12" fill="{DARK}" font-family="{FONT}">{yname}</text>')
        out.append(f'<text x="{self.ox-8}" y="{self.oy+15}" font-size="11" fill="{GRAY}" text-anchor="end" font-family="{FONT}">O</text>')
        return "\n".join(out)

    def curve(self, f, a, b, color, n=90, width=2.0, dash=None):
        pts = []
        step = (b - a) / n
        for i in range(n + 1):
            x = a + i * step
            pts.append(f"{self.X(x):.1f},{self.Y(f(x)):.1f}")
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="{width}"{d}/>'

    def line(self, f, a, b, color, width=2.0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<line x1="{self.X(a):.1f}" y1="{self.Y(f(a)):.1f}" '
                f'x2="{self.X(b):.1f}" y2="{self.Y(f(b)):.1f}" stroke="{color}" stroke-width="{width}"{d}/>')

    def dot(self, x, y, color, r=4, label=None, dx=8, dy=-8, size=12, anchor="start"):
        out = [f'<circle cx="{self.X(x):.1f}" cy="{self.Y(y):.1f}" r="{r}" fill="{color}"/>']
        if label:
            out.append(f'<text x="{self.X(x)+dx:.1f}" y="{self.Y(y)+dy:.1f}" font-size="{size}" '
                       f'fill="{color}" text-anchor="{anchor}" font-family="{FONT}">{esc(label)}</text>')
        return "\n".join(out)


def wrap(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{label}">\n  <rect width="{w}" height="{h}" fill="#ffffff"/>\n'
            f'{body}\n</svg>\n')


def esc(s):
    """SVG 是 XML：文本里的 & < > 必须转义，否则整张图解析失败。"""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def txt(x, y, s, size=12, color=DARK, anchor="start", weight=None):
    w = f' font-weight="{weight}"' if weight else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}"{w} font-family="{FONT}">{esc(s)}</text>')


# ---------------------------------------------------------------- 图 1 坐标系
def fig_coordinate():
    p = Plane(200, 220, 28)
    b = [p.axes(-5, 7, -4, 5, xticks=(-4, -2, 2, 4, 6), yticks=(-3, -1, 1, 3, 4))]
    b.append(txt(360, 70, "第一象限", 11, GRAY))
    b.append(txt(70, 70, "第二象限", 11, GRAY))
    b.append(txt(70, 350, "第三象限", 11, GRAY))
    b.append(txt(360, 350, "第四象限", 11, GRAY))
    # A(3,2) 的两段距离虚线
    b.append(f'<line x1="{p.X(3):.1f}" y1="{p.oy}" x2="{p.X(3):.1f}" y2="{p.Y(2):.1f}" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    b.append(f'<line x1="{p.ox}" y1="{p.Y(2):.1f}" x2="{p.X(3):.1f}" y2="{p.Y(2):.1f}" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    b.append(p.dot(3, 2, BLUE, 4.5, "A(3，2)", 8, -8))
    b.append(p.dot(-2, 1, GREEN, 4.5, "B(−2，1)", -8, -8, anchor="end"))
    b.append(p.dot(0, -3, RED, 4.5, "C(0，−3)", 8, 14))
    b.append(txt(240, 372, "A 的横坐标 3：向右 3 格；纵坐标 2：向上 2 格", 11, BLUE, "middle"))
    return wrap(480, 400, "\n".join(b),
                "平面直角坐标系分成四个象限，标出点 A（3，2）及其到两轴的虚线、点 B（负2，1）、点 C（0，负3）")


# ---------------------------------------------------------------- 图 2 一次函数
def fig_linear():
    p = Plane(200, 240, 26)
    b = [p.axes(-4, 7, -3, 6, xticks=(-2, 2, 4, 6), yticks=(-1, 1, 3, 5))]
    b.append(p.line(lambda x: 2 * x + 1, -2, 2.9, BLUE))
    b.append(p.line(lambda x: -x + 3, -2.8, 5.6, GREEN))
    b.append(p.dot(0, 1, BLUE, 3.5))
    b.append(p.dot(0, 3, GREEN, 3.5))
    b.append(txt(p.X(3.2), p.Y(5.2), "y = 2x + 1", 12, BLUE))
    b.append(txt(p.X(4.2), p.Y(2.2), "y = −x + 3", 12, GREEN))
    b.append(txt(p.X(-3.6), p.Y(-2.4), "k > 0 上升", 11, BLUE))
    b.append(txt(p.X(2.2), p.Y(-2.4), "k < 0 下降", 11, GREEN))
    b.append(txt(p.X(0.6), p.Y(5.4), "与 y 轴交点纵坐标就是 b", 11, GRAY))
    return wrap(480, 400, "\n".join(b),
                "两条直线 y 等于 2x 加 1 与 y 等于负 x 加 3，分别与 y 轴交于 1 和 3，前者上升后者下降")


# ---------------------------------------------------------------- 图 3 方案比较
def fig_compare():
    p = Plane(110, 330, 2.6, 6.0)
    b = [p.axes(-3, 133, -3, 50, xticks=(50, 100), yticks=(20, 30, 40))]
    b.append(p.line(lambda x: 0.3 * x, 0, 128, BLUE))
    b.append(p.line(lambda x: 20 + 0.1 * x, 0, 128, GREEN))
    # 交点竖虚线
    b.append(f'<line x1="{p.X(100):.1f}" y1="{p.oy}" x2="{p.X(100):.1f}" y2="{p.Y(30):.1f}" stroke="{GRAY}" stroke-width="1" stroke-dasharray="4 3"/>')
    b.append(p.dot(100, 30, RED, 4, "(100，30)", 12, 22))
    b.append(f'<line x1="{p.X(70):.1f}" y1="{p.Y(46):.1f}" x2="{p.X(78):.1f}" y2="{p.Y(46):.1f}" stroke="{BLUE}" stroke-width="2"/>')
    b.append(txt(p.X(80), p.Y(46) + 4, "y = 0.3x（A 方案）", 11, BLUE))
    b.append(f'<line x1="{p.X(70):.1f}" y1="{p.Y(41):.1f}" x2="{p.X(78):.1f}" y2="{p.Y(41):.1f}" stroke="{GREEN}" stroke-width="2"/>')
    b.append(txt(p.X(80), p.Y(41) + 4, "y = 20 + 0.1x（B 方案）", 11, GREEN))
    b.append(txt(240, 388, "交点左侧 A 更省，右侧 B 更省", 11, DARK, "middle"))
    return wrap(480, 400, "\n".join(b),
                "两条直线 y 等于 0.3x 与 y 等于 20 加 0.1x 在（100，30）相交，交点左侧第一条更低、右侧第二条更低")


# ---------------------------------------------------------------- 图 4 反比例
def fig_inverse():
    p = Plane(200, 240, 26)
    b = [p.axes(-6, 8, -6, 6, xticks=(-4, -2, 2, 4, 6), yticks=(-4, -2, 2, 4))]
    b.append(p.curve(lambda x: 6 / x, 1.0, 8.4, BLUE))
    b.append(p.curve(lambda x: 6 / x, -8.4, -1.0, BLUE))
    b.append(f'<rect x="{p.ox}" y="{p.Y(3):.1f}" width="{p.X(2)-p.ox:.1f}" height="{p.oy-p.Y(3):.1f}" '
             f'fill="{BLUE}" fill-opacity="0.12" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    b.append(p.dot(2, 3, BLUE, 4.5))
    b.append(txt(p.X(2) + 8, p.Y(3) - 8, "P(2，3)", 12, BLUE))
    b.append(f'<line x1="{p.X(2.9):.1f}" y1="{p.Y(4.9):.1f}" x2="{p.X(2.1):.1f}" y2="{p.Y(3.3):.1f}" '
             f'stroke="{GRAY}" stroke-width="1" stroke-dasharray="3 3"/>')
    b.append(txt(p.X(3.0), p.Y(5.1), "矩形面积 = |k| = 6", 11, BLUE))
    b.append(txt(p.X(5.0), p.Y(3.6), "y = 6/x", 12, BLUE))
    b.append(txt(240, 408, "两支关于原点对称，永远不与坐标轴相交", 11, GRAY, "middle"))
    return wrap(460, 420, "\n".join(b),
                "反比例函数 y 等于 x 分之 6 的两支双曲线，第一象限上点 P（2，3）与两轴围成面积为 6 的矩形")


# ---------------------------------------------------------------- 图 5 抛物线基本性质
def fig_parabola():
    p = Plane(200, 250, 24, 22)
    b = [p.axes(-3, 7, -5, 6, xticks=(2, 4, 6), yticks=(-4, -2, 2, 4))]
    b.append(f'<line x1="{p.X(1):.1f}" y1="{p.Y(6):.1f}" x2="{p.X(1):.1f}" y2="{p.Y(-5):.1f}" '
             f'stroke="{GRAY}" stroke-width="1" stroke-dasharray="5 4"/>')
    b.append(p.curve(lambda x: x * x - 2 * x - 3, -2.0, 4.0, BLUE))
    b.append(p.dot(1, -4, RED, 4.5))
    b.append(txt(p.X(1) + 10, p.Y(-4) + 6, "顶点 (1，−4)", 12, RED))
    b.append(p.dot(-1, 0, GREEN, 4))
    b.append(txt(p.X(-1) - 8, p.Y(0) - 10, "(−1，0)", 12, GREEN, "end"))
    b.append(p.dot(3, 0, GREEN, 4))
    b.append(txt(p.X(3) + 8, p.Y(0) - 10, "(3，0)", 12, GREEN))
    b.append(p.dot(0, -3, GREEN, 3.5))
    b.append(txt(p.X(1) + 10, p.Y(6) + 14, "对称轴 x = 1", 11, GRAY))
    b.append(txt(p.X(3.9), p.Y(2.2), "y = x² − 2x − 3", 12, BLUE))
    b.append(txt(56, 402, "开口向上：a > 0", 11, BLUE))
    return wrap(460, 420, "\n".join(b),
                "抛物线 y 等于 x 平方减 2x 减 3，开口向上，对称轴 x 等于 1，顶点（1，负4），与 x 轴交于（负1，0）和（3，0）")


# ---------------------------------------------------------------- 图 6 判别式三种情形
def fig_roots():
    cols = [(95, "Δ > 0：两个交点", lambda x: x * x - 2 * x - 2, 16, "两个不等实根"),
            (280, "Δ = 0：一个交点", lambda x: x * x - 2 * x + 1, 0, "两个相等实根"),
            (465, "Δ < 0：没有交点", lambda x: x * x - 2 * x + 3, -8, "没有实根")]
    b = []
    for cx, title, f, delta, note in cols:
        p = Plane(cx, 130, 13)
        b.append(txt(cx, 24, title, 12, DARK, "middle", 600))
        b.append(p.axes(-2.4, 2.4, -3.2, 6.0, xticks=(1,), yticks=()))
        b.append(p.curve(f, -0.85, 2.85, BLUE))
        b.append(txt(cx, 214, note, 11, RED, "middle"))
        b.append(txt(cx, 234, f"Δ = {delta}", 11, GRAY, "middle"))
    return wrap(560, 248, "\n".join(b),
                "三个小坐标系并列：判别式大于零时抛物线与 x 轴有两个交点，等于零时相切于一点，小于零时没有交点")


# ---------------------------------------------------------------- 图 7 面积最值
def fig_max():
    p = Plane(110, 300, 16, 1.15)
    b = [p.axes(-1, 21, -8, 212, xticks=(5, 10, 15, 20), yticks=(100, 200))]
    b.append(p.curve(lambda x: -2 * x * x + 40 * x, 0, 20, BLUE))
    b.append(f'<line x1="{p.X(10):.1f}" y1="{p.oy}" x2="{p.X(10):.1f}" y2="{p.Y(200):.1f}" '
             f'stroke="{GRAY}" stroke-width="1" stroke-dasharray="4 3"/>')
    b.append(f'<line x1="{p.ox}" y1="{p.Y(200):.1f}" x2="{p.X(10):.1f}" y2="{p.Y(200):.1f}" '
             f'stroke="{GRAY}" stroke-width="1" stroke-dasharray="4 3"/>')
    b.append(p.dot(10, 200, RED, 4.5))
    b.append(txt(p.X(10) + 12, p.Y(200) - 12, "顶点 (10，200)", 12, RED))
    b.append(txt(152, 250, "S = −2x² + 40x", 12, BLUE))
    b.append(txt(152, 272, "x = 10 时取最大值 200", 11, RED))
    return wrap(480, 360, "\n".join(b),
                "面积 S 关于宽 x 的抛物线 S 等于负 2x 平方加 40x，在 x 等于 10 处取最大值 200")


if __name__ == "__main__":
    figs = {
        "coordinate-plane.svg": fig_coordinate,
        "linear-graph.svg": fig_linear,
        "linear-compare.svg": fig_compare,
        "inverse-graph.svg": fig_inverse,
        "parabola-basic.svg": fig_parabola,
        "parabola-roots.svg": fig_roots,
        "parabola-max.svg": fig_max,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in figs.items():
        (OUT / name).write_text(fn(), encoding="utf-8")
        print("written", name)
