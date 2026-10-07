#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 2043《【例5.11】杨辉三角形》分层测试数据生成器（cyaron，目标 ROJ 题号 5045）
# 用法：mkdir -p data && cd data && python3 ../data.py
#
# 题意：输入行数 n (2<=n<=20)，输出杨辉三角形前 n 行：第 i 行恰 i 个数，
#       每个数是上一行相邻两数之和（第 i 行第 j 列 = C(i-1, j-1)），
#       数与数之间用一个空格隔开。
#   题面范围：2 <= n <= 20（content.md【题目描述】「前 n(2≤n≤20) 行」；
#             官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=2043 本轮实抓核对一致）。
#   限制：time 1000 ms / memory 64 MB（config.json；官方页「1000 ms / 65536 KB」一致）。
#   单组输入：一个测试点就是一个整数 n，没有多组数据、没有 T。
#
# 【输入域与"分层/穷举"的处置】
#   本题输入域极小且离散：合法的 n 只有 19 个取值（2..20）。每个测试点只含一个
#   整数 n，10 个测试点最多放 10 个不同取值，无法把 19 个全放进来；而输出没有
#   任何随机成分（给定 n 答案唯一确定），因此不存在"随机小/中/大规模"的构造空间，
#   也不存在值域（本题无数组/权值输入）。
#   本包据此采用**确定性枚举 + 结构分层**：
#     * 低段连续：点 1/3/4/2（按 n 排序）取 n=2,3,4,5 —— 把范围下界起连续 4 个值
#       全部覆盖，杨辉三角所有实现类错误（末位 1 漏写、行数差一、0/1 下标混用、
#       行内个数错）在最小规模处就会暴露，连续段保证不依赖某单个值的巧合；
#     * 题面样例值：点 2 用 n=5（【输入样例】原样），与题面【输出样例】逐字节回归；
#     * 中上段稀疏：点 5-8 取 n=8/12/16/18；顶格：点 9/10 取 n=19/20；
#     * 嵌套完备性说明：杨辉三角前 n 行是前 n+1 行的前缀，故 n=20 一点的输出
#       包含任意 n<=20 的正确前 n 行内容；10 点合起来在"梯形内容"维度上全覆盖，
#       在"行数/循环边界"维度上有 2..5 连续段 + 16/18/19/20 上段值兜底。
#     * 未落盘的 9 个取值（6,7,9,10,11,13,14,15,17）由 work/stress.py 的 A 组
#       （19 个合法 n × 5 种输入字节形态 = 95 组）对拍兼顶，不留空白。
#
# 【分层设计（10 组，规模从下界铺到上限）】
#   点 1-2  边界层：n=2（范围下界，输出最少 2 行 3 个数）；n=5（题面【输入样例】
#          声明的特殊值，输出须逐字节等于【输出样例】）
#   点 3-4  小规模：n=3（最小奇数）、n=4（最小偶数段）—— 点 1-4 恰好覆盖 2..5
#          全部取值；输出最多 15 个数，可逐格手算核对
#   点 5-6  中等规模：n=8（范围中间偏低，首次成片出现非平凡中间值）；
#          n=12（范围中间偏高，输出 78 个数，最大数 C(11,5)=462）
#   点 7-8  大规模：n=16（范围上段，输出 136 个数）；n=18（逼近上限，输出 171 个数）
#   点 9-10 顶格层：n=19（题面上限-1 = 最大奇数）；n=20（题面上限 = 最大输出量，
#          20 行 210 个数，最大数 C(19,9)=92378）
#   注：合法 n 只有 19 个取值（2..20），10 个测试点放不下全部；未落盘取值(6,7,9..11,
#       13..15,17) 由 work/stress.py 的 A 组（19 个 n × 5 种输入形态）全覆盖对拍兼顶。
#   分层项适用性：本题输入是一个整数 n，“全最大值/答案为 0 或 1 的极端/有序逆序/
#   链/重复值/极端权值/卡常结构”等结构类分层项均不适用（无数组、无多组、n<=20 时
#   std 实测 0.002 s，不存在可卡常数）；等价覆盖见上方“确定性枚举 + 结构分层”。
#
# 【生成方式】IO(file_prefix="problem", data_id=i) + io.output_gen("../std")，
#   与 problems/1000/data.py、.ybt-import/staging/2041/data.py 等既有包一致。
#   数据完全确定性（无随机），逐字节可复现。
from cyaron import *  # 引入CYaRon的库

import os

NMIN, NMAX = 2, 20  # 题面明文范围 [2,20]

# 本包 10 个测试点：(data_id, n, 层次, 设计意图)
CASES = [
    (1, 2, "边界层", "范围下界 n=2：输出最少（2 行 3 个数），"
                    "压'行数循环边界 + 每行末位 1'的退化情形"),
    (2, 5, "边界层(题面特殊值)", "【输入样例】原样 n=5：输出须与题面【输出样例】逐字节一致"),
    (3, 3, "小规模", "n=3（最小奇数）：与 n=2 相邻，验证行数按 n 精确增长，可手算"),
    (4, 4, "小规模", "n=4（最小偶数段）：点 1-4 恰好覆盖 2..5 全部取值，可手算"),
    (5, 8, "中等规模", "n=8：范围中间偏低，输出 36 个数，最大数 C(7,3)=35"
                      "（首次成片出现非平凡中间值）"),
    (6, 12, "中等规模", "n=12：范围中间偏高，输出 78 个数，最大数 C(11,5)=462"),
    (7, 16, "大规模", "n=16：范围上段，输出 136 个数，最大数 C(15,7)=6435"),
    (8, 18, "大规模", "n=18：逼近上限，输出 171 个数，最大数 C(17,8)=24310"),
    (9, 19, "顶格层", "题面上限-1 = 最大奇数 n=19：输出 190 个数，最大数 C(18,9)=48620"),
    (10, 20, "顶格层", "题面上限 n=20 / 最大输出量：20 行 210 个数，"
                       "最大数 C(19,9)=C(19,10)=92378（验证数值正确）"),
]


def truth_rows(n):
    """Python 独立真值：按题面递推逐行构造杨辉三角（大整数，无溢出）。"""
    rows = []
    for i in range(n):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = rows[i - 1][j - 1] + rows[i - 1][j]
        rows.append(row)
    return rows


def expect_out(n):
    """期望输出文本：第 i 行 i 个数、数间恰一个空格、行末无多余空格、每行单个 '\\n'。"""
    return "\n".join(" ".join(map(str, row)) for row in truth_rows(n)) + "\n"


def gen_case(data_id, n, layer, note):
    assert NMIN <= n <= NMAX, "n=%d 超出题面范围 [%d,%d]" % (n, NMIN, NMAX)
    io = IO(file_prefix="problem", data_id=data_id)  # problem{data_id}.in / .out
    io.input_writeln(n)                              # "n\n"，与仓库较新包一致
    io.output_gen("../std")                          # .out 由 std 生成
    rows = truth_rows(n)
    print("problem%-2d: n=%-2d 层次=%-18s 行数=%-2d 共 %-3d 个数 最大数=%-6d -- %s"
          % (data_id, n, layer, n, n * (n + 1) // 2, max(rows[-1]), note))


def sample_expected():
    """题面【输出样例】的原样字节（content.md 中为 CRLF、末行无换行；这里规范化为
    仓库惯例的 LF + 单个末尾换行，用于点 2（n=5）的逐字节回归）。"""
    raw = "1\r\n1 1\r\n1 2 1\r\n1 3 3 1\r\n1 4 6 4 1"
    return raw.replace("\r\n", "\n") + "\n"


def self_check():
    """生成后立即审计：成对齐全、输入格式合规、输出与独立 Python 真值逐字节一致。"""
    bad = 0
    for data_id, n, _layer, _note in CASES:
        in_path, out_path = "problem%d.in" % data_id, "problem%d.out" % data_id
        try:
            raw_in = open(in_path, "rb").read()
            raw_out = open(out_path, "rb").read()
        except OSError as exc:
            print("MISSING pair for point %d: %s" % (data_id, exc))
            bad += 1
            continue
        # (1) 输入格式：恰为 "n\n"
        if raw_in != ("%d\n" % n).encode():
            print("BAD INPUT problem%d.in: %r (expect %r)" % (data_id, raw_in, "%d\n" % n))
            bad += 1
        # (2) 输出 == 独立 Python 真值（大整数递推），逐字节
        want = expect_out(n).encode()
        if raw_out != want:
            print("OUTPUT != TRUTH problem%d (n=%d): got %r..., want %r..."
                  % (data_id, n, raw_out[:60], want[:60]))
            bad += 1
        # (3) 输出结构：n 行、第 i 行 i 个数、数间恰一空格、行末无空格、单末尾换行
        text = raw_out.decode()
        lines = text.split("\n")
        if lines[-1] != "" or len(lines) != n + 1:
            print("BAD LINES problem%d: %d 行(含末尾空段), 期望 %d 行 + 末尾换行"
                  % (data_id, len(lines), n))
            bad += 1
        for i, line in enumerate(lines[:-1], start=1):
            parts = line.split(" ")
            if len(parts) != i or any(p == "" for p in parts):
                print("BAD ROW problem%d line %d: %r" % (data_id, i, line))
                bad += 1
                break
    # (4) 点 2 == 题面【输出样例】（规范化 CRLF 后逐字节）
    sample = sample_expected().encode()
    got2 = open("problem2.out", "rb").read()
    if got2 != sample:
        print("SAMPLE MISMATCH problem2.out: %r" % got2)
        bad += 1
    if bad:
        print("SELF-CHECK FAILED: %d issue(s)" % bad)
        raise SystemExit(1)
    print("SELF-CHECK OK: 10/10 成对，输入均为 'n\\n'，"
          "输出 == 独立 Python 大整数真值（逐字节），结构合规，点 2 == 题面【输出样例】")
    print("分层覆盖：边界 2 点(n=2,5) + 小规模 2 点(n=3,4) + 中等 2 点(n=8,12) "
          "+ 大规模 2 点(n=16,18) + 顶格 2 点(n=19,20)")


if __name__ == "__main__":
    assert os.path.exists("../std"), "../std 未编译，先执行 g++ -O2 -std=c++17 ../std.cpp -o ../std"
    for _data_id, _n, _layer, _note in CASES:
        gen_case(_data_id, _n, _layer, _note)
    self_check()
