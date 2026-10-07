#!/usr/bin/env python3
# 一本通 1803《列数字》数据生成器
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py
#
# 题面数据范围：1 ≤ N ≤ 1000，单组测试数据（一行一个整数 N）。
# 本题输入就是一个整数 N，答案由 N 唯一确定（无随机结构），故 10 组数据按
# N 的取值分层覆盖：下界 / 小 / 中 / 大 / 顶格，且覆盖不同的答案量级。
#
# 分层设计（10 组）：
#   点 1     下界：N=1，最小输入（答案 1，仅恒等置换）
#   点 2     小：  N=2（答案 2）
#   点 3     小：  N=3（答案 3，最小含合数轮换的规模）
#   点 4     样例：N=10（题面样例，答案 16，用于回归样例）
#   点 5     小：  N=20（答案 70，两位数）
#   点 6     中：  N=100（答案 18663，五位数）
#   点 7     中：  N=300（答案 6 位数）
#   点 8     大：  N=500（答案 10 位数）
#   点 9     顶格-1：N=999（顶格邻域，答案 13 位数）
#   点 10    顶格：N=1000（数据范围上界，答案 3018714402027）
#
# 输出生成：不依赖 cyaron 的 output_gen，直接用 subprocess 跑 std 显式产 .out，
#   避免写缓冲未 flush 导致 0 字节 .out；并对每个 .out 断言非空、格式合法，
#   且与一份独立 Python 实现（素数幂背包 DP）的结果逐点比对。
import os
import subprocess
import sys

STD = os.path.abspath("../std")

# (数据点编号, N)
GROUPS = [
    (1, 1),      # 下界
    (2, 2),      # 小
    (3, 3),      # 小
    (4, 10),     # 题面样例
    (5, 20),     # 小
    (6, 100),    # 中
    (7, 300),    # 中
    (8, 500),    # 大
    (9, 999),    # 顶格邻域
    (10, 1000),  # 顶格（范围上界）
]


def reference_answer(n):
    """独立实现：素数幂背包计数，验证 std 输出。"""
    primes = [x for x in range(2, n + 1)
              if all(x % d for d in range(2, int(x ** 0.5) + 1))]
    dp = [0] * (n + 1)
    dp[0] = 1
    for p in primes:
        pw, q = [], p
        while q <= n:
            pw.append(q)
            q *= p
        nd = dp[:]
        for j in range(n + 1):
            if dp[j]:
                for q in pw:
                    if j + q <= n:
                        nd[j + q] += dp[j]
        dp = nd
    return sum(dp)


def gen(idx, n):
    in_path = f"problem{idx}.in"
    out_path = f"problem{idx}.out"
    with open(in_path, "w", encoding="utf-8") as f:
        f.write(f"{n}\n")
        f.flush()
        os.fsync(f.fileno())
    with open(in_path, "rb") as fin:
        r = subprocess.run([STD], stdin=fin, capture_output=True, timeout=60)
    assert r.returncode == 0, f"problem{idx}: std exit {r.returncode} {r.stderr!r}"
    out = r.stdout.decode().strip()
    assert out != "", f"problem{idx}: empty .out"
    assert out.isdigit(), f"problem{idx}: non-integer .out {out!r}"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out + "\n")
        f.flush()
        os.fsync(f.fileno())
    # 复核：非空、行数=1、与独立实现一致
    raw = open(out_path, "rb").read()
    assert len(raw) > 0, f"problem{idx}: 0-byte .out"
    assert raw.count(b"\n") == 1, f"problem{idx}: line count != 1"
    ref = reference_answer(n)
    assert int(out) == ref, f"problem{idx}: std={out} ref={ref}"
    print(f"problem{idx}: N={n} ans={out} (ref OK, .out {len(raw)} bytes)")


if __name__ == "__main__":
    assert os.path.exists(STD), f"std binary not found: {STD}"
    for idx, n in GROUPS:
        gen(idx, n)
    print(f"ALL {len(GROUPS)} PAIRS OK")
