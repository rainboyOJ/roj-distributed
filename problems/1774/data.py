#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一本通 1774《大逃杀》造数据脚本。
分层：边界 / 小 / 中 / 大 / 顶格，共 10 组，产出 data/problem1..10.in 与 .out。

说明：
- 不使用 cyaron 的 output_gen（其写缓冲不 flush 会产出 0 字节 .out）；改为编译 std.cpp 后
  用 subprocess 显式运行生成 .out，并断言 .out 非空且恰好 1 行（本题输出恒为一行整数，
  故不存在“无解空输出点”）。
- 数组上限按题面上限 N=305 开（std 内），本脚本生成的数据满足 n,T<=300，0<=w_i,t_i,c<=1e6。
- 树构造均为 O(n)，无 O(n^2) Python 循环。
- 编译产物用临时目录承载，运行结束后删除（清理编译产物）。
"""
import os
import random
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

random.seed(20240517)


def make_case(n, T, w, t, edges):
    lines = ["%d %d" % (n, T),
             " ".join(str(x) for x in w),
             " ".join(str(x) for x in t)]
    for a, b, c in edges:
        lines.append("%d %d %d" % (a, b, c))
    return "\n".join(lines) + "\n"


def rand_tree(n, cmax, span=None):
    """随机树：点 i 的父亲在 [max(1,i-span), i-1] 中随机（O(n) 构造）。"""
    edges = []
    for i in range(2, n + 1):
        lo = 1 if span is None else max(1, i - span)
        fa = random.randint(lo, i - 1)
        edges.append((fa, i, random.randint(0, cmax)))
    return edges


def path_tree(n, cmax):
    return [(i, i + 1, random.randint(0, cmax)) for i in range(1, n)]


def star_tree(n, cmax):
    return [(1, i, random.randint(0, cmax)) for i in range(2, n + 1)]


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


def build_cases():
    cases = []

    # 1. 边界：n=1, T=0，无敌人，拿到唯一资源（最大值 1e6）
    cases.append(("边界 n=1 T=0 单点可拿", make_case(1, 0, [1000000], [0], [])))

    # 2. 边界：n=1, T=0，敌人耗时 1>T，什么也拿不到（答案 0）
    cases.append(("边界 n=1 敌人耗时超过 T", make_case(1, 0, [1000000], [1], [])))

    # 3. 小：n=2，T=1，边权 1，两端都无敌人，可走完全程
    cases.append(("小 n=2 一条边", make_case(2, 1, [5, 7], [0, 0], [(1, 2, 1)])))

    # 4. 小：n=5 链，全部无敌人（t_i=0 特殊性质）
    cases.append(("小 n=5 链 全无敌人",
                  make_case(5, 300, rnd(5, 0, 10), [0] * 5, path_tree(5, 3))))

    # 5. 中：n=10 星形（1 为心），小值
    cases.append(("中 n=10 星形",
                  make_case(10, 300, rnd(10, 0, 20), rnd(10, 0, 5), star_tree(10, 5))))

    # 6. 中：n=50 链（度数不超过 2 的特殊性质），值/耗时中等
    cases.append(("中 n=50 链 大值",
                  make_case(50, 300, rnd(50, 0, 1000000), rnd(50, 0, 100),
                            path_tree(50, 1000))))

    # 7. 大：n=100 随机树，T=300，混合规模
    cases.append(("大 n=100 随机树",
                  make_case(100, 300, rnd(100, 0, 1000000), rnd(100, 0, 300),
                            rand_tree(100, 100, 5))))

    # 8. 顶格 n=300 星形，T=300，边权可大到 1e6（大量边不可用）
    cases.append(("顶格 n=300 星形",
                  make_case(300, 300, rnd(300, 0, 1000000), rnd(300, 0, 300),
                            star_tree(300, 1000000))))

    # 9. 顶格 n=300 链（度数<=2），T=300，全部无敌人，边权 1e6 内
    cases.append(("顶格 n=300 链 全无敌人",
                  make_case(300, 300, rnd(300, 0, 1000000), [0] * 300,
                            path_tree(300, 1000000))))

    # 10. 顶格 n=300 随机树，T=300，w/c 取到 1e6 量级，t 落在可行范围内
    cases.append(("顶格 n=300 随机树 极值",
                  make_case(300, 300, rnd(300, 0, 1000000), rnd(300, 0, 300),
                            rand_tree(300, 1000000, 8))))

    return cases


SAMPLE_IN = """17 54
5 5 1 1 1 25 1 10 15 3 6 6 66 4 4 4 4
0 1 3 0 0 0 1 3 2 0 6 7 54 0 0 0 0
1 8 3
2 8 3
8 7 7
7 13 0
7 14 0
15 14 2
16 14 3
17 14 5
7 9 4
9 10 25
10 11 0
10 12 0
7 6 20
3 6 3
3 4 3
3 5 3
"""


def main():
    tmp = tempfile.mkdtemp(prefix="ybt1774_")
    try:
        exe = os.path.join(tmp, "std")
        subprocess.run(["g++", "-O2", "-o", exe, os.path.join(HERE, "std.cpp")],
                       check=True)

        # 样例校验
        r = subprocess.run([exe], input=SAMPLE_IN, capture_output=True,
                           text=True, timeout=120)
        got = r.stdout.strip()
        assert got == "68", "sample mismatch: got %r" % got
        print("[sample] 17 54 -> %s (expected 68) OK" % got)

        if os.path.isdir(DATA):
            shutil.rmtree(DATA)
        os.makedirs(DATA)

        cases = build_cases()
        assert len(cases) == 10, "need 10 cases"

        for idx, (name, content) in enumerate(cases, 1):
            ip = os.path.join(DATA, "problem%d.in" % idx)
            op = os.path.join(DATA, "problem%d.out" % idx)
            with open(ip, "w", encoding="utf-8") as f:
                f.write(content)
            with open(ip, "r", encoding="utf-8") as fin:
                r = subprocess.run([exe], stdin=fin, capture_output=True,
                                   text=True, timeout=120)
            assert r.returncode == 0, "std failed on case %d: %s" % (idx, r.stderr)
            with open(op, "w", encoding="utf-8") as f:
                f.write(r.stdout)
            with open(op, "r", encoding="utf-8") as f:
                out = f.read()
            assert out.strip() != "", "case %d empty .out" % idx
            assert len(out.strip().splitlines()) == 1, \
                "case %d .out line count != 1" % idx
            print("[case %2d] %-30s -> %s" % (idx, name, out.strip()))

        print("done: 10 cases in %s" % DATA)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)  # 清理编译产物


if __name__ == "__main__":
    sys.exit(main())
