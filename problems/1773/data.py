#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1773《消息传递》数据生成器
# ---------------------------------------------------------------------------
# 输入格式：第一行 N；随后 N-1 行，第 i 行（i 从 2 到 N）为编号 i 的人的直接上级编号。
# 数据范围（题面【数据规模与约定】）：
#   20%  N<=3000 ; 50%  N<=20000 ; 100%  N<=200000
# 分层 10 组：样例 / 最小 / 小 / 20%边界 / 50%边界 / 顶格，覆盖链、星、随机、平衡二叉树。
# 生成约束：parent[i] in [1, i-1]（i=2..N），保证是一棵以 1 为根、连通无环的合法树。
# .out 一律由 std 显式跑出（subprocess），并断言非空、恰 2 行、格式合法，
# 规避 cyaron output_gen 缓冲未 flush 导致 0 字节 .out 的隐患。
# 生成全部为 O(N) 线性，无 O(N^2) Python 循环。
# ---------------------------------------------------------------------------
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "std")
OUTDIR = os.path.join(HERE, "data")
os.makedirs(OUTDIR, exist_ok=True)


def build_parents(kind, n, rng):
    """返回长度为 n-1 的 parent 列表，第 j 项为点 (j+2) 的直接上级，取值 [1, i-1]。"""
    if n <= 1:
        return []
    if kind == "chain":                       # 链：1-2-...-n（最深）
        return [i - 1 for i in range(2, n + 1)]
    if kind == "star":                        # 星：全部挂 1（最大度）
        return [1] * (n - 1)
    if kind == "binary":                      # 完全二叉树：i 的父亲 i//2
        return [i // 2 for i in range(2, n + 1)]
    if kind == "random":                      # 随机递归树
        return [rng.randint(1, i - 1) for i in range(2, n + 1)]
    if kind == "shallow":                     # 浅随机树（一半直接挂根）
        return [1 if rng.random() < 0.5 else rng.randint(1, i - 1)
                for i in range(2, n + 1)]
    raise ValueError("unknown kind: " + kind)


def write_in(path, n, parents):
    parts = [str(n)]
    parts.extend(map(str, parents))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
        f.write("\n")


def run_std(in_path, out_path, n):
    with open(in_path, "rb") as fin:
        proc = subprocess.run([STD], stdin=fin, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=60)
    if proc.returncode != 0:
        raise RuntimeError("std failed rc=%d stderr=%s" %
                           (proc.returncode, proc.stderr.decode(errors="ignore")[:500]))
    raw = proc.stdout
    if len(raw) == 0:
        raise RuntimeError("std produced empty output for %s" % in_path)
    with open(out_path, "wb") as f:
        f.write(raw)
    # ---- 结构断言 ----
    text = raw.decode()
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    assert len(lines) == 2, "expected 2 lines, got %d for %s" % (len(lines), in_path)
    t = int(lines[0])
    assert t >= 1, "min time must be >=1"
    toks = lines[1].split()
    assert len(toks) >= 1, "no source node listed"
    vals = [int(x) for x in toks]
    assert all(1 <= v <= n for v in vals), "source out of range"
    assert all(vals[i] < vals[i + 1] for i in range(len(vals) - 1)), "not strictly ascending"
    return t, len(vals)


# (data_id, 描述, kind, N)
CASES = [
    (1,  "题面样例1（星，N=4）",        "sample1", None),
    (2,  "题面样例2（N=8）",            "sample2", None),
    (3,  "最小规模 N=1",                "n1",      None),
    (4,  "小规模随机树 N=100",          "random",  100),
    (5,  "20%边界 深链 N=3000",         "chain",   3000),
    (6,  "50%边界 随机树 N=20000",      "random",  20000),
    (7,  "顶格 深链 N=200000",          "chain",   200000),
    (8,  "顶格 星 N=200000",            "star",    200000),
    (9,  "顶格 随机树 N=200000",        "random",  200000),
    (10, "顶格 平衡二叉树 N=200000",    "binary",  200000),
]


def main():
    if not os.path.exists(STD):
        print("std not found: %s (请先编译)" % STD, file=sys.stderr)
        sys.exit(1)
    summary = []
    for (did, desc, kind, n) in CASES:
        rng = random.Random(177300 + did)
        if kind == "sample1":
            n = 4
            parents = [1, 1, 1]
        elif kind == "sample2":
            n = 8
            parents = [1, 1, 3, 4, 4, 4, 3]
        elif kind == "n1":
            n = 1
            parents = []
        else:
            parents = build_parents(kind, n, rng)
        in_path = os.path.join(OUTDIR, "problem%d.in" % did)
        out_path = os.path.join(OUTDIR, "problem%d.out" % did)
        write_in(in_path, n, parents)
        t, cnt = run_std(in_path, out_path, n)
        summary.append((did, desc, n, t, cnt, os.path.getsize(in_path), os.path.getsize(out_path)))
        print("case %2d  N=%-7d time=%-8d #src=%-7d  in=%-9dB out=%-8dB  %s"
              % (did, n, t, cnt, os.path.getsize(in_path), os.path.getsize(out_path), desc))
    print("ALL %d CASES OK" % len(CASES))


if __name__ == "__main__":
    main()
