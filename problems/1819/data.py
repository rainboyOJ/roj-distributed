#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1819《字符串游戏》分层数据生成器 + 用 std 显式产出 .out
#
# 题面范围（100%）：1≤n≤10^5，1≤k≤10^9，所有字符串长度不超过 10^5，数据组数不超过 10 组。
# 本生成器口径：**每组数据**的字符串长度总和 ≤ 10^5（题面未明说「总和/单串」，
#   取更保守的读法；单串也 ≤ 10^5）；k ∈ [1,1e9]；组数 ∈ [1,10]。
# 输入无 T，多组数据读到 EOF。
#
# 分层（10 组，边界/小/中/大/顶格）：
#   点1  题面样例原样（3 组，含 k=1/2/3 与多组数据）→ HY/HY/Teacher
#   点2  极小边界：n=1、k=1/1e9、单字符/双字符 → 覆盖 !win 与 奇偶 两支
#   点3  手推混合小数据：win&&lose / win&&!lose / !win 三分支全覆盖
#   点4  深链顶格：|s|≈1e5 的单串长链（考验栈深），含 k 偶数下的 HY 胜
#   点5  n 顶格：n=10^5（每串长 1，字母循环重复），k 奇偶各一组
#   点6  结构边界：满 26 叉一层 / 满 26 叉两层（!win）
#   点7  随机小：n=50，|s|≤6，字母表 4（结构密集）
#   点8  随机中：n=1000，|s|≤10，字母表 26
#   点9  大且答案可手推：a + 「b」前缀满三层 26 叉（win&&lose→HY）；7 字母满 5 层（!win）
#   点10 顶格多组：10 组数据，总量 ≈ 9e5 字符，奇偶 k 混搭（性能顶格）
#
# 说明：所有 .out 均由 std.cpp 编译出的可执行文件经 subprocess 显式跑出（无缓冲丢失风险），
#       并断言非空、行数 == 组数、行内容合法；手推点额外断言精确答案。
import itertools
import os
import random
import subprocess
import sys
import tempfile
import time

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, 'data')
ALPHA = 'abcdefghijklmnopqrstuvwxyz'
HY = 'HY wins!'
TE = 'Teacher wins!'
ALLOWED = {HY, TE}


def all_words(prefix, alphabet, depth):
    """prefix + 由 alphabet 组成的所有 depth 长后缀（不排序，itertools 顺序）。"""
    return [prefix + ''.join(t) for t in itertools.product(alphabet, repeat=depth)]


def rand_words(n, lo, hi, alphabet, rng):
    return [''.join(rng.choice(alphabet) for _ in range(rng.randint(lo, hi))) for _ in range(n)]


def write_in(path, groups):
    lines = []
    for n, k, ss in groups:
        assert len(ss) == n, f'{path}: n={n} 与串数 {len(ss)} 不符'
        assert 1 <= n <= 100000 and 1 <= k <= 10 ** 9
        total = 0
        for s in ss:
            assert s and s.islower() and s.isalpha() and len(s) <= 100000, repr(s[:40])
            total += len(s)
        assert total <= 100000, f'{path}: 该组总长 {total} 超 1e5'
        lines.append(f'{n} {k}')
        lines.extend(ss)
    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    assert len(groups) <= 10
    return len(groups)


def build_points():
    rng = random.Random(1819)
    pts = []

    # ---- 点1：题面样例 ----
    pts.append(('题面样例（3 组）', [(2, 3, ['a', 'b']), (3, 1, ['a', 'b', 'c']), (1, 2, ['ab'])],
                [HY, HY, TE]))

    # ---- 点2：极小边界 ----
    pts.append(('n=1 极小 + k 边界', [
        (1, 1, ['a']),            # win&&!lose, k 奇 -> HY
        (1, 1, ['aa']),           # !win -> Teacher
        (1, 10 ** 9, ['a']),      # k 偶 -> Teacher
        (1, 999999999, ['aa']),   # !win, k 奇 -> Teacher
        (1, 1, ['z']),            # 字母表右端边界 -> HY
    ], [HY, TE, TE, TE, HY]))

    # ---- 点3：手推混合（三分支全覆盖） ----
    pts.append(('手推混合小数据（三分支）', [
        (3, 2, ['ab', 'ac', 'b']),      # win&&lose, k 偶 -> HY
        (2, 2, ['a', 'bcd']),           # win&&!lose, k 偶 -> Teacher
        (2, 3, ['a', 'bcd']),           # win&&!lose, k 奇 -> HY
        (2, 2, ['ab', 'ac']),           # !win -> Teacher
        (3, 1, ['a', 'b', 'c']),        # 满 3 叉一层, k=1 -> HY
        (2, 10 ** 9, ['a', 'bc']),      # win&&lose, k 偶 -> HY
    ], [HY, TE, HY, TE, HY, HY]))

    # ---- 点4：深链顶格（|s|≈1e5，栈深/长串） ----
    pts.append(('深链顶格 |s|≈1e5', [
        (2, 10 ** 9, ['a', 'b' + 'c' * 99997]),   # b 下链深 99997(奇) -> win&&lose, k 偶 -> HY
        (1, 10 ** 9, ['d' + 'e' * 99997]),        # 单串偶长(99998) -> !win -> Teacher
    ], [HY, TE]))

    # ---- 点5：n 顶格 ----
    big_n = [ALPHA[i % 26] for i in range(100000)]
    pts.append(('n=1e5 顶格（每串长1）', [
        (100000, 10 ** 9, big_n),      # 26 叶子子 -> win&&!lose, k 偶 -> Teacher
        (100000, 999999999, big_n),    # k 奇 -> HY
    ], [TE, HY]))

    # ---- 点6：结构边界（满树） ----
    pts.append(('满 26 叉一层/两层', [
        (26, 999999999, list(ALPHA)),                      # 一层 -> HY
        (676, 1, all_words('', ALPHA, 2)),                 # 两层 -> !win -> Teacher
        (26, 10 ** 9, list(ALPHA)),                        # 一层, k 偶 -> Teacher
    ], [HY, TE, TE]))

    # ---- 点7：随机小（密集结构） ----
    pts.append(('随机小 n=50 |s|<=6 字母表4', [(50, 1, rand_words(50, 1, 6, 'abcd', rng))], None))

    # ---- 点8：随机中 ----
    pts.append(('随机中 n=1000 |s|<=10', [(1000, 999999999, rand_words(1000, 1, 10, ALPHA, rng))], None))

    # ---- 点9：大且答案可手推 ----
    #   满 A 叉深 d 树：win[根] = (d 奇)，lose[根] = (d 偶) —— d 偶则先手必败。
    pts.append(('大：b 前缀满 3 层 26 叉 + 11 字母满 4 层', [
        # 结构：根子 'a'(叶) 与 'b'(深 3 奇 -> win=true, lose=false) -> win&&lose -> 任意 k 均 HY
        (1 + 26 ** 3, 10 ** 9, ['a'] + all_words('b', ALPHA, 3)),
        # 全 4 长串（11 字母）-> 满树深 4(偶) -> !win -> Teacher
        (11 ** 4, 999999999, all_words('', ALPHA[:11], 4)),
    ], [HY, TE]))

    # ---- 点10：顶格多组（10 组） ----
    g10 = [
        (2000, 10 ** 9, rand_words(2000, 40, 50, ALPHA, rng)),
        (1 + 26 ** 3, 10 ** 9, ['a'] + all_words('b', ALPHA, 3)),      # win&&lose -> HY（手推）
        (7 ** 5, 999999999, all_words('', ALPHA[:7], 5)),              # 满树深5(奇)+k奇 -> HY（手推）
        (2000, 1, rand_words(2000, 40, 50, 'ab', rng)),
        (5 ** 6, 10 ** 9, all_words('', ALPHA[:5], 6)),                # 满树深6(偶) -> Teacher（手推）
        (1 + 5 ** 5, 10 ** 9, ['a'] + all_words('b', ALPHA[:5], 5)),   # win&&lose -> HY（手推）
        (4000, 999999999, rand_words(4000, 15, 24, ALPHA, rng)),
        (676, 10 ** 9, all_words('', ALPHA, 2)),                       # 满树深2(偶) -> Teacher（手推）
        (20000, 1, rand_words(20000, 1, 4, 'abc', rng)),
        (2, 10 ** 9, ['a', 'b' + 'c' * 99997]),                        # 深链 win&&lose -> HY（手推）
    ]
    pts.append(('顶格 10 组 / 总量≈7e5 字符', g10,
                [None, HY, HY, None, TE, HY, None, TE, None, HY]))
    return pts


def compile_std(workdir):
    binpath = os.path.join(workdir, 'std1819')
    compilers = ['g++-16', 'g++', 'clang++']
    err = ''
    for cc in compilers:
        try:
            r = subprocess.run([cc, '-O2', '-std=c++17', '-o', binpath, os.path.join(BASE, 'std.cpp')],
                               capture_output=True, text=True, timeout=120)
        except FileNotFoundError:
            continue
        if r.returncode == 0:
            print(f'[build] {cc} -O2 -std=c++17 -> ok')
            return binpath
        err = r.stderr
    raise SystemExit(f'compile failed: {err}')


def main():
    os.makedirs(DATA, exist_ok=True)
    pts = build_points()
    assert len(pts) == 10, len(pts)
    tmpdir = tempfile.mkdtemp(prefix='ybt1819_')
    binpath = compile_std(tmpdir)

    print(f'{"点":>3} {"组数":>4} {"字符数":>8} {"秒":>6}  答案')
    ok = True
    for i, (desc, groups, expect) in enumerate(pts, 1):
        in_path = os.path.join(DATA, f'problem{i}.in')
        out_path = os.path.join(DATA, f'problem{i}.out')
        ngroups = write_in(in_path, groups)
        t0 = time.time()
        with open(in_path, 'rb') as fi, open(out_path, 'wb') as fo:
            subprocess.run([binpath], stdin=fi, stdout=fo, check=True, timeout=120)
        dt = time.time() - t0

        raw = open(out_path, 'rb').read()
        assert raw, f'problem{i}.out 为空'
        lines = raw.decode().split('\n')
        assert lines[-1] == '', f'problem{i}.out 末行缺换行'
        lines = lines[:-1]
        assert len(lines) == ngroups, f'problem{i}: 输出 {len(lines)} 行 != 组数 {ngroups}'
        for ln in lines:
            assert ln in ALLOWED, f'problem{i}: 非法行 {ln!r}'
        if expect is not None:
            assert len(expect) == ngroups
            for g, (got, exp) in enumerate(zip(lines, expect), 1):
                if exp is not None and got != exp:
                    ok = False
                    print(f'  !! problem{i} 组{g}: got {got!r} expected {exp!r}')
        chars = os.path.getsize(in_path)
        tag = '/'.join('HY' if l == HY else 'TE' for l in lines)
        print(f'{i:>3} {ngroups:>4} {chars:>8} {dt:>6.2f}  {tag}   {desc}')
    print('[verify] 非空/行数/行内容 全部通过；手推点答案一致' if ok else '[verify] 手推点存在不一致！')
    subprocess.run(['rm', '-rf', tmpdir], check=True)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
