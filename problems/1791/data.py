#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1791《太空飞船》分层测试数据生成器
#
# 用法：
#   g++ -O2 -std=c++17 std.cpp -o std
#   mkdir -p data
#   python3 data.py
# 产出：data/problem1.in ... data/problem10.in 以及同名 .out（.out 由 std 显式跑出）
#
# 说明（按任务书提示）：
#   cyaron 的 io.output_gen 若写缓冲不 flush 会产出 0 字节 .out，故本生成器不依赖 cyaron，
#   改为「Python 写 .in」+「subprocess 显式运行 std 写 .out」，并断言：
#     * .in 非空、.out 非空、.out 恰好 1 行（本题输出恒为一行整数）；
#     * 所有 N/K/L 均在题面范围内（1<=L_i<=1000，1<=K<=N）。
#   本题无「无解空输出」点，故 .out 一律要求非空。
#
# 题面数据范围（content.md / 官方页 1791）：
#   1 <= L_i <= 1000；10 个测试点；n<=400 的点 K 最大 20；n>400 的点（N=1000/100000/300000）
#   K 仅为 2 或 3（与 std.cpp 的分支设计一致）。
# 时限 1000 ms：本数据集最大点 N=300000，std 走 O(N) 双指针/二分分支，可稳定跑完。

import json
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "std")          # 编译产物（std.cpp）
OUTDIR = os.path.join(HERE, "data")
MAXL = 1000                              # 题面：1 <= L_i <= 1000


def build_cases():
    """返回 [(点号, n, k, L数组, 分层说明), ...]，恰好 10 组。"""
    rng = random.Random(17910001)  # 固定种子，结果可复现
    cases = []

    # ---- 边界层 ----
    cases.append((1, 2, 2, [1, MAXL],
                  "边界层：N=2=K（最小规模），L∈{1,1000} 取上下界极值"))

    # ---- 大 n / 小 k（题面 n>400 点 K 只到 3）----
    cases.append((2, 100000, 2, [rng.randint(1, MAXL) for _ in range(100000)],
                  "大 n 小 k：N=100000, K=2，L 均匀随机 [1,1000]"))

    # ---- 小 n ----
    cases.append((3, 100, 3, [1 if i % 2 == 0 else MAXL for i in range(100)],
                  "小 n：N=100, K=3，L 交替 1/1000（结构化，考二分切点）"))

    # ---- 大 n / k=3 / L 上界 ----
    cases.append((4, 100000, 3, [MAXL] * 100000,
                  "大 n：N=100000, K=3，L 全 1000（长度上界）"))

    # ---- 顶格 n ----
    cases.append((5, 300000, 3, [rng.randint(1, MAXL) for _ in range(300000)],
                  "顶格层：N=300000（题面上界）, K=3，L 均匀随机"))

    # ---- 小 n / L 下界 ----
    cases.append((6, 50, 6, [1] * 50,
                  "小 n：N=50, K=6，L 全 1（长度下界）"))

    # ---- 小 n ----
    cases.append((7, 100, 7, [rng.randint(1, MAXL) for _ in range(100)],
                  "小 n：N=100, K=7，L 均匀随机"))

    # ---- 中 n ----
    cases.append((8, 200, 10, [rng.randint(1, MAXL) for _ in range(200)],
                  "中 n：N=200, K=10，L 均匀随机"))

    # ---- 中 n ----
    cases.append((9, 300, 15, [rng.randint(1, MAXL) for _ in range(300)],
                  "中 n：N=300, K=15，L 均匀随机"))

    # ---- 顶格 k ----
    cases.append((10, 400, 20, [rng.randint(1, MAXL) for _ in range(400)],
                  "顶格层：N=400, K=20（K 上界，走 n<=400 斜率优化分支）"))

    return cases


def main():
    if not os.path.exists(STD):
        sys.exit("找不到 std 可执行文件：请先 g++ -O2 -std=c++17 std.cpp -o std")
    os.makedirs(OUTDIR, exist_ok=True)

    cases = build_cases()
    assert len(cases) == 10, "必须恰好 10 个测试点"
    assert [c[0] for c in cases] == list(range(1, 11)), "点号必须为 1..10"

    # ---- 静态自检：范围与结构 ----
    for idx, n, k, arr, _note in cases:
        assert len(arr) == n, "点%d：L 个数 %d != N %d" % (idx, len(arr), n)
        assert 1 <= k <= n, "点%d：K=%d 越界（应 1<=K<=N=%d）" % (idx, k, n)
        assert all(1 <= x <= MAXL for x in arr), "点%d：存在越界 L_i" % idx

    records = []
    print("%-4s %-8s %-5s %-9s %s" % ("点", "N", "K", "S", "分层说明"))
    for idx, n, k, arr, note in cases:
        inp = "%d %d\n%s\n" % (n, k, " ".join(map(str, arr)))
        inpath = os.path.join(OUTDIR, "problem%d.in" % idx)
        with open(inpath, "w") as f:
            f.write(inp)

        # 显式跑 std 生成 .out（避免 cyaron output_gen 的写缓冲隐患）
        r = subprocess.run([STD], input=inp.encode(), stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=120)
        assert r.returncode == 0, "点%d：std 非零退出 rc=%d err=%s" % (
            idx, r.returncode, r.stderr.decode()[:200])
        out = r.stdout.decode()
        outpath = os.path.join(OUTDIR, "problem%d.out" % idx)
        with open(outpath, "w") as f:
            f.write(out)

        # ---- 动态自检：文件非空 + 行数符合预期（恒 1 行）----
        insize = os.path.getsize(inpath)
        outsize = os.path.getsize(outpath)
        lines = out.strip().split("\n")
        assert insize > 0, "点%d：.in 为空" % idx
        assert outsize > 0, "点%d：.out 为 0 字节（无解空输出点除外，本题无此情形）" % idx
        assert len(lines) == 1 and lines[0].strip() != "", \
            "点%d：.out 行数 %d（应恰好 1 行）" % (idx, len(lines))
        val = int(lines[0].strip())
        assert val >= 0, "点%d：答案为负（%d），违反方差非负性" % (idx, val)
        # 方差*K^2 的上界粗检：<= K^2 * S^2
        S = sum(arr)
        assert val <= k * k * S * S, "点%d：答案超上界" % idx

        records.append({"path": "problem%d.in" % idx, "size": insize})
        records.append({"path": "problem%d.out" % idx, "size": outsize})
        print("%-4d %-8d %-5d %-9d %s" % (idx, n, k, S, note))

    # ---- 写 data.json（仓库惯例：文件清单 + 字节数，按路径排序）----
    records.sort(key=lambda x: (len(x["path"]), x["path"]))
    with open(os.path.join(HERE, "data.json"), "w") as f:
        json.dump({"files": records}, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("\nOK：10 组 .in/.out 已生成到 %s" % OUTDIR)


if __name__ == "__main__":
    main()
