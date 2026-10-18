### 【题目描述】

给定一棵有 $N$ 个顶点的树，其中第 $i$ 条边连接顶点 $a_i$ 和 $b_i$。记 $x_i$ 为满足 $\mathrm{dist}(u, v) = i$ 的点对 $(u, v)$ 的数量。请对每个 $i = 1, 2, \cdots, N - 1$ 求出 $x_i$。

$\mathrm{dist}(u, v)$ 表示顶点 $u$ 与 $v$ 之间唯一路径上的边数。

### 【输入】

```
$N$
$a_0$ $b_0$
$a_1$ $b_1$
$\vdots$
$a_{N-2}$ $b_{N-2}$
```

### 【输出】

```
$x_1$ $x_2$ $\ldots$ $x_{N-1}$
```

### 【输入样例】

```
8
0 1
1 2
2 3
1 4
4 7
1 5
2 6
```

### 【输出样例】

```
7 10 9 2 0 0 0
```

### 【数据范围】

- $1 \leq N \leq 200000$
- $0 \leq a_i, b_i < N$
- $a_i \neq b_i$

### 【来源】

Library Checker（yosupo06） frequency_table_of_tree_distance
