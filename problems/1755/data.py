#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1755《星际探测》分层测试数据生成器
#
# 用法：python3 data.py            （脚本自己编译 std.cpp 并产出 data/problem*.in|out）
#
# 题面范围（content.md）：
#   1 <= N, Q <= 1e5；1 <= K <= 6；1 <= D, V <= 1e9；1 <= L <= R <= 1e9；
#   保证所有区域的 D 互不相等、V 互不相等。
#   限制 time 2000 ms / memory 256 MB（config.json）。
#
# ---- 分层策略（10 组；边界 / 小 / 中 / 大 / 顶格）----
#   点 1  边界层：n=1，两次询问都不足 K 块 => 输出全 0（题面「没有 K 块区域可供选择」）。
#   点 2  样例层：题面样例，逐字比对期望输出 5 / 52 / 924。
#   点 3  小规模 K=1（对应 30% 子任务）：n=10，含空区间、单点区间、全区间。
#   点 4  小规模 K<=2（对应 60% 子任务）：n=30。
#   点 5  小规模 K<=3（对应 80% 子任务）：n=60。
#   点 6  小规模全 K<=6：n=50，K∈[1,6]。
#   点 7  中等规模：n=1000, q=1000，K∈[1,6]，区间含空/窄/宽。
#   点 8  大规模随机：n=1e5, q=1e5，K∈[1,6]，L,R 随机（含空区间）。
#   点 9  大规模顶格 K=6：n=1e5, q=1e5，K 恒为 6，L,R 随机（线段树访问结点最多）。
#   点 10 顶格边界：n=1e5, q=1e5，D、V 取 1e9 附近（大乘积取模 2^32 回绕），
#         L,R 取 1/1e9/精确 D 值，K∈[1,6]。
#
#   生成用固定随机种子，完全可复现；所有 D、V 组内互不相等。
#   .out 一律用 std 显式跑出（subprocess），并断言非空、行数 == Q。

import json
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
STD = os.path.join(HERE, "std")
DMAX = 10 ** 9

SAMPLE_IN = "5 3\n5 4 7 2 6\n1 4 5 3 2\n6 7 1\n2 6 2\n1 8 3\n"
SAMPLE_OUT = "5\n52\n924\n"


def distinct(cnt, lo, hi, rng):
    """从 [lo,hi] 取 cnt 个互不相同的整数（cnt 远小于区间长度）。"""
    return rng.sample(range(lo, hi + 1), cnt)


def random_queries(Ds, qcount, kgen, rng, empty_ratio=0.15):
    Dsort = sorted(Ds)
    n = len(Dsort)
    qs = []
    for _ in range(qcount):
        if rng.random() < empty_ratio:
            L = rng.randint(1, DMAX)
            R = rng.randint(L, DMAX)
        else:
            i = rng.randrange(n)
            j = rng.randrange(n)
            if i > j:
                i, j = j, i
            L, R = Dsort[i], Dsort[j]
        qs.append((L, R, kgen(rng)))
    return qs


def serialize(n, Ds, Vs, queries):
    out = ["%d %d" % (n, len(queries)), " ".join(map(str, Ds)), " ".join(map(str, Vs))]
    for L, R, K in queries:
        out.append("%d %d %d" % (L, R, K))
    return "\n".join(out) + "\n"


# ---------------- 各测试点 ----------------
def case1():
    # 边界：n=1，任何询问可选区域 0 块 => 0
    n, Ds, Vs = 1, [5], [7]
    qs = [(1, DMAX, 1), (5, 5, 6), (1, 4, 1)]
    return n, Ds, Vs, qs, "边界层：n=1，可选不足 K 块，输出全 0"


def case2():
    return (5, [5, 4, 7, 2, 6], [1, 4, 5, 3, 2],
            [(6, 7, 1), (2, 6, 2), (1, 8, 3)],
            "样例层：题面样例，期望 5/52/924")


def case3():
    rng = random.Random(175503)
    n = 10
    Ds = distinct(n, 1, 60, rng)
    Vs = distinct(n, 1, 60, rng)
    Dsort = sorted(Ds)
    qs = [(1, DMAX, 1), (Dsort[0], Dsort[0], 1), (Dsort[0], Dsort[-1], 1),
          (Dsort[3], Dsort[5], 1), (DMAX, DMAX, 1)]
    qs += random_queries(Ds, 5, lambda r: 1, rng, 0.2)
    return n, Ds, Vs, qs, "小规模：n=10，K=1（30% 子任务）"


def case4():
    rng = random.Random(175504)
    n = 30
    Ds = distinct(n, 1, 200, rng)
    Vs = distinct(n, 1, 200, rng)
    qs = random_queries(Ds, 30, lambda r: r.randint(1, 2), rng, 0.15)
    return n, Ds, Vs, qs, "小规模：n=30，K<=2（60% 子任务）"


def case5():
    rng = random.Random(175505)
    n = 60
    Ds = distinct(n, 1, 400, rng)
    Vs = distinct(n, 1, 400, rng)
    qs = random_queries(Ds, 60, lambda r: r.randint(1, 3), rng, 0.15)
    return n, Ds, Vs, qs, "小规模：n=60，K<=3（80% 子任务）"


def case6():
    rng = random.Random(175506)
    n = 50
    Ds = distinct(n, 1, 500, rng)
    Vs = distinct(n, 1, 500, rng)
    qs = random_queries(Ds, 50, lambda r: r.randint(1, 6), rng, 0.15)
    return n, Ds, Vs, qs, "小规模：n=50，K∈[1,6]"


def case7():
    rng = random.Random(175507)
    n, q = 1000, 1000
    Ds = distinct(n, 1, 10 ** 6, rng)
    Vs = distinct(n, 1, 10 ** 6, rng)
    qs = random_queries(Ds, q, lambda r: r.randint(1, 6), rng, 0.15)
    return n, Ds, Vs, qs, "中等规模：n=q=1000，K∈[1,6]"


def case8():
    rng = random.Random(175508)
    n, q = 100000, 100000
    Ds = distinct(n, 1, DMAX, rng)
    Vs = distinct(n, 1, DMAX, rng)
    qs = random_queries(Ds, q, lambda r: r.randint(1, 6), rng, 0.15)
    return n, Ds, Vs, qs, "大规模随机：n=q=1e5，K∈[1,6]"


def case9():
    rng = random.Random(175509)
    n, q = 100000, 100000
    Ds = distinct(n, 1, DMAX, rng)
    Vs = distinct(n, 1, DMAX, rng)
    qs = random_queries(Ds, q, lambda r: 6, rng, 0.1)
    return n, Ds, Vs, qs, "大规模顶格：n=q=1e5，K=6（访问结点最多）"


def case10():
    rng = random.Random(175510)
    n, q = 100000, 100000
    lo = DMAX - n + 1
    Ds = distinct(n, lo, DMAX, rng)          # D 全在 1e9 附近
    Vs = distinct(n, lo, DMAX, rng)          # V 全在 1e9 附近，乘积回绕 2^32
    Dsort = sorted(Ds)
    qs = [(1, DMAX, 6), (1, DMAX, 1), (DMAX, DMAX, 1),
          (1, 1, 6), (Dsort[0], Dsort[0], 1), (Dsort[0], Dsort[-1], 6)]
    qs += random_queries(Ds, q - len(qs), lambda r: r.randint(1, 6), rng, 0.2)
    return n, Ds, Vs, qs, "顶格边界：D,V 近 1e9，K∈[1,6]，取模回绕"


CASES = [
    (1, case1), (2, case2), (3, case3), (4, case4), (5, case5),
    (6, case6), (7, case7), (8, case8), (9, case9), (10, case10),
]


def build_std():
    cmd = ["g++", "-O2", "-std=c++17", "-o", STD, os.path.join(HERE, "std.cpp")]
    subprocess.run(cmd, check=True)


def main():
    build_std()
    os.makedirs(DATA, exist_ok=True)
    manifest = []
    for idx, fn in CASES:
        n, Ds, Vs, qs, note = fn()
        assert len(Ds) == n and len(Vs) == n, "点 %d D/V 数量与 n 不符" % idx
        assert len(set(Ds)) == n and len(set(Vs)) == n, "点 %d D/V 出现重复" % idx
        for L, R, K in qs:
            assert 1 <= L <= R <= DMAX and 1 <= K <= 6, "点 %d 询问越界" % idx
        text = serialize(n, Ds, Vs, qs)

        in_path = os.path.join(DATA, "problem%d.in" % idx)
        out_path = os.path.join(DATA, "problem%d.out" % idx)
        with open(in_path, "w") as f:
            f.write(text)

        # 显式用 std 跑出 .out（不用 cyaron output_gen，避免缓冲未 flush 产出 0 字节）
        with open(in_path, "rb") as fin, open(out_path, "wb") as fout:
            subprocess.run([STD], stdin=fin, stdout=fout, check=True)

        with open(out_path, "r") as f:
            lines = f.read().splitlines()
        assert lines, "点 %d .out 为空（%d 行预期）" % (idx, len(qs))
        assert len(lines) == len(qs), "点 %d .out 行数 %d != Q=%d" % (idx, len(lines), len(qs))

        if idx == 2:
            got = "\n".join(lines) + "\n"
            assert got == SAMPLE_OUT, "样例输出不符: %r" % got

        for name in ("problem%d.in" % idx, "problem%d.out" % idx):
            manifest.append({"path": name, "size": os.path.getsize(os.path.join(DATA, name))})

        print("problem%-2d n=%-6d Q=%-6d K∈[%d,%d]  %s" % (
            idx, n, len(qs), min(k for _, _, k in qs), max(k for _, _, k in qs), note))

    manifest.sort(key=lambda item: item["path"])
    with open(os.path.join(HERE, "data.json"), "w") as f:
        json.dump({"files": manifest}, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("data.json 已写入，共 %d 个文件" % len(manifest))


if __name__ == "__main__":
    sys.exit(main())
