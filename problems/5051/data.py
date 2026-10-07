#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
一本通 2049《【例5.19】字符串判等》（目标 ROJ 题号 5051）测试数据生成器。

题意：输入两行（每行只由大小写字母和空格组成）；把两行各自「删去所有空格 + 大写转小写」
      后比较，相同输出 YES，否则输出 NO。

数据范围与分层依据：
  - 题面（content.md / 官方 OJ 页）**未声明**每行长度上限；
  - 同题面在计蒜客 T1115 的版本给出「字符串长度不超过 100」（来源见 std.cpp 注释 [7]），
    且全部可得网络 AC 代码的字符数组都开 105 / 256 / 1000（[3][4][5][6]），
    本包据此取 **每行长度 <= 100**（MAXLEN），与教科书「第五章 数组 · 例 5.19」的教学规模一致。
  - 字符集严格限定为 [A-Za-z ] 三者，与题面「由大小写字母和空格组成」一致。

10 个测试点的分层（从最小铺到顶格，详见 gen-report.md 的分层表）：

  点  层              设计意图
  --  --------------  --------------------------------------------------------------
  1   边界层          最小规模：两行各 1 字符，`a` / `A` -> YES（单字符 + 大小写折叠）
  2   边界层          题面【输入样例】原样 -> YES（题面声明的特殊值，可手算）
  3   边界层          退化极端：一行全是空格（长度顶格 100）、另一行为空行
                      -> 两侧规范化后都是空串 -> YES（「空串」极端 + 全空格顶格）
  4   小规模随机      每行 4..10 字母，两行随机大小写 + 行首/行尾/内部空格，
                      且一侧规范串是另一侧的**真前缀**（尾部删 1..n-1 个字母）
                      -> NO（卡「只比到较短串结束就判 YES」的错解，可手算）
  5   小规模随机 Y    随机规范串（1..8 字母），两行用「不同大小写 + 不同空格位置」
                      表达同一规范串 -> YES
  6   中等规模随机    每行 20..40 字符，随机大小写 + 约 15% 空格，两侧独立随机
                      （真值由内容决定，生成器用独立参考实现复算）
  7   大规模随机      字母多重集合相同、排列不同（anagram）的 60..80 字母 +
                      随机空格 -> NO：专门卡「字母 ASCII 求和 / 26 桶计数 / 哈希代替逐位比较」的错解
  8   大规模随机      每行 80..100 字符（接近上限，空格占比高），两侧独立随机
  9   顶格层          两行各恰 100 字符；规范化后前 98 个字符相同、最后 1 个不同
                      -> NO：最坏比较深度，必须比到最后一个字符
  10  顶格层          两行各恰 100 字符；一行全大写 + 前后各 11 个空格、
                      一行全小写 + 中间 22 个空格，规范化后均为 a-z 重复三轮
                      -> YES：大小写与空格位置完全错开，强制正确折叠/丢空格

分层清单对照：点 1、2 为**题面声明的特殊值 / 最小规模**（边界层）；点 3 为该题特有的
**退化极端**（全空格 vs 空行，双方规范化后均为空串）；点 4、5 小规模随机（可手算）；
点 6 中等；点 7、8 大规模（含 anagram 定向结构）；点 9、10 顶格。
四个边界/极端项（最小规模、题面样例、空串退化、顶格长度）超出「点 1-2」两个名额，
故边界层占点 1-3、小规模随机占点 4-5，保证「从最小铺到顶格」不断层。

生成方式：cyaron 的 IO(file_prefix="problem", data_id=i) + io.output_gen("../std")，
每个点用独立随机种子 random.seed(2049 + 点号)，可精确复现。
生成后内置自检：用与 std.cpp 无关的纯 Python 参考实现复算期望输出，与 std 产出的 .out
逐字节比对，并断言每个点的结构性特征（字符集、行长上限、分层特征）。
"""

import os
import random
import string as pystring   # 注意：cyaron 也导出名为 string 的子模块，故这里改名导入
import sys

from cyaron import *  # 引入CYaRon的库

# --------------------------------------------------------------------------
# 全局设定
# --------------------------------------------------------------------------
MAXLEN = 100                          # 每行长度上限（题面上限口径，见文件头说明）
ALPHA_L = pystring.ascii_lowercase    # 'a'..'z'
ALPHA_U = pystring.ascii_uppercase    # 'A'..'Z'
SAMPLE_L1 = "a A bb BB ccc CCC"   # 题面【输入样例】第一行
SAMPLE_L2 = "Aa BBbb CCCccc"      # 题面【输入样例】第二行


def ref_normalize(s):
    """独立参考实现（纯 Python，与 std.cpp 的 C 代码路径完全不同）：

    删去所有空格，再把大写字母折叠成小写。返回规范化后的串。
    """
    return "".join(ch for ch in s if ch != " ").lower()


def random_letters(n, letters=ALPHA_L):
    """随机取 n 个字母。"""
    return "".join(random.choice(letters) for _ in range(n))


def random_case(s, lower_rate=0.5):
    """把 s 中每个字母以 lower_rate 的概率变小写，否则变大写。"""
    return "".join(
        ch.lower() if random.random() < lower_rate else ch.upper() for ch in s
    )


def inject_spaces(s, space_rate, case_rate=0.5):
    """在 s 的每个字符前以 space_rate 的概率插入空格，字符本身随机大小写；
    末尾也以 space_rate 的概率补一个空格（覆盖行尾空格）。"""
    out = []
    for ch in s:
        if random.random() < space_rate:
            out.append(" ")
        out.append(ch.lower() if random.random() < case_rate else ch.upper())
    if random.random() < space_rate:
        out.append(" ")
    return "".join(out)


# --------------------------------------------------------------------------
# 10 个测试点的构造函数：返回 (line1, line2, 设计说明)
# --------------------------------------------------------------------------

def build_point(i):
    random.seed(2049 + i)  # 每个点独立种子，保证可复现

    # ---------------- 点 1：边界层 · 最小规模 ----------------
    if i == 1:
        return ("a", "A", "边界层：最小规模（两行各 1 字符），a vs A -> YES（大小写折叠）")

    # ---------------- 点 2：边界层 · 题面样例原样 ----------------
    if i == 2:
        return (SAMPLE_L1, SAMPLE_L2, "边界层：题面【输入样例】原样 -> YES（题面特殊值）")

    # ---------------- 点 3：边界层 · 退化极端（双方规范化后均为空串） ----------------
    if i == 3:
        l1 = " " * MAXLEN          # 长度顶格且全为空格
        l2 = ""                    # 空行（最短）
        return (l1, l2, "边界层：退化极端——全空格行（长 100）vs 空行 -> 双方规范化后均为空串 -> YES")

    # ---------------- 点 4：小规模随机 · 真值 NO（且为「真前缀」结构） ----------------
    if i == 4:
        n = random.randint(4, 10)
        core = random_letters(n)
        # 第 2 行的规范串 = core 删去末尾 k 个字母（1 <= k <= n-1）：
        # 即一侧规范化后是另一侧的**真前缀**，用来卡「只比到较短串结束就判 YES」的错解。
        k = random.randint(1, n - 1)
        core2 = core[:n - k]
        l1 = inject_spaces(core, space_rate=0.25)
        l2 = inject_spaces(core2, space_rate=0.25)
        l1 = " " + l1                      # 行首空格（必现）
        l2 = l2 + " "                      # 行尾空格（必现）
        return (l1, l2, "小规模随机：一行规范化后是另一行的真前缀（尾部删 k 个字母）-> NO（卡「只比到较短串结束」的错解）")

    # ---------------- 点 5：小规模随机 · 真值 YES（大小写/空格全错位） ----------------
    if i == 5:
        n = random.randint(1, 8)
        core = random_letters(n)
        # 两行表达同一个规范串，但大小写概率与空格位置都不同
        l1 = inject_spaces(core, space_rate=0.5, case_rate=0.0)    # 全大写 + 随机空格
        l2 = inject_spaces(core, space_rate=0.3, case_rate=1.0)    # 全小写 + 另一套空格
        return (l1, l2, "小规模随机：同一规范串（1..8 字母），两行大小写与空格位置全错开 -> YES")

    # ---------------- 点 6：中等规模随机 ----------------
    if i == 6:
        core1 = random_letters(random.randint(20, 40))
        core2 = random_letters(random.randint(20, 40))
        l1 = inject_spaces(core1, space_rate=0.15)
        l2 = inject_spaces(core2, space_rate=0.15)
        return (l1, l2, "中等规模随机：每行 20..40 字符、约 15% 空格，两侧独立随机（真值由自检复算）")

    # ---------------- 点 7：大规模随机 · anagram（卡求和/哈希错解） ----------------
    if i == 7:
        n = random.randint(60, 80)
        small_alpha = ALPHA_L[:8]                      # 只用 8 种字母，便于构造同多重集合的排列
        core1 = "".join(random.choice(small_alpha) for _ in range(n))
        core2 = core1
        while core2 == core1:                          # 重排到与 core1 不同为止
            core2 = "".join(random.sample(core1, len(core1)))
        l1 = inject_spaces(core1, space_rate=0.12)
        l2 = inject_spaces(core2, space_rate=0.12)
        assert len(l1) <= MAXLEN and len(l2) <= MAXLEN, "点 7 行长超上限"
        return (l1, l2, "大规模随机：字母多重集合相同、排列不同（anagram，60..80 字母）-> NO（卡求和/哈希错解）")

    # ---------------- 点 8：大规模随机（接近上限） ----------------
    if i == 8:
        n1 = random.randint(60, 80)
        n2 = random.randint(60, 80)
        core1 = random_letters(n1)
        core2 = random_letters(n2)
        l1 = inject_spaces(core1, space_rate=0.2)
        l2 = inject_spaces(core2, space_rate=0.2)
        assert len(l1) <= MAXLEN and len(l2) <= MAXLEN, "点 8 行长超上限，请调小 n1/n2"
        return (l1, l2, "大规模随机：每行 80..100 字符（接近上限、空格占比约 20%），两侧独立随机")

    # ---------------- 点 9：顶格层 · 最坏比较深度 ----------------
    if i == 9:
        # 两行都恰 100 字符；规范化后长度同为 99，前 98 个字符相同，仅最后 1 个字符不同 -> NO。
        # 比较器必须一路比到最后一位才能发现差异（最坏比较深度）。
        prefix = random_letters(98)
        c1 = random.choice(ALPHA_L)
        c2 = random.choice([c for c in ALPHA_L if c != c1])
        l1 = " " + prefix + c1          # 行首空格 + 98 字母 + 字母1 = 100 字符，规范串 = prefix+c1
        l2 = prefix + " " + c2           # 98 字母 + 中间空格 + 字母2 = 100 字符，规范串 = prefix+c2
        assert len(l1) == MAXLEN and len(l2) == MAXLEN
        return (l1, l2, "顶格层：两行各 100 字符，规范化后前 98 字符相同、仅最后 1 字符不同 -> NO（最坏比较深度）")

    # ---------------- 点 10：顶格层 · 大小写/空格全错位 YES ----------------
    if i == 10:
        core = ALPHA_L * 3                       # 78 个字母，覆盖 a-z 三轮
        # 第 1 行：全大写，前面 11 个空格 + 后面 11 个空格 = 100 字符
        l1 = " " * 11 + core.upper() + " " * 11
        # 第 2 行：全小写，中间 22 个空格 = 100 字符（空格位置与第 1 行完全错开）
        l2 = core[:39] + " " * 22 + core[39:]
        assert len(l1) == MAXLEN and len(l2) == MAXLEN
        assert ref_normalize(l1) == ref_normalize(l2) == core
        return (l1, l2, "顶格层：两行各 100 字符，一行全大写（前后空格）、一行全小写（中间空格）-> YES")

    raise ValueError("未知测试点编号：%d" % i)


# --------------------------------------------------------------------------
# 生成 + 生成后自检
# --------------------------------------------------------------------------

def main():
    expected_info = {}
    for i in range(1, 11):
        l1, l2, note = build_point(i)
        io = IO(file_prefix="problem", data_id=i)  # problemI.in / problemI.out
        io.input_write(l1, "\n", l2, "\n")
        io.output_gen("../std")
        io.close()   # 显式关闭，确保 .in/.out 的缓冲落盘后下方自检才能读到完整内容
        expected_info[i] = (l1, l2, note)

    # ---- 生成后自检：读回 .in/.out，用独立参考实现复算并逐字节比对 ----
    here = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(here, "data")
    problems = []

    def check(cond, msg):
        if not cond:
            problems.append(msg)

    for i in range(1, 11):
        l1, l2, note = expected_info[i]
        in_path = os.path.join(data_dir, "problem%d.in" % i)
        out_path = os.path.join(data_dir, "problem%d.out" % i)
        raw_in = open(in_path, "r", encoding="utf-8", newline="").read()
        raw_out = open(out_path, "r", encoding="utf-8", newline="").read()

        parts = raw_in.split("\n")
        check(len(parts) == 3 and parts[2] == "",
              "点 %d：.in 应为「两行 + 结尾换行」（实际切得 %d 段）" % (i, len(parts)))
        r1, r2 = parts[0], parts[1]

        # (1) 输入与生成器构造一致（含行尾空格，逐字符相等）
        check(r1 == l1 and r2 == l2, "点 %d：读回的输入与构造不一致" % i)
        # (2) 字符集严格为 [A-Za-z ]
        for ln, name in ((r1, "第1行"), (r2, "第2行")):
            bad = set(ch for ch in ln if ch not in ALPHA_L and ch not in ALPHA_U and ch != " ")
            check(not bad, "点 %d：%s 出现非法字符 %r" % (i, name, sorted(bad)))
            check(len(ln) <= MAXLEN, "点 %d：%s 长度 %d 超过上限 %d" % (i, name, len(ln), MAXLEN))
        # (3) 独立参考实现复算期望输出，与 std 产出的 .out 逐字节比对
        want = "YES\n" if ref_normalize(r1) == ref_normalize(r2) else "NO\n"
        check(raw_out == want,
              "点 %d：std 输出 %r != 参考实现 %r" % (i, raw_out, want))

        ans = raw_out.strip()
        print("点 %2d | 行1 长 %3d 规范 %3d | 行2 长 %3d 规范 %3d | %s | %s"
              % (i, len(r1), len(ref_normalize(r1)), len(r2), len(ref_normalize(r2)), ans, note))

    # ---- 分层结构性断言 ----
    r1, r2 = expected_info[1][0], expected_info[1][1]
    check(len(r1) == 1 and len(r2) == 1 and r1.lower() == r2.lower(), "点 1 不是最小规模 YES")
    check(expected_info[2][0] == SAMPLE_L1 and expected_info[2][1] == SAMPLE_L2, "点 2 不是题面样例原样")
    check(expected_info[3][0] == " " * MAXLEN and expected_info[3][1] == "", "点 3 不是退化极端")
    check(ref_normalize(expected_info[3][0]) == "" and ref_normalize(expected_info[3][1]) == "",
          "点 3 双方规范化后应为空串")
    check(len(expected_info[4][0]) <= 16 and len(expected_info[4][1]) <= 16, "点 4 不是小规模")
    check(ref_normalize(expected_info[4][0]) != ref_normalize(expected_info[4][1]), "点 4 应为 NO")
    n4a, n4b = ref_normalize(expected_info[4][0]), ref_normalize(expected_info[4][1])
    check(len(n4a) > len(n4b) and n4a.startswith(n4b),
          "点 4 应满足：较短行为较长行的真前缀")
    check(ref_normalize(expected_info[5][0]) == ref_normalize(expected_info[5][1]), "点 5 应为 YES")
    check(ref_normalize(expected_info[7][0]) != ref_normalize(expected_info[7][1]), "点 7 应为 NO")
    check(sorted(ref_normalize(expected_info[7][0])) == sorted(ref_normalize(expected_info[7][1])),
          "点 7 两行规范化后应为同一字母多重集合（anagram）")
    check(len(expected_info[9][0]) == MAXLEN and len(expected_info[9][1]) == MAXLEN, "点 9 应两行均顶格 100")
    n9a, n9b = ref_normalize(expected_info[9][0]), ref_normalize(expected_info[9][1])
    check(len(n9a) == len(n9b) == 99, "点 9 规范化后长度应为 99")
    check(n9a[:-1] == n9b[:-1], "点 9 规范化后前 98 字符应完全相同")
    check(n9a[-1] != n9b[-1], "点 9 规范化后最后 1 个字符应不同")
    check(ref_normalize(expected_info[10][0]) == ref_normalize(expected_info[10][1]) == ALPHA_L * 3,
          "点 10 规范化后应为 a-z 三轮")
    check(len(expected_info[10][0]) == MAXLEN and len(expected_info[10][1]) == MAXLEN, "点 10 应两行均顶格 100")

    if problems:
        print("\n自检失败：", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        raise SystemExit(1)
    print("\n自检全部通过：10/10 组 .in/.out 成对，字符集/长度/分层特征/参考实现复算均一致。")


if __name__ == "__main__":
    main()
