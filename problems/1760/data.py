#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 一本通 1760《树上数颜色》 数据生成器
#
# 输出 problem1.in/.out ... problem10.in/.out，共 10 组，按规模分层：
#   1-2   边界层（n=1 / n=2，含强制在线 t=1）
#   3-4   小规模随机（n=50 / n=500，链 + t=1）
#   5-6   中等规模随机（n=3000 随机树 / n=20000 链）
#   7-8   大规模（n=50000 随机树 / n=100000 链 + 最坏询问）
#   9-10  顶格（n=q=100000：星形大量修改 / 随机树强制在线）
#
# 注意：题目 t=1 时需对除操作类型外的数异或上一次询问答案 lastans。
# 生成器先用“明文”操作写成 t=0 输入，跑 std 得到答案（即 lastans 序列），
# 再据此异或编码成最终 t=1 输入；最终 .out 就是这些答案。
# 生成过程全部 O(n+q)，无 O(n^2) 循环。
import os
import random
import subprocess
import sys

random.seed(20260101)

BASE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(BASE, "std")
DATA = os.path.join(BASE, "data")


# ---------------------------------------------------------------------------
# 基础构造
# ---------------------------------------------------------------------------
def rand_tree(n, style="random"):
    """返回 n-1 条边（节点编号 1..n）。"""
    edges = []
    if style == "chain":
        for i in range(2, n + 1):
            edges.append((i - 1, i))
    elif style == "star":
        for i in range(2, n + 1):
            edges.append((1, i))
    else:  # random
        for i in range(2, n + 1):
            edges.append((random.randint(1, i - 1), i))
    return edges


def gen_ops(n, q, mode, colors=None):
    """生成明文操作列表。每个元素为 tuple：('Q',u,l,r) 或 ('M',u,c)。"""
    ops = []
    for _ in range(q):
        if mode == "allq_root":          # 全是根节点、全颜色区间（最坏询问）
            ops.append(("Q", 1, 1, n))
        elif mode == "allm":             # 全是修改
            ops.append(("M", random.randint(1, n), random.randint(1, n)))
        elif mode == "q":                # 全询问
            u = random.randint(1, n)
            l = random.randint(1, n)
            r = random.randint(l, n)
            ops.append(("Q", u, l, r))
        elif mode == "m":                # 全修改
            ops.append(("M", random.randint(1, n), random.randint(1, n)))
        else:                            # 混合
            if random.random() < 0.5:
                u = random.randint(1, n)
                l = random.randint(1, n)
                r = random.randint(l, n)
                ops.append(("Q", u, l, r))
            else:
                ops.append(("M", random.randint(1, n), random.randint(1, n)))
    # 保证至少有一个询问，使 .out 非空
    if not any(o[0] == "Q" for o in ops):
        u = random.randint(1, n)
        l = random.randint(1, n)
        r = random.randint(l, n)
        ops[-1] = ("Q", u, l, r)
    return ops


def plain_lines(n, t, colors, edges, ops):
    out = ["%d %d %d" % (n, len(ops), t)]
    out.append(" ".join(map(str, colors)))
    for u, v in edges:
        out.append("%d %d" % (u, v))
    for o in ops:
        if o[0] == "Q":
            out.append("1 %d %d %d" % (o[1], o[2], o[3]))
        else:
            out.append("2 %d %d" % (o[1], o[2]))
    return out


def run_std(in_path):
    """跑 std，返回 (answers 列表, 行数)。"""
    with open(in_path, "rb") as fi:
        res = subprocess.run([STD], stdin=fi, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, timeout=120)
    if res.returncode != 0:
        raise RuntimeError("std failed on %s: %s" % (in_path, res.stderr.decode()[:500]))
    txt = res.stdout.decode().split()
    return [int(x) for x in txt]


def emit(data_id, n, t, colors, edges, ops):
    """写出 problem{id}.in/.out；t=1 时先跑明文再异或编码。"""
    nq = sum(1 for o in ops if o[0] == "Q")
    assert nq >= 1, "test %d 无询问" % data_id
    plain = plain_lines(n, 0, colors, edges, ops)
    tmp_in = os.path.join(DATA, "_plain%d.in" % data_id)
    with open(tmp_in, "w") as f:
        f.write("\n".join(plain) + "\n")
    answers = run_std(tmp_in)
    assert len(answers) == nq, "test %d 答案行数 %d != 询问数 %d" % (data_id, len(answers), nq)
    os.remove(tmp_in)

    if t == 0:
        lines = plain
        lines[0] = "%d %d 0" % (n, len(ops))
    else:
        lines = ["%d %d 1" % (n, len(ops)), " ".join(map(str, colors))]
        for u, v in edges:
            lines.append("%d %d" % (u, v))
        last = 0
        ai = 0
        for o in ops:
            if o[0] == "Q":
                lines.append("1 %d %d %d" % (o[1] ^ last, o[2] ^ last, o[3] ^ last))
                last = answers[ai]
                ai += 1
            else:
                lines.append("2 %d %d" % (o[1] ^ last, o[2] ^ last))

    in_path = os.path.join(DATA, "problem%d.in" % data_id)
    out_path = os.path.join(DATA, "problem%d.out" % data_id)
    with open(in_path, "w") as f:
        f.write("\n".join(lines) + "\n")

    # 用最终 .in 再跑一遍 std，直接产出 .out（顺带验证 t=1 编码自洽）
    final_ans = run_std(in_path)
    assert len(final_ans) == nq, "test %d 最终输出行数异常" % data_id
    if t == 1:
        assert final_ans == answers, "test %d t=1 编码解码不自洽" % data_id
    with open(out_path, "w") as f:
        f.write("\n".join(map(str, final_ans)) + "\n")

    assert os.path.getsize(out_path) > 0, "test %d .out 为空" % data_id
    print("problem%d: n=%d q=%d t=%d queries=%d maxans=%d"
          % (data_id, n, len(ops), t, nq, max(final_ans)))


def main():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(STD):
        print("std 未编译，请先: g++ -O2 -std=c++17 std.cpp -o std", file=sys.stderr)
        sys.exit(1)

    # 1. 边界：n=1，单点
    n, q = 1, 3
    emit(1, n, 0, [1], [], [("Q", 1, 1, 1), ("M", 1, 1), ("Q", 1, 1, 1)])

    # 2. 边界：n=2，t=1 强制在线小例（同色 / 全区间 / 单点修改）
    n, q = 2, 6
    colors = [1, 2]
    edges = [(1, 2)]
    ops = [("Q", 1, 1, 2), ("M", 2, 1), ("Q", 1, 1, 1),
           ("Q", 2, 1, 2), ("M", 1, 2), ("Q", 1, 1, 2)]
    emit(2, n, 1, colors, edges, ops)

    # 3. 小规模随机树 + 全同色 + 无修改（答案只可能为 0 或 1）
    n, q = 50, 200
    colors = [3] * n
    edges = rand_tree(n, "random")
    emit(3, n, 0, colors, edges, gen_ops(n, q, "q"))

    # 4. 小规模链 + t=1 强制在线
    n, q = 500, 1000
    colors = [random.randint(1, n) for _ in range(n)]
    edges = rand_tree(n, "chain")
    emit(4, n, 1, colors, edges, gen_ops(n, q, "mix"))

    # 5. 中等规模随机树
    n, q = 3000, 3000
    colors = [random.randint(1, n) for _ in range(n)]
    edges = rand_tree(n, "random")
    emit(5, n, 0, colors, edges, gen_ops(n, q, "mix"))

    # 6. 中等规模链（深子树，询问区间偏大）
    n, q = 20000, 20000
    colors = [random.randint(1, n) for _ in range(n)]
    edges = rand_tree(n, "chain")
    emit(6, n, 0, colors, edges, gen_ops(n, q, "mix"))

    # 7. 大规模随机树
    n, q = 50000, 50000
    colors = [random.randint(1, n) for _ in range(n)]
    edges = rand_tree(n, "random")
    emit(7, n, 0, colors, edges, gen_ops(n, q, "mix"))

    # 8. 大规模链，全部为“根 + 全颜色区间”最坏询问
    n, q = 100000, 100000
    colors = [random.randint(1, n) for _ in range(n)]
    edges = rand_tree(n, "chain")
    emit(8, n, 0, colors, edges, gen_ops(n, q, "allq_root"))

    # 9. 顶格：链 + 一半修改（深子树询问 + 大量修改重建，卡综合性能）
    n, q = 100000, 100000
    colors = [random.randint(1, n) for _ in range(n)]
    edges = rand_tree(n, "chain")
    emit(9, n, 0, colors, edges, gen_ops(n, q, "mix"))

    # 10. 顶格：随机树 + t=1 强制在线，全规模
    n, q = 100000, 100000
    colors = [random.randint(1, n) for _ in range(n)]
    edges = rand_tree(n, "random")
    emit(10, n, 1, colors, edges, gen_ops(n, q, "mix"))


if __name__ == "__main__":
    main()
