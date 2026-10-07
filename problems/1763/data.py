#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 一本通 1763《简单树》数据生成器
#
# 题意：n 个点的带权树，m 个询问 L R x —— 求编号在 [L,R] 内的所有点到点 x 的距离之和。
#       type=1 表示强制在线：输入的 L,R,x 都要异或 lastans = 上一次答案 mod n（初始 0）。
# 数据范围：1<=n,m<=60000，0<=type<=1，1<=a,b<=n，0<=c<=10^9。
#
# 分层设计（10 组，单测点；每组注释写明规模与意图）：
#   1  边界层：n=1（最小值），m=2，type=1 —— 单点树 + 强制在线分支，答案全 0
#   2  边界层：n=2，边权 10^9（最大值），type=0 —— 手算答案（0 / 10^9）并断言
#   3  小规模：题面样例 n=5,m=3（手算 27/15/12），type=0 —— 与【输出样例】逐字比对
#   4  小规模：n=200 链，m=1000，type=1 —— 强制在线 + 链形小例
#   5  小规模边界：n=300 星形，m=300，边权全 0 —— 极端权值，答案全 0
#   6  中等规模：n=5000 随机树，m=5000，type=0，边权随机 [0,10^9]
#   7  中等规模：n=20000 随机树，m=20000，type=1（强制在线）
#   8  大规模：n=50000 星形（度数顶格），m=50000，type=0
#   9  顶格层：n=60000 链（深度顶格），m=60000，边权全 10^9，询问取整区间
#              —— 答案最大（≈1.8e18），溢出压力 + 链形树剖结构
#   10 顶格层：n=60000 完全二叉树（树剖/主席树节点数最多的结构），m=60000，
#              type=1（强制在线），边权随机 [0,10^9] —— 峰值内存/时间点
#
# 说明：type=1 的输入需要「上一次答案」，因此先用明文（type=0）写出并跑 std 得到答案，
#       再按 lastans 异或编码成最终输入；最后用最终 .in 再跑一遍 std 得到 .out，
#       并断言「解码后的答案 == 明文答案」，保证在线编码自洽。
#       生成与校验全部 O(n+m)，无 O(n^2) 循环。
import os
import random
import subprocess
import sys

from cyaron import IO

BASE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(BASE, "std")
DATA = os.path.join(BASE, "data")

MAXN = 60000
MAXM = 60000
MAXC = 10 ** 9

random.seed(17630001)


# ---------------------------------------------------------------------------
# 造树 / 造询问（全部 O(n+m)）
# ---------------------------------------------------------------------------
def rand_tree(n, style="random", wlo=0, whi=MAXC):
    """返回 n-1 条边 (a,b,c)，节点编号 1..n。"""
    if style == "chain":
        edges = [(i - 1, i) for i in range(2, n + 1)]
    elif style == "star":
        edges = [(1, i) for i in range(2, n + 1)]
    elif style == "cbt":
        edges = [(i // 2, i) for i in range(2, n + 1)]
    else:
        edges = [(random.randint(1, i - 1), i) for i in range(2, n + 1)]
    return [(a, b, random.randint(wlo, whi)) for a, b in edges]


def q_random(n, m):
    out = []
    for _ in range(m):
        l = random.randint(1, n)
        r = random.randint(l, n)
        out.append((l, r, random.randint(1, n)))
    return out


def q_full(n, m):
    """全区间 [1,n] 的询问：答案最大（顶格层用）。"""
    return [(1, n, random.randint(1, n)) for _ in range(m)]


# ---------------------------------------------------------------------------
# 落盘 + 校验
# ---------------------------------------------------------------------------
def run_std(in_path):
    """用 std 跑出答案（显式 subprocess，避免 cyaron 输出缓冲问题）。"""
    with open(in_path, "rb") as fi:
        res = subprocess.run(["nice", "-n", "19", STD], stdin=fi,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             timeout=120)
    if res.returncode != 0:
        raise RuntimeError("std 在 %s 上失败: %s" % (in_path, res.stderr.decode()[:400]))
    return [int(x) for x in res.stdout.split()]


def plain_lines(n, edges, queries):
    out = ["%d %d 0" % (n, len(queries))]
    for a, b, c in edges:
        out.append("%d %d %d" % (a, b, c))
    for l, r, x in queries:
        out.append("%d %d %d" % (l, r, x))
    return out


def emit(data_id, n, type_flag, edges, queries, note="", expect=None):
    """生成 problem{id}.in/.out，并做多重断言。"""
    m = len(queries)
    assert 1 <= n <= MAXN, "n=%d 超上限" % n
    assert 1 <= m <= MAXM, "m=%d 超上限" % m
    assert len(edges) == n - 1, "边数 %d != n-1" % len(edges)
    for a, b, c in edges:
        assert 1 <= a <= n and 1 <= b <= n and a != b, "非法边 (%d,%d)" % (a, b)
        assert 0 <= c <= MAXC, "边权越界 %d" % c
    for l, r, x in queries:
        assert 1 <= l <= r <= n and 1 <= x <= n, "非法询问 (%d,%d,%d)" % (l, r, x)

    os.makedirs(DATA, exist_ok=True)
    in_path = os.path.join(DATA, "problem%d.in" % data_id)
    out_path = os.path.join(DATA, "problem%d.out" % data_id)

    # 1) 明文（type=0）跑一遍 std，拿到真实答案序列
    plain = plain_lines(n, edges, queries)
    tmp_plain = os.path.join(DATA, "_plain%d.in" % data_id)
    with open(tmp_plain, "w") as f:
        f.write("\n".join(plain) + "\n")
    answers = run_std(tmp_plain)
    assert len(answers) == m, "明文答案行数 %d != m=%d" % (len(answers), m)
    if expect is not None:
        assert answers == list(expect), "与手算/公式预期不符:\n%s\n%s" % (answers[:10], list(expect)[:10])
    os.remove(tmp_plain)

    # 2) type=1 时按 lastans 异或编码
    if type_flag == 0:
        lines = plain
    else:
        lines = ["%d %d 1" % (n, m)]
        for a, b, c in edges:
            lines.append("%d %d %d" % (a, b, c))
        last = 0
        for (l, r, x), ans in zip(queries, answers):
            lines.append("%d %d %d" % (l ^ last, r ^ last, x ^ last))
            last = ans % n

    # 3) 用 cyaron 的 IO（仓库惯例接口）写出最终 .in，再跑 std 产出 .out，
    #    并校验行数 / 非空 / 在线编码自洽
    io = IO(file_prefix="problem", data_id=data_id)
    io.input_write("\n".join(lines) + "\n")
    io.close()

    final = run_std(in_path)
    assert len(final) == m, "最终答案行数 %d != m=%d" % (len(final), m)
    if type_flag == 1:
        assert final == answers, "type=1 编码解码不自洽"
    with open(out_path, "w") as f:
        f.write("\n".join(map(str, final)) + "\n")

    assert os.path.getsize(out_path) > 0, "problem%d.out 为空" % data_id
    with open(in_path) as f:
        nlines = sum(1 for _ in f)
    assert nlines == 1 + (n - 1) + m, "problem%d.in 行数 %d 异常" % (data_id, nlines)

    print("problem%-2d n=%-6d m=%-6d type=%d %-28s maxans=%d"
          % (data_id, n, m, type_flag, note, max(final)))


def main():
    if not os.path.exists(STD):
        print("std 未编译，请先: g++ -O2 -std=c++17 std.cpp -o std", file=sys.stderr)
        sys.exit(1)
    os.makedirs(DATA, exist_ok=True)
    os.chdir(DATA)          # 使 cyaron 的 IO(file_prefix="problem") 落在 data/ 下

    # 1. 边界：n=1（最小值），type=1，答案恒 0
    emit(1, 1, 1, [], [(1, 1, 1), (1, 1, 1)], "n=1 单点+在线", expect=[0, 0])

    # 2. 边界：n=2，边权 10^9（最大值），手算断言
    e2 = [(1, 2, MAXC)]
    q2 = [(1, 2, 1), (1, 1, 1), (2, 2, 2), (1, 2, 2), (2, 2, 1), (1, 1, 2)]
    #     (1,2,1)=1e9, (1,1,1)=0, (2,2,2)=0, (1,2,2)=1e9, (2,2,1)=1e9, (1,1,2)=dist(1,2)=1e9
    emit(2, 2, 0, e2, q2, "n=2 最大边权", expect=[MAXC, 0, 0, MAXC, MAXC, MAXC])

    # 3. 小规模：题面样例（手算 27/15/12）
    e3 = [(1, 2, 3), (1, 3, 3), (2, 4, 3), (2, 5, 3)]
    q3 = [(1, 5, 3), (1, 5, 2), (2, 3, 4)]
    emit(3, 5, 0, e3, q3, "题面样例", expect=[27, 15, 12])

    # 4. 小规模：n=200 链，type=1 强制在线
    emit(4, 200, 1, rand_tree(200, "chain"), q_random(200, 1000), "n=200 链+在线")

    # 5. 小规模边界：n=300 星形，边权全 0（答案恒 0）
    e5 = [(1, i, 0) for i in range(2, 301)]
    q5 = q_random(300, 300)
    emit(5, 300, 0, e5, q5, "n=300 星形 权值全0", expect=[0] * 300)

    # 6. 中等规模：n=5000 随机树
    emit(6, 5000, 0, rand_tree(5000, "random"), q_random(5000, 5000), "n=5000 随机树")

    # 7. 中等规模：n=20000 随机树，type=1
    emit(7, 20000, 1, rand_tree(20000, "random"), q_random(20000, 20000), "n=20000 随机树+在线")

    # 8. 大规模：n=50000 星形（度数顶格）
    emit(8, 50000, 0, rand_tree(50000, "star"), q_random(50000, 50000), "n=50000 星形")

    # 9. 顶格层：n=60000 链 + 边权全 10^9 + 整区间询问
    #    答案闭式：10^9 * Σ_{i=1}^{n} |i-x|，用公式断言（不依赖任何暴力）
    n9, m9 = MAXN, MAXM
    e9 = [(i - 1, i, MAXC) for i in range(2, n9 + 1)]
    q9 = q_full(n9, m9)
    exp9 = [MAXC * ((x - 1) * x // 2 + (n9 - x) * (n9 - x + 1) // 2) for _, _, x in q9]
    emit(9, n9, 0, e9, q9, "n=60000 链 权值1e9 整区间", expect=exp9)

    # 10. 顶格层：n=60000 完全二叉树，type=1，边权随机
    emit(10, MAXN, 1, rand_tree(MAXN, "cbt"), q_random(MAXN, MAXM), "n=60000 完全二叉树+在线")


if __name__ == "__main__":
    main()
