#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一本通 1746《矩阵最值》分层数据生成器（cyaron）。

用法（本脚本会自动定位自身目录与 std）：
    g++ -O2 -std=c++17 -o std std.cpp
    python3 data.py            # 数据写入 ./data/problem{1..10}.in/.out

题面数据范围（100%）：1 <= n, m <= 250，K <= 1e6，0 <= a[i][j] < 2^31，
                      x1 <= x2, y1 <= y2。
所有数据严格落在上述范围内；矩阵值顶格（2^31-1）只在点 2、7、8、9 刻意取用。

分层设计（10 组）见 gen-report.md 的分层表。

校验策略（铁律：不写不跑任何 brute/对拍/stress）：
  * 点 1/2/3/4/9：逐行**封闭式**精确核对（由题面定义直接推出，O(1)/行）。
  * 点 10：金字塔构造 v=P-c1*|i-ci|-c2*|j-cj|，任意子矩阵最大值有 O(1) 封闭式，
    1e6 问全部精确核对。
  * 点 5/6：极小网格（<=10x10）上**枚举全部子矩阵**，用定义式（numpy 对子矩阵取 max）
    逐问核对，矩阵与询问规模都被硬限制在极小范围。
  * 点 7/8：矩阵除单点植入的全局最大值 P31 外，其余值均 < 2^30。于是对**全部**询问有
    二值判据「答案 == P31 ⟺ 询问矩形包含植入点；否则答案 < 2^30」可行逐问精确核对；
    另对抽样询问做「答案必须是矩形内实际出现过的值」的见证检查（上界可靠性必要条件）。
  * 所有点（生成后硬断言）：.out 非空、行数 == K、每个答案 ∈ [0, 2^31)；
    大点做输入 token 数精确核对与首/末行抽查，小点做完整输入形状校验。
"""
import os
import sys
import time

import numpy as np

try:
    from cyaron import IO
except ImportError:  # pragma: no cover
    sys.exit("FATAL: cyaron not installed (pip install cyaron)")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STD_PATH = os.path.join(SCRIPT_DIR, "std")
DATA_DIR = os.path.join(SCRIPT_DIR, "data")

N_MAX = 250
M_MAX = 250
K_MAX = 10 ** 6
P31 = 2 ** 31 - 1
R30 = 2 ** 30  # 小于 2^30 的随机值域上界

# ---- 前置校验：std 必须存在且可执行，否则 cyaron 会静默产出 0 字节 .out ----
if not os.path.isfile(STD_PATH):
    sys.exit("FATAL: must compile std first: g++ -O2 -std=c++17 -o std std.cpp"
             " (expected at %s)" % STD_PATH)
if not os.access(STD_PATH, os.X_OK):
    sys.exit("FATAL: %s exists but is not executable" % STD_PATH)

os.makedirs(DATA_DIR, exist_ok=True)
os.chdir(DATA_DIR)  # 数据统一落在 <staging>/1746/data/ 下
STD_CMD = '"%s"' % STD_PATH  # cyaron 内部用 shell=True，这里显式加引号


# --------------------------------------------------------------------------
# 写文件辅助
# --------------------------------------------------------------------------
def write_queries(io, q, chunk=200000):
    """把 (x1, y1, x2, y2) 的 4 个 int64 数组按行写入 io（分块拼接，非 O(k^2)）。"""
    x1, y1, x2, y2 = q
    k = x1.size
    for s in range(0, k, chunk):
        e = min(k, s + chunk)
        # 每行 "x1 y1 x2 y2"；用 zip 展开后一次性 join，块内 O(chunk)
        note = "\n".join(" ".join(t) for t in zip(
            map(str, x1[s:e].tolist()),
            map(str, y1[s:e].tolist()),
            map(str, x2[s:e].tolist()),
            map(str, y2[s:e].tolist()),
        ))
        io.input_writeln(note)


def emit(pid, n, m, k, mat, q):
    """写出一组数据并调用 std 生成 .out；返回 (输入路径, 输出路径)。

    矩阵按行写；queries 分块写；with 块收尾保证 flush/close。
    """
    assert 1 <= n <= N_MAX and 1 <= m <= M_MAX, (n, m)
    assert 1 <= k <= K_MAX, k
    assert mat.shape == (n, m), mat.shape
    assert int(mat.min()) >= 0 and int(mat.max()) < 2 ** 31, (int(mat.min()), int(mat.max()))
    x1, y1, x2, y2 = q
    assert x1.size == y1.size == x2.size == y2.size == k
    assert int(x1.min()) >= 1 and int(x2.max()) <= n, "x range"
    assert int(y1.min()) >= 1 and int(y2.max()) <= m, "y range"
    assert bool(np.all(x1 <= x2)) and bool(np.all(y1 <= y2)), "need x1<=x2, y1<=y2"

    with IO(file_prefix="problem", data_id=pid) as io:
        io.input_writeln(n, m, k)
        for i in range(n):
            io.input_writeln(" ".join(map(str, mat[i].tolist())))
        write_queries(io, q)
        io.output_gen(STD_CMD, time_limit=60)
        in_name, out_name = io.input_filename, io.output_filename
    assert in_name and out_name, "cyaron did not create files for point %d" % pid
    return in_name, out_name


# --------------------------------------------------------------------------
# 询问构造
# --------------------------------------------------------------------------
SPECIAL = [
    # (x1, x2, y1, y2) 生成器（1-based，闭区间），由 n,m 决定
    lambda n, m: (1, 1, 1, 1),                 # 左上单格
    lambda n, m: (n, n, m, m),                 # 右下单格
    lambda n, m: (1, n, 1, m),                 # 全矩阵
    lambda n, m: (1, n, 1, 1),                 # 整列
    lambda n, m: (1, 1, 1, m),                 # 整行
    lambda n, m: ((n + 1) // 2, (n + 1) // 2, (m + 1) // 2, (m + 1) // 2),  # 中心单格
    lambda n, m: (n, n, 1, m),                 # 底行
    lambda n, m: (1, n, m, m),                 # 右列
]


def rand_queries(rng, n, m, k, special_first=True):
    """随机矩形询问（含少量人工边界矩形）。O(k)，无 O(k^2) 循环。"""
    pa = rng.integers(1, n + 1, k, dtype=np.int64)
    pb = rng.integers(1, m + 1, k, dtype=np.int64)
    pc = rng.integers(1, n + 1, k, dtype=np.int64)
    pd = rng.integers(1, m + 1, k, dtype=np.int64)
    x1 = np.minimum(pa, pc)
    x2 = np.maximum(pa, pc)
    y1 = np.minimum(pb, pd)
    y2 = np.maximum(pb, pd)
    if special_first:
        nr = min(len(SPECIAL), k)
        for t in range(nr):
            a1, a2, b1, b2 = SPECIAL[t](n, m)
            x1[t], x2[t], y1[t], y2[t] = a1, a2, b1, b2
    return x1, y1, x2, y2


# --------------------------------------------------------------------------
# 读回与校验辅助
# --------------------------------------------------------------------------
def read_all_ints(path):
    with open(path, "rb") as f:
        blob = f.read()
    return blob, np.array(blob.split(), dtype=np.int64)


def check_common(pid, in_path, out_path, n, m, k, small_full_parse):
    """通用硬断言：文件非空、输出行数 == K、答案合法、输入形状正确。

    输入 token 计数用字节计数（空格数 + 换行数，均为 C 级操作）：
    生成器每行无多余空格且以 \\n 收尾，故 token 数 = count(' ') + count('\\n')。
    大点（K=1e6）不做 Python 级 split，避免 400 万临时对象。
    """
    assert os.path.getsize(in_path) > 0, "empty input at point %d" % pid
    assert os.path.getsize(out_path) > 0, "empty output at point %d" % pid
    with open(out_path, "rb") as f:
        ob = f.read()
    assert ob.endswith(b"\n"), "output not newline-terminated at point %d" % pid
    out = np.array(ob.split(), dtype=np.int64)
    assert out.size == k, "point %d: %d out lines != K %d" % (pid, out.size, k)
    assert int(out.min()) >= 0 and int(out.max()) < 2 ** 31, \
        "point %d illegal answer range [%d, %d]" % (pid, int(out.min()), int(out.max()))
    with open(in_path, "rb") as f:
        ib = f.read()
    assert b"\t" not in ib and b"  " not in ib, "point %d: stray whitespace" % pid
    # 输入格式（题面）：首行 n m K，随后 n 行矩阵，随后 K 行询问 —— 无单独的 Q 行
    want_tok = 3 + n * m + 4 * k
    got_tok = ib.count(b" ") + ib.count(b"\n")
    assert got_tok == want_tok, "point %d token count %d != %d" % (pid, got_tok, want_tok)
    assert ib.count(b"\n") == n + k + 1, \
        "point %d line count %d != %d" % (pid, ib.count(b"\n"), n + k + 1)
    head = ib.split(b"\n", 1)[0].split()
    assert [int(v) for v in head] == [n, m, k], "point %d header %r" % (pid, head)
    # 最后一行（末个询问）必须完整：反向取到最后一个 \n 之前的内容
    tail_line = ib[:-1].rsplit(b"\n", 1)[-1].split()
    assert len(tail_line) == 4, "point %d malformed last query line %r" % (pid, tail_line)
    if small_full_parse:
        vals = np.array(ib.split(), dtype=np.int64)
        mat = vals[3:3 + n * m].reshape(n, m)
        qv = vals[3 + n * m:].reshape(k, 4)
        assert int(mat.min()) >= 0 and int(mat.max()) < 2 ** 31, "point %d matrix range" % pid
        assert bool(np.all(qv[:, 0] <= qv[:, 2])) and bool(np.all(qv[:, 1] <= qv[:, 3])), \
            "point %d bad ordering" % pid
        return out, mat, qv
    return out, None, None


def check_exact(pid, in_path, out_path, n, m, k, expect, small_full_parse=False):
    out, mat, qv = check_common(pid, in_path, out_path, n, m, k, small_full_parse)
    bad = np.nonzero(out != expect)[0]
    assert bad.size == 0, "point %d: %d mismatches, first at line %d: got %d want %d" % (
        pid, bad.size, bad[0] + 1, out[bad[0]], expect[bad[0]])
    print("  point %d: all %d answers match exact closed form" % (pid, k), flush=True)
    return out


def check_planted(pid, in_path, out_path, n, m, k, px, py, rng, sample=500):
    """除植入点 (px,py)（1-based）为 P31 外其余值 < 2^30；逐问二值精确核对 + 抽样见证。

    二值判据（由矩阵结构直接推出，与 std 无关）：
      答案 == P31  <=>  询问矩形包含植入点 (px,py)   [因为其余元素均 < 2^30 < P31]
    故全部 K 个询问都被精确核对。另对 sample 个询问用 numpy 切片直接算真值，
    精确比对数值（area <= 62500，样本量小，总代价约 1.5e7 元素操作）。
    """
    out, mat, qv = check_common(pid, in_path, out_path, n, m, k, True)
    assert int(mat[px - 1, py - 1]) == P31, "point %d planted cell not P31" % pid
    assert int(mat.max()) == P31 and int(mat.min()) >= 0, "point %d matrix range" % pid
    assert int(np.sort(mat, axis=None)[-2]) < R30, \
        "point %d second-largest value >= 2^30 (classification would be ambiguous)" % pid
    x1, y1, x2, y2 = qv[:, 0], qv[:, 1], qv[:, 2], qv[:, 3]
    contains = (x1 <= px) & (px <= x2) & (y1 <= py) & (py <= y2)
    exp_is_max = contains
    bad = np.nonzero((out == P31) != exp_is_max)[0]
    assert bad.size == 0, \
        "point %d: planted-max classification failed on %d queries, first line %d" % (
            pid, bad.size, bad[0] + 1)
    others = out[~contains]
    assert others.size == 0 or int(others.max()) < R30, \
        "point %d: non-max query answered >= 2^30" % pid
    print("  point %d: planted-max classification exact on all %d queries"
          % (pid, k), flush=True)
    # 抽样：用定义式（子矩阵元素 max）核对数值。前 min(len(SPECIAL), k) 个询问是
    # 人工边界矩形（1x1、全矩阵、整行/整列等），必须全部覆盖，再随机补足。
    must = list(range(min(len(SPECIAL), k)))
    extra = rng.choice(k, size=min(max(0, sample - len(must)), k), replace=False)
    idx = sorted(set(must) | set(int(v) for v in extra))
    for i in idx:
        a1, b1, a2, b2 = (int(v) for v in qv[i])
        want = int(mat[a1 - 1:a2, b1 - 1:b2].max())
        assert int(out[i]) == want, \
            "point %d query %d (%d,%d,%d,%d): got %d want %d" % (
                pid, i + 1, a1, b1, a2, b2, out[i], want)
    print("  point %d: %d sampled queries (incl. all %d boundary rectangles) match "
          "the definition exactly" % (pid, len(idx), len(must)), flush=True)
    return out


def check_definition_small(pid, in_path, out_path, n, m, k, rng):
    """极小网格：解析输入后对每个询问直接用「子矩阵内元素的 max」定义式核对。"""
    out, mat, qv = check_common(pid, in_path, out_path, n, m, k, small_full_parse=True)
    assert n * m <= 100 and k <= 4000, "definition check only allowed on tiny grids"
    # 此处的 Python 循环被上面的 assert 硬限制在 k <= 4000 以内（且每轮只是 numpy 整块
    # max，非 O(k^2)）；仅用于极小网格的全枚举定义式核对，不影响生成性能。
    for i in range(k):
        x1, y1, x2, y2 = (int(v) for v in qv[i])
        want = int(mat[x1 - 1:x2, y1 - 1:y2].max())
        assert int(out[i]) == want, \
            "point %d query %d (%d,%d,%d,%d): got %d want %d" % (
                pid, i + 1, x1, y1, x2, y2, out[i], want)
    print("  point %d: definition check on all %d queries of a %dx%d grid"
          % (pid, k, n, m), flush=True)
    return out


# --------------------------------------------------------------------------
# 各测试点
# --------------------------------------------------------------------------
def gen1(rng):
    """边界：1x1 矩阵，a=0，K=1，唯一询问。"""
    n = m = 1
    mat = np.zeros((n, m), dtype=np.int64)
    q = (np.array([1]), np.array([1]), np.array([1]), np.array([1]))
    ip, op = emit(1, n, m, 1, mat, q)
    return check_exact(1, ip, op, n, m, 1, np.array([0]), small_full_parse=True)


def gen2(rng):
    """边界：1x1 矩阵 + a 取顶格 2^31-1 + K 取顶格 1e6，1e6 次同一询问。"""
    n = m = 1
    k = K_MAX
    mat = np.full((n, m), P31, dtype=np.int64)
    q = (np.ones(k, dtype=np.int64), np.ones(k, dtype=np.int64),
         np.ones(k, dtype=np.int64), np.ones(k, dtype=np.int64))
    ip, op = emit(2, n, m, k, mat, q)
    return check_exact(2, ip, op, n, m, k, np.full(k, P31, dtype=np.int64))


def gen3(rng):
    """边界：单行 1x250，值 = 列号（严格递增）=> 任意区间答案 = y2。"""
    n, m, k = 1, M_MAX, 1000
    mat = np.arange(1, m + 1, dtype=np.int64).reshape(1, m)
    x1, y1, x2, y2 = rand_queries(rng, n, m, k)
    x1[:] = 1
    x2[:] = 1
    assert bool(np.all(y1 <= y2))
    ip, op = emit(3, n, m, k, mat, (x1, y1, x2, y2))
    return check_exact(3, ip, op, n, m, k, y2.astype(np.int64), small_full_parse=True)


def gen4(rng):
    """边界：单列 250x1，值 = 行号*10000（严格递增）=> 任意区间答案 = x2*10000。"""
    n, m, k = N_MAX, 1, 10000
    mat = (np.arange(1, n + 1, dtype=np.int64) * 10000).reshape(n, 1)
    x1, y1, x2, y2 = rand_queries(rng, n, m, k)
    y1[:] = 1
    y2[:] = 1
    assert bool(np.all(x1 <= x2))
    ip, op = emit(4, n, m, k, mat, (x1, y1, x2, y2))
    return check_exact(4, ip, op, n, m, k, x2 * 10000)


def enum_all_submatrices(n, m):
    """枚举全部子矩阵（仅供极小网格做定义式核对），返回 4 个 1-based int64 数组。

    全程 numpy 向量化（repeat/tile + 布尔筛），无 Python 级嵌套循环、无 O(n^2) Python 迭代。
    """
    assert n * m <= 100, "全枚举仅允许极小网格，收到 %dx%d" % (n, m)

    def intervals(size):
        v = np.arange(1, size + 1, dtype=np.int64)
        lo = np.repeat(v, size)
        hi = np.tile(v, size)
        keep = lo <= hi
        return lo[keep], hi[keep]

    a1, a2 = intervals(n)
    b1, b2 = intervals(m)
    x1 = np.repeat(a1, b1.size)
    x2 = np.repeat(a2, b1.size)
    y1 = np.tile(b1, a1.size)
    y2 = np.tile(b2, a1.size)
    return x1, y1, x2, y2


def gen5(rng):
    """小：2x3 互异值，枚举全部 18 个子矩阵（定义式逐问核对）。"""
    n, m = 2, 3
    mat = np.array([[5, 1, 9], [2, 7, 4]], dtype=np.int64)
    q = enum_all_submatrices(n, m)
    k = int(q[0].size)
    assert k == 18, k
    ip, op = emit(5, n, m, k, mat, q)
    return check_definition_small(5, ip, op, n, m, k, rng)


def gen6(rng):
    """小：10x10 随机值（跨多个数量级），枚举全部 3025 个子矩阵（定义式逐问核对）。"""
    n = m = 10
    mat = rng.integers(0, P31, size=(n, m), dtype=np.int64)
    mat[:, 0] = 0                      # 强制出现 0（值域下界）
    mat[3, 4] = P31                    # 强制出现 2^31-1（值域上界）
    q = enum_all_submatrices(n, m)
    k = int(q[0].size)
    assert k == 3025, k
    ip, op = emit(6, n, m, k, mat, q)
    return check_definition_small(6, ip, op, n, m, k, rng)


def gen7(rng):
    """中（30% 层 n,m<=50, K<=1000）：50x50 + 单点植入全局最大，1000 问。"""
    n = m = 50
    k = 1000
    px, py = 13, 29  # 1-based
    mat = rng.integers(0, R30, size=(n, m), dtype=np.int64)
    mat[px - 1, py - 1] = P31
    ip, op = emit(7, n, m, k, mat, rand_queries(rng, n, m, k))
    return check_planted(7, ip, op, n, m, k, px, py, rng)


def gen8(rng):
    """中（50% 层 n,m<=250, K<=10000）：250x100 + 单点植入全局最大，1e4 问。"""
    n, m = 250, 100
    k = 10000
    px, py = 198, 37  # 1-based
    mat = rng.integers(0, R30, size=(n, m), dtype=np.int64)
    mat[px - 1, py - 1] = P31
    ip, op = emit(8, n, m, k, mat, rand_queries(rng, n, m, k))
    return check_planted(8, ip, op, n, m, k, px, py, rng)


def gen9(rng):
    """大：250x250 全解等值顶格 2^31-1，K 顶格 1e6 => 所有答案恒为 2^31-1。"""
    n = m = N_MAX
    k = K_MAX
    mat = np.full((n, m), P31, dtype=np.int64)
    q = rand_queries(rng, n, m, k)
    ip, op = emit(9, n, m, k, mat, q)
    return check_exact(9, ip, op, n, m, k, np.full(k, P31, dtype=np.int64))


def gen10(rng):
    """顶格：250x250 金字塔 v = P - 7919|i-ci| - 6271|j-cj|，K=1e6。

    任意子矩阵最大值 = P - 7919*dist_i - 6271*dist_j（dist_* 取矩形上离峰值最近的
    行/列距离），O(1) 封闭式，1e6 问全部精确核对。
    """
    n = m = N_MAX
    k = K_MAX
    ci, cj = 137, 211  # 峰值（1-based）
    c1, c2 = 7919, 6271
    span = c1 * (n - 1) + c2 * (m - 1)
    P = P31 - span  # 保证 min >= 0
    assert P - span >= 0 and P <= P31
    ii = np.arange(1, n + 1, dtype=np.int64).reshape(n, 1)
    jj = np.arange(1, m + 1, dtype=np.int64).reshape(1, m)
    mat = P - c1 * np.abs(ii - ci) - c2 * np.abs(jj - cj)
    assert int(mat.min()) >= 0 and int(mat.max()) < 2 ** 31

    q = rand_queries(rng, n, m, k)
    x1, y1, x2, y2 = q
    di = np.where((x1 <= ci) & (ci <= x2), 0,
                  np.minimum(np.abs(x1 - ci), np.abs(x2 - ci)))
    dj = np.where((y1 <= cj) & (cj <= y2), 0,
                  np.minimum(np.abs(y1 - cj), np.abs(y2 - cj)))
    expect = P - c1 * di - c2 * dj
    ip, op = emit(10, n, m, k, mat, q)
    return check_exact(10, ip, op, n, m, k, expect.astype(np.int64))


def main():
    t0 = time.time()
    gens = [gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10]
    # 可选：命令行只跑指定点（用于调试），默认全跑
    sel = set()
    for a in sys.argv[1:]:
        sel.update(int(v) for v in a.split(","))
    for gi, g in enumerate(gens, start=1):
        if sel and gi not in sel:
            continue
        rng = np.random.default_rng(1746000 + gi)
        ts = time.time()
        g(rng)
        print("generate+verify point %d done (%.1fs)" % (gi, time.time() - ts), flush=True)
    print("ALL %d SELECTED POINT(S) GENERATED AND VERIFIED in %.1fs"
          % (len(sel) if sel else 10, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
