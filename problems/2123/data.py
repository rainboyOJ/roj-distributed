#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
一本通 2123《图的存储与访问》（目标 ROJ 题号 2123）测试数据生成器。

题意（content.md 逐字口径）：
  给出 N 个点、M 条边的**有向图**，K 次询问；每次询问给出 (X, Y)，求从点 X 出发能否抵达
  点 Y。能抵达输出 Yes，否则输出 No（共 K 行）。
  第 1 行 N M K；接下来 M 行每行 U_i V_i 表示有向边 (U_i, V_i)（只有 U_i -> V_i 一个方向）；
  接下来 K 行每行 X Y 表示询问。

数据范围与分层依据：
  - 题面【提示】「对于 100% 的数据，1 <= N, M <= 10^3」（官方 OJ 页
    http://ybt.ssoier.cn:8088/problem_show.php?pid=2123 实测一致）→ N、M 上限均取 10^3。
  - 题面**未声明 K 的上限**；本包取工作范围 1 <= K <= 10^3（与 N、M 同量级），
    依据与风险见 gen-report.md 风险点 2。std 对每个询问是 O(1) 查表（可达集预处理），
    故该取值不影响标程正确性。
  - 题面**未禁止重边与自环**（只说「M 条边，每行 2 个整数 U_i, V_i」），故本包数据显式包含
    重边与自环（点 1/3/7/9/10 定向构造，点 5/6/8 随机边天然含），见风险点 4。
  - **可达性语义**：题面未明确「x = y 时算不算可达」。网络来源（std.cpp 注释 [2][3]）一致采用
    「路径长度可为 0，reach[x][x] 恒为真」的通行约定。为让数据与本处语义选择**完全解耦**，
    生成器强制校验每条询问满足：**「长度 >= 0」与「长度 >= 1」两种读法结论一致**
    （即只使用无歧义对：x != y，或 x == y 但 x 有自环 / 处于环上）。见风险点 3。

10 个测试点分层（从最小铺到顶格；详见 gen-report.md 分层表）：

  点  层            规模 N/M/K        结构                                   设计意图
  --  -----------  ----------------  -------------------------------------  ------------------------------------
  1   边界层       1 / 1 / 1         自环 1->1                              全最小规模；自环极端 -> Yes
  2   边界层       4 / 3 / 2         题面【输入样例】原样                     题面声明值（可手算）
  3   小规模随机   4 / 6 / 6         含 2 条重边 + 1 条自环 的小随机           重边/自环合法性 + 方向唯一性 + (x,x)->Yes
  4   小规模随机   8 / 10 / 8        无重边无自环的稀疏随机                    可手算量级
  5   中等规模随机 150 / 400 / 200   均匀随机有向图                           范围中间档随机
  6   中等规模随机 300 / 500 / 200   均匀随机有向图（边更稀疏）              中间档偏上
  7   大规模菊花   800 / 800 / 400   菊花(hub)：中心 1 连出其余 799 点 + 中心自环  单源可达全图 / 叶子间大量不可达
  8   大规模随机   1000 / 1000 / 500 均匀随机有向图                           N、M 均顶满的随机
  9   顶格层       1000 / 1000 /1000 999 长链 + 1 条重边                       最长可达路径 / 最坏搜索深度（卡递归 DFS）
  10  顶格层       1000 / 1000 /1000 500 点强连通环 + 500 条随机边（含自环）    稠密可达集（环内 25 万对全可达）+ 稀疏分量对照

随机性：每个测试点使用独立 Random(2123 + 点号)，与调用顺序无关、可精确复现。
生成后自检：读回 .in/.out，用**与 std.cpp 实现路径无关的纯 Python 参考实现**复算期望答案并
逐字节比对，同时断言每点的结构性特征（规模上限、重边/自环、长链、强连通环、无歧义询问）。
"""

import os
import random
import sys

from cyaron import *  # 引入CYaRon的库

# --------------------------------------------------------------------------
# 全局设定（题面范围）
# --------------------------------------------------------------------------
MAXN = 1000          # 点数上限（题面「1 <= N, M <= 10^3」）
MAXM = 1000          # 边数上限（同上）
MAXK = 1000          # 询问数工作上限（题面未声明 K 上限；取与 N、M 同量级，见风险点 2）

SAMPLE_N, SAMPLE_M, SAMPLE_K = 4, 3, 2                     # 题面【输入样例】
SAMPLE_EDGES = [(1, 2), (2, 4), (4, 3)]                    # 题面【输入样例】的边
SAMPLE_QUERIES = [(1, 3), (4, 1)]                          # 题面【输入样例】的询问


# --------------------------------------------------------------------------
# 独立参考实现（纯 Python，与 std.cpp 的 C++ 路径完全不同）
# --------------------------------------------------------------------------
def build_reference(n, edges):
    """返回 (R0, R1)：
         R0[s]：从 s 出发、**路径长度 >= 0** 可达的点集（通行传递闭包语义，s ∈ R0[s]）
         R1[s]：从 s 出发、**路径长度 >= 1** 可达的点集（严格正长度）
       两者对同一 (x, y) 结论不同 <=> 只能靠零长度路径到达 <=> x == y 且 x 不在任何环上。
    """
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)

    R0 = [set() for _ in range(n + 1)]
    for s in range(1, n + 1):
        seen = R0[s]
        seen.add(s)                      # 零长度路径：自己可达自己
        stack = [s]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)

    R1 = [set() for _ in range(n + 1)]
    for s in range(1, n + 1):
        acc = R1[s]
        for v in adj[s]:
            acc |= R0[v]                 # s 先走一步到 v，再从 v 走零或多步
    return R0, R1


def is_unambiguous(R0, R1, x, y):
    """两种语义读法结论是否一致（一致才允许写入数据）。"""
    return (y in R0[x]) == (y in R1[x])


def sample_yes(n, R0, R1, rng, cnt, used):
    """抽样 cnt 个答案为 Yes 且语义无歧义的**去重**询问（不与 used 重复）。

    Yes 且无歧义 <=> y ∈ R0[x] 且 y ∈ R1[x]（存在正长度通路）。
    直接在候选上抽样，不做 10^6 级全扫描。
    """
    cand = [s for s in range(1, n + 1) if R0[s] & R1[s]]
    if not cand:
        return []
    pool, seen = [], set(used)
    tries = 0
    limit = 200 * cnt + 2000
    while len(pool) < cnt and tries < limit:
        tries += 1
        s = rng.choice(cand)
        ys = sorted(R0[s] & R1[s])
        y = ys[rng.randrange(len(ys))]
        if (s, y) in seen:
            continue
        seen.add((s, y))
        pool.append((s, y))
    if len(pool) < cnt:                                # 兜底：全量枚举（候选很少时）
        for s in cand:
            for y in sorted(R0[s] & R1[s]):
                if len(pool) >= cnt:
                    break
                if (s, y) in seen:
                    continue
                seen.add((s, y))
                pool.append((s, y))
            if len(pool) >= cnt:
                break
    return pool


def sample_no(n, R0, rng, cnt, used, tries_factor=400):
    """抽样 cnt 个答案为 No 的**去重**询问（不与 used 重复）。

    No 必无歧义：R1[s] ⊆ R0[s]，故 y ∉ R0[s] 蕴含 y ∉ R1[s]。
    """
    pool, seen = [], set(used)
    tried = 0
    limit = max(cnt * tries_factor, 3000)
    while len(pool) < cnt and tried < limit:
        tried += 1
        x = rng.randint(1, n)
        y = rng.randint(1, n)
        if y in R0[x] or (x, y) in seen:
            continue
        seen.add((x, y))
        pool.append((x, y))
    if len(pool) < cnt:                                # 兜底：全量扫描（稠密图才可能走到）
        for x in range(1, n + 1):
            for y in range(1, n + 1):
                if len(pool) >= cnt:
                    break
                if y in R0[x] or (x, y) in seen:
                    continue
                seen.add((x, y))
                pool.append((x, y))
            if len(pool) >= cnt:
                break
    return pool


def make_queries(n, R0, R1, rng, k, yes_ratio, forced=()):
    """生成 k 个「语义无歧义且互不重复」的询问：约 yes_ratio 比例为 Yes，forced 先放入。"""
    forced = list(forced)
    assert len(set(forced)) == len(forced), "强制询问自身有重复"
    for (x, y) in forced:                              # 断言强制询问本身无歧义
        assert is_unambiguous(R0, R1, x, y), "强制询问 (%d,%d) 语义有歧义" % (x, y)
    assert len(forced) <= k, "强制询问数 %d 超过 K=%d" % (len(forced), k)
    need = k - len(forced)
    nyes = int(round(need * yes_ratio))
    nno = need - nyes
    used = set(forced)                                 # 全局去重集合

    yes_pool = sample_yes(n, R0, R1, rng, nyes, used) if nyes else []
    used |= set(yes_pool)
    no_pool = sample_no(n, R0, rng, nno, used) if nno else []
    assert len(yes_pool) >= nyes, "Yes 询问池不足（要 %d，只有 %d）" % (nyes, len(yes_pool))
    assert len(no_pool) >= nno, "No 询问池不足（要 %d，只有 %d）" % (nno, len(no_pool))

    qs = forced + yes_pool[:nyes] + no_pool[:nno]
    rng.shuffle(qs)
    return qs


def random_edges(rng, n, m, allow_loop=True, no_dup=False):
    """均匀随机有向边序列：允许重边（no_dup=False 时）；allow_loop 控制是否允许自环。"""
    edges = []
    seen = set()
    guard = 0
    while len(edges) < m and guard < 200 * m + 10000:
        guard += 1
        u = rng.randint(1, n)
        v = rng.randint(1, n)
        if not allow_loop and u == v:
            continue
        if no_dup and (u, v) in seen:
            continue
        seen.add((u, v))
        edges.append((u, v))
    assert len(edges) == m, "随机边生成不足（n=%d m=%d 只有 %d 条）" % (n, m, len(edges))
    return edges


# --------------------------------------------------------------------------
# 10 个测试点构造：返回 (n, edges, queries, note)
# --------------------------------------------------------------------------
def build_point(i):
    rng = random.Random(2123 + i)      # 每个点独立种子，可精确复现

    # ---------------- 点 1：边界层 · 全最小规模 + 自环 ----------------
    if i == 1:
        n, edges, k = 1, [(1, 1)], 1
        R0, R1 = build_reference(n, edges)
        qs = make_queries(n, R0, R1, rng, k, 1.0, forced=[(1, 1)])
        return (n, edges, qs,
                "边界层：全最小规模 N=M=K=1；唯一边为自环 1->1，唯一询问 (1,1) -> Yes")

    # ---------------- 点 2：边界层 · 题面【输入样例】原样 ----------------
    if i == 2:
        return (SAMPLE_N, SAMPLE_EDGES, SAMPLE_QUERIES,
                "边界层：题面【输入样例】原样（N=4 M=3 K=2）—— 答案 Yes/No，题面声明值")

    # ---------------- 点 3：小规模随机 · 含重边 + 自环 ----------------
    if i == 3:
        n, m, k = 4, 6, 6
        for extra in range(60):                        # 换种子直到 Yes/No 询问都取得到
            rng3 = random.Random(2123 + i + extra * 1000)
            base = []
            while len(base) < 3:                       # 3 条互不相同的普通边（u != v）
                u = rng3.randint(1, n)
                v = rng3.randint(1, n)
                if u != v and (u, v) not in base:
                    base.append((u, v))
            u3 = base[rng3.randrange(len(base))][0]
            edges = list(base) + [base[0], base[0]]    # + 2 条**重边**
            edges.append((u3, u3))                     # + 1 条**自环**
            while len(edges) < m:                      # + 1 条补充随机边
                edges.append((rng3.randint(1, n), rng3.randint(1, n)))
            assert len(edges) == m
            R0, R1 = build_reference(n, edges)
            self_q = [(u3, u3)]                        # 自环点的 (x,x) 询问 -> Yes（语义无歧义）
            if sample_yes(n, R0, R1, rng3, 1, set()) and sample_no(n, R0, rng3, 1, set()):
                qs = make_queries(n, R0, R1, rng3, k, 0.5, forced=self_q)
                return (n, edges, qs,
                        "小规模随机：N=4 M=6 K=6，含 2 条重边 + 1 条自环 + 自环点 (x,x) 询问")
        raise AssertionError("点 3 找不到 Yes/No 齐备的含自环随机图")

    # ---------------- 点 4：小规模随机 · 无重边无自环 ----------------
    if i == 4:
        n, m, k = 8, 10, 8
        for extra in range(60):
            rng4 = random.Random(2123 + i + extra * 1000)
            edges = random_edges(rng4, n, m, allow_loop=False, no_dup=True)
            R0, R1 = build_reference(n, edges)
            if sample_yes(n, R0, R1, rng4, 1, set()) and sample_no(n, R0, rng4, 1, set()):
                qs = make_queries(n, R0, R1, rng4, k, 0.5)
                return (n, edges, qs,
                        "小规模随机：N=8 M=10 K=8，无重边无自环、Yes/No 各半（可手算量级）")
        raise AssertionError("点 4 找不到 Yes/No 齐备的随机图")

    # ---------------- 点 5：中等规模随机（中间档） ----------------
    if i == 5:
        n, m, k = 150, 400, 200
        edges = random_edges(rng, n, m)                # 允许自环/重边（题面未禁止）
        R0, R1 = build_reference(n, edges)
        qs = make_queries(n, R0, R1, rng, k, 0.4)
        return (n, edges, qs,
                "中等规模随机：N=150 M=400 K=200，均匀随机有向图（Yes:No ≈ 4:6）")

    # ---------------- 点 6：中等规模随机（中间档偏上） ----------------
    if i == 6:
        n, m, k = 300, 500, 200
        edges = random_edges(rng, n, m)
        R0, R1 = build_reference(n, edges)
        qs = make_queries(n, R0, R1, rng, k, 0.35)
        return (n, edges, qs,
                "中等规模随机：N=300 M=500 K=200，均匀随机有向图（更稀疏、更靠近上限档）")

    # ---------------- 点 7：大规模 · 菊花（hub）定向结构 -------------
    if i == 7:
        n, m, k = 800, 800, 400
        # 菊花（星）：中心点 1 向其余 799 个点各连一条出边（799 条），再加中心点自环 1 条 = M=800。
        # 可达性极端：reach(1) = 全部 800 点（中心单源可达全图，卡「只扩几步/固定小 visited」），
        #             reach(v) = {v}（叶子之间互不可达 -> 大量 No）。
        edges = [(1, v) for v in range(2, n + 1)] + [(1, 1)]
        assert len(edges) == m, "点 7 边数 %d != %d" % (len(edges), m)
        R0, R1 = build_reference(n, edges)
        qs = make_queries(n, R0, R1, rng, k, 0.5,
                          forced=[(1, n), (n, 1), (1, 1), (n, n - 1)])
        return (n, edges, qs,
                "大规模菊花(hub)：N=M=800 K=400，中心 1 连出全部 799 点 + 中心自环；"
                "单源可达全图 / 叶子间大量不可达")

    # ---------------- 点 8：大规模随机（N、M 顶满） ----------------
    if i == 8:
        n, m, k = MAXN, MAXM, 500
        edges = random_edges(rng, n, m)
        R0, R1 = build_reference(n, edges)
        qs = make_queries(n, R0, R1, rng, k, 0.35)
        return (n, edges, qs,
                "大规模随机：N=1000 M=1000 K=500，均匀随机有向图（N、M 均取满上限）")

    # ---------------- 点 9：顶格层 · 长链（最长可达路径 / 最坏搜索深度） ----------------
    if i == 9:
        n, m, k = MAXN, MAXM, 1000
        edges = [(u, u + 1) for u in range(1, n)]      # 999 条链边 1->2->...->1000
        edges.append((1, 2))                           # 第 1000 条 = 重边
        assert len(edges) == m
        R0, R1 = build_reference(n, edges)
        qs = make_queries(n, R0, R1, rng, k, 0.5,
                          forced=[(1, n), (n, 1), (2, n), (n, n - 1)])
        return (n, edges, qs,
                "顶格层：N=M=1000 K=1000，999 长链 + 1 条重边；i<=j 可达 / i>j 不可达，卡递归 DFS 深度")

    # ---------------- 点 10：顶格层 · 强连通环 + 随机稀疏分量 ----------------
    if i == 10:
        n, m, k = MAXN, MAXM, 1000
        half = 500
        edges = [(u, u + 1) for u in range(1, half)]   # 1->2->...->500
        edges.append((half, 1))                        # 500->1：1..500 构成 500 点强连通环
        while len(edges) < m:                          # 501..1000 上 500 条随机边（含自环/重边）
            edges.append((rng.randint(half + 1, n), rng.randint(half + 1, n)))
        assert len(edges) == m
        R0, R1 = build_reference(n, edges)
        qs = make_queries(n, R0, R1, rng, k, 0.6,
                          forced=[(1, half), (half, 1), (1, 1), (half, half),
                                  (1, n), (n, 1), (half + 1, half)])
        return (n, edges, qs,
                "顶格层：N=M=1000 K=1000，500 点强连通环（环内 25 万对全可达）+ 500 条随机边；含环上 (x,x)")

    raise ValueError("未知测试点编号：%d" % i)


# --------------------------------------------------------------------------
# 生成 + 生成后自检
# --------------------------------------------------------------------------
def main():
    here = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(here, "data")
    built = {}

    # 前置检查：cyaron 的 io.output_gen("../std") 需要 staging/2123/std 已编译；
    # 缺失时它会写出空 .out（后续自检会报错），故这里提前报错、不留半成品。
    std_path = os.path.join(here, "std")
    if not (os.path.exists(std_path) and os.access(std_path, os.X_OK)):
        print("缺少可执行文件 %s —— 请先执行 g++ -O2 -std=c++17 std.cpp -o std" % std_path,
              file=sys.stderr)
        raise SystemExit(2)
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    print("=== 生成 10 组测试数据（problem1..problem10） ===")
    for i in range(1, 11):
        n, edges, qs, note = build_point(i)
        m, k = len(edges), len(qs)
        assert 1 <= n <= MAXN, "点 %d：N=%d 超范围" % (i, n)
        assert 1 <= m <= MAXM, "点 %d：M=%d 超范围" % (i, m)
        assert 1 <= k <= MAXK, "点 %d：K=%d 超范围" % (i, k)
        for (u, v) in edges:
            assert 1 <= u <= n and 1 <= v <= n, "点 %d：边 (%d,%d) 越界" % (i, u, v)
        for (x, y) in qs:
            assert 1 <= x <= n and 1 <= y <= n, "点 %d：询问 (%d,%d) 越界" % (i, x, y)

        io = IO(file_prefix="problem", data_id=i)      # problemI.in / problemI.out
        io.input_write(n, m, k, "\n")
        for (u, v) in edges:
            io.input_write(u, v, "\n")
        for (x, y) in qs:
            io.input_write(x, y, "\n")
        io.output_gen("../std")
        io.close()                                     # 显式关闭，保证 .in/.out 落盘后再自检
        built[i] = (n, edges, qs, note)

    # ---- 生成后自检 ----
    problems = []

    def check(cond, msg):
        if not cond:
            problems.append(msg)

    print("\n=== 生成后自检：.in 回读 + 独立 Python 参考实现复算 + 结构性断言 ===")
    for i in range(1, 11):
        n, edges, qs, note = built[i]
        in_path = os.path.join(data_dir, "problem%d.in" % i)
        out_path = os.path.join(data_dir, "problem%d.out" % i)
        raw_in = open(in_path, "r", encoding="utf-8", newline="").read()
        raw_out = open(out_path, "r", encoding="utf-8", newline="").read()

        toks = raw_in.split()
        check(len(toks) >= 3 and toks[:3] == [str(n), str(len(edges)), str(len(qs))],
              "点 %d：.in 首行 %r 与构造不符" % (i, toks[:3]))
        rn, rm, rk = int(toks[0]), int(toks[1]), int(toks[2])
        check(len(toks) == 3 + 2 * rm + 2 * rk,
              "点 %d：.in 数字个数 %d != 3+2M+2K=%d" % (i, len(toks), 3 + 2 * rm + 2 * rk))
        r_edges = [(int(toks[3 + 2 * j]), int(toks[4 + 2 * j])) for j in range(rm)]
        r_qs = [(int(toks[3 + 2 * rm + 2 * j]), int(toks[4 + 2 * rm + 2 * j])) for j in range(rk)]
        check(r_edges == edges, "点 %d：回读的边序列与构造不一致" % i)
        check(r_qs == qs, "点 %d：回读的询问序列与构造不一致" % i)

        # (1) 规模与编号范围（题面上限）
        check(1 <= rn <= MAXN, "点 %d：N=%d 超出题面上限 %d" % (i, rn, MAXN))
        check(1 <= rm <= MAXM, "点 %d：M=%d 超出题面上限 %d" % (i, rm, MAXM))
        check(1 <= rk <= MAXK, "点 %d：K=%d 超出本包工作上限 %d" % (i, rk, MAXK))
        for (u, v) in r_edges:
            check(1 <= u <= rn and 1 <= v <= rn, "点 %d：边 (%d,%d) 编号越界" % (i, u, v))
        for (x, y) in r_qs:
            check(1 <= x <= rn and 1 <= y <= rn, "点 %d：询问 (%d,%d) 编号越界" % (i, x, y))

        # (2) 独立参考实现复算 + 与 std 输出逐字节比对
        R0, R1 = build_reference(rn, r_edges)
        want = "".join(("Yes\n" if y in R0[x] else "No\n") for (x, y) in r_qs)
        check(raw_out == want, "点 %d：std 输出与独立参考实现不一致" % i)
        check(raw_out.count("\n") == rk, "点 %d：输出行数 %d != K=%d" % (i, raw_out.count("\n"), rk))

        # (3) 语义无歧义守卫：每条询问在两种读法下结论一致
        for (x, y) in r_qs:
            check(is_unambiguous(R0, R1, x, y),
                  "点 %d：询问 (%d,%d) 在「长度>=0」与「长度>=1」两种读法下结论不同" % (i, x, y))

        nyes = want.count("Yes")
        print("点 %2d | N=%4d M=%4d K=%4d | Yes %4d / No %4d | %s"
              % (i, rn, rm, rk, nyes, rk - nyes, note))

    # (4) 逐点结构性断言
    n1, e1, q1, _ = built[1]
    check(n1 == 1 and e1 == [(1, 1)] and q1 == [(1, 1)], "点 1 不是「N=M=K=1 + 自环 (1,1)」全最小规模")
    check(built[2][1] == SAMPLE_EDGES and built[2][2] == SAMPLE_QUERIES, "点 2 不是题面样例原样")

    n3, e3, q3, _ = built[3]
    check(len(set(e3)) < len(e3), "点 3 应含重边")
    check(any(u == v for (u, v) in e3), "点 3 应含自环")
    check(any(x == y for (x, y) in q3), "点 3 应含自环点 (x,x) 形式的询问")
    check(n3 == 4 and len(e3) == 6, "点 3 规模应为 N=4 M=6")

    n4, e4, _, _ = built[4]
    check(len(set(e4)) == len(e4) and all(u != v for (u, v) in e4), "点 4 不应含重边或自环")
    check(n4 == 8 and len(e4) == 10, "点 4 规模应为 N=8 M=10")

    check(built[5][0] == 150 and len(built[5][1]) == 400, "点 5 规模应为 N=150 M=400")
    check(built[6][0] == 300 and len(built[6][1]) == 500, "点 6 规模应为 N=300 M=500")

    n7, e7, q7, _ = built[7]
    eset7 = set(e7)
    check(n7 == 800 and len(e7) == 800, "点 7 规模应为 N=800 M=800")
    check(all(((1, v) in eset7) for v in range(2, n7 + 1)), "点 7 应含中心 1 -> 其余全部点的菊花边")
    check((1, 1) in eset7, "点 7 应含中心点自环")
    R0_7, _R1_7 = build_reference(n7, e7)
    check(len(R0_7[1]) == n7, "点 7 中心应可达全部 %d 个点（实际 %d）" % (n7, len(R0_7[1])))
    check(all(len(R0_7[v]) == (n7 if v == 1 else 1) for v in range(1, n7 + 1)),
          "点 7 除中心外，每个叶子应只可达自己")
    check(any(x == y for (x, y) in q7), "点 7 应含中心点 (x,x) 形式的询问")

    check(built[8][0] == MAXN and len(built[8][1]) == MAXM, "点 8 应 N=M=1000 顶满")

    n9, e9, _, _ = built[9]
    eset9 = set(e9)
    check(n9 == MAXN and len(e9) == MAXM, "点 9 应 N=M=1000 顶格")
    check(all(((u, u + 1) in eset9) for u in range(1, n9)), "点 9 应含 1->2->...->1000 完整长链")
    check(len(eset9) < len(e9), "点 9 应含重边")

    n10, e10, q10, _ = built[10]
    check(n10 == MAXN and len(e10) == MAXM, "点 10 应 N=M=1000 顶格")
    eset10 = set(e10)
    check(all(((u, u + 1) in eset10) for u in range(1, 500)) and (500, 1) in eset10,
          "点 10 应含 1..500 的完整强连通环")
    R0_10, _R1_10 = build_reference(n10, e10)
    check(len(R0_10[1]) >= 500, "点 10 环内应至少 500 点互相可达（实际 %d）" % len(R0_10[1]))
    check(any(x == y for (x, y) in q10), "点 10 应含环上 (x,x) 形式的询问")

    if problems:
        print("\n自检失败：", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        raise SystemExit(1)
    print("\n自检全部通过：10/10 组 .in/.out 成对齐全；规模不超过题面上限；"
          "std 输出与独立参考实现逐字节一致；每条询问在两种语义读法下均无歧义；"
          "各点分层结构性断言（自环 / 重边 / 长链 / 强连通环 / 顶格）全部成立。")


if __name__ == "__main__":
    main()
