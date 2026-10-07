#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 2110《【例5.1】素数环》数据生成器（cyaron，仓库惯例）
#
# 题意：输入正整数 n（题面范围 4 <= n <= 30），把 1..n 组成一个环，使相邻两个整数
#       之和均为素数；输出任意一个满足条件的环（单行 n 个数，空格分隔）。
#       无解时（奇数 n：1..n 中奇数比偶数多一个，环上必有"奇+奇"相邻，其和为偶数 > 2，
#       不是素数 ⇒ 无解），三个主流实现 [1][2][3] 都**不输出任何内容**（0 字节 .out），
#       本包与之保持一致。
#
# 输出顺序约定（关键，已逐字节核对题面样例）：
#   主流写法（a[1]=1 固定、候选递增、首个解）对 n=6 得 `1 4 3 2 5 6`，题面样例是它的
#   循环移位/同构读法 `4 3 2 5 6 1`（本质同一个环；题面只要求"组成一个环"，无起点方向
#   语义）。std.cpp 采用等价写法（末位固定 1、首位从 2 起递增），对 n=6 输出与样例逐字节
#   一致；对全部偶数 n∈[4,30] 与主流首解旋转移位后完全一致（本脚本内逐组断言）。
#
# 分层设计（10 组 .in）：
#   点  层            n    设计意图
#   --  -----------  ---  ------------------------------------------------------------
#   1   边界·最小 n   4    题面下界；最小合法环（1 2 3 4 的同构写法），可手算验证
#   2   边界·无解     5    最小的奇数 n ⇒ 无解；官方约定输出为空（0 字节），
#                          卡"奇数直接乱输出/死循环"的实现
#   3   题面样例      6    题面【输入样例】原样；.out 必须逐字节等于 `4 3 2 5 6 1`
#   4   小规模        8    小规模偶数，可手算展开验证
#   5   小规模       10    小规模偶数
#   6   中等         14    中等规模
#   7   中等         20    中等规模
#   8   大规模       26    接近上限（1..30 中除 28/30 外最大偶数，含 26=13+13 需排除自加）
#   9   边界·无解    29    最大奇数 n（题面上界 30 内的奇数上界）⇒ 无解，空 .out
#   10  顶格         30    题面上限；标程最坏搜索规模
#
# 生成方式：cyaron IO(file_prefix="problem", data_id=i) + io.output_gen(std 绝对路径)，
#   产出 problem1.in/.out ... problem10.in/.out。每个点规模固定、无随机量 ⇒ 天然可复现。
#   运行位置：建议在 data/ 下运行 `python3 ../data.py`（或任意 cwd，脚本会自行定位 std 与 data/）。
#
# ⚠ 防 cyaron 静默 0 字节 .out 的三重防护（本脚本内建）：
#   ① 启动先断言 std 存在且可执行（脚本同目录），并用题面样例（n=6）实跑，必须逐字节等于
#      `4 3 2 5 6 1\n`，否则直接 SystemExit(1)；
#   ② 每组生成后回读 .in/.out，断言 .in 恰一行整数、.out 非空（偶数点）/为空（奇数点）、
#      行数符合预期（偶数点恰 1 行）；
#   ③ 用**独立的纯 Python 参考实现**（主流写法：a[1]=1 固定 + 候选递增 + 首个解，
#      再做旋转移位；与 std.cpp 的"末位固定 1"搜索序完全不同的一条代码路径）复算，
#      逐字节比对 std 的 .out；顺带校验环合法性（1..n 的排列 + 相邻含首尾和为素数）。

import os
import sys

from cyaron import IO

MINN, MAXN = 4, 30           # 题面数据范围
SAMPLE_N = 6                 # 题面【输入样例】
SAMPLE_OUT = "4 3 2 5 6 1"   # 题面【输出样例】

# --------------------------------------------------------------------------
# 独立的纯 Python 参考实现（主流约定 → 与 std 同构）
# --------------------------------------------------------------------------
def _sieve(limit):
    is_p = [True] * (limit + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if is_p[i]:
            for j in range(i * i, limit + 1, i):
                is_p[j] = False
    return is_p


ISPRIME = _sieve(2 * MAXN + 2)


def mainstream_first_solution(n):
    """主流写法：a[1]=1 固定、候选 1..n 递增、找到首个完整环即返回（纯 Python 递归）。"""
    path = [1]
    used = {1}

    def dfs():
        if len(path) == n:
            return ISPRIME[path[-1] + path[0]]
        for v in range(1, n + 1):
            if v not in used and ISPRIME[path[-1] + v]:
                used.add(v)
                path.append(v)
                if dfs():
                    return True
                path.pop()
                used.remove(v)
        return False

    if dfs():
        return path[:]
    return None


def reference_solution(n):
    """参考输出：主流首解做左旋一位（1 移到末尾），与 std.cpp 的搜索序等价。

    奇数 n 直接返回 None（无解）：奇环无法奇偶交替 ⇒ 不存在合法环；若不短路，
    纯 Python 的穷举 DFS 在 n=29 上会指数级挂死。"""
    if n % 2 == 1:
        return None
    sol = mainstream_first_solution(n)
    if sol is None:
        return None
    return sol[1:] + sol[:1]


def is_valid_ring(n, seq):
    """校验 seq 是 1..n 的排列且相邻（含首尾）之和均为素数。"""
    if sorted(seq) != list(range(1, n + 1)):
        return False, "不是 1..n 的排列"
    L = len(seq)
    for i in range(L):
        if not ISPRIME[seq[i] + seq[(i + 1) % L]]:
            return False, "相邻和 %d+%d 非素数" % (seq[i], seq[(i + 1) % L])
    return True, "ok"


# --------------------------------------------------------------------------
# 防护 ①：std 必须存在 + 题面样例实跑
# --------------------------------------------------------------------------
def preflight():
    std = os.path.join(os.path.dirname(os.path.abspath(__file__)), "std")
    if not (os.path.isfile(std) and os.access(std, os.X_OK)):
        sys.exit("FATAL: 标程不存在或不可执行：%s（先 g++ -O2 -std=c++17 std.cpp -o std）" % std)
    import subprocess
    for n in (SAMPLE_N,):
        out = subprocess.run([std], input="%d\n" % n, capture_output=True,
                             text=True, timeout=10).stdout
    if out != SAMPLE_OUT + "\n":
        sys.exit("FATAL: 标程对样例 n=%d 输出 %r，与题面样例 %r 不一致" % (n, out, SAMPLE_OUT + "\n"))
    return std


# --------------------------------------------------------------------------
# 10 个测试点：n 固定、无随机量
# --------------------------------------------------------------------------
POINTS = [
    (1, 4,  "边界层·最小 n；最小合法环，可手算验证"),
    (2, 5,  "边界层·无解（最小奇数 n）；官方约定输出为空"),
    (3, 6,  "题面【输入样例】原样；.out 须逐字节等于 4 3 2 5 6 1"),
    (4, 8,  "小规模偶数，可展开验证"),
    (5, 10, "小规模偶数"),
    (6, 14, "中等规模"),
    (7, 20, "中等规模"),
    (8, 26, "大规模·接近上限"),
    (9, 29, "边界层·无解（题面上界内的最大奇数）"),
    (10, 30, "顶格层·题面上限"),
]


def find_data_dir():
    """数据落在当前工作目录（约定在 data/ 下运行）；否则退回脚本旁的 data/。"""
    if os.path.exists(os.path.join(os.getcwd(), "problem1.in")):
        return os.getcwd()
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def main():
    std = preflight()

    for i, n, _note in POINTS:
        io = IO(file_prefix="problem", data_id=i)   # problem<i>.in / problem<i>.out
        io.input_write(n, "\n")                     # 单行 n
        # 用 std 的**绝对路径**（不依赖 cwd，避免 ../std 找不到时 cyaron 静默产出 0 字节）
        io.output_gen(std, time_limit=10)           # 标程产出答案（超时即报错，不静默）
        io.close()                                  # 显式关闭，确保 .in/.out 落盘

    data_dir = find_data_dir()
    problems = []

    def check(cond, msg):
        if not cond:
            problems.append(msg)

    print("点   层/意图                        n   期望输出                 .out 字节  校验")
    for i, n, note in POINTS:
        in_path = os.path.join(data_dir, "problem%d.in" % i)
        out_path = os.path.join(data_dir, "problem%d.out" % i)
        raw_in = open(in_path, "r", encoding="utf-8", newline="").read()
        raw_out = open(out_path, "r", encoding="utf-8", newline="").read()

        # (1) 输入格式：恰一行 `n` + 换行
        check(raw_in == "%d\n" % n, "点 %d：.in=%r 应为 %r" % (i, raw_in, "%d\n" % n))

        # (2) 期望输出：独立参考实现（偶数 ⇒ 一行 n 个数；奇数 ⇒ 空）
        ref = reference_solution(n)
        if ref is None:
            want = ""
        else:
            want = " ".join(str(x) for x in ref) + "\n"
        check(raw_out == want,
              "点 %d：std 输出 %r != 独立参考实现 %r（n=%d）" % (i, raw_out, want, n))

        # (3) 行数/非空/排列与素数环合法性
        if ref is None:
            check(raw_out == "", "点 %d：奇数 n=%d 应为空输出，实际 %r" % (i, n, raw_out))
            verdict = "空输出=无解（规范 [1][2][3]）"
        else:
            check(raw_out.endswith("\n") and raw_out.count("\n") == 1,
                  "点 %d：偶数点应恰 1 行（含行末换行），实际换行数 %d" % (i, raw_out.count("\n")))
            check(raw_out.strip() != "", "点 %d：偶数点 .out 不得为空" % i)
            nums = [int(t) for t in raw_out.split()]
            check(len(nums) == n, "点 %d：应为 %d 个数，实际 %d" % (i, n, len(nums)))
            ok, why = is_valid_ring(n, nums)
            check(ok, "点 %d：std 输出不是合法素数环（%s）" % (i, why))
            verdict = "合法环·与参考逐字节一致"

        print("%2d   %-30s %3d  %-22s %6d    %s" %
              (i, note, n,
               (SAMPLE_OUT if i == 3 else (want.strip()[:20] if want else "(空)")),
               len(raw_out.encode("utf-8")), verdict))

    # (4) 分层结构断言
    check(POINTS[0][1] == MINN and POINTS[-1][1] == MAXN, "首点应为最小 n=4、末点应为顶格 n=30")
    check(any(n % 2 == 1 for _, n, _ in POINTS), "缺少奇数（无解）测试点")
    check(any(n == SAMPLE_N for _, n, _ in POINTS), "缺少题面样例点 n=6")
    for _, n, _ in POINTS:
        check(MINN <= n <= MAXN, "点 n=%d 超出题面范围 [4,30]" % n)

    # (5) std 对题面范围内全部取值的行为自检（全覆盖，与测试点无关）
    import subprocess
    std = os.path.join(os.path.dirname(os.path.abspath(__file__)), "std")
    if not (os.path.isfile(std) and os.access(std, os.X_OK)):
        sys.exit("FATAL: 自检阶段找不到标程（preflight 通过而这里失败，不应发生）")
    for n in range(MINN, MAXN + 1):
        out = subprocess.run([std], input="%d\n" % n, capture_output=True,
                             text=True, timeout=10).stdout
        if n % 2 == 1:
            check(out == "", "自检：奇数 n=%d 应为空输出，实际 %r" % (n, out))
        else:
            nums = [int(t) for t in out.split()]
            ok, why = is_valid_ring(n, nums)
            check(ok, "自检：n=%d 输出不是合法素数环（%s）" % (n, why))
            ref = reference_solution(n)
            check(out == " ".join(str(x) for x in ref) + "\n",
                  "自检：n=%d 与独立参考实现不一致" % n)
    print("\n全覆盖自检：n=4..30 共 27 个取值，偶数点合法环、奇数点空输出、全部与独立参考一致。")

    if problems:
        print("\n自检失败：", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        raise SystemExit(1)
    print("自检全部通过：10/10 组 .in/.out 成对；样例逐字节一致；格式/合法性/独立参考复算均通过。")


if __name__ == "__main__":
    main()
