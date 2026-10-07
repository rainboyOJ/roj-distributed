#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一本通 高手训练 1719《过河》分层测试数据生成器（cyaron）

模型（与 std.cpp 头注一致）：河宽 W；可行走集合 = y=0 / y=W 两直线与买的木圆盘
（可伸出地面）。圆心必须放在木桩 (X_k,Y_k)；同种盘可买任意多块。两盘可通行 ⇔
圆心距 ≤ R1+R2（相切即可）；触底 ⇔ Y≤R；触顶 ⇔ W−Y≤R。问题 = 点权（价格 C）
最短路，起点触底盘、终点触顶盘；输出最小花费，无解输出 impossible。

范围（题面）：1≤T≤10；1≤N,M≤250；2≤W≤10^9；0≤X_k≤10^9；1≤Y_k≤W；
1≤R_k≤10^9；1≤C_k≤10^6。档位：10% N,M≤5；30% N,M≤30；20% X_k=0；70% N,M≤100。

分层（点 1 为样例 T=3，其余 T=10）：
  1  题面样例原样                -> 206 / 5 / impossible
  2  最小边界 N=M=1~2、W=2/3、   -> 手推：1 / impossible / 1000000 ...
     相切、X/C 顶格、不可行
  3  X_k=0 档（20%）             -> 手推：10^6、5.1*10^7、1.25*10^8 ...
  4  N,M≤5 档（10%）             -> 手推：3 / 15 / 3 ...
  5  N,M≤30 档（30%）            -> 手推：1.5*10^7 / 15 / 16 ...
  6  N,M≤100 档（70%）           -> 手推：50 / 26 / 5.1*10^7 ...
  7  顶格随机 N=M=250 全量程     -> std 实测回归向量（种子 1 复现）
  8  已知答案构造：细链 126、     -> 手推：126 / 1.26*10^8 / 2.5*10^8 ...
     1.26*10^8、2.5*10^8、精确相切
  9  对抗最坏：Pareto 半径递增、  -> std 实测（7 组 impossible + 3 组大答案）
     全连通但触不到顶（全节点弹出）
 10  顶格大答案 + 精确相切陷阱   -> 手推：2.49*10^8 / 1.25*10^8 / 4 ...

用法：python3 .ybt-import/staging/1719/data.py
std 缺失时脚本会现场编译到 work/std（编译产物属临时构建物）。
"""

import os
import random
import subprocess
import sys

from cyaron import IO

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
STD = os.path.join(HERE, "std")
STD_SRC = os.path.join(HERE, "std.cpp")
WORK_STD = os.path.join(HERE, "work", "std")

MAXN = MAXM = 250
MAXW = 10 ** 9
MAXC = 10 ** 6

# 各点 std 实测输出（回归对照；带 None 的位置为随机/不预设）
EXPECT = {
    1: ["206", "5", "impossible"],
    2: ["1", "impossible", "impossible", "1", "1000000", "5",
        "2", "6", "impossible", "1"],
    3: ["1000000", "impossible", "51000000", "50000000", "51", "8",
        "125000000", "impossible", "51", "12"],
    4: ["3", "1", "15", "impossible", "3", "impossible", "1000000",
        "1", "3", "1000000"],
    5: ["15000000", "8", "15", "10", "impossible", "16", "16",
        "2", None, "impossible"],
    6: ["50", "26", "30", "51000000", "50000000", "51", "impossible",
        "17", "50", "51"],
    7: ["4204", "5775", "9807", "6752", "9271", "1633", "14779",
        "15516", "4756", "708"],
    8: ["126", "126", "126000000", "126000000", "250000000", "10",
        "6", "3", "1250000", "3"],
    9: [None] * 10,
    10: ["249000000", "125000000", "126000000", "250000000", "125000000",
         "125", "4", "impossible", "2", "impossible"],
}


def ensure_std():
    """确保 std 可执行文件存在（优先同级 std，其次 work/std，否则现场编译）。"""
    if os.path.exists(STD):
        return STD
    if os.path.exists(WORK_STD):
        return WORK_STD
    if not os.path.exists(STD_SRC):
        sys.exit("std.cpp not found: %s" % STD_SRC)
    os.makedirs(os.path.dirname(WORK_STD), exist_ok=True)
    subprocess.run(["g++", "-O2", "-std=c++17", "-o", WORK_STD, STD_SRC],
                   check=True)
    print("compiled std: %s -> %s" % (STD_SRC, WORK_STD))
    return WORK_STD


def check_case(stakes, discs, W):
    """校验一组数据满足题面全部范围限制（生成器自身防呆）。"""
    assert 1 <= len(stakes) <= MAXN, "N out of range"
    assert 1 <= len(discs) <= MAXM, "M out of range"
    assert 2 <= W <= MAXW, "W out of range"
    for x, y in stakes:
        assert 0 <= x <= MAXW and 1 <= y <= W, ("stake", x, y, W)
    for r, c in discs:
        assert 1 <= r <= MAXW and 1 <= c <= MAXC, ("disc", r, c)


def emit(io, text):
    io.input_write(text)
    io.output_gen(STD_PATH)
    io.output_file.flush()


def run_and_read(idx, ncases):
    with open(os.path.join(DATA_DIR, "problem%d.out" % idx)) as f:
        ans = f.read().split()
    assert len(ans) == ncases, ("answer count", idx, ans)
    for a in ans:
        assert a == "impossible" or (a.isdigit() and int(a) >= 1), \
            ("format", idx, a)
    return ans


def check_expect(idx, ans, expect):
    if expect is None:
        return
    assert len(expect) == len(ans), ("expect count", idx)
    for i, (a, e) in enumerate(zip(ans, expect)):
        assert e is None or a == e, ("answer mismatch", idx, i + 1, a, e)


def write_layer(idx, cases, expect=None, note=""):
    """写出 data/problem{idx}.in 并用 std 生成 .out。"""
    assert 1 <= idx <= 10
    lines = ["%d" % len(cases)]
    for stakes, discs, W in cases:
        check_case(stakes, discs, W)
        lines.append("%d %d %d" % (len(stakes), len(discs), W))
        lines.extend("%d %d" % (x, y) for x, y in stakes)
        lines.extend("%d %d" % (r, c) for r, c in discs)
    io = IO(file_prefix=os.path.join(DATA_DIR, "problem"), data_id=idx)
    emit(io, "\n".join(lines) + "\n")
    ans = run_and_read(idx, len(cases))
    check_expect(idx, ans, expect)
    print("problem%-2d %-24s -> %s" % (idx, note, " ".join(ans)))
    return ans


SAMPLE = """3
11 4 13
19 10
8 7
11 4
26 1
4 2
15 4
19 4
1 9
4 6
19 5
15 10
2 1
3 100
4 10000
5 1000000
11 4 13
19 10
8 7
11 4
26 1
4 2
15 4
19 4
1 9
4 6
19 5
15 10
2 1
3 2
4 3
5 4
1 1 1000000000
0 500000000
1 1
"""


def write_sample(idx, text, expect=None, note=""):
    """直接写入原始文本（题面样例），并用 std 生成 .out。"""
    io = IO(file_prefix=os.path.join(DATA_DIR, "problem"), data_id=idx)
    emit(io, text)
    with open(os.path.join(DATA_DIR, "problem%d.out" % idx)) as f:
        ans = f.read().split()
    if expect:
        check_expect(idx, ans, expect)
    print("problem%-2d %-24s -> %s" % (idx, note, " ".join(ans)))
    return ans


def gen2(rnd):
    """点 2：最小边界（N=M=1~2、W=2/3、底顶相切、X/C 顶格、不可行）。"""
    L2 = [
        ([(0, 1)], [(1, 1)], 2),              # R=Y=1, W=2Y 最小可行
        ([(0, 1)], [(1, 1)], 3),              # W 只差 1 -> impossible
        ([(0, 2)], [(1, 1)], 2),              # 桩在顶线，R 不够 -> impossible
        ([(0, 2)], [(2, 1)], 2),              # R=W 单盘双触
        ([(0, 1)], [(1, 1000000)], 2),        # C 顶格
        ([(0, 1), (0, 3)], [(2, 5)], 3),      # 单盘同时触底触顶
        ([(0, 2), (0, 5)], [(1, 3), (3, 2)], 5),
        ([(0, 3), (0, 10)], [(7, 3), (5, 4)], 17),  # 精确相切 d=7=R1+R2
        ([(0, 500000000)], [(1, 1)], 10 ** 9),      # 最宽河 -> impossible
        ([(10 ** 9, 1)], [(1, 1)], 2),        # X 顶格 + 可行
    ]
    return write_layer(2, L2, EXPECT[2], "最小边界")


def gen3(rnd):
    """点 3：X_k=0 档（20%），含 N=M=250 与 W=10^9。"""
    dec99 = [(rnd.randint(2, MAXW), 1000000) for _ in range(99)]
    dec29 = [(rnd.randint(3, MAXW), 1000000) for _ in range(29)]
    dec249 = [(rnd.randint(2, MAXW), 1000000) for _ in range(249)]
    dec28 = [(rnd.randint(3, MAXW), 1000000) for _ in range(28)]
    L3 = [
        ([(0, 500000000)], [(500000000, 1000000)], 10 ** 9),
        ([(0, i) for i in range(1, 31)], [(1, 1)], 32),
        ([(0, i) for i in range(1, 101)], [(1, 1000000)], 101),
        ([(0, i) for i in range(1, 101)], [(1, 1000000)], 100),
        ([(0, i) for i in range(1, 101)], [(1, 1)] + dec99, 101),
        ([(0, i) for i in range(1, 31)], [(2, 1)] + dec29, 31),
        ([(0, i) for i in range(1, 251)], [(1, 1000000)], 250),
        ([(0, i) for i in range(1, 251)], [(500000000, 1000000)], 10 ** 9),
        ([(0, i) for i in range(1, 101)], [(1, 1)] + dec249, 101),
        ([(0, i) for i in range(1, 11)], [(1, 2)] + dec28, 11),
    ]
    return write_layer(3, L3, EXPECT[3], "X_k=0 档(20%)")


def gen4(rnd):
    """点 4：N,M≤5 档（10%）。"""
    L4 = [
        ([(3 * k, 4 * k) for k in range(1, 6)], [(5, 1)], 25),
        ([(0, 1)], [(1, 1)], 2),
        ([(0, i) for i in range(1, 6)], [(1, 5)], 6),
        ([(3 * k, 4 * k) for k in range(1, 6)], [(5, 1)], 100),
        ([(0, 1), (4, 4)], [(2, 1), (3, 2)], 5),
        ([(0, 1), (4, 4)], [(2, 1), (2, 2)], 5),
        ([(0, 1)], [(10 ** 9, 1000000)], 10 ** 9),
        ([(0, 1), (2, 3), (4, 2), (1, 4), (3, 5)],
         [(2, 3), (2, 5), (3, 2), (5, 1), (5, 9)], 6),
        ([(1, 2), (3, 4), (2, 5), (4, 1), (0, 3)],
         [(6, 3), (4, 7), (2, 1), (8, 9), (3, 5)], 10),
        ([(0, i) for i in range(1, 6)],
         [(10 ** 9, 1000000), (1, 1), (2, 2), (3, 3), (4, 4)],
         10 ** 9),
    ]
    return write_layer(4, L4, EXPECT[4], "N,M<=5 档(10%)")


def gen5(rnd):
    """点 5：N,M≤30 档（30%）。"""
    dec29 = [(rnd.randint(3, MAXW), 1000000) for _ in range(29)]
    L5 = [
        ([(0, i) for i in range(1, 31)], [(1, 1000000)], 30),
        ([(0, i) for i in range(1, 31)], [(2, 1)] + dec29, 31),
        ([(3 * k, 4 * k) for k in range(1, 31)], [(5, 1)], 121),
        ([(0, 2), (6, 10)], [(4, 3), (6, 7)], 12),
        ([(0, i) for i in range(1, 31)], [(500000000, 1000000)], 10 ** 9),
        ([(0, 2 * i) for i in range(1, 31)], [(2, 1)], 61),
        ([(5 * t, 12 * t) for t in range(1, 31)], [(13, 1)], 373),
        ([(0, 30), (0, 15), (0, 1)], [(15, 2), (29, 3)], 30),
        ([(1, 2), (18, 28), (4, 9), (11, 17), (27, 5),
          (6, 21), (22, 13), (9, 26), (14, 3), (25, 19),
          (2, 7), (16, 24), (7, 12), (29, 30), (3, 16),
          (19, 8), (12, 22), (24, 2), (8, 11), (21, 27),
          (5, 14), (26, 6), (13, 25), (28, 20), (10, 4),
          (20, 29), (17, 1), (23, 10), (15, 23), (30, 18)],
         [(29, 1000), (13, 7), (21, 3), (5, 999), (26, 11),
          (8, 500), (17, 2), (3, 100), (30, 60), (11, 42),
          (23, 9), (7, 300), (19, 25), (2, 7), (28, 90),
          (14, 5), (6, 77), (25, 12), (10, 33), (4, 200),
          (22, 6), (16, 19), (9, 88), (27, 14), (1, 55),
          (20, 4), (12, 66), (18, 8), (15, 111), (24, 22)], 30),
        ([(0, 5 * i) for i in range(1, 31)],
         [(10 ** 6, 1000), (10 ** 5, 3)], 150000001),
    ]
    return write_layer(5, L5, EXPECT[5], "N,M<=30 档(30%)")


def gen6(rnd):
    """点 6：N,M≤100 档（70%）。"""
    L6 = [
        ([(3 * k, 4 * k) for k in range(1, 101)], [(5, 1)], 401),
        ([(0, i) for i in range(1, 101)], [(2, 1)], 101),
        ([(3 * k, 4 * k) for k in range(1, 61)], [(5, 1)], 241),
        ([(0, i) for i in range(1, 101)], [(1, 1000000)], 101),
        ([(0, i) for i in range(1, 101)], [(1, 1000000)], 100),
        ([(5 * t, 12 * t) for t in range(1, 101)], [(13, 1)], 1213),
        ([(7 * t, 24 * t) for t in range(1, 101)], [(25, 1)], 2426),
        ([(0, i) for i in range(1, 101)],
         [(1, 999999), (3, 1), (2, 500000)], 101),
        ([(3 * k, 4 * k) for k in range(1, 101)],
         [(5, 1), (4, 2), (3, 3), (10 ** 9, 1000000)], 401),
        ([(5 * t, 12 * t) for t in range(1, 101)],
         [(13, 1)] + [(14 + 10 ** 7 * j, 10001 + 10000 * j) for j in range(99)],
         1213),
    ]
    return write_layer(6, L6, EXPECT[6], "N,M<=100 档(70%)")


def gen7(rnd):
    """点 7：顶格随机（种子 1 复现基准随机流；回归对照向量见 EXPECT[7]）。"""
    cases = []
    r7 = random.Random(1)   # 专用流，与基准脚本 random.seed(1) 完全一致
    for _ in range(10):
        N = M = MAXN
        W = MAXW
        stakes = [(r7.randint(0, MAXW), r7.randint(1, W)) for _ in range(N)]
        discs = [(r7.randint(1, MAXW), r7.randint(1, MAXC)) for _ in range(M)]
        cases.append((stakes, discs, W))
    return write_layer(7, cases, EXPECT[7], "顶格随机 N=M=250")


def gen8(rnd):
    """点 8：已知答案（细链 126 / 2.5*10^8 / 精确相切 / 同盘双触）。"""
    dec249 = [(rnd.randint(3, MAXW), 1000000 - j) for j in range(1, 250)]
    L8 = [
        ([(0, 2 * i) for i in range(1, 251)], [(2, 1)], 501),
        ([(0, 2 * i) for i in range(1, 251)], [(2, 1)] + dec249, 501),
        ([(0, 2 * i) for i in range(1, 251)], [(2, 1000000)], 501),
        ([(0, i) for i in range(1, 251)], [(1, 1000000)], 251),
        ([(0, 2 * i - 1) for i in range(1, 251)], [(1, 1000000)], 500),
        ([(0, 2), (0, 10)], [(4, 5)], 12),
        ([(0, 3), (0, 10)], [(7, 3), (5, 4)], 17),
        ([(0, 1), (4, 4)], [(2, 1), (3, 2)], 5),
        ([(0, 1), (3, 5)], [(2, 250000), (3, 1000000)], 8),
        ([(3 * k, 4 * k) for k in range(1, 6)], [(5, 1)], 25),
    ]
    return write_layer(8, L8, EXPECT[8], "已知答案构造")


def gen9(rnd):
    """点 9：对抗最坏（Pareto 半径递增，全连通但永远触不到顶 -> 全节点弹出）。"""
    cases = []
    # 7 组：所有木桩最多只能触底，R 递增 Pareto，答案恒为 impossible
    for t in range(7):
        r9 = random.Random(9000 + t)
        stakes = [(r9.randint(0, MAXW), r9.randint(1, 4 * 10 ** 8))
                  for _ in range(MAXN)]
        discs = [(10 ** 6 * (j + 1), 4000 * (j + 1)) for j in range(MAXM)]
        cases.append((stakes, discs, MAXW))
    # 3 组：密连通大半径（全部圆盘可触底、大量触顶），答案中等
    for t in range(3):
        r9 = random.Random(9100 + t)
        stakes = [(r9.randint(0, MAXW), r9.randint(2 * 10 ** 8, 8 * 10 ** 8))
                  for _ in range(MAXN)]
        discs = [(5 * 10 ** 8 + 2 * 10 ** 6 * j, 4000 * (j + 1))
                 for j in range(MAXM)]
        cases.append((stakes, discs, MAXW))
    return write_layer(9, cases, EXPECT[9], "对抗最坏")


def gen10(rnd):
    """点 10：顶格大答案 + 精确相切陷阱（大坐标整数判定）。"""
    L10 = [
        # 对角链，步长 4*10^6：每盘最多跨 2 桩 -> 125 盘 = 1.25*10^8
        ([(10 ** 9 - 4 * 10 ** 6 * i, 4 * 10 ** 6 * i) for i in range(1, 251)],
         [(4 * 10 ** 6, 1000000)], 10 ** 9),
        # 竖直链 4*10^6 步长 + 249 个 R<10^6 的便宜干扰盘 -> 125*10^6
        ([(0, 4 * 10 ** 6 * i) for i in range(1, 251)],
         [(4 * 10 ** 6, 1000000)] +
         [(rnd.randint(1, 10 ** 6), 1) for _ in range(249)], 10 ** 9),
        # 竖直链奇偶错位（首末桩各贴一边）-> 126 盘 = 1.26*10^8
        ([(0, 4 * 10 ** 6 * i - 2 * 10 ** 6) for i in range(1, 251)],
         [(4 * 10 ** 6, 1000000)] +
         [(rnd.randint(1, 10 ** 6), 1) for _ in range(249)], 10 ** 9),
        # R=1 细链 250 盘 C=10^6 -> 2.5*10^8
        ([(0, 2 * i - 1) for i in range(1, 251)], [(1, 1000000)], 500),
        # 3-4-5 相切链 R=5 -> 125 盘 = 1.25*10^8
        ([(3 * k, 4 * k) for k in range(1, 251)], [(5, 1000000)], 1001),
        # 同链 + 249 个贵干扰盘 -> 125
        ([(3 * k, 4 * k) for k in range(1, 251)],
         [(5, 1)] + [(rnd.randint(6, MAXW), 1000000) for _ in range(249)],
         1001),
        # 精确相切陷阱：d = sqrt(10^18 + (10^9-1)^2) ≈ 1414213561.666,
        # R=707106781 时 2R=1414213562 >= d 可连 -> 2 盘 = 4
        ([(0, 1), (10 ** 9, 10 ** 9)], [(707106781, 2)], 10 ** 9),
        # 同坐标但 R=707106780: 2R=1414213560 < d -> impossible
        ([(0, 1), (10 ** 9, 10 ** 9)], [(707106780, 1)], 10 ** 9),
        # Pareto 支配：R=707106782 且更便宜 -> 只剩该种盘，2 盘 = 2
        ([(0, 1), (10 ** 9, 10 ** 9)],
         [(707106781, 1000000), (707106782, 1)], 10 ** 9),
        # 250 桩同点 (0,1)：R=5*10^8 无法触顶 W-1 -> impossible
        ([(0, 1)] * 250,
         [(500000000, 1000)] +
         [(rnd.randint(2, 10 ** 8 - 1), 1000000) for _ in range(249)],
         10 ** 9),
    ]
    return write_layer(10, L10, EXPECT[10], "顶格大答案+相切陷阱")


def main():
    global STD_PATH
    os.makedirs(DATA_DIR, exist_ok=True)
    STD_PATH = ensure_std()
    rnd = random.Random(20251006)   # 固定种子，保证生成器可复现

    # ---- 1. 题面样例原样（T=3）----
    write_sample(1, SAMPLE, EXPECT[1], "题面样例")

    gen2(rnd)
    gen3(rnd)
    gen4(rnd)
    gen5(rnd)
    gen6(rnd)
    gen7(rnd)
    gen8(rnd)
    gen9(rnd)
    gen10(rnd)
    print("all 10 cases generated into %s" % DATA_DIR)


if __name__ == "__main__":
    main()
