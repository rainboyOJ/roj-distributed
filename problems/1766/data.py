#!/usr/bin/env python3
# 一本通 1766《成绩单》 分层数据生成器
# ---------------------------------------------------------------------------
# 同源原题: 洛谷 P5336 [THUSC 2016] 成绩单 (题面与本目录 content.md 逐字一致,
#   已实抓 https://www.luogu.com.cn/problem/P5336 核对)。标程来源见 std.cpp 头注。
#
# 数据范围 (题面): 100% 数据 n<=50, a<=100, b<=10, w_i<=1000。
#   （洛谷 P5336 写的是 a<=1500；本数据集按一本通官方题面的 a<=100 造，
#     std 对 a<=1500 同样不溢出，见 std.cpp 头注「代价上界」。）
#   注意: 一个批次可以是「原序列上被先抽走元素隔开」的一段 —— 不能按原序列连续
#   区间划分来造/判数据 (那样的错误模型在题面样例上会得到 21, 而正确答案是 15)。
#
# 分层设计:
#   点 1  边界层: n=1, a=0 b=0, w=[1000]            (最小规模 + 最小参数)
#   点 2  边界层: n=2, a=100 b=0, w=[1,1000]        (b=0, 参数 a 顶格)
#   点 3  边界层: n=3, a=1 b=1, w=[5,1,5]           (跨中间合并的最小判别例)
#   点 4  边界层: n=5, a=0 b=1, w=[1,2,3,4,5]       (a=0)
#   点 5  小规模: n=10, a=3 b=1, 题面样例           (样例回归, 期望 15)
#   点 6  中规模: n=20, a=5 b=2, 随机 w∈[1,1000]    (中等 + 重复值)
#   点 7  中规模: n=50, a=100 b=10, w_i=20i 递增    (全不同, V 顶格, 单调)
#   点 8  大规模: n=50, a=100 b=10, w 全为 1000     (最大合并, 期望 a=100)
#   点 9  大规模: n=50, a=100 b=10, w 交替 1/1000   (两类无法同时合并)
#   点 10 顶格层: n=50, a=100 b=10, 随机 w∈[1,1000] (规模/参数全顶格)
#
# .out 一律用 subprocess 显式调用 work/std 生成 (规避 cyaron 写缓冲未 flush 产生
# 0 字节 .out 的隐患), 并断言 .out 非空、恰为 1 行、取值在 int 范围内。
# 生成器全部 O(n), 无 O(n^2) Python 循环。
#
# 运行方式 (必须在 data/ 下跑, IO 与 .out 都落在 cwd):
#   g++ -O2 -std=c++17 -o work/std std.cpp
#   cd data && python3 ../data.py
# ---------------------------------------------------------------------------
import os
import random
import subprocess
import sys

from cyaron import IO

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "work", "std")

SAMPLE_W = [7, 10, 9, 10, 6, 7, 10, 7, 1, 2]


def gen(data_id, n, a, b, w, quiet=True):
    """写 problem{data_id}.in，并用 std 跑出 problem{data_id}.out。返回答案。"""
    assert len(w) == n, "n 与 w 长度不符"
    assert 1 <= n <= 50, "n 超范围"
    assert 0 <= a <= 100, "a 超范围"
    assert 0 <= b <= 10, "b 超范围"
    assert all(1 <= x <= 1000 for x in w), "w_i 超范围"

    text = "%d\n%d %d\n%s\n" % (n, a, b, " ".join(map(str, w)))

    io = IO(file_prefix="problem", data_id=data_id)
    io.input_write(text)
    io.close()

    in_path = "problem%d.in" % data_id
    out_path = "problem%d.out" % data_id

    # ---- 用 subprocess 显式跑 std 生成 .out ----
    with open(in_path, "rb") as f:
        inp = f.read()
    res = subprocess.run([STD], input=inp, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, timeout=110)
    if res.returncode != 0:
        raise RuntimeError("std failed on case %d: rc=%d err=%s"
                           % (data_id, res.returncode, res.stderr[:300]))
    out = res.stdout

    # ---- 断言 .out 非空且恰为 1 行 ----
    assert len(out) > 0, "case %d .out 为空!" % data_id
    lines = out.decode().split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    assert len(lines) == 1, "case %d 行数 %d != 1" % (data_id, len(lines))
    v = int(lines[0])
    assert 0 <= v < (1 << 31), "case %d 答案 %s 越界" % (data_id, lines[0])

    with open(out_path, "wb") as f:
        f.write(out)

    if not quiet:
        print("case %2d: n=%2d a=%3d b=%2d 答案=%d" % (data_id, n, a, b, v))
    return v


def main():
    if not os.path.exists(STD):
        print("std 不存在, 请先编译: g++ -O2 -std=c++17 -o work/std std.cpp",
              file=sys.stderr)
        sys.exit(1)

    rnd = random.Random(1766)
    answers = {}

    # 1 边界: n=1, a=0 b=0
    answers[1] = gen(1, 1, 0, 0, [1000])
    # 2 边界: n=2, b=0, a 顶格
    answers[2] = gen(2, 2, 100, 0, [1, 1000])
    # 3 边界: 跨中间合并的最小判别例
    answers[3] = gen(3, 3, 1, 1, [5, 1, 5])
    # 4 边界: a=0
    answers[4] = gen(4, 5, 0, 1, [1, 2, 3, 4, 5])
    # 5 小规模: 题面样例
    answers[5] = gen(5, 10, 3, 1, SAMPLE_W)
    # 6 中规模: n=20 随机
    answers[6] = gen(6, 20, 5, 2, [rnd.randint(1, 1000) for _ in range(20)])
    # 7 中规模: n=50 递增 (全不同, V 顶格)
    answers[7] = gen(7, 50, 100, 10, [20 * i for i in range(1, 51)])
    # 8 大规模: n=50 全等
    answers[8] = gen(8, 50, 100, 10, [1000] * 50)
    # 9 大规模: n=50 交替
    answers[9] = gen(9, 50, 100, 10, [1 if i % 2 == 0 else 1000 for i in range(50)])
    # 10 顶格: n=50 随机
    answers[10] = gen(10, 50, 100, 10, [rnd.randint(1, 1000) for _ in range(50)])

    # 结构性断言 (可手算的判别点)
    assert answers[1] == 0, "case1 应为 0"
    assert answers[2] == 100, "case2 应为 100"
    assert answers[3] == 2, "case3 应为 2 (跨中间合并)"
    assert answers[4] == 0, "case4 应为 0"
    assert answers[5] == 15, "case5 (题面样例) 应为 15"
    assert answers[8] == 100, "case8 应为 100 (一批全等)"
    assert answers[9] == 2600, "case9 应为 2600 (26 批 × a)"

    print("data.py: 10 组数据生成完成")
    for i in range(1, 11):
        print("  case %2d -> %d" % (i, answers[i]))


if __name__ == "__main__":
    main()
