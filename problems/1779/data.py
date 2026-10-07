#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
一本通 1779《第K小数》 测试数据生成器（cyaron）。

题意：给一个长度 <=17、由 '0'~'9' 组成、无前导零的字符串 S，求「用 S 中数字的所有排列
      构成的、无前导零且能被 17 整除的整数」中第 K 小的那个。K <= 17!，数据保证有解。

数据范围（content.md【提示】/ 官方 OJ 页）：
  40%  : |S| <= 12, K <= 2*10^6
  100% : |S| <= 17, K <= 17!
本包 10 个点全部按 |S| <= 17 的**题面上限**设计，数字集 [0-9]，S 无前导零（题面要求）。

分层（从最小铺到顶格）：
  点 1  边界层  n=2 最小规模（也是原题样例 1：17 1 -> 17），唯一合法排列
  点 2  边界层  题面【输入样例】原样：2242223 2 -> 2242232
  点 3  边界层  n=2 且唯一合法排列恰是字典序最大者（51 1 -> 51）
  点 4  小规模  n=6..8 随机数字，K 随机小值（可手算量级）
  点 5  小规模  n=8..10 随机，K 取总合法数附近（卡「贪心边界」）
  点 6  中等    n=12（40% 档 |S| 上界），K = min(2*10^6, 总合法数)（40% 档 K 上界）
  点 7  中等    n=12，K = 总合法数（该规模最大 K）
  点 8  大规模  n=15 随机，K 随机大值
  点 9  顶格    n=17 随机，K=1（最小排列）
  点 10 顶格    n=17 且数字只取 {0,1,2}（大量重复数字），K = 总合法数（最大 K）
               —— 同时压「不同字符串去重计数」与「K 取上界」

生成方式：cyaron IO(file_prefix="problem", data_id=i) 写 problemI.in，
          .out 由 subprocess **显式调用 std** 生成（规避 cyaron output_gen 的
          「写缓冲未 flush 产生 0 字节 .out」隐患），并断言 .out 非空、恰 1 行、
          与独立 Python 参考实现逐字节一致，且答案满足「长度=n / 无前导零 / 被 17 整除」。
每个随机点用独立随机种子，可复现。
"""

import os
import random
import subprocess
import sys

from cyaron import IO  # 引入 CYaRon 的库

MOD = 17
INV10 = 12  # 10 * 12 = 120 ≡ 1 (mod 17)

# ---------------------------------------------------------------------------
# 独立 Python 参考实现（与 std.cpp 的 C++ 实现路径不同，用于选 K 与复核 .out）
#   H(c)[t] = 用数字重数 c 能拼出的**不同字符串**中，数值 ≡ t (mod 17) 的个数
# ---------------------------------------------------------------------------
_memo = {}


def H(c):
    key = tuple(c)
    v = _memo.get(key)
    if v is not None:
        return v
    if sum(c) == 0:
        res = [0] * MOD
        res[0] = 1
    else:
        res = [0] * MOD
        for d in range(10):
            if c[d] == 0:
                continue
            c2 = list(c)
            c2[d] -= 1
            sub = H(c2)
            for t in range(MOD):
                res[t] += sub[((t - d) % MOD) * INV10 % MOD]
    _memo[key] = res
    return res


def _pow10mod(n):
    p = [1] * (n + 1)
    for i in range(1, n + 1):
        p[i] = p[i - 1] * 10 % MOD
    return p


def total_valid(s):
    """S 的合法排列（无前导零且被 17 整除）总数。"""
    n = len(s)
    c = [0] * 10
    for ch in s:
        c[int(ch)] += 1
    pw = _pow10mod(n)
    tot = 0
    for d in range(1, 10):
        if c[d] == 0:
            continue
        c[d] -= 1
        need = ((MOD - d) % MOD) * pw[n - 1] % MOD
        tot += H(c)[need]
        c[d] += 1
    return tot


def kth(s, K):
    """S 的第 K 小合法排列。"""
    n = len(s)
    c = [0] * 10
    for ch in s:
        c[int(ch)] += 1
    pw = _pow10mod(n)
    out = []
    p = 0
    for i in range(n):
        m = sum(c)
        for d in range(10):
            if c[d] == 0:
                continue
            if i == 0 and d == 0:
                continue
            np = (p * 10 + d) % MOD
            need = ((MOD - np) % MOD) * pw[m - 1] % MOD
            c[d] -= 1
            cnt = H(c)[need]
            c[d] += 1
            if K > cnt:
                K -= cnt
            else:
                out.append(str(d))
                p = np
                c[d] -= 1
                break
    return "".join(out)


# ---------------------------------------------------------------------------
# 随机 S：首位非零、合法排列数 >= 1（否则重抽）
# ---------------------------------------------------------------------------
def rand_s(n, rng, digits=range(10), tries=20000):
    digs = list(digits)
    first = [d for d in digs if d != 0]
    for _ in range(tries):
        s = [str(rng.choice(digs)) for _ in range(n)]
        s[0] = str(rng.choice(first))
        s = "".join(s)
        t = total_valid(s)
        if t >= 1:
            return s, t
    raise RuntimeError("无法为 n=%d 抽到有解的 S" % n)


# ---------------------------------------------------------------------------
# 10 个测试点
# ---------------------------------------------------------------------------
def build_point(i):
    rng = random.Random(1779 + i)  # 每点独立种子，可复现

    if i == 1:  # 边界层：最小规模（原题样例 1）
        return "17", 1, "边界层：n=2 最小规模，唯一合法排列 17（原题样例 1：17 1）"

    if i == 2:  # 边界层：题面样例原样
        return "2242223", 2, "边界层：题面【输入样例】原样 2242223 2 -> 2242232"

    if i == 3:  # 边界层：唯一解且为最大排列
        return "51", 1, "边界层：n=2 且唯一合法排列恰为字典序最大者（51 1 -> 51）"

    if i == 4:  # 小规模随机
        s, t = rand_s(rng.randint(6, 8), rng)
        K = rng.randint(1, t)
        return s, K, "小规模随机：n=%d，K=%d（总合法数 %d，量级可手算）" % (len(s), K, t)

    if i == 5:  # 小规模随机，K 取尾部
        s, t = rand_s(rng.randint(8, 10), rng)
        K = rng.randint(max(1, t - 3), t)
        return s, K, "小规模随机：n=%d，K=%d（贴近上界，总合法数 %d）" % (len(s), K, t)

    if i == 6:  # 中等，40% 档上界
        s, t = rand_s(12, rng)
        K = min(2 * 10 ** 6, t)
        return s, K, "中等规模：n=12（40%% 档 |S| 上界），K=min(2e6,总合法数)=%d" % K

    if i == 7:  # 中等，K 取最大
        s, t = rand_s(12, rng)
        return s, t, "中等规模：n=12，K=总合法数=%d（该规模最大 K）" % t

    if i == 8:  # 大规模随机
        s, t = rand_s(15, rng)
        K = rng.randint(1, t)
        return s, K, "大规模随机：n=15，K=%d（总合法数 %d）" % (K, t)

    if i == 9:  # 顶格，K=1
        s, t = rand_s(17, rng)
        return s, 1, "顶格层：n=17，K=1（最小排列，总合法数 %d）" % t

    if i == 10:  # 顶格，数字重复多，K 取最大
        s, t = rand_s(17, rng, digits=range(3))
        return s, t, "顶格层：n=17 且数字仅取 {0,1,2}（大量重复），K=总合法数=%d（去重计数 + K 上界）" % t

    raise ValueError("未知测试点 %d" % i)


# ---------------------------------------------------------------------------
def main():
    here = os.path.dirname(os.path.abspath(__file__))
    std_path = os.path.join(here, "std")
    data_dir = os.path.join(here, "data")
    os.makedirs(data_dir, exist_ok=True)

    if not os.path.exists(std_path):
        raise SystemExit("找不到 std 可执行文件，请先编译：g++ -O2 -std=c++17 -o std std.cpp")

    os.chdir(data_dir)  # cyaron IO 在当前目录下产出 problemI.in

    plan = []
    for i in range(1, 11):
        s, K, note = build_point(i)
        t = total_valid(s)
        assert 1 <= K <= t, "点 %d：K=%d 超出 [1,%d]" % (i, K, t)

        io = IO(file_prefix="problem", data_id=i)
        io.input_write("%s %d\n" % (s, K))
        io.close()  # 确保 .in 落盘

        in_path = "problem%d.in" % i
        out_path = "problem%d.out" % i
        with open(in_path, "rb") as f:
            raw_in = f.read()
        # 用 subprocess 显式跑 std 产出 .out（避免 cyaron output_gen 缓冲未 flush 的 0 字节隐患）
        r = subprocess.run([std_path], input=raw_in, stdout=subprocess.PIPE, timeout=120)
        assert r.returncode == 0, "点 %d：std 退出码 %d" % (i, r.returncode)
        out = r.stdout
        with open(out_path, "wb") as f:
            f.write(out)

        plan.append((i, s, K, t, note, raw_in, out))

    # ---------------- 生成后自检 ----------------
    problems = []

    def check(cond, msg):
        if not cond:
            problems.append(msg)

    print("点   n  |S|                K              总合法数      答案                说明")
    for (i, s, K, t, note, raw_in, out) in plan:
        out_txt = out.decode("utf-8", "replace")
        # (1) .in 内容与构造一致（恰好一行 "S K" + 换行）
        check(raw_in == ("%s %d\n" % (s, K)).encode(), "点 %d：.in 与构造不一致" % i)
        check(raw_in.count(b"\n") == 1, "点 %d：.in 行数不为 1" % i)
        # (2) .out 非空且恰 1 行
        check(len(out) > 0, "点 %d：.out 为空（0 字节）" % i)
        check(out_txt.endswith("\n") and out_txt.count("\n") == 1,
              "点 %d：.out 应为单行且带换行" % i)
        ans = out_txt.strip()
        # (3) 答案结构性校验：长度=n、无前导零、被 17 整除
        check(len(ans) == len(s), "点 %d：答案长度 %d != n=%d" % (i, len(ans), len(s)))
        check(not (len(ans) > 1 and ans[0] == "0"), "点 %d：答案有前导零" % i)
        check(ans != "" and ans.isdigit() and int(ans) % 17 == 0, "点 %d：答案不能被 17 整除" % i)
        check(sorted(ans) == sorted(s), "点 %d：答案数字多重集合 != S" % i)
        # (4) 与独立 Python 参考实现逐字节比对
        exp = kth(s, K) + "\n"
        check(out_txt == exp, "点 %d：std 输出 %r != 参考 %r" % (i, out_txt, exp))
        # (5) K 范围
        check(1 <= K <= t, "点 %d：K 越界" % i)

        print("%2d  %2d  %-17s %-15d %-13d %-19s %s"
              % (i, len(s), s, K, t, ans, note))

    # ---------------- 分层结构性断言 ----------------
    check(plan[0][1] == "17" and plan[0][2] == 1, "点 1 应为最小规模 17 1")
    check(plan[1][1] == "2242223" and plan[1][2] == 2, "点 2 应为题面样例")
    check(plan[1][6].decode().strip() == "2242232", "点 2 答案应为 2242232")
    check(plan[2][1] == "51" and plan[2][6].decode().strip() == "51", "点 3 应为 51 -> 51")
    check(6 <= len(plan[3][1]) <= 8, "点 4 不是小规模 n=6..8")
    check(8 <= len(plan[4][1]) <= 10, "点 5 不是小规模 n=8..10")
    check(len(plan[5][1]) == 12 and plan[5][2] == min(2 * 10 ** 6, plan[5][3]),
          "点 6 应为 n=12 且 K=min(2e6,总数)")
    check(len(plan[6][1]) == 12 and plan[6][2] == plan[6][3], "点 7 应为 n=12 且 K=总数")
    check(len(plan[7][1]) == 15, "点 8 应为 n=15")
    check(len(plan[8][1]) == 17 and plan[8][2] == 1, "点 9 应为 n=17 且 K=1")
    check(len(plan[9][1]) == 17 and plan[9][2] == plan[9][3], "点 10 应为 n=17 且 K=总数")
    check(set(plan[9][1]) <= {"0", "1", "2"}, "点 10 数字应仅取 {0,1,2}")

    if problems:
        print("\n自检失败：", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        raise SystemExit(1)
    print("\n自检全部通过：10/10 组 .in/.out 成对且非空，答案满足「长度=n / 无前导零 / 被 17 整除 /"
          " 数字多重集合=S」，并与独立 Python 参考实现逐字节一致。")


if __name__ == "__main__":
    main()
