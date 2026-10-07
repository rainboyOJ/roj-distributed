#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1818《树上取石子》分层数据生成器（10 组）
#
# 题面要点（见 content.md）：
#   给定一棵有向树（n 个结点，每点有石子数 num[i]，给出 n-1 条 "u v" 表示 u 是 v 的父亲），
#   Alice 先取根，之后两人交替，**后手**从刚被取走结点的儿子里选一个继续，走到叶子结束。
#   Alice 偏好：先让 Bob 尽可能少，再让自己尽可能多；Bob 偏好：先让自己尽可能多，再让 Alice 尽可能少。
#   输出一行两个整数（Alice 得石、Bob 得石）。1<=n<=1e5，1<=num[i]<=1e4，答案在 [0,2^31)。
#
# 分层设计（10 个测试点）：
#   点 1  边界：n=1（最小规模，根即叶子）num=1                    -> 1 0
#   点 2  边界：n=2（最小非平凡）num 顶格 10000                    -> 10000 10000
#   点 3  边界：n=3 星形，根 1 + 两个叶子 10000（Bob 一选取平，
#              考察第二关键字：Bob 取平后 Alice 都为 0）           -> 1 10000
#   点 4  边界：n=3 链 1-2-3，num=1,2,3（考察深度奇偶）            -> 4 2
#   点 5  小  ：n=10 链，num=1..10（手算：Alice 取 1,3,5,7,9）      -> 25 30
#   点 6  中  ：n=1000 随机树（父 < 子），num 1..1e4
#   点 7  大  ：n=20000 随机树，num 1..1e4
#   点 8  顶格：n=100000 星形（根 1 挂 99999 个叶子，最大度数）     -> num[1] 与 max(num[2..])
#   点 9  顶格：n=100000 链（最大深度，显式栈防爆栈），num 全 = 1e4
#              （路径和 1e9，顶到 2^31 边界）                      -> 500000000 500000000
#   点 10 顶格：n=100000 完全二叉树，num 随机 ∈{1,2}（大量取平，
#              考察第二关键字在满树上的传播）
#
# 说明：本题不存在无解情形（每条根到叶路径都有解），故所有点输出都必须非空。
# 生成 .out 的方式：用 subprocess 显式运行 std（不使用 cyaron 的 output_gen，避免写缓冲
# 未 flush 导致 0 字节 .out），并在每组写完后断言 .out 非空、恰好 1 行、恰好 2 个非负整数。
# 手算点（1-5、8、9）额外断言与预期输出逐字节一致；题面样例同样单独跑一遍断言 7 16。
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
TIME_LIMIT = 1.0  # 题面 1000 ms


# ---------------------------------------------------------------- std 定位
def find_std():
    """优先用已编译好的 std 二进制，找不到就把 std.cpp 编到临时目录。"""
    for cand in (os.path.join(HERE, "std"), os.path.join(HERE, "work", "std"),
                 os.path.join(HERE, os.pardir, "std")):
        if os.path.isfile(cand) and os.access(cand, os.X_OK):
            return cand, None
    tmpdir = tempfile.mkdtemp(prefix="std_1818_")
    out = os.path.join(tmpdir, "std")
    subprocess.run(["g++", "-O2", "-std=c++17", "-o", out, os.path.join(HERE, "std.cpp")],
                   check=True)
    return out, tmpdir


# ---------------------------------------------------------------- 造图
def rand_tree(n, rng):
    """随机递归树：v 的父亲在 [1, v-1] 中均匀取（O(n)）。"""
    edges = [(rng.randint(1, v - 1), v) for v in range(2, n + 1)]
    return edges


def chain(n):
    return [(i, i + 1) for i in range(1, n)]


def star(n):
    return [(1, v) for v in range(2, n + 1)]


def complete_binary(n):
    return [(v // 2, v) for v in range(2, n + 1)]


# ---------------------------------------------------------------- 跑 std
def run_std(std_bin, in_path, out_path):
    with open(in_path, "r") as fin, open(out_path, "w") as fout:
        t0 = time.perf_counter()
        proc = subprocess.run([std_bin], stdin=fin, stdout=fout, timeout=60)
        dt = time.perf_counter() - t0
    if proc.returncode != 0:
        raise RuntimeError("%s: std 退出码 %d" % (in_path, proc.returncode))
    with open(out_path, "r") as f:
        raw = f.read()
    if raw.strip() == "":
        raise RuntimeError("%s -> %s: 输出为空（.out 0 字节或全空白）" % (in_path, out_path))
    lines = raw.rstrip("\n").split("\n")
    if len(lines) != 1:
        raise RuntimeError("%s: 期望恰好 1 行输出，实际 %d 行" % (out_path, len(lines)))
    toks = lines[0].split()
    if len(toks) != 2 or not all(t.lstrip("-").isdigit() for t in toks):
        raise RuntimeError("%s: 输出不是两个整数: %r" % (out_path, lines[0]))
    a, b = int(toks[0]), int(toks[1])
    if a < 0 or b < 0:
        raise RuntimeError("%s: 出现负数答案 %d %d" % (out_path, a, b))
    return (a, b), dt


def write_case(idx, n, nums, edges):
    """写 data/problem{idx}.in，并断言结构自洽。"""
    assert len(nums) == n, (idx, len(nums), n)
    assert len(edges) == n - 1, (idx, len(edges), n)
    assert all(1 <= x <= 10000 for x in nums), idx
    for u, v in edges:
        assert 1 <= u < v <= n, (idx, u, v)  # 本题数据统一按拓扑序给边（父编号 < 子编号）
    in_path = os.path.join(DATA_DIR, "problem%d.in" % idx)
    with open(in_path, "w") as f:
        f.write("%d\n" % n)
        f.write(" ".join(map(str, nums)) + "\n")
        f.write("".join("%d %d\n" % (u, v) for u, v in edges))
    return in_path


def emit(std_bin, idx, n, nums, edges, note, expected=None):
    in_path = write_case(idx, n, nums, edges)
    out_path = os.path.join(DATA_DIR, "problem%d.out" % idx)
    (a, b), dt = run_std(std_bin, in_path, out_path)
    if expected is not None and (a, b) != expected:
        raise RuntimeError("点 %d 与手算预期不符: got %d %d, want %d %d" %
                           (idx, a, b, expected[0], expected[1]))
    if dt > TIME_LIMIT:
        raise RuntimeError("点 %d 运行 %.3fs 超过题面时限 1s" % (idx, dt))
    total = sum(nums)
    if a + b > total:
        raise RuntimeError("点 %d: 答案和 %d 超过石子总数 %d" % (idx, a + b, total))
    tag = " (手算校验通过)" if expected is not None else ""
    print("  problem%-2d n=%-6d %-28s -> %d %d  [%.3fs]%s" %
          (idx, n, note, a, b, dt, tag))
    return {"idx": idx, "n": n, "note": note, "a": a, "b": b, "dt": dt}


def hand_check(std_bin, name, text, expected):
    """用临时文件跑 std，校验手算/样例预期（不产生 data/ 产物）。"""
    tmp = tempfile.mkdtemp(prefix="chk_1818_")
    inp = os.path.join(tmp, "in.txt")
    outp = os.path.join(tmp, "out.txt")
    with open(inp, "w") as f:
        f.write(text)
    got, dt = run_std(std_bin, inp, outp)
    if got != expected:
        raise RuntimeError("手算校验 %s 失败: got %s, want %s" % (name, got, expected))
    print("  [ok] %-26s -> %d %d  [%.3fs]" % (name, got[0], got[1], dt))
    return got


def main():
    import random
    os.makedirs(DATA_DIR, exist_ok=True)
    std_bin, tmpdir = find_std()
    print("std: %s" % std_bin)
    rows = []

    # ---- 0. 题面样例（content.md 的输入/输出样例）----
    print("题面样例与手算校验:")
    hand_check(std_bin, "题面样例 n=6", "6\n4 16 16 5 3 1\n1 2\n2 4\n1 3\n3 5\n3 6\n", (7, 16))
    hand_check(std_bin, "n=1 单点", "1\n1\n", (1, 0))
    hand_check(std_bin, "n=2 两结点", "2\n10000 10000\n1 2\n", (10000, 10000))
    hand_check(std_bin, "n=3 星形取平", "3\n1 10000 10000\n1 2\n1 3\n", (1, 10000))
    hand_check(std_bin, "n=3 链深度奇偶", "3\n1 2 3\n1 2\n2 3\n", (4, 2))
    hand_check(std_bin, "n=10 链手算", "10\n1 2 3 4 5 6 7 8 9 10\n" +
               "".join("%d %d\n" % (i, i + 1) for i in range(1, 10)), (25, 30))
    hand_check(std_bin, "n=4 单边深链", "4\n5 5 5 5\n1 2\n2 3\n3 4\n", (10, 10))
    # 1->2->3 与 1->4->5 两条链：solve(2)=(3,2), solve(4)=(5,4)（Bob 取链头，Alice 取链尾）。
    # 根处 Bob 在 2/4 间选：B(2)=2 < B(4)=4，取 4 -> Alice = 1 + A(4) = 6, Bob = B(4) = 4。
    hand_check(std_bin, "n=5 根挂双链", "5\n1 2 3 4 5\n1 2\n2 3\n1 4\n4 5\n", (6, 4))
    print("生成 10 组测试数据:")

    # ---- 1. 边界：n=1 ----
    rows.append(emit(std_bin, 1, 1, [1], [], "边界 n=1 单点", (1, 0)))

    # ---- 2. 边界：n=2，num 顶格 ----
    rows.append(emit(std_bin, 2, 2, [10000, 10000], [(1, 2)], "边界 n=2 值顶格", (10000, 10000)))

    # ---- 3. 边界：n=3 星形，Bob 一选取平 ----
    rows.append(emit(std_bin, 3, 3, [1, 10000, 10000], star(3), "边界 n=3 星形取平", (1, 10000)))

    # ---- 4. 边界：n=3 链 ----
    rows.append(emit(std_bin, 4, 3, [1, 2, 3], chain(3), "边界 n=3 链", (4, 2)))

    # ---- 5. 小：n=10 链 ----
    rows.append(emit(std_bin, 5, 10, list(range(1, 11)), chain(10), "小 n=10 链", (25, 30)))

    # ---- 6. 中：n=1000 随机树 ----
    rng = random.Random(1818)
    nums6 = [rng.randint(1, 10000) for _ in range(1000)]
    rows.append(emit(std_bin, 6, 1000, nums6, rand_tree(1000, rng), "中 n=1000 随机树"))

    # ---- 7. 大：n=20000 随机树 ----
    nums7 = [rng.randint(1, 10000) for _ in range(20000)]
    rows.append(emit(std_bin, 7, 20000, nums7, rand_tree(20000, rng), "大 n=20000 随机树"))

    # ---- 8. 顶格：n=100000 星形（最大度数）----
    n8 = 100000
    nums8 = [rng.randint(1, 10000) for _ in range(n8)]
    rows.append(emit(std_bin, 8, n8, nums8, star(n8), "顶格 n=1e5 星形",
                     (nums8[0], max(nums8[1:]))))

    # ---- 9. 顶格：n=100000 链，num 全 1e4（最大深度 + 最大和）----
    n9 = 100000
    nums9 = [10000] * n9
    rows.append(emit(std_bin, 9, n9, nums9, chain(n9), "顶格 n=1e5 链 num=1e4",
                     (50000 * 10000, 50000 * 10000)))

    # ---- 10. 顶格：n=100000 完全二叉树，num ∈{1,2}（大量取平）----
    n10 = 100000
    nums10 = [rng.randint(1, 2) for _ in range(n10)]
    rows.append(emit(std_bin, 10, n10, nums10, complete_binary(n10), "顶格 n=1e5 完全二叉树 取平"))

    # ---- 汇总 ----
    print("\n汇总: %d 组, 最大运行时间 %.3fs (时限 %.1fs), 输出文件均非空且格式正确" %
          (len(rows), max(r["dt"] for r in rows), TIME_LIMIT))
    for r in rows:
        in_path = os.path.join(DATA_DIR, "problem%d.in" % r["idx"])
        out_path = os.path.join(DATA_DIR, "problem%d.out" % r["idx"])
        assert os.path.getsize(in_path) > 0 and os.path.getsize(out_path) > 0
        with open(out_path) as f:
            assert len(f.read().rstrip("\n").split("\n")) == 1
    if tmpdir:
        subprocess.run(["rm", "-rf", tmpdir])
    print("data/ 下 problem1..problem10 的 .in/.out 全部生成并通过断言")


if __name__ == "__main__":
    sys.exit(main())
