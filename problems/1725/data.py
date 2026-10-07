#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1725《账本核算》分层测试数据生成器（cyaron，仓库惯例）
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py
#
# 题意：T 组账本。每组给 n（月数）、m（条查询记录），随后 m 行 x y w 表示
#       「第 x..y 个月的总收入 = w」。判断每组是否存在合法的收入序列 A[1..n]。
#
# 数据范围（content.md 明文，官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=1725 一致）：
#   T < 100；n, m < 100；1 <= x <= y <= n；w 题面未给范围 => 常规取 ±10^4，
#   点 10 另配 ±10^6 大权重（题面未规定 w；取「int 仍安全」的上限口径：
#   99 个月累计 99*10^6 = 9.9*10^7 << 2^31-1，避免误杀网络主流的 int 写法）。
#   限制 time 1000 ms / memory 162 MB（config.json）。
#
# 建模：记前缀和 s[i]=A[1]+...+A[i]，则每条信息即 s[y]-s[x-1]=w；整组有整数解
#    <=> 带权并查集/差分约束下无矛盾。本文件内置带权并查集判决器，**仅用于生成期自检**，
#    保证每个 case 的 true/false 标签真实、每点配比符合设计意图（非对拍、非暴力）。
#
# ---- 分层策略（多组数据题：逐点放大 T 与 n/m）----
#   点 1  边界层：T=1、n=m=1、w=0（最小规模 + 权重边界值）-> true
#   点 2  边界层：最小规模 false（n=2，同一区间两次给出不同 w）-> false
#   点 3  边界层：**题面样例逐字复现**（T=2）-> true / false（.out 回归锚点）
#   点 4  小规模随机：T=20，n,m∈[1,5]，全部由随机合法账本派生 -> 全 true（真值侧压力）
#   点 5  小规模随机：T=30，n,m∈[1,10]，true/false 交替；掺 x=y 单月约束
#   点 6  中等规模随机：T=50，n,m∈[20,50]，true/false 交替
#   点 7  中等偏大随机：T=60，n,m∈[50,90]，true/false 交替
#   点 8  大规模随机：T=99（T 上界），n,m∈[90,99]，true/false 交替
#   点 9  顶格层：T=99，n=m=99（n,m 上界），**全部 true**：合法账本派生 + 结构化区间
#         （x=y 单月 / x=1 前缀 / y=n 后缀 / x=1&y=n 全长），同时压 99 行 true 输出
#   点 10 顶格层（最坏混合）：T=99，n=m=99，true/false 交替，w 取 ±10^6/0 极端，
#         含重复区间与全长约束（图最稠密 + 大权重）
#
# 固定随机种子，结果完全可复现。

import os
import random

from cyaron import IO  # 引入CYaRon的库

MAXT = 99   # T < 100
MAXNM = 99  # n, m < 100

W_LO, W_HI = -10000, 10000  # 常规权重范围（题面未规定 w，取一本通常用档）
W_EXT = 10 ** 6             # 点 10 的大权重幅值 w ∈ ±10^6（int 安全上限口径，见文首说明）
AMP_EXT = W_EXT // (MAXNM + 1)  # 大权重点的单月幅度，保证 n 个月前缀和仍 <= 10^6

STD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "std")


# ---------------- 带权并查集判决器：s[y]-s[x-1]=w 组是否无矛盾 ----------------
class WeightedDSU:
    def __init__(self, n_nodes):
        self.parent = list(range(n_nodes))
        self.pot = [0] * n_nodes  # pot[i] = s[i] - s[parent[i]]

    def find(self, x):
        if self.parent[x] == x:
            return x
        root = self.find(self.parent[x])
        self.pot[x] += self.pot[self.parent[x]]
        self.parent[x] = root
        return root

    def unite(self, a, b, w):
        """声明 s[b] - s[a] = w；返回 False 表示与已有约束矛盾。"""
        ra, rb = self.find(a), self.find(b)
        pa, pb = self.pot[a], self.pot[b]
        if ra == rb:
            return pb - pa == w
        self.parent[rb] = ra
        self.pot[rb] = pa + w - pb
        return True


def is_consistent(n, cons):
    """cons: [(x, y, w)]；判断 s[y]-s[x-1]=w 组是否有解（n 为结点数上界，仅需 n >= max y）。"""
    dsu = WeightedDSU(n + 1)  # 结点 0..n 表前缀和
    for x, y, w in cons:
        if not dsu.unite(x - 1, y, w):
            return False
    return True


# ---------------- 构造器 ----------------
def ledger_case(rng, n, m, amp=None):
    """由随机合法账本派生：先造 A[1..n]（|A_i| <= amp），再取区间和 => 必然 true。"""
    if amp is None:
        amp = W_HI // 4
    A = [rng.randint(-amp, amp) for _ in range(n)]
    pre = [0] * (n + 1)
    for i in range(1, n + 1):
        pre[i] = pre[i - 1] + A[i - 1]
    cons = []
    for _ in range(m):
        x = rng.randint(1, n)
        y = rng.randint(x, n)
        cons.append((x, y, pre[y] - pre[x - 1]))
    return cons


def make_case(rng, n, m, want_true, w_lo=W_LO, w_hi=W_HI, amp=None, tries=80):
    """造一组标签为 want_true 的约束组。"""
    for _ in range(tries):
        if want_true:
            cons = ledger_case(rng, n, m, amp)
        else:
            cons = []
            for _ in range(m):
                x = rng.randint(1, n)
                y = rng.randint(x, n)
                cons.append((x, y, rng.randint(w_lo, w_hi)))
        if is_consistent(n, cons) == want_true:
            return cons
    if not want_true and m >= 2:
        cons = ledger_case(rng, n, max(m - 2, 0), amp)
        x = rng.randint(1, n)
        y = rng.randint(x, n)
        w = rng.randint(w_lo, w_hi)
        cons.append((x, y, w))
        cons.append((x, y, w + 1 if w < W_EXT else w - 1))  # 同区间矛盾对
        assert not is_consistent(n, cons)
        return cons
    raise AssertionError("make_case 失败: want_true=%s n=%d m=%d" % (want_true, n, m))


# ---------------- 各测试点：每点 = (说明, [(n, cons, want?)...]) ----------------
def build_points():
    points = []

    # 点 1：边界 —— T=1、n=m=1、w=0
    points.append(("边界层：T=1、n=m=1、w=0（最小规模 + 权重边界）", [(1, [(1, 1, 0)], True)]))

    # 点 2：边界 —— 最小规模 false（同区间两次不同 w）
    points.append(("边界层：n=2，同一区间 (1,1) 两次给出不同 w=5/7 -> 必 false",
                   [(2, [(1, 1, 5), (1, 1, 7)], False)]))

    # 点 3：题面样例逐字复现
    points.append(("边界层：题面样例逐字复现（T=2）", [
        (3, [(1, 2, 10), (1, 3, -5), (3, 3, -15)], True),
        (5, [(1, 5, 100), (3, 5, 50), (1, 2, 51)], False),
    ]))

    # 点 4：小规模随机，全 true
    rng = random.Random(172504)
    pts4 = []
    for _ in range(20):
        n = rng.randint(1, 5)
        m = rng.randint(1, 5)
        pts4.append((n, make_case(rng, n, m, True), True))
    points.append(("小规模随机：T=20，n,m∈[1,5]，全部由随机合法账本派生 -> 全 true", pts4))

    # 点 5：小规模随机 true/false 交替，含 x=y 单月约束
    rng = random.Random(172505)
    pts5 = []
    for i in range(30):
        n = rng.randint(1, 10)
        m = rng.randint(1, 10)
        want = True if m == 1 else (i % 2 == 0)
        cons = make_case(rng, n, m, want)
        if i % 3 == 0:  # 掺入单月（x=y）约束，保持标签不变
            x = rng.randint(1, n)
            cand = [(x, x, cons[0][2])] + list(cons[1:])
            if is_consistent(n, cand) == want:
                cons = cand
        pts5.append((n, cons, want))
    points.append(("小规模随机：T=30，n,m∈[1,10]，true/false 交替；含 x=y 单月约束", pts5))

    # 点 6：中等规模，true/false 交替
    rng = random.Random(172506)
    pts6 = []
    for i in range(50):
        n = rng.randint(20, 50)
        m = rng.randint(20, 50)
        want = (i % 2 == 0)
        pts6.append((n, make_case(rng, n, m, want), want))
    points.append(("中等规模随机：T=50，n,m∈[20,50]，true/false 交替", pts6))

    # 点 7：中等偏大，true/false 交替
    rng = random.Random(172507)
    pts7 = []
    for i in range(60):
        n = rng.randint(50, 90)
        m = rng.randint(50, 90)
        want = (i % 2 == 0)
        pts7.append((n, make_case(rng, n, m, want), want))
    points.append(("中等偏大随机：T=60，n,m∈[50,90]，true/false 交替", pts7))

    # 点 8：大规模 + T 上界
    rng = random.Random(172508)
    pts8 = []
    for i in range(MAXT):
        n = rng.randint(90, MAXNM)
        m = rng.randint(90, MAXNM)
        want = (i % 2 == 0)
        pts8.append((n, make_case(rng, n, m, want), want))
    points.append(("大规模随机：T=99（T 上界），n,m∈[90,99]，true/false 交替", pts8))

    # 点 9：顶格 n=m=99 且全部 true（含结构化区间）
    rng = random.Random(172509)
    pts9 = []
    for _ in range(MAXT):
        n = MAXNM
        A = [rng.randint(-10000, 10000) for _ in range(n)]
        pre = [0] * (n + 1)
        for t in range(1, n + 1):
            pre[t] = pre[t - 1] + A[t - 1]
        spans = []
        for j in range(1, n + 1):
            if j % 4 == 0:
                spans.append((1, j))       # 前缀 x=1
            elif j % 4 == 1:
                spans.append((j, j))       # 单月 x=y
            elif j % 4 == 2:
                spans.append((j, n))       # 后缀 y=n
            else:
                spans.append((rng.randint(1, j), j))
        spans.append((1, n))               # 全长 x=1&y=n
        spans = spans[:MAXNM]
        spans[-1] = (1, n)                 # 确保「全长约束」不被截断（保持 m=99 且含 x=1&y=n）
        cons = [(x, y, pre[y] - pre[x - 1]) for (x, y) in spans]
        assert is_consistent(n, cons)
        pts9.append((n, cons, True))
    points.append(("顶格层：T=99，n=m=99 且全 true；含 x=y / x=1 / y=n / x=1&y=n 结构", pts9))

    # 点 10：顶格最坏混合（极值权重 + 重复区间 + 全长）
    rng = random.Random(172510)
    pts10 = []
    for i in range(MAXT):
        n = MAXNM
        m = MAXNM
        want = (i % 2 == 0)
        if i % 2 == 0:
            cons = make_case(rng, n, m, want, -W_EXT, W_EXT, amp=AMP_EXT)  # w ∈ ±10^6
            if i % 4 == 0:
                cons[0] = (1, n, cons[0][2])                      # 全长约束
                if is_consistent(n, cons) != want:
                    cons = make_case(rng, n, m, want, -W_EXT, W_EXT, amp=AMP_EXT)
        else:
            cons = make_case(rng, n, m, want)
            if i % 4 == 1:                                        # 重复区间
                x, y, w = cons[0]
                cons[1] = (x, y, w)
                if is_consistent(n, cons) != want:
                    cons = make_case(rng, n, m, want)
        pts10.append((n, cons, want))

    # 点 10 前两组换成确定性的边界结构（保证 w 恰好取到 ±10^6 与 0）
    n = MAXNM
    c_ext_true = [(1, 1, W_EXT)] * 50 + [(1, n, W_EXT)] + \
        [(2, n, 0), (2, 2, 0), (n, n, 0)] * 16                       # 50 + 1 + 48 = 99
    c_ext_false = [(1, 1, W_EXT), (1, 1, -W_EXT)] + [(1, n, W_EXT), (2, n, 0)] * 48 + \
        [(n, n, 0)]                                                  # 2 + 96 + 1 = 99
    assert len(c_ext_true) == MAXNM and is_consistent(n, c_ext_true)
    assert len(c_ext_false) == MAXNM and not is_consistent(n, c_ext_false)
    pts10[0] = (n, c_ext_true, True)    # A[1]=10^6，其余月 0；单月/全长均为 +10^6
    pts10[1] = (n, c_ext_false, False)  # 同一区间 (1,1) 同时要求 +10^6 与 -10^6
    points.append(("顶格层（最坏混合）：T=99，n=m=99，true/false 交替；w 含 ±10^6 大权重、"
                   "重复区间与 x=1&y=n 全长约束", pts10))

    return points


# ---------------- 生成 + 自检 ----------------
def main():
    # std 二进制缺失时必须硬失败：否则 io.output_gen 会静默产出空 .out
    if not os.path.exists(STD):
        raise SystemExit("找不到 std 二进制：%s\n请先执行 g++ -O2 -std=c++17 std.cpp -o std" % STD)

    points = build_points()
    assert len(points) == 10, "必须恰好 10 个测试点"

    all_cases = []
    ntrue = nfalse = 0
    for idx, (note, data) in enumerate(points, 1):
        assert 0 < len(data) <= MAXT, "点 %d 组数 %d 越界 (T<100)" % (idx, len(data))
        cnt = [0, 0]
        for n, cons, want in data:
            assert 1 <= n < 100 and 1 <= len(cons) < 100, "点 %d 的 n/m 越界" % idx
            for x, y, w in cons:
                assert 1 <= x <= y <= n, "点 %d 区间非法 (%d,%d) n=%d" % (idx, x, y, n)
                assert abs(w) <= W_EXT, "点 %d 权重越界 w=%d" % (idx, w)
            lab = is_consistent(n, cons)
            assert lab == want, "点 %d 存在标签不符的 case（构造 bug）" % idx
            cnt[lab] += 1
            all_cases.append((n, cons))
        ntrue += cnt[1]
        nfalse += cnt[0]
        print("problem%-2d: T=%-2d n∈[%d,%d] m∈[%d,%d] true=%-2d false=%-2d -- %s"
              % (idx, len(data), min(c[0] for c in data), max(c[0] for c in data),
                 min(len(c[1]) for c in data), max(len(c[1]) for c in data), cnt[1], cnt[0], note))

    # 覆盖自检：边界与顶格都被真实使用
    assert min(len(c) for _n, c in all_cases) == 1, "缺 m=1 最小规模"
    assert max(len(c) for _n, c in all_cases) == MAXNM, "缺 m=99 顶格规模"
    assert min(n for n, _c in all_cases) == 1, "缺 n=1 最小规模"
    assert any(len(c) == MAXT for _n, c in all_cases), "缺 T=99 顶格组数"
    assert any(x == y for _n, c in all_cases for x, y, _w in c), "缺 x=y 单月约束"
    assert any(x == 1 and y == n for n, c in all_cases for x, y, _w in c), "缺 x=1&y=n 全长约束"
    assert any(abs(w) == W_EXT for _n, c in all_cases for _x, _y, w in c), "缺 w=±10^6 大权重"
    assert any(w == 0 for _n, c in all_cases for _x, _y, w in c), "缺 w=0 权重边界值"
    print("覆盖自检通过：共 %d 组 case，true=%d，false=%d" % (len(all_cases), ntrue, nfalse))

    # ---------------- 写文件 ----------------
    for idx, (_note, data) in enumerate(points, 1):
        io = IO(file_prefix="problem", data_id=idx)   # problem{idx}.in / problem{idx}.out
        io.input_writeln(len(data))                   # 第一行：T
        for n, cons, _want in data:
            io.input_writeln(n, len(cons))
            for x, y, w in cons:
                io.input_writeln(x, y, w)
        io.output_gen(STD)
    print("生成完成：data/problem1..10.in/.out")


if __name__ == "__main__":
    main()
