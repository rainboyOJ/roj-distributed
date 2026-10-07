#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1789《分班》 分层测试数据生成器
# ---------------------------------------------------------------------------
# 用法（在本目录下执行）：
#     nice -n 19 timeout 600 python3 data.py
# 产物：./data/problem1.in/.out … ./data/problem10.in/.out
# 说明：
#   * .in 由本脚本按分层策略构造；
#   * .out 一律用 **subprocess 显式调用 ./std** 生成（不走 cyaron 的 output_gen，
#     规避其写缓冲不 flush 导致 0 字节 .out 的隐患），生成后逐点断言
#     「文件非空 + 行数 == 该文件的数据组数 case + 每行 3 个整数」。
#   * ./std 缺失（已清理编译产物）时，现场用 g++ 从 std.cpp 编译。
#
# 题面数据规模（ybt 官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=1789 表格原文，
# 含 rowspan，已按 HTML 还原）：
#   编号 1：M=5，N=1        ｜ 编号 2：M≤10，N≤3   ｜ 编号 3：M≤100，N≤10
#   编号 4：M≤1000，N≤50    ｜ 编号 5..10：M≤10000，N≤200
#   全表：1≤A≤B≤M，1≤X[i]≤100000
#   G[i]：编号 1..4 ∈ [-1000,1000]；编号 5..7 ∈ [0,1000]；编号 8..10 ∈ [-1000,1000]
#   多组数据：case ≤ 10（第一行给出组数）
# 限制：time 1000 ms / memory 262144 KB（config.json 记为 1000ms/256MB）
#
# ---- 分层策略（10 个测试点，逐点从边界铺到顶格）----
#  点 1  边界层：M=5,N=1,A=1,B=5（题面最小规模；N=1 时只能 1 个班，
#        必然 sigma=G[1]*ΣW、class=1、last=5 —— 可手算锚点）。
#  点 2  边界层：**题面【输入样例】原样**（M=10,N=3,A=1,B=4），逐字节回归 186 3 4。
#  点 3  边界+小规模：case=5 —— 四个「退化/并列」手算锚点 + 一组 M=100,N=10 随机（含负 G）：
#        (a) 并列代价 tie-break 锚点：M=3,N=2,A=1,B=2,X=[1,2,3],G=[1,1]
#            → 两种分法代价都为 2，必须取 last 更小者 → 2 2 1；
#        (b) 全等 X（W≡0）：M=6,N=2,A=1,B=5 → 0 2 1（sigma=0 时先压班数再压 last）。
#        (d)(e) G 全相等（代价 = G*ΣW 与划分无关）：M=10,N=4，B=5 → 255 2 5；B=6 → 255 2 4
#              （分别验证 last 取到 B 与未取到 B 两种情形）。
#  点 4  中规模：M=1000,N=50,A=1,B=40：一组随机 + 一组全等 X 手算锚点（0 25 40）。
#  点 5  大规模：M=10000,N=200,A=1,B=10000（G∈[0,1000]）：随机 + 全等 X 锚点（0 1 10000）。
#  点 6  顶格 + 紧结构（G∈[0,1000]，case=3）：
#        (a) A=1,B=60 全等 X → class 被 B 卡死为 ceil(10000/60)=167，last=40（手算锚点）；
#        (b) A=B=50 全等 X → 恰好 200 班、每班 50 人（0 200 50）；
#        (c) A=1,B=10000 随机 X —— 顶格随机压力。
#  点 7  顶格最紧：A=B=50（M=10000,N=200）→ 唯一合法结构就是 200 班 × 50 人，随机 X。
#  点 8  负 G 层（G∈[-1000,1000]，case=2）：
#        (a) A=1,B=200 随机 X 随机 G；
#        (b) G 全 -1000 → 代价与划分无关（= -1000*ΣW），压成最小班数 ceil(10000/200)=50，
#            last=200 —— 完整手算锚点，验证负 G 下的字典序 tie-break。
#  点 9  负 G 顶格（G∈[-1000,1000]，case=2）：
#        (a) A=B=50 随机 X 且 G 含负值（200 班强制结构 + 负代价）；
#        (b) 全等 X 且 G 全 -1000 → sigma=0、class=1、last=10000。
#  点 10 顶格卡时：case=10 × (M=10000,N=200,A=1,B=100) 随机 X + 含负 G —— 单文件最大负载。
#
#  边界清单：最小规模→点1；题面样例→点2；sigma=0→点3(b)/4(b)/5(b)/6(a)(b)/9(b)；
#   sigma<0（负 G）→点3(c)/4(a)/8/9(a)/10；并列最小代价→点3(a)；last 取到 B→点4(b)；
#   last 取到 A→点3(a)（A=1）；班数被 N 卡死→点6(b)/7/9(a)；班数被 B 卡死→点6(a)；
#   多组数据→点3/4/5/6/8/9/10；全部随机种子固定，结果完全可复现。
#  注：**本套数据所有组均保证有可行分法**（题面未定义无解输出格式，故不构造无解点）。

import os
import random
import subprocess

from cyaron import IO  # 引入 CYaRon 的库

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "std")
STD_CPP = os.path.join(HERE, "std.cpp")
DATA_DIR = os.path.join(HERE, "data")

XMAX = 100000


def ensure_std():
    """../std 缺失（已清理编译产物）时，从 std.cpp 现场编译。"""
    if not os.path.exists(STD):
        subprocess.check_call(["g++", "-O2", "-std=c++17", STD_CPP, "-o", STD])
        print("compiled std from std.cpp")


def rand_x(rng, m, lo=1, hi=XMAX):
    return [rng.randint(lo, hi) for _ in range(m)]


def g_sym(rng, n, lo, hi):
    """对称区间（可能含负值）的随机 G。"""
    return [rng.randint(lo, hi) for _ in range(n)]


def g_pos(rng, n, lo=0, hi=1000):
    """非负区间 [0,1000] 的随机 G。"""
    return [rng.randint(lo, hi) for _ in range(n)]


def feasible_k_range(m, a, b, n):
    """返回可行班数 k 的区间 [klo, khi]（khi 已与 N 取交）；不可行返回 None。"""
    klo = (m + b - 1) // b            # 每班最多 b 人
    khi = min(n, m // a)              # 每班至少 a 人
    if klo > khi:
        return None
    return klo, khi


def sigma_of(x, g, blocks):
    """按给定划分 blocks=[(l,r),...] 复算 sigma（生成期自检用，非暴力搜索）。"""
    m = len(x)
    avg = sum(x) // m
    w = [(v - avg) ** 2 for v in x]
    pre = [0] * (m + 1)
    for i in range(m):
        pre[i + 1] = pre[i] + w[i]
    return sum(g[j - 1] * (pre[r] - pre[l - 1]) for j, (l, r) in enumerate(blocks, 1))


# ============================== 各测试点构造 ==============================

# ---- 点 1：M=5,N=1,A=1,B=5（题面最小规模，手算锚点）----
P1_X = [10, 20, 30, 40, 50]        # sum=150, avg=30, W=[400,100,0,100,400], ΣW=1000
P1_G = [7]
P1 = dict(M=5, N=1, A=1, B=5, X=P1_X, G=P1_G,
          expect="7000 1 5", note="边界：最小规模 M=5,N=1（唯一分法 1 班 5 人）")

# ---- 点 2：题面【输入样例】原样 ----
P2 = dict(M=10, N=3, A=1, B=4,
          X=[16, 11, 12, 13, 10, 15, 16, 17, 18, 14], G=[4, 5, 1],
          expect="186 3 4", note="边界：题面输入样例原样（逐字节回归）")

# ---- 点 3：case=3（并列 tie-break 锚点 + 全等 X 锚点 + M=100 随机含负 G）----
P3 = [
    dict(M=3, N=2, A=1, B=2, X=[1, 2, 3], G=[1, 1],
         expect="2 2 1",
         note="并列最小代价：(1,2)/(2,1) 代价都为 2，须取 last 更小者 → last=1"),
    dict(M=6, N=2, A=1, B=5, X=[1] * 6, G=[1, 1],
         expect="0 2 1", note="全等 X ⇒ ΣW=0 ⇒ sigma=0，先压班数(2)再压 last(1)"),
    dict(M=100, N=10, A=2, B=11,
         X=rand_x(random.Random(178903), 100),
         G=g_sym(random.Random(178931), 10, -1000, 1000),
         note="小规模随机（M=100,N=10，A=2,B=11 ⇒ 恰好 10 班），G 含负值"),
    dict(M=10, N=4, A=2, B=5, X=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], G=[3, 3, 3, 3],
         expect="255 2 5",
         note="G 全相等 ⇒ sigma=G*ΣW=3*85=255 与划分无关；压班数 ceil(10/5)=2，last=5"),
    dict(M=10, N=4, A=2, B=6, X=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], G=[3, 3, 3, 3],
         expect="255 2 4",
         note="G 全相等且 B=6 ⇒ sigma=255、class=2、last=10-6=4（last 未取到 B）"),
]

# ---- 点 4：M=1000,N=50,A=1,B=40 ----
P4 = [
    dict(M=1000, N=50, A=1, B=40,
         X=rand_x(random.Random(178904), 1000),
         G=g_sym(random.Random(178941), 50, -1000, 1000),
         note="中规模随机（M=1000,N=50），G 含负值"),
    dict(M=1000, N=50, A=1, B=40, X=[100000] * 1000,
         G=g_pos(random.Random(178942), 50),
         expect="0 25 40",
         note="全等 X：sigma=0；班数下限 ceil(1000/40)=25，last=1000-24*40=40（取到 B）"),
]

# ---- 点 5：M=10000,N=200,A=1,B=10000，G∈[0,1000] ----
P5 = [
    dict(M=10000, N=200, A=1, B=10000,
         X=rand_x(random.Random(178905), 10000),
         G=g_pos(random.Random(178951), 200),
         note="大规模随机（M,N 顶格；G∈[0,1000]）"),
    dict(M=10000, N=200, A=1, B=10000, X=[1] * 10000,
         G=g_pos(random.Random(178952), 200),
         expect="0 1 10000", note="全等 X：sigma=0，1 个班即可（class=1,last=10000）"),
]

# ---- 点 6：顶格紧结构，G∈[0,1000]，case=3 ----
P6 = [
    dict(M=10000, N=200, A=1, B=60, X=[5] * 10000,
         G=g_pos(random.Random(178961), 200),
         expect="0 167 40",
         note="全等 X；班数下限 ceil(10000/60)=167，last=10000-166*60=40"),
    dict(M=10000, N=200, A=50, B=50, X=[5] * 10000,
         G=g_pos(random.Random(178962), 200),
         expect="0 200 50", note="A=B=50 ⇒ 恰好 200 班 × 50 人（班数被 N 卡死）"),
    dict(M=10000, N=200, A=1, B=10000,
         X=rand_x(random.Random(178906), 10000),
         G=g_pos(random.Random(178963), 200),
         note="顶格随机压力（case=3 之一）"),
]

# ---- 点 7：顶格最紧 A=B=50（唯一合法结构），随机 X，G∈[0,1000] ----
P7 = dict(M=10000, N=200, A=50, B=50,
          X=rand_x(random.Random(178907), 10000),
          G=g_pos(random.Random(178971), 200),
          note="A=B=50：唯一合法划分是 200 班 × 50 人（class=200,last=50）")

# ---- 点 8：负 G 层，G∈[-1000,1000]，case=2 ----
_R8X = rand_x(random.Random(178908), 10000)
P8 = [
    dict(M=10000, N=200, A=1, B=200, X=_R8X,
         G=g_sym(random.Random(178981), 200, -1000, 1000),
         note="负 G 随机（A=1,B=200）"),
    dict(M=10000, N=200, A=1, B=200, X=_R8X, G=[-1000] * 200,
         expect=None,  # 期望值由 ΣW 现算，见下方断言
         note="G 全 -1000：代价 = -1000*ΣW 与划分无关 ⇒ 压班数 ceil(10000/200)=50，last=200"),
]

# ---- 点 9：负 G 顶格，case=2 ----
P9 = [
    dict(M=10000, N=200, A=50, B=50,
         X=rand_x(random.Random(178909), 10000),
         G=g_sym(random.Random(178991), 200, -1000, 1000),
         note="A=B=50 强制 200 班 × 50 人，G 含负值"),
    dict(M=10000, N=200, A=1, B=10000, X=[1] * 10000, G=[-1000] * 200,
         expect="0 1 10000", note="全等 X 且 G 全负：ΣW=0 ⇒ sigma=0，1 班即可"),
]

# ---- 点 10：顶格卡时，case=10 ----
P10 = [
    dict(M=10000, N=200, A=1, B=100,
         X=rand_x(random.Random(1789100 + t), 10000),
         G=g_sym(random.Random(1789101 + t), 200, -1000, 1000),
         note="卡时组 %d/10" % (t + 1))
    for t in range(10)
]

POINTS = [
    (1, [P1], "边界层：M=5,N=1（题面最小规模）"),
    (2, [P2], "边界层：题面【输入样例】原样"),
    (3, P3, "小规模层：并列 tie-break 锚点 + 全等 X 锚点 + M=100 随机（负 G）"),
    (4, P4, "中规模层：M=1000,N=50 随机 + 全等 X 锚点"),
    (5, P5, "大规模层：M=10000,N=200 随机 + 全等 X 锚点"),
    (6, P6, "顶格层：班数被 B/N 卡死的紧结构 + 顶格随机"),
    (7, [P7], "顶格层：A=B=50 唯一合法结构"),
    (8, P8, "负 G 层：随机负 G + G 全 -1000 的手算锚点"),
    (9, P9, "负 G 顶格层：强制 200 班 + 全等 X 锚点"),
    (10, P10, "顶格卡时层：case=10 × M=10000,N=200"),
]

# ============================== 生成前自检 ==============================
assert len(POINTS) == 10, "必须恰好 10 个测试点"

for idx, groups, _note in POINTS:
    assert 1 <= len(groups) <= 10, "点 %d 的 case 数越界" % idx
    for g in groups:
        M, N, A, B = g["M"], g["N"], g["A"], g["B"]
        assert len(g["X"]) == M, "点 %d 的 X 长度 != M" % idx
        assert len(g["G"]) == N, "点 %d 的 G 长度 != N" % idx
        assert 1 <= A <= B <= M, "点 %d 的 A/B 越界" % idx
        assert all(1 <= v <= XMAX for v in g["X"]), "点 %d 的 X 越界" % idx
        assert feasible_k_range(M, A, B, N) is not None, "点 %d 存在无解组（本套数据禁止）" % idx

# 逐点的题面规模（按编号）上界校验
LIMITS = {1: (5, 1), 2: (10, 3), 3: (100, 10), 4: (1000, 50)}
for idx, groups, _note in POINTS:
    for g in groups:
        if idx in LIMITS:
            mmax, nmax = LIMITS[idx]
            assert g["M"] <= mmax and g["N"] <= nmax, "点 %d 超出编号规模 M<=%d,N<=%d" % (idx, mmax, nmax)
        else:
            assert g["M"] <= 10000 and g["N"] <= 200, "点 %d 超出 M<=10000,N<=200" % idx
        if idx in (1, 2, 3, 4):
            assert all(-1000 <= v <= 1000 for v in g["G"]), "点 %d 的 G 超出 [-1000,1000]" % idx
        elif idx in (5, 6, 7):
            assert all(0 <= v <= 1000 for v in g["G"]), "点 %d 的 G 超出 [0,1000]" % idx
        else:
            assert all(-1000 <= v <= 1000 for v in g["G"]), "点 %d 的 G 超出 [-1000,1000]" % idx

# 手算锚点（构造点）的自检：用 sigma_of 按题目定义独立复算，确认 expect 与之一致
#  点 1：唯一分法 [(1,5)]
assert sigma_of(P1_X, P1_G, [(1, 5)]) == 7000, "点 1 锚点复算不符"
#  点 3(a)：两种并列分法的代价都为 2，last 最小者 = 1
assert sigma_of([1, 2, 3], [1, 1], [(1, 1), (2, 3)]) == 2
assert sigma_of([1, 2, 3], [1, 1], [(1, 2), (3, 3)]) == 2
#  点 3(d)(e)：G 全相等 ⇒ 代价 = G*ΣW，与划分无关
_X10 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
assert sigma_of(_X10, [3] * 4, [(1, 5), (6, 10)]) == 255
assert sigma_of(_X10, [3] * 4, [(1, 4), (5, 10)]) == 255
#  点 8(b)：代价 = -1000*ΣW（与划分无关）
_x8 = P8[1]["X"]
_avg8 = sum(_x8) // len(_x8)
_SW8 = sum((v - _avg8) ** 2 for v in _x8)
P8[1]["expect"] = "%d 50 200" % (-1000 * _SW8)

# 打印各点概览
print("各点 case 数:", " ".join(str(len(g)) for _, g, _ in POINTS))
print("各点最大 M:", " ".join(str(max(x["M"] for x in g)) for _, g, _ in POINTS))
for idx, groups, _n in POINTS:
    print("  点 %-2d: %d 组  M=%s N=%s  A/B=%s"
          % (idx, len(groups),
             "/".join(str(x["M"]) for x in groups),
             "/".join(str(x["N"]) for x in groups),
             "/".join("%d,%d" % (x["A"], x["B"]) for x in groups)))

# ============================== 生成 ==============================
ensure_std()
if not os.path.isdir(DATA_DIR):
    os.makedirs(DATA_DIR)
os.chdir(DATA_DIR)

SUMMARY = []
for idx, groups, note in POINTS:
    io = IO(file_prefix="problem", data_id=idx, disable_output=True)
    io.input_writeln(len(groups))
    for g in groups:
        io.input_writeln(g["M"], g["N"], g["A"], g["B"])
        io.input_writeln(g["X"])       # 第二行：M 个 X
        io.input_writeln(g["G"])       # 第三行：N 个 G
    io.close()                          # 显式关闭并 flush .in

    in_path = "problem%d.in" % idx
    out_path = "problem%d.out" % idx
    # 用 subprocess 显式跑 std 产出 .out（不依赖 cyaron 的写缓冲）
    with open(in_path, "rb") as fi, open(out_path, "wb") as fo:
        subprocess.run([STD], stdin=fi, stdout=fo, check=True)

    # ---- 断言：非空 + 行数 == case + 每行 3 个整数 + 结构合法 ----
    in_size = os.path.getsize(in_path)
    out_size = os.path.getsize(out_path)
    assert in_size > 0, "%s 为空" % in_path
    assert out_size > 0, "%s 为空（std 无输出？）" % out_path
    with open(out_path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    assert len(lines) == len(groups), \
        "%s 行数 %d != case %d" % (out_path, len(lines), len(groups))

    parsed = []
    for li, ln in enumerate(lines):
        parts = ln.split()
        assert len(parts) == 3, "%s 第 %d 行不是 3 个数: %r" % (out_path, li + 1, ln)
        sigma, cls, last = (int(t) for t in parts)
        g = groups[li]
        assert 1 <= cls <= g["N"], "%s 第 %d 行 class=%d 超出 [1,N]" % (out_path, li + 1, cls)
        assert g["A"] <= last <= g["B"], "%s 第 %d 行 last=%d 超出 [A,B]" % (out_path, li + 1, last)
        assert cls * g["A"] <= g["M"] and cls * g["B"] >= g["M"], \
            "%s 第 %d 行 (class,last) 与 M 不相容" % (out_path, li + 1)
        if all(v >= 0 for v in g["G"]):
            assert sigma >= 0, "%s 第 %d 行 G 非负但 sigma=%d < 0" % (out_path, li + 1, sigma)
        if g.get("expect") is not None:
            assert ln == g["expect"], \
                "%s 第 %d 行 %r != 手算锚点 %r" % (out_path, li + 1, ln, g["expect"])
        parsed.append((sigma, cls, last))

    SUMMARY.append((idx, len(groups), in_size, out_size, note))
    print("problem%-2d: case=%d  in=%7dB out=%6dB  %s" % (idx, len(groups), in_size, out_size, note))
    for li, (sigma, cls, last) in enumerate(parsed):
        print("     组%-2d: sigma=%-22d class=%-4d last=%-6d | %s"
              % (li + 1, sigma, cls, last, groups[li]["note"]))

print("\n全部 10 点生成完毕：problem1.in/.out … problem10.in/.out（成对齐全，断言全部通过）")

# ============================== 登记 data.json ==============================
# 仓库惯例：data.json 记录 data/ 下所有文件的相对路径与字节数（按路径字典序）。
import json
entries = []
for name in sorted(os.listdir(".")):
    if name.startswith("problem") and (name.endswith(".in") or name.endswith(".out")):
        entries.append({"path": name, "size": os.path.getsize(name)})
assert len(entries) == 20, "data/ 下应恰好 10 个 .in + 10 个 .out，实际 %d" % len(entries)
with open(os.path.join(HERE, "data.json"), "w", encoding="utf-8") as f:
    json.dump({"files": entries}, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("已登记 data.json：%d 个文件" % len(entries))
