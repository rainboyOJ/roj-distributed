#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 一本通 2032《【例4.18】分解质因数》分层数据生成器（cyaron）
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py
# 参考仓库惯例：problems/1000/data.py、problems/5006/data.py、.ybt-import/staging/2030/data.py
#
# 题意：输入一个正整数 n，输出 n 的质因数分解式 "n=p1*p2*...*pk"，
#       质因数（含重复）由小到大排列，如 36 -> "36=2*2*3*3"。
# 数据范围（题面【提示】明文，官方 OJ 页 http://ybt.ssoier.cn:8088/problem_show.php?pid=2032 一致）：
#       2 <= n <= 20000（单组输入，一个测试点 = 一个 n）。
# 限制：time 1000 ms / memory 65536 KB（config.json 与官方页一致）。
#
# ---- 分层策略（单组输入题：一个测试点 = 一个 n；务必先读这里）----
#   本题每个测试点只能承载**一个 n**，而任务书「边界层」清单点名要求覆盖
#   最小/最大、答案为"只有 1 个质因数"的极端、题面声明的特殊值（样例 36）——
#   这些是互斥的输入值，2 个测试点装不下。因此与同卷 staging/2030 一致，
#   把边界层扩为**点 1-4**（清单 100% 覆盖），后续层次顺延，规模仍严格
#   从最小铺到顶格：
#
#     点 1 ｜边界层｜n=2（=全最小值，质数）
#       最小合法输入；n 为质数 ⇒ 分解式恰 1 个质因数、**完全不出现 '*'**，
#       是"答案只有 1 个因子"的极端；也抓"只处理合数、把质数漏打"的实现。
#     点 2 ｜边界层｜n=4（=最小合数，2*2）
#       题面原文"分解质因数只针对合数"，4 是范围内最小合数；
#       答案含**重复因子** 2*2：逼出"每个质因子必须按重数重复输出"与
#       "乘号印在因子之间"（4=2*2 不能写成 4=2、4=2*2*、4=2×2）。
#     点 3 ｜边界层（题面声明的特殊值）｜n=36
#       题面【输入样例】原样，输出必须逐字节等于 "36=2*2*3*3\n"（见下方自检）。
#     点 4 ｜边界层｜n=20000（=全最大值）
#       上界顶格；20000 = 2^4 * 5^4（两个质数的高次幂混合），
#       同时检验上界处的重复因子与因子排序（2 必须全部在 5 前面）。
#     点 5 ｜小规模随机｜n=134（=2*67）
#       百量级**两不同质数**（半素数），可手算核验；随机抽自 [100,900]（种子 2032）。
#     点 6 ｜小规模随机｜n=772（=2^2*193）
#       百量级：**重复因子 + 大质数尾巴** 193 > sqrt(772)≈27.8，可手算；
#       随机抽自 [100,900]（种子 2032 的后续抽），互补点 5 的无重数形态。
#     点 7 ｜中等规模随机｜n=7435（=5*1487）
#       千量级随机；尾部质因子 1487 > 1000 且 >> sqrt(7435)≈86.2，
#       专门检验"试除到 sqrt 后剩余的商必须补打"这类实现（写错会输出 7435=5）。
#     点 8 ｜大规模随机（接近上限）｜n=16977（=3*5659）
#       贴上限带 [15000,19999] 随机；尾因子 5659 是范围内很大的质数（> sqrt(16977)≈130.3），
#       与点 7 一起覆盖"大质数尾巴"在接近上限处的同构情形。
#     点 9 ｜顶格层（按题型构造最坏结构）｜n=16384
#       [2,20000] 内 **质因数重数最大** Ω(n)=14（2^14）：分解式最长（14 个因子、
#       13 个 '*'），输出量最大、'*' 数量最多，是输出格式的最坏结构。
#     点 10｜顶格层（按题型构造最坏结构）｜n=19950
#       [2,20000] 内 **不同质因数个数最大** ω(n)=5，且是所有 ω=5 的数中**最大的**
#       （19950 = 2*3*5*5*7*19，同时含重复因子 5*5）：因子枚举完整性 + 贴近上限，
#       任何漏枚举质因子/排序错误/重数与种类数混淆都会暴露。（附：19866=2*3*7*11*43
#       是范围内最大的**无平方因子**且 ω=5 的数，本条已由点 10 的最大性一并覆盖。）
#
#   结论：10 个点覆盖 边界 4 + 小规模 2 + 中等 1 + 大规模 1 + 顶格 2，
#   从最小值 2 一路铺到最大值 20000，**无任何重复值**，
#   不存在「10 个点全是小随机」；点 4/8/9/10 均贴 [15000,20000] 上限带。
#
# ---- 精度口径 ----
#   本题**全程整数运算，无浮点**：不存在 %g / printf 尾零等跨平台文本差异。
#   输出为精确十进制整数 + '*' + 单个换行，macOS / glibc / Windows 逐字节一致。
#   点 3 的输出与题面【输出样例】逐字节比对（"36=2*2*3*3\n"）。
#
# ---- 可复现性 ----
#   点 5-8 的随机 n 用固定种子 random.Random(2032) + 拒绝采样在 Python 侧一次算定，
#   下方断言把抽到的值钉死（134/772/7435/16977），跨 Python 版本/平台重跑
#   逐字节一致（若某版本随机流变化会直接 assert 失败，而不是静默换数据）。

from cyaron import *  # 引入CYaRon的库

import os
import random

NMIN, NMAX = 2, 20000  # 题面【提示】明文范围

# ---------------------------------------------------------------------------
# 固定种子抽取点 5-8 的随机值（钉死为常量，见上方"可复现性"）
# ---------------------------------------------------------------------------
def _factor_list(m):
    """内部小工具：试除分解，返回质因子列表（本文件自检也复用）。"""
    fs = []
    d = 2
    while d * d <= m:
        while m % d == 0:
            fs.append(d)
            m //= d
        d += 1
    if m > 1:
        fs.append(m)
    return fs


RNG = random.Random(2032)


def _draw_pred(lo, hi, pred):
    """在 [lo,hi] 上按固定种子随机抽数直到满足 pred（拒绝采样，结果确定）。"""
    while True:
        v = RNG.randint(lo, hi)
        if pred(v):
            return v


# 点 5：小规模随机｜两不同质数的半素数
_rand_n5 = _draw_pred(100, 900, lambda v: len(_factor_list(v)) == 2
                      and len(set(_factor_list(v))) == 2)
# 点 6：小规模随机｜含重复因子且因子数 >= 3（互补点 5）
_rand_n6 = _draw_pred(100, 900, lambda v: len(_factor_list(v)) >= 3
                      and len(_factor_list(v)) > len(set(_factor_list(v))))
# 点 7：中等规模随机｜尾部质因子 > 1000（远超 sqrt）
_rand_n7 = _draw_pred(1000, 9000, lambda v: len(_factor_list(v)) >= 2
                      and max(_factor_list(v)) > 1000)
# 点 8：大规模随机（接近上限）｜尾部质因子 > 3000
_rand_n8 = _draw_pred(15000, 19999, lambda v: len(_factor_list(v)) >= 2
                      and max(_factor_list(v)) > 3000)
assert (_rand_n5, _rand_n6, _rand_n7, _rand_n8) == (134, 772, 7435, 16977), \
    "固定种子抽取结果与预期不符：%r" % ((_rand_n5, _rand_n6, _rand_n7, _rand_n8),)

# ---------------------------------------------------------------------------
# cyaron 生成：10 组，每组一个 n，输出由已编译的 ../std 生成
# ---------------------------------------------------------------------------
CASES = [
    (1, 2,     "边界层｜全最小值 n=2（质数）：答案恰 1 个质因数、无 '*'"),
    (2, 4,     "边界层｜最小合数 n=4（2*2）：题面只说合数，最小合数 + 重复因子"),
    (3, 36,    "边界层(题面特殊值)｜【输入样例】n=36：输出须逐字节为 \"36=2*2*3*3\\n\""),
    (4, 20000, "边界层｜全最大值 n=20000（2^4*5^4）：上界顶格 + 重复因子 + 因子排序"),
    (5, _rand_n5, "小规模随机｜n=134（2*67）：百量级两不同质数，可手算"),
    (6, _rand_n6, "小规模随机｜n=772（2*2*193）：重复因子 + 尾质因子 193 > sqrt(n)"),
    (7, _rand_n7, "中等规模随机｜n=7435（5*1487）：尾质因子 >1000 且 >> sqrt(n)"),
    (8, _rand_n8, "大规模随机(接近上限)｜n=16977（3*5659）：近上限处的大质数尾巴"),
    (9, 16384, "顶格层(最坏结构)｜n=16384=2^14：范围内重数最大 Ω=14，分解式最长"),
    (10, 19950, "顶格层(最坏结构)｜n=19950=2*3*5*5*7*19：范围内不同质因数最多 ω=5 且最大"),
]

# 前置断言：data_id 与 n 全部合法且互不重复
ids = [c[0] for c in CASES]
ns = [c[1] for c in CASES]
assert sorted(ids) == list(range(1, 11)), "data_id 必须恰为 1..10"
assert len(set(ns)) == len(ns), "测试点取值不得重复"
assert all(NMIN <= n <= NMAX for n in ns), "存在超出题面范围 [2,20000] 的 n"
assert os.path.exists("../std"), "请先编译 std：g++ -O2 -std=c++17 std.cpp -o std"

for data_id, n, note in CASES:
    io = IO(file_prefix="problem", data_id=data_id)  # problem{i}.in / problem{i}.out
    io.input_writeln(n)                              # 单行 "n\n"
    io.output_gen("../std")                          # 调用 ../std 产出 .out
    io.close()                                       # 刷盘，保证后面读取 .in/.out 是最新的
    print("problem%-2d n=%-5d %s" % (data_id, n, note))

# ---------------------------------------------------------------------------
# 自检 1：Python 侧独立真值（试除分解）核对全部 10 组 .out，逐字节
# ---------------------------------------------------------------------------
def factor_string(n):
    """独立真值：试除分解（与 std 的"从小至大试除 + 循环后补尾商"实现路径独立编写）"""
    m, fs = n, []
    d = 2
    while d * d <= m:
        while m % d == 0:
            fs.append(d)
            m //= d
        d += 1
    if m > 1:
        fs.append(m)
    return "%d=%s\n" % (n, "*".join(str(f) for f in fs))


problems = 0
for data_id, n, _note in CASES:
    with open("problem%d.in" % data_id, "rb") as f:
        in_bytes = f.read()
    with open("problem%d.out" % data_id, "rb") as f:
        out_bytes = f.read()
    assert in_bytes == ("%d\n" % n).encode(), \
        "problem%d.in 应为 %r，实际 %r" % (data_id, ("%d\n" % n).encode(), in_bytes)
    expect = factor_string(n).encode()
    assert out_bytes == expect, \
        "problem%d.out 与独立真值不符：期望 %r，实际 %r" % (data_id, expect, out_bytes)
    problems += 1
print("自检：%d 组 .in/.out 与 Python 独立真值逐字节一致" % problems)

# 自检 2：点 3 必须逐字节等于题面【输出样例】
with open("problem3.out", "rb") as f:
    sample_out = f.read()
assert sample_out == b"36=2*2*3*3\n", "样例输出不符：%r" % sample_out
print("自检：problem3.out == b'36=2*2*3*3\\n'（题面【输出样例】逐字节一致）")

# 自检 3：点 9/点 10 的结构性声明必须为真（Ω 最大 / ω 最大）
big_omega_max = max((len(_factor_list(m)), m) for m in range(NMIN, NMAX + 1))
small_omega_max = max((len(set(_factor_list(m))), m) for m in range(NMIN, NMAX + 1))
assert big_omega_max == (14, 16384), "Ω 最大值声明不符：%r" % (big_omega_max,)
assert small_omega_max == (5, 19950), "ω 最大值声明不符：%r" % (small_omega_max,)
print("自检：Ω 最大 = 14 @ n=16384；ω 最大 = 5 @ n=19950（均与测试点一致）")

# 自检 4：输出规模与点 9 最长分解式
longest = max((len(factor_string(m)), m) for m in range(NMIN, NMAX + 1))
print("自检：范围内最长分解式长度 = %d 字节 @ n=%d（点 9 覆盖）" % longest)
print("全部自检通过。")
