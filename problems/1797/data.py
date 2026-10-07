#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 一本通 1797《K维斐波那契》数据生成器
#
# 题意：F(1)=F(2)=1, F(i)=F(i-1)+F(i-2)；A 为 n^k 的 k 维超立方体，
#       A(i_1..i_k)=F(i_1+...+i_k-k+1)，求所有元素之和 mod 1e9+7。
#       输入第一行 T，接下来 T 行每行 n k；每组输出一行答案。
# 数据范围（题面【提示】）：T<=100，n,k<=10^9；
#       20% 数据 n,k<=5；另有 20% 数据 k=1；60% 数据 k<=100。
#
# 运行方式：本脚本放在 staging/1797/，在 data/ 子目录内执行：
#       cd data && python3 ../data.py
#   标程二进制 ../std 由 `g++ -O2 -o std std.cpp` 生成。
#
# ⚠ cyaron output_gen 的写缓冲隐患规避：
#   本脚本对每组先写 .in，再调用 io.output_gen("../std")（该实现内部会先 flush 输入文件，
#   再以 subprocess 方式显式运行 std 并把 stdout 落到 .out）。
#   ★ 实测该版本 cyaron 的 output_gen 写完后**不 flush output_file**，同进程内立即读取会
#     读到 0 字节——故本脚本在 output_gen 之后显式执行 io.output_file.flush()（双保险：
#     读文件前再 os.fsync 一次），随后**显式断言**：
#     - .in 非空、行数 == 1+T；
#     - .out 非空、行数 == T（本题每组必有输出，无空输出点）；
#     - 每行输出均为非负整数（模意义下）。
#   任何断言失败即抛错中止，杜绝 0 字节 .out 静默通过。
#
# 分层设计（10 组）：
#   点 1   边界层   ：题面样例 T=3，(2,2)(4,1)(1,3) → 期望 5 7 1
#   点 2   边界层   ：n=1,k=1 的最小非退化点（唯一元素 F(1)=1）
#   点 3   边界层   ：n=1,k=1e9（k 顶格但维度退化，仍只有 1 个元素，答案 1）
#   点 4   边界层   ：k=1,n=1e9（“另有 20% 数据 k=1” 的顶格，答案 = ΣF(i) = F(n+2)-1）
#   点 5   小规模层 ：T=5，n,k∈[1,5]（对应 “20% 数据 n,k<=5”）
#   点 6   中规模层 ：T=20，k=1，n∈[1,1e9] 随机（k=1 层大规模，卡 n 顶格）
#   点 7   中规模层 ：T=100，n∈[1,1000]，k∈[1,100]（对应 “60% 数据 k<=100”，T 顶格）
#   点 8   中规模层 ：T=50，n,k∈[1,1000] 随机
#   点 9   大规模层 ：T=100，n,k∈[1,1e9] 全区间随机（T 顶格 + 值域顶格）
#   点 10  顶格层   ：T=100，n=k=1e9（T、n、k 三者同时顶格）
#
# 备注：本题输入规模极小（每组仅两个整数），不存在数组上限/内存问题；
#       所有点 std 均在毫秒级跑完，无性能风险。

from cyaron import IO  # 引入CYaRon的库
import os
import random

random.seed(1797)  # 固定种子，便于复现

NMAX = 10 ** 9  # 题面上限


def write_case(i, pairs, note):
    """写出第 i 组：第一行 T，接下来 T 行 n k。用 ../std 生成 .out 并做断言。"""
    io = IO(file_prefix="problem", data_id=i)  # problem{i}.in / problem{i}.out
    io.input_writeln(len(pairs))
    for (n, k) in pairs:
        io.input_writeln(n, k)
    io.output_gen("../std")  # 内部先 flush 输入，再 subprocess 运行 std
    io.output_file.flush()   # ★ 关键：output_gen 不 flush，必须显式落盘
    os.fsync(io.output_file.fileno())

    with open("problem%d.in" % i, encoding="utf-8") as f:
        in_text = f.read()
    in_lines = [ln for ln in in_text.split("\n") if ln.strip() != ""]

    with open("problem%d.out" % i, encoding="utf-8") as f:
        out_text = f.read()
    out_lines = [ln for ln in out_text.split("\n") if ln.strip() != ""]

    # ---- 断言：.in 结构正确 ----
    assert in_text.strip() != "", "problem%d.in 为空（0 字节风险）" % i
    assert len(in_lines) == len(pairs) + 1, \
        "problem%d.in 行数 %d != 1+T(%d)" % (i, len(in_lines), len(pairs) + 1)
    assert int(in_lines[0].strip()) == len(pairs), \
        "problem%d.in 首行 T 与数据组数不符" % i

    # ---- 断言：.out 非空且行数 == T（本题无空输出点） ----
    assert out_text.strip() != "", "problem%d.out 为空（0 字节风险）" % i
    assert len(out_lines) == len(pairs), \
        "problem%d.out 行数 %d != T(%d)" % (i, len(out_lines), len(pairs))
    for ln in out_lines:
        assert ln.strip().isdigit(), "problem%d.out 含非数字输出: %r" % (i, ln)
        assert 0 <= int(ln.strip()) < 10 ** 9 + 7, \
            "problem%d.out 越界（应 <1e9+7）: %r" % (i, ln)

    head = " ".join(out_lines[:6]) + (" ..." if len(out_lines) > 6 else "")
    print("problem%-2d: T=%-3d ans[first]=%-20s -- %s" % (i, len(pairs), head, note))


# ---- 点 1：边界层（题面样例），期望 5 / 7 / 1 ----
write_case(1, [(2, 2), (4, 1), (1, 3)],
           "边界层：题面样例 T=3，(2,2)(4,1)(1,3) 期望 5 7 1")

# ---- 点 2：边界层 n=1,k=1（唯一元素 F(1)=1） ----
write_case(2, [(1, 1)], "边界层：n=1,k=1，唯一元素 F(1)=1")

# ---- 点 3：边界层 n=1,k=1e9（k 顶格，维度退化） ----
write_case(3, [(1, NMAX)],
           "边界层：n=1,k=1e9（k 顶格、维度退化），答案仍为 1")

# ---- 点 4：边界层 k=1,n=1e9（“另有 20% 数据 k=1” 顶格） ----
write_case(4, [(NMAX, 1)],
           "边界层：k=1,n=1e9（k=1 层顶格），答案 = ΣF(i) = F(n+2)-1")

# ---- 点 5：小规模层（20% 数据 n,k<=5） ----
small = [(random.randint(1, 5), random.randint(1, 5)) for _ in range(5)]
write_case(5, small, "小规模层：T=5，n,k∈[1,5]（20% 数据 n,k<=5）")

# ---- 点 6：中规模层 k=1，n 全区间随机（20 组） ----
k1 = [(random.randint(1, NMAX), 1) for _ in range(20)]
k1[0] = (1, 1)                 # 混入最小边界
k1[-1] = (NMAX, 1)             # 混入 n 顶格
write_case(6, k1, "中规模层：T=20，k=1，n∈[1,1e9] 随机（含 n=1 与 n=1e9 边界）")

# ---- 点 7：中规模层 k<=100（60% 数据），T 顶格 ----
k100 = [(random.randint(1, 1000), random.randint(1, 100)) for _ in range(100)]
write_case(7, k100, "中规模层：T=100（顶格），n∈[1,1000]，k∈[1,100]（60% 数据 k<=100）")

# ---- 点 8：中规模层 n,k∈[1,1000] 随机 ----
mid = [(random.randint(1, 1000), random.randint(1, 1000)) for _ in range(50)]
write_case(8, mid, "中规模层：T=50，n,k∈[1,1000] 随机")

# ---- 点 9：大规模层 n,k 全区间随机（T 顶格） ----
big = [(random.randint(1, NMAX), random.randint(1, NMAX)) for _ in range(100)]
write_case(9, big, "大规模层：T=100，n,k∈[1,1e9] 全区间随机（T 与值域均顶格）")

# ---- 点 10：顶格层 n=k=1e9，T 顶格 ----
write_case(10, [(NMAX, NMAX)] * 100,
           "顶格层：T=100，n=k=1e9（T、n、k 三者同时顶格）")
