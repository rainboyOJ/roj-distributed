#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1788《爬山》分层数据生成器
# 范围（题面）：1≤n≤5e5，0≤x,y≤1e6，x 严格递增。
# 分层（10 组）：
#   p1 n=1 / p2 n=2 / p3 题面样例 / p4 共线递增链 / p5 共线递减链 /
#   p6 全等高（平局取右）/ p7 山峰形 n=200 / p8 锯齿 n=1000（多转向）/
#   p9 n=2e5 随机 / p10 顶格 n=5e5 尖峰+深谷对抗混合
import random, subprocess, os, sys
random.seed(1788)

def emit(name, pts):
    with open(f'data/{name}.in', 'w') as f:
        f.write(str(len(pts)) + '\n')
        f.write('\n'.join(f'{x} {y}' for x, y in pts) + '\n')
    print(name, 'n=', len(pts))

# 先确保 std 存在
if not os.path.exists('/tmp/std1788'):
    sys.exit('std 缺失')

emit('problem1', [(0, 5)])
emit('problem2', [(0, 3), (1, 7)])
emit('problem3', [(0, 10), (1, 5), (2, 0), (3, 6)])
emit('problem4', [(i, 2 * i + 1) for i in range(50)])                      # 共线递增
emit('problem5', [(i, 2 * (100 - i)) for i in range(100)])                 # 共线递减
emit('problem6', [(i, 7) for i in range(300)])                             # 全等高
# p7 山峰形
p7 = [(i, i if i <= 100 else 200 - i) for i in range(200)]
emit('problem7', p7)
# p8 锯齿：高低交替（尖峰/深谷）
p8 = [(i, 10**6 if i % 2 == 0 else 0) for i in range(1000)]
emit('problem8', p8)
# p9 随机 2e5
p9 = [(i, random.randint(0, 10**6)) for i in range(200000)]
emit('problem9', p9)
# p10 顶格 5e5：随机 + 局部尖峰/深谷交替块
p10 = []
for i in range(500000):
    block = i // 1000
    if block % 3 == 0:
        y = 10**6 if i % 2 == 0 else 0
    elif block % 3 == 1:
        y = i % 10**6
    else:
        y = random.randint(0, 10**6)
    p10.append((i, y))
emit('problem10', p10)

# 用 std 产 .out 并断言
for i in range(1, 11):
    with open(f'data/problem{i}.out', 'w') as f:
        subprocess.run(['/tmp/std1788'], stdin=open(f'data/problem{i}.in'), stdout=f, check=True)
    out = open(f'data/problem{i}.out').read().strip().split('\n')
    n_in = open(f'data/problem{i}.in').readline().strip()
    assert len(out) == int(n_in), f'problem{i} 行数不符'
    assert all(l.lstrip('-').isdigit() for l in out), f'problem{i} 非整数'
    assert all(int(l) >= 0 for l in out), f'problem{i} 负步数'
    print(f'problem{i}: .out OK ({len(out)} 行, 最大 {max(int(l) for l in out)})')
print('ALL 10 CASES OK')
