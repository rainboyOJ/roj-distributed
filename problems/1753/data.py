#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 一本通 1753《区间连通性》数据生成器
# -----------------------------------------------------------------------------
# 题面范围：1 <= n <= 1e5；区间端点在 32 位有符号整数范围内；操作 1 加入的区间长度
#           严格大于此前所有区间。限制 1000ms / 256MB。
#
# 分层设计（10 组，从边界/小/中/大铺到顶格）：
#   1  样例层  ：题面【输入样例】原样（n=5，2 次询问，答案 NO/YES）
#   2  边界层  ：极小规模 + 端点相切结构（相切不算连通，用于检验严格不等号）
#   3  小随机  ：n=200，宽范围均匀放置（多为不相交，答案偏 NO）
#   4  小簇    ：n=1000，聚集放置（大量正长度相交，答案偏 YES）
#   5  中随机  ：n=5000，混合放置
#   6  中嵌套  ：n=10000，逐层包含（深嵌套，检验连通块线段合并）
#   7  大随机  ：n=100000，宽范围均匀放置（端点分散，集合规模大）
#   8  大簇    ：n=100000，聚集放置（反复合并同一连通块）
#   9  顶格嵌套：n=100000，逐层包含（最深嵌套 + 顶格 n）
#  10  顶格相切：n=100000，大量端点相切 + 混合（检验边界正确性 + 顶格 n）
#
# 生成约定：
#   * 严格保证每次操作 1 的新区间长度 > 此前所有区间长度（cur_len 单调递增）。
#   * 端点全程限制在 [-(2^31), 2^31-1] 内（用 long long 计算，std 亦用 long long）。
#   * 每个测试点至少含 1 次询问，故 .out 非空；断言 .out 行数 == 询问次数。
#   * 只用 O(n) 的 Python 循环，不做任何 O(n^2) 操作。
#
# 输出生成：**显式**用 subprocess 运行 std 生成 .out（不依赖 cyaron 写缓冲），
#           避免 0 字节 .out 的隐患。
import os
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "std")
DATA = os.path.join(HERE, "data")

LO = -(2 ** 31)          # 32 位有符号下界
HI = 2 ** 31 - 1         # 32 位有符号上界
MAXLEN = HI - LO         # 可能的最大长度


def place(rnd, mode, new_len, intervals, state):
    """按 mode 为长度 new_len 的新区间挑选左端点 x，返回 x。"""
    if mode == "wide":
        return rnd.randint(LO + 1, HI - new_len)
    if mode == "cluster":
        base = state["base"]
        return base + rnd.randint(-500, 500)
    if mode == "nested":
        if not intervals:
            return rnd.randint(-1000, 0)
        min_x = state["min_x"]
        max_y = state["max_y"]
        span = max_y - min_x
        room = new_len - span - 1        # 需 d <= room 才能保证 y > max_y
        if room < 0:
            room = 0
        d = rnd.randint(0, min(room, 1000))
        return min_x - d
    if mode == "inside":
        if not intervals:
            return rnd.randint(LO + 1, HI - new_len)
        k = rnd.randrange(len(intervals))
        ex, ey = intervals[k]
        exlen = ey - ex
        room = new_len - exlen - 1
        if room < 0:
            room = 0
        a = rnd.randint(0, min(room, 1000))
        return ex - a
    if mode == "touch":
        if not intervals:
            return rnd.randint(LO + 1, HI - new_len)
        k = rnd.randrange(len(intervals))
        if rnd.random() < 0.5:
            x = intervals[k][1]                       # 新区间左端 = 某区间右端（相切）
            if x + new_len <= HI:
                return x
        x = intervals[k][0] - new_len                 # 新区间右端 = 某区间左端（相切）
        if x >= LO + 1:
            return x
        return rnd.randint(LO + 1, HI - new_len)
    raise ValueError(mode)


def gen_ops(n, seed, mode):
    """生成 n 个操作；返回 (ops, query_count)。"""
    rnd = random.Random(seed)
    intervals = []           # 按加入顺序保存 (x, y)
    state = {"base": rnd.randint(-100000, 100000), "min_x": 0, "max_y": 0}
    step = max(1, 2000000000 // max(1, n))     # 长度增量上界，保证总长 < 2^31
    cur_len = 0
    ops = []
    nq = 0
    for _ in range(n):
        # 至少先攒够 2 个区间才可询问（a != b）
        do_add = (len(intervals) < 2) or (rnd.random() < 0.5)
        if do_add:
            new_len = cur_len + rnd.randint(1, step)
            if new_len > MAXLEN - 10:
                new_len = MAXLEN - 10
            if new_len <= cur_len:
                new_len = cur_len + 1
            cur_len = new_len
            x = place(rnd, mode, new_len, intervals, state)
            y = x + new_len
            # 夹紧到合法范围（正常情况下不会触发）
            if x < LO:
                x = LO
                y = x + new_len
            if y > HI:
                y = HI
                x = y - new_len
            ops.append((1, x, y))
            intervals.append((x, y))
            if not intervals or len(intervals) == 1:
                state["min_x"] = x
                state["max_y"] = y
            else:
                state["min_x"] = min(state["min_x"], x)
                state["max_y"] = max(state["max_y"], y)
        else:
            a = rnd.randrange(len(intervals))
            b = rnd.randrange(len(intervals))
            while b == a:
                b = rnd.randrange(len(intervals))
            ops.append((2, a + 1, b + 1))
            nq += 1
    # 兜底：若一次询问都没有，把最后一个操作改成询问
    if nq == 0 and len(intervals) >= 2:
        ops[-1] = (2, 1, 2)
        nq = 1
    return ops, nq


def write_case(idx, ops, nq):
    inpath = os.path.join(DATA, "problem%d.in" % idx)
    outpath = os.path.join(DATA, "problem%d.out" % idx)
    with open(inpath, "w") as f:
        f.write("%d\n" % len(ops))
        f.write("\n".join("%d %d %d" % o for o in ops))
        f.write("\n")
    with open(inpath, "rb") as fin:
        res = subprocess.run([STD], stdin=fin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert res.returncode == 0, "test %d: std returncode %d: %s" % (idx, res.returncode, res.stderr[:200])
    toks = res.stdout.split()
    assert len(toks) == nq, "test %d: expect %d query outputs, got %d" % (idx, nq, len(toks))
    assert nq >= 1 and len(toks) >= 1, "test %d: empty output" % idx
    with open(outpath, "wb") as f:
        f.write(res.stdout)
    yes = sum(1 for t in toks if t == b"YES")
    return inpath, outpath, len(toks), yes


def main():
    os.makedirs(DATA, exist_ok=True)
    assert os.path.exists(STD), "std binary not found: %s" % STD

    # 手工小数据（点 1 样例、点 2 边界相切），便于逐字节人工核对
    manual = {
        1: ([(1, 1, 5), (1, 5, 11), (2, 1, 2), (1, 2, 9), (2, 1, 2)], 2),
        # 2 边界：端点相切（不连通）与「相差一点即连通」对照
        #   区间1=(0,5) 区间2=(5,12) 仅端点相切 -> NO（长度 5<7 严格递增）
        #   区间3=(-10,3) 与区间1 正长度相交 -> 2,3 不连通 -> NO；1,3 连通 -> YES
        #   区间4=(3,20) 与区间3 相切、与区间1/2 相交 -> 全体连通 -> YES
        2: ([(1, 0, 5), (1, 5, 12), (2, 1, 2),
             (1, -10, 3), (2, 2, 3), (2, 1, 3),
             (1, 3, 20), (2, 1, 2)], 4),
    }
    spec = {
        3: (200, "wide", 175303),
        4: (1000, "cluster", 175304),
        5: (5000, "wide", 175305),
        6: (10000, "nested", 175306),
        7: (100000, "wide", 175307),
        8: (100000, "cluster", 175308),
        9: (100000, "nested", 175309),
        10: (100000, "touch", 175310),
    }
    results = []
    for idx in range(1, 11):
        if idx in manual:
            ops, nq = manual[idx]
        else:
            n, mode, seed = spec[idx]
            ops, nq = gen_ops(n, seed, mode)
        info = write_case(idx, ops, nq)
        results.append((idx, len(ops), nq, info[2], info[3]))
        print("test %2d: n=%-6d queries=%-6d out_lines=%-6d YES=%d" %
              (idx, len(ops), nq, info[2], info[3]))

    # 样例点额外校验
    with open(os.path.join(DATA, "problem1.out")) as f:
        got = f.read().split()
    assert got == ["NO", "YES"], "sample mismatch: %r" % got
    print("sample check: NO / YES  OK")
    # 边界点额外校验（人工推导）
    with open(os.path.join(DATA, "problem2.out")) as f:
        got2 = f.read().split()
    assert got2 == ["NO", "NO", "YES", "YES"], "boundary mismatch: %r" % got2
    print("boundary check: NO / NO / YES / YES  OK")


if __name__ == "__main__":
    main()
