#!/usr/bin/env python3
# 一本通 1765《树上斐波那契》 分层数据生成器
# ---------------------------------------------------------------------------
# 数据范围: n,m <= 1e5, 1 <= X,Y <= n, 1 <= k <= 1e15 (k 上限 1e15);
#           30% 数据 n,m<=1000, k<=100; 另外 30% 数据父亲在编号更小的点中随机产生。
# 分层设计:
#   点 1  边界层: n=1 (无父亲行), 单点更新/查询, 含 k=1 与 k=1e15
#   点 2  边界层: n=2 链, 小 k, 子树/路径退化为链
#   点 3  小规模随机: n=10, m=20
#   点 4  小规模(30%档): n=100, m=100, k<=100
#   点 5  30%档边界: n=1000, m=1000, k<=100
#   点 6  第二档: n=1000, m=1000, 随机父亲(编号更小), k<=1e15
#   点 7  大规模随机树: n=m=1e5, 随机父亲, k<=1e15
#   点 8  大规模链(最深深树): n=m=1e5, 含深点小 k(触发负下标 Fib(K), K<0)
#   点 9  大规模菊花: n=m=1e5, 深度浅, k 顶格 1e15
#   点 10 顶格混合: n=m=1e5, 毛毛虫结构, 先批量更新再批量查询, k 顶格
#
# .out 一律用 subprocess 显式调用 std 生成 (避免 cyaron 写缓冲未 flush 导致 0 字节),
# 并断言 .out 非空且行数 == 询问数, 每行取值合法。
# ---------------------------------------------------------------------------
import os
import random
import subprocess
import sys

from cyaron import IO

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "work", "std")
MOD = 10 ** 9 + 7
KMAX = 10 ** 15


def build_fathers(n, shape, rnd):
    """返回 fa[2..n] 列表 (fa[i] 为节点 i 的父亲)。所有形状保证 fa[i] < i, 根为 1。"""
    fa = [0] * (n + 1)
    if shape == "chain":
        for i in range(2, n + 1):
            fa[i] = i - 1
    elif shape == "star":
        for i in range(2, n + 1):
            fa[i] = 1
    elif shape == "binary":
        for i in range(2, n + 1):
            fa[i] = i // 2
    elif shape == "random":
        for i in range(2, n + 1):
            fa[i] = rnd.randint(1, i - 1)
    elif shape == "caterpillar":
        # 主链 1..spine, 其余点作为主链上点的叶子
        spine = max(1, n // 2)
        for i in range(2, spine + 1):
            fa[i] = i - 1
        nxt = spine + 1
        v = 1
        while nxt <= n:
            fa[nxt] = v
            nxt += 1
            v = v % spine + 1
    else:
        raise ValueError(shape)
    return fa


def gen_ops(rnd, n, m, kmin, kmax, query_ratio, small_k_at_deep=False):
    """生成 m 条操作 (字符串列表)。保证至少 1 次询问与 1 次更新。"""
    ops = []
    for _ in range(m):
        if rnd.random() < query_ratio:
            x = rnd.randint(1, n)
            y = rnd.randint(1, n)
            if rnd.random() < 0.3:
                y = x
            ops.append("Q %d %d" % (x, y))
        else:
            x = rnd.randint(1, n)
            r = rnd.random()
            if small_k_at_deep and r < 0.5:
                k = rnd.randint(1, 100)          # 深点小 k => K = k - dep[x] 可能为负
            elif r < 0.1:
                k = kmin
            elif r < 0.2:
                k = kmax
            else:
                k = rnd.randint(kmin, kmax)
            ops.append("U %d %d" % (x, k))
    # 强制至少一个 Q 与一个 U
    if not any(o[0] == "Q" for o in ops):
        ops[0] = "Q 1 %d" % n
    if not any(o[0] == "U" for o in ops):
        ops[1] = "U 1 %d" % kmin
    return ops


def gen(data_id, n, m, shape, kmin, kmax, seed, query_ratio=0.5,
        small_k_at_deep=False, ops=None, quiet=True):
    rnd = random.Random(seed)
    fa = build_fathers(n, shape, rnd)
    if ops is None:
        ops = gen_ops(rnd, n, m, kmin, kmax, query_ratio, small_k_at_deep)
    assert len(ops) == m

    # ---- 组装 .in 文本 ----
    parts = ["%d %d" % (n, m)]
    for i in range(2, n + 1):
        parts.append(str(fa[i]))
    parts.extend(ops)
    text = "\n".join(parts) + "\n"

    io = IO(file_prefix="problem", data_id=data_id)
    io.input_write(text)
    io.close()

    in_path = "problem%d.in" % data_id
    out_path = "problem%d.out" % data_id

    # ---- 用 subprocess 显式跑 std 生成 .out ----
    with open(in_path, "rb") as f:
        inp = f.read()
    res = subprocess.run([STD], input=inp, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, timeout=110)
    if res.returncode != 0:
        raise RuntimeError("std failed on case %d: rc=%d err=%s"
                           % (data_id, res.returncode, res.stderr[:300]))
    out = res.stdout

    nq = sum(1 for o in ops if o[0] == "Q")
    # ---- 断言 .out 非空且行数 == 询问数 (无解空输出点除外: 本文件每点均有询问) ----
    assert nq > 0, "case %d 无询问" % data_id
    assert len(out) > 0, "case %d .out 为空!" % data_id
    lines = out.decode().split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    assert len(lines) == nq, ("case %d 行数 %d != 询问数 %d"
                              % (data_id, len(lines), nq))
    for ln in lines:
        v = int(ln)
        assert 0 <= v < MOD, "case %d 非法答案 %s" % (data_id, ln)

    with open(out_path, "wb") as f:
        f.write(out)

    if not quiet:
        print("case %d: n=%d m=%d shape=%s queries=%d bytes=%d"
              % (data_id, n, m, shape, nq, len(out)))
    return in_path, out_path, len(lines)


def main():
    if not os.path.exists(STD):
        print("std 不存在, 请先编译: g++ -O2 -std=c++17 -o work/std std.cpp",
              file=sys.stderr)
        sys.exit(1)

    # 点 1: 边界 n=1 (无父亲行), 单点更新/查询, 含 k=1 与 k=1e15
    gen(1, 1, 6, "star", 1, KMAX, seed=101, query_ratio=0.4,
        ops=["U 1 1", "Q 1 1", "U 1 %d" % KMAX, "Q 1 1", "Q 1 1", "U 1 2"])

    # 点 2: 边界 n=2 链
    gen(2, 2, 8, "chain", 1, 100, seed=102, query_ratio=0.5)

    # 点 3: 小规模随机
    gen(3, 10, 20, "random", 1, 100, seed=103, query_ratio=0.5)

    # 点 4: 30% 档 n=100, m=100, k<=100
    gen(4, 100, 100, "random", 1, 100, seed=104, query_ratio=0.5)

    # 点 5: 30% 档边界 n=m=1000, k<=100
    gen(5, 1000, 1000, "random", 1, 100, seed=105, query_ratio=0.5)

    # 点 6: 第二档 n=m=1000, 随机父亲, k<=1e15
    gen(6, 1000, 1000, "random", 1, KMAX, seed=106, query_ratio=0.5)

    # 点 7: 大规模随机树 n=m=1e5
    gen(7, 100000, 100000, "random", 1, KMAX, seed=107, query_ratio=0.5)

    # 点 8: 大规模链, 含深点小 k (K<0 触发负下标 Fib)
    gen(8, 100000, 100000, "chain", 1, KMAX, seed=108, query_ratio=0.45,
        small_k_at_deep=True)

    # 点 9: 大规模菊花 (深度浅), k 顶格
    gen(9, 100000, 100000, "star", KMAX, KMAX, seed=109, query_ratio=0.5)

    # 点 10: 顶格混合, 毛毛虫, 先批量更新再批量查询
    rnd = random.Random(110)
    ops10 = []
    for i in range(50000):
        ops10.append("U %d %d" % (rnd.randint(1, 100000), rnd.randint(1, KMAX)))
    for i in range(50000):
        ops10.append("Q %d %d" % (rnd.randint(1, 100000), rnd.randint(1, 100000)))
    gen(10, 100000, 100000, "caterpillar", 1, KMAX, seed=110, ops=ops10)

    print("data.py: 10 组数据生成完成")


if __name__ == "__main__":
    main()
