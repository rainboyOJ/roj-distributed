#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1802《寿司晚宴》分层测试数据生成器（cyaron，仓库惯例）
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py
# 参考仓库惯例：.ybt-import/staging/1222/data.py、staging/1671/data.py
#
# 题意：给定 n, p，统计「把 2..n 分给 G / W（可有人不分），且任取 x∈G、y∈W 都有 gcd(x,y)=1」的方案数 mod p。
# 数据范围（题面明文）：2 <= n <= 500；0 <= p <= 1e9（原 NOI 题面为 0 < p <= 1e9，见 §6 风险点）。
#   子任务分档：n<=30 / n<=100 / n<=200 / n<=500。
# 限制 time 2000 ms / memory 512 MB（config.json）。
#
# ---- 分层策略（单组数据题：按 n 的档位 + p 的极端分层，每点 1 组，共 10 组）----
#   点 1  边界层：n=2（题面下界），p=1（模 1 极端 -> 答案恒 0）
#   点 2  边界层：n=2（题面下界），p=1e9（p 上限）
#   点 3  边界层：n=3（最小非平凡 n，含唯一小质数 2 与大质因子 1/3 混合）
#   点 4  样例回归：n=4, p=10000 —— 题面【输入样例1】，答案必须 21
#   点 5  小规模顶格：n=30, p=1e9 —— 子任务 1 的 n 上限
#   点 6  样例回归 + 中规模顶格：n=100, p=100000000 —— 题面【输入样例2】，答案必须 3107203（子任务 4 上限）
#   点 7  中大规模顶格：n=200, p=999999937（接近 p 上限的大质数模）—— 子任务 6 的 n 上限
#   点 8  大规模：n=300, p=1e9 —— 子任务 8 档位内的中间规模
#   点 9  顶格 + 模 1：n=500（n 上限）, p=1 —— 顶格规模下答案恒 0 的极端
#   点 10 顶格：n=500（n 上限）, p=1e9（p 上限）—— 最坏规模 + 最大模数
#
#   覆盖说明：n 的四个子任务分档边界 30 / 100 / 200 / 500 全部取到；n 的下界 2 与最小非平凡 3 取到；
#   p 的三个极端 1（最小有效模数）/ 10000（样例）/ 999999937 / 1e9（上限）取到。
#   生成后由 std 显式产出 .out（subprocess，避免 cyaron 写缓冲未 flush 产生 0 字节 .out），
#   并断言 .out 非空、恰 1 行、取值在 [0, p-1]，且两个样例点的答案逐字等于题面输出。

import os
import subprocess
import sys

from cyaron import IO  # 引入CYaRon的库

STD = "../std"           # data/ 的上一级即 staging/1802/
TIMEOUT_S = 120          # 顶格点实测 < 0.05 s，120 s 仅作兜底

N_MIN, N_MAX = 2, 500    # 题面 n 范围
P_MAX = 10 ** 9          # 题面 p 上限

# (点号, n, p, 层次说明)
CASES = [
    (1,  2,   1,           "边界层：n=2（题面下界）× p=1（最小有效模数），答案恒 0"),
    (2,  2,   P_MAX,       "边界层：n=2（题面下界）× p=1e9（p 上限）"),
    (3,  3,   P_MAX,       "边界层：最小非平凡 n=3"),
    (4,  4,   10000,       "样例回归：题面【输入样例1】(4 10000)，期望答案 21"),
    (5,  30,  P_MAX,       "小规模顶格：n=30（子任务1上限）× p=1e9"),
    (6,  100, 100000000,   "样例回归+中规模顶格：题面【输入样例2】(100 100000000)，期望答案 3107203"),
    (7,  200, 999999937,   "中大规模顶格：n=200（子任务6上限）× 近上限大质数模"),
    (8,  300, P_MAX,       "大规模：n=300（子任务8档内）× p=1e9"),
    (9,  500, 1,           "顶格+模1：n=500（n上限）× p=1，答案恒 0 的极端"),
    (10, 500, P_MAX,       "顶格：n=500（n上限）× p=1e9（p上限），最坏规模+最大模数"),
]

# 题面明文样例答案（硬编码回归，冲突时以样例为准）
SAMPLE_EXPECT = {4: 21, 6: 3107203}

# ---------------- 自检 1：分层表本身合法 ----------------
assert len(CASES) == 10, "必须恰好 10 个测试点"
assert [c[0] for c in CASES] == list(range(1, 11)), "点号必须为 1..10"
for idx, n, p, _note in CASES:
    assert N_MIN <= n <= N_MAX, "点 %d 的 n=%d 越界" % (idx, n)
    assert 1 <= p <= P_MAX, "点 %d 的 p=%d 越界（正式数据严格 p>=1）" % (idx, p)

if not os.path.exists(STD):
    sys.exit("找不到标程 %s，请先在 staging/1802/ 下编译：g++ -O2 -std=c++17 std.cpp -o std" % STD)

# ---------------- 生成 + 自检 2：文件与答案 ----------------
summary = []
for idx, n, p, note in CASES:
    io = IO(file_prefix="problem", data_id=idx)   # problem{idx}.in / problem{idx}.out
    io.input_writeln(n, p)                       # 单组数据：一行 "n p"
    io.close()                                   # 关键：显式 flush+close，否则 cyaron 写缓冲会留下 0 字节 .in

    in_name, out_name = "problem%d.in" % idx, "problem%d.out" % idx
    # 显式用 subprocess 跑 std 产 .out，并显式 flush/close（规避 cyaron 写缓冲隐患）
    with open(in_name, "rb") as fin, open(out_name, "wb") as fout:
        proc = subprocess.run([STD], stdin=fin, stdout=fout,
                              stderr=subprocess.PIPE, timeout=TIMEOUT_S)
        fout.flush()
        os.fsync(fout.fileno())   # 显式落盘，确保 .out 非空（0 字节即视为生成失败，下面有断言）
    assert proc.returncode == 0, "点 %d：std 退出码 %d，stderr=%r" % (idx, proc.returncode, proc.stderr)

    # 断言 .in 非空且恰一行
    with open(in_name, "rb") as f:
        in_bytes = f.read()
    assert in_bytes == b"%d %d\n" % (n, p), "点 %d：.in 内容异常 %r" % (idx, in_bytes)

    # 断言 .out 非空、恰 1 行、以换行结尾、是十进制整数
    with open(out_name, "rb") as f:
        out_bytes = f.read()
    assert len(out_bytes) > 0, "点 %d：.out 为 0 字节（std 未正常输出）" % idx
    assert out_bytes.endswith(b"\n"), "点 %d：.out 未以换行结尾 %r" % (idx, out_bytes)
    lines = out_bytes.split(b"\n")
    assert len(lines) == 2 and lines[1] == b"", "点 %d：.out 行数 != 1（%r）" % (idx, out_bytes)
    ans = int(lines[0])
    assert 0 <= ans < p, "点 %d：答案 %d 不在 [0, p-1]（p=%d）" % (idx, ans, p)
    if p == 1:
        assert ans == 0, "点 %d：p=1 时答案必须为 0，实得 %d" % (idx, ans)
    if idx in SAMPLE_EXPECT:
        assert ans == SAMPLE_EXPECT[idx], \
            "点 %d：样例答案不符，期望 %d，实得 %d" % (idx, SAMPLE_EXPECT[idx], ans)

    summary.append((idx, n, p, ans, len(in_bytes), len(out_bytes), note))

# ---------------- 自检 3：分层单调/覆盖检查 ----------------
ns = [c[1] for c in CASES]
assert min(ns) == N_MIN and max(ns) == N_MAX, "未覆盖 n 的下界或上限"
assert {30, 100, 200, 500} <= set(ns), "未覆盖全部子任务分档边界"
assert {1, P_MAX} <= {c[2] for c in CASES}, "未覆盖 p 的下界或上限"

print("点  n    p           答案         .in/.out 字节  说明")
for idx, n, p, ans, li, lo, note in summary:
    print("%-3d %-4d %-12d %-11d %-3d/%-3d      %s" % (idx, n, p, ans, li, lo, note))
print("生成完毕：10 组 problemN.in/.out 成对齐全，样例点 4/6 与题面输出逐字一致。")
