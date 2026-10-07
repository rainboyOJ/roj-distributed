#!/usr/bin/env python
# 一本通 2126《[USACO19OPEN] Milk Factory》 分层数据生成器
#
# 题意：N 个加工站（1..N，1<=N<=100）、N-1 条**单向**传送带 a_i -> b_i；题面括号说明这些
#       通道用「最小数量」把所有站连起来 => 无向结构是一棵树。求最小的 i，使从其他每个
#       加工站出发都能沿有向边（可经中间站）到达 i；不存在则输出 -1。
# 限制：time 1000ms / memory 64MB（config.json）。
#
# 分层设计（10 组，每组 1 个测试用例；N 从最小铺到题面上限）：
#   点  层             N     结构                                    期望答案   设计意图
#   --  ------------  ----  --------------------------------------  ---------  --------------------------------
#   1   边界层          1    无通道（0 行边）                          1        全最小规模；答案 1 的极端；
#                                                                              退化输入（无通道）
#   2   边界层          2    2 -> 1                                    1        最小非平凡规模；唯一 sink 且
#                                                                              为最大编号（卡「答案只能是 1」）
#   3   小规模·特殊值   3    题面样例原样 1->2, 3->2                     2        题面【输入样例】原样喂入
#   4   小规模随机      5..9 随机树 + 随机定向（条件 sink>=2）           -1       小规模**无解**随机数据，
#                                                                              可人工展开每个 i 验证
#   5   中等规模随机   30    随机树·全部朝随机根（根∈[2,N]）              根       有解·唯一 sink·中等规模
#   6   中等规模随机   45    随机树 + 随机定向（条件 sink>=2）           -1       无解·多 sink·中等规模
#   7   大规模·星形    80    星形：所有叶子 -> 中心 1                     1       有解·答案=1 的极端·最大度数
#                                                                              N-1=79（卡「出度/度数」类错解）
#   8   大规模·链      90    链（有序）1->2->...->90                     90       有解·答案=最大编号·DFS 路径最深
#                                                                              （N-1=89 层），接近上限
#   9   顶格层         100   链 1->2->...->100                         100       顶格·答案=100：标程需先枚举
#                                                                              1..99 全部失败才命中，枚举最坏
#   10  顶格层         100   随机树 + 随机定向（条件 sink>=2）           -1       顶格·无解：100 个 i 全部
#                                                                              失败（标程工作量最大情形）
#
# 关于题面列表里的「多解」：本题在题面保证（N-1 条边、无向结构是树）下**答案至多唯一**——
#   若 i≠j 同时满足，则 i 可到 j、j 可到 i，构成有向环，与「N-1 条边连通无环」矛盾。
#   所以数据里不存在「多解」这一层，只有「有解（唯一）」与「无解」；理由已写入 gen-report.md。
#   同理，本生成器**不造**含环或不连通的一般有向图（虽然题面输入约束字面上未禁止 a_i->b_i
#   形成环，但「用最小数量通道连通所有站」的保证意味着数据应为树；若造环会把依赖该保证的
#   官方解法判错，属越界数据）。
#
# 生成方式：cyaron 的 IO(file_prefix="problem", data_id=i) + io.output_gen("../std")，
#   产出 problem1.in/.out ... problem10.in/.out。每个点用独立固定种子，重跑结果一致。
# 生成后自检：读回 .in/.out，用**独立的纯 Python 参考实现**（逐点反向 BFS 可达性计数，
#   与 std.cpp 的反图 DFS 不同路径）复算答案并逐字节比对；同时断言每个点的分层结构特征
#   （树性、N 值、sink 数、答案、链/星形等）。

import os
import random
import sys

from cyaron import IO  # 引入 CYaRon 的库

MAXN = 100  # 题面上限 1 <= N <= 100


# --------------------------------------------------------------------------
# 独立参考实现（纯 Python，与 std.cpp 的 C++ 反图 DFS 完全不同的实现路径）
# --------------------------------------------------------------------------
def ref_answer(n, edges):
    """按题面定义逐点判定：能否从所有其他站到达 i（反向 BFS 计数），返回最小 i，否则 -1。"""
    rev = [[] for _ in range(n + 1)]  # 反图：rev[b] 存所有 a 使 a->b
    for (a, b) in edges:
        rev[b].append(a)
    for i in range(1, n + 1):
        seen = [False] * (n + 1)
        seen[i] = True
        stack = [i]
        cnt = 0
        while stack:
            u = stack.pop()
            cnt += 1
            for v in rev[u]:
                if not seen[v]:
                    seen[v] = True
                    stack.append(v)
        if cnt == n:
            return i
    return -1


def is_tree(n, edges):
    """题面保证的结构：N-1 条边、无自环、无向意义下连通无环。"""
    if len(edges) != max(0, n - 1):
        return False, "边数 %d != N-1=%d" % (len(edges), n - 1)
    for (a, b) in edges:
        if not (1 <= a <= n and 1 <= b <= n) or a == b:
            return False, "非法边 (%d,%d)" % (a, b)
    par = list(range(n + 1))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    for (a, b) in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False, "出现环于边 (%d,%d)" % (a, b)
        par[ra] = rb
    roots = set(find(v) for v in range(1, n + 1))
    if len(roots) != 1:
        return False, "不连通（%d 个连通块）" % len(roots)
    return True, "tree"


def sinks(n, edges):
    out = set(u for (u, _v) in edges)
    return [v for v in range(1, n + 1) if v not in out]


# --------------------------------------------------------------------------
# 结构构造
# --------------------------------------------------------------------------
def random_tree(n, rnd):
    """随机树：父亲随机取 1..v-1（保证连通无环），再随机重标号打散编号偏置。"""
    assert n >= 1
    if n == 1:
        return []
    es = [(rnd.randint(1, v - 1), v) for v in range(2, n + 1)]
    perm = list(range(1, n + 1))
    rnd.shuffle(perm)
    lab = dict((i + 1, perm[i]) for i in range(n))
    return [(lab[u], lab[v]) for (u, v) in es]


def orient_toward_root(n, undirected_edges, root):
    """把所有无向边定向为「指向 root」：唯一 sink = root，所有站都能到达 root。"""
    adj = [[] for _ in range(n + 1)]
    for (u, v) in undirected_edges:
        adj[u].append(v)
        adj[v].append(u)
    par = [0] * (n + 1)
    seen = [False] * (n + 1)
    seen[root] = True
    order = [root]
    for u in order:
        for w in adj[u]:
            if not seen[w]:
                seen[w] = True
                par[w] = u
                order.append(w)
    assert len(order) == n, "构造的不是树"
    return [(v, par[v]) for v in range(1, n + 1) if v != root]


def random_orientation(edges, rnd):
    return [(u, v) if rnd.random() < 0.5 else (v, u) for (u, v) in edges]


def chain_up(n):
    return [(i, i + 1) for i in range(1, n)]


def star_to_center(n, center):
    return [(v, center) for v in range(1, n + 1) if v != center]


def randomised_tree_no_solution(n, rnd, tries=200):
    """随机树 + 随机定向，条件化到 sink 数 >= 2（即必然 -1）；返回 (edges, sink列表)。"""
    for _ in range(tries):
        t = random_tree(n, rnd)
        es = random_orientation(t, rnd)
        sk = sinks(n, es)
        if len(sk) >= 2:
            return es, sk
    raise RuntimeError("N=%d 未能构造出多 sink 的随机定向" % n)


# --------------------------------------------------------------------------
# 10 个测试点的构造：返回 (n, edges, 该点的分层说明)
# --------------------------------------------------------------------------
def build_point(i):
    rnd = random.Random(2126000 + i)  # 每点独立固定种子，数据可复现

    # ---- 点 1：边界层 · N=1（全最小规模 / 退化无通道 / 答案 1 的极端）----
    if i == 1:
        return (1, [], "边界层：N=1 全最小规模，0 条通道 → 答案 1（答案 1 的极端）")

    # ---- 点 2：边界层 · N=2（最小非平凡规模；唯一 sink 且为最大编号）----
    if i == 2:
        return (2, [(2, 1)], "边界层：N=2，唯一通道 2->1 → 答案 1（最小规模有解，sink=最大编号）")

    # ---- 点 3：小规模 · 题面【输入样例】原样（题面声明的特殊值）----
    if i == 3:
        return (3, [(1, 2), (3, 2)], "小规模：题面【输入样例】原样 3 / 1 2 / 3 2 → 答案 2")

    # ---- 点 4：小规模随机 · 无解（sink >= 2）----
    if i == 4:
        n = rnd.randint(5, 9)
        es, sk = randomised_tree_no_solution(n, rnd)
        return (n, es, "小规模随机：随机树随机定向（sink=%s，共 %d 个）→ 答案 -1，可人工展开验证" %
                (sk, len(sk)))

    # ---- 点 5：中等规模随机 · 有解（全部朝随机根，根 != 1）----
    if i == 5:
        n = 30
        t = random_tree(n, rnd)
        root = rnd.randint(2, n)          # 根 != 1，答案不是最小值 1
        es = orient_toward_root(n, t, root)
        return (n, es, "中等规模随机：N=30 随机树全部朝根（根=%d）→ 答案 %d（有解·唯一 sink）" %
                (root, root))

    # ---- 点 6：中等规模随机 · 无解 ----
    if i == 6:
        n = 45
        es, sk = randomised_tree_no_solution(n, rnd)
        return (n, es, "中等规模随机：N=45 随机树随机定向（%d 个 sink）→ 答案 -1" % len(sk))

    # ---- 点 7：大规模 · 星形指向中心 1（答案 1 的极端，最大度数）----
    if i == 7:
        n = 80
        es = star_to_center(n, 1)
        return (n, es, "大规模：N=80 星形全部指向中心 1（最大度数 79）→ 答案 1（有解·答案 1 极端）")

    # ---- 点 8：大规模 · 有序链，答案 = 最大编号 N ----
    if i == 8:
        n = 90
        es = chain_up(n)
        return (n, es, "大规模：N=90 有序链 1->2->...->90 → 答案 90（有解·DFS 路径最深 89 层）")

    # ---- 点 9：顶格层 · N=100 有序链，答案 = 100 ----
    if i == 9:
        n = MAXN
        es = chain_up(n)
        return (n, es, "顶格层：N=100 链 1->2->...->100 → 答案 100（标程需枚举 1..99 全失败）")

    # ---- 点 10：顶格层 · N=100 随机树随机定向（无解，标程全枚举最坏）----
    if i == 10:
        n = MAXN
        es, sk = randomised_tree_no_solution(n, rnd)
        return (n, es, "顶格层：N=100 随机树随机定向（%d 个 sink）→ 答案 -1（100 个 i 全失败，工作量最大）" % len(sk))

    raise ValueError("未知测试点编号：%d" % i)


# --------------------------------------------------------------------------
# 生成 + 生成后自检
# --------------------------------------------------------------------------
def find_data_dir():
    """数据落在当前工作目录（约定在 data/ 下运行 data.py）；否则退回脚本旁的 data/。"""
    if os.path.exists(os.path.join(os.getcwd(), "problem1.in")):
        return os.getcwd()
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def main():
    expected = {}
    for i in range(1, 11):
        n, edges, note = build_point(i)
        # 生成前先做结构断言：题面保证「N-1 条边连通无环」=> 必须是树
        ok, why = is_tree(n, edges)
        assert ok, "点 %d：生成的数据不是题面保证的树结构（%s）" % (i, why)
        assert 1 <= n <= MAXN, "点 %d：N=%d 超出题面上限" % (i, n)

        io = IO(file_prefix="problem", data_id=i)  # problem<i>.in / problem<i>.out
        io.input_write(n, "\n")
        for (u, v) in edges:
            io.input_write(u, v, "\n")
        io.output_gen("../std")  # 用标程生成答案
        io.close()               # 显式关闭，确保 .in/.out 落盘后自检才能读到完整内容
        expected[i] = (n, edges, note)

    data_dir = find_data_dir()
    problems = []

    def check(cond, msg):
        if not cond:
            problems.append(msg)

    print("点  层             N    边数  答案   结构特征")
    for i in range(1, 11):
        n, edges, note = expected[i]
        in_path = os.path.join(data_dir, "problem%d.in" % i)
        out_path = os.path.join(data_dir, "problem%d.out" % i)
        raw_in = open(in_path, "r", encoding="utf-8", newline="").read()
        raw_out = open(out_path, "r", encoding="utf-8", newline="").read()

        # (1) 输入格式：首行 N，随后恰 N-1 行「a b」，末尾有换行
        lines = raw_in.split("\n")
        check(lines[-1] == "", "点 %d：.in 末尾缺少换行" % i)
        lines = lines[:-1] if lines and lines[-1] == "" else lines
        check(lines[0].strip() == str(n), "点 %d：首行 %r 应为 %d" % (i, lines[0], n))
        check(len(lines) - 1 == max(0, n - 1),
              "点 %d：边行数 %d 应为 N-1=%d" % (i, len(lines) - 1, max(0, n - 1)))
        parsed = []
        for ln in lines[1:]:
            parts = ln.split()
            check(len(parts) == 2 and all(p.lstrip("-").isdigit() for p in parts),
                  "点 %d：边行 %r 格式非法（应为两个整数）" % (i, ln))
            if len(parts) == 2:
                parsed.append((int(parts[0]), int(parts[1])))
        check(parsed == edges, "点 %d：读回的边与构造不一致" % i)
        ok, why = is_tree(n, parsed)
        check(ok, "点 %d：读回的数据不是树（%s）" % (i, why))

        # (2) 独立参考实现复算答案，与 std 产出的 .out 逐字节比对
        want = "%d\n" % ref_answer(n, parsed)
        check(raw_out == want, "点 %d：std 输出 %r != 独立参考实现 %r" % (i, raw_out, want))

        sk = sinks(n, parsed)
        print("%2d  %-14s %3d  %4d  %-5s  %s" %
              (i, note.split("：")[0], n, len(parsed), raw_out.strip(), note.split("：", 1)[1]))

    # (3) 分层结构性断言
    check(expected[1][0] == 1 and expected[1][1] == [], "点 1 应为 N=1 无通道")
    check(expected[2][1] == [(2, 1)] and ref_answer(2, [(2, 1)]) == 1, "点 2 应为 2->1 且答案 1")
    check(expected[3][1] == [(1, 2), (3, 2)] and ref_answer(3, [(1, 2), (3, 2)]) == 2,
          "点 3 应为题面样例原样（答案 2）")
    check(5 <= expected[4][0] <= 9 and ref_answer(*expected[4][:2]) == -1,
          "点 4 应为小规模（5..9）且无解")
    check(len(sinks(4, expected[4][1])) >= 2, "点 4 应至少有 2 个 sink")
    check(expected[5][0] == 30 and ref_answer(*expected[5][:2]) != -1, "点 5 应为 N=30 有解")
    check(expected[6][0] == 45 and ref_answer(*expected[6][:2]) == -1, "点 6 应为 N=45 无解")
    check(expected[7][0] == 80 and ref_answer(*expected[7][:2]) == 1, "点 7 应为 N=80 星形且答案 1")
    check(len(sinks(80, expected[7][1])) == 1 and sinks(80, expected[7][1])[0] == 1,
          "点 7 应只有 sink=1")
    check(expected[8][1] == chain_up(90) and ref_answer(90, chain_up(90)) == 90,
          "点 8 应为 N=90 有序链且答案 90")
    check(expected[9][1] == chain_up(100) and ref_answer(100, chain_up(100)) == 100,
          "点 9 应为 N=100 链且答案 100")
    check(expected[10][0] == MAXN and ref_answer(*expected[10][:2]) == -1,
          "点 10 应为 N=100 无解（顶格）")
    check(max(expected[i][0] for i in range(1, 11)) == MAXN, "缺少 N=100 的顶格测试点")

    if problems:
        print("\n自检失败：", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        raise SystemExit(1)
    print("\n自检全部通过：10/10 组 .in/.out 成对；格式/树性/分层特征/独立参考实现复算均一致。")


if __name__ == "__main__":
    main()
