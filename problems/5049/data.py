#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 一本通 2047《【例5.16】过滤空格》分层测试数据生成器（cyaron）
# 用法（在本目录下）：
#     g++ -O2 -std=c++17 std.cpp -o std
#     mkdir -p data && cd data && python3 ../data.py
# 参考仓库惯例：problems/1000/data.py（IO(file_prefix="problem", data_id=i) + output_gen("../std")）、
#               problems/5006/data.py（无输入题只生成 1 组）、
#               .ybt-import/staging/2044/data.py（分层 + 生成期自检）。
#
# ---------------------------------------------------------------------------
# 题意（content.md，逐字核对；官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=2047
#       本轮实抓，正文各节被站点清空、仅余标题/限制/样例，样例与 content.md 逐字节一致；
#       OpenJudge NOI 1.7 第 23 题 http://noi.openjudge.cn/ch0107/23/ 同题，描述逐字一致）：
#   【题目描述】过滤多余的空格。一个句子中也许有多个连续空格，过滤掉多余的空格，
#              只留下一个空格。
#   【输入】一行，一个字符串（长度不超过 200），句子的头和尾都没有空格。
#   【输出】过滤之后的句子。
#   【输入样例】Hello      world.This is    c language.
#   【输出样例】Hello world.This is c language.
#   config.json：time 1000 ms / memory 64 MB（官方页「时间限制 1000 ms 内存限制 65536 KB」，
#   一致；官方页提交数 76430 / 通过数 51003）。
#
# ---------------------------------------------------------------------------
# 数据范围与口径（与 std.cpp 头部注释一致）：
#   * 规模：**单行字符串，长度（字符数）不超过 200**，本包按上限 200 顶格铺满
#     （点 9/10 恰为 200 字符），其余点从 1 逐级铺到近上限。
#   * 结构：**句子的头和尾都没有空格**（题面明文）⇒ 本包所有输入满足
#     `line == line.strip(" ")`、`" " not in (line[0], line[-1])`。
#   * 字符集：题面「一个句子」——本包只用**可打印非空白 ASCII**：
#     字母（大小写）+ 数字 + 标点（含 '.'、','、'!' 等），分隔符只用**普通空格 ' '**
#     （不生成制表符/其它空白，题面只提「空格」；这也让 `cin>>s`/`scanf("%s")`
#     与 `getline` 两类主流读入路线在数据上等价）。
#   * 输出：把每个连续空格段压缩为恰一个空格后的句子；**长度不固定**（如点 10 从 200
#     压到 3），故无「固定输出长度」假设。
#   * 单组输入：每组数据只有一行，不存在「组数 T / 多组数据」维度。
#
# ---------------------------------------------------------------------------
# 分层设计（10 个测试点；每点的规模与设计意图见下面 CASES 注释）：
#   点 1  ｜边界层｜**理论最小规模**：长度 1、无空格（"A"）——输出 = 输入
#   点 2  ｜边界层｜**最小非平凡**：长度 3、恰 1 段 1 个空格（"a b"）——过滤后原样，
#          覆盖「唯一空格段不压缩」；与点 1 一起钉住「输出=输入」两条最小形态
#   点 3  ｜边界层（题面声明的特殊值）｜**【输入样例】原样**（39 字符）：
#          期望输出须逐字节等于【输出样例】（31 字符），做样例回归
#   点 4  ｜小规模随机｜长度 ≤ 12，小写词 + 1..3 空格段随机（种子 2047+4 复现）：
#          可手算逐段核对
#   点 5  ｜中等规模随机｜长度 60..95，混合字符集（大小写+数字+标点）随机多段
#   点 6  ｜中等规模定向·脆弱实现杀手｜长度 90..110：**空格紧邻标点/数字**
#          （如 "a.  ,b"、"3.14  q!"）——杀「只看空格前后是否为字母」的脆弱实现
#          （来源 [7] a3031655208 的 isspace+isalpha 判据在此数据上会丢空格）；
#          同时含多重长短段
#   点 7  ｜大规模随机｜长度 100..180，混合字符集随机（近上限随机）
#   点 8  ｜大规模随机（近上限）｜长度 190..199（贴住 200 下限一侧随机）
#   点 9  ｜顶格层·最多词数/最多空格段数｜**恰 200 字符 = 题面上限**：
#          100 个词、99 段各 1 个空格（"ab c c ... c"）——输出 = 输入（幂等），
#          扫描/分词路径上词边界最多
#   点 10 ｜顶格层·最大压缩率｜**恰 200 字符 = 题面上限**：1 词 + 198 个空格 + 1 词
#          （"a" + " "*198 + "b"）——输出 "a b"（3 字符），单段最长、压缩比最大，
#          且同时钉住「首尾无空格 + 只留一个空格」的最强形态
#
#   分层项适用性（题面性质决定，详见 gen-report.md「分层对照」）：
#     * 「答案为 0 或 1 的极端」不适用——本题输出是字符串；等价物是
#       **输出=输入的幂等极端**（点 1/2/9）与**压缩到最短的极端**（点 10），均已覆盖。
#     * 「有序/逆序、链」不适用（输入是一行字符，无序列结构）；等价物是
#       **重复值（点 9 的 100 个同字符词）与单点极端结构（点 10 的单段长空格）**。
#     * 「卡常结构」不适用——算法 O(len)、len ≤ 200，实测 std 顶格点 < 2 ms（限 1000 ms），
#       不存在可卡的常数；顶格层按「最大规模 × 两个极端结构」设计。
#     * 「多组数据按组数分层」不适用——单组输入，无组数维度。
#
#   随机性：全部随机点用固定种子（2047 + 点号），逐字节可复现。
#   自检（本文件末尾执行）：
#     1) Python 独立直译题面（第三条路线，与 std 的前向扫描、brute 的按词重排都无关）
#        预测每组期望输出，与 problemN.out **逐字节**比对；
#     2) 断言每组 .in 为**单行**、行末恰一个 '\n'、无行首/行末空格、无连续 '\n'；
#     3) 断言每行长度 ≤ 200（题面上限）、只含可打印非空白 ASCII + 普通空格；
#     4) 断言 10 组 .in/.out 成对齐全、点 3 与题面样例输入/输出逐字节一致；
#     5) 断言点 9/10 的长度恰为 200（顶格）、点 9 输出==输入、点 10 输出为 "a b"。

from cyaron import *  # 引入CYaRon的库

import os
import random
import re
import string

MAX_LEN = 200  # 题面：长度不超过 200

LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGITS = string.digits
PUNCT = ".,!?;:-'\"()"  # 标点（题面样例里出现了 '.'）
MIXED = LOWER + UPPER + DIGITS + PUNCT

SAMPLE_IN = "Hello      world.This is    c language."   # 题面【输入样例】原样
SAMPLE_OUT = "Hello world.This is c language.\n"        # 题面【输出样例】


# ---------------------------------------------------------------------------
# Python 独立真值：按题面直译
#   行 → 用普通空格切分 → 丢空串段 → 以恰一个空格连接
# 这是与 std.cpp（前向跳段扫描）、work/brute.cpp（scanf 按词读取）都不同的第三条路线。
# ---------------------------------------------------------------------------
def truth(stdin_text):
    line = stdin_text.rstrip("\r\n")
    words = [w for w in line.split(" ")]
    return " ".join(w for w in words if w != "") + "\n"


def check_line(line):
    """题面口径合法性检查（生成期断言）。"""
    assert line != "", "输入不得为空行"
    assert len(line) <= MAX_LEN, "长度 %d 超出题面上限 %d" % (len(line), MAX_LEN)
    assert line == line.strip(" "), "句子的头和尾都不得有空格"
    assert "\t" not in line and "\n" not in line and "\r" not in line, "不得含制表符/换行"
    assert all(0x20 <= ord(c) <= 0x7E for c in line), "只允许可打印 ASCII（含普通空格）"
    return line


CASES = []


def add(data_id, line, note):
    assert data_id == len(CASES) + 1, "data_id 必须连续递增"
    check_line(line)
    CASES.append((data_id, line, note))


def make_line(words, gaps):
    """words: 词表；gaps: 相邻词之间的空格数（len = len(words)-1）。"""
    assert len(gaps) == len(words) - 1
    parts = [words[0]]
    for w, g in zip(words[1:], gaps):
        parts.append(" " * g)
        parts.append(w)
    return "".join(parts)


def rand_words(rng, alphabet, n, lo=1, hi=6):
    return ["".join(rng.choice(alphabet) for _ in range(rng.randint(lo, hi))) for _ in range(n)]


# ---- 点 1-2：边界层 ----
add(1, "A",
    "边界层｜理论最小规模：长度 1、无空格（'A'）——输出 = 输入（恒等）")

add(2, "a b",
    "边界层｜最小非平凡：长度 3、恰 1 段 1 个空格（'a b'）——唯一空格段不压缩，"
    "输出 = 输入；钉住「过滤后仍保留一个空格」")

# ---- 点 3：题面声明的特殊值（官方样例原样）----
add(3, SAMPLE_IN,
    "边界层(题面特殊值)｜【输入样例】原样（39 字符、2 段多空格）："
    "期望输出须逐字节等于【输出样例】'Hello world.This is c language.\\n'（31 字符）")

# ---- 点 4：小规模随机（可手算）----
rng4 = random.Random(2047 + 4)
words4 = rand_words(rng4, LOWER, rng4.randint(4, 5), lo=1, hi=3)
gaps4 = [rng4.randint(1, 3) for _ in range(len(words4) - 1)]
line4 = make_line(words4, gaps4)
assert len(line4) <= 12
add(4, line4,
    "小规模随机｜长度 ≤ 12（种子 2047+4 复现）：小写词 + 1..3 空格段，可手算逐段核对")

# ---- 点 5：中等规模随机 ----
rng5 = random.Random(2047 + 5)
while True:
    words5 = rand_words(rng5, MIXED, rng5.randint(12, 16), lo=1, hi=6)
    gaps5 = [rng5.randint(1, 5) for _ in range(len(words5) - 1)]
    line5 = make_line(words5, gaps5)
    if 60 <= len(line5) <= 95:
        break
assert 60 <= len(line5) <= 95
add(5, line5,
    "中等规模随机｜长度 %d（60..95，种子 2047+5 复现）：混合字符集（大小写+数字+标点）"
    "多段随机，范围中间档" % len(line5))

# ---- 点 6：中等规模定向·脆弱实现杀手 ----
# 段落设计：空格紧邻标点/数字，专杀「只看前后是否字母」的 isalpha/isspace 类脆弱实现
# （典型来源 [7] a3031655208 的判据），也让「只保留字母间的空格」类错解必错。
# 反复拼接同一模式至长度 ~100（中等规模上限附近），保持「空格紧邻非字母」高密度。
BASE6_W = ["a.", ",b", "3.14", "q!", "?z", "Hi.", "e-", "-f", "no1", "(g)"]
BASE6_G = [3, 1, 5, 2, 1, 4, 1, 2, 3, 3]
words6 = list(BASE6_W)
gaps6 = list(BASE6_G[:len(words6) - 1])
# 逐词追加，直到再追加一个就会超过 100 字符为止
while True:
    nxt_gap = BASE6_G[len(gaps6) % len(BASE6_G)]
    nxt_word = BASE6_W[len(words6) % len(BASE6_W)]
    if len(make_line(words6, gaps6)) + nxt_gap + len(nxt_word) > 105:
        break
    gaps6.append(nxt_gap)
    words6.append(nxt_word)
line6 = make_line(words6, gaps6)
assert 90 <= len(line6) <= 110, "点 6 长度 %d 超出预期" % len(line6)
assert len(line6) <= MAX_LEN
# 定向断言：至少 2 处的空格一侧是标点/数字（isalpha 类实现会丢这些空格）
adjacent_punct = sum(
    1 for i, g in enumerate(gaps6) if g > 0 and (
        not words6[i][-1].isalpha() or not words6[i + 1][0].isalpha())
)
assert adjacent_punct >= 2, "点 6 必须包含 ≥2 处「空格紧邻非字母」"
add(6, line6,
    "中等规模定向·脆弱实现杀手｜长度 %d（90..110）：多维长空格段且**空格紧邻标点/数字"
    "（%d 处）**——杀「只保留字母间空格 / isalpha 判据」类脆弱实现；含多重长短段"
    % (len(line6), adjacent_punct))

# ---- 点 7：大规模随机 ----
rng7 = random.Random(2047 + 7)
while True:
    words7 = rand_words(rng7, MIXED, rng7.randint(25, 32), lo=1, hi=6)
    gaps7 = [rng7.randint(1, 6) for _ in range(len(words7) - 1)]
    line7 = make_line(words7, gaps7)
    if 100 <= len(line7) <= 180:
        break
assert 100 <= len(line7) <= 180
add(7, line7,
    "大规模随机｜长度约 150（种子 2047+7 复现）：混合字符集随机，接近上限")

# ---- 点 8：大规模随机（近上限）----
rng8 = random.Random(2047 + 8)
while True:
    words8 = rand_words(rng8, MIXED, rng8.randint(35, 45), lo=1, hi=8)
    gaps8 = [rng8.randint(1, 5) for _ in range(len(words8) - 1)]
    line8 = make_line(words8, gaps8)
    if 190 <= len(line8) <= MAX_LEN - 1:   # 190..199：贴住上限、留 1 字符间隔
        break
assert 190 <= len(line8) <= 199
add(8, line8,
    "大规模随机（近上限）｜长度 %d（190..199，种子 2047+8 复现）：贴住题面上限、"
    "多段多词长随机的最大规模随机形态" % len(line8))

# ---- 点 9：顶格层·最多词数 / 最多空格段数 ----
# "ab" + " c"*99 = 2 + 198 = 200 字符；100 个词、99 段各 1 个空格；过滤后原样（幂等）。
line9 = "ab" + " c" * 99
assert len(line9) == 200
add(9, line9,
    "顶格层·最多词数｜**恰 200 字符 = 题面上限**：100 个词、99 段各 1 个空格"
    "（'ab' + ' c'×99）——输出 = 输入（幂等），词/段边界数量最大")

# ---- 点 10：顶格层·最大压缩率 ----
# "a" + 198 个空格 + "b" = 200 字符；过滤后为 "a b"（3 字符），压缩比最大。
line10 = "a" + " " * 198 + "b"
assert len(line10) == 200
add(10, line10,
    "顶格层·最大压缩率｜**恰 200 字符 = 题面上限**：1 词 + 198 个空格 + 1 词"
    "（'a' + ' '×198 + 'b'）——输出 'a b'（3 字符），单段最长、压缩比最大")

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
        runs = len(re.findall(r" +", line))
        print("problem%-2d: 长度=%-3d 空格段数=%-3d 输出长度=%-3d -- %s"
              % (data_id, len(line), runs, len(truth(line + "\n")) - 1, note))

    # ---- 自检 1-5 ----
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
        if body_line != line:
            print("MISMATCH problem%d.in: %r (expect %r)" % (data_id, body_line, line)); bad += 1
        if len(body_line) > MAX_LEN:
            print("TOO LONG problem%d.in: %d > %d" % (data_id, len(body_line), MAX_LEN)); bad += 1
        if any(c == "\t" for c in body_line):
            print("TAB in problem%d.in" % data_id); bad += 1

        # Python 独立真值 vs std 输出（逐字节）
        want = truth(text).encode()
        if raw_out != want:
            print("OUTPUT != TRUTH problem%d: %r (expect %r)" % (data_id, raw_out, want)); bad += 1

    # 点 3 与题面样例逐字节一致
    if open("problem3.in", "rb").read().decode() != SAMPLE_IN + "\n":
        print("SAMPLE INPUT MISMATCH"); bad += 1
    if open("problem3.out", "rb").read().decode() != SAMPLE_OUT:
        print("SAMPLE OUTPUT MISMATCH"); bad += 1

    # 顶格/极端点定向断言
    if len(open("problem9.in", "rb").read().decode()[:-1]) != 200:
        print("POINT 9 NOT AT LIMIT"); bad += 1
    if open("problem9.out", "rb").read().decode() != open("problem9.in", "rb").read().decode():
        print("POINT 9 SHOULD BE IDEMPOTENT (out == in)"); bad += 1
    if len(open("problem10.in", "rb").read().decode()[:-1]) != 200:
        print("POINT 10 NOT AT LIMIT"); bad += 1
    if open("problem10.out", "rb").read().decode() != "a b\n":
        print("POINT 10 SHOULD COMPRESS TO 'a b'"); bad += 1

    # 抽查 2 组人工可核对的小数据
    for probe_id, want_out in ((1, "A\n"), (2, "a b\n")):
        got = open("problem%d.out" % probe_id, "rb").read().decode()
        if got != want_out:
            print("PROBE FAIL problem%d: %r != %r" % (probe_id, got, want_out)); bad += 1

    if bad:
        print("SELF-CHECK FAILED: %d issue(s)" % bad)
        raise SystemExit(1)

    print()
    print("SELF-CHECK OK: 10/10 .in/.out 成对齐全；每组 .in 均为单行（行末恰一个 '\\n'、"
          "无行首/行末空格、无制表符）；每行长度 <= %d；" % MAX_LEN)
    print("              每组 .out == Python 独立直译真值（第三条路线）；"
          "点 3 与题面样例逐字节一致；点 9/10 恰为 200 字符顶格。")
    print("分层覆盖：边界 3 点（len1/最小非平凡/样例）+ 小规模 1 点 + 中等 2 点（随机+定向）"
          "+ 大规模 2 点 + 顶格 2 点（最多词数/最大压缩率）。")


if __name__ == "__main__":
    main()
