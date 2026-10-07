#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1745《分组》数据生成器（cyaron）
# 用法：g++ -O2 -std=c++17 -o std std.cpp && mkdir -p data && cd data && python3 ../data.py
#
# 题面数据范围（100%）：2 <= n <= 1e5，0 <= K <= 1e9，1 <= r_i, a_i <= 1e9，
#                        1 <= Q <= 1e5，1 <= x, y <= n，x != y。
# 所有数据严格落在上述范围内（r/a 用 1e9 顶格值只在边界层刻意取）。
#
# 分层设计（10 组）：
#   点 1  边界层：n 很小 + r/a 取 1 与 1e9 极端 + K=0，答案恰为 2 与 -1 两种极端；
#   点 2  边界层：n=2 下限（题面最小），K=0，顶格权值，无解 -1；
#   点 3  小规模：全 r 相等 + K=1e9 顶格，由构造可知每问答案恒为 n（解析断言）；
#   点 4  小规模随机：n=20、值域 [1,10]，可手算核对，答案量级小；
#   点 5  小规模：重复 r（仅有 4 种地位）+ 年龄聚类，专测地位并列（同 r 可当队长）；
#   点 6  中等规模随机：n=Q=2000，值域满 [1,1e9]；
#   点 7  中等规模：r 只有 100 种取值（大量并列块）+ 年龄分散，K 中等；
#   点 8  大规模：年龄密集（1e5 宽度）+ K 较大，绝大多数询问有解；
#   点 9  大规模极端：K=0（年龄必须完全相同才可同组）+ 年龄仅 100 个取值，
#        大量 -1 输出，压 -1 分支与年龄并列路径；
#   点 10 顶格层：n=Q=1e5、K=5e8、值域满，标准最大规模 + 大量可行解。
import os
import random
import sys

from cyaron import IO

N_MAX = 100000
V_MAX = 1000000000
K_MAX = 1000000000

# ---- 前置校验：std 必须存在，否则 cyaron 会静默产出 0 字节 .out ----
if not os.path.exists("../std"):
    sys.exit("FATAL: must compile std first: g++ -O2 -std=c++17 -o std std.cpp")
if os.path.isdir("../std"):
    sys.exit("FATAL: ../std is a directory, expected the compiled std binary")


def pairs(rnd, n, q):
    """返回 q 个互不相同的 (x, y)，x != y，均落在 [1, n]。

    复杂度 O(q)（每个候选对 O(1) 构造，无 O(n^2) 循环）：
    - 2q <= n 时直接采样 2q 个互异下标再两两配对（下标互异 => 对互异）；
    - 否则按随机取对 + 集合去重（可选对数为 C(n,2)，远大于 q <= 1e5，重试极少）。
    """
    if q <= 0:
        return []
    if 2 * q <= n:
        flat = rnd.sample(range(1, n + 1), 2 * q)
        it = iter(flat)
        return list(zip(it, it))
    seen = set()
    res = []
    while len(res) < q:
        a, b = rnd.randint(1, n), rnd.randint(1, n)
        if a == b:
            continue
        key = (a, b) if a < b else (b, a)
        if key in seen:
            continue
        seen.add(key)
        res.append((a, b))
    return res


def pairs_near(rnd, n, K, count):
    """返回 count 个 x != y 且 |x - y| <= 2K 的询问（用于保证有解分支被覆盖）。O(count)。"""
    d = max(1, min(2 * K if K < n else n - 1, n - 1))
    res = []
    while len(res) < count:
        x = rnd.randint(1, n)
        y = x + rnd.randint(1, d) * rnd.choice((-1, 1))
        if 1 <= y <= n:
            res.append((x, y))
    return res


def emit(pid, n, K, r, ag, queries):
    """写出一组数据：n、K、r 序列、年龄序列、Q 与询问；由 std 生成 .out。"""
    assert 2 <= n <= N_MAX and 0 <= K <= K_MAX and 1 <= len(queries) <= 100000
    assert all(1 <= v <= V_MAX for v in r) and all(1 <= v <= V_MAX for v in ag)
    assert len(r) == n and len(ag) == n
    for x, y in queries:
        assert 1 <= x <= n and 1 <= y <= n and x != y
    with IO(file_prefix="problem", data_id=pid) as io:
        io.input_writeln(n, K)
        io.input_writeln(" ".join(map(str, r)))
        io.input_writeln(" ".join(map(str, ag)))
        io.input_writeln(len(queries))
        for x, y in queries:
            io.input_writeln(x, y)
        io.output_gen("../std")
    return len(queries)


# ---------------- 点 1：边界层 ----------------
# n=4，K=0，r/a 取 1 与 1e9 两个极端：前两人地位/年龄完全相同，后两人相同且顶格。
# 解析答案：同组对 (1,2)->2、(3,4)->2；跨极端对年龄差 > K=0 -> -1。
def gen1():
    n = 4
    r = [1, 1, V_MAX, V_MAX]
    ag = [1, 1, V_MAX, V_MAX]
    qs = [(1, 2), (3, 4), (1, 3), (2, 4)]
    assert emit(1, n, 0, r, ag, qs) == 4
    return {1: 2, 2: 2, 3: -1, 4: -1}  # 解析期望（逐行）


# ---------------- 点 2：边界层（n 下限） ----------------
# n=2（题面最小）、K=0、两人地位并列且顶格、年龄相差 1 -> 无论谁当队长都超差，输出 -1。
def gen2():
    n = 2
    r = [V_MAX, V_MAX]
    ag = [V_MAX - 1, V_MAX]
    qs = [(1, 2)]
    assert emit(2, n, 0, r, ag, qs) == 1
    return {1: -1}


# ---------------- 点 3：小规模 + K 顶格 + 全 r 相等 ----------------
# K=1e9 覆盖全部年龄差，且所有人 r 相同（地位并列，人人都可当队长），
# 解析结论：任意询问答案恒为 n。用于验证并列地位 + 最大 K 的组合。
def gen3():
    rnd = random.Random(1745003)
    n = 100
    r = [rnd.randint(1, V_MAX)] * n
    ag = [rnd.randint(1, V_MAX) for _ in range(n)]
    qs = pairs(rnd, n, 100)
    assert emit(3, n, K_MAX, r, ag, qs) == 100
    return "all_n"  # 特殊断言：所有答案 == n


# ---------------- 点 4：小规模（全 r 相等 + 年龄重复，有解析式校验） ----------------
# n=20，r 全相等（地位全并列，人人都可当队长）、年龄 [1,10] 大量重复、K=2。
# 全 r 相等时按题面定义可得独立解析式（见 main() 中 all_r_equal 分支）：
#   答案 = max{ #{j : |a_j - a_p| <= K} : a_p ∈ [max(a_x,a_y)-K, min(a_x,a_y)+K] }，
#   无合法队长则为 -1。该点专测“地位并列”分支（同 r 的块必须先整块入树再查询）。
def gen4():
    rnd = random.Random(1745004)
    n = 20
    r = [7] * n
    ag = [rnd.randint(1, 10) for _ in range(n)]
    qs = pairs(rnd, n, 20)
    assert emit(4, n, 2, r, ag, qs) == 20
    return ("all_r_equal", ag)  # 附年龄表供解析式校验


# ---------------- 点 5：结构化数据（有精确解析式，不靠对拍） ----------------
# 构造：r_i = a_i = i（i = 1..n，地位两两不同且与年龄同序）。
# 由题面定义可推出精确解（见 main() 中 r_eq_a 分支）：
#   令 u = max(x,y), v = min(x,y)，队长 p 合法 <=> p ∈ [u, min(n, v+K)]；
#   p 当队长的最大人数 = #{j : j <= p, |j-p| <= K} = min(p, K + 1)。
#   答案 = max_{p ∈ [u, min(n, v+K)]} min(p, K+1) = min(min(n, v+K), K+1)；
#   区间为空（u > min(n, v+K)）则为 -1。
# 该点同时逐询问断言上式的 -1 分支与精确数值，n=1000 下每次查询 O(1)。
# 查询构型：一半取 |x-y| <= 2K（因窗口仅 v+K..v+2K，刚好一半有解、一半 -1），
# 一半完全随机（n=1000 时绝大多数 |x-y| > 2K，输出 -1），两个分支均被覆盖。
# K=17：|x-y| > 2K=34 的询问无极（-1），|x-y| 较小的询问答案 = min(u, K+1) 模式，
# 两种分支均大量出现。
def gen5():
    rnd = random.Random(1745005)
    n = 1000
    r = list(range(1, n + 1))
    ag = list(range(1, n + 1))
    qs = pairs_near(rnd, n, 17, 100) + pairs(rnd, n, 100)
    rnd.shuffle(qs)
    assert emit(5, n, 17, r, ag, qs) == len(qs)
    return ("r_eq_a", 17, ag)


# ---------------- 点 6：中等规模随机（有解与无解混合） ----------------
# n=Q=2000，r 满值域，但年龄压缩到 [1,1e4]、K=1500：
# 年龄窗宽 2K=3000 占年龄跨度 30%，约一半询问有解，答案从 2 到上千均有。
def gen6():
    rnd = random.Random(1745006)
    n = 2000
    r = [rnd.randint(1, V_MAX) for _ in range(n)]
    ag = [rnd.randint(1, 10000) for _ in range(n)]
    qs = pairs(rnd, n, 2000)
    assert emit(6, n, 1500, r, ag, qs) == 2000
    return None


# ---------------- 点 7：中等规模（大量地位并列块 + 有解/无解混合） ----------------
# r ∈ [1,100]（n=5000 时平均每档 50 人）、年龄 [1,1e5]、K=5000：
# 询问阈值 start 会大量落在同 r 块中间，专测 lower_bound 取块首的并列处理；
# K 取到年龄跨度的 5%，有解比例适中，答案分布同时覆盖小值与大值。
def gen7():
    rnd = random.Random(1745007)
    n = 5000
    r = [rnd.randint(1, 100) for _ in range(n)]
    ag = [rnd.randint(1, 100000) for _ in range(n)]
    qs = pairs(rnd, n, 5000)
    assert emit(7, n, 5000, r, ag, qs) == 5000
    return None


# ---------------- 点 8：大规模（年龄密集，绝大多数询问有解） ----------------
# n=Q=30000，年龄仅 [1,200000] 宽度而 K=100000（半宽），地位满值域：
# 四分之一以上的年龄对必然相容，答案普遍 >= 2，检验最大值线段树的大面积查询。
def gen8():
    rnd = random.Random(1745008)
    n = 30000
    r = [rnd.randint(1, V_MAX) for _ in range(n)]
    ag = [rnd.randint(1, 200000) for _ in range(n)]
    qs = pairs(rnd, n, 30000)
    assert emit(8, n, 100000, r, ag, qs) == 30000
    return None


# ---------------- 点 9：大规模极端（K=0 + 年龄并列多） ----------------
# n=Q=60000，K=0：只有年龄完全相同的人才可能同组，输出以 -1 为主，
# 年龄仅取 [1,100] 的 100 个值 -> 大量并列。压 -1 分支、同年龄查询与块内并列。
# K=0 时有精确解析式（见 main() 中的 k0_analytic 校验）：
#   令 c = #{j : a_j == a_x}。若 a_x != a_y 则 -1；否则答案恒为 c。
#   推导：组内所有人年龄必须 = 队长年龄 = a_x（K=0），且队长 r 最大；
#   取年龄为 a_x 的人中 r 最大者为队长，可收进全部同年龄者，故答案为 c。
def gen9():
    rnd = random.Random(1745009)
    n = 60000
    r = [rnd.randint(1, V_MAX) for _ in range(n)]
    ag = [rnd.randint(1, 100) for _ in range(n)]
    qs = pairs(rnd, n, 60000)
    assert emit(9, n, 0, r, ag, qs) == 60000
    return ("k0_analytic", dict.fromkeys(ag), ag)  # 附带年龄表供解析式校验


# ---------------- 点 10：顶格层 ----------------
# n=Q=1e5（题面上限）、K=5e8（半值域）、r/a 满 [1,1e9]：
# 标准最大规模，年龄区间宽、答案分布覆盖 2..n 与 -1，且所有数组/线段树下标接近上限。
def gen10():
    rnd = random.Random(1745010)
    n = N_MAX
    r = [rnd.randint(1, V_MAX) for _ in range(n)]
    ag = [rnd.randint(1, V_MAX) for _ in range(n)]
    qs = pairs(rnd, n, 100000)
    assert emit(10, n, 500000000, r, ag, qs) == 100000
    return None


def sanity_check_leaders(pid, n, K, r, ag, queries, out, rnd, sample=8):
    """独立性抽查（非对拍/非暴力）：

    由题面定义可直接推出必要条件——若某询问答案 != -1，则必存在一个合法队长 p
    满足 r_p >= max(r_x, r_y) 且 a_p ∈ [max(a_x,a_y)-K, min(a_x,a_y)+K]。
    本检查对被抽样的询问做 O(n) 扫描验证该必要条件（不依赖 std 的内部实现思路）。
    """
    idx = rnd.sample(range(len(queries)), min(sample, len(queries)))
    checked = 0
    for i in idx:
        x, y = queries[i]
        if out[i] == -1:
            continue
        lo_r = max(r[x - 1], r[y - 1])
        lo_a = max(ag[x - 1], ag[y - 1]) - K
        hi_a = min(ag[x - 1], ag[y - 1]) + K
        ok = any(r[j] >= lo_r and lo_a <= ag[j] <= hi_a for j in range(n))
        assert ok, "point %d query %d: leader witness missing" % (pid, i + 1)
        checked += 1
    return checked


def no_legal_leader(r, ag, K, x, y):
    """题面定义的直接判定（O(n)）：是否存在合法队长 p。

    必要条件/充分条件均来自定义：p 当队长可行 <=> r_p >= max(r_x, r_y)
    且 |a_x - a_p| <= K 且 |a_y - a_p| <= K（因为 x、y、p 同在一组）。
    与 std 内部不共享任何代码路径。
    """
    lo_r = max(r[x - 1], r[y - 1])
    lo_a = max(ag[x - 1], ag[y - 1]) - K
    hi_a = min(ag[x - 1], ag[y - 1]) + K
    for j in range(len(r)):
        if r[j] >= lo_r and lo_a <= ag[j] <= hi_a:
            return False
    return True


def main():
    gens = [gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10]
    expect = {}
    for g in gens:
        expect[g.__name__[-1]] = g()
        print(g.__name__, "done", flush=True)

    # ---- 生成后断言：.out 非空、行数与 Q 一致、答案合法（-1 或 [2, n]） ----
    problems = []
    for pid in range(1, 11):
        pin = os.path.join("problem%d.in" % pid)
        pout = os.path.join("problem%d.out" % pid)
        assert os.path.exists(pin) and os.path.exists(pout), "missing pair for %d" % pid
        assert os.path.getsize(pin) > 0 and os.path.getsize(pout) > 0, "empty file %d" % pid
        with open(pin) as f:
            first = f.readline().split()
            n, K = int(first[0]), int(first[1])
            r = list(map(int, f.readline().split()))
            ag = list(map(int, f.readline().split()))
            q = int(f.readline())
            qs = []
            for _ in range(q):
                a, b = map(int, f.readline().split())
                qs.append((a, b))
        assert len(r) == n and len(ag) == n, "shape mismatch %d" % pid
        out = [int(t) for t in open(pout).read().split()]
        assert len(out) == q, "out lines %d != Q %d at point %d" % (len(out), q, pid)
        assert all(v == -1 or 2 <= v <= n for v in out), "illegal answer at point %d" % pid
        # 点 3：构造保证任意询问答案恒为 n
        if "all_n" == expect.get(str(pid)):
            assert all(v == n for v in out), "point %d expect all %d" % (pid, n)
        # 点 1/2：n 极小，逐行核对解析期望值
        if isinstance(expect.get(str(pid)), dict):
            for line, want in expect[str(pid)].items():
                assert out[line - 1] == want, "point %d line %d: got %d want %d" % (
                    pid, line, out[line - 1], want)
        # 点 1-5（n,Q <= 100）：逐询问精确验证「输出 -1 <=> 不存在合法队长」
        if n <= 100 and q <= 100:
            for i, (x, y) in enumerate(qs):
                assert (out[i] == -1) == no_legal_leader(r, ag, K, x, y), \
                    "point %d query %d: -1 branch inconsistent" % (pid, i + 1)
            print("  point %d: all %d queries match the -1-iff-no-leader rule" % (pid, q), flush=True)
        # 点 4：全 r 相等时的解析式（直接由题面定义推导，不复用 std 内部逻辑）：
        #   合法队长 p <=> a_p ∈ [max(a_x,a_y)-K, min(a_x,a_y)+K]（r 全并列自动满足）；
        #   该队长的最大小组 = #{j : |a_j - a_p| <= K}（r 无限制）；
        #   答案 = 合法队长中的最大值，无合法队长则为 -1（此时必然 -1，
        #   因为 -1 <=> max(a_x,a_y) - min(a_x,a_y) > 2K <=> 窗口内空）。
        if isinstance(expect.get(str(pid)), tuple) and expect[str(pid)][0] == "all_r_equal":
            ages = expect[str(pid)][1]
            for i, (x, y) in enumerate(qs):
                lo = max(ages[x - 1], ages[y - 1]) - K
                hi = min(ages[x - 1], ages[y - 1]) + K
                best = 0
                for ap in ages:            # n <= 100 的小点，非 O(n^2) 大循环
                    if lo <= ap <= hi:
                        c = sum(1 for v in ages if abs(v - ap) <= K)
                        best = max(best, c)
                want = -1 if best < 2 else best
                assert out[i] == want, \
                    "point %d all-r-equal q%d: got %d want %d" % (pid, i + 1, out[i], want)
            print("  point %d all-r-equal closed form: %d queries match" % (pid, q), flush=True)
        # 点 5：r_i = a_i = i 的精确解析式校验
        if isinstance(expect.get(str(pid)), tuple) and expect[str(pid)][0] == "r_eq_a":
            kv = expect[str(pid)][1]
            for i, (x, y) in enumerate(qs):
                u, v = max(x, y), min(x, y)
                hi = min(n, v + kv)
                want = -1 if u > hi else min(hi, kv + 1)
                assert out[i] == want, \
                    "point %d r=i,a=i q%d (%d,%d): got %d want %d" % (pid, i + 1, x, y, out[i], want)
            print("  point %d r=a=i exact formula: %d queries match" % (pid, q), flush=True)
        # 点 9：K=0 的精确解析式校验（c = 与 x 同年龄的人数；a_x != a_y -> -1）
        if isinstance(expect.get(str(pid)), tuple) and expect[str(pid)][0] == "k0_analytic":
            agecnt = {}
            for v in ag:
                agecnt[v] = agecnt.get(v, 0) + 1
            bad = 0
            for i, (x, y) in enumerate(qs):
                want = -1 if ag[x - 1] != ag[y - 1] else agecnt[ag[x - 1]]
                if out[i] != want:
                    bad += 1
                    if bad <= 3:
                        print("  MISMATCH q%d (%d,%d): got %d want %d"
                              % (i + 1, x, y, out[i], want))
            assert bad == 0, "point 9 analytic check failed on %d/%d queries" % (bad, q)
            print("  point 9 k0-analytic: all %d queries match closed form" % q, flush=True)
        # 抽检（点 9/10 各 8 条非 -1 询问）：必要条件的独立验证
        w = 0
        if pid == 10:
            w = sanity_check_leaders(pid, n, K, r, ag, qs, out, random.Random(1745000 + pid))
        nz = sum(1 for v in out if v == -1)
        mx = max(out)
        problems.append((pid, os.path.getsize(pin), n, K, q, len(out), nz, mx, w))
        print("check point %d ok: n=%d K=%d Q=%d lines=%d -1count=%d maxans=%d witnesses=%d"
              % (pid, n, K, q, len(out), nz, mx, w), flush=True)
    print("ALL CHECKS PASSED", flush=True)


if __name__ == "__main__":
    main()
