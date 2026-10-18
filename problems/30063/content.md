### 【题目描述】

给定一个由 $\lbrace 0, 1, \dots, N-1 \rbrace$ 构成的排列 $P$。
请按顺序处理以下 $Q$ 个查询：

- `$l$ $r$`：输出 $(P_l, P_{l+1}, \dots, P_{r-1})$ 的最长上升子序列的长度。

### 【输入】

```
$N$ $Q$
$P_0$ $P_1$ $\cdots$ $P_{N-1}$
$l_0$ $r_0$
$l_1$ $r_1$
$\vdots$
$l_{Q-1}$ $r_{Q-1}$
```

### 【输出】

对于每个查询，输出一个整数，表示对应子序列的最长上升子序列长度。

### 【输入样例】

```
4 3
0 2 1 3
0 2
0 4
1 3
```

### 【输出样例】

```
2
3
1
```

### 【数据范围】

- $1 \leq N \leq 100000$
- $1 \leq Q \leq 100000$
- $P$ 是由 $\lbrace 0, 1, \dots, N-1 \rbrace$ 构成的排列
- $0 \leq l_i \leq r_i \leq N$

### 【来源】

Library Checker（yosupo06） static_range_lis_query
