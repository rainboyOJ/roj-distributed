#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 一本通 2030《【例4.16】找素数》分层数据生成器（cyaron）
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py
# 参考仓库惯例：problems/1000/data.py、problems/5006/data.py、.ybt-import/staging/2026/data.py
#
# 题意：输入 a,b，由小到大输出 [a,b] 内所有素数，每个数占一行。
# 数据范围（题面【提示】明文，官方 OJ 页 http://ybt.ssoier.cn:8088/problem_show.php?pid=2030 一致）：
#   1 <= a <= b <= 20000。
# 限制：time 1000 ms / memory 65536 KB（config.json 与官方页一致）。
#
# ---- 分层策略（单组输入题：一个测试点 = 一个 (a,b) 对；务必先读这里）----
#   本题每个测试点只能承载**一对 (a,b)**，而任务书「边界层」清单里点名要求覆盖
#   1、2、全最小值、全最大值、答案为 0 或 1 的极端、题面声明的特殊值 (5 10) ——
#   这些是互斥的输入对，2 个测试点装不下。因此本包把边界层扩到**点 1-4**
#   （覆盖清单 100%，见下表标注），后面的层次整体顺延，规模依然严格从最小铺到顶格：
#
#     点 1 ｜边界层｜(1,1)
#       全最小值 + 答案为 **0 个素数**的空输出极端 + 退化区间 a=b；
#       核心考验「1 既不是质数也不是合数」必须排除（打印 1 即错）。
#     点 2 ｜边界层｜(2,2)
#       最小素数 n=2 + 答案为**恰 1 行**的极端 + a=b 退化；
#       常见错误「偶数都跳过」会把 2 一起漏掉，此点唯一命中。
#     点 3 ｜边界层（题面声明的特殊值）｜(5,10)
#       题面【输入样例】原样，输出必须逐字节等于【输出样例】"5\n7"（见 data.py 自检与 gen-report）。
#     点 4 ｜边界层｜(20000,20000)
#       全最大值 a=b=20000（=2^4·5^4，合数）+ 上界退化 + 空输出；
#       专抓上界开闭写错（n < b / n <= b 混淆）与「上界附近不判定」的漏判。
#     点 5 ｜小规模（确定、可手算）｜(1,100)
#       1..100 共 25 个素数；含 1 的排除、个位素数、4/9/25/49 等平方数误判测试。
#     点 6 ｜小规模随机｜(a,b) ⊆ [1,400]（种子生成）
#       ~百量级随机区间，可手算核验；随机开闭端点，覆盖 a 落在合数/素数上的两种情形。
#     点 7 ｜中等规模随机｜窗口 ⊆ [1,12000]，长度 2000~4000
#       中段规模随机；a、b 均随机，扫描量与输出量同时上岸。
#     点 8 ｜大规模随机（接近上限）｜窗口 ⊆ [5000,19000]，长度 5000~9000
#       单点扫描量数千~上万，输出数百行，接近题面上限的大规模随机。
#     点 9 ｜顶格层（按题型构造最坏结构）｜(19609,20000)
#       b 取题面上限；区间横跨 [1,20000] 内**最大素数间隙** 19609→19661
#       （52 个连续合数），且覆盖上界邻域全部素数 19961..19997：
#       稀疏区 + 上界端点同时上，检验「长连续合数段不误报、上界不遗漏」。
#     点 10｜顶格层（全长最大）｜(1,20000)
#       题面上限全长：（b-a+1）=20000 全部候选、2262 行最大输出量、
#       扫描+试除总工作量最大点（卡常/边界总检）。
#
#   结论：10 个点覆盖 边界 4 + 小规模 2 + 中等 1 + 大规模 1 + 顶格 2，
#   从 (1,1) 空输出一路铺到 (1,20000) 全长，**没有任何两点重复**，
#   不存在「10 个点全是小随机」；点 5-10 的输出行数单调放大（25→~2262）。
#
# ---- 精度口径 ----
#   本题**全程整数运算，无浮点**：不存在 %g / printf 尾零等跨平台文本差异。
#   输出为精确十进制整数 + 单个换行，macOS / glibc / Windows 逐字节一致。
#   点 3 的输出与题面【输出样例】逐字节比对（"5\n7\n"）。

from cyaron import *  # 引入CYaRon的库

import os
import random

AMIN, AMAX = 1, 20000  # 题面【提示】明文范围

# 固定种子 ⇒ 点 6/7/8 的随机区间完全可复现（同一台机器/任何机器均一致，
# 因为随机量在 Python 侧一次算定后以显式整数写入 .in，不依赖 cyaron 内部随机流）。
RNG = random.Random(2030)

# 每个测试点：(data_id, a, b, 分层标注)
# 点 6/7/8 的值由固定种子 RNG 在**生成时**算出（见下方代码，同一 Python 版本/平台
# 结果确定；即便跨版本随机流微变，跑一次后写死到 CASES 即可逐字节复现）。
CASES = []


def _add(data_id, a, b, note):
    assert AMIN <= a <= b <= AMAX, "非法数据点 (%d,%d) 超出 [%d,%d]" % (a, b, AMIN, AMAX)
    CASES.append((data_id, a, b, note))


# ---- 点 1-5：边界层 + 小规模确定值 ----
_add(1, 1, 1, "边界层｜全最小值 a=b=1：答案为空（0 个素数），必须排除 1；退化区间")
_add(2, 2, 2, "边界层｜最小素数 a=b=2：答案恰 1 行；防「偶数全跳过」把 2 漏掉")
_add(3, 5, 10, "边界层(题面特殊值)｜【输入样例】原样：输出须逐字节为 \"5\\n7\\n\"")
_add(4, 20000, 20000, "边界层｜全最大值 a=b=20000(=2^4*5^4 合数)：空输出；抓上界开闭写错")
_add(5, 1, 100, "小规模(确定/可手算)｜1..100 共 25 个素数；含 1 排除与 4/9/25/49 平方误判")

# ---- 点 6：小规模随机 ⊆ [1,400]，长度 ≥ 30（避免退化成单点）----
_len6 = RNG.randint(30, 150)
_a6 = RNG.randint(1, 400 - _len6 + 1)
_b6 = _a6 + _len6 - 1
_add(6, _a6, _b6, "小规模随机｜区间 ⊆ [1,400]，长度 %d（种子 2030 复现），百量级可手算核验" % _len6)

# ---- 点 7：中等规模随机，窗口 ⊆ [1,12000]，长度 2000~4000 ----
_len7 = RNG.randint(2000, 4000)
_a7 = RNG.randint(1, 12000 - _len7 + 1)
_b7 = _a7 + _len7 - 1
_add(7, _a7, _b7, "中等规模随机｜窗口 ⊆ [1,12000]，长度 %d；中段规模扫描+输出上岸" % _len7)

# ---- 点 8：大规模随机（接近上限），窗口 ⊆ [5000,19000]，长度 5000~9000 ----
_len8 = RNG.randint(5000, 9000)
_a8 = RNG.randint(5000, 19000 - _len8 + 1)
_b8 = _a8 + _len8 - 1
_add(8, _a8, _b8, "大规模随机(近上限)｜窗口 ⊆ [5000,19000]，长度 %d；大规模扫描+数百行输出" % _len8)

# ---- 点 9-10：顶格层 ----
_add(9, 19609, 20000,
     "顶格层(最坏结构)｜b=上限20000；横跨最大素数间隙 19609→19661(52 个连续合数)，"
     "含上界邻域素数 19961..19997：稀疏区+上界端点同时考验")
_add(10, 1, 20000,
     "顶格层(全长最大)｜题面上限全长 (b-a+1)=20000、2262 行最大输出、最大总工作量")

assert len(CASES) == 10, "必须恰好 10 个测试点"
assert len({(a, b) for _, a, b, _ in CASES}) == 10, "10 个测试点不得重复"

# ---- Python 独立真值（埃氏筛，与 std 的 6k±1 试除是两条独立路径）----
_SIEVE_N = AMAX
_IS_PRIME = bytearray([1]) * (_SIEVE_N + 1)
_IS_PRIME[0] = _IS_PRIME[1] = 0
for _i in range(2, int(_SIEVE_N ** 0.5) + 1):
    if _IS_PRIME[_i]:
        for _j in range(_i * _i, _SIEVE_N + 1, _i):
            _IS_PRIME[_j] = 0


def truth(a, b):
    """独立真值：返回 [a,b] 内素数的期望输出文本（每数一行，行末换行）。"""
    return "".join("%d\n" % n for n in range(a, b + 1) if _IS_PRIME[n])


def gen_case(data_id, a, b, note):
    io = IO(file_prefix="problem", data_id=data_id)   # problem{data_id}.in / .out
    io.input_writeln(a, b)                            # "a b\n"（空格分隔 + 行末换行）
    io.output_gen("../std")                           # .out 由 std 生成
    nprime = sum(1 for n in range(a, b + 1) if _IS_PRIME[n])
    print("problem%-2d: a=%-5d b=%-5d 输出 %-5d 行 -- %s" % (data_id, a, b, nprime, note))


def self_check():
    """生成后立即审计：成对齐全、输入格式合规、std 输出与 Python 筛法真值逐字节一致。"""
    bad = 0
    for data_id, a, b, _note in CASES:
        in_path, out_path = "problem%d.in" % data_id, "problem%d.out" % data_id
        try:
            raw_in = open(in_path, "r", encoding="utf-8").read()
            raw_out = open(out_path, "r", encoding="utf-8").read()
        except OSError as exc:
            print("MISSING pair for point %d: %s" % (data_id, exc))
            bad += 1
            continue
        want_in = "%d %d\n" % (a, b)
        want_out = truth(a, b)
        if raw_in != want_in:
            print("BAD INPUT problem%d.in: %r (expect %r)" % (data_id, raw_in, want_in))
            bad += 1
        if raw_out != want_out:
            got_lines = raw_out.splitlines()
            exp_lines = want_out.splitlines()
            print("OUTPUT != TRUTH problem%d: got %d lines expect %d lines (a=%d b=%d)"
                  % (data_id, len(got_lines), len(exp_lines), a, b))
            bad += 1
    # 题面样例逐字节核对（点 3）
    sample_out = open("problem3.out", encoding="utf-8").read()
    if sample_out != "5\n7\n":
        print("SAMPLE MISMATCH: problem3.out=%r expect '5\\n7\\n'" % sample_out)
        bad += 1
    if bad:
        print("SELF-CHECK FAILED: %d issue(s)" % bad)
        raise SystemExit(1)
    print("SELF-CHECK OK: 10/10 pairs, inputs well-formed, outputs == Python 埃氏筛真值"
          " (含题面样例 5 10 -> 5\\n7\\n 逐字节比对)")
    print("分层覆盖：边界 4 点 + 小规模 2 点 + 中等 1 点 + 大规模 1 点 + 顶格 2 点")


if __name__ == "__main__":
    assert os.path.exists("../std"), "../std 未编译，先执行 g++ -O2 -std=c++17 ../std.cpp -o ../std"
    for _data_id, _a, _b, _note in CASES:
        gen_case(_data_id, _a, _b, _note)
    self_check()
