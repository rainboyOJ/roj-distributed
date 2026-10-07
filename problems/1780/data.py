#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一本通 1780《修墙》分层测试数据生成器（题源：GDSOI2018 模拟 4.19 修墙）

用法（在 .ybt-import/staging/1780/ 下）：
    nice -n 19 timeout 120 g++ -O2 -std=c++17 -o std std.cpp
    nice -n 19 timeout 120 python3 data.py
产物：data/problem1.in + data/problem1.out ... data/problem10.in + data/problem10.out

关于 .out 的产生方式（避开 cyaron output_gen 写缓冲不 flush 的坑）：
    本脚本不用 cyaron 的 output_gen，而是写盘后用 subprocess 显式调 std
    （`nice -n 19 timeout 120 ./std < problemN.in > problemN.out`），
    随后逐点断言：.out 非空、行数恰好等于 q（本题每个询问必有一行输出，
    无解时输出 0，故不存在合法空输出点）、每行都是 >=0 的整数，
    并对「可手算的黄金样例」逐行比对期望值。

题意：0 起编号后 (i,j) 为白格 <=> (i & j) == 0；询问矩形内白格四连通块数。
数据范围（content.md 子任务表）：
    子任务1 q<=300   , x2,y2<=300
    子任务2 q<=3000  , x2,y2<=3000
    子任务3 q<=1e5   , x2,y2<=1e9
    子任务4 q<=1e6   , x2,y2<=1e9

分层策略（10 个测试点，从最小边界铺到顶格）：
    problem1  边界层：q=1，(1,1,1,1) 最小单格（白） -> 1（最小输入、最小非空答案）
    problem2  边界/手算层：20 组可手算的黄金询问（含题面 4 组样例、
              行 0/列 0 退化矩形、单格、x1=x2、y1=y2、跨 2 的幂边界），
              逐行断言期望值（期望值由"白格判据 + 父亲唯一性"手工推得，非暴力枚举）
    problem3  小规模随机：q=300, 坐标<=300（子任务1 上限：q 与坐标同时顶格）
    problem4  小规模顶格结构：q=300, 坐标<=300 —— 全图正方形/整行/整列/最大单格/细长条
    problem5  中规模随机：q=3000, 坐标<=3000（子任务2 上限）
    problem6  中规模顶格结构：q=3000, 坐标<=3000 —— 全图/整行/整列/最大单格 + 近上限随机
    problem7  大规模随机：q=1e5, 坐标<=1e9（子任务3 上限）
    problem8  大规模顶格结构：q=1e5, 坐标<=1e9 —— 全图(1,1,1e9,1e9)/整行/整列/最大单格 + 随机
    problem9  顶格满负荷随机：q=1e6, 坐标<=1e9（子任务4 上限，最大 q）
    problem10 顶格满负荷极端：q=1e6, 坐标<=1e9 —— 全图与最大单格交替 + 最大整行/整列 + 近上限随机
"""

import json
import os
import random
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
STD = os.path.join(HERE, "std")

L1 = 300          # 子任务1 坐标上限
L2 = 3000         # 子任务2 坐标上限
LB = 10 ** 9      # 子任务3/4 坐标上限

# ---------------------------------------------------------------- 生成原语
def rnd_queries(q, lim, seed):
    """q 组随机询问，保证 1 <= x1 <= x2 <= lim, 1 <= y1 <= y2 <= lim。O(q)。"""
    rnd = random.Random(seed)
    for _ in range(q):
        a = rnd.randint(1, lim)
        b = rnd.randint(1, lim)
        if a > b:
            a, b = b, a
        c = rnd.randint(1, lim)
        d = rnd.randint(1, lim)
        if c > d:
            c, d = d, c
        yield (a, c, b, d)


def near_max_queries(q, lim, seed):
    """近上限随机：左端点小、右端点贴上限（大面积矩形，答案多为小常数）。O(q)。"""
    rnd = random.Random(seed)
    for _ in range(q):
        a = rnd.randint(1, 8)
        b = rnd.randint(max(1, lim - 7), lim)
        c = rnd.randint(1, 8)
        d = rnd.randint(max(1, lim - 7), lim)
        if a > b:
            a, b = b, a
        if c > d:
            c, d = d, c
        yield (a, c, b, d)


def structured_queries(q, lim, seed):
    """顶格结构：全图 / 整行 / 整列 / 最大单格 / 细长条，其余用近上限随机补足。O(q)。"""
    head = [
        (1, 1, lim, lim),            # 全图正方形 -> 1（白格图连通）
        (1, 1, lim, 1),              # 第 0 列整列 -> 1
        (1, 1, 1, lim),              # 第 0 行整行 -> 1
        (lim, lim, lim, lim),        # 最大单格（黑） -> 0
        (1, lim, 1, lim),            # 第 0 行单格（白） -> 1
        (lim, 1, lim, 1),            # 第 0 列单格（白） -> 1
        (1, 1, lim, 2),              # 两列全高
        (lim - 1, 1, lim, lim),      # 最底两行
        (1, lim - 1, lim, lim),      # 最右两列
        (lim // 2, lim // 2, lim, lim),
    ]
    yield from head
    n = len(head)
    for t in near_max_queries(q - n, lim, seed):
        yield t


def extreme_queries(q, seed):
    """顶格满负荷极端：全图(答案1) 与 最大单格(答案0) 交替 + 最大整行/整列 + 近上限随机。O(q)。"""
    rnd = random.Random(seed)
    for i in range(q):
        r = i % 6
        if r == 0:
            yield (1, 1, LB, LB)          # 全图 -> 1
        elif r == 1:
            yield (LB, LB, LB, LB)        # 最大单格（黑） -> 0
        elif r == 2:
            yield (1, 1, LB, 1)           # 最大整列（第 0 列） -> 1
        elif r == 3:
            yield (1, 1, 1, LB)           # 最大整行（第 0 行） -> 1
        elif r == 4:
            a = rnd.randint(1, 4)
            b = rnd.randint(LB - 3, LB)
            c = rnd.randint(1, 4)
            d = rnd.randint(LB - 3, LB)
            yield (a, c, b, d)
        else:
            a = rnd.randint(1, LB)
            b = rnd.randint(a, LB)
            c = rnd.randint(1, LB)
            d = rnd.randint(c, LB)
            yield (a, c, b, d)


# ---------------------------------------------------------------- 黄金样例（手工推导）
# 期望值来源：白格判据 W(i,j) <=> (i&j)==0 与"父亲 = 唯一白邻居（行/列下标减 1）"手工推得，
# 不含任何暴力枚举/对拍。题面样例 4 组逐字取自 content.md。
GOLDEN = [
    # (x1, y1, x2, y2, 期望, 说明)
    (2, 2, 2, 2, 0, "题面样例4：单格 (1,1) 黑（1&1!=0）"),
    (1, 1, 1, 1, 1, "最小单格 (0,0)：0&0==0 白，唯一根"),
    (1, 1, 5, 5, 1, "题面样例1：左上 5x5"),
    (2, 2, 3, 6, 3, "题面样例2"),
    (4, 2, 7, 5, 3, "题面样例3"),
    (1, 1, 1, 2, 1, "第 0 行两格，连通"),
    (1, 1, 2, 2, 1, "3 格 L 形，连通"),
    (1, 1, 4, 4, 1, "4x4 三角块，连通（= 2x2 的 3 个白色子块）"),
    (2, 2, 3, 3, 2, "4 格中 2 个对角白格互不相邻"),
    (3, 1, 4, 8, 2, "行 2..3 全宽：两个连通块"),
    (1, 2, 1, 4, 1, "第 0 行连续 3 格"),
    (2, 2, 2, 3, 1, "单白格 (1,2)"),
    (2, 1, 2, 1, 1, "单白格 (1,0)"),
    (5, 1, 8, 4, 1, "4x4 三角块（偏移 (4,0)），连通"),
    (5, 5, 5, 5, 0, "单格 (4,4)：4&4!=0 黑"),
    (3, 3, 3, 3, 0, "单格 (2,2)：2&2!=0 黑"),
    (1, 1, 1, LB, 1, "第 0 行整行（1e9 格）连通"),
    (1, 1, LB, 1, 1, "第 0 列整列（1e9 格）连通"),
    (1, 1, LB, LB, 1, "全图（1e9 x 1e9）连通"),
    (LB, LB, LB, LB, 0, "最大坐标单格 (1e9-1,1e9-1) 黑"),
]


def golden_queries():
    for x1, y1, x2, y2, _e, _n in GOLDEN:
        yield (x1, y1, x2, y2)


# ---------------------------------------------------------------- 测试点定义
# (idx, q, 备注, 生成器工厂, 期望断言 {行号(0起): 期望值})
def build_cases():
    cases = []
    cases.append((1, 1, "边界层：q=1，最小单格 (1,1,1,1) 白 -> 1", lambda: iter([(1, 1, 1, 1)]), {0: 1}))
    cases.append((2, len(GOLDEN), "边界/手算层：20 组黄金询问（含题面样例），逐行比对期望",
                  golden_queries, {i: e for i, (_a, _b, _c, _d, e, _n) in enumerate(GOLDEN)}))

    cases.append((3, 300, "小规模随机：q=300, 坐标<=300（子任务1 顶格）",
                  lambda: rnd_queries(300, L1, 178003), {}))
    exp4 = {0: 1, 1: 1, 2: 1, 3: 0, 4: 1, 5: 1}
    cases.append((4, 300, "小规模顶格结构：q=300, 坐标<=300（全图/整行/整列/最大单格/细长条）",
                  lambda: structured_queries(300, L1, 178004), exp4))

    cases.append((5, 3000, "中规模随机：q=3000, 坐标<=3000（子任务2 顶格）",
                  lambda: rnd_queries(3000, L2, 178005), {}))
    exp6 = {0: 1, 1: 1, 2: 1, 3: 0, 4: 1, 5: 1}
    cases.append((6, 3000, "中规模顶格结构：q=3000, 坐标<=3000",
                  lambda: structured_queries(3000, L2, 178006), exp6))

    cases.append((7, 100000, "大规模随机：q=1e5, 坐标<=1e9（子任务3 顶格）",
                  lambda: rnd_queries(100000, LB, 178007), {}))
    exp8 = {0: 1, 1: 1, 2: 1, 3: 0, 4: 1, 5: 1}
    cases.append((8, 100000, "大规模顶格结构：q=1e5, 坐标<=1e9",
                  lambda: structured_queries(100000, LB, 178008), exp8))

    cases.append((9, 1000000, "顶格满负荷随机：q=1e6, 坐标<=1e9（子任务4 上限）",
                  lambda: rnd_queries(1000000, LB, 178009), {}))
    exp10 = {}
    for i in range(1000000):
        r = i % 6
        if r == 0 or r == 2 or r == 3:
            exp10[i] = 1
        elif r == 1:
            exp10[i] = 0
    cases.append((10, 1000000, "顶格满负荷极端：q=1e6, 坐标<=1e9（全图/最大单格/最大整行整列交替 + 近上限随机）",
                  lambda: extreme_queries(1000000, 178010), exp10))
    return cases


def write_in(path, q, gen):
    with open(path, "w", encoding="ascii", buffering=1 << 20) as f:
        f.write("%d\n" % q)
        n = 0
        for (x1, y1, x2, y2) in gen:
            f.write("%d %d %d %d\n" % (x1, y1, x2, y2))
            n += 1
    assert n == q, "生成器产出行数 %d != 声明的 q=%d" % (n, q)
    return n


def run_std(in_path, out_path):
    t0 = time.time()
    with open(in_path, "rb") as fi, open(out_path, "wb") as fo:
        # 耗时命令统一 nice -n 19 timeout 120 包裹
        subprocess.run(["nice", "-n", "19", "timeout", "120", STD],
                       stdin=fi, stdout=fo, check=True)
    return time.time() - t0


def verify(out_path, q, expect):
    size = os.path.getsize(out_path)
    assert size > 0, "%s 为空文件（.out 必须非空）" % out_path
    with open(out_path, "r", encoding="ascii") as f:
        lines = f.read().split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    assert len(lines) == q, "%s 行数 %d != q=%d" % (out_path, len(lines), q)
    for i, ln in enumerate(lines):
        assert ln.strip().lstrip("-").isdigit(), "%s 第 %d 行非整数: %r" % (out_path, i + 1, ln)
        assert int(ln) >= 0, "%s 第 %d 行答案为负: %r" % (out_path, i + 1, ln)
    for i, e in expect.items():
        got = int(lines[i])
        assert got == e, "%s 第 %d 行期望 %d 实得 %d" % (out_path, i + 1, e, got)
    return size


def main():
    if not os.path.isfile(STD):
        print("缺少可执行 std，请先编译：g++ -O2 -std=c++17 -o std std.cpp", file=sys.stderr)
        return 1
    os.makedirs(DATA_DIR, exist_ok=True)
    cases = build_cases()
    assert len(cases) == 10, "必须恰好 10 个测试点"

    rows = []
    for idx, q, note, gen_factory, expect in cases:
        in_path = os.path.join(DATA_DIR, "problem%d.in" % idx)
        out_path = os.path.join(DATA_DIR, "problem%d.out" % idx)
        t0 = time.time()
        write_in(in_path, q, gen_factory())
        t_gen = time.time() - t0
        t_std = run_std(in_path, out_path)
        out_size = verify(out_path, q, expect)
        in_size = os.path.getsize(in_path)
        rows.append((idx, q, in_size, out_size, t_gen, t_std, note))
        print("problem%-2d q=%-8d in=%-10d out=%-10d gen=%5.2fs std=%5.2fs  断言通过  %s"
              % (idx, q, in_size, out_size, t_gen, t_std, note))

    # data.json（与仓库其它 staging 目录同格式）
    files = []
    for idx in range(1, 11):
        for ext in ("in", "out"):
            p = "problem%d.%s" % (idx, ext)
            files.append({"path": p, "size": os.path.getsize(os.path.join(DATA_DIR, p))})
    with open(os.path.join(HERE, "data.json"), "w", encoding="utf-8") as f:
        json.dump({"files": files}, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("\n全部 10 点生成 + 校验通过；data.json 已更新（%d 个文件）。" % len(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
