#!/usr/bin/env python

# 1800 质数 —— 分层测试数据生成器
# 题意：将 1..n 分成尽可能少的集合，使每个集合元素和均为质数；
#       输出最少集合数 cnt 与方案（第 i 个数表示自然数 i 所在集合编号，任意方案），无解输出 -1。
# 数据范围（题面）：30% 的数据 n<=20；100% 的数据 n<=6000。时间 1000 ms / 内存 256 MB。
# 输入仅一行一个正整数 n，故每组数据只需选一个 n，按"分支 + 规模"分层：
#   点1-4 边界层（无解 / cnt=1 / 最小 cnt=2 / 30% 上限）
#   点5-6 最小三集合分支（S 为奇数且 S-2 为合数）
#   点7   中等规模（cnt=2 分支）
#   点8   中大规模（cnt=3 分支）
#   点9   接近上限（cnt=3 分支，卡满筛选上界）
#   点10  顶格（n=6000，S=18003000 为偶数，cnt=2 分支）
# 说明：S = n(n+1)/2；S 为质数 -> cnt=1（仅 n=2）；否则若能写成两质数之和 -> cnt=2；
#       否则 cnt=3（哥德巴赫弱猜想，n>=18 时首现，如 n=18,25,33,...）；n=1 无解。
from cyaron import IO  # 引入CYaRon的库
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "std")            # 标程（../std，已编译）
DATA_DIR = os.path.join(HERE, "data")      # 数据统一放 data/ 子目录

# (n, 层次说明)
CASES = [
    (1,    "边界层：最小 n，S=1 非质数，无解 -> -1"),
    (2,    "边界层：最小 cnt=1（S=3 为质数，全局唯一）"),
    (3,    "边界层：最小 cnt=2（S=6=3+3）"),
    (20,   "边界层：30% 数据上限 n<=20（S=210 为偶数，cnt=2）"),
    (18,   "最小三集合分支：S=171，S-2=169=13^2 为合数，cnt=3"),
    (25,   "三集合分支：S=325，S-2=323=17*19 为合数，cnt=3"),
    (1500, "中等规模：S=1125750 为偶数，cnt=2"),
    (3002, "中大规模三集合分支：S=4507503 为奇数，cnt=3"),
    (5998, "接近上限的三集合分支：S=17991001，cnt=3（筛到 1.8e7 量级）"),
    (6000, "顶格层：n 取题面上限，S=18003000 为偶数，cnt=2"),
]


def sieve(limit):
    """埃氏筛，返回 bool 列表（is_prime）。"""
    isp = bytearray([1]) * (limit + 1)
    isp[0] = isp[1] = 0
    i = 2
    while i * i <= limit:
        if isp[i]:
            isp[i * i::i] = bytearray(len(range(i * i, limit + 1, i)))
        i += 1
    return isp


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.chdir(DATA_DIR)

    if not os.path.exists(STD):
        sys.exit("标程未找到：%s（请先 g++ -O2 -std=c++17 -o std std.cpp）" % STD)

    for i, (n, note) in enumerate(CASES, 1):
        io = IO(file_prefix="problem", data_id=i)   # problem{i}.in / problem{i}.out
        io.input_writeln(n)
        # 显式 flush + close，避免 cyaron 写缓冲导致 .in 为空 / 0 字节
        io.input_file.flush()
        io.input_file.close()
        if io.output_file is not None:
            io.output_file.close()

        inp, outp = io.input_filename, io.output_filename
        # 用 subprocess 显式跑 std 产出 .out（不依赖 output_gen 的内部缓冲）
        with open(inp, "rb") as fi, open(outp, "wb") as fo:
            subprocess.run([STD], stdin=fi, stdout=fo, check=True, timeout=60)

        # ---- 断言：输入正确落盘 ----
        with open(inp, "r") as f:
            raw_in = f.read()
        assert raw_in == "%d\n" % n, "点%d .in 内容异常: %r" % (i, raw_in)

        # ---- 断言：输出非空、行数/列数符合预期 ----
        with open(outp, "r") as f:
            raw_out = f.read()
        assert raw_out.strip() != "", "点%d .out 为空（0 字节或全空白）" % i
        lines = [ln for ln in raw_out.split("\n") if ln.strip() != ""]

        if n == 1:
            # 唯一无解点：只有一行 -1
            assert len(lines) == 1 and lines[0].strip() == "-1", "点%d 无解输出异常: %r" % (i, raw_out)
            print("problem%d: n=%d -> -1  (%s)" % (i, n, note))
            continue

        assert len(lines) == 2, "点%d 期望 2 行，实际 %d 行" % (i, len(lines))
        cnt = int(lines[0])
        nums = list(map(int, lines[1].split()))
        assert cnt in (1, 2, 3), "点%d cnt=%d 越界" % (i, cnt)
        assert len(nums) == n, "点%d 方案元素数 %d != n=%d" % (i, len(nums), n)
        assert all(1 <= v <= cnt for v in nums), "点%d 存在越界集合编号" % i

        # 每组集合和必须为质数，且不能有空集合
        sums = [0] * (cnt + 1)
        for idx, v in enumerate(nums, 1):
            sums[v] += idx
        assert all(sums[g] > 0 for g in range(1, cnt + 1)), "点%d 存在空集合" % i
        S = n * (n + 1) // 2
        isp = sieve(S)
        assert all(isp[sums[g]] for g in range(1, cnt + 1)), \
            "点%d 集合和非质数: %s" % (i, sums[1:])
        assert sum(sums[1:]) == S
        print("problem%d: n=%d -> cnt=%d sums=%s  (%s)" % (i, n, cnt, sums[1:], note))

    print("生成完成：data/problem1.in/.out ... data/problem10.in/.out（10 组，全部断言通过）")


if __name__ == "__main__":
    main()
