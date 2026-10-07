#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 一本通 2050《【例5.20】字串包含》分层数据生成器（cyaron）
# 参考仓库惯例：problems/1000/data.py、problems/5006/data.py、staging/2040/data.py
# 目标 ROJ 题号：5052（落地由主控脚本完成，本包只在 staging/2050/ 内产出）
#
# ── 题意 ──────────────────────────────────────────────────────────────────
# 一次循环移位 = 把首字符移到末尾。判定「其中一个字符串是否是另一字符串经过若干次
# 循环移位后的新串的子串」；是则输出 true，否则 false。
# 例：CDAA 是 AABCD 两次移位后的新串 BCDAA 的子串 -> true；
#     ABCD 与 ACBD 无论如何移位都不能互相包含 -> false。
#
# ── 数据范围（题面唯一声明）────────────────────────────────────────────────
# 一行，两个字符串，单个空格隔开；只含字母和数字；**长度不超过 30**。
# 限制：time 1000 ms / memory 64 MB（config.json）。
# 本题是**单组输入**（一个测试点 = 一对字符串），不存在「多组数据按组数分层」，
# 规模维度是**字符串长度**（1..30）与**结构**（是否含循环移位包含关系）。
#
# ── 分层表（10 组）────────────────────────────────────────────────────────
#   点 1  边界层（全最小值）：|s1|=|s2|=1，答案 true —— 最短可能的正例
#   点 2  边界层（全最大值 + 负例极端）：|s1|=|s2|=30 且字符集不交 -> false
#   点 3  小规模（题面声明值）：题面【输入样例】AABCD / CDAA -> true，可手算
#   点 4  小规模结构（错解陷阱）：|s2|>|s1| 且跨周期，aba / baab -> false
#        —— 「无条件双向 s2 in s1+s1 或 s1 in s2+s2」的经典错解在此假阳性
#   点 5  小规模随机：|s| ∈ [1,5]，字母表 {a,b} —— 短到可手算验证
#   点 6  中等规模随机：|s| ∈ [10,20]，字母表 {a,b,c} —— 范围中间档
#   点 7  中等规模结构（反向包含）：|s2| > |s1|，s1 只藏在 s2 的某个循环移位里
#        -> true，「只把 s1 当容器」的错误实现会漏判
#   点 8  大规模随机（接近上限）：|s1| = 30 随机，s2 = 某循环移位的随机截断 -> true
#   点 9  顶格层结构：周期串 ("aab"*10) 的跨接缝子串（|s1|=30, |s2|=7）-> true
#   点 10 顶格层结构（最坏负例）：a^30 / a^29+b，30/30 且只差一个字符 -> false
#
# 自检：data.py 内置**独立的 Python 真值实现**（显式枚举全部循环移位再查子串，
# 与 std.cpp 的 s1+s1 化简路线不同），逐点断言 std 输出 == Python 真值；
# 同时断言长度 ≤ 30、字符集仅字母数字。
#
# 随机性：每个随机点用独立 random.Random(2050 + 点号)，与调用顺序无关、可复现。

from cyaron import *  # 引入CYaRon的库

import random
import re

MAXLEN = 30  # 题面上限：长度不超过 30
ALNUM = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


# ── 独立的 Python 真值实现（题面字面语义，用于逐点自检 std 输出）────────────
def rotations(s):
    """s 的全部循环移位串（|s| 个；移位 0 次与 |s| 次同为 s，集合一致）。"""
    return {s[i:] + s[:i] for i in range(len(s))}


def stmt_truth(a, b):
    """题面：其中一个字符串是否是另一字符串若干次循环移位后的新串的子串。"""
    return any(b in r for r in rotations(a)) or any(a in r for r in rotations(b))


def naive_wrong_both(a, b):
    """经典错解（仅供区分度说明，不参与真值）：无条件双向倍长检查。"""
    return (b in a + a) or (a in b + b)


# ── 用例构造 ──────────────────────────────────────────────────────────────
def random_pair(seed, lo1, hi1, lo2, hi2, alphabet):
    """独立随机源生成一对随机串（长度在给定区间内）。"""
    rnd = random.Random(seed)
    a = "".join(rnd.choice(alphabet) for _ in range(rnd.randint(lo1, hi1)))
    b = "".join(rnd.choice(alphabet) for _ in range(rnd.randint(lo2, hi2)))
    return a, b


def planted_rotation_substring(seed, container_len, s_lo, s_hi, alphabet):
    """构造「短串是长串某个循环移位的子串」的正例（匹配可跨接缝）。"""
    rnd = random.Random(seed)
    c = "".join(rnd.choice(alphabet) for _ in range(container_len))
    k = rnd.randrange(container_len)
    rot = c[k:] + c[:k]                      # c 的一个循环移位
    L = rnd.randint(s_lo, s_hi)
    start = rnd.randrange(container_len - L + 1)
    return c, rot[start:start + L]           # (长, 短)：短串落在 rot 内 -> true


def build_point7(seed):
    """点 7：反向包含正例 —— |s2| > |s1|，s1 只出现在 s2 的某个循环移位里。

    构造：core = s1；取 k ∈ [1,|core|-1]、rot = core 的第 k 次移位、
    suf 以 core[k:] 开头，令 s2 = pre + rot + suf。
    则把 s2 左移 |pre| 格得到 rot+suf+pre = core[k:] + core[:k] + core[k:] + junk + pre
                                                   = core[k:] + core + junk + pre，
    其中 core 连续出现 —— 即 s1 是 s2 某个循环移位的子串（且 s2 更长，反方向不可能）。
    """
    rnd = random.Random(seed)
    n = rnd.randint(6, 9)
    core = "".join(rnd.choice("abc") for _ in range(n))          # s1
    k = rnd.randint(1, n - 1)
    rot = core[k:] + core[:k]
    pre = "".join(rnd.choice("abc") for _ in range(rnd.randint(2, 4)))
    suf = core[k:] + "".join(rnd.choice("abc") for _ in range(rnd.randint(0, 2)))
    s2 = pre + rot + suf                                          # 保证 |s2| > |core|
    return core, s2


def build_point8(seed):
    """点 8：接近上限的随机正例 —— |s1|=30 随机（字母表 {a,b}），
    s2 取 s1 某个随机循环移位的一段随机截断，长度 ∈ [15,30]（可能跨接缝），
    使该点成为真正的大规模随机点（而非短串退化为平凡包含）。"""
    return planted_rotation_substring(seed, MAXLEN, 15, MAXLEN, "ab")


def build_point9():
    """点 9：顶格层周期结构正例 —— s1 = "aab"*10（|s1|=30），
    s2 = (s1+s1)[26:33]，长度 7；该子串从 s1 末端跨到开头，只有环形展开才能匹配。"""
    s1 = "aab" * 10
    s2 = (s1 + s1)[26:33]
    return s1, s2


# ── 10 个测试点 ------------------------------------------------------------
RND5 = random_pair(2050 + 5, 1, 5, 1, 5, "ab")            # 点 5：小规模随机
RND6 = random_pair(2050 + 6, 10, 20, 10, 20, "abcXYZ079")  # 点 6：中等规模随机（含数字/大写）
P7 = build_point7(2050 + 7)                               # 点 7：反向包含正例
P8 = build_point8(2050 + 8)                               # 点 8：贴近上限的随机正例
P9 = build_point9()                                       # 点 9：周期串跨接缝正例

CASES = [
    ("a", "a",
     "边界层（全最小值）：|s1|=|s2|=1，长度取题面下界 1；答案 true（最短正例）"),
    ("a" * 30, "b" * 30,
     "边界层（全最大值 + 负例极端）：|s1|=|s2|=30 顶格长度，字符集不交，"
     "任何移位都无法互相包含 -> false"),
    ("AABCD", "CDAA",
     "题面【输入样例】：题面唯一声明值，可手算（AABCD 两次移位得 BCDAA，CDAA 是其子串）-> true"),
    ("aba", "baab",
     "小规模结构（错解陷阱）：|s2|>|s1| 且 s2 恰好跨 s1 的两个周期片段，"
     "题面语义为 false；错解 `b in a+a or a in b+b` 会在此假阳性输出 true"),
    (RND5[0], RND5[1],
     "小规模随机：|s| ∈ [1,5]，字母表 {a,b}（短到可手算验证，随机关系含包裹式匹配）"),
    (RND6[0], RND6[1],
     "中等规模随机：|s| ∈ [10,20]，字母表 {a,b,c,X,Y,Z,0,7,9}"
     "（范围中间档；覆盖题面声明的「字母和数字」字符集中的数字与大写字母）"),
    (P7[0], P7[1],
     "中等规模结构（反向包含）：|s2| > |s1|，s1 只出现在 s2 的某个循环移位里 -> true；"
     "「只把 s1 当容器、不做长度判定」的实现会漏判"),
    (P8[0], P8[1],
     "大规模随机（接近上限）：|s1|=30 顶格随机，s2 = 某循环移位的随机截断"
     "（长度 ∈ [15,30]，可能跨接缝）-> true"),
    (P9[0], P9[1],
     "顶格层结构（跨接缝正例）：s1 = ('aab'*10) 长 30 周期串，s2 = (s1+s1)[26:33] 长 7，"
     "匹配从 s1 末端跨到开头 -> true"),
    ("a" * 30, "a" * 29 + "b",
     "顶格层结构（最坏负例）：30/30 顶格长度且只差一个字符，两条路都不成立 -> false"),
]

# ── 生成 + 逐点自检 ─────────────────────────────────────────────────────────
print("一本通 2050《【例5.20】字串包含》数据生成（10 组，单组输入）")
print("-" * 96)
for idx, (a, b, note) in enumerate(CASES, start=1):
    # 输入合法性自检（题面：只含字母和数字，长度 ≤ 30）
    assert 1 <= len(a) <= MAXLEN, "s1 长度越界: %d" % len(a)
    assert 1 <= len(b) <= MAXLEN, "s2 长度越界: %d" % len(b)
    assert re.fullmatch(r"[A-Za-z0-9]+", a) and re.fullmatch(r"[A-Za-z0-9]+", b), \
        "字符串含非字母数字字符: %r %r" % (a, b)
    assert " " not in a and " " not in b, "字符串含空格"

    io = IO(file_prefix="problem", data_id=idx)   # problem{idx}.in / problem{idx}.out
    io.input_writeln(a, b)                        # 一行，两个字符串，单个空格隔开
    io.output_gen("../std")                       # 用编译后的标程产出 .out
    io.output_file.flush()                        # cyaron 的 .out 是带缓冲句柄，读回前先落盘

    truth = stmt_truth(a, b)                      # Python 独立真值
    got = open("problem%d.out" % idx, encoding="utf-8").read().strip()
    assert got == ("true" if truth else "false"), \
        "点 %d 输出与 Python 真值不符: std=%r truth=%s" % (idx, got, truth)

    print("problem%-2d | s1=%-32r | s2=%-32r | std=%-5s | 真值=%-5s | %s"
          % (idx, a, b, got, "true" if truth else "false", note))

# 区分度说明：错解在点 4 上会给出 true（题面真值 false）
_w = naive_wrong_both(CASES[3][0], CASES[3][1])
print("-" * 96)
print("区分度自检：点 4 (aba/baab) 题面真值 = %s，经典错解（无条件双向倍长）给出 %s -> %s"
      % (stmt_truth(*CASES[3][:2]), _w, "可区分错解" if _w != stmt_truth(*CASES[3][:2]) else "未区分"))
print("全部 10 个测试点生成完毕，且与 Python 独立真值逐点一致。")
