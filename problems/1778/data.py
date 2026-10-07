#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 一本通 1778《好数字》（目标 ROJ 题号 1778）分层测试数据生成器
#
# 题意：2n 位数字（允许前导 0，每位属于给定数字集合 S）称为好数字，若
#       「前 n 位之和 == 后 n 位之和」或「奇数位之和 == 偶数位之和」；求好数字个数 mod 999983。
#       输入：第一行 n；第二行一个长度不超过 10 的字符串表示 S。
#       输出：一行一个整数。
#
# 数据范围（题面【提示】原文）：20% 的数据 n ≤ 7；100% 的数据 n ≤ 1000，|S| ≤ 10。
#
# 分层设计（10 组，从最小铺到顶格；n 与 |S| 两个维度同时铺满）：
#   1  边界：n=1, |S|=1（S="0"）—— 最小 n + 最小 |S|，全 0 退化，答案恒为 1。
#   2  边界：n=1, |S|=10（S="0123456789"）—— 最小 n + 最大 |S|，答案 = |S| = 10（可解析验证）。
#   3  小规模：n=2, S="0987654321" —— 题面【输入样例】，答案 1240（题面声明值）。
#   4  小规模：n=2, S="12" —— 题面描述中直接给出的例子（n=2,S={1,2} → 8 个）。
#   5  20% 档上界：n=7, S="13579" —— 题面「n ≤ 7」子任务的上界，|S|=5 全奇数集。
#   6  中等 + 退化：n=64, S="5" —— |S|=1 退化在中等规模下的表现，答案恒为 1。
#   7  中等偏大：n=100, |S|=10 顶格（S="0123456789"）。
#   8  大规模（n 偶）：n=500, S="123456789"（|S|=9）—— 覆盖 n 为偶数分支（l1 == l2）。
#   9  大规模（n 奇）：n=999, |S|=10 顶格 —— 覆盖 n 为奇数分支（l1 = (n+1)/2 ≠ l2 = n/2）。
#  10  顶格：n=1000 顶格 + |S|=10 顶格 —— 本题最大规模（DP 表最大、内层总代价最大）。
#
# 覆盖对照：n ∈ {1,2,7,64,100,500,999,1000}（含最小/20%上界/顶格，奇偶皆有）；
#           |S| ∈ {1,5,9,10}（含最小 1 与最大 10）；S 的给出顺序含降序（"0987654321"，
#           与题面样例一致）与升序（"0123456789"），验证实现不依赖字符串顺序。
#
# 答案锚点说明（EXPECT）：
#   * 解析可证（独立于标程算法，非暴力/对拍）：
#       - |S| = 1 ⇒ 答案恒为 1（2n 位全同数字，两个条件同时成立且唯一）→ 点 1、点 6；
#       - n = 1 ⇒ 答案 = |S|（2 位数字 a b：两条件都要求 a == b）→ 点 2（= 10）；
#       - 点 3 = 1240（题面【输出样例】）、点 4 = 8（题面描述举例）。
#   * 其余点（5、7、8、9、10）的 EXPECT 为标程输出的**回归锚点**（本次一次性钉死，
#     用途是后续重跑 data.py 时若数值漂移立即报错），并非独立复算结果——
#     本次任务书禁止写 brute/对拍，故未做独立第二实现复算（已在 gen-report.md 如实记录）。
#
# 用法：在本目录（staging/1778/）直接运行：
#   nice -n 19 timeout 120 python3 data.py
# 脚本自动切到 data/ 子目录，产物为 problem1..10.in/.out（cyaron IO 写到 cwd，../std 为本目录标程）。
# 交付包已清理编译产物（无 ./std）；此时脚本会用 g++ 从 std.cpp 现场编译，保证可一键复现。

import hashlib
import os
import subprocess

from cyaron import IO

if not os.path.isdir("data"):
    os.makedirs("data")
os.chdir("data")


def ensure_std():
    """../std 缺失（已清理编译产物）时，从 ../std.cpp 现场编译。"""
    if not os.path.exists("../std"):
        subprocess.check_call(["g++", "-O2", "-std=c++17", "../std.cpp", "-o", "../std"])
        print("compiled ../std from ../std.cpp")


ensure_std()

MOD = 999983

# 10 个正式测试点：(n, S)
CASES = [
    (1, "0"),
    (1, "0123456789"),
    (2, "0987654321"),
    (2, "12"),
    (7, "13579"),
    (64, "5"),
    (100, "0123456789"),
    (500, "123456789"),
    (999, "0123456789"),
    (1000, "0123456789"),
]

NOTES = [
    "boundary: n=1, |S|=1 (S=0) 最小规模，全 0 退化 -> 1",
    "boundary: n=1, |S|=10 最大数字集，答案=|S|=10",
    "small: 题面【输入样例】n=2, S=0987654321 -> 1240",
    "small: 题面描述举例 n=2, S={1,2} -> 8",
    "20% 档上界: n=7, |S|=5 全奇数集",
    "medium + 退化: n=64, |S|=1 -> 1",
    "medium: n=100, |S|=10 顶格",
    "large (n even): n=500, |S|=9 -> l1 == l2 分支",
    "large (n odd): n=999, |S|=10 顶格 -> l1 != l2 分支",
    "max: n=1000 顶格, |S|=10 顶格 -> 本题最大规模",
]

# 见文件头「答案锚点说明」
EXPECT = {
    1: 1,
    2: 10,
    3: 1240,
    4: 8,
    5: 798909,     # 标程回归锚点
    6: 1,
    7: 126623,     # 标程回归锚点
    8: 492598,     # 标程回归锚点
    9: 521511,     # 标程回归锚点
    10: 495241,    # 标程回归锚点
}

# 解析可证 / 题面声明的额外断言（(n, S) -> 期望答案），用于校验标程在已知值上正确。
ANALYTIC = [
    (1, "0123456789", 10),   # n=1 ⇒ 答案 = |S|
    (2, "12", 8),            # 题面描述举例
    (2, "0987654321", 1240),  # 题面输出样例
    (3, "12", 28),           # 手推：A=Σf2²=20，I=(Σf2²)(Σf1²)=6·2=12 ⇒ 2·20-12=28
    (5, "0", 1),             # |S|=1 ⇒ 1
    (1000, "7", 1),          # |S|=1 ⇒ 1（顶格 n 退化）
]


def run_std(n, s):
    """跑 ../std，返回 (答案字符串, 原始 stdout)。"""
    inp = ("%d\n%s\n" % (n, s)).encode()
    out = subprocess.run(["../std"], input=inp, stdout=subprocess.PIPE, check=True).stdout
    return out.decode().strip(), out


def dump(data_id, n, s, note):
    """写 problem<data_id>.in，用 ../std 生成 .out，并做非空/行数/值域/锚点自检。"""
    io = IO(file_prefix="problem", data_id=data_id)
    io.input_write("%d\n%s\n" % (n, s))
    io.output_gen("../std")
    io.close()  # 显式关闭（刷盘）后再自检，规避 cyaron 写缓冲未 flush 产出 0 字节 .out

    in_path = "problem%d.in" % data_id
    out_path = "problem%d.out" % data_id

    raw_in = open(in_path, "rb").read()
    raw_out = open(out_path, "rb").read()
    assert len(raw_in) > 0, "%s 为空（cyaron 写缓冲未 flush）" % in_path
    assert len(raw_out) > 0, "%s 为空（cyaron 写缓冲未 flush）" % out_path

    # .in 结构：2 行（n、S）
    in_lines = raw_in.decode().splitlines()
    assert len(in_lines) == 2, "%s 行数应为 2，实为 %d" % (in_path, len(in_lines))
    assert int(in_lines[0]) == n and in_lines[1] == s, "%s 内容与预期不符" % in_path

    # .out 结构：1 行非负整数，< MOD
    out_lines = raw_out.decode().splitlines()
    assert len(out_lines) == 1, "%s 行数应为 1，实为 %d" % (out_path, len(out_lines))
    got = out_lines[0].strip()
    assert got.isdigit(), "%s 非非负整数：%r" % (out_path, got)
    val = int(got)
    assert 0 <= val < MOD, "%s 超出 [0, 999983)：%d" % (out_path, val)

    exp = EXPECT[data_id]
    if val != exp:
        raise SystemExit("problem%d 答案不符：std=%d，锚点=%d" % (data_id, val, exp))
    print("problem%-2d: n=%-5d |S|=%-2d  %-52s ans=%d"
          % (data_id, n, len(s), note, val))


# ── 正式 10 个测试点 ──
for _i, (_n, _s) in enumerate(CASES, start=1):
    dump(_i, _n, _s, NOTES[_i - 1])

# ── 解析可证 / 题面声明值的额外断言（不产出数据文件） ──
for _n, _s, _exp in ANALYTIC:
    _got, _ = run_std(_n, _s)
    assert _got == str(_exp), \
        "解析锚点失败：n=%d S=%s -> %s，期望 %d" % (_n, _s, _got, _exp)
print("解析锚点全部通过：%d 组（含题面样例 1240、题面举例 8、n=1 ⇒ |S|、|S|=1 ⇒ 1）"
      % len(ANALYTIC))

# ── 产物清单与可复现性摘要 ──
h = hashlib.md5()
for _i in range(1, 11):
    for _suf in ("in", "out"):
        p = "problem%d.%s" % (_i, _suf)
        assert os.path.exists(p), "缺文件 %s" % p
        h.update(open(p, "rb").read())
print("产物齐全：problem1.in/.out … problem10.in/.out（.in 10 个、.out 10 个）")
print("数据 md5 汇总：%s" % h.hexdigest())
