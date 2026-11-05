"""按自检结果修复内容缺陷。每条修复都做替换前后断言，替换不上就报错。"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "content" / "points"

fixes = []


def load(pid):
    return json.loads((P / f"{pid}.json").read_text(encoding="utf-8"))


def save(pid, d):
    (P / f"{pid}.json").write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def sub(pid, path, old, new, note):
    """path: 形如 sections.examples[2].question 的列表式路径"""
    d = load(pid)
    node = d
    for key in path:
        if isinstance(key, int):
            node = node[key]
        else:
            node = node[key]
    if old not in node:
        if new in node:
            fixes.append((pid, note + "（已是修复后状态，跳过）"))
            return
        raise SystemExit(f"[{pid}] 修复失败，未找到原文：{note}\n  查找串：{old[:60]}")
    node = node.replace(old, new)
    # 回写
    d2 = load(pid)
    n2 = d2
    for key in path[:-1]:
        n2 = n2[key]
    n2[path[-1]] = node
    save(pid, d2)
    fixes.append((pid, note))


# 1. m1-03-01 ex2：「如图所示」指向不存在的图
sub("m1-03-01-coordinates-and-function",
    ["sections", "examples", 1, "question"],
    "某地一天的气温 $T$（℃）与时间 $t$（时）的关系如图所示：$0$ 时 $2$℃，$6$ 时 $-1$℃，$14$ 时 $8$℃，$24$ 时 $3$℃。",
    "某地一天的气温 $T$（℃）随时间 $t$（时）变化，记录了四个时刻的数据：$0$ 时 $2$℃，$6$ 时 $-1$℃，$14$ 时 $8$℃，$24$ 时 $3$℃。",
    "ex2 去掉虚假图引用「如图所示」")
sub("m1-03-01-coordinates-and-function",
    ["sections", "examples", 1, "solution"],
    "在图象上找纵坐标的最大值与最小值对应的点。最高点是 $t=14$ 时的点，纵坐标 $8$，即最高气温 $8$℃；最低点是 $t=6$ 时的点，纵坐标 $-1$，即最低气温 $-1$℃。温差为 $8-(-1)=9$℃。注意最低气温出现在清晨而非午夜，读图要以图象为准，不能凭生活经验猜。",
    "把四个时刻的温度并排比较：$2$℃、$-1$℃、$8$℃、$3$℃。最高的是 $8$℃，出现在 $t=14$；最低的是 $-1$℃，出现在 $t=6$。温差为 $8-(-1)=9$℃。注意最低气温出现在清晨而非午夜，读数据要以记录为准，不能凭生活经验猜。",
    "ex2 解答同步去掉「在图象上找」")

# 3. m2-03-02 ex2：对角线 18 几何不可能 + 「四顶点距离两两相等」错误
sub("m2-03-02-parallelogram",
    ["sections", "examples", 1, "question"],
    "平行四边形围栏相邻两边分别为 8 米和 5 米，一条对角线长 18 米。求围栏周长，以及这条对角线被交点分成的两段长。",
    "平行四边形围栏相邻两边分别为 8 米和 5 米，一条对角线长 10 米。求围栏周长，以及这条对角线被交点分成的两段长。",
    "ex2 对角线 18 改为 10（对角线必须小于两边之和 13）")
sub("m2-03-02-parallelogram",
    ["sections", "examples", 1, "solution"],
    "对边相等，周长 $=2\\times(8+5)=26$（米）。对角线互相平分，交点 $O$ 把这条对角线分成相等的两段：$18\\div 2=9$（米）。下料时四个顶点到交点的距离两两相等，可据此校验框架是否装正。",
    "对边相等，周长 $=2\\times(8+5)=26$（米）。对角线互相平分，交点 $O$ 把这条对角线分成相等的两段：$10\\div 2=5$（米）。下料时可用「两条对角线都被交点平分」来校验框架是否装正——注意一般平行四边形只有同一条对角线上的两个顶点到交点等距（$OA=OC$、$OB=OD$），并非四个顶点到交点都等距。",
    "ex2 每段 9 改 5，并纠正「四顶点等距」的错误说法")
sub("m2-03-02-parallelogram",
    ["sections", "examples", 1, "answer"],
    "周长 26 米，对角线被交点平分，每段 9 米。",
    "周长 26 米，对角线被交点平分，每段 5 米。",
    "ex2 答案同步改为每段 5 米")

# 4. m2-05-01 ex3：题干「上底定为 2 米」与所求 DE=4.8 自相矛盾
sub("m2-05-01-proportional-segments",
    ["sections", "examples", 2, "question"],
    "上底（$DE$）定为 $2$ 米时，测得 $AD=2$ 米、$AB=5$ 米、$BC=12$ 米。求 $DE$ 的实际长度应为多少？并求两侧斜边上「上段」占全长的比例。",
    "测得 $AD=2$ 米、$AB=5$ 米、$BC=12$ 米。求导轨 $DE$ 的长度，并求两侧斜边上「上段」占全长的比例。",
    "ex3 题干删去与答案矛盾的「上底定为 2 米」")

# 5. m1-01-03 ex3：context 与题目内容不符
sub("m1-01-03-factorization",
    ["sections", "examples", 2, "context"],
    "包装盒四角剪去小正方形后的用料计算",
    "因式分解的完整拆分与代入求值",
    "ex3 context 与实际题目（纯因式分解）对齐")

# 7. m2-05-02 pitfall：假陷阱 + 省略号断句
sub("m2-05-02-similar-triangles",
    ["sections", "pitfalls", 2, "wrong"],
    "周长比为 $k$，各边分别为 $ka$、$kb$、$kc$，周长是 $k(a+b+c)$，所以周长比…… 不同于边比。",
    "周长比等于相似比的平方 $k^{2}$：各边分别为 $ka$、$kb$、$kc$，周长是 $k(a+b+c)$，所以周长比是 $k^{2}$。",
    "pitfalls[2].wrong 改为真正的错误说法（把面积比套到周长）")
sub("m2-05-02-similar-triangles",
    ["sections", "pitfalls", 2, "why"],
    "恰恰相反：$ka+kb+kc=k(a+b+c)$，周长比就是 $k$——线性量按同一倍数伸缩后相加，倍数不变。怀疑周长比不是 $k$ 的直觉来自把面积（$k^2$）混了进来。",
    "周长是各边相加，倍数不会叠加：$ka+kb+kc=k(a+b+c)$，所以周长比就是 $k$。只有面积是二维量，底与高各乘一个 $k$ 才得到 $k^{2}$——把面积的结论套到周长上就会多出一个 $k$。",
    "pitfalls[2].why 与 wrong 对齐，去掉「恰恰相反」的错位表述")

# 8. m1-03-01 ex3：与 m1-02-01 ex3 出租车情境数字完全重复
sub("m1-03-01-coordinates-and-function",
    ["sections", "examples", 2, "question"],
    "某市出租车起步价 $10$ 元，含 $3$ 千米；超过 $3$ 千米的部分每千米 $2.4$ 元。写出车费 $y$（元）与里程 $x$（千米）之间的函数关系式，并求 $x=8$ 时的车费。",
    "某快递首重 $1$ 千克内收费 $8$ 元，超过 $1$ 千克的部分每千克续重 $2$ 元。写快递费 $y$（元）与重量 $x$（千克）之间的函数关系式，并求 $x=5$ 时的快递费。",
    "ex3 换成快递情境，避免与 m1-02-01 ex3 完全重复")
sub("m1-03-01-coordinates-and-function",
    ["sections", "examples", 2, "solution"],
    "分两段写。当 $0<x\\le 3$ 时，车费固定为起步价，$y=10$。当 $x>3$ 时，车费为起步价加上超程费，$y=10+2.4(x-3)=2.4x+2.8$。所以 $y=\\begin{cases}10 & (0<x\\le 3)\\\\ 2.4x+2.8 & (x>3)\\end{cases}$。当 $x=8$ 时属于第二段，$y=2.4\\times 8+2.8=19.2+2.8=22$ 元。检验：超程 $5$ 千米，费用 $10+2.4\\times 5=22$ 元，一致。",
    "分两段写。当 $0<x\\le 1$ 时，只付首重费，$y=8$。当 $x>1$ 时，费用为首重费加续重费，$y=8+2(x-1)=2x+6$。所以 $y=\\begin{cases}8 & (0<x\\le 1)\\\\ 2x+6 & (x>1)\\end{cases}$。当 $x=5$ 时属于第二段，$y=2\\times 5+6=16$ 元。检验：首重 $1$ 千克 $8$ 元，续重 $4$ 千克 $8$ 元，合计 $16$ 元，一致。",
    "ex3 解答同步改为快递计费")
sub("m1-03-01-coordinates-and-function",
    ["sections", "examples", 2, "answer"],
    "$y=\\begin{cases}10 & (0<x\\le 3)\\\\ 2.4x+2.8 & (x>3)\\end{cases}$；$x=8$ 时车费 $22$ 元。",
    "$y=\\begin{cases}8 & (0<x\\le 1)\\\\ 2x+6 & (x>1)\\end{cases}$；$x=5$ 时快递费 $16$ 元。",
    "ex3 答案同步改为快递计费")

print(f"完成 {len(fixes)} 处内容修复：")
for pid, note in fixes:
    print(f"  {pid:<38}{note}")
