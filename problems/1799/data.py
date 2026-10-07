#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一本通 1799《数列》 数据生成器。

分层造 10 组 data/problem1.in ... problem10.in，并用 std 二进制跑出对应 .out。
- 输入只有一行 n（3 <= n <= 10^5000）。
- 用 subprocess 显式调用 ./std 产出 .out（避免写缓冲不 flush 的隐患），
  并断言 .out 非空、行数=1、内容为 [0,1e9+7) 内的整数。
- 另用独立 Python 公式交叉校验 std 输出（非暴力，闭式公式）。

用法：先 g++ -O2 -o std std.cpp，再 python3 data.py
"""
import os
import subprocess
import sys

try:  # Python 3.11+ 默认限制 4300 位十进制字符串转 int
    sys.set_int_max_str_digits(100000)
except AttributeError:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
STD = os.path.join(HERE, "std")
MOD = 10 ** 9 + 7

# ---- 分层用例：边界 / 小 / 中 / 大 / 顶格 / 取模边界 ----
NINES_5000 = "9" * 5000                                   # 10^5000 - 1，5000 位
POW10_5000 = "1" + "0" * 5000                             # 10^5000，顶格（5001 位）
CASES = [
    ("3",                          "最小值边界"),
    ("4",                          "次小"),
    ("10",                         "10% 档上界 n<=10"),
    ("200",                        "30% 档上界 n<=200"),
    ("2000",                       "50% 档上界 n<=2000"),
    ("1000000000000000000",        "70% 档上界 n=10^18"),
    (str(MOD),                     "n ≡ 0 (mod p) 取模边界"),
    (str(MOD - 1 - 1),             "n+1 ≡ 0 (mod p-1) 指数边界"),
    (NINES_5000,                   "5000 位全 9"),
    (POW10_5000,                   "顶格 n=10^5000"),
]


def py_answer(s: str) -> int:
    """独立实现：f(n) = 2^(n+1) - 4n - (n-1)(n-2)  (mod p)。"""
    n = int(s)
    return (pow(2, n + 1, MOD) - 4 * n - (n - 1) * (n - 2)) % MOD


def main() -> int:
    if not os.path.exists(STD):
        print("缺少 std 可执行文件，请先编译 std.cpp", file=sys.stderr)
        return 1
    os.makedirs(DATA, exist_ok=True)

    for i, (n, note) in enumerate(CASES, start=1):
        in_path = os.path.join(DATA, f"problem{i}.in")
        out_path = os.path.join(DATA, f"problem{i}.out")
        with open(in_path, "w") as f:
            f.write(n + "\n")

        with open(in_path, "r") as fin, open(out_path, "w") as fout:
            subprocess.run([STD], stdin=fin, stdout=fout, check=True)
            fout.flush()
            os.fsync(fout.fileno())

        raw = open(out_path).read()
        assert raw.strip() != "", f"problem{i}.out 为空 (n={note})"
        lines = raw.strip().splitlines()
        assert len(lines) == 1, f"problem{i}.out 行数 {len(lines)} != 1"
        got = int(lines[0])
        assert 0 <= got < MOD, f"problem{i}.out 越界: {got}"
        exp = py_answer(n)
        assert got == exp, f"problem{i} 与公式不符: std={got} py={exp}"
        print(f"problem{i}.in/.out OK  ({note})  n 位数={len(n)}  ans={got}")

    print("全部 10 组生成并通过校验。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
