#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一本通 1808《斐波那契数列》数据生成脚本。

- 分层造 10 组数据（边界 / 小 / 中 / 大 / 顶格；含 -1 与答案<=10^7 的分层点）。
- 用 std.cpp 显式 subprocess 跑出 .out（不用 cyaron，避免 output_gen 不 flush
  导致 0 字节 .out 的隐患），并断言 .out 非空、行数 == 1、内容为整数。
- 自检（非对拍/非暴力）：
    * ans >= 0 时，用 fast doubling 验证 F_ans ≡ a (mod 10^13)（答案合法性）。
    * a = F_k mod 10^13 构造的用例，验证 ans <= k。
    * ans == -1 时，验证 a mod 8 ∈ {4,6}（F_n mod 8 的像为 {0,1,2,3,5,7}，
      4/6 永不出现，属已证的必要条件）。
- 输出目录：本文件同级的 data/，文件名 problem1.in/.out ... problem10.in/.out。
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
STD_CPP = os.path.join(HERE, "std.cpp")
MOD = 10 ** 13


def fib_pair(n, mod=MOD):
    """返回 (F_n, F_{n+1}) mod mod，fast doubling，O(log n)。"""
    if n == 0:
        return (0, 1 % mod)
    a, b = fib_pair(n >> 1, mod)
    c = (a * ((2 * b - a) % mod)) % mod
    d = (a * a + b * b) % mod
    if n & 1:
        return (d, (c + d) % mod)
    return (c, d)


def fib(n, mod=MOD):
    return fib_pair(n, mod)[0]


# ---- 分层用例表：(a, 备注, 构造用的 k 或 None) ------------------------------
F1E6 = fib(10 ** 6)
F1E7 = fib(10 ** 7)
F1E9 = fib(10 ** 9)
CASES = [
    (0,                  "边界：a=0（F_0=0，答案 0）",            None),
    (1,                  "边界/题面样例：a=1 → 1",                None),
    (4,                  "边界 -1：a≡4 (mod 8)，F_n mod 8 像不含 4", None),
    (6,                  "边界 -1：a≡6 (mod 8)，F_n mod 8 像不含 6", None),
    (55,                 "小：a=55=F_10，答案应 ≤ 10",            10),
    (fib(1000),          "小：a=F_1000 mod 1e13，答案应 ≤ 1000",  1000),
    (F1E6,               "中：a=F_10^6 mod 1e13，答案应 ≤ 10^6",  10 ** 6),
    (F1E7,               "中/分层线：a=F_10^7 mod 1e13，答案 ≤ 10^7", 10 ** 7),
    (F1E9,               "大：a=F_10^9 mod 1e13，答案 ≤ 10^9",    10 ** 9),
    (10 ** 13 - 1,       "顶格：a=10^13-1（= -1 mod 1e13）",      None),
]


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    # 编译 std.cpp 到临时路径（编译产物不落在 staging 目录）
    tmpdir = tempfile.mkdtemp(prefix="ybt1808_")
    binary = os.path.join(tmpdir, "std_1808")
    print("[build] g++ -O2 -std=c++17 std.cpp")
    r = subprocess.run(
        ["g++", "-O2", "-std=c++17", "-o", binary, STD_CPP],
        capture_output=True, text=True, timeout=120,
    )
    assert r.returncode == 0, "compile failed:\n" + r.stderr
    print("[build] OK")

    try:
        for idx, (a, note, k) in enumerate(CASES, start=1):
            assert 0 <= a < MOD, f"a out of range: {a}"
            in_path = os.path.join(DATA_DIR, "problem%d.in" % idx)
            out_path = os.path.join(DATA_DIR, "problem%d.out" % idx)

            with open(in_path, "w") as f:
                f.write("%d\n" % a)

            # 显式 subprocess 跑 std 产 .out（规避 cyaron flush 隐患）
            with open(in_path) as fin, open(out_path, "w") as fout:
                pr = subprocess.run(["nice", "-n", "19", binary],
                                    stdin=fin, stdout=fout, timeout=120)
            assert pr.returncode == 0, "std run failed on problem%d" % idx

            # --- .out 断言：非空 + 行数 == 1 + 合法整数 ---
            raw = open(out_path).read()
            assert raw.strip() != "", "problem%d.out is empty" % idx
            lines = [ln for ln in raw.splitlines() if ln.strip() != ""]
            assert len(lines) == 1, \
                "problem%d.out expected 1 line, got %d" % (idx, len(lines))
            ans = int(lines[0].strip())

            # --- 自检 1：正解合法性 F_ans ≡ a (mod 1e13) ---
            if ans >= 0:
                assert ans < 15 * 10 ** 12, "ans out of period"
                assert fib(ans) == a, \
                    "problem%d: F_%d != a" % (idx, ans)
            else:
                assert ans == -1
                # --- 自检 2：-1 的必要条件 a mod 8 ∈ {4,6} ---
                assert a % 8 in (4, 6), \
                    "problem%d: -1 but a%%8=%d not a known non-image" % (idx, a % 8)

            # --- 自检 3：由 a=F_k 构造的用例，答案必须 ≤ k ---
            if k is not None:
                assert ans >= 0 and ans <= k, \
                    "problem%d: ans=%d > k=%d" % (idx, ans, k)

            print("[case %2d] a=%-14d ans=%-14d  %s" % (idx, a, ans, note))
    finally:
        try:
            os.remove(binary)
        except OSError:
            pass
        try:
            os.rmdir(tmpdir)
        except OSError:
            pass
        print("[cleanup] temp binary removed")

    print("[done] 10 cases -> data/problem{1..10}.in/.out")


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
