#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 一本通 1783《矩阵填数》 数据生成器（目标 ROJ 题号 1783）
#
# 题面：h×w 矩阵每格填 1..m；n 个子矩阵“最大值 = v”的限制；求方案数 mod 1e9+7。
#       多组数据：第一行 T；每组 h w m n；随后 n 行 x1 y1 x2 y2 v。
# 范围：T ≤ 5，1 ≤ h,w,m ≤ 10000，1 ≤ v ≤ m，1 ≤ n ≤ 10。
#
# 产物：problem1.in/.out … problem10.in/.out（IO(file_prefix="problem", data_id=i)）。
#
# ⚠ 关于 .out 生成：不使用 cyaron 的 io.output_gen（其写缓冲不显式 flush 时可能留下
#   0 字节 .out）。本脚本用 subprocess 显式把 problemN.in 喂给 std，直接写 problemN.out，
#   并在末尾断言 .out 非空、行数 == 组数 T、每行都是非负整数。
#
# ⚠ 性能：本题 std 为 O(3^n + n·2^n·log MOD)，n ≤ 10；顶格点 (h=w=m=10000, n=10, T=5)
#   实测远低于 config.json 的 2000 ms。生成器只做 O(n) 的随机构造，无 O(n²) Python 循环。
#
# 分层（10 个测试点，从最小铺到顶格）：
#   点 1     边界层：h=w=m=n=1，单格 1×1 限制 v=1，答案 1
#   点 2     边界层：n=1/n=2、全最大值单格 (m=10000)、答案 0 的矛盾构造、m=1 全 1 构造
#   点 3     小规模：题面【输入样例】原样（T=2 → 28 / 76475）
#   点 4     小规模随机：h,w,m∈[2,6]，n∈[1,3]（可手算量级）
#   点 5     中等规模随机：h,w∈[50,500]，m∈[50,500]，n∈[3,6]
#   点 6     中等规模随机：h,w∈[500,3000]，m∈[500,3000]，n∈[5,8]
#   点 7     大规模随机：h,w∈[3000,8000]，m∈[3000,8000]，n∈[8,10]
#   点 8     大规模随机：h,w∈[8000,10000]，m∈[8000,10000]，n∈[8,10]（贴近上限）
#   点 9     顶格层：h=w=m=10000，n=10，随机大子矩阵，T=5
#   点 10    顶格层（最坏结构）：h=w=m=10000，n=10，T=5：
#              (A) 10 个完全相同的整矩阵限制 v=m —— 容斥最坏（子集并集全同）
#              (B) 严格嵌套链 S_1⊃…⊃S_10，v 严格递减 —— 分层最深
#              (C) 10 个大子矩阵同 v=m 且两两重叠 —— 等值组容斥最坏
#              (D) 一个 v=1 的小限制 + 若干 v=m 的大限制 —— 触发 (v-1)=0 与 0^0 约定
#              (E) 10 个相同的 1×1 限制 v=m + 整矩阵限制 v=m —— 退化面积
#
# 随机性：每个点用独立 random.Random(1783 + 点号)，与调用顺序无关，可精确复现。

import os
import random
import subprocess

from cyaron import IO  # 引入 CYaRon 的库

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "std")            # 直接编译在题目目录
if not os.path.exists(STD):
    STD = os.path.join(HERE, "..", "std")  # 兼容从 data/ 运行时 std 在上层

MAXH = MAXW = MAXM = 10000  # 题面上限


def rect(h, w, m, rng):
    """随机合法子矩阵 (x1,y1,x2,y2,v)。"""
    x1 = rng.randint(1, h)
    x2 = rng.randint(1, h)
    if x1 > x2:
        x1, x2 = x2, x1
    y1 = rng.randint(1, w)
    y2 = rng.randint(1, w)
    if y1 > y2:
        y1, y2 = y2, y1
    return (x1, y1, x2, y2, rng.randint(1, m))


def rand_case(h, w, m, n, rng):
    return (h, w, m, [rect(h, w, m, rng) for _ in range(n)])


def consistent_case(h, w, m, rects, rng):
    """由“隐藏填数”反推 v，保证构造出的实例一定有解（答案 ≥ 1），避免随机 v 大量退化到 0。

    做法：把矩阵按所有子矩阵的边界做坐标压缩（至多 21×21 个压缩格），给每个压缩格随机
    取 1..m 的值，再把每条限制的 v 设为它在隐藏填数下覆盖区域的最大值。这样隐藏填数本身就是
    一个合法方案，实例必然可满足，同时 v 分布自然、限制间关系多样。
    复杂度 O(n²)（n = 限制条数 ≤ 10），无矩阵级循环。
    """
    xs = sorted(set([1, h + 1] + [r[0] for r in rects] + [r[2] + 1 for r in rects]))
    ys = sorted(set([1, w + 1] + [r[1] for r in rects] + [r[3] + 1 for r in rects]))
    nx, ny = len(xs) - 1, len(ys) - 1
    t = [[rng.randint(1, m) for _ in range(ny)] for _ in range(nx)]
    cons = []
    for (x1, y1, x2, y2, _v) in rects:
        mx = 0
        for i in range(nx):
            if not (xs[i] >= x1 and xs[i + 1] - 1 <= x2):
                continue
            for j in range(ny):
                if ys[j] >= y1 and ys[j + 1] - 1 <= y2 and t[i][j] > mx:
                    mx = t[i][j]
        cons.append((x1, y1, x2, y2, mx))
    return (h, w, m, cons)


def fmt(cases):
    lines = [str(len(cases))]
    for h, w, m, cons in cases:
        lines.append("%d %d %d %d" % (h, w, m, len(cons)))
        for c in cons:
            lines.append("%d %d %d %d %d" % c)
    return "\n".join(lines) + "\n"


def gen(i, cases, note):
    """写出 problemN.in（cyaron），再用 subprocess 跑 std 生成 problemN.out，并做断言。"""
    io = IO(file_prefix="problem", data_id=i)
    io.input_write(fmt(cases))
    io.close()  # 显式 flush + 关闭 .in（避免缓冲问题）

    inp = "problem%d.in" % i
    outp = "problem%d.out" % i
    with open(inp, "rb") as fi, open(outp, "wb") as fo:
        r = subprocess.run([STD], stdin=fi, stdout=fo, timeout=120)
    assert r.returncode == 0, "problem%d: std 返回码 %d" % (i, r.returncode)

    assert os.path.getsize(outp) > 0, "problem%d: .out 为 0 字节（无解空输出点除外）" % i
    with open(outp) as f:
        out_lines = [ln for ln in f.read().splitlines() if ln.strip() != ""]
    assert len(out_lines) == len(cases), \
        "problem%d: 输出行数 %d != 组数 %d" % (i, len(out_lines), len(cases))
    for ln in out_lines:
        assert ln.strip().isdigit(), "problem%d: 输出行含非数字 %r" % (i, ln)
        assert 0 <= int(ln) < 1000000007, "problem%d: 输出越界 %r" % (i, ln)

    print("problem%-2d T=%-2d %s | out=%s%s"
          % (i, len(cases), note, ",".join(out_lines[:4]),
             ",..." if len(out_lines) > 4 else ""))


# ---------------- 点 1：边界层（最小规模） ----------------
gen(1, [(1, 1, 1, [(1, 1, 1, 1, 1)])],
    "边界层：h=w=m=n=1，单格限制 v=1，答案恒为 1")

# ---------------- 点 2：边界层（n=1/n=2、答案 0、全最大值、m=1） ----------------
gen(2, [
        (1, 1, MAXM, [(1, 1, 1, 1, MAXM)]),                       # n=1，m 顶格，答案 10000
        (2, 2, 5, [(1, 1, 2, 2, 3), (1, 1, 1, 1, 5)]),            # n=2，矛盾 → 答案 0
        (3, 3, 1, [(1, 1, 3, 3, 1), (2, 2, 2, 2, 1)]),            # m=1 全 1，恒 1 种
    ],
    "边界层：n=1(m顶格单格) / n=2 矛盾构造(答案0) / m=1 全 1")

# ---------------- 点 3：小规模（题面样例原样） ----------------
gen(3, [
        (3, 3, 2, [(1, 1, 2, 2, 2), (2, 2, 3, 3, 1)]),
        (4, 4, 4, [(1, 1, 2, 3, 3), (2, 3, 4, 4, 2), (2, 1, 4, 3, 2), (1, 2, 3, 4, 4)]),
    ],
    "小规模：题面【输入样例】原样（期望 28 / 76475）")

# ---------------- 点 4：小规模随机（可手算量级） ----------------
_rng = random.Random(1783 + 4)
_p4 = []
for _ in range(2):
    _h, _w, _m = _rng.randint(2, 6), _rng.randint(2, 6), _rng.randint(2, 6)
    _rs = [rect(_h, _w, _m, _rng) for _ in range(_rng.randint(1, 3))]
    _p4.append(consistent_case(_h, _w, _m, _rs, _rng))
gen(4, _p4, "小规模随机(有解构造)：h,w,m∈[2,6]，n∈[1,3]")

# ---------------- 点 5：中等规模随机 ----------------
_rng = random.Random(1783 + 5)
_p5 = []
for _ in range(3):
    _h, _w, _m = _rng.randint(50, 500), _rng.randint(50, 500), _rng.randint(50, 500)
    _rs = [rect(_h, _w, _m, _rng) for _ in range(_rng.randint(3, 6))]
    _p5.append(consistent_case(_h, _w, _m, _rs, _rng))
gen(5, _p5, "中等规模随机(有解构造)：h,w,m∈[50,500]，n∈[3,6]")

# ---------------- 点 6：中等规模随机 ----------------
_rng = random.Random(1783 + 6)
_p6 = []
for _ in range(3):
    _h, _w, _m = _rng.randint(500, 3000), _rng.randint(500, 3000), _rng.randint(500, 3000)
    _rs = [rect(_h, _w, _m, _rng) for _ in range(_rng.randint(5, 8))]
    _p6.append(consistent_case(_h, _w, _m, _rs, _rng))
gen(6, _p6, "中等规模随机(有解构造)：h,w,m∈[500,3000]，n∈[5,8]")

# ---------------- 点 7：大规模随机 ----------------
_rng = random.Random(1783 + 7)
_p7 = []
for _ in range(4):
    _h, _w, _m = _rng.randint(3000, 8000), _rng.randint(3000, 8000), _rng.randint(3000, 8000)
    _rs = [rect(_h, _w, _m, _rng) for _ in range(_rng.randint(8, 10))]
    _p7.append(consistent_case(_h, _w, _m, _rs, _rng))
gen(7, _p7, "大规模随机(有解构造)：h,w,m∈[3000,8000]，n∈[8,10]")

# ---------------- 点 8：大规模随机（贴近上限） ----------------
_rng = random.Random(1783 + 8)
_p8 = []
for _ in range(5):
    _h, _w, _m = _rng.randint(8000, MAXH), _rng.randint(8000, MAXW), _rng.randint(8000, MAXM)
    _rs = [rect(_h, _w, _m, _rng) for _ in range(_rng.randint(8, 10))]
    _p8.append(consistent_case(_h, _w, _m, _rs, _rng))
gen(8, _p8, "大规模随机(有解构造)：h,w,m∈[8000,10000]，n∈[8,10]（贴近上限）")


def big_rect(h, w, rng, lo=0.3):
    """大子矩阵（边长占比 ≥ lo），用于顶格层制造大面积交并。"""
    x1 = rng.randint(1, max(1, int(h * (1 - lo))))
    y1 = rng.randint(1, max(1, int(w * (1 - lo))))
    x2 = rng.randint(min(h, x1 + int(h * lo)), h)
    y2 = rng.randint(min(w, y1 + int(w * lo)), w)
    return (x1, y1, x2, y2)


# ---------------- 点 9：顶格层（上限 + 随机大子矩阵，有解构造） ----------------
_rng = random.Random(1783 + 9)
_p9 = []
for _ in range(5):
    _rs = []
    for _j in range(10):
        x1, y1, x2, y2 = big_rect(MAXH, MAXW, _rng)
        _rs.append((x1, y1, x2, y2, 0))
    _p9.append(consistent_case(MAXH, MAXW, MAXM, _rs, _rng))
gen(9, _p9, "顶格层：h=w=m=10000，n=10 随机大子矩阵(有解构造)，T=5")

# ---------------- 点 10：顶格层（最坏结构） ----------------
_p10 = []

# (A) 10 个完全相同的整矩阵限制 v=m —— 子集交并全同，容斥最坏
_p10.append((MAXH, MAXW, MAXM, [(1, 1, MAXH, MAXW, MAXM)] * 10))

# (B) 严格嵌套链 S_1⊃S_2⊃…⊃S_10，v 严格递减 —— 分层最深
_chain = []
for k in range(10):
    _chain.append((1 + k, 1 + k, MAXH - k, MAXW - k, MAXM - k))
_p10.append((MAXH, MAXW, MAXM, _chain))

# (C) 10 个大子矩阵同 v=m 且两两重叠 —— 等值组容斥最坏
_rng = random.Random(1783 + 10)
_cons_c = []
for _j in range(10):
    x1, y1, x2, y2 = big_rect(MAXH, MAXW, _rng, lo=0.5)
    _cons_c.append((x1, y1, x2, y2, MAXM))
_p10.append((MAXH, MAXW, MAXM, _cons_c))

# (D) 一个 v=1 的小限制 + 若干 v=m 的大限制 —— 触发 (v-1)=0 与 0^0 约定
_cons_d = [(5000, 5000, 5001, 5001, 1)]
for _j in range(9):
    x1, y1, x2, y2 = big_rect(MAXH, MAXW, _rng, lo=0.4)
    _cons_d.append((x1, y1, x2, y2, MAXM))
_p10.append((MAXH, MAXW, MAXM, _cons_d))

# (E) 10 个相同的 1×1 限制 v=m + 整矩阵限制 v=m —— 退化面积/重复限制
_cons_e = [(1, 1, 1, 1, MAXM)] * 9 + [(1, 1, MAXH, MAXW, MAXM)]
_p10.append((MAXH, MAXW, MAXM, _cons_e))

gen(10, _p10,
    "顶格最坏结构：同整矩阵×10 / 嵌套链 / 同值大重叠 / v=1 触发 0^0 / 退化 1×1 重复")

print("自检通过：10 个测试点 .in/.out 成对齐全，.out 非空且行数 == 组数 T。")
