#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1739《观光巴士》数据生成器（cyaron）
#
# 用法：
#   cd .ybt-import/staging/1739
#   g++ -O2 -std=c++17 std.cpp -o std     # 生成前必须先编译 std（否则 .out 会是 0 字节）
#   mkdir -p data && cd data && python3 ../data.py
#
# 题面数据范围（content.md）：
#   n <= 1000；每站两条出边（第 i 条线路从 ceil(i/2) 出发）；1 <= e_i <= n；e_i != 起点；
#   0 <= l_i <= 1000；d_i 题面未给上界；每天 24 小时；保证「坐遍所有线路回到 1 号站」的方案存在。
#
# 合法实例的构造（全部 O(n)，无 O(n^2) Python 循环）：
#   构造一个「站级有向多重图」：每站出度恰 2（线路 2v+1、2v+2 从站 v 出发），
#   并让每站入度也恰 2、无自环、全图弱连通 —— 此时由欧拉回路判定定理，
#   「坐遍所有线路恰一次并回到 1 号站」的方案必然存在（即题目保证的条件）。
#   两条构造途径：
#     A. 站点序列法（seq_random）：seq 中每个站恰出现 2 次、循环相邻两两不同；
#        第 j 个位置的线路终点取 seq[(j+1) mod 2n]；seq 本身就是一条合法巡回。
#     B. 双步长法（build_shift）：站 v 的两条线路分别驶向 v+1 与 v+k (mod n)，
#        用于构造「许多站的入边来自不同前驱」的交叉结构（并环逻辑的最坏实例）。
#     C. 后继交换法（succ_swaps）：从 n-环出发随机交换两条线路的终点
#        （交换保持各站入度=2，且避免自环），再检查弱连通；用于制造随机交叉边。
#
# 关于 l_i 的取值口径（题面歧义，详见 gen-report.md「风险点」）：
#   题面同时写 l_i ∈ [0,1000]（小时）与「每天 24 小时」；唯一自洽读法是时刻取模 24。
#   本生成器全部取 0 <= l_i <= 23，使「第 1 天 l_i 首发」与「每日 (l_i mod 24) 时刻发车」
#   两种读法答案一致，数据不依赖该歧义。
#
# 分层设计（10 组，规模从最小铺到顶格；每组为单实例，注释写明规模与设计意图）：
#   点 1-2  边界层：n 最小可行（n=1 无合法实例，见报告）、全最小（答案为 0 的极端）、
#                  全日内最大（l=23,d=24，手算可核）；
#   点 3-4  小规模 + 题面特殊值：题面样例 1 / 样例 2 原样（逐字节回归 32 / 192）；
#   点 5    小规模随机：n=16，可枚举/手算量级；
#   点 6    中等规模随机（交叉结构）：n=200，后继交换法制造随机交叉边；
#   点 7    中等规模随机（极端重复值分布）：n=600，l∈{0,23}、d∈{1,24} 二值混合；
#   点 8    大规模最坏结构：n=1000 双步长构造 k=499，初始局部配对被切成 ~500 个
#           分量（考「并环」/最小合并代价的最坏结构）；
#   点 9    顶格层随机：n=1000 全范围随机；
#   点 10   顶格层构造：站级单环 + 全相等极端权值（l≡23, d≡1，所有接续等待恒 23），
#           答案有闭式 48000，专卡「漏取模 / 贪心局部配对 / 忘记并环」类错误。

from cyaron import IO
import os
import random

# ---------------------------------------------------------------------------
# 合法实例构造 A：站点序列
# ---------------------------------------------------------------------------


def seq_random(n, rng):
    """随机站点序列：每站恰 2 次，循环相邻两两不同。

    n >= 4：随机排列 p 与轮换量 k∈[2,n-2]，拼接 p + p[k:] + p[:k]；
    n = 3：用基点模式 [0,1,0,2,1,2] 随机重标号；
    n = 2：只有 [0,1,0,1] / [1,0,1,0] 两种。
    """
    if n == 2:
        return [0, 1, 0, 1] if rng.random() < 0.5 else [1, 0, 1, 0]
    if n == 3:
        q = [0, 1, 2]
        rng.shuffle(q)
        return [q[x] for x in (0, 1, 0, 2, 1, 2)]
    p = list(range(n))
    rng.shuffle(p)
    k = rng.randint(2, n - 2)
    return p + p[k:] + p[:k]


def seq_cycle(n):
    """站级单环：0,1,...,n-1,0,1,...,n-1（每站两条线都驶向下一站）。"""
    seq = list(range(n))
    return seq + seq


def build_e(seq, n):
    """由站点序列还原每条线路的终点（返回 1-based 的 e[1..2n]）。"""
    m = len(seq)
    assert m == 2 * n
    seen = [0] * n
    route_at = [0] * m
    for j, v in enumerate(seq):
        assert 0 <= v < n
        seen[v] += 1
        assert seen[v] <= 2
        route_at[j] = 2 * v + seen[v]      # 1-based 线路号：站 v 的两条线路为 2v+1、2v+2
    assert all(s == 2 for s in seen)
    e = [0] * (m + 1)
    for j in range(m):
        nxt = seq[(j + 1) % m]
        e[route_at[j]] = nxt + 1
    _check_legal(e, n)
    return e


# ---------------------------------------------------------------------------
# 合法实例构造 B：后继交换
# ---------------------------------------------------------------------------


def succ_swaps(n, rng, rounds):
    """返回 1-based 的 e[1..2n]：从 n-环出发随机交换两种线路终点。

    交换保持各站入度=2、出度=2，并避免自环；但可能破坏弱连通，
    由调用方用 _connected() 检查后决定是否重试（本函数内只检查结构与自环）。
    """
    su = [0] * (2 * n)                     # 0-based：线路 i 的终点站
    for v in range(n):
        su[2 * v] = (v + 1) % n
        su[2 * v + 1] = (v + 1) % n
    done = 0
    guard = 0
    while done < rounds and guard < 20 * rounds:
        guard += 1
        a = rng.randrange(2 * n)
        b = rng.randrange(2 * n)
        if a == b:
            continue
        sa, sb = su[a], su[b]
        ua, ub = a // 2, b // 2
        if sa == ub or sb == ua:            # 交换后会产生自环
            continue
        su[a], su[b] = sb, sa
        done += 1
    e = [0] * (2 * n + 1)
    for i in range(2 * n):
        e[i + 1] = su[i] + 1
    _check_structure(e, n)
    return e


def build_shift(n, k):
    """「双步长」构造：站 v 的两条线路分别驶向 v+1 与 v+k (mod n)。

    返回 1-based e[1..2n]。k∈[2, n-1] 时无自环、每站入度=2，且 k 与 n 互质时
    弱连通（k=1 或 k=n-1 也对，但为避免退化不取）。该构造下很多站的「两条入边」
    来自不同前驱、两条出边去向不同后继，配合特定 l/d 可让局部最优配对把巡回
    切成一大一小两个（或 k+1 个）分量，是「并环」逻辑的最坏结构。
    """
    assert 2 <= k <= n - 1
    m = 2 * n
    e = [0] * (m + 1)
    for v in range(n):
        e[2 * v + 1] = (v + 1) % n + 1
        e[2 * v + 2] = (v + k) % n + 1
    _check_legal(e, n)
    return e


def _connected(e, n):
    """站级线图弱连通检查（并查集）。"""
    par = list(range(n))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    for i in range(1, 2 * n + 1):
        u = (i + 1) // 2 - 1                # 起点站（0-based）
        v = e[i] - 1
        ru, rv = find(u), find(v)
        if ru != rv:
            par[ru] = rv
    return all(find(v) == find(0) for v in range(n))


def _check_structure(e, n):
    """仅结构校验：e_i 范围、无自环、入度=2（出度恒 2）。"""
    m = 2 * n
    assert len(e) == m + 1
    indeg = [0] * n
    for i in range(1, m + 1):
        start = (i + 1) // 2 - 1            # 0-based 起点站
        assert 1 <= e[i] <= n, "e_i 超出 [1,n]"
        assert e[i] - 1 != start, "e_i 不得等于起点（无自环）"
        indeg[e[i] - 1] += 1
    assert all(d == 2 for d in indeg), "每站入度必须为 2（出度恒 2）"


def _check_legal(e, n):
    """入度=2、无自环、弱连通（欧拉回路存在的充要条件）。"""
    _check_structure(e, n)
    assert _connected(e, n), "站级线图必须弱连通，否则不存在题目保证的巡回"


# ---------------------------------------------------------------------------
# 写文件 + 产出输出 + 交付前硬校验
# ---------------------------------------------------------------------------


def gen_case(t, n, e, lfun, dfun, expect=None):
    """生成第 t 组数据并完成硬校验。

    - 生成前检查 ../std 存在（否则 cyaron 会静默产出 0 字节 .out）；
    - 生成后检查 .in/.out 存在、非空、行数/.out 行数正确、答案为合法非负整数、
      满足平凡下界与上界；expect 给出时断言答案与闭式/手工值一致。
    """
    assert os.path.exists("../std"), "缺少 ../std：请先 g++ -O2 -std=c++17 std.cpp -o std"
    m = 2 * n
    _check_legal(e, n)
    lv = [0] * (m + 1)
    dv = [0] * (m + 1)
    for i in range(1, m + 1):
        lv[i], dv[i] = lfun(i), dfun(i)
        assert 0 <= lv[i] <= 23, "本题数据统一取 0<=l<=23（题面 l 口径歧义，见报告）"
        assert 0 <= dv[i], "d_i 不应为负"

    io = IO(file_prefix="problem", data_id=t)
    lines = [str(n)]
    for i in range(1, m + 1):
        lines.append("%d %d %d" % (e[i], lv[i], dv[i]))
    io.input_writeln("\n".join(lines))
    io.output_gen("../std")
    io.close()                              # 确保 .in/.out 落盘后再做校验

    inp, outp = "problem%d.in" % t, "problem%d.out" % t
    assert os.path.exists(inp) and os.path.exists(outp), "cyaron 未产出文件"
    sz_in, sz_out = os.path.getsize(inp), os.path.getsize(outp)
    assert sz_in > 0 and sz_out > 0, "存在 0 字节文件（std 缺失或运行失败）"
    with open(inp, "r", encoding="utf-8") as f:
        in_lines = f.read().splitlines()
    with open(outp, "r", encoding="utf-8") as f:
        out_lines = f.read().splitlines()
    assert len(in_lines) == 1 + m, "输入行数应为 1+2n"
    assert len(out_lines) == 1, "输出应恰有 1 行"
    assert out_lines[0].strip().isdigit(), "答案应为非负整数"
    ans = int(out_lines[0].strip())
    sum_d = sum(dv[1:])
    assert ans >= sum_d, "答案不应小于 Σd（各项等待与首班时刻均非负）"
    assert ans <= sum_d + 23 + 23 * (m - 1), "答案超出平凡上界"
    if expect is not None:
        assert ans == expect, "第 %d 组答案 %d 与期望 %d 不符" % (t, ans, expect)
    print("problem%-2d n=%-4d ans=%-8d in=%-7dB out=%-4dB%s"
          % (t, n, ans, sz_in, sz_out, (" expect=%d OK" % expect) if expect is not None else ""))
    return ans


def gen_fixed_sample(t, n, text, expect):
    """题面样例原样回归（小规模 + 题面声明特殊值）。"""
    assert os.path.exists("../std"), "缺少 ../std：请先 g++ -O2 -std=c++17 std.cpp -o std"
    io = IO(file_prefix="problem", data_id=t)
    io.input_writeln(text)
    io.output_gen("../std")
    io.close()                              # 确保 .in/.out 落盘后再做校验
    with open("problem%d.in" % t, encoding="utf-8") as f:
        in_lines = f.read().splitlines()
    with open("problem%d.out" % t, encoding="utf-8") as f:
        out = f.read()
    assert len(in_lines) == 1 + 2 * n
    ans = int(out.split()[0])
    assert ans == expect, "第 %d 组（题面样例）应为 %d，实得 %d" % (t, expect, ans)
    print("problem%-2d n=%-4d ans=%-8d in=%-7dB out=%-4dB 题面样例 OK"
          % (t, n, ans, os.path.getsize("problem%d.in" % t), os.path.getsize("problem%d.out" % t)))


# ---------------------------------------------------------------------------
# 各测试点
# ---------------------------------------------------------------------------


def gen1():
    # 边界层：n=2（n=1 不存在合法实例，见报告），全最小 l≡0、d≡0。
    # 任何巡回：总时间 = Σd + 首班等待 + Σ接续等待 = 0 + 0 + 0 => 答案为 0 的极端。
    rng = random.Random(173901)
    gen_case(1, 2, build_e(seq_random(2, rng), 2), lambda i: 0, lambda i: 0, expect=0)


def gen2():
    # 边界层：n=4，全「日内最大」l≡23、d≡24（与样例 2 车程同量级）。
    # (l_e+d_e) mod 24 = 23 = l_f => 所有 W ≡ 0；答案 = Σd + l_首班 = 192 + 23 = 215（手算）。
    rng = random.Random(173902)
    gen_case(2, 4, build_e(seq_random(4, rng), 4), lambda i: 23, lambda i: 24, expect=215)


def gen3():
    # 小规模 + 题面特殊值：样例 1 原样（n=2），题面答案 32。
    gen_fixed_sample(3, 2, "2\n2 1 5\n2 0 3\n1 4 4\n1 6 3", 32)


def gen4():
    # 小规模 + 题面特殊值：样例 2 原样（n=4，全 d=24），题面答案 192。
    gen_fixed_sample(
        4, 4,
        "4\n3 0 24\n2 0 24\n4 0 24\n4 0 24\n2 0 24\n1 0 24\n3 0 24\n1 0 24",
        192,
    )


def gen5():
    # 小规模随机：n=16，l∈[0,23]、d∈[0,24]（含 d=0 与 d=24 两端），手算/枚举量级。
    rng = random.Random(173905)
    n = 16
    gen_case(5, n, build_e(seq_random(n, rng), n),
             lambda i: rng.randint(0, 23), lambda i: rng.randint(0, 24))


def gen6():
    # 中等规模随机（交叉结构）：n=200，后继交换法随机交换终点，制造大量交叉边。
    # 与 seq_random 的结构互补：这里许多站的「两条入边」来自不同前驱，
    # 局部最优配对会产生若干分量，需正确并环。
    rng = random.Random(173906)
    n = 200
    e = None
    for seed in range(300):
        cand = succ_swaps(n, rng, rng.randint(20, 120))
        if _connected(cand, n):
            e = cand
            break
    assert e is not None, "未构造出连通的交换结构"
    gen_case(6, n, e, lambda i: rng.randint(0, 23), lambda i: rng.randint(0, 24))


def gen7():
    # 中等规模随机（极端重复值分布）：n=600，l∈{0,23}、d∈{1,24} 二值混合。
    # (l+d) mod 24 ∈ {0,1,23} ⇒ 接续等待 W ∈ {0,1,22,23}：最快与最慢接续并存，
    # 局部最优配对倾向把巡回切成许多小环，专门压测「并环」逻辑。
    rng = random.Random(173907)
    n = 600
    gen_case(7, n, build_e(seq_random(n, rng), n),
             lambda i: rng.choice([0, 23]), lambda i: rng.choice([1, 24]))


def gen8():
    # 大规模最坏结构（并行交叉构造）：n=1000，「双步长」构造 k=499（站 v 的两条线路分别
    # 驶向 v+1 与 v+499），l ∈ {0,23} 交替、d≡1。
    # 此时局部最优初始配对的巡回被切成 ~500 个分量（n=200 同型实验实测 15 个分量，
    # n=1000 同参数实测 500 个），必须依赖正确的「最小合并代价」逻辑才能连成单环，
    # 是「并环」逻辑的最坏结构（穷举验证见 gen-report.md）。
    n = 1000
    e = build_shift(n, 499)
    gen_case(8, n, e, lambda i: (i % 2) * 23, lambda i: 1)


def gen9():
    # 顶格层随机：n=1000（题面上限），l∈[0,23]、d∈[0,24] 全范围随机。
    rng = random.Random(173909)
    n = 1000
    gen_case(9, n, build_e(seq_random(n, rng), n),
             lambda i: rng.randint(0, 23), lambda i: rng.randint(0, 24))


def gen10():
    # 顶格层构造（最坏结构）：n=1000，站级单环 + 全相等极端权值 l≡23、d≡1。
    # 所有接续等待 W(e,f) = (23 - (23+1)) mod 24 = 23 恒为最大等待；
    # 任意合法巡回都有 2n-1 = 1999 次接续，答案闭式
    #   = Σd + l_首班 + 1999*23 = 2000 + 23 + 45977 = 48000。
    # 该点同时卡「首班不取模 24」「局部贪心配对」「漏并环」三类错误。
    n = 1000
    gen_case(10, n, build_e(seq_cycle(n), n), lambda i: 23, lambda i: 1, expect=48000)


if __name__ == "__main__":
    random.seed(20261006)
    for g in (gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10):
        g()
    print("all 10 data points generated and validated")
