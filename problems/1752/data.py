#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 1752《纪念碑》数据生成器
#
# 题面：n×m 方格土地（左下角格 (1,1)，右上角格 (n,m)），p 个矩形建筑物，
#       第 i 个左下角 (x1,y1)、右上角 (x2,y2)，占格 x∈[x1,x2], y∈[y1,y2]。
#       求不覆盖任何建筑物的最大正方形边长（格数）。
#
# 数据范围（题面【数据规模】原文）：
#       30%  p ≤ 1000
#       70%  p ≤ 30000
#       100% p ≤ 400000， m,n ≤ 1000000
#
# 输入格式：题面写「每一组数据的第一行包含 n,m,p」，但**未给组数 T**，样例为单组。
#   本生成器按「单组」造数（每个 .in 一个测试点，恰一组数据），std 按读到 EOF 处理，
#   兼容单组/多组两种口径（单组时输出恰 1 行）。
#
# 生成方式：cyaron 的 IO(file_prefix="problem", data_id=i) + io.output_gen("../std")。
#   **运行方式：在 data/ 子目录下执行 `python3 ../data.py`**（故 std 路径为 ../std）。
#   用 `with IO(...) as io:` 保证退出时 flush，避免缓冲未落盘产生 0 字节文件；
#   生成后用 `_self_check()` 逐个断言 .in/.out 非空、行数正确、答案在合法区间。
#
# 分层设计（10 个测试点）：
#   点 1    边界层：n=m=1,p=0（最小规模，答案 1）
#   点 2    边界层：n=m=1,p=1 全覆盖（答案 0，覆盖「答案为 0」极端）
#   点 3    样例：题面【输入样例】原样，答案 3（唯一可手算核对点）
#   点 4    小规模随机：n,m∈[1,8]，p∈[0,4]
#   点 5    小规模退化结构：n=m=15，p=30 条「线段型」建筑物（x1=x2 或 y1=y2，仿样例）
#   点 6    中等规模随机：n=m=500，p=400
#   点 7    70% 档：n=m=20000，p=30000（题面 70% 上限）
#   点 8    大规模随机：n=m=200000，p=100000
#   点 9    接近顶格（稀疏）：n=m=1000000，p=100000
#   点 10   顶格：n=m=1000000，p=400000（题面 100% 上限，最坏规模）
#
# 随机性：每个点使用独立 random.Random(1752 + 点号)，与调用顺序无关，可精确复现。
# 复杂度：每点 O(p) 生成，无 O(n²) 循环。

from cyaron import *  # noqa: F401,F403  （IO 等）

import os
import random
import sys

MAXN = 10 ** 6   # 题面 m,n 上限
MAXP = 400000    # 题面 p 上限

SAMPLE = (
    "13 5 8\n"
    "8 4 10 4\n"
    "4 3 4 4\n"
    "10 2 12 2\n"
    "8 2 8 4\n"
    "2 4 6 4\n"
    "10 3 10 4\n"
    "12 3 12 4\n"
    "2 2 4 2\n"
)

# 记录 (点号, n, m, p, note)，用于末尾自检
_meta = []


def rand_rects(rng, n, m, p, maxsize=None):
    """生成 p 个随机矩形（保证 x1<=x2, y1<=y2）。maxsize 限制单边跨度上界。"""
    rects = []
    for _ in range(p):
        x1 = rng.randint(1, n)
        y1 = rng.randint(1, m)
        if maxsize is None:
            x2 = rng.randint(x1, n)
            y2 = rng.randint(y1, m)
        else:
            x2 = min(n, x1 + rng.randint(0, maxsize))
            y2 = min(m, y1 + rng.randint(0, maxsize))
        rects.append((x1, y1, x2, y2))
    return rects


def rand_segments(rng, n, m, p):
    """生成 p 条轴平行线段型建筑物（x1==x2 竖线，或 y1==y2 横线），仿题面样例结构。"""
    rects = []
    for _ in range(p):
        if rng.random() < 0.5:
            x = rng.randint(1, n)
            y1 = rng.randint(1, m)
            y2 = rng.randint(y1, m)
            rects.append((x, y1, x, y2))
        else:
            y = rng.randint(1, m)
            x1 = rng.randint(1, n)
            x2 = rng.randint(x1, n)
            rects.append((x1, y, x2, y))
    return rects


def build_text(n, m, rects):
    parts = ["%d %d %d" % (n, m, len(rects))]
    for (x1, y1, x2, y2) in rects:
        parts.append("%d %d %d %d" % (x1, y1, x2, y2))
    return "\n".join(parts) + "\n"


def gen(i, n, m, rects, note):
    text = build_text(n, m, rects)
    with IO(file_prefix="problem", data_id=i) as io:  # problemI.in / problemI.out
        io.input_write(text)
        io.output_gen("../std")                      # 用 std 跑出 .out
    _meta.append((i, n, m, len(rects), note))
    print("problem%-2d: n=%-8d m=%-8d p=%-7d -- %s" % (i, n, m, len(rects), note))


def gen_text(i, text, n, m, p, note):
    with IO(file_prefix="problem", data_id=i) as io:
        io.input_write(text)
        io.output_gen("../std")
    _meta.append((i, n, m, p, note))
    print("problem%-2d: n=%-8d m=%-8d p=%-7d -- %s" % (i, n, m, p, note))


def main():
    # ---- 点 1：边界层，最小规模，答案 1 ----
    gen_text(1, "1 1 0\n", 1, 1, 0,
             "边界层：n=m=1,p=0 最小规模（答案应为 1）")

    # ---- 点 2：边界层，全覆盖，答案 0 ----
    gen_text(2, "1 1 1\n1 1 1 1\n", 1, 1, 1,
             "边界层：1×1 土地被 1 个建筑完全覆盖（答案应为 0）")

    # ---- 点 3：题面样例（唯一可手算核对点）----
    gen_text(3, SAMPLE, 13, 5, 8,
             "题面【输入样例】原样（答案应为 3，与输出样例一致）")

    # ---- 点 4：小规模随机 ----
    r4 = random.Random(1752 + 4)
    n4 = r4.randint(1, 8); m4 = r4.randint(1, 8); p4 = r4.randint(0, 4)
    gen(4, n4, m4, rand_rects(r4, n4, m4, p4), "小规模随机：n,m∈[1,8]，p∈[0,4]")

    # ---- 点 5：小规模退化结构（线段型，仿样例）----
    r5 = random.Random(1752 + 5)
    gen(5, 15, 15, rand_segments(r5, 15, 15, 30),
        "小规模退化结构：n=m=15，p=30 条线段型建筑（x1=x2 或 y1=y2，仿样例）")

    # ---- 点 6：中等规模随机 ----
    r6 = random.Random(1752 + 6)
    gen(6, 500, 500, rand_rects(r6, 500, 500, 400),
        "中等规模随机：n=m=500，p=400")

    # ---- 点 7：70% 档 ----
    r7 = random.Random(1752 + 7)
    gen(7, 20000, 20000, rand_rects(r7, 20000, 20000, 30000, maxsize=8),
        "70% 档：n=m=20000，p=30000（题面 70% 上限）")

    # ---- 点 8：大规模随机 ----
    r8 = random.Random(1752 + 8)
    gen(8, 200000, 200000, rand_rects(r8, 200000, 200000, 100000, maxsize=6),
        "大规模随机：n=m=200000，p=100000")

    # ---- 点 9：接近顶格（稀疏，答案较大）----
    r9 = random.Random(1752 + 9)
    gen(9, MAXN, MAXN, rand_rects(r9, MAXN, MAXN, 100000, maxsize=4),
        "接近顶格（稀疏）：n=m=1e6，p=1e5，小建筑 -> 答案较大")

    # ---- 点 10：顶格 ----
    r10 = random.Random(1752 + 10)
    gen(10, MAXN, MAXN, rand_rects(r10, MAXN, MAXN, MAXP, maxsize=5),
        "顶格：n=m=1e6，p=400000（题面 100% 上限，最坏规模）")

    _self_check()


def _self_check():
    """逐点校验：.in/.out 非空、.in 行数与 p 一致、.out 恰 1 行且答案在 [0, min(n,m)]。"""
    problems = []
    expected = {1: 1, 2: 0, 3: 3}
    for (i, n, m, p, note) in _meta:
        fin = "problem%d.in" % i
        fout = "problem%d.out" % i
        if not (os.path.exists(fin) and os.path.getsize(fin) > 0):
            problems.append("点 %d: %s 缺失或为空" % (i, fin))
            continue
        if not (os.path.exists(fout) and os.path.getsize(fout) > 0):
            problems.append("点 %d: %s 缺失或为空" % (i, fout))
            continue
        with open(fin, "r") as f:
            lines = f.read().splitlines()
        head = lines[0].split()
        if len(head) != 3 or list(map(int, head)) != [n, m, p]:
            problems.append("点 %d: .in 首行 %r 与预期 (%d %d %d) 不符" % (i, head, n, m, p))
        # 行数：首行 + p 行
        if len(lines) != p + 1:
            problems.append("点 %d: .in 行数 %d != p+1=%d" % (i, len(lines), p + 1))
        for k in range(1, p + 1):
            if len(lines[k].split()) != 4:
                problems.append("点 %d: 第 %d 行不是 4 个整数" % (i, k + 1))
                break
        with open(fout, "r") as f:
            outs = f.read().splitlines()
        if len(outs) != 1:
            problems.append("点 %d: .out 行数 %d != 1（单组数据应恰 1 行）" % (i, len(outs)))
            continue
        try:
            ans = int(outs[0].strip())
        except ValueError:
            problems.append("点 %d: .out 首行 %r 不是整数" % (i, outs[0]))
            continue
        if not (0 <= ans <= min(n, m)):
            problems.append("点 %d: 答案 %d 越界 [0, %d]" % (i, ans, min(n, m)))
        if i in expected and ans != expected[i]:
            problems.append("点 %d: 答案 %d != 预期 %d" % (i, ans, expected[i]))
        print("  check 点 %-2d: .in %d 行, .out=%d  -- ok" % (i, len(lines), ans))

    if problems:
        print("\n自检失败：", file=sys.stderr)
        for pr in problems:
            print("  - " + pr, file=sys.stderr)
        raise SystemExit(1)
    print("\n自检通过：10 个测试点 .in/.out 均非空且成对，行数与答案区间均符合预期。")


if __name__ == "__main__":
    main()
