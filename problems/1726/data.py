#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1726《矩阵》分层测试数据生成器（cyaron，仓库惯例）
# 用法：g++ -O2 -std=c++17 -Wall std.cpp -o std && mkdir -p data && cd data && python3 ../data.py
# 参考仓库惯例：.ybt-import/staging/1724/data.py、1725/data.py、1222/data.py。
#
# 题意（content.md 明文）：n×m 矩阵初始全 0，可对任一行/任一列整体 +1 或 -1（次数不限、可抵消）。
#   记第 i 行净操作数为 r_i、第 j 列净操作数为 c_j（均为任意整数），则限制 (x,y,k) 化为
#       r_x + c_y = k 。
#   问是否存在整数 r、c 同时满足全部 k 条限制 ⇒ Yes / No。
#   建模（std.cpp）：行点 x(1..n) 与列点 n+y(1..m)，列点点值取 −c_j ⇒ 限制化为带符号等式
#   「值(x) − 值(n+y) = k」，即二部图上每条闭合交替走法的交替和必须为 0（详见 std.cpp 头注与
#   gen-report.md 的来源列表 —— 本题同 BZOJ 4500）。
#
# 数据范围（content.md）：T ≤ 5；1 ≤ n,m,k ≤ 1000 且 k ≤ n×m；c 题面未给区间（只写"整数 c"）。
#   限制：2000 ms / 256 MB（config.json；官方页实抓 2000 ms / 262144 KB，一致）。
#
# ---- 分层策略（10 个测试点：边界 / 小 / 中 / 大 / 顶格；顶格顶到题面上限 T=5、n=m=1000、k=1000）----
#   点 1  边界层（最小输入）  ：T=1，n=m=k=1，(1,1,0) ⇒ Yes。
#   点 2  边界层（样例回归）  ：题面【输入样例】原样（T=2）⇒ Yes / No，与【输出样例】逐字节对照。
#   点 3  边界层（最小 No）   ：n=1,m=2,k=2，同格 (1,1) 同时要求 0 与 1 ⇒ No。
#   点 4  小规模 Yes          ：n=m=8，k=12，按隐藏整数解 (r,c)∈[-5,5] 反推 ⇒ Yes。
#   点 5  小规模混合          ：T=2；10×10(k=15：隐藏解 + 四元矛盾环) ⇒ No；6×6(k=10 隐藏解) ⇒ Yes。
#   点 6  中等规模 Yes        ：T=5，n=m=100，k=1000×5（密网格 + 同行/同列星型）⇒ 全 Yes。
#   点 7  中大规模 No         ：n=m=500，k=1000，996 条一致 + 四元交替环（交替和 ±1≠0）⇒ No。
#   点 8  大规模 Yes 顶格     ：T=5，n=m=1000，k=1000×5，|c| 含 10^6 大权值 + 重复三元组 ⇒ 全 Yes。
#   点 9  顶格层 No（长环）   ：n=m=1000，k=1000 构成长度 1000 的偶交替环，交替和 = ±1≠0 ⇒ No
#                              （必须读完整组输入才发现矛盾，卡"提前 break 不读完输入"的实现）。
#   点 10 顶格层最坏混合      ：T=5，n=m=1000/k=1000，Yes/No 交替；含 n=1 单行、m=1 单列退化形状、
#                              同行/同列密集星型、重复边、"同格两值"直接矛盾、长度 998 的矛盾环。
#
# ---- 数据正确性保证（生成期证书自检；**不使用任何 brute / 对拍 / stress**）----
#   · Yes 组：按隐藏整数解 (r,c) 反推每条限制，并逐条复验 r_x + c_y == k（witness 检查，O(k)）；
#     有 witness ⇒ 系统有整数解 ⇒ 答案必为 Yes。
#   · No 组：只用两种可解析证明的矛盾结构，并显式复算证书：
#       (a) 同一格 (x,y) 出现两个不同 k ⇒ 直接矛盾（点 3、点 10-2）；
#       (b) 偶交替环 交替和 Σ(k_{i,i} − k_{i+1,i}) ≠ 0 ⇒ 沿环累加约束得 0 = 交替和 ≠ 0，矛盾
#           （点 5、点 7、点 9、点 10-5）；生成期断言交替和确为非零整数。
#   · 生成后用"构造期望"断言 std 刚写出的 .out 内容（期望来自上述证书，与 std 算法无关）。
#   · 随机部分固定种子，完全可复现。

import os
import random
import sys

from cyaron import IO

MAXK = 1000          # k 上限（题面）
MAXNM = 1000         # n、m 上限（题面）
MAXT = 5             # T 上限（题面）
BIGC = 1000000       # 大权值 c 的量级（题面未给 c 区间，取 10^6，见 gen-report.md 风险点）

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(OUT_DIR, "std")


# ============================ 构造工具与证书自检 ============================

def check_witness(n, m, cons, r, c, tag):
    """Yes 组证书：隐藏整数解 (r,c) 必须满足全部限制 ⇒ 答案必为 Yes。O(k)。"""
    for x, y, k in cons:
        assert 1 <= x <= n and 1 <= y <= m, "%s: 坐标越界 (%d,%d)" % (tag, x, y)
        assert r[x] + c[y] == k, "%s: witness 违约 (%d,%d,%d) r=%d c=%d" % (
            tag, x, y, k, r[x], c[y])


def even_cycle_cells(rows, cols):
    """偶交替环的 2p 个格子：(r1,c1),(r2,c1),(r2,c2),...,(rp,cp),(r1,cp)。
    rows/cols 长度均为 p、元素各自互异（p ≥ 2），故 2p 个格子互异。"""
    p = len(rows)
    assert p >= 2 and len(set(rows)) == p and len(set(cols)) == p
    cells = []
    for i in range(p):
        cells.append((rows[i], cols[i]))            # k_{i,i}
        cells.append((rows[(i + 1) % p], cols[i]))  # k_{i+1,i}（i = p-1 时即 (r1,cp)）
    assert len(set(cells)) == 2 * p
    return cells


def even_cycle_alt_sum(cells, kmap):
    """环交替和 Σ_i (k_{i,i} − k_{i+1,i})。为 0 是可行必要条件；≠ 0 ⇒ 必 No。O(len)。"""
    p = len(cells) // 2
    s = 0
    for i in range(p):
        s += kmap[cells[2 * i]] - kmap[cells[2 * i + 1]]
    return s


def make_no_group(n, m, p, seed_rows, seed_cols, inject=True, seed_rc=0, lo=-1000, hi=1000):
    """构造一个"隐藏解一致 + 偶交替环被扰动"的 No 组（k = 2p）。

    证书：交替和 ≠ 0（扰动一格使其偏 ±1）⇒ 必 No。返回 (n, m, cons, "No", alt)。
    """
    r, c = hidden_rc(n, m, seed_rc, lo=lo, hi=hi)
    rows = random.Random(seed_rows).sample(range(1, n + 1), p)
    cols = random.Random(seed_cols).sample(range(1, m + 1), p)
    cells = even_cycle_cells(rows, cols)
    kmap = {}
    for x, y in cells:
        kmap[(x, y)] = r[x] + c[y]
    alt = 0
    if inject:
        kmap[cells[1]] += 1                     # 单独扰动一项 ⇒ 交替和 = ±1 ≠ 0
        alt = even_cycle_alt_sum(cells, kmap)
        assert alt != 0, "No 证书失效：交替和 %d" % alt
    cons = [(x, y, kmap[(x, y)]) for x, y in cells]
    assert len(cons) == 2 * p and len(cons) <= n * m
    return n, m, cons, "No", alt, kmap


def append_consistent(cons, kmap, used, n, m, k, r, c, seed, pool=None):
    """向 cons 补齐到 k 条限制：新增格子取隐藏解值（与已有 kmap 不冲突）。O(k)。"""
    rng = random.Random(seed)
    guard = 0
    while len(cons) < k and guard < 50:
        guard += 1
        for x, y, v in consistent_cells(n, m, k - len(cons) + 3, r, c, rng, pool=pool):
            if (x, y) in used or (x, y) in kmap:
                continue
            used.add((x, y))
            kmap[(x, y)] = v
            cons.append((x, y, v))
            if len(cons) == k:
                break
    assert len(cons) == k, "补齐失败：%d/%d" % (len(cons), k)
    return cons


def hidden_rc(n, m, seed, lo=0, hi=0):
    """随机隐藏整数解 r[1..n]、c[1..m]（闭区间 [lo,hi]；lo==hi==0 即全 0）。"""
    rng = random.Random(seed)
    r = [0] * (n + 1)
    c = [0] * (m + 1)
    for i in range(1, n + 1):
        r[i] = rng.randint(lo, hi)
    for j in range(1, m + 1):
        c[j] = rng.randint(lo, hi)
    return r, c


def distinct_cells(n, m, k, rng):
    """从 n×m 个格子中不放回抽 k 个（O(k)，不建全网格）。返回 [(x,y),...]。"""
    assert k <= n * m
    ids = rng.sample(range(n * m), k)
    return [(i // m + 1, i % m + 1) for i in ids]


def consistent_cells(n, m, k, r, c, rng, pool=None):
    """取 k 个互异格子（pool 非空时优先复用，以制造同行/同列星型结构），值取 r_x + c_y。O(k)。"""
    cells = []
    seen = set()
    if pool:
        tries = 0
        while len(cells) < k and tries < 30 * k:
            x, y = pool[rng.randrange(len(pool))]
            tries += 1
            if (x, y) not in seen:
                seen.add((x, y))
                cells.append((x, y))
    if len(cells) < k:                        # 兜底：用互异随机格子补足
        for x, y in distinct_cells(n, m, k, rng):
            if (x, y) not in seen:
                seen.add((x, y))
                cells.append((x, y))
            if len(cells) == k:
                break
    assert len(cells) == k, "取格失败：%d/%d" % (len(cells), k)
    return [(x, y, r[x] + c[y]) for x, y in cells]


def dup_cons(cons, times, rng):
    """随机把若干条已有限制重复一次（覆盖带权并查集"同集合已连通"分支）。O(k)。"""
    idxs = set(rng.sample(range(len(cons)), min(times, len(cons))))
    out = []
    for i, item in enumerate(cons):
        out.append(item)
        if i in idxs:
            out.append(item)
    return out


# ============================ 10 个测试点 ============================

def build_points():
    points = []

    # ---- 点 1：边界层（最小输入，Yes）----
    g1 = (1, 1, [(1, 1, 0)], "Yes")
    check_witness(1, 1, g1[2], [0, 0], [0, 0], "点1")
    points.append(("边界层：T=1，n=m=k=1，限制 (1,1,0) ⇒ Yes（最小合法输入）", [g1]))

    # ---- 点 2：边界层（题面样例原样回归）----
    g2a = (2, 2, [(1, 1, 0), (1, 2, 0), (2, 1, 2), (2, 2, 2)], "Yes")
    g2b = (2, 2, [(1, 1, 0), (1, 2, 0), (2, 1, 2), (2, 2, 1)], "No")
    check_witness(2, 2, g2a[2], [0, 0, 2], [0, 0, 0], "点2a")     # r=(0,2), c=(0,0)
    kmap2 = {}
    for x, y, k in g2b[2]:
        kmap2[(x, y)] = k
    alt2 = even_cycle_alt_sum([(1, 1), (2, 1), (2, 2), (1, 2)], kmap2)   # (0-2) + (1-0) = -1
    assert alt2 != 0, "点2b 证书失效：交替和 %d" % alt2
    points.append(("边界层：题面【输入样例】原样回归（T=2）⇒ Yes/No（与【输出样例】逐字节对照；"
                   "第 2 组交替和=%d≠0）" % alt2,
                   [g2a, g2b]))

    # ---- 点 3：边界层（最小 No：同格两值直接矛盾）----
    g3 = (1, 2, [(1, 1, 0), (1, 1, 1)], "No")
    seen3 = {}
    for x, y, k in g3[2]:
        assert (x, y) not in seen3 or seen3[(x, y)] != k, "点3 证书失效"
        seen3[(x, y)] = k
    assert len(seen3) == 1                            # 证书：同格 (1,1) 被要求两个值
    points.append(("边界层：n=1,m=2,k=2，同格 (1,1) 同时要求 0 与 1 ⇒ No（最小 No）", [g3]))

    # ---- 点 4：小规模 Yes（隐藏解）----
    r4, c4 = hidden_rc(8, 8, 172604, lo=-5, hi=5)
    cons4 = consistent_cells(8, 8, 12, r4, c4, random.Random(172_604_1))
    check_witness(8, 8, cons4, r4, c4, "点4")
    points.append(("小规模 Yes：n=m=8，k=12，隐藏整数解 (r,c)∈[-5,5] 反推 ⇒ Yes", [(8, 8, cons4, "Yes")]))

    # ---- 点 5：小规模混合（T=2）----
    n5, m5, p5 = 10, 10, 5                              # 环上 2p = 10 格
    n5, m5, cons5a, want5a, alt5, kmap5 = make_no_group(
        n5, m5, p5, seed_rows=172_605_1, seed_cols=172_605_2, seed_rc=172605, lo=-3, hi=3)
    r5, c5 = hidden_rc(n5, m5, 172605, lo=-3, hi=3)
    cons5a = append_consistent(cons5a, kmap5, set(kmap5), n5, m5, 15, r5, c5, 172_605_3)
    g5a = (n5, m5, cons5a, "No")

    r5b, c5b = hidden_rc(6, 6, 172_605_4, lo=-4, hi=4)
    cons5b = consistent_cells(6, 6, 10, r5b, c5b, random.Random(172_605_5))
    check_witness(6, 6, cons5b, r5b, c5b, "点5b")
    g5b = (6, 6, cons5b, "Yes")
    points.append(("小规模混合：T=2；10×10(k=15：隐藏解 + 10 格交替环（5 行×5 列，交替和=%d≠0) ⇒ No；"
                   "6×6(k=10 纯隐藏解) ⇒ Yes" % alt5, [g5a, g5b]))

    # ---- 点 6：中等规模 Yes（T=5，n=m=100，k=1000，星型结构）----
    grp6 = []
    for t in range(5):
        n, m = 100, 100
        r, c = hidden_rc(n, m, 172606 + t, lo=-1000, hi=1000)
        rng = random.Random(172_606_100 + t)
        pool = [(rng.randint(1, 5), rng.randint(1, m)) for _ in range(60)] + \
               [(rng.randint(1, n), rng.randint(1, 3)) for _ in range(40)]
        cons = consistent_cells(n, m, MAXK, r, c, rng, pool=pool)
        check_witness(n, m, cons, r, c, "点6-%d" % (t + 1))
        grp6.append((n, m, cons, "Yes"))
    points.append(("中等规模 Yes：T=5，n=m=100，k=1000×5（密网格 + 同行/同列星型）⇒ 全 Yes", grp6))

    # ---- 点 7：中大规模 No（995 条一致 + 四元矛盾环 ⇒ k=1000）----
    n7, m7 = 500, 500
    r7, c7 = hidden_rc(n7, m7, 172607, lo=-500, hi=500)
    rows7 = random.Random(172_607_1).sample(range(1, n7 + 1), 2)
    cols7 = random.Random(172_607_2).sample(range(1, m7 + 1), 2)
    cells7 = even_cycle_cells(rows7, cols7)
    kmap7 = {}
    for x, y in cells7:
        kmap7[(x, y)] = r7[x] + c7[y]
    kmap7[cells7[1]] += 1
    alt7 = even_cycle_alt_sum(cells7, kmap7)
    assert alt7 != 0
    cons7 = [(x, y, kmap7[(x, y)]) for x, y in cells7]
    cons7 = append_consistent(cons7, kmap7, set(cells7), n7, m7, MAXK, r7, c7, 172_607_3)
    assert len(cons7) == MAXK and len(cons7) <= n7 * m7
    points.append(("中大规模 No：n=m=500，k=1000（4 条矛盾环边 交替和=%d≠0 + 996 条一致边）⇒ No"
                   % alt7, [(n7, m7, cons7, "No")]))

    # ---- 点 8：大规模 Yes 顶格（T=5，n=m=1000，k=1000，大权值 + 重复三元组）----
    grp8 = []
    for t in range(5):
        n, m = MAXNM, MAXNM
        lo, hi = (-BIGC, BIGC) if t == 0 else (-10000, 10000)
        r, c = hidden_rc(n, m, 172608 + t, lo=lo, hi=hi)
        rng = random.Random(172_608_100 + t)
        cons = consistent_cells(n, m, 960, r, c, rng)
        cons = dup_cons(cons, 40, rng)                # 960 + 40 = 1000，含重复三元组
        assert len(cons) == MAXK, len(cons)
        check_witness(n, m, cons, r, c, "点8-%d" % (t + 1))
        grp8.append((n, m, cons, "Yes"))
    points.append(("大规模 Yes 顶格：T=5，n=m=1000，k=1000×5，|c| 含 10^6、含重复三元组 ⇒ 全 Yes",
                   grp8))

    # ---- 点 9：顶格层 No（长度 1000 的偶交替环 ⇒ 交替和 = ±1 ≠ 0）----
    t9 = make_no_group(MAXNM, MAXNM, MAXK // 2, seed_rows=172_609_1, seed_cols=172_609_2,
                       seed_rc=172609, lo=-100, hi=100)
    n9, m9, cons9, want9, alt9, _kmap9 = t9
    points.append(("顶格层 No：n=m=1000，k=1000 构成长度 1000 的偶交替环，交替和=%d≠0 ⇒ No"
                   "（须读完整组输入才发现矛盾）" % alt9, [(n9, m9, cons9, want9)]))

    # ---- 点 10：顶格层最坏混合（T=5，Yes/No 交替 + 退化形状）----
    grp10 = []
    # (10-1) n=1 单行退化，k=1000=n*m 铺满全格，隐藏解 ⇒ Yes
    n, m = 1, MAXNM
    r, c = hidden_rc(n, m, 172610, lo=-BIGC, hi=BIGC)
    cons = consistent_cells(n, m, MAXK, r, c, random.Random(172_610_1))
    check_witness(n, m, cons, r, c, "点10-1")
    assert len(cons) == MAXK == n * m
    grp10.append((n, m, cons, "Yes"))
    # (10-2) n=1 单行 + 同格两值直接矛盾 ⇒ No（显式构造，不依赖随机抽取顺序或 std 行为）
    base = grp10[0][2]
    kmap10 = {}
    for x, y, k in base:
        kmap10[(x, y)] = k
    assert (1, 1) in kmap10 and (1, 2) in kmap10
    v11 = kmap10[(1, 1)]
    # 拿走 (1,1)、(1,2) 两条，换回两条 (1,1) 且 k 不同 ⇒ k 仍为 1000，且同格直接矛盾
    cons = [t for t in base if t[:2] not in ((1, 1), (1, 2))] + [(1, 1, v11), (1, 1, v11 + 1)]
    assert len(cons) == MAXK, len(cons)
    ks_at_11 = set(k for x, y, k in cons if (x, y) == (1, 1))
    assert ks_at_11 == {v11, v11 + 1}, "点10-2 证书失效：%s" % ks_at_11
    grp10.append((1, m, cons, "No"))
    # (10-3) m=1 单列退化，隐藏解 + 100 条重复边 ⇒ Yes
    n, m = MAXNM, 1
    r, c = hidden_rc(n, m, 172611, lo=-1000, hi=1000)
    rng = random.Random(172_611_1)
    cons = dup_cons(consistent_cells(n, m, 900, r, c, rng), 100, rng)
    assert len(cons) == MAXK and len(cons) <= n * m
    check_witness(n, m, cons, r, c, "点10-3")
    grp10.append((n, m, cons, "Yes"))
    # (10-4) n=m=1000 顶格，同行/同列密集星型（隐藏解）⇒ Yes
    n, m = MAXNM, MAXNM
    r, c = hidden_rc(n, m, 172612, lo=-1000, hi=1000)
    rng = random.Random(172_612_1)
    pool = [(rng.randint(1, 4), rng.randint(1, m)) for _ in range(300)] + \
           [(rng.randint(1, n), rng.randint(1, 4)) for _ in range(300)]
    cons = consistent_cells(n, m, MAXK, r, c, rng, pool=pool)
    check_witness(n, m, cons, r, c, "点10-4")
    grp10.append((n, m, cons, "Yes"))
    # (10-5) n=m=1000 顶格，长度 998 的矛盾环 + 2 条一致边 ⇒ No
    n, m, p = MAXNM, MAXNM, 499
    t10 = make_no_group(n, m, p, seed_rows=172_613_1, seed_cols=172_613_2,
                        seed_rc=172613, lo=-1000, hi=1000)
    _n, _m, cons, _w, alt10, kmap10 = t10
    r, c = hidden_rc(n, m, 172613, lo=-1000, hi=1000)
    cons = append_consistent(cons, kmap10, set(kmap10), n, m, MAXK, r, c, 172_613_3)
    assert len(cons) == MAXK
    grp10.append((n, m, cons, "No"))
    points.append(("顶格层最坏混合：T=5，n=m=1000/k=1000（含 n=1 单行、m=1 单列退化形状、同行/同列"
                   "星型、重复边、同格两值矛盾、长度 998 矛盾环 交替和=%d≠0），答案 Yes/No 交替"
                   % alt10, grp10))

    return points


# ============================ 生成 + 自检 ============================

def main():
    if not os.path.exists(STD):
        raise SystemExit("找不到 std 二进制：%s\n请先执行 g++ -O2 -std=c++17 -Wall std.cpp -o std" % STD)

    points = build_points()
    assert len(points) == 10, "必须恰好 10 个测试点"

    # ---------- 全量范围自检（题面约束）----------
    n_yes = n_no = 0
    for idx, (note, data) in enumerate(points, 1):
        assert 1 <= len(data) <= MAXT, "点 %d 组数 %d 越界" % (idx, len(data))
        cy = cn = 0
        for n, m, cons, want in data:
            assert 1 <= n <= MAXNM and 1 <= m <= MAXNM, "点 %d n/m 越界 %d %d" % (idx, n, m)
            assert 1 <= len(cons) <= MAXK, "点 %d k=%d 越界" % (idx, len(cons))
            assert len(cons) <= n * m, "点 %d k>n*m" % idx
            for x, y, k in cons:
                assert 1 <= x <= n and 1 <= y <= m, "点 %d 坐标越界 (%d,%d)" % (idx, x, y)
                assert abs(k) <= 10 * BIGC, "点 %d c 越界 %d" % (idx, k)
            assert want in ("Yes", "No")
            cy += want == "Yes"
            cn += want == "No"
        n_yes += cy
        n_no += cn
        print("problem%-2d: T=%d n∈[%d,%d] m∈[%d,%d] k∈[%d,%d]  Yes=%d No=%d -- %s" % (
            idx, len(data),
            min(g[0] for g in data), max(g[0] for g in data),
            min(g[1] for g in data), max(g[1] for g in data),
            min(len(g[2]) for g in data), max(len(g[2]) for g in data), cy, cn, note))

    all_groups = [g for _note, data in points for g in data]
    all_cons = [t for g in all_groups for t in g[2]]
    # 覆盖自检：边界与顶格都被真实使用，答案非单一
    assert min(g[0] for g in all_groups) == 1 and min(g[1] for g in all_groups) == 1, "缺 n=1/m=1"
    assert max(g[0] for g in all_groups) == MAXNM and max(g[1] for g in all_groups) == MAXNM
    assert max(len(g[2]) for g in all_groups) == MAXK and min(len(g[2]) for g in all_groups) == 1
    assert max(len(d) for _n, d in points) == MAXT and min(len(d) for _n, d in points) == 1
    assert n_yes > 0 and n_no > 0
    assert any(len(set((x, y) for x, y, _k in g[2])) < len(g[2]) for g in all_groups), "缺重复格"
    assert any(abs(k) >= BIGC for _x, _y, k in all_cons), "缺大权值 c"
    assert any(k == 0 for _x, _y, k in all_cons), "缺 c=0"
    assert any(k < 0 for _x, _y, k in all_cons), "缺负权值 c"
    print("覆盖自检通过：%d 组 case（Yes=%d, No=%d），总限制 %d 条" % (
        len(all_groups), n_yes, n_no, len(all_cons)))

    # ---------- 写文件 + 构造期望断言 ----------
    for idx, (_note, data) in enumerate(points, 1):
        io = IO(file_prefix="problem", data_id=idx)      # problem{idx}.in / problem{idx}.out
        buf = [str(len(data))]
        for n, m, cons, _want in data:
            buf.append("%d %d %d" % (n, m, len(cons)))
            buf.extend("%d %d %d" % (x, y, k) for x, y, k in cons)
        io.input_write("\n".join(buf) + "\n")
        io.output_gen(STD)
        io.output_file.flush()   # output_gen 写入的是缓冲流，必须先 flush 再回读
        # 用构造期望核对 std 输出（期望来自生成期证书，与 std 算法无关）
        want_all = [g[3] for g in data]
        with open(io.output_filename, encoding="utf-8") as fh:
            got = [ln.strip() for ln in fh if ln.strip()]
        assert got == want_all, "点 %d 输出不符：期望 %s 实得 %s" % (idx, want_all, got)
    print("生成完成并逐点核对：data/problem1..10.in/.out（构造期望 = std 输出）")


if __name__ == "__main__":
    main()
