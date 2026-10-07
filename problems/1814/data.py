#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一本通 1814「方格染色」造数据脚本 (10 组, 分层: 边界/小/中/大/顶格)

输入格式: 一行三个正整数 n m k  (2<=n<=300, n^2<=m<=100000, n<=k<=m)
输出格式: 一行一个实数, 期望得分 (答案>1e99 输出 1e99; 相对误差 <=1e-6)

分层表 (data/problem{1..10}.in/.out):
  problem1  : n=2  m=4      k=2      最小边界 (n 最小, m=n^2 最小)    手算 5/3
  problem2  : n=2  m=4      k=4      最小 k=m 边界 (全黑)              手算 2^4=16
  problem3  : n=2  m=100000 k=2      m 顶格 + n 最小 (近 1 的小答案)   手算 1+4k(k-1)/(m(m-1))
  problem4  : n=3  m=9      k=3      m=n^2 边界, k=n 边界              手算 15/14
  problem5  : n=3  m=10     k=5      30% 层 m<=10 边界                 手算 43/28
  problem6  : n=5  m=25     k=25     小 n, k=m (全黑)                  手算 2^10=1024
  problem7  : n=10 m=200    k=200    60% 层边界 (m<=200), k=m         手算 2^20=1048576
  problem8  : n=100 m=10000 k=9900   中 n, k 接近 m (大答案求和路径)   仅范围断言
  problem9  : n=300 m=90000 k=89000  n 顶格, m=n^2, 长 log 前缀        仅范围断言
  problem10 : n=300 m=100000 k=100000 全顶格, k=m (答案 2^600 被截断)  手算 1e99

校验策略 (不写/不跑任何 brute、对拍、stress):
  - 手算点: 由题面概率模型独立推导的闭式值直接断言 (见下方 HAND 注释);
  - 通用断言: 输出恰 1 行且非空; 1 <= ans <= min(2^(2n), 1e99)*(1+eps); k=m 时 ans=min(2^(2n),1e99)。
  - 生成器本身 O(1)/组 (只写 3 个整数), 无任何 O(n^2) Python 循环。

运行: nice -n 19 timeout 120 python3 data.py
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
STD_CPP = os.path.join(HERE, "std.cpp")
BIN = os.path.join(HERE, ".std_bin")

REL_TOL = 1e-9   # std 双精度误差 ~1e-12, 留 3 个数量级余量


def compile_std():
    for cxx in ("g++-16", "g++", "clang++"):
        path = shutil.which(cxx)
        if not path:
            continue
        r = subprocess.run([path, "-O2", "-std=c++17", "-o", BIN, STD_CPP],
                           capture_output=True, text=True)
        if r.returncode == 0:
            print("[compile] %s -O2 -std=c++17 -> %s" % (cxx, os.path.basename(BIN)))
            return
        print("[compile] %s failed: %s" % (cxx, r.stderr.strip().splitlines()[:1]))
    raise SystemExit("no working C++ compiler")


def run_std(inp):
    r = subprocess.run([BIN], input=inp, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise SystemExit("std runtime error: %s" % r.stderr[:500])
    return r.stdout


def close_to(got, want):
    return abs(got - want) <= REL_TOL * max(1.0, abs(want))


def emit(idx, n, m, k, note, hand=None, hand_desc=""):
    """写 problem{idx}.in, 用 std 显式跑出 problem{idx}.out, 断言非空/1 行/数值合理"""
    inp = "%d %d %d\n" % (n, m, k)
    out = run_std(inp)
    lines = out.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    assert len(lines) == 1, "problem%d: expect exactly 1 line, got %r" % (idx, out)
    assert lines[0].strip() != "", "problem%d: empty output" % idx
    val = float(lines[0])

    # 通用上下界: 得分 2^{r+c} 恒在 [1, 2^{2n}] 内, 且被 1e99 截断
    upper = min(2.0 ** (2 * n), 1e99)
    assert val >= 1.0 - REL_TOL, "problem%d: ans=%r < 1" % (idx, val)
    assert val <= upper * (1 + REL_TOL), "problem%d: ans=%r > min(2^2n,1e99)=%r" % (idx, val, upper)
    if k == m:
        assert close_to(val, upper), "problem%d: k=m should give %r, got %r" % (idx, upper, val)

    # 手算点
    if hand is not None:
        assert close_to(val, hand), \
            "problem%d: hand-check failed: got %r want %r (%s)" % (idx, val, hand, hand_desc)

    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "problem%d.in" % idx), "w") as f:
        f.write(inp)
    with open(os.path.join(DATA, "problem%d.out" % idx), "w") as f:
        f.write(lines[0] + "\n")
    tag = "  [hand %s]" % hand_desc if hand is not None else ""
    print("[data] problem%d: n=%-3d m=%-6d k=%-6d ans=%-18.10e  %s%s"
          % (idx, n, m, k, val, note, tag))
    return val


def main():
    compile_std()

    # 手算闭式 (由题面概率模型独立推导, 非脚本内重算):
    #   (2,4,2):  2 黑格同行/同列各 2/6 概率 -> 1 + 4*(1/6) = 5/3
    #   (2,4,4):  全黑 -> r=c=2 -> 2^4 = 16
    #   (2,1e5,2): 两数都在棋盘 (概率 C(4,2)/C(1e5,2)) 时 5/3, 否则 1 -> 1 + 4k(k-1)/(m(m-1))
    #   (3,9,3):  1 + 6*C(3,3)/C(9,3) = 1 + 6/84 = 15/14
    #   (3,10,5): B=5 (p=1/2): 1+6*(5/42)+9*(1/126)=25/14; B=4 (p=1/2): 1+6*(1/21)=9/7
    #             -> (25/14+18/14)/2 = 43/28
    #   (5,25,25),(10,200,200): k=m 全黑 -> 2^(2n)
    #   (300,1e5,1e5): 2^600 ≈ 4.15e180 > 1e99 -> 1e99
    cases = [
        (1, 2, 4, 2, "最小边界 n=2,m=n^2=4", 5.0 / 3.0, "5/3"),
        (2, 2, 4, 4, "最小 k=m 边界 (全黑)", 16.0, "2^4"),
        (3, 2, 100000, 2, "m 顶格 + n 最小, 近 1 小答案",
         1.0 + 4.0 * 2 * 1 / (100000.0 * 99999.0), "1+4k(k-1)/(m(m-1))"),
        (4, 3, 9, 3, "m=n^2 边界, k=n 边界", 15.0 / 14.0, "15/14"),
        (5, 3, 10, 5, "30% 层 m<=10 边界", 43.0 / 28.0, "43/28"),
        (6, 5, 25, 25, "小 n, k=m 全黑", 1024.0, "2^10"),
        (7, 10, 200, 200, "60% 层边界 m<=200, k=m", 1048576.0, "2^20"),
        (8, 100, 10000, 9900, "中 n, k 接近 m (大答案求和)", None, ""),
        (9, 300, 90000, 89000, "n 顶格, m=n^2, 长 log 前缀", None, ""),
        (10, 300, 100000, 100000, "全顶格, k=m -> 2^600 截断 1e99", 1e99, "1e99(cap)"),
    ]
    for idx, n, m, k, note, hand, hdesc in cases:
        # 约束自检: 2<=n<=300, n^2<=m<=1e5, n<=k<=m
        assert 2 <= n <= 300 and n * n <= m <= 100000 and n <= k <= m, \
            "problem%d: constraint violated (%d,%d,%d)" % (idx, n, m, k)
        emit(idx, n, m, k, note, hand, hdesc)

    files = sorted(os.listdir(DATA))
    print("[check] data/ 共 %d 个文件: %s" % (len(files), " ".join(files)))
    assert files == sorted("problem%d.%s" % (i, e) for i in range(1, 11) for e in ("in", "out")), \
        "data/ 文件命名不符合 problem1..10.in/.out"
    print("[clean] 删除编译产物 %s" % os.path.basename(BIN))
    if os.path.exists(BIN):
        os.remove(BIN)


if __name__ == "__main__":
    main()
