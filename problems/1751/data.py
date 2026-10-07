#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
一本通 1751《字符串排序》测试数据生成器（目标 ROJ 题号 1751）。

题意（见 content.md / 官方题面）：
    给定长度为 n 的小写字母串 S，有 m 次操作，每次给定 l, r, x：
        x=1 -> 把 S[l..r] 升序排序；x=0 -> 把 S[l..r] 降序排序。
    求最终字符串。
    ★ 参数顺序：题面正文写“每行三个整数 x,l,r”，但【输入样例】`1 3 1 / 3 5 0`
      只有按 `l r x` 解释才能得到样例输出 `abdcc`（l=1,r=3,升序 → "cab"→"abc"；
      l=3,r=5,降序 → "ccd"→"dcc"），故 **以样例为准，输入顺序为 l r x**。

数据范围（题面【数据规模】）：
    40%  n, m <= 1000
    100% n, m <= 100000
    S 只含小写字母；1 <= l <= r <= n；x ∈ {0,1}。

10 个测试点分层（从最小铺到顶格）：

  点  层        n       m        字母表   设计意图
  --  --------  ------  --------  -------  ---------------------------------------------
  1   边界      1       1         1 种     n=m=1 最小规模（区间退化到单点）
  2   边界      5       2         4 种     题面【输入样例】原样 -> abdcc（可手算核对）
  3   边界      2       4         2 种     n=2 极小；升/降序 + 单点区间交替
  4   小        10      10        26 种    小规模随机，可手算验证
  5   小        100     100       26 种    小规模随机
  6   中        1000    1000      26 种    40% 档上限
  7   中        10000   10000     26 种    中间档
  8   大        50000   50000     26 种    接近上限
  9   顶格      100000  100000    2 种     顶格 + 字母表极小（每段计数大，最坏“多重复”结构）
  10  顶格      100000  100000    26 种    顶格 + 含大量整串排序（最坏区间长度）

  * 点 9 用 2 种字母：任意区间内几乎所有字符都相同，cnt 统计后各段很长，
    覆盖段数虽少但单段极长，考验区间覆盖的下传/回收。
  * 点 10 用 26 种字母 + 大量 l=1,r=n 的整串排序：每次操作覆盖段数最多（<=26），
    是 std 单次操作代价的最大化结构。

生成方式：
    - 纯 Python 写 .in（不依赖 cyaron 的 output_gen，规避其“std 缺失时静默产出
      0 字节 .out”的隐患）：先断言 std 可执行文件存在，再用 subprocess 跑 std 产出 .out，
      并对每个 .out 断言非空、长度 == n、字符多重集合与输入 S 一致（排序不改变字符计数）。
    - 每个点用独立随机种子 random.Random(1751 + 点号)，与调用顺序无关，逐字节可复现。
"""

import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
STD = os.path.join(HERE, "std")          # 标程可执行文件（由 std.cpp 编译而来）
ALPHA = "abcdefghijklmnopqrstuvwxyz"

NMAX = 100000                            # 题面 n,m 上限
MMAX = 100000

SAMPLE_S = "cabcd"
SAMPLE_OPS = [(1, 3, 1), (3, 5, 0)]
SAMPLE_OUT = "abdcc"


def rand_ops(rng, n, m, alpha, full_range_ratio=0.0):
    """生成 m 个合法操作 (l, r, x)，保证 1<=l<=r<=n, x∈{0,1}。

    以 full_range_ratio 的概率产生整串区间 (l=1, r=n)，其余为随机区间。
    """
    ops = []
    for _ in range(m):
        if rng.random() < full_range_ratio:
            l, r = 1, n
        else:
            a = rng.randint(1, n)
            b = rng.randint(1, n)
            l, r = (a, b) if a <= b else (b, a)
        ops.append((l, r, rng.randint(0, 1)))
    return ops


def rand_string(rng, n, alpha):
    return "".join(rng.choice(alpha) for _ in range(n))


def build_point(i):
    """返回 (S, ops, note)。每个点独立种子，可精确复现。"""
    rng = random.Random(1751 + i)

    if i == 1:                                   # 边界：最小规模
        return "a", [(1, 1, 1)], "边界层：n=m=1 最小规模（区间退化为单点）"

    if i == 2:                                   # 边界：题面样例
        return SAMPLE_S, list(SAMPLE_OPS), "边界层：题面【输入样例】原样（期望 abdcc，可手算）"

    if i == 3:                                   # 边界：n=2 极小 + 两方向/单点
        ops = [(1, 2, 1), (1, 2, 0), (1, 1, 1), (2, 2, 0)]
        return "ba", ops, "边界层：n=2 极小，升/降序 + 单点区间交替"

    if i == 4:                                   # 小规模随机
        n, m = 10, 10
        return (rand_string(rng, n, ALPHA), rand_ops(rng, n, m, ALPHA),
                "小规模随机：n=m=10，26 字母（可手算）")

    if i == 5:                                   # 小规模随机
        n, m = 100, 100
        return (rand_string(rng, n, ALPHA), rand_ops(rng, n, m, ALPHA),
                "小规模随机：n=m=100，26 字母")

    if i == 6:                                   # 中规模（40% 档上限）
        n, m = 1000, 1000
        return (rand_string(rng, n, ALPHA), rand_ops(rng, n, m, ALPHA),
                "中规模随机：n=m=1000（题面 40% 档上限）")

    if i == 7:                                   # 中规模
        n, m = 10000, 10000
        return (rand_string(rng, n, ALPHA), rand_ops(rng, n, m, ALPHA),
                "中规模随机：n=m=10000，中间档")

    if i == 8:                                   # 大规模
        n, m = 50000, 50000
        return (rand_string(rng, n, ALPHA), rand_ops(rng, n, m, ALPHA),
                "大规模随机：n=m=50000，接近上限")

    if i == 9:                                   # 顶格 + 字母表极小
        n, m = NMAX, MMAX
        return (rand_string(rng, n, "ab"), rand_ops(rng, n, m, "ab"),
                "顶格层：n=m=1e5 + 仅 2 种字母（大量重复，覆盖段极长）")

    if i == 10:                                  # 顶格 + 大量整串排序
        n, m = NMAX, MMAX
        ops = rand_ops(rng, n, m, ALPHA, full_range_ratio=0.5)
        return (rand_string(rng, n, ALPHA), ops,
                "顶格层：n=m=1e5 + 50% 整串排序（每次操作覆盖段数最多）")

    raise ValueError("未知测试点编号：%d" % i)


def main():
    # ---- 前置：std 必须存在（否则 cyaron/手工产出 0 字节 .out 会静默通过） ----
    if not (os.path.isfile(STD) and os.access(STD, os.X_OK)):
        print("错误：找不到可执行的标程 %s，请先编译 std.cpp。" % STD, file=sys.stderr)
        raise SystemExit(2)

    os.makedirs(DATA_DIR, exist_ok=True)
    problems = []
    summary = []

    for i in range(1, 11):
        S, ops, note = build_point(i)
        n, m = len(S), len(ops)

        # ---- 结构自检（生成时即校验合法性） ----
        assert set(S) <= set(ALPHA), "点 %d：S 含非小写字母" % i
        assert 1 <= n <= NMAX, "点 %d：n=%d 越界" % (i, n)
        assert 1 <= m <= MMAX, "点 %d：m=%d 越界" % (i, m)
        for (l, r, x) in ops:
            assert 1 <= l <= r <= n, "点 %d：非法区间 (%d,%d)" % (i, l, r)
            assert x in (0, 1), "点 %d：非法 x=%r" % (i, x)

        # ---- 写 .in ----
        in_path = os.path.join(DATA_DIR, "problem%d.in" % i)
        with open(in_path, "w", encoding="utf-8") as f:
            f.write("%d %d\n" % (n, m))
            f.write(S + "\n")
            f.write("".join("%d %d %d\n" % op for op in ops))
            f.flush()
            os.fsync(f.fileno())

        # ---- 跑 std 产出 .out ----
        with open(in_path, "rb") as fin:
            proc = subprocess.run([STD], stdin=fin, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, timeout=120)
        assert proc.returncode == 0, "点 %d：std 返回码 %d，stderr=%r" % (
            i, proc.returncode, proc.stderr[:200])
        out = proc.stdout.decode("utf-8")

        out_path = os.path.join(DATA_DIR, "problem%d.out" % i)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(out)
            f.flush()
            os.fsync(f.fileno())

        # ---- 生成后自检：.out 非空、行数/长度正确、字符多重集合守恒 ----
        body = out.strip("\n")
        assert out != "", "点 %d：.out 为空（std 缺失或崩溃）" % i
        assert out.count("\n") == 1 and out.endswith("\n"), \
            "点 %d：.out 应为「一行答案 + 换行」" % i
        assert len(body) == n, "点 %d：答案长度 %d != n=%d" % (i, len(body), n)
        assert set(body) <= set(ALPHA), "点 %d：答案含非小写字母" % i
        # 排序不改变字符多重集合 —— 无需暴力即可独立校验正确性
        assert sorted(body) == sorted(S), "点 %d：答案字符多重集合与输入 S 不一致" % i
        if i == 2:
            assert body == SAMPLE_OUT, "点 2：样例输出 %r != %r" % (body, SAMPLE_OUT)

        problems.append(i)
        summary.append((i, n, m, len(set(S)), note, body[:40] + ("..." if n > 40 else "")))

    # ---- 分层结构性断言 ----
    assert problems == list(range(1, 11)), "测试点不齐：%r" % problems
    print("%-3s %-7s %-7s %-6s %s" % ("点", "n", "m", "字母表", "设计意图"))
    for (i, n, m, ka, note, sample) in summary:
        print("%-3d %-7d %-7d %-6d %s" % (i, n, m, ka, note))
    print("\n自检全部通过：10/10 组 .in/.out 成对，.out 均非空、长度==n、字符多重集合守恒；"
          "点 2 输出 == 题面样例 %s。" % SAMPLE_OUT)


if __name__ == "__main__":
    main()
