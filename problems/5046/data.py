#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 一本通 2044《【例5.12】回文字串》分层测试数据生成器（cyaron）
# 用法（在本目录下）：
#     g++ -O2 -std=c++17 std.cpp -o std
#     mkdir -p data && cd data && python3 ../data.py
# 参考仓库惯例：problems/1000/data.py（IO(file_prefix="problem", data_id=i) + output_gen("../std")）、
#               problems/5006/data.py（无输入题只生成 1 组）、
#               .ybt-import/staging/2036/data.py、staging/2034/data.py（分层 + 生成期自检）。
#
# ---------------------------------------------------------------------------
# 题意（content.md；官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=2044
#       本轮实抓核对，题面五节与 content.md 逐字一致）：
#   【题目描述】输入一串字符,字符个数不超过 100,且以"."结束。 判断它们是否构成回文。
#   【输入】一行字符串。
#   【输出】是否为回文串。是输出"Yes"，否输出"No"。
#   【输入样例】abccb        【输出样例】No
#   config.json：time 1000 ms / memory 64 MB（官方页「时间限制 1000 ms
#               内存限制 65536 KB」，一致；官方页提交数 67960 / 通过数 29255）。
#
# ---------------------------------------------------------------------------
# 数据范围与判读（与 std.cpp 头部注释一致，逐条给依据）：
#   * 规模：**整行（含终止符 '.'）字符个数不超过 100**，本包取这一最严格读法
#     ⇒ 回文主体长度 ≤ 99。这是题面唯一给出的定量约束；10 个点全部满足
#     （顶格测试点整行恰 100 字符：99 个主体字符 + 1 个 '.'）。
#   * 终止符：'.' 只作为**行尾终止符**出现、不参与回文判断；本包数据保证
#     主体内**不含内嵌 '.'**（否则与主流实现的读取路线冲突，见 gen-report.md 风险点）。
#   * 字符集：题面只写「一串字符」。全部 7 个网络来源的 AC 代码都用
#     `cin >> s` / `scanf("%s")` 读入，⇒ 官方数据不含空白符（否则它们不可能通过）。
#     本包因此只用**可打印非空白 ASCII**：小写 / 大写 / 数字 / 符号（不含 '.'），
#     且不含空格、制表符。这样标准实现（`cin >> s` 与按行读两种路线）都能正确读入。
#   * 空主体：输入恰为 "."（去掉终止符后为空串）时判 Yes（空串按回文处理）。
#     依据：主流实现去掉 '.' 后长度为 0、比较循环 0 次，必然落入 Yes 分支
#     （如来源 [2] 的双指针版对 "." 也输出 Yes）。
#   * 单组输入：每组数据只有一行，不存在「组数 T / 多组数据」维度。
#
# ---------------------------------------------------------------------------
# 分层设计（10 个测试点；每点的规模与设计意图见下面 CASES 注释）：
#   点 1  ｜边界层｜最小规模：行="."（回文主体为空串），答案 Yes —— 全题理论最小输入
#   点 2  ｜边界层｜回文主体长度 1："a."，退化回文，答案 Yes —— 最短非空主体
#   点 3  ｜边界层（题面声明的特殊值）｜【输入样例】原样 `abccb`（题面逐字，未带 '.'）
#          ，期望输出 = 【输出样例】"No"（样例回归，逐字节断言）
#   点 4  ｜小规模随机｜主体长度 3，小写随机（可手算核对，答案 No）
#   点 5  ｜中等规模随机｜主体长度 40，混合字符集随（大小写+数字+符号）
#   点 6  ｜中等规模定向·多重陷阱｜主体长度 40，除最内一对 (19,20) 仅大小写不同
#          （'a'/'A'）外其余 19 对全等 ⇒ 答案 No；定向杀 IGNORE_CASE / SKIP_INNER /
#          FIRST_PAIR / EVEN_ONLY 四类错解
#   点 7  ｜大规模随机｜主体长度 88，混合字符集随机（近上限随机，答案 No）
#   点 8  ｜大规模定向（最坏比较次数）｜主体长度 99，仅第 (47,51) 一对仅大小写不同、
#          其余 48 对全对称 ⇒ 答案 No，须比完 48/49 对才判出；同时杀 IGNORE_CASE /
#          EVEN_ONLY / FIRST_PAIR
#   点 9  ｜顶格层｜主体长度 99 全 'z'（整行 100 字符，题面上限）—— 全相等/重复值顶格
#   点 10 ｜顶格层｜主体长度 99，**混合字符集（大小写+数字+符号，不含 '.'）镜像回文**
#          （整行 100 字符）—— 顶格 Yes（49 对全部相等） + 字符集覆盖最广
#
#   分层项适用性（题面性质决定，详见 gen-report.md「分层对照」）：
#     * 「答案为 0 或 1 的极端」不适用 —— 本题输出是 Yes/No 二值；Yes 由点 1/2/9/10
#       覆盖、No 由点 3/4/5/6/7/8 覆盖（两条分支都有顶格与边界载体）。
#     * 「有序/逆序、链」不适用（输入是一行字符，无序列结构），等价物是
#       **重复值（点 9 全 'z'）与对称结构（点 6/8/10）**，均已覆盖。
#     * 「卡常结构」不适用 —— 判定是 O(n)、n ≤ 100，实测 std 顶格点 < 2 ms（限 1000 ms），
#       不存在可卡的常数/结构；顶格层因此按「最大输入规模 + 最坏比较次数」设计。
#     * 「多组数据按组数分层」不适用 —— 单组输入，无组数维度。
#
#   随机性：全部随机点用固定种子（2044 + 点号），逐字节可复现。
#   自检（本文件末尾执行）：
#     1) Python 独立直译题面（第三条路线，与 std 的双指针、brute 的逆序串都无关）
#        预测每组期望输出，与 problemN.out **逐字节**比对；
#     2) 断言每组 .in 为**单行**、行末恰一个 '\n'、无行首/行末空格、无连续空格；
#     3) 断言每行长度 ≤ 100（题面上限）、除样例点外均以 '.' 结束、主体内无 '.'；
#     4) 断言 10 组 .in/.out 成对齐全、点 3 与题面样例逐字节一致。

from cyaron import *  # 引入CYaRon的库

import os
import random
import string

# ---------------------------------------------------------------------------
# 字符串常量
# ---------------------------------------------------------------------------
LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGITS = string.digits
# 符号集：string.punctuation 去掉 '.'（'.' 是终止符，主体内不得出现）
PUNCT_NO_DOT = string.punctuation.replace(".", "")
MIXED = LOWER + UPPER + DIGITS + PUNCT_NO_DOT

MAX_LINE = 100  # 题面：「字符个数不超过 100」= 整行（含终止符）上限，本包取最严格读法

SAMPLE_IN = "abccb"       # 题面【输入样例】原样（逐字，未带 '.'）
SAMPLE_OUT = "No\n"       # 题面【输出样例】


# ---------------------------------------------------------------------------
# Python 独立真值：按题面直译
#   行 → 去掉行尾终止符 '.' → 双指针判回文
# 这是与 std.cpp（C++ 双指针）、work/brute.cpp（逆序串）都不同的第三条路线。
# ---------------------------------------------------------------------------
def is_palindrome_body(body):
    return body == body[::-1]


def truth(stdin_text):
    line = stdin_text.rstrip("\r\n")
    if line.endswith("."):
        line = line[:-1]
    return "Yes\n" if is_palindrome_body(line) else "No\n"


# ---------------------------------------------------------------------------
# 构造 10 组：(data_id, line, note)
#   line = 写入 .in 的整行内容（不含行末 '\n'，由 io.input_writeln 补）
# ---------------------------------------------------------------------------
CASES = []


def add(data_id, line, note):
    assert data_id == len(CASES) + 1, "data_id 必须连续递增"
    assert len(line) <= MAX_LINE, "点 %d：行长度 %d 超出题面上限 %d" % (data_id, len(line), MAX_LINE)
    assert line == line.strip(), "点 %d：行首/行末不允许有空白" % data_id
    if data_id != 3:  # 点 3 是题面样例原样（不带 '.'），见 std.cpp 判读
        assert line.endswith("."), "点 %d：除样例点外每行必须以 '.' 结束" % data_id
        assert "." not in line[:-1], "点 %d：主体内不得含内嵌 '.'" % data_id
    assert not any(ch.isspace() for ch in line), "点 %d：不得含空白字符" % data_id
    CASES.append((data_id, line, note))


# ---- 点 1-2：边界层 ----
add(1, ".",
    "边界层｜最小规模：整行仅终止符 '.'（回文主体为空串），答案 Yes —— 全题理论最小输入")

add(2, "a.",
    "边界层｜回文主体长度 1（最短非空主体）：'a' 退化为回文，答案 Yes")

# ---- 点 3：题面声明的特殊值（官方样例原样）----
add(3, SAMPLE_IN,
    "边界层(题面特殊值)｜【输入样例】原样 'abccb'（题面逐字、未带 '.'）："
    "期望输出须逐字节等于【输出样例】'No\\n'，做样例回归")

# ---- 点 4：小规模随机（可手算）----
random.seed(2044 + 4)
L4 = 3  # 固定为最小可手算的非平凡长度（比 2 多一对判断）
body4 = "".join(random.choice(LOWER) for _ in range(L4))
assert not is_palindrome_body(body4), "点 4 期望为 No（可手算核对，断言固化）"
add(4, body4 + ".",
    "小规模随机｜主体长度 3、小写随机（种子 2044+4 复现）：可手算逐对核对（答案 No）")

# ---- 点 5-6：中等规模 ----
random.seed(2044 + 5)
L5 = 40
body5 = "".join(random.choice(MIXED) for _ in range(L5))
assert not is_palindrome_body(body5), "点 5 期望为 No（随机长串几乎必然非回文，断言固化）"
add(5, body5 + ".",
    "中等规模随机｜主体长度 40、混合字符集（大小写+数字+符号，不含 '.'）随机"
    "（种子 2044+5 复现）：范围中间档，字符集覆盖宽")

# 点 6：中等规模**定向多重陷阱**——除最内一对外全对称，且最内一对仅大小写不同
L6 = 40
random.seed(2044 + 6)
half6 = "".join(random.choice(LOWER) for _ in range(L6 // 2))
body6 = half6[:L6 // 2 - 1] + "a" + "A" + half6[:L6 // 2 - 1][::-1]
assert len(body6) == L6
# 最内对 (19,20) = 'a'/'A'，其余 19 对逐字节相等
assert all(body6[i] == body6[L6 - 1 - i] for i in range(L6 // 2 - 1)), "点 6 结构不符"
assert body6[L6 // 2 - 1] == "a" and body6[L6 // 2] == "A"
assert not is_palindrome_body(body6)                      # 正确答案 No（大小写敏感）
assert body6.lower() == body6.lower()[::-1]               # 忽略大小写后是回文 ⇒ 杀 IGNORE_CASE
# 逐条断言四类错解的模拟行为（保证数据确实能杀它们）：
#   · 只比首对（FIRST_PAIR）→ (0,39) 相等 ⇒ 误判 Yes
#   · 漏最内一对（SKIP_INNER，半长 20 ⇒ 只跑 i<19）⇒ 误判 Yes
#   · 只比偶数下标对（EVEN_ONLY，i=0,2,...,18 后 i=20>j=19 停）⇒ 误判 Yes
assert body6[0] == body6[L6 - 1]                                  # 杀 FIRST_PAIR
assert all(body6[i] == body6[L6 - 1 - i] for i in range(L6 // 2 - 1))  # 杀 SKIP_INNER
assert all(body6[i] == body6[L6 - 1 - i] for i in range(0, L6 // 2, 2))  # 杀 EVEN_ONLY
add(6, body6 + ".",
    "中等规模定向·多重陷阱｜主体长度 40：除**最内一对 (19,20) 仅大小写不同**（'a'/'A'）外"
    "其余 19 对逐字节相等 ⇒ 正确答案 No；同时定向杀四类错解：逐字节大小写敏感"
    "（IGNORE_CASE 会输出 Yes）、内对漏判（SKIP_INNER 误判 Yes）、"
    "只比首对（FIRST_PAIR 误判 Yes）、只比偶数下标对（EVEN_ONLY 跳过 i=19 误判 Yes）")

# ---- 点 7-8：大规模 ----
random.seed(2044 + 7)
L7 = 88
body7 = "".join(random.choice(MIXED) for _ in range(L7))
assert not is_palindrome_body(body7), "点 7 期望为 No（随机长串几乎必然非回文，断言固化）"
add(7, body7 + ".",
    "大规模随机｜主体长度 88（接近上限）、混合字符集随机（种子 2044+7 复现）："
    "答案 No（首对即不同，提前退出）")

# 点 8：大规模**定向最坏比较次数**——只有一对（奇数下标对）不同且仅大小写不同
L8 = 99                                   # 99 为奇数：配对下标 i = 0..48
random.seed(2044 + 8)
half8 = "".join(random.choice(UPPER + DIGITS) for _ in range(L8 // 2))
body8 = half8 + "z" + half8[::-1]         # 先构造 99 长回文
body8 = body8[:47] + "a" + body8[48:51] + "A" + body8[52:]   # 破坏对 (47,51)，且仅大小写不同
assert len(body8) == L8 and not is_palindrome_body(body8)
assert body8.lower() == body8.lower()[::-1]                  # 忽略大小写后是回文 ⇒ 杀 IGNORE_CASE
assert all(body8[i] == body8[L8 - 1 - i] for i in range(47)), "点 8 结构不符（须仅一对不同）"
# EVEN_ONLY 访问的偶数下标对 (0,98),(2,96),...,(48,50) 全相等 ⇒ 它误判 Yes（正确为 No）
assert all(body8[i] == body8[L8 - 1 - i] for i in range(0, 50, 2)), "杀 EVEN_ONLY 的前提不符"
assert body8[0] == body8[L8 - 1]                              # 杀 FIRST_PAIR（首对相等）
assert body8[47] != body8[51] and body8[47].lower() == body8[51].lower()
add(8, body8 + ".",
    "大规模定向·最坏比较次数｜主体长度 99：仅第 (47,51) 一对**仅大小写不同**（'a'/'A'）、"
    "其余 48 对逐字节相等 ⇒ 正确答案 No，且必须比完 48/49 对才判出；"
    "同时杀 IGNORE_CASE / EVEN_ONLY / FIRST_PAIR")

# ---- 点 9-10：顶格层 ----
add(9, "z" * 99 + ".",
    "顶格层｜主体长度 99 全为同一字符（重复值顶格），整行 100 字符 = 题面上限："
    "答案 Yes，且 49 对全部需要比较")

random.seed(2044 + 10)
half10 = "".join(random.choice(MIXED) for _ in range(99 // 2))
body10 = half10 + "Q" + half10[::-1]
assert len(body10) == 99 and is_palindrome_body(body10)
add(10, body10 + ".",
    "顶格层｜主体长度 99 的**混合字符集镜像回文**（大小写+数字+符号，不含 '.'），"
    "整行 100 字符 = 题面上限：答案 Yes，字符集覆盖最广（49 对全等）")

assert len(CASES) == 10, "必须恰好 10 个测试点"
assert len({line for _, line, _ in CASES}) == 10, "10 个测试点的输入必须互不相同"


# ---------------------------------------------------------------------------
# 生成与自检
# ---------------------------------------------------------------------------
def main():
    assert os.path.exists("../std"), "请先编译 std：g++ -O2 -std=c++17 std.cpp -o std"
    print("== 生成 %d 组数据 ==" % len(CASES))

    for data_id, line, note in CASES:
        io = IO(file_prefix="problem", data_id=data_id)  # problem{i}.in / problem{i}.out
        io.input_writeln(line)                           # 单行 + 行末恰一个 '\n'
        io.output_gen("../std")
        io.close()
        print("problem%-2d: 行长度=%-3d 主体长度=%-3d 期望=%-4s -- %s"
              % (data_id, len(line), len(line.rstrip(".")), truth(line + "\n").strip(), note))

    # ---- 自检 1-4 ----
    bad = 0
    for data_id, line, _note in CASES:
        in_path, out_path = "problem%d.in" % data_id, "problem%d.out" % data_id
        raw_in = open(in_path, "rb").read()
        raw_out = open(out_path, "rb").read()

        # 单行、行末恰一个 '\n'、无多余空白
        if not raw_in.endswith(b"\n") or raw_in.count(b"\n") != 1:
            print("BAD FORMAT problem%d.in: %r" % (data_id, raw_in)); bad += 1
        text = raw_in.decode()
        body_line = text[:-1]
        if body_line != body_line.strip() or "  " in body_line:
            print("BAD SPACE problem%d.in: %r" % (data_id, raw_in)); bad += 1
        if body_line != line:
            print("MISMATCH problem%d.in: %r (expect %r)" % (data_id, body_line, line)); bad += 1
        if len(body_line) > MAX_LINE:
            print("TOO LONG problem%d.in: %d > %d" % (data_id, len(body_line), MAX_LINE)); bad += 1

        # Python 独立真值 vs std 输出（逐字节）
        want = truth(text).encode()
        if raw_out != want:
            print("OUTPUT != TRUTH problem%d: %r (expect %r)" % (data_id, raw_out, want)); bad += 1

    # 点 3 与题面样例逐字节一致
    if open("problem3.in", "rb").read().decode() != SAMPLE_IN + "\n":
        print("SAMPLE INPUT MISMATCH"); bad += 1
    if open("problem3.out", "rb").read().decode() != SAMPLE_OUT:
        print("SAMPLE OUTPUT MISMATCH"); bad += 1

    # 抽查 2 组人工可核对的小数据
    for probe_id, want_out in ((1, "Yes\n"), (2, "Yes\n")):
        got = open("problem%d.out" % probe_id, "rb").read().decode()
        if got != want_out:
            print("PROBE FAIL problem%d: %r != %r" % (probe_id, got, want_out)); bad += 1

    if bad:
        print("SELF-CHECK FAILED: %d issue(s)" % bad)
        raise SystemExit(1)

    print()
    print("SELF-CHECK OK: 10/10 .in/.out 成对齐全；每组 .in 均为单行（行末恰一个 '\\n'、"
          "无行首行末空格、无连续空格）；每行长度 <= %d；" % MAX_LINE)
    print("              每组 .out == Python 独立直译真值（第三条路线）；"
          "点 3 与题面样例逐字节一致。")
    print("分层覆盖：边界 3 点（./a./样例）+ 小规模 1 点 + 中等 2 点 + 大规模 2 点 + 顶格 2 点；"
          "答案 Yes 4 点 / No 6 点。")


if __name__ == "__main__":
    main()
