#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1729《魔法石》数据生成器（cyaron，分层 10 组）
#
# 输入格式（content.md）：
#   第 1 行：T —— 测试组数
#   每组：第 1 行 n m（岛屿数、桥数）
#         随后 m 行 x y c（桥两端 + c=1 表示桥心有魔法石）
#         最后 1 行 src dst（起点、传送门所在岛）
# 输出：T 行，每组一行 YES / NO
#
# 数据范围（题面【提示】）：n,m <= 300000，T <= 10（题面只给上界，未给下界）。
#   本数据集按“英文原题（CF 652E）的保证”从严构造：1<=n、0<=m、无自环、**无重边**，
#   且每组图**连通**（src/dst 可达）；多组数据下每组 n,m 均不超过 3e5。
#
# 分层策略（10 组，从边界铺到顶格；注释见各点）：
#   1  题面样例（T=3）—— 与样例输出 YES/NO/YES 逐行比对
#   2  边界最小层（T=7）：n=1,m=0 全最小 / n=2 单桥有石 / 最小三角含石 / 全 0 链 /
#      无石挂树 / src==dst 可绕回取石 / src==dst 单桥无法返回
#   3  小规模结构化（T=5）：显式手算走法可核（环 / 样例2型陷阱 / 共点双三角 / 悬挂含石边双 / 石在终点块）
#   4  小规模随机 + 不可达石陷阱（T=2）：n=50 随机；n=101 石在桥另一侧 -> 设计 NO
#   5  中等：随机 n=5e3 + 大环（n=5e3，环上恰一条石边，设计 YES）
#   6  中等偏大：n=1e5、m=2e5 随机（树 + 十万补边，p(石)=0.5）
#   7  大规模随机：n=3e5、m=3e5（树 + 补边，p(石)=0.05）
#   8  大规模结构化陷阱（T=2）：n≈3e5 长链（迭代 DFS 深度压测）
#      g1 石边挂在支链上 -> 设计 NO（题面样例 2 的放大版）
#      g2 石边恰在主链路上 + 一条远处弦边 -> 设计 YES
#   9  顶格单组最坏结构：n=m=3e5，哈密顿大环 1-2-...-n-1（整体 2-边连通），
#      唯一石边取 (n,1)，src=n、dst=2 -> 设计 YES（显式走法 n->1->2）
#  10  顶格多组（T=10，每组 n=1e5、m≈1.1e5）-> 1.09e6 边，压测多组复用与清空
#      （末组为“不可达石”NO 结构，见下）
#
# 说明：
#   - 生成全是 O(n+m) 的线性循环，无任何 O(n^2) Python 循环；
#   - 固定随机种子（random.Random(1729+i)），输出逐字节可复现；
#   - **先校验 std 已编译存在**（cyaron 在 std 缺失时会静默产出 0 字节 .out），
#     生成后再断言 .in 结构合法、.out 非空、行数 == T、答案 ∈ {YES,NO}，
#     并对设计上答案确定的点核对期望值；
#   - 本任务铁律禁止 brute/对拍/stress，故本生成器不含任何暴力枚举或随机对拍，
#     设计确定的点均以“显式走法/结构论证”给出期望答案（见注释）。
#
# 运行（在题目目录下）：g++ -O2 -std=c++17 std.cpp -o std && python3 data.py
#   （data.py 自动把 cwd 切到 <本目录>/data，.in/.out 落在此处）

import os
import random
import sys

from cyaron import IO

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
STD = os.path.join(HERE, "std")

MAXN = MAXM = 300000
MAXT = 10

# ---------------------------------------------------------------------------
# 前置守卫：std 必须已编译且可执行，否则立即报错退出
# （cyaron 的 output_gen(std) 在 std 不存在/不可执行时会静默产出 0 字节 .out）
# ---------------------------------------------------------------------------
if (not os.path.isfile(STD)) or os.path.getsize(STD) == 0 or (not os.access(STD, os.X_OK)):
    sys.stderr.write(
        "[data.py] FATAL: 标程 %s 未编译或不可执行，请先运行：\n"
        "  g++ -O2 -std=c++17 std.cpp -o std\n" % STD
    )
    raise SystemExit(2)

os.makedirs(DATA_DIR, exist_ok=True)
os.chdir(DATA_DIR)

# ---------------------------------------------------------------------------
# 造图工具
# ---------------------------------------------------------------------------

def rand_tree_w(rng, n, p1):
    """随机递归树（i 连到 1..i-1 中均匀随机点），边权以概率 p1 取 1。"""
    out = []
    for i in range(2, n + 1):
        out.append((rng.randint(1, i - 1), i, 1 if rng.random() < p1 else 0))
    return out


def rand_extras(rng, n, k, p1, used):
    """k 条随机补边（**简单图**：不造自环、不造重边；used 为已用无序点对集合）。"""
    out = []
    while len(out) < k:
        u = rng.randint(1, n)
        v = rng.randint(1, n)
        if u == v:
            continue
        key = (u, v) if u < v else (v, u)
        if key in used:
            continue
        used.add(key)
        out.append((u, v, 1 if rng.random() < p1 else 0))
    return out


def chain_w(n, wmap):
    """链 1-2-...-n；wmap[(i,i+1)] 给边权，默认 0。"""
    return [(i, i + 1, wmap.get((i, i + 1), 0)) for i in range(1, n)]


def cycle_w(n, wmap):
    """环 1-2-...-n-1；wmap 给指定边权（含 (n,1)）。"""
    out = [(i, i + 1, wmap.get((i, i + 1), 0)) for i in range(1, n)]
    out.append((n, 1, wmap.get((n, 1), 0)))
    return out


def rand_group(rng, n, m, p1):
    """随机单连通简单图：随机树 + 补边（无自环无重边），共 m 条，返回 (n, edges, src, dst)。"""
    assert n - 1 <= m, "随机点要求 m >= n-1 才能连通"
    assert m <= n * (n - 1) // 2, "m 超过简单图上限"
    edges = rand_tree_w(rng, n, p1)
    used = set()
    for (u, v, _c) in edges:
        used.add((u, v) if u < v else (v, u))
    edges += rand_extras(rng, n, m - (n - 1), p1, used)
    src = rng.randint(1, n)
    dst = rng.randint(1, n)
    while dst == src:
        dst = rng.randint(1, n)
    return (n, edges, src, dst)


def build_input(groups):
    """按题面格式拼出完整输入文本（单次 join，无 O(n^2) 操作）。"""
    parts = ["%d\n" % len(groups)]
    for n, edges, src, dst in groups:
        parts.append("%d %d\n" % (n, len(edges)))
        parts.append("".join("%d %d %d\n" % e for e in edges))
        parts.append("%d %d\n" % (src, dst))
    return "".join(parts)


def check_walk(idx, gi, edges, walk, src, dst):
    """证书校验：按 walk 逐步消耗边（多重集），证明存在一条边不重、经过至少一条石边的
    src->dst 路径 => 该组答案必为 YES。
    walk 元素 = (u, v, need_stone)；need_stone=True 要求该步走权 1 的边。
    复杂度 O(|walk|)，与图规模无关；这是对“设计 YES”的**正向证书**验证，不是暴力求解。
    """
    avail = {}
    for (u, v, c) in edges:
        avail.setdefault((min(u, v), max(u, v)), []).append(c)
    cur = src
    saw = False
    for (u, v, need_stone) in walk:
        assert cur == u, "点 %d 组 %d: 走法不连续（现 %d，步起点 %d）" % (idx, gi, cur, u)
        key = (min(u, v), max(u, v))
        lst = avail.get(key)
        assert lst, "点 %d 组 %d: 走法用了不存在/已耗尽的边 %r" % (idx, gi, key)
        if need_stone:
            pick = next((i for i, c in enumerate(lst) if c == 1), None)
            assert pick is not None, "点 %d 组 %d: 该步需权 1 边但不可用" % (idx, gi)
        else:
            pick = 0
        if lst.pop(pick) == 1:
            saw = True
        cur = v
    assert cur == dst, "点 %d 组 %d: 走法未终止于 dst" % (idx, gi)
    assert saw, "点 %d 组 %d: 走法未收集到魔法石" % (idx, gi)


def check_input_file(path, groups_meta):
    """逐行结构校验 .in：T / 每组 n m / m 行 x y c / src dst，并检查取值范围与
    “简单图”不变量（无自环、无重边）及**连通性**（与英文原题保证一致，见 gen-report 第五节）。
    复杂度 O(Σ(n+m))，全程线性，无任何 O(n^2) 逐对检查。
    """
    with open(path, "r") as f:
        first = f.readline().strip()
        assert first == str(len(groups_meta)), "首行 T 不符：%r" % first
        for (n, m) in groups_meta:
            ln = f.readline().split()
            assert len(ln) == 2, "组头行格式错"
            assert int(ln[0]) == n and int(ln[1]) == m, "组头 n m 不符：%r" % ln
            assert 1 <= n <= MAXN and 0 <= m <= MAXM, "n/m 越界"
            seen_pairs = set()
            parent = list(range(n + 1))

            def root(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x

            for _ in range(m):
                x, y, c = f.readline().split()
                x = int(x); y = int(y); c = int(c)
                assert 1 <= x <= n and 1 <= y <= n, "端点越界"
                assert x != y, "出现自环"
                assert c in (0, 1), "c 必须 0/1"
                key = (x, y) if x < y else (y, x)
                assert key not in seen_pairs, "出现重边 %r" % (key,)
                seen_pairs.add(key)
                rx, ry = root(x), root(y)
                if rx != ry:
                    parent[rx] = ry
            assert all(root(v) == root(1) for v in range(2, n + 1)), "图不连通"
            s = f.readline().split()
            assert len(s) == 2, "src dst 行格式错"
            s0 = int(s[0]); s1 = int(s[1])
            assert 1 <= s0 <= n and 1 <= s1 <= n, "src/dst 越界"
        assert f.read().strip() == "", "文件尾部存在多余内容"


def run_point(idx, groups, expected, note, meta, shuffle=True, walks=None):
    """生成第 idx 个测试点：写 .in -> std 生成 .out -> 断言 .out 非空/行数/期望值。
    walks 不为 None 时，对指定组（walk 非 None 的下标）做证书校验，
    以显式边不重走法独立证明其 YES 判定。
    """
    rng = random.Random(1729 + idx)
    if shuffle:
        for g in groups:
            rng.shuffle(g[1])  # 打乱边的输入顺序，避免 std 依赖有序输入
    if walks:
        for gi, w in enumerate(walks):
            if not w:
                continue
            n_, e_, s_, d_ = groups[gi]
            check_walk(idx, gi + 1, e_, w, s_, d_)
    text = build_input(groups)
    io = IO(file_prefix="problem", data_id=idx)
    io.input_write(text)
    io.output_gen("../std")  # 约定：data.py 在 data/ 下运行，标程在上一级
    io.input_file.flush()
    io.output_file.flush()  # cyaron 的 .out 是带缓冲的文件对象，必须先落盘再断言

    in_path = os.path.join(DATA_DIR, "problem%d.in" % idx)
    out_path = os.path.join(DATA_DIR, "problem%d.out" % idx)

    assert os.path.getsize(in_path) > 0, "点 %d: .in 为空" % idx
    assert os.path.isfile(out_path) and os.path.getsize(out_path) > 0, \
        "点 %d: .out 为空（std 是否缺失/崩溃？）" % idx

    check_input_file(in_path, meta)

    with open(out_path) as f:
        toks = f.read().split()
    assert len(toks) == len(groups), \
        "点 %d: .out 行数 %d != T %d" % (idx, len(toks), len(groups))
    assert all(t in ("YES", "NO") for t in toks), "点 %d: 输出非 YES/NO" % idx
    if expected is not None:
        assert len(expected) == len(toks), "点 %d: 期望长度不符" % idx
        for i, (e, got) in enumerate(zip(expected, toks)):
            if e is not None:
                assert e == got, "点 %d: 第 %d 组期望 %s 实得 %s" % (idx, i + 1, e, got)
    print("  problem%-2d ok  T=%-2d lines=%-8s size=%8d B  ans=%s   %s"
          % (idx, len(groups), sum(len(g[1]) for g in groups),
             os.path.getsize(in_path), ",".join(toks[:4]) + ("..." if len(toks) > 4 else ""),
             note))
    return toks


POINT_INFO = []

# ===========================================================================
# 点 1：题面样例（T=3）—— 期望与【输出样例】逐行一致 YES / NO / YES
# ===========================================================================
run_point(1, [
    (6, [(1, 2, 0), (2, 3, 0), (3, 1, 0), (3, 4, 1), (4, 5, 0), (5, 6, 0), (6, 4, 0)], 1, 6),
    (5, [(1, 2, 0), (2, 3, 0), (3, 4, 0), (2, 5, 1)], 1, 4),
    (5, [(1, 2, 0), (2, 3, 0), (3, 1, 0), (3, 4, 0), (4, 5, 1), (5, 3, 0)], 1, 2),
], ["YES", "NO", "YES"], "题面样例", [(6, 7), (5, 4), (5, 6)], shuffle=False,
   walks=[
       [(1, 2, 0), (2, 3, 0), (3, 4, 1), (4, 5, 0), (5, 6, 0)],       # 1->2->3->4(石)->5->6
       None,                                                           # NO 组无证书
       [(1, 3, 0), (3, 4, 0), (4, 5, 1), (5, 3, 0), (3, 2, 0)],        # 绕右侧块取石后到 2
   ])

# ===========================================================================
# 点 2：边界最小层（T=7，全部手算可核）
#   a) n=1,m=0（全最小值，无桥无石），src=dst=1：全图无石 -> NO
#   b) n=2,m=1 单桥有石，src=1,dst=2：只能走这条桥，得石 YES
#   c) n=3 三角含石边 1-2（全 0 无石对照见 f），src=1,dst=3：走 1->2(得石)->3 YES
#      （最小含石 2-边连通块，不经桥的取石走法）
#   d) n=3 全 0 链，src=1,dst=3：全图无石 -> NO
#   e) n=4 三角 + 挂叶，全 0，src=4,dst=1：全图无石 -> NO
#   f) n=3 三角（含石边 1-2），src=dst=1：闭合走法 1->2->3->1 得石 YES
#   g) n=2,m=1 全 0，src=dst=1：无石且无法返回（桥崩塌）-> NO
# ===========================================================================
run_point(2, [
    (1, [], 1, 1),
    (2, [(1, 2, 1)], 1, 2),
    (3, [(1, 2, 1), (2, 3, 0), (3, 1, 0)], 1, 3),
    (3, [(1, 2, 0), (2, 3, 0)], 1, 3),
    (4, [(1, 2, 0), (2, 3, 0), (3, 1, 0), (3, 4, 0)], 4, 1),
    (3, [(1, 2, 1), (2, 3, 0), (3, 1, 0)], 1, 1),
    (2, [(1, 2, 0)], 1, 1),
], ["NO", "YES", "YES", "NO", "NO", "YES", "NO"], "边界最小层",
   [(1, 0), (2, 1), (3, 3), (3, 2), (4, 4), (3, 3), (2, 1)],
   walks=[
       None,                              # n=1,m=0：无石可收，恒 NO
       [(1, 2, 1)],                       # 唯一边即石边
       [(1, 2, 1), (2, 3, 0)],            # 最小三角，取石后到终点
       None,
       None,
       [(1, 2, 1), (2, 3, 0), (3, 1, 0)], # src==dst 绕三角闭合得石
       None,
   ])

# ===========================================================================
# 点 3：小规模结构化（T=3，显式走法可手算核对）
#   a) 4-环 1-2-3-4-1，唯一石边 1-2，src=1,dst=4：走 1->2->3->4（一次用完三条边）YES
#   b) 星形中心 1 连 2/3/4/5 全 0，石边挂在叶子 2 的支链 2-6 上，src=4,dst=5：
#      去 6 必须借道桥 2-6 再原路返回 -> 不可能 YES；且全链路无别的石 -> NO
#      （题面样例第 2 组的同型陷阱）
#   c) 双三角共点：{1,2,3} 石边 1-2，{3,4,5} 全 0，src=4,dst=5：
#      显式走法 4->3->1->2->3->5，五条边各不相同且终点 5，得石 YES
#      （考验“共点合并成同一 2-边连通块”的语义）
#   d) n=6 悬挂含石边双：主链 1-2-3 全 0（src=1,dst=3），桥 (2,4,0) 下挂
#      三角 {4,5,6} 且内含石边 (5,6,1)：石落在桥树上的**分支**里，
#      绕进去需走两遍桥 (2,4) 不可能 -> 设计 NO
#      （比 b) 更狠：石在真正的 2-边连通块内而非桥上，专杀“同连通块有石即 YES”）
#   e) 石在**终点块**（n=6，连通简单图）：三角 A={1,2,3} 全 0（src=1），割边 (3,4,0)，
#      三角 B={4,5,6} 含石边 5-6（dst=6）：走 1->2->3->4->5->6，石边直接落在路上 -> YES
#      （与前四组互补：石在 src 块 / 分支块 / 终点块三种位置都覆盖到）
# ===========================================================================
run_point(3, [
    (4, [(1, 2, 1), (2, 3, 0), (3, 4, 0), (4, 1, 0)], 1, 4),
    (6, [(1, 2, 0), (1, 3, 0), (1, 4, 0), (1, 5, 0), (2, 6, 1)], 4, 5),
    (5, [(1, 2, 1), (2, 3, 0), (3, 1, 0), (3, 4, 0), (4, 5, 0), (5, 3, 0)], 4, 5),
    (6, [(1, 2, 0), (2, 3, 0), (2, 4, 0), (4, 5, 0), (5, 6, 1), (6, 4, 0)], 1, 3),
    (6, [(1, 2, 0), (2, 3, 0), (3, 1, 0), (3, 4, 0), (4, 5, 0), (5, 6, 1), (6, 4, 0)], 1, 6),
], ["YES", "NO", "YES", "NO", "YES"], "小规模结构化",
   [(4, 4), (6, 5), (5, 6), (6, 6), (6, 7)],
   walks=[
       [(1, 2, 1), (2, 3, 0), (3, 4, 0)],                          # 4-环取石到 4
       None,
       [(4, 3, 0), (3, 1, 0), (1, 2, 1), (2, 3, 0), (3, 5, 0)],    # 双三角共点绕行
       None,
       [(1, 2, 0), (2, 3, 0), (3, 4, 0), (4, 5, 0), (5, 6, 1)],    # 石在终点块，路上取石
   ])

# ===========================================================================
# 点 4：小规模随机 + 不可达石陷阱（T=2，均为简单图）
#   g1: n=50/m=100 随机树+补边（p(石)=0.15），由 std 判定（非设计确定）
#   g2: n=101 结构性 NO（简单图，无重边）：
#       A = {1..98} 无石大环 1-2-...-98-1；割边桥 (98,99,0)；
#       B = {99,100,101} 含石三角（石边 99-100）
#       src=1、dst=2（均在 A），设计 NO：石全在 B，而跨入 B 必须来回走割边 (98,99)
#       —— “图里有石但不可达”陷阱，防“有石即 YES”的错解）
# ===========================================================================
rng4 = random.Random(1729 + 4)
n4a = 101
A4 = cycle_w(98, {}) + [(98, 99, 0), (99, 100, 1), (100, 101, 0), (101, 99, 0)]
run_point(4, [rand_group(rng4, 50, 100, 0.15), (n4a, A4, 1, 2)],
          [None, "NO"], "小规模随机+不可达石陷阱", [(50, 100), (n4a, 102)])

# ===========================================================================
# 点 5：中等（T=2）
#   g1: n=5000/m=10000 随机（p(石)=0.2），由 std 判定
#   g2: n=5000 大环（m=5000）+ 唯一石边 (2,3)，src=n、dst=1（设计 YES）：
#       走法 n->n-1->...->3->2 经过石边 (3,2)，再 2->1 到终点，边各用一次 YES
# ===========================================================================
rng5 = random.Random(1729 + 5)
_walk5b = [(i + 1, i, 1 if (i, i + 1) == (2, 3) else 0) for i in range(4999, 1, -1)] + [(2, 1, 0)]
run_point(5, [
    rand_group(rng5, 5000, 10000, 0.2),
    (5000, cycle_w(5000, {(2, 3): 1}), 5000, 1),
], [None, "YES"], "中等规模", [(5000, 10000), (5000, 5000)],
   walks=[None, _walk5b])

# ===========================================================================
# 点 6：中等偏大（T=1）：n=1e5、m=2e5 随机（树 + 1e5+1 条补边，p(石)=0.5）
# ===========================================================================
rng6 = random.Random(1729 + 6)
run_point(6, [rand_group(rng6, 100000, 200000, 0.5)], None, "中等偏大随机",
          [(100000, 200000)])

# ===========================================================================
# 点 7：大规模随机（T=1）：n=3e5、m=3e5（随机递归树 + 1 条补边，p(石)=0.05）
# ===========================================================================
rng7 = random.Random(1729 + 7)
run_point(7, [rand_group(rng7, 300000, 300000, 0.05)], None, "大规模随机",
          [(300000, 300000)])

# ===========================================================================
# 点 8：大规模结构化陷阱（T=2，n≈3e5 长链 -> 迭代 DFS 深度压测，递归写法必爆栈）
#   g1: 链 1-2-...-299999（全 0）+ 支链石边 (2,300000,1)，src=1、dst=299999
#       设计 NO：石在桥 (2,300000) 的另一侧，取石需走两遍该桥，不可能；主链上无石
#   g2: 链 1-2-...-3e5，主链中间边 (150000,150001) 权 1，其余 0，
#       另加一条远处弦边 (5,150000,0)（m=3e5，保持简单图）；src=1、dst=3e5
#       设计 YES：石边是主链上的割边，必经一次；弦边只把 {5..150000} 并成一个无石大边双，
#       不改变结论（同时检验“路径经过无石大边双”不被误判）
# ===========================================================================
V = 299999
_walk8b = [(i, i + 1, 1 if (i, i + 1) == (150000, 150001) else 0) for i in range(1, 300000)]
run_point(8, [
    (V + 1, chain_w(V, {}) + [(2, V + 1, 1)], 1, V),
    (300000, chain_w(300000, {(150000, 150001): 1}) + [(5, 150000, 0)], 1, 300000),
], ["NO", "YES"], "长链陷阱/弦边边双",
   [(V + 1, 299999), (300000, 300000)], walks=[None, _walk8b])

# ===========================================================================
# 点 9：顶格单组最坏结构（n=m=3e5）
#   哈密顿大环 1-2-...-n-1（n 条边 ⇒ n=m=3e5 双顶格，整体 2-边连通）；
#   唯一石边取 (n,1)（环边）；src=n、dst=2
#   设计 YES：显式走法 n->1（走石边，得石）->2（走边 (1,2)），两条边各用一次即到达终点；
#   同时该结构也是 tarjan 迭代深度的最坏情形之一（DFS 沿环走满 n 层）
# ===========================================================================
n9 = 300000
run_point(9, [
    (n9, cycle_w(n9, {(n9, 1): 1}), n9, 2),
], ["YES"], "顶格单组（哈密顿大环）", [(n9, 300000)],
   walks=[[(n9, 1, 1), (1, 2, 0)]])

# ===========================================================================
# 点 10：顶格多组（T=10，每组 n=1e5），合计约 1.1e6 条边，压测多组复用/清空与总规模
#   g1..g9: 随机树 + 补边，m=1.1e5（p(石)=0.1），由 std 判定
#   g10: “不可达石”结构 NO（n=1e5，简单图）：A = {1..99996} 无石大环 + 割边桥 (99996,99997,0)
#        + B = {99997..100000} 含石 4-环（石边 99997-99998）；src=1、dst=2
#        设计 NO（大尺度上重复点 4g2 的陷阱，确保 NO 判定非小数据偶合）
# ===========================================================================
rng10 = random.Random(1729 + 10)
G10 = [rand_group(rng10, 100000, 110000, 0.1) for _ in range(9)]
B10 = cycle_w(99996, {}) + [(99996, 99997, 0)] \
      + [(99997, 99998, 1), (99998, 99999, 0), (99999, 100000, 0), (100000, 99997, 0)]
G10.append((100000, B10, 1, 2))
run_point(10, G10, [None] * 9 + ["NO"], "顶格多组 T=10",
          [(100000, 110000)] * 9 + [(100000, 100001)])

print("[data.py] all 10 points generated & self-checked (std=%s)" % STD)
