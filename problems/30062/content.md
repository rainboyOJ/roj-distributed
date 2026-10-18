### 【题目描述】

给定一个长度为 $N$ 的整数序列 $(A_0, A_1, \ldots, A_{N-1})$。依次处理以下 $Q$ 个查询。

- `$l_i$ $r_i$`：输出 $(A_{l_i}, A_{l_i+1}, \ldots, A_{r_i-1})$ 中的逆序对个数。

序列 $(B_0, B_1, \ldots, B_{M-1})$ 中的一个逆序对是指满足
$0 \leq i < j \lt M$ 且 $B_i \gt B_j$ 的下标对 $(i, j)$。

### 【输入】

```
$N$ $Q$
$A_0$ $A_1$ $\ldots$ $A_{N-1}$
$l_0$ $r_0$
$l_1$ $r_1$
$\vdots$
$l_{Q-1}$ $r_{Q-1}$
```

### 【输出】

输出 $Q$ 行，第 $i$ 行为第 $i$ 个查询的答案，即 $(A_{l_i}, A_{l_i+1}, \ldots, A_{r_i-1})$ 中的逆序对个数。

### 【输入样例】

```
4 2
4 1 4 0
1 3
0 4
```

### 【输出样例】

```
0
4
```

### 【数据范围】

- $1 \leq N \leq 100000$
- $1 \leq Q \leq 100000$
- $0 \leq A_i \leq 1000000000$
- $0 \leq l_i \lt r_i \leq N$

### 【来源】

Library Checker（yosupo06） static_range_inversions_query
