"""m2-04 / m2-05 / m2-06 共 15 篇：证明板块由「算理推导步骤」改为「结论化证明」。

结构（与 m1 二十篇、m2-07 三篇样板一致）：
- conclusion：这一条证明了什么（一句命题，陈述结论本身）
- proof：完整的推理过程
- key：这一步凭什么成立（用到的定理、满足的条件）

改写规则：
1. 条数与原 steps 一一对应，不合并、不拆分。
2. 每条 step 的开头标签（如「切线长定理：」）是标题而非推理，移入 conclusion；
   标签之后的正文一字不改地进入 proof。
3. 数学内容一字不差：proof 与「原文去掉标签」逐字相等（脚本断言）。
4. 渲染层会自动加「结论 N」编号与「关键一步」标签，故两个字段都不带这些前缀。

原始 steps 备份在 tools/m2_geo_steps_original.json，供逐字比对与回滚。
备份缺失时脚本从现有文件的 proof 字段反推（proof 即「原文去掉标签」），
仍能校验条数一致性与 proof 是否等于 HEADERS 标签之后的正文。
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
C = ROOT / "content" / "points"
ORIG_FILE = pathlib.Path(__file__).resolve().parent / "m2_geo_steps_original.json"

# 每篇每条 step 开头要摘掉的标签（标题），逐条对应
HEADERS = {
    "m2-04-01-circle-properties": ["用轴对称证垂径定理：", "换成三角形语言：", "四量关系："],
    "m2-04-02-central-inscribed-angles": ["", "第二类：", "推论链："],
    "m2-04-03-circle-position": ["", "共线三点无解：", "直线与圆的数量刻画："],
    "m2-04-04-tangent-lines": ["性质定理（切线垂直于过切点的半径）：", "判定定理：", "切线长定理：", "直角三角形内切圆半径："],
    "m2-04-05-arc-sector-cone": ["弧长公式：", "扇形面积公式：", "圆锥侧面展开："],
    "m2-04-06-regular-polygon": ["存在中心（外接圆）：", "内切圆与边心距直角三角形：", "面积公式：", "正六边形特例："],
    "m2-05-01-proportional-segments": ["先证等分特例（基础版）：", "再过渡到成比例（一般版思路）：", "三角形中的比例转移：", "$\\tfrac{DE}{BC}$ 进比例："],
    "m2-05-02-similar-triangles": ["预备引理（平行引理）：", "AA 判定：", "线段比 $=k$（以高为例）：", "面积比 $=k^2$："],
    "m2-05-03-similar-models": ["A 字型（回顾）：", "8 字型：", "母子型：", "一线三等角："],
    "m2-05-04-homothety": ["位似图形必相似：", "平行性保形状：", "坐标规律：", "$k<0$ 的旋转效果："],
    "m2-05-05-projection-views": ["影长测高的相似来源（平行投影）：", "中心投影的相似来源：", "正投影保形（线段版）：", "三视图对齐三律："],
    "m2-06-01-symmetry": ["轴对称的垂直平分：", "轴对称的全等：", "中心对称的中点：", "中心对称是旋转的特例："],
    "m2-06-02-translation-rotation": ["平移保持长度与方向：", "平移保持角度：", "旋转保持到中心的距离：", "旋转角处处相等："],
    "m2-06-03-transform-coordinates": ["平移规律：", "关于 $x$ 轴对称：", "关于原点对称：", "折叠的等量来源："],
    "m2-06-04-geometric-extremum": ["将军饮马的不等式：", "取等时的落点：", "造桥选址的平移消元：", "定边直角生成圆："],
}

STEPS = {
    # ================================================== m2-04 圆
    "m2-04-01-circle-properties": [
        {
            "conclusion": "垂径定理：垂直于弦的直径平分这条弦，并且平分弦所对的两条弧。",
            "proof": "圆关于任意一条直径所在直线对称——对称轴过圆心，圆心不动，圆翻折后与自身重合。设直径 $CD$ 所在直线垂直于弦 $AB$，则 $A$ 关于这条直线的对称点 $A'$ 既在圆上（对称性），又在过 $A$ 且垂直于对称轴的直线上——而这条直线正是 $AB$ 所在直线（$AB\\perp CD$）。所以 $A'$ 是直线 $AB$ 与圆的另一个交点，即 $B$。对称点连线被对称轴垂直平分：$CD$ 平分 $AB$，也把弧 $AB$ 翻成两段相等的弧。",
            "key": "依据是轴对称的定义与性质：圆关于过圆心的任意一条直线对称，这条对称轴同时是圆上点的对称轴。$A'$ 是 $A$ 关于该直线的对称点，由对称性 $A'$ 仍在圆上；又对称轴垂直平分对应点连线，所以 $A'$ 与 $A$ 的连线垂直于 $CD$，即落在 $AB$ 所在直线上。既然 $A'$ 既在圆上又在直线 $AB$ 上且与 $A$ 不同，它就只能是直线 $AB$ 与圆的另一个交点 $B$。而 $CD$ 垂直平分 $AA'$（$A'$ 就是 $B$，所以 $AA'$ 就是弦 $AB$），弧 $AB$ 被这条对称轴整条翻折过去，两段弧因此相等。",
        },
        {
            "conclusion": "等腰三角形三线合一的说法与轴对称说法等价：$OD$ 同时是 $\\triangle OAB$ 底边上的高、中线与顶角平分线，所以 $AD=BD$，弦所对的两段弧也相等。",
            "proof": "连 $OA$、$OB$，$OA=OB=R$，$\\triangle OAB$ 是等腰三角形；$OD$ 是底边上的高，由三线合一（m2-02-04），$D$ 同时是中点——$AD=BD$，顶角也被平分，弧随之对半分。两种说法一静一动，说的是同一件事。",
            "key": "依据是等腰三角形的三线合一（m2-02-04）：在等腰三角形中，底边上的高与底边上的中线、顶角平分线是同一条线。$OA=OB=R$ 保证 $\\triangle OAB$ 是等腰三角形，而 $OD\\perp AB$ 由已知条件给出，所以 $OD$ 就是这条三线合一中的高，$D$ 顺带成为 $AB$ 的中点；顶角被平分后，两条半径把整圆分成两段相等的弧。",
        },
        {
            "conclusion": "半径、弦心距与弦长之间满足勾股关系 $R^2=d^2+(a/2)^2$；拱桥公式 $R^2=(R-h)^2+(a/2)^2$ 是它的变形。",
            "proof": "垂径定理保证 $D$ 是中点，于是 $OD\\perp AB$、$AD=a/2$，在直角 $\\triangle OAD$ 中用勾股定理（m2-02-05）：$R^2=d^2+(a/2)^2$。拱桥公式是它的变形：设拱高 $h$、跨度 $a$，圆心在拱内侧距桥面 $R-h$ 处（图 1 右），勾股即 $R^2=(R-h)^2+(a/2)^2$。",
            "key": "依据是勾股定理（m2-02-05）用在直角 $\\triangle OAD$ 上：$OD\\perp AB$ 给出直角，$AD=a/2$ 给出半弦长，斜边是半径 $OA=R$，于是 $R^2=OD^2+AD^2=d^2+(a/2)^2$。拱桥情形只是把 $OD$ 换成圆心到桥面的距离 $R-h$，同一个式子换个外形。",
        },
    ],
    "m2-04-02-central-inscribed-angles": [
        {
            "conclusion": "圆周角定理的第一类情形：圆心 $O$ 在 $\\angle ACB$ 的一条边上时，$\\angle ACB=\\tfrac12\\angle AOB$。",
            "proof": "圆周角定理按圆心位置分三类证明。设圆周角 $\\angle ACB$ 所对弧的圆心角为 $\\angle AOB$。第一类：圆心 $O$ 在 $\\angle ACB$ 的一条边上（$B$、$O$、$C$ 共线）。连 $OA$：$OA=OC$，等腰 $\\triangle OAC$ 中 $\\angle OAC=\\angle OCA$（即圆周角）；$\\angle AOB$ 是 $\\triangle OAC$ 的外角，等于两不相邻内角之和 $=2\\angle OCA$。所以 $\\angle ACB=\\tfrac12\\angle AOB$。",
            "key": "依据是等腰三角形的底角相等与三角形的外角性质：$OA=OC$ 都是半径，所以 $\\triangle OAC$ 是等腰三角形，$\\angle OAC=\\angle OCA$；$\\angle AOB$ 是 $\\triangle OAC$ 的外角，等于与它不相邻的两个内角 $\\angle OAC$ 与 $\\angle OCA$ 之和，于是 $\\angle AOB=2\\angle OCA$。又 $B$、$O$、$C$ 共线时 $\\angle OCA$ 就是 $\\angle ACB$，两边同除以 2 即得。",
        },
        {
            "conclusion": "圆心在角的内部或外部时，圆周角定理同样成立——三类位置合起来，定理对任何位置成立。",
            "proof": "圆心在角内部。连 $CO$ 并延长交圆于 $D$，把 $\\angle ACB$ 拆成 $\\angle ACD+\\angle DCB$，每一个都属第一类（$D$、$O$、$C$ 共线），相加即 $\\angle ACB=\\tfrac12\\angle AOB$。第三类：圆心在角外部，同理连 $CO$ 延长，作差（$\\angle ACB=\\angle DCB-\\angle DCA$）结论相同。三种情况合起来，定理对任何位置成立——这是「分类讨论」在几何证明里的经典演出。",
            "key": "依据是「同一圆周角拆出的两个小角都满足第一类情形」：内部情形连 $CO$ 延长交圆于 $D$，$D$、$O$、$C$ 共线，于是 $\\angle ACD$ 与 $\\angle DCB$ 都属于第一类，各是各自圆心角的一半，相加即得；外部情形用两个同类角相减。分类讨论之所以合法，是因为圆心相对 $\\angle ACB$ 的位置只有「边上、内部、外部」三种，互不重叠且穷尽全部情形。",
        },
        {
            "conclusion": "圆周角定理的三条推论：同弧所对的圆周角相等；半圆所对的圆周角是直角；圆内接四边形的对角互补。",
            "proof": "同弧上两个圆周角 $\\angle ACB$、$\\angle ADB$ 都等于 $\\tfrac12\\angle AOB$，故相等；弧换成半圆，圆心角 $180^{\\circ}$，圆周角 $90^{\\circ}$（图 1 右）；顶点处的两条半径反向共线时，圆周角 $90^{\\circ}$ 所对弧是半圆，所对弦过圆心即直径。圆内接四边形 $ABCD$：$\\angle A$ 对弧 $BCD$（不含 $A$ 的那段），$\\angle C$ 对弧 $BAD$，两段弧恰好拼成整圆 $360^{\\circ}$，各取一半相加：$\\angle A+\\angle C=\\tfrac12\\times 360^{\\circ}=180^{\\circ}$——对角互补。",
            "key": "依据是圆周角定理本身加弧的度数：同一段弧所对的两个圆周角都等于它所对圆心角的一半，而这两个圆周角对的是同一个 $\\angle AOB$，故相等；弧为半圆时圆心角是 $180^{\\circ}$，一半即 $90^{\\circ}$。内接四边形中 $\\angle A$ 与 $\\angle C$ 所对的两段弧合起来是整圆 $360^{\\circ}$，各取一半再相加得 $\\tfrac12\\times 360^{\\circ}=180^{\\circ}$，即对角互补。",
        },
    ],
    "m2-04-03-circle-position": [
        {
            "conclusion": "过不共线的三点可以作圆，而且只可以作一个：圆心是任意两段连线的垂直平分线的交点，半径是圆心到任一顶点的距离。",
            "proof": "过不共线三点作圆的圆心必须到三点等距。到 $A$、$B$ 等距的点在线段 $AB$ 的垂直平分线上（m2-01-05），到 $B$、$C$ 等距的在 $BC$ 的垂直平分线上——圆心只能在这两条线的交点处。不共线时两条垂直平分线必相交于一点 $O$，且 $O$ 到 $A$、$B$、$C$ 等距，以 $OA$ 为半径的圆同时过三点；交点唯一，所以圆唯一。",
            "key": "依据是垂直平分线的判定与性质（m2-01-05）：到线段两端距离相等的点恰在这条线段的垂直平分线上，所以圆心必须同时落在 $AB$ 与 $BC$ 的垂直平分线上。不共线时两条垂直平分线不平行，交于唯一一点 $O$；$O$ 到三点等距，以 $OA$ 为半径的圆就同时过三点。交点唯一，所以圆也唯一。",
        },
        {
            "conclusion": "三点共线时作不出圆。",
            "proof": "设三点共线，若有圆心 $O$ 到三点等距，则 $O$ 在每两点连线的垂直平分线上——而这些连线是同一条直线，它的垂直平分线彼此平行，没有交点，矛盾。",
            "key": "依据是垂直平分线的性质加上平行线不相交：若圆心 $O$ 到三点等距，它就得同时在三条（其实是同一直线上的）连线的垂直平分线上，而同一直线的垂直平分线彼此平行、没有交点，与「圆心存在」矛盾。共线时三点的垂直平分线不但不交，还互相平行。",
        },
        {
            "conclusion": "圆与直线的位置关系由圆心到直线的距离 $d$ 与半径 $R$ 决定：$d>R$ 无公共点，$d=R$ 只有一个公共点，$d<R$ 有两个公共点。",
            "proof": "圆心 $O$ 到直线 $l$ 的垂线段长为 $d$（垂足 $H$）。$\\odot O$ 上各点到 $O$ 距离都是 $R$：若 $d>R$，则 $l$ 上离 $O$ 最近的点 $H$ 都已在圆外，无公共点；$d=R$ 时最近点恰好落在圆上，其余点全在圆外，唯一公共点；$d<R$ 时 $H$ 在圆内，而 $l$ 伸向无穷远必穿出圆，与圆交于两点（垂径定理保证弦长 $2\\sqrt{R^2-d^2}$，m2-04-01）。",
            "key": "依据是垂线段最短：$H$ 是 $l$ 上离 $O$ 最近的点，所以 $l$ 上每点到 $O$ 的距离都不小于 $d$。$d>R$ 时连最近点都在圆外，整条直线无公共点；$d=R$ 时最近点恰好落在圆上，其余点都在圆外，公共点唯一；$d<R$ 时 $H$ 在圆内，而 $l$ 无限延伸必定穿出圆，与圆交于两点，弦长由垂径定理给出为 $2\\sqrt{R^2-d^2}$。",
        },
    ],
    "m2-04-04-tangent-lines": [
        {
            "conclusion": "切线的性质定理：圆的切线垂直于经过切点的半径。",
            "proof": "设 $AB$ 切 $\\odot O$ 于 $C$，连 $OC$。反证：若 $OC$ 不垂直于 $AB$，则圆心到直线的距离 $d<OC=R$（垂线段最短，m2-01-03），于是直线与圆相交、有两个公共点，与「相切（唯一公共点）」矛盾。故 $OC\\perp AB$。",
            "key": "依据是垂线段最短（m2-01-03）加上「相切只有一个公共点」：若 $OC$ 不垂直于 $AB$，则圆心到直线的垂线段比 $OC$ 还短，即 $d<OC=R$，按 m2-04-03 的判定（$d<R$ 时相交）直线与圆有两个公共点，与相切矛盾。所以 $OC\\perp AB$。",
        },
        {
            "conclusion": "切线的判定定理：过半径外端且垂直于该半径的直线与圆相切。",
            "proof": "设直线 $l$ 过半径 $OC$ 的外端 $C$ 且 $l\\perp OC$。在 $l$ 上任取异于 $C$ 的点 $P$，连 $OP$：$OP>OC=R$（斜线大于垂线段），即 $l$ 上除 $C$ 外的点全在圆外——公共点只有 $C$ 一个，$l$ 是切线。",
            "key": "依据是直角三角形中斜边大于直角边：$l\\perp OC$ 且 $P$ 在 $l$ 上，$\\triangle OCP$ 是直角三角形，斜边 $OP$ 必大于直角边 $OC=R$，所以 $l$ 上除 $C$ 外的点全在圆外；而 $C$ 本身在圆上，公共点唯一，故 $l$ 与圆相切。",
        },
        {
            "conclusion": "切线长定理：从圆外一点引圆的两条切线，切线长相等，且连线 $OP$ 平分这两条切线所夹的角；$\\angle AOB+\\angle APB=180^{\\circ}$。",
            "proof": "$PA$、$PB$ 切 $\\odot O$ 于 $A$、$B$，连 $OA$、$OB$、$OP$。由性质定理 $\\angle OAP=\\angle OBP=90^{\\circ}$；$OA=OB$（半径），$OP$ 公共——直角三角形全等（HL，m2-02-02）：$\\triangle OAP\\cong\\triangle OBP$。所以 $PA=PB$（切线长相等）、$\\angle OPA=\\angle OPB$（$OP$ 平分 $\\angle APB$）。四边形 $OAPB$ 内角和 $360^{\\circ}$，减去两个 $90^{\\circ}$ 得 $\\angle AOB+\\angle APB=180^{\\circ}$。",
            "key": "依据是直角三角形全等的 HL 判定（m2-02-02）：$\\triangle OAP$ 与 $\\triangle OBP$ 都是直角三角形，斜边 $OP$ 是公共边，直角边 $OA=OB$ 都是半径，两条斜边与一条直角边分别相等，故两三角形全等，于是对应边 $PA=PB$、对应角 $\\angle OPA=\\angle OPB$。而 $\\angle AOB+\\angle APB=180^{\\circ}$ 来自四边形 $OAPB$ 内角和 $360^{\\circ}$ 减去两个直角 $\\angle OAP$、$\\angle OBP$。",
        },
        {
            "conclusion": "直角三角形的内切圆半径 $r=\\dfrac{ab}{a+b+c}=\\dfrac{a+b-c}{2}$，其中 $a$、$b$ 是两条直角边，$c$ 是斜边。",
            "proof": "设两直角边 $a$、$b$、斜边 $c$，内心到三边的距离都是 $r$。面积法：$S=\\tfrac12 ab$，又 $S=\\tfrac12 ar+\\tfrac12 br+\\tfrac12 cr=\\tfrac12(a+b+c)r$，故 $r=\\dfrac{ab}{a+b+c}=\\tfrac{a+b-c}{2}$（最后一步用 $c^2=a^2+b^2$ 恒等变形：$\\dfrac{ab}{a+b+c}=\\dfrac{ab(a+b-c)}{(a+b)^2-c^2}=\\dfrac{ab(a+b-c)}{2ab}$）。",
            "key": "依据是面积法的两种算法必须相等：直角三角形按整体算得 $S=\\tfrac12 ab$，按内心分成的三个小三角形算得 $S=\\tfrac12 ar+\\tfrac12 br+\\tfrac12 cr=\\tfrac12(a+b+c)r$（内心到三边的距离都是 $r$，所以三个高都等于 $r$），两式相等即得 $r=\\dfrac{ab}{a+b+c}$。最后一步是代数恒等变形：由 $c^2=a^2+b^2$ 得 $(a+b)^2-c^2=2ab$，所以 $\\dfrac{ab}{a+b+c}=\\dfrac{ab(a+b-c)}{(a+b)^2-c^2}=\\dfrac{ab(a+b-c)}{2ab}=\\dfrac{a+b-c}{2}$。",
        },
    ],
    "m2-04-05-arc-sector-cone": [
        {
            "conclusion": "弧长公式：$n^{\\circ}$ 的弧长 $l=\\tfrac{n\\pi R}{180}$，等价地 $\\tfrac{l}{2\\pi R}=\\tfrac{n}{360}$。",
            "proof": "把整圆按 $1^{\\circ}$ 圆心角切成 $360$ 等份（圆心角相等的弧相等，m2-04-02），每份弧长 $\\tfrac{2\\pi R}{360}=\\tfrac{\\pi R}{180}$。$n^{\\circ}$ 的弧含 $n$ 份：$l=\\tfrac{n\\pi R}{180}$。本质是比例：$\\tfrac{l}{2\\pi R}=\\tfrac{n}{360}$（图 1 左）。",
            "key": "依据是圆心角相等的弧相等（m2-04-02）：把整圆按 $1^{\\circ}$ 圆心角切成 $360$ 等份，每份弧长就是 $\\tfrac{2\\pi R}{360}=\\tfrac{\\pi R}{180}$；$n^{\\circ}$ 的弧正好含 $n$ 份，所以 $l=\\tfrac{n\\pi R}{180}$。写成 $\\tfrac{l}{2\\pi R}=\\tfrac{n}{360}$ 就看出弧长与圆心角成正比。",
        },
        {
            "conclusion": "扇形面积公式 $S=\\tfrac{n\\pi R^2}{360}$，且 $S=\\tfrac12 lR$。",
            "proof": "同理 $\\tfrac{S}{\\pi R^2}=\\tfrac{n}{360}$，得 $S=\\tfrac{n\\pi R^2}{360}$。由 $l=\\tfrac{n\\pi R}{180}$ 得 $\\tfrac{n\\pi R^2}{360}=\\tfrac12\\times \\tfrac{n\\pi R}{180}\\times R=\\tfrac12 lR$——与三角形面积「$\\tfrac12$ 底高」同构：把弧拉直当底、半径当高。",
            "key": "依据与弧长同理：扇形与整个圆是同心的、圆心角成比例的两块图形，面积之比等于圆心角之比 $\\tfrac{n}{360}$，得 $S=\\tfrac{n\\pi R^2}{360}$；再用 $l=\\tfrac{n\\pi R}{180}$ 把 $n$ 消掉，得 $\\tfrac{n\\pi R^2}{360}=\\tfrac12\\times \\tfrac{n\\pi R}{180}\\times R=\\tfrac12 lR$。这与三角形面积「$\\tfrac12$ 底高」是同一个模式：把弧拉直当底、半径当高。",
        },
        {
            "conclusion": "圆锥侧面展开成扇形，扇形半径等于母线、弧长等于底面周长 $2\\pi r$，故侧面积 $S_{侧}=\\pi rl$，展开图的圆心角 $\\theta=\\tfrac{360r}{l}$。",
            "proof": "沿母线剪开侧壁摊平，曲面无拉伸无折叠，面积不变。摊平后：顶点为圆心，原来从顶点出发的每条母线长都是 $l$，摊平后自然成为半径 $l$ 的扇形半径；底面圆周被摊开成扇形的弧，长度不变为 $2\\pi r$（图 1 右）。由弧长公式反解圆心角：$2\\pi r=\\tfrac{\\theta\\pi l}{180}$，$\\theta=\\tfrac{360 r}{l}$；面积用 $\\tfrac12 lR$ 版：$S_{侧}=\\tfrac12\\times 2\\pi r\\times l=\\pi r l$。",
            "key": "依据是曲面剪开摊平不改变面积：沿母线剪开后，原来的每条母线变成从顶点出发的半径（长仍是 $l$），底面圆周变成扇形的弧（长仍是 $2\\pi r$），所以展开图是一个半径 $l$、弧长 $2\\pi r$ 的扇形。用弧长公式反解圆心角得 $\\theta=\\tfrac{360 r}{l}$；用 $S=\\tfrac12 lR$ 版（弧长取 $2\\pi r$、半径取 $l$）即得 $S_{侧}=\\tfrac12\\times 2\\pi r\\times l=\\pi r l$。",
        },
    ],
    "m2-04-06-regular-polygon": [
        {
            "conclusion": "正 $n$ 边形有外接圆，圆心是相邻两边垂直平分线的交点；绕圆心旋转 $\\tfrac{360^{\\circ}}{n}$ 图形与自身重合，中心角为 $\\tfrac{360^{\\circ}}{n}$。",
            "proof": "设 $O$ 是正 $n$ 边形两条相邻边垂直平分线的交点。由各边相等，$O$ 到这条边的两个端点等距（垂直平分线性质，m2-01-05），再由各角相等可以推出 $O$ 到所有顶点等距（等距的传递沿对称链完成）——全部顶点落在以 $O$ 为圆心、$R$ 为半径的圆上。换个视角：绕 $O$ 旋转 $\\tfrac{360^{\\circ}}{n}$，每条边、每个角换到下一个位置，图形与自身重合——旋转对称保证了「均匀分布」，中心角必为 $\\tfrac{360^{\\circ}}{n}$（图 1 左）。",
            "key": "依据是垂直平分线的性质（m2-01-05）与旋转对称：各边相等，所以圆心到每个顶点的距离沿相邻边逐步传递相等，各角相等保证传递不断档，于是全部顶点落在以该点为圆心的同一个圆上；而绕圆心转 $\\tfrac{360^{\\circ}}{n}$ 图形与自身重合，说明各边把整周 $360^{\\circ}$ 均分，中心角只能是 $\\tfrac{360^{\\circ}}{n}$。",
        },
        {
            "conclusion": "正 $n$ 边形有内切圆，边心距 $OM=r$，且 $R^2=r^2+(\\tfrac{a}{2})^2$。",
            "proof": "连 $OA$、$OB$（相邻顶点），$\\triangle OAB$ 是等腰三角形（$OA=OB=R$）。从 $O$ 向底边 $AB$ 作垂线段 $OM$，由三线合一（m2-02-04）：$M$ 是 $AB$ 中点（$AM=\\tfrac{a}{2}$）、$\\angle AOM$ 平分中心角。以 $OM=r$ 为半径作圆，与每条边都相切（垂足恰为切点，圆心到直线距离 $=r$，m2-04-03/04）——这就是内切圆，$OM$ 即边心距。于是在 Rt$\\triangle OAM$ 中：$R^2=r^2+(\\tfrac{a}{2})^2$。",
            "key": "依据是等腰三角形三线合一（m2-02-04）与「圆心到直线的距离等于半径时直线与圆相切」（m2-04-03/04）：连相邻两顶点得 $OA=OB=R$，底边上的高 $OM$ 同时是中线（$AM=\\tfrac{a}{2}$）与顶角平分线；各边到圆心 $O$ 的距离都等于 $r$，以 $r$ 为半径的圆与每条边都相切，垂足就是切点。于是在直角三角形 $OAM$ 中用勾股定理（m2-02-05）得 $R^2=r^2+(\\tfrac{a}{2})^2$。",
        },
        {
            "conclusion": "正 $n$ 边形的面积 $S=\\tfrac12\\times$周长$\\times r$，其中 $r$ 是边心距。",
            "proof": "中心把正 $n$ 边形拆成 $n$ 个全等等腰三角形（旋转对称），每个面积 $\\tfrac12\\times a\\times r$（底 $a$、高 $r$）。总和 $S=\\tfrac12 n a r=\\tfrac12\\times$周长$\\times r$。它与扇形面积 $\\tfrac12 lR$（m2-04-05）共享同一个形象：把边（或弧）拉直当底、中心距离当高。",
            "key": "依据是旋转对称保证的分割：中心把正 $n$ 边形分成 $n$ 个全等的等腰三角形，每个以边 $a$ 为底、边心距 $r$ 为高，面积 $\\tfrac12\\times a\\times r$，$n$ 个相加即 $S=\\tfrac12 n a r=\\tfrac12\\times$周长$\\times r$。它与扇形面积 $\\tfrac12 lR$（m2-04-05）是同一个形象：把边（或弧）拉直当底、中心到边的距离当高。",
        },
        {
            "conclusion": "正六边形的边长等于外接圆半径，即 $a=R$。",
            "proof": "中心角 $60^{\\circ}$，等腰三角形顶角 $60^{\\circ}$ 且两腰 $R$ 相等——顶角 $60^{\\circ}$ 的等腰三角形底角也各 $60^{\\circ}$，是等边三角形，所以 $a=R$。六个等边三角形拼出正六边形（图 1 左），这解释了「圆规取半径沿圆周截六段恰好闭合」的经典作图。",
            "key": "依据是等腰三角形的底角相等与三角形内角和：中心角 $60^{\\circ}$ 的等腰三角形两底角也各是 $60^{\\circ}$，三角全等故三边相等，$a=R$。六个这样的等边三角形正好拼成正六边形，说明「圆规取半径沿圆周截六段恰好闭合」不是巧合，而是 $60^{\\circ}$ 中心角与等边三角形的必然结果。",
        },
    ],
    # ================================================== m2-05 相似与投影
    "m2-05-01-proportional-segments": [
        {
            "conclusion": "等分特例：三条平行线把两条截线分成的对应线段成比例；间距相等时，同一条截线上的两段相等。",
            "proof": "设平行线 $l_1$、$l_2$、$l_3$，$l_1$、$l_2$ 间距离与 $l_2$、$l_3$ 间距离相等。连接 $A$ 与 $E$、过 $B$ 作 $AE$ 的平行线交 $DE$ 于 $G$——平移把「平行线间距离相等」翻译成「$BD=EG$ 且 $GE=EF$」，得 $DE=EF$；同法处理另一条直线得 $AB=BC$。",
            "key": "依据是「平行线间距离相等则被它们截出的线段相等」这条最基本的事实（可由平移或全等证明）：$l_1$、$l_2$ 与 $l_2$、$l_3$ 间距相等，过 $B$ 作 $AE$ 的平行线后，$BD$ 与 $EG$ 落在宽度相同的夹层里所以相等，$GE$ 与 $EF$ 同理，于是 $DE=EF$；换另一条截线用同样办法得 $AB=BC$。等分情形是后面成比例的特例。",
        },
        {
            "conclusion": "一般结论：两条平行线分截线所得的对应线段成比例，$\\tfrac{DE}{EF}=\\tfrac{AB}{BC}$。",
            "proof": "距离不相等时，设 $\\tfrac{AB}{BC}=\\tfrac{m}{n}$（$m$、$n$ 为正整数，比值是无理数时用有理数逼近的极限思想处理，初中阶段承认结论）。把 $AB$ 等分成 $m$ 份、$BC$ 等分成 $n$ 份，过每个分点作 $l_1$ 的平行线——这组新平行线把两条直线截出的份数完全同步：一条上 $m+n$ 份，另一条上也 $m+n$ 份，对应夹层里的线段彼此相等，于是 $\\tfrac{DE}{EF}=\\tfrac{m}{n}=\\tfrac{AB}{BC}$。",
            "key": "依据是把「成比例」细分成「等分」再数份数：把 $AB$ 均分成 $m$ 份、$BC$ 均分成 $n$ 份后，过各分点作平行线，这组新平行线在两条截线上切出的段数同步（同为 $m+n$ 段），落在同一夹层里的线段彼此相等，于是总长之比就等于份数之比 $\\tfrac{m}{n}$，即 $\\tfrac{DE}{EF}=\\tfrac{AB}{BC}$。份数同步是能按层配对的前提。",
        },
        {
            "conclusion": "在三角形中，平行于 $BC$ 的线段 $DE$ 把两边按同一比例分开：$\\tfrac{AD}{DB}=\\tfrac{AE}{EC}$，等价地 $\\tfrac{AD}{AB}=\\dfrac{AE}{AC}$。",
            "proof": "把 $DE$ 与 $BC$ 看成一组平行线，$\\triangle ABC$ 的两边 $AB$、$AC$ 正是被这组平行线所截的两条直线，直接套定理得 $\\tfrac{AD}{DB}=\\tfrac{AE}{EC}$；再用合比变形 $\\tfrac{AD}{DB}=\\tfrac{AD}{AB-AD}$ 推出 $\\tfrac{AD}{AB}=\\tfrac{AE}{AC}$。",
            "key": "依据是上面刚证的成比例定理直接套用：$DE\\parallel BC$ 时，$AB$、$AC$ 就是被这两条平行线所截的两条直线，所以对应段之比相等。后一步是纯代数变形——把分母写成 $AB-AD$ 与 $AC-AE$，两边同除以对应的整段，利用合比关系即得 $\\tfrac{AD}{AB}=\\dfrac{AE}{AC}$。",
        },
        {
            "conclusion": "平行线段与整段也成比例：$\\tfrac{DE}{BC}=\\tfrac{AD}{AB}$，即两者都等于「平行线到顶点的份数比」。",
            "proof": "$DE$ 与 $BC$ 是两条平行线，被 $AB$、$AC$ 所截——由第 1 步的等分思路倒推回去（把比例「细分成等分」），可以证明 $\\tfrac{DE}{BC}=\\tfrac{AD}{AB}$：都等于「平行线到顶点的份数比」。初中教材把它与判定放在一起，此处作为定理体系的一环接受并使用。",
            "key": "依据与前面的等分思路同源，是逆用：把 $AB$、$AC$ 都细分成同样的份数，$DE$ 与 $BC$ 分别落在从顶点 $A$ 数起的第 $k$ 份与第 $N$ 份处，两个比都是「第几份占全部几份」，所以 $\\tfrac{DE}{BC}=\\tfrac{k}{N}$；同理 $AD$ 与 $AB$ 的份数比也是 $\\tfrac{k}{N}$，两个比相等。有了这一条，两条小段比之外才补上整段比。",
        },
    ],
    "m2-05-02-similar-triangles": [
        {
            "conclusion": "平行引理：$\\triangle ABC$ 中若 $DE\\parallel BC$（$D$ 在 $AB$ 上、$E$ 在 $AC$ 上），则 $\\triangle ADE\\sim\\triangle ABC$。",
            "proof": "$\\triangle ABC$ 中 $DE\\parallel BC$（$D$ 在 $AB$ 上、$E$ 在 $AC$ 上），则 $\\triangle ADE\\sim\\triangle ABC$。由 m2-05-01 的比例转移 $\\tfrac{AD}{AB}=\\tfrac{AE}{AC}$；再把 $DE$ 平移到过 $B$（或 $C$）用同法得第三组比 $\\tfrac{DE}{BC}=\\tfrac{AD}{AB}$——三边成比例；角由平行线的同位角（m2-01-03）直接相等。",
            "key": "依据是 m2-05-01 的比例转移与平行线同位角（m2-01-03）：$\\tfrac{AD}{AB}=\\tfrac{AE}{AC}$ 给出两组对应边成比例，再把 $DE$ 平移到过 $B$ 用同法得 $\\tfrac{DE}{BC}=\\tfrac{AD}{AB}$，三组对应边全部成比例；角由 $DE\\parallel BC$ 的同位角直接相等。两组边成比例加一组角相等，就得到两个三角形相似。",
        },
        {
            "conclusion": "AA 判定：两个角对应相等的三角形相似。",
            "proof": "$\\triangle ABC$ 与 $\\triangle DEF$ 两角对应相等。把小的平移旋转，让 $\\angle A$ 与 $\\angle D$ 重合、$AB$ 落在 $DE$ 上——$\\angle B=\\angle E$ 强制 $BC\\parallel EF$（同位角相等则平行），于是落入第 1 步的平行引理：$\\triangle ABC$ 与大三角形中「被平行线截出的三角形」相似。两角锁定形状，边只剩整体伸缩一个自由度。",
            "key": "依据是「同位角相等则两直线平行」：把 $\\angle A$ 与 $\\angle D$ 重合、$AB$ 落在 $DE$ 上之后，$\\angle B=\\angle E$ 迫使 $BC\\parallel EF$，于是落回上面那条平行引理，图形位置摆正后对应关系一眼可见。两角锁定形状，边只剩整体伸缩一个自由度，这正是相似比 $k$ 可以是任意正数的根源。",
        },
        {
            "conclusion": "相似三角形的对应线段（包括高、中线、角平分线）之比都等于相似比 $k$。",
            "proof": "设 $AH\\perp BC$ 于 $H$、$DK\\perp EF$ 于 $K$（对应高）。AA 已经保证 $\\triangle ABH\\sim\\triangle DEK$（直角与 $\\angle B=\\angle E$），故 $\\tfrac{DK}{AH}=\\tfrac{DE}{AB}=k$。中线、角平分线同理——都被各自的「小三角形相似」保送为 $k$。",
            "key": "依据是相似三角形对应边成比例：$AH$ 与 $DK$ 分别是两个相似三角形的一对对应高，而 $\\triangle ABH\\sim\\triangle DEK$ 由直角与 $\\angle B=\\angle E$ 用 AA 得到，所以 $\\tfrac{DK}{AH}=\\tfrac{DE}{AB}=k$。中线、角平分线同理——各自也能配出一对相似的小三角形，被「小三角形相似」保送为 $k$。",
        },
        {
            "conclusion": "相似三角形的面积比等于相似比的平方：$\\tfrac{S_{DEF}}{S_{ABC}}=k^2$。",
            "proof": "$S_{\\triangle ABC}=\\tfrac12 BC\\cdot AH$，$S_{\\triangle DEF}=\\tfrac12 EF\\cdot DK$。两式相除：$\\tfrac{S_{DEF}}{S_{ABC}}=\\tfrac{EF}{BC}\\cdot\\tfrac{DK}{AH}=k\\cdot k=k^2$。底乘高、两个一维量各贡献一个 $k$。",
            "key": "依据是面积公式「底乘高的一半」：$S_{\\triangle ABC}=\\tfrac12 BC\\cdot AH$，$S_{\\triangle DEF}=\\tfrac12 EF\\cdot DK$，两式相除时底之比 $\\tfrac{EF}{BC}=k$ 与高之比 $\\tfrac{DK}{AH}=k$ 各出一个因子，乘起来就是 $k^2$。两个一维量各贡献一个 $k$，所以面积按 $k^2$ 变。",
        },
    ],
    "m2-05-03-similar-models": [
        {
            "conclusion": "A 字型：$DE\\parallel BC$ 时 $\\triangle ADE\\sim\\triangle ABC$，比例式即平行线分线段成比例。",
            "proof": "$\\angle A$ 公共；$\\angle ADE=\\angle B$（$DE\\parallel BC$ 同位角，m2-01-03）。AA 得 $\\triangle ADE\\sim\\triangle ABC$，比例式即 m2-05-01 的比例转移。",
            "key": "依据是 AA 加平行线同位角（m2-01-03）：$\\angle A$ 是公共角，$\\angle ADE=\\angle B$ 由 $DE\\parallel BC$ 的同位角相等得到，两角对应相等即相似；写出的比例式与 m2-05-01 的比例转移是同一个式子，说明 A 字型不是新结论，而是比例定理的一种外形。",
        },
        {
            "conclusion": "8 字型：$\\triangle ABP\\sim\\triangle DCP$，比例式 $\\tfrac{AP}{DP}=\\tfrac{BP}{CP}=\\tfrac{AB}{DC}$。",
            "proof": "两条交叉直线相交于 $P$，$AD$ 与 $BC$ 各是一条截线，$AB\\parallel CD$。$\\angle APB=\\angle CPD$（对顶角，m2-01-03）；$\\angle PAB=\\angle PDC$（内错角，截线 $AD$ 截平行线 $AB$、$CD$）。AA 得 $\\triangle ABP\\sim\\triangle DCP$，比例式 $\\tfrac{AP}{DP}=\\tfrac{BP}{CP}=\\tfrac{AB}{DC}$——配对规律：站在同一条截线两端的两个顶点互为对应。",
            "key": "依据是两组角分别由平行线性质给出：$\\angle APB=\\angle CPD$ 是对顶角（m2-01-03），$\\angle PAB=\\angle PDC$ 是截线 $AD$ 截平行线 $AB$、$CD$ 所得的内错角，AA 判定成立。对应顶点要按「站在同一条截线两端的两个顶点互为对应」来排：$A$、$D$ 同在截线 $AD$ 上、$B$、$C$ 同在截线 $BC$ 上，所以相似写作 $\\triangle ABP\\sim\\triangle DCP$，比例式才不会写反。",
        },
        {
            "conclusion": "母子型：直角三角形斜边上的高把图形分成两个与原三角形相似的小三角形，$\\triangle ABD\\sim\\triangle CBA\\sim\\triangle CAD$，由此 $AB^2=BD\\cdot BC$、$AD^2=BD\\cdot DC$、$AC^2=DC\\cdot BC$。",
            "proof": "Rt$\\triangle ABC$（$\\angle BAC=90^{\\circ}$），$AD\\perp BC$ 于 $D$。$\\angle ADB=\\angle BAC=90^{\\circ}$ 且 $\\angle B$ 公共，得 $\\triangle ABD\\sim\\triangle CBA$；同理 $\\angle ADC=\\angle BAC=90^{\\circ}$ 且 $\\angle C$ 公共，得 $\\triangle CAD\\sim\\triangle CBA$，于是 $\\triangle ABD\\sim\\triangle CBA\\sim\\triangle CAD$（两两相似）。对应边写成比例：$\\triangle ABD\\sim\\triangle CBA$ 给 $\\tfrac{AB}{CB}=\\tfrac{BD}{BA}$，交叉相乘即 $AB^2=BD\\cdot BC$；再由 $\\triangle ABD\\sim\\triangle CAD$ 得 $\\tfrac{BD}{AD}=\\tfrac{AD}{CD}$，即 $AD^2=BD\\cdot DC$；由 $\\triangle CAD\\sim\\triangle CBA$ 得 $AC^2=DC\\cdot BC$。",
            "key": "依据是 AA 判定反复使用：$\\angle ADB=\\angle BAC=90^{\\circ}$ 且 $\\angle B$ 公共，所以 $\\triangle ABD\\sim\\triangle CBA$；$\\angle ADC=\\angle BAC=90^{\\circ}$ 且 $\\angle C$ 公共，所以 $\\triangle CAD\\sim\\triangle CBA$，两两相似。比例式要按相似书写顺序取对应边：$\\triangle ABD\\sim\\triangle CBA$ 给出 $AB\\leftrightarrow CB$、$BD\\leftrightarrow BA$，交叉相乘即 $AB^2=BD\\cdot BC$；$\\triangle ABD\\sim\\triangle CAD$ 给出 $BD\\leftrightarrow AD$、$AD\\leftrightarrow CD$，得 $AD^2=BD\\cdot DC$；$\\triangle CAD\\sim\\triangle CBA$ 给出 $CA\\leftrightarrow CB$、$CD\\leftrightarrow CA$，得 $AC^2=DC\\cdot BC$。",
        },
        {
            "conclusion": "一线三等角：$\\angle B=\\angle C=\\angle ADE=\\alpha$ 时 $\\triangle ABD\\sim\\triangle DCE$，对应边 $AB\\leftrightarrow DC$、$BD\\leftrightarrow CE$、$AD\\leftrightarrow DE$。",
            "proof": "$\\angle B=\\angle C=\\angle ADE=\\alpha$，$B$、$D$、$C$ 在同一直线上（$D$ 在中间），$A$、$E$ 在直线同侧。在 $D$ 处用平角：$\\angle ADB=180^{\\circ}-\\angle ADC$，而 $\\angle ADC=\\angle ADE+\\angle EDC=\\alpha+\\angle EDC$，故 $\\angle ADB=180^{\\circ}-\\alpha-\\angle EDC$。再看 $\\triangle DEC$ 的内角和：$\\angle DEC=180^{\\circ}-\\angle C-\\angle EDC=180^{\\circ}-\\alpha-\\angle EDC$。两个右边完全相同，故 $\\angle ADB=\\angle DEC$；配上 $\\angle B=\\angle C=\\alpha$，AA 得 $\\triangle ABD\\sim\\triangle DCE$（对应边 $AB\\leftrightarrow DC$、$BD\\leftrightarrow CE$、$AD\\leftrightarrow DE$）。",
            "key": "依据是「同一直线上的邻补角」与三角形内角和：在 $D$ 处 $\\angle ADB=180^{\\circ}-\\angle ADC$，而 $\\angle ADC=\\angle ADE+\\angle EDC=\\alpha+\\angle EDC$，故 $\\angle ADB=180^{\\circ}-\\alpha-\\angle EDC$；在 $\\triangle DEC$ 中 $\\angle DEC=180^{\\circ}-\\angle C-\\angle EDC=180^{\\circ}-\\alpha-\\angle EDC$，两个右边相同，故 $\\angle ADB=\\angle DEC$。再配 $\\angle B=\\angle C=\\alpha$，AA 成立——两个已知等角把「$B$、$D$、$C$ 一条直线」换成了两个可配对的角。",
        },
    ],
    "m2-05-04-homothety": [
        {
            "conclusion": "位似图形一定相似：$\\triangle A'B'C'$ 与 $\\triangle ABC$ 位似于中心 $O$、位似比 $k$ 时，对应边之比都是 $k$，对应角相等。",
            "proof": "设 $\\triangle ABC$ 与 $\\triangle A'B'C'$ 位似于中心 $O$，位似比 $k$，$A'、B'$ 在射线 $OA$、$OB$ 上且 $OA'=k\\cdot OA$、$OB'=k\\cdot OB$。$\\triangle OAB$ 与 $\\triangle OA'B'$ 共享顶角 $\\angle AOB=\\angle A'OB'$（同一射线），两边成比例（$\\tfrac{OA'}{OA}=\\tfrac{OB'}{OB}=k$），SAS 相似（m2-05-02）得 $\\triangle OAB\\sim\\triangle OA'B'$，故 $\\tfrac{A'B'}{AB}=k$ 且 $\\angle OAB=\\angle OA'B'$（$A'B'\\parallel AB$）。三边同理全部成比例、三角对应相等——两个三角形相似。",
            "key": "依据是 SAS 相似判定（m2-05-02）：$A'$、$B'$ 在射线 $OA$、$OB$ 上，所以 $\\angle AOB=\\angle A'OB'$（同一个顶角），且 $\\tfrac{OA'}{OA}=\\tfrac{OB'}{OB}=k$（夹这个角的两边成比例），角相等与边的比例同时成立，故 $\\triangle OA'B'\\sim\\triangle OAB$，$\\tfrac{A'B'}{AB}=k$、$\\angle OAB=\\angle OA'B'$ 随之得出。三个顶点的相似合起来整个图形相似——位似比直接就是相似比。",
        },
        {
            "conclusion": "位似把每条边变成与原边平行的对应边，角度一个不变，形状只能整体伸缩。",
            "proof": "第 1 步顺带证出 $A'B'\\parallel AB$、$B'C'\\parallel BC$——位似把每条边都平移成原边的平行线，角度一个不动，形状只能整体伸缩。这就是「复印机文化」的几何内核。",
            "key": "依据是上面顺带证出的 $A'B'\\parallel AB$：由 $\\angle OAB=\\angle OA'B'$ 且 $OA$、$OA'$ 在同一直线上，同位角相等两直线平行（m2-01-03），$A'B'$ 与 $AB$ 方向一致；其余各边同理。平行线之间的角由方向决定，方向不变角度就不变，所以位似是「复印机文化」的几何内核。",
        },
        {
            "conclusion": "位似的坐标规律：以原点为位似中心时，点 $P(x,y)$ 的对应点是 $(kx,\\ ky)$；$k<0$ 时落在反向延长线上，公式仍统一。",
            "proof": "以原点 $O(0,0)$ 为位似中心，点 $P(x,y)$ 的对应点 $P'$ 在射线 $OP$ 上且 $|OP'|=|k|\\cdot|OP|$。$OP$ 的方向向量就是 $(x,y)$ 本身，沿它拉长 $k$ 倍得 $(kx,\\ ky)$（$k<0$ 时沿反向延长线，坐标取负乘 $|k|$，公式统一为 $(kx,\\ ky)$）。多边形每个顶点各自如此，整体完成变换。",
            "key": "依据是「对应点与位似中心共线且长度按位似比放大」：$P'$ 在射线 $OP$ 上说明方向不变，$|OP'|=|k|\\cdot|OP|$ 说明长短按同一个倍数伸缩，而 $P(x,y)$ 的两个坐标正是沿两条坐标轴方向的分量，方向不变、长度同倍变，两个分量就同时乘上 $k$。$k<0$ 时落在反向延长线上，两个分量同时取负乘 $|k|$，写成 $(kx,\\ ky)$ 仍然统一。多边形的每个顶点各自如此，整体变换一次完成。",
        },
        {
            "conclusion": "$k<0$ 的位似带一次翻面：$(x,y)\\to(-mx,-my)$，等于先放大 $m$ 倍再关于原点对称。",
            "proof": "$k=-m$（$m>0$）时 $(x,y)\\to(-mx,-my)$——等于先乘 $m$ 放大再关于原点对称（旋转 $180^{\\circ}$，m2-06-02 的中心对称在坐标系里的形态）。位似比的正负号是「要不要翻面」的开关。",
            "key": "依据是坐标取负的几何含义：$k=-m$（$m>0$）时两个分量同时变号，点 $(x,y)$ 落到原点另一侧关于原点对称的位置上，这正是中心对称（m2-06-02 的中心对称在坐标系里的形态），只不过先乘 $m$ 放大。所以位似比的正负号不是记号细节，而是「翻不翻面」的开关：$k>0$ 朝向不变，$k<0$ 朝向相反。",
        },
    ],
    "m2-05-05-projection-views": [
        {
            "conclusion": "平行投影下影长与物高成比例：$\\tfrac{杆高}{杆影}=\\dfrac{楼高}{楼影}$。",
            "proof": "太阳光近似平行，竖直的杆与楼各自和影子构成的直角三角形中，光线是同一组平行线截出的斜边——两角分别相等（光线倾角相同、地面与竖直方向垂直），AA 相似（m2-05-02）：$\\tfrac{杆高}{杆影}=\\tfrac{楼高}{楼影}$。影长比例就是相似比（图 1 左）。",
            "key": "依据是 AA 相似（m2-05-02）：太阳光平行，杆与楼各自和影子构成的直角三角形中，光线倾角相同给出第一个锐角相等，地面与竖直方向都垂直给出第二个直角，两角对应相等即相似。相似三角形的对应边成比例，杆高对应楼高、杆影对应楼影，比值相等——影长比例就是相似比。",
        },
        {
            "conclusion": "中心投影下人与灯形成的两个三角形同样相似，影子越长说明人离灯越远。",
            "proof": "路灯 $L$、人头顶 $H$、影端 $F$ 共线（一条光线）；人与影构成的三角形与路灯高和「灯到影端」构成的三角形共用顶角 $\\angle L$，竖直人与竖直灯平行给出第二对角相等——AA 相似。影子越长，说明人离灯越远——相似比随时在变。",
            "key": "依据是 AA 相似：路灯、头顶与影端在同一条光线上，两个三角形共用顶角 $\\angle L$；竖直的人与竖直的路灯互相平行，给出第二对相等的角，AA 判定成立。与平行投影不同的是这里的相似比随时在变——顶角固定而两边长短随人的位置改变，所以影子越长说明人离灯越远。",
        },
        {
            "conclusion": "正投影不改变平行于投影面的线段的长度和方向；倾斜的线段影子变短，垂直于投影面的线段影子缩成一点。",
            "proof": "设线段 $AB$ 平行于投影面，投影线是一组垂直于投影面的平行线——它们把 $AB$ 的两个端点「平移」到投影面上，平移不改变长度与方向，故影子 $A'B'=AB$，线段平移即全等。线段倾斜时，把 $AB$ 分解为「平行于面」（原样保留）与「沿投影线方向」（缩成 0）两个分量——影子只剩前者，故变短；垂直投影面时全缩为一点。",
            "key": "依据是「投影线是一组互相平行且都垂直于投影面的平行线」：线段平行于投影面时，两个端点沿投影线落到投影面上，等于把整条线段平移过去，平移不改变长度与方向，所以影子 $A'B'=AB$；倾斜时线段可拆成「平行于面」与「沿投影线方向」两个分量，后者被投影压成 $0$，只剩前者，故变短；完全垂直时两个分量都归零，影子是一个点。",
        },
        {
            "conclusion": "三视图对齐三律：长对正（主视图与俯视图）、高平齐（主视图与左视图）、宽相等（俯视图与左视图）。",
            "proof": "把立体放进长方体盒子里（长 $=$ 左右、宽 $=$ 前后、高 $=$ 上下）。主视图是「正面压扁」：保留长与高；俯视图是「顶上压扁」：保留长与宽；左视图是「左面压扁」：保留宽与高。三张图两两共享一个维度——共享的那一维必须相等：长对正（主与俯共「长」）、高平齐（主与左共「高」）、宽相等（俯与左共「宽」）。",
            "key": "依据是三张视图各自压扁的方向：主视图正面压扁保留长与高，俯视图顶上压扁保留长与宽，左视图左面压扁保留宽与高。两张视图共享的那一维必须相等，否则同一个棱长在两张图上会读出两个数——这是画图时的自检标准，也是由三视图还原立体的依据。",
        },
    ],
    # ================================================== m2-06 图形与变换
    "m2-06-01-symmetry": [
        {
            "conclusion": "轴对称的性质：对称轴垂直平分对应点连线。",
            "proof": "设 $A$ 与 $A'$ 关于直线 $l$ 对称，$M$ 是 $AA'$ 与 $l$ 的交点（图 1 左）。翻折把 $l$ 两侧的半平面互换、$l$ 上每一点原地不动，所以 $A$ 落到 $A'$、$M$ 不动。翻折不改变长度：$MA$ 翻折后等于 $MA'$，即 $M$ 是 $AA'$ 中点；射线 $MA$ 翻折后落在射线 $MA'$ 上，而 $M$ 处翻折不改直线的「直」，两射线合成一条直线，$l\\perp AA'$。于是 $l$ 垂直平分 $AA'$。",
            "key": "依据是轴对称的定义与「翻折不改变长度」：翻折把 $l$ 两侧的半平面互换、$l$ 上每一点原地不动，所以 $A$ 落到 $A'$、$M$ 留在原地。翻折不改变长度给出 $MA=MA'$，而 $M$ 又在 $AA'$ 上，$M$ 到 $AA'$ 两端等距即它是中点；又射线 $MA$ 翻折后落在射线 $MA'$ 上，过 $M$ 的直线翻折后仍是同一条直线，两射线合成一条直线即 $AA'$，而它与 $l$ 成直角——中点加垂直，就是垂直平分。",
        },
        {
            "conclusion": "轴对称图形全等：翻折不改变长度与角度，所以对应边相等、对应角相等。",
            "proof": "翻折是「整体搬运」，每条线段长度不变、每个角大小不变，重合即说明所有对应边、对应角相等——全等（$\\mathrm{SAS}$、$\\mathrm{SSS}$ 等判定都不必动用，翻折本身就是证明）。轴对称是继平移、旋转之后第三种「不改变形状与大小」的搬运方式。",
            "key": "依据是翻折是「整体搬运」：每条线段长度不变、每个角大小不变，翻过去能与自身重合，说明所有对应边、对应角相等——这正是全等的含义，不必再回到 $\\mathrm{SAS}$、$\\mathrm{SSS}$ 去凑判定条件。轴对称是继平移、旋转之后第三种「不改变形状与大小」的搬运方式。",
        },
        {
            "conclusion": "中心对称的性质：对称中心是任意一对对应点连线的中点，旋转 $180^{\\circ}$ 的两图形全等。",
            "proof": "设 $B$ 绕 $O$ 旋转 $180^{\\circ}$ 到 $B'$（图 1 右）。$B$、$O$、$B'$ 共线；$OB$ 旋转 $180^{\\circ}$ 后与原线段反向共线，长度不变，所以 $OB=OB'$ 且方向相反——$O$ 恰是线段 $BB'$ 的中点。对应边 $AB$ 旋转后落在 $A'B'$ 处且等长，故旋转 $180^{\\circ}$ 的两图形全等。",
            "key": "依据是旋转 $180^{\\circ}$ 的效果：点 $B$ 绕 $O$ 转过半圈后与 $B'$ 关于 $O$ 对称，$B$、$O$、$B'$ 落在同一条直线上，且 $OB$ 旋转 $180^{\\circ}$ 后与原线段反向共线、长度不变，所以 $OB=OB'$ 且方向相反，$O$ 恰是 $BB'$ 的中点。整幅图形转过半圈与自身重合，对应边 $AB$ 落到 $A'B'$ 且等长，故两图形全等。",
        },
        {
            "conclusion": "中心对称是旋转 $180^{\\circ}$ 的特例：它拥有旋转的全部性质，又多一条独家性质——对应点连线经过中心且被中心平分。",
            "proof": "旋转 $180^{\\circ}$ 是「转半圈」——旋转角取到平角的特殊情况。所以中心对称拥有旋转的全部性质（对应点到中心等距、对应线段等长），又因「转半圈」多出一条独家性质：对应点连线共点且被平分（旋转 $90^{\\circ}$ 时对应点连线不过中心、更不被平分）。",
            "key": "依据是旋转三要素（中心、角度、方向）里角度取到 $180^{\\circ}$ 的特殊情形：转半圈与一般旋转一样保持到中心的距离、对应线段等长，但只有转半圈时才保证每对对应点的连线都过中心并被它平分——旋转 $90^{\\circ}$ 时连线不过中心、更不被平分，所以这一条是它独有的。",
        },
    ],
    "m2-06-02-translation-rotation": [
        {
            "conclusion": "平移保持线段的长度和方向：$AB\\parallel A'B'$ 且 $AB=A'B'$。",
            "proof": "设平移把 $A\\to A'$、$B\\to B'$。按定义，$AA'$ 与 $BB'$ 同向等长——四边形 $ABB'A'$ 的对边 $AB$ 与 $A'B'$ 也同向等长（每一点位移相同，$B$ 相对 $A$ 的位置向量在移动前后不变），所以 $ABB'A'$ 是平行四边形（m2-03-02 判定），得 $AB\\parallel A'B'$ 且 $AB=A'B'$。",
            "key": "依据是平行四边形的判定（m2-03-02）：平移按定义使 $AA'$ 与 $BB'$ 同向等长，四边形 $ABB'A'$ 的这组对边平行且相等，所以它是平行四边形，平行四边形的另一组对边 $AB$ 与 $A'B'$ 也平行且相等。原文那句「每一点位移相同」是关键——$B$ 相对 $A$ 的位置在移动前后不变，才敢断定这个四边形是平行四边形。",
        },
        {
            "conclusion": "平移保持角度，平移前后的图形全等。",
            "proof": "角由两条射线的方向决定；两条射线被同步搬运后方向都不变（每条线段仍与原线段平行），夹角自然不变。于是平移前后的图形全等——「电梯里的人形」前后能完全重合。",
            "key": "依据是角的大小只由两条射线的方向决定：平移后每条线段仍与原线段平行（上一条的结论），方向没变，两条射线的夹角自然不变；再配上长度也不变，对应边、对应角都相等，图形全等——「电梯里的人形」前后能完全重合就是这个道理。",
        },
        {
            "conclusion": "旋转保持到旋转中心的距离：$OA=OA'$、$OB=OB'$。",
            "proof": "旋转是绕 $O$ 的刚体转动，$A$ 走过的轨迹是以 $O$ 为圆心、$OA$ 为半径的圆弧，半径全程不变，故 $OA=OA'$。同理 $OB=OB'$。",
            "key": "依据是旋转中「到中心的距离」这一条不变量：点 $A$ 沿以 $O$ 为圆心、$OA$ 为半径的圆弧移动，这个半径就是它到 $O$ 的距离，全程不变，落到 $A'$ 上自然有 $OA=OA'$；$B$ 同理。这是后面用 SAS 判定旋转前后图形全等的前提。",
        },
        {
            "conclusion": "同一个旋转里所有点转过的角度都相等：$\\angle AOA'=\\angle BOB'=\\alpha$，且旋转前后的图形全等。",
            "proof": "设旋转把 $A\\to A'$、$B\\to B'$。$\\triangle OAB$ 与 $\\triangle OA'B'$ 中 $OA=OA'$、$OB=OB'$；把 $\\triangle OAB$ 绕 $O$ 转 $\\alpha$ 恰落在 $\\triangle OA'B'$ 上（这就是旋转的定义），两边一夹角全等（$\\mathrm{SAS}$，m2-02-02），故 $\\angle AOB=\\angle A'OB'$、$AB=A'B'$。于是 $\\angle AOA'=\\angle BOB'=\\alpha$（各等于 $\\angle AOB+\\angle BOA'$ 型的同一圈角），对应线段相等、图形全等。",
            "key": "依据是 SAS 判定（m2-02-02）：$OA=OA'$、$OB=OB'$ 由半径不变给出，把 $\\triangle OAB$ 绕 $O$ 转 $\\alpha$ 恰落在 $\\triangle OA'B'$ 上（这正是旋转的定义），两组边相等加夹角相等，三角形全等，于是 $\\angle AOB=\\angle A'OB'$、$AB=A'B'$ 随之得出。$\\angle AOA'=\\angle BOB'$ 则由「同一圈上的和」得出：$\\angle AOA'=\\angle AOB+\\angle BOA'$，$\\angle BOB'=\\angle BOA'+\\angle A'OB'$，而全等已给出 $\\angle AOB=\\angle A'OB'$，两个式子的右边相等，故 $\\angle AOA'=\\angle BOB'=\\alpha$。",
        },
    ],
    "m2-06-03-transform-coordinates": [
        {
            "conclusion": "平移的坐标规律：$(x,y)\\to(x+a,\\ y+b)$，横坐标同加、纵坐标同加。",
            "proof": "设平移向右 $a$、向上 $b$。每个点位移相同，横坐标一律加 $a$、纵坐标一律加 $b$——对应点连线段平行且相等（m2-06-02 平移性质），在坐标系里读出来就是「横同加、纵同加」，$(x,y)\\to(x+a,\\ y+b)$。",
            "key": "依据是平移的坐标意义：每个点位移相同，向右 $a$ 就使所有点的横坐标一律加 $a$，向上 $b$ 就使所有点的纵坐标一律加 $b$。这与平移保持长度方向（m2-06-02）完全一致——对应点连线段平行且相等，在坐标系里读出来就是两个坐标各自加同一个数。",
        },
        {
            "conclusion": "关于坐标轴对称的坐标规律：关于 $x$ 轴对称得 $(x,\\ -y)$，关于 $y$ 轴对称得 $(-x,\\ y)$。",
            "proof": "设 $P(x,y)$ 与 $P'$ 关于 $x$ 轴对称。对称轴垂直平分对应点连线：$PP'\\perp x$ 轴（连线竖直，横坐标相同，$x'=x$），且 $x$ 轴过 $PP'$ 中点（$\\tfrac{y+y'}{2}=0$，即 $y'=-y$）——得 $(x,\\ -y)$。关于 $y$ 轴同理得 $(-x,\\ y)$。",
            "key": "依据是轴对称垂直平分对应点连线（m2-06-01）：$PP'\\perp x$ 轴说明连线竖直，横坐标相同，$x'=x$；$x$ 轴过 $PP'$ 中点说明中点纵坐标是 $0$，即 $\\tfrac{y+y'}{2}=0$，故 $y'=-y$。关于 $y$ 轴同理：连线水平故纵坐标不变，$y'=y$；中点横坐标为 $0$，$x'=-x$。规律是「垂直于对称轴的那个坐标分量不变号」。",
        },
        {
            "conclusion": "关于原点对称的坐标规律：$(x,y)\\to(-x,\\ -y)$，它等于先关于 $x$ 轴再关于 $y$ 轴的两次复合。",
            "proof": "点 $P(x,y)$ 绕原点旋转 $180^{\\circ}$（中心对称）：对应点与 $O$ 共线且 $O$ 平分连线段——$\\tfrac{x+x'}{2}=0$、$\\tfrac{y+y'}{2}=0$，得 $(-x,\\ -y)$。也可看成「关于 $x$ 轴再关于 $y$ 轴」两步复合：$(x,y)\\to(x,\\ -y)\\to(-x,\\ -y)$——两次翻面等价于转半圈。",
            "key": "依据是中心对称时原点平分对应点连线（m2-06-01）：$\\tfrac{x+x'}{2}=0$、$\\tfrac{y+y'}{2}=0$，两个坐标同时取负。而先关于 $x$ 轴再关于 $y$ 轴：$(x,y)\\to(x,\\ -y)\\to(-x,\\ -y)$，结果相同——两次翻面等价于转半圈，这从计算上又验证了一次上一条。",
        },
        {
            "conclusion": "折叠问题中的相等关系都来自轴对称：翻折前后全等，每对对应边、对应角都是不变量，折痕还给出「落点」的位置约束。",
            "proof": "折叠是轴对称，翻折前后全等——折叠涉及的每对对应边、对应角都是不变量；折痕垂直平分对应点连线给出「落点」的位置约束。把不变量与新图形中可用勾股的直角三角形拼起来，就得到方程（例 2：折叠角相等证出等腰，勾股列方程解出重叠区域）。",
            "key": "依据是轴对称的两条性质（m2-06-01）：折叠是轴对称，翻折前后图形全等，所以每对对应边、对应角都是不变量，是折叠题里「证等腰」「证相等」的直接依据；折痕垂直平分对应点连线，又限定了落点的位置。折叠题要的往往是一个新长度，而新图形里往往正好有一个可用勾股定理（m2-02-05）算的直角三角形，把不变量搬进去就列得出方程。",
        },
    ],
    "m2-06-04-geometric-extremum": [
        {
            "conclusion": "将军饮马模型：$A'$ 是 $A$ 关于 $l$ 的对称点时，$AP+PB\\geqslant A'B$，等号当且仅当 $P$ 在线段 $A'B$ 上。",
            "proof": "设 $A'$ 是 $A$ 关于 $l$ 的对称点，$P$ 为 $l$ 上任意一点。对称轴垂直平分 $AA'$，$l$ 上每点到 $A$、$A'$ 距离相等（m2-01-05 的中垂线性质），故 $AP=A'P$，$AP+PB=A'P+PB$。路径 $A'\\to P\\to B$ 是一条折线，而两点之间线段最短：$A'P+PB\\geqslant A'B$，等号当且仅当 $P$ 落在线段 $A'B$ 上（图 1 左红线）。",
            "key": "依据是垂直平分线的性质（m2-01-05）加上「两点之间线段最短」：$l$ 是 $AA'$ 的垂直平分线，所以 $l$ 上任一点 $P$ 到 $A$、$A'$ 距离相等，$AP$ 才能换成 $A'P$，路径长保持不变。随后用的是两点之间线段最短：$A'\\to P\\to B$ 是折线，其长度不小于直线段 $A'B$，等号当且仅当三点共线且 $P$ 在 $A'B$ 之间。",
        },
        {
            "conclusion": "等号能取到：$P$ 取 $l$ 与线段 $A'B$ 的交点时，最小值就是 $A'B$。",
            "proof": "$P$ 是 $l$ 与线段 $A'B$ 的交点——存在且唯一（$A'$ 与 $B$ 分居 $l$ 两侧，线段必穿过 $l$）。所以最小值不只是「大于等于」，而是可以取到的 $A'B$。",
            "key": "依据是「线段与直线的位置关系」：$A$ 与 $A'$ 关于 $l$ 对称，$A'$ 与 $B$ 分居 $l$ 两侧，所以线段 $A'B$ 必与 $l$ 相交，交点存在且唯一。于是下界不是一句空话，而是实实在在能达到的最小值 $A'B$——这正是「化归为两点之间距离」比直接硬算要省力的原因。",
        },
        {
            "conclusion": "造桥选址：桥的长度和方向固定时，把 $A$ 平移成 $A'=A+(0,\\ a)$ 就有 $AP+PQ+QB\\geqslant A'B+a$，等号当 $Q$ 在线段 $A'B$ 上。",
            "proof": "桥向量 $\\vec{PQ}=(0,\\ a)$ 固定。把 $A$ 平移成 $A'=A+(0,\\ a)$，则 $AP=A'Q$（两线段是同一向量下的平移对应），于是 $AP+PQ+QB=A'Q+QB+a\\geqslant A'B+a$——等号当 $Q$ 在线段 $A'B$ 上。定长 $a$ 是「常数项」，平移把它提出来后剩下的又回到线段最短。",
            "key": "依据是「平移消元」：桥的长度和方向都是固定的，把 $A$ 沿同一方向平移同样距离得 $A'$，$AP$ 与 $A'Q$ 是同一次平移下的对应线段，所以 $AP=A'Q$，于是总长 $AP+PQ+QB$ 中的 $PQ$ 被拆成 $A'Q$ 与常数 $a$，剩下的问题又回到「两点之间线段最短」：$A'Q+QB\\geqslant A'B$。定长 $a$ 是常数项，平移把它提出来后不影响取等条件。",
        },
        {
            "conclusion": "定边定角求轨迹：$\\angle APB=90^{\\circ}$ 时 $P$ 的轨迹是以 $AB$ 为直径的圆（去掉 $A$、$B$ 两点）；锁定这个圆后，定点 $Q$ 到圆上动点 $P$ 的距离满足 $|QO-r|\\leqslant QP\\leqslant QO+r$，最值在三点共线时取到。",
            "proof": "设 $\\angle APB=90^{\\circ}$，$O$ 为 $AB$ 中点。直角三角形斜边上的中线等于斜边一半（m2-04-01）：$OP=\\tfrac12 AB$，为定值——$P$ 到定点 $O$ 距离恒等于定长 $\\tfrac{AB}{2}$，轨迹是以 $AB$ 为直径的圆（去掉 $A$、$B$ 两点）。反之，直径上的圆周角是直角（m2-04-02），圆上（除端点外）每点都满足 $\\angle APB=90^{\\circ}$——条件与轨迹严丝合缝。锁定圆后，定点 $Q$ 到圆上动点 $P$ 的距离满足 $|QO-r|\\leqslant QP\\leqslant QO+r$——这正是三角形三边关系（两边之和大于等于第三边、两边之差小于等于第三边，等号都在三点共线时取得，m2-02-01）：$Q$、$O$、$P$ 三点共线时取到两端，最值就是 $d\\mp r$。",
            "key": "依据是直角三角形斜边上的中线等于斜边的一半（m2-04-01）：$O$ 是 $AB$ 中点，所以 $OP=\\tfrac12 AB$ 是定长，$P$ 到定点 $O$ 的距离被锁死，轨迹就是以 $O$ 为圆心、$\\tfrac{AB}{2}$ 为半径的圆——也就是以 $AB$ 为直径的圆；反过来「直径上的圆周角是直角」（m2-04-02）保证圆上每点都满足条件，条件与轨迹正好吻合。锁定圆后，$QP$ 的取值范围由三角形三边关系（m2-02-01）给出：两边之和大于等于第三边、两边之差小于等于第三边，等号都在三点共线时取得，故最值是 $d\\mp r$。",
        },
    ],
}

# ---------------------------------------------------------------- 校验与写盘
FORBIDDEN = ("显然", "易证", "不难看出")
BARE_TEX = ("frac", "times", "cdot", "circ", "angle", "triangle", "sqrt",
            "perp", "parallel", "geqslant", "leqslant", "tfrac", "overrightarrow")


def bare_tex_check(pid, field, v):
    """$ 之外不得出现裸 TeX 命令（audit_site.py 同款规则）。"""
    import re
    stripped = re.sub(r"\$[^$]*\$", "", v)
    for cmd in BARE_TEX:
        if "\\" + cmd in stripped:
            return f"{pid}.{field}: $ 外有 TeX 命令 \\{cmd}"
    return None


def load_original():
    """取回原始 steps。有备份用备份；无备份则从现文件的 proof 字段反推。"""
    if ORIG_FILE.exists():
        return json.loads(ORIG_FILE.read_text(encoding="utf-8"))
    out = {}
    for pid in STEPS:
        d = json.loads((C / f"{pid}.json").read_text(encoding="utf-8"))
        st = d["sections"]["why"]["steps"]
        if st and isinstance(st[0], dict):
            out[pid] = [s["proof"] for s in st]
        else:
            out[pid] = st
    return out


def main(dry_run=False):
    orig = load_original()
    assert set(orig) == set(STEPS), "备份与新内容篇目不一致"
    total = 0
    problems = []
    for pid, steps in STEPS.items():
        old = orig[pid]
        if len(old) != len(steps):
            problems.append(f"{pid}: 原 {len(old)} 步，新 {len(steps)} 条，条数必须一一对应")
            continue
        heads = HEADERS[pid]
        for i, (o, s) in enumerate(zip(old, steps), 1):
            if set(s) != {"conclusion", "proof", "key"}:
                problems.append(f"{pid}[{i}]: 字段必须正好是三项")
                continue
            if not all(v.strip() for v in s.values()):
                problems.append(f"{pid}[{i}]: 存在空字段")
                continue
            # 1) 标签剥离后，proof 必须与原文逐字相等
            #    o 可能是「带标签的原文」（有备份时），也可能是「已剥离的 proof」
            #    （无备份时从现文件反推），两种都要能对上。
            head = heads[i - 1]
            if head and o.startswith(head):
                body = o[len(head):]
            else:
                body = o
            if body != s["proof"]:
                problems.append(f"{pid}[{i}]: proof 与原文不一致\n"
                                f"    原文: {body[:90]}\n    新文: {s['proof'][:90]}")
            # 2) 字段级规矩
            for k, v in s.items():
                if v.startswith("结论 "):
                    problems.append(f"{pid}[{i}].{k}: 不要写编号前缀")
                if "关键一步：" in v:
                    problems.append(f"{pid}[{i}].{k}: 不要重复渲染层的标签")
                for w in FORBIDDEN:
                    if w in v:
                        problems.append(f"{pid}[{i}].{k}: 命中跳步话术「{w}」")
                if v.count("$") % 2:
                    problems.append(f"{pid}[{i}].{k}: $ 不成对（{v.count('$')} 个）")
                if "\\\\\\" in v:
                    problems.append(f"{pid}[{i}].{k}: 含三连反斜杠")
                bad = bare_tex_check(pid, k, v)
                if bad:
                    problems.append(bad)
        if problems:
            continue
        total += len(steps)
        if not dry_run:
            p = C / f"{pid}.json"
            d = json.loads(p.read_text(encoding="utf-8"))
            d["sections"]["why"]["steps"] = steps
            p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{pid}: {len(steps)} 条结论" + ("（dry-run，未写盘）" if dry_run else ""))
    if problems:
        print(f"\n✗ {len(problems)} 处问题：")
        for p in problems:
            print("  ✗", p)
        return 1
    print(f"\n合计 {len(STEPS)} 篇 / {total} 条结论")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(dry_run="--check" in sys.argv))
