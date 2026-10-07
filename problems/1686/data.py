#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1686《最小操作次数》分层测试数据生成器
# 用法：在 data/ 目录下执行  python3 ../data.py
# 产出 problem1.in/out ... problem10.in/out（10 组，覆盖题面全范围）
#
# 题面范围：1<=n,m<=50，1<=|s|<=10000，字符集 {A-Z, 0-9, '-', '*'}，
# 目标串 = s + '*'，保证合法方案一定存在。
#
# 通用构造（保证必有解）：
#   1) 先生成网格；
#   2) 在网格上从 (0,0) 出发随机模拟合法操作序列（选择当前字符 / 滑行到
#      第一个不同字符格），记录被选择的字符序列 rec；
#   3) 结束时反复随机滑行直到落在 '*' 格并选择它；
#   4) 令 s = rec 去掉末尾 '*'，则目标串 s+'*' 恰被该序列实现 => 必有解。
#
# 顶格大 |s| 采用"蛇形轨道 + 端点停靠点"结构：
#   - 一条蛇形单格宽通道贯穿网格，通道相邻格字符互不相同，
#     通道旁每个位置都紧贴一个 '*' 停靠点；
#   - 在通道上向前滑行、选择端点字符、滑回，可逐字符积攒任意长度的 rec；
#   - 随时可以一步滑到相邻的 '*' 结束 => 对 |s|=10000 必然快速收敛且必有解。

from cyaron import *
import random

DR = [-1, 1, 0, 0]
DC = [0, 0, -1, 1]

# ---------------- 基础工具 ----------------

def legal_dirs(g, n, m, r, c):
    res = []
    for d in range(4):
        nr, nc = r + DR[d], c + DC[d]
        while 0 <= nr < n and 0 <= nc < m and g[nr][nc] == g[r][c]:
            nr += DR[d]; nc += DC[d]
        if 0 <= nr < n and 0 <= nc < m:
            res.append(d)
    return res

def slide(g, n, m, r, c, d):
    nr, nc = r + DR[d], c + DC[d]
    while 0 <= nr < n and 0 <= nc < m and g[nr][nc] == g[r][c]:
        nr += DR[d]; nc += DC[d]
    return nr, nc

def gen_random_grid(n, m, alpha):
    return [[random.choice(alpha) for _ in range(m)] for _ in range(n)]

def walk_and_extract(g, n, m, sel_target, max_walk):
    """随机模拟：约做 sel_target 次选择 + 若干滑行，最后滑到 '*' 格并选它。
    返回 s（不含末尾 '*'），失败返回 None。"""
    r, c = 0, 0
    rec = []
    sels = 0
    while sels < sel_target:
        dirs = legal_dirs(g, n, m, r, c)
        if dirs and random.random() < 0.45:
            r, c = slide(g, n, m, r, c, random.choice(dirs))
        else:
            rec.append(g[r][c])
            sels += 1
    for _ in range(max_walk):
        if g[r][c] == '*':
            break
        dirs = legal_dirs(g, n, m, r, c)
        if not dirs:
            return None
        r, c = slide(g, n, m, r, c, random.choice(dirs))
    if g[r][c] != '*':
        return None
    rec.append('*')
    s = ''.join(rec[:-1])
    return s if len(s) >= 1 else None

def gen_case_walk(n, m, alpha, sel_target, seed, max_walk, retries=500):
    """通用入口：拒绝采样直到成功。返回 (grid, s)。"""
    st = random.getstate()
    random.seed(seed)
    try:
        for _ in range(retries):
            g = gen_random_grid(n, m, alpha)
            s = walk_and_extract(g, n, m, sel_target, max_walk)
            if s is not None:
                return g, s
        raise RuntimeError("gen_case_walk failed: n=%d m=%d" % (n, m))
    finally:
        random.setstate(st)

def snake_cells(n, m):
    """蛇形遍历全部格子的坐标序列，相邻坐标曼哈顿距离为 1。"""
    cells = []
    for i in range(n):
        cols = range(m) if i % 2 == 0 else range(m - 1, -1, -1)
        for j in cols:
            cells.append((i, j))
    return cells

def gen_snake_case(n, m, s_len, seed, track_letters='ABCDEFGHIJ', dock_char='*',
                   fill_alpha=None):
    """蛇形轨道构造（保证必有解、|s| 可精确到 s_len）。
    轨道 = 蛇形全部格子中去掉终点停靠点后的一条路径；
    轨道相邻格字符互不相同（取循环字母表），故沿轨道滑动一次直达首个不同字符格，
    即轨道的下一个/上一个轨道格（因为轨道每格字符都与相邻轨道格不同，
    且轨道外格子若同字符也不影响：滑动沿直线逐格比较）。
    为彻底避免轨道外同字符干扰，轨道外全部填充 '*'（停靠点无处不在，
    任何偏离轨道的滑行都会落在 '*' 上）。
    过程：从 (0,0)（轨道起点，字符为轨道字母）出发，沿蛇形轨道前进/后退滑行
    并选择字符积攒 rec，最后滑到轨道终点（固定为 '*'）结束。
    """
    st = random.getstate()
    random.seed(seed)
    try:
        cells = snake_cells(n, m)
        total = len(cells)
        assert total >= 2
        # 终点停靠点：蛇形最后一个格子
        end = cells[-1]
        g = [['*'] * m for _ in range(n)]
        # 轨道格赋循环字母（相邻不同即可，2 个字母就够，但用 10 个更随机）
        L = len(track_letters)
        for idx, (r, c) in enumerate(cells[:-1]):
            g[r][c] = track_letters[idx % L]
        g[end[0]][end[1]] = '*'
        # 模拟：沿轨道前后走，k 记录当前轨道下标（cells 中的索引）
        rec = []
        k = 0
        r, c = cells[0]
        # 需要至少前进一次（若 (0,0) 就是终点旁则无轨道，但 n*m>=2 保证有）
        # 策略：前进到轨道末尾前一个，然后 [选择, 后退一格, 选择, 前进一格] 循环。
        # 滑行：从轨道格 k 向轨道格 k+1 方向滑——由于 g[k+1] != g[k]，一次滑到 k+1。
        def dir_to(a, b):
            ar, ac = a; br, bc = b
            if br == ar - 1: return 0
            if br == ar + 1: return 1
            if bc == ac - 1: return 2
            return 3
        # 先走到轨道倒数第二格（cells[-2]）
        last_track = total - 2
        while k < last_track:
            d = dir_to(cells[k], cells[k + 1])
            r, c = slide(g, n, m, r, c, d)
            assert (r, c) == cells[k + 1], "snake slide off track"
            k += 1
        # 循环积攒：在 cells[last_track] 与 cells[last_track-1] 之间往返
        while len(rec) < s_len:
            rec.append(g[r][c])
            if len(rec) >= s_len:
                break
            nk = last_track - 1 if k == last_track else last_track
            d = dir_to(cells[k], cells[nk])
            r, c = slide(g, n, m, r, c, d)
            assert (r, c) == cells[nk]
            k = nk
        # 结束：滑到终点 '*'（cells[-1]，与 cells[-2] 相邻）
        if k != last_track:
            d = dir_to(cells[k], cells[last_track])
            r, c = slide(g, n, m, r, c, d)
            k = last_track
        d = dir_to(cells[last_track], cells[total - 1])
        r, c = slide(g, n, m, r, c, d)
        assert (r, c) == end and g[r][c] == '*'
        rec.append('*')
        s = ''.join(rec[:-1])
        assert len(s) == s_len
        return g, s
    finally:
        random.setstate(st)

# ---------------- 数据写出 ----------------

def emit(io, g, s):
    n, m = len(g), len(g[0])
    io.input_writeln(n, m)
    for row in g:
        io.input_writeln(''.join(row))
    io.input_writeln(s)

ALPHA_FULL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-*'

# ---- 点1【边界层】：1x2 最小边界，|s|=1。
#    唯一操作路径：选 'A'、右滑到 '*'、选 '*'，答案=2。----
g1 = [['A', '*']]
io = IO(file_prefix="problem", data_id=1)
emit(io, g1, 'A')
io.output_gen("../std")

# ---- 点2【边界层】：2x2，起点即 '*' 且 s='*'（s 唯一字符与起点相同）。
#    设计意图：考验"选择当前字符"在起点即可匹配、以及必须再找一个 '*' 收尾。----
g2 = [['*', 'A'], ['B', '*']]
io = IO(file_prefix="problem", data_id=2)
emit(io, g2, '*')
io.output_gen("../std")

# ---- 点3【小规模随机】：8x8，4 字符小字母表（大片同字符区考验滑行），|s|=10，可手算 ----
g3, s3 = gen_case_walk(8, 8, 'AB-*', 10, seed=1003, max_walk=300)
io = IO(file_prefix="problem", data_id=3)
emit(io, g3, s3)
io.output_gen("../std")

# ---- 点4【小规模随机】：12x12 全字符集随机，|s|=15 ----
g4, s4 = gen_case_walk(12, 12, ALPHA_FULL, 15, seed=1004, max_walk=300)
io = IO(file_prefix="problem", data_id=4)
emit(io, g4, s4)
io.output_gen("../std")

# ---- 点5【中等规模随机】：25x25，12 字符，|s|=120 ----
g5, s5 = gen_case_walk(25, 25, 'ABCDEFGHIJ-*', 120, seed=1005, max_walk=1500)
io = IO(file_prefix="problem", data_id=5)
emit(io, g5, s5)
io.output_gen("../std")

# ---- 点6【中等规模随机】：35x35 全字符集，|s|=500 ----
g6, s6 = gen_case_walk(35, 35, ALPHA_FULL, 500, seed=1006, max_walk=5000)
io = IO(file_prefix="problem", data_id=6)
emit(io, g6, s6)
io.output_gen("../std")

# ---- 点7【大规模随机】：50x50，3 字符小字母表（滑行距离长、同字符大片），|s|=3000 ----
g7, s7 = gen_case_walk(50, 50, 'A-*', 3000, seed=1007, max_walk=50000)
io = IO(file_prefix="problem", data_id=7)
emit(io, g7, s7)
io.output_gen("../std")

# ---- 点8【大规模随机】：50x50 全字符集（转移分支多），|s|=5000 ----
g8, s8 = gen_case_walk(50, 50, ALPHA_FULL, 5000, seed=1008, max_walk=80000)
io = IO(file_prefix="problem", data_id=8)
emit(io, g8, s8)
io.output_gen("../std")

# ---- 点9【顶格层】：50x50 蛇形轨道构造，|s|=10000（题面上限）。
#    轨道+全 '*' 底：最坏结构之一（长目标串+每步滑行仅一格，卡 BFS 状态数）。----
g9, s9 = gen_snake_case(50, 50, 10000, seed=1009)
io = IO(file_prefix="problem", data_id=9)
emit(io, g9, s9)
io.output_gen("../std")

# ---- 点10【顶格层】：50x50 蛇形轨道（2 字母轨道，答案结构不同），|s|=10000 顶格 ----
g10, s10 = gen_snake_case(50, 50, 10000, seed=1010, track_letters='AZ')
io = IO(file_prefix="problem", data_id=10)
emit(io, g10, s10)
io.output_gen("../std")
