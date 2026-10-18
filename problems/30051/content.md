### 【题目描述】

给定一个长度为 $N$ 的整数序列 $a_0, a_1, \dots, a _ {N - 1}$。请按顺序处理以下 $Q$ 个查询：

- `0 $l$ $r$ $b$`：对于每个 $i = l, \dots, {r-1}$，令 $a_i \gets \min(a_i, b)$。
- `1 $l$ $r$ $b$`：对于每个 $i = l, \dots, {r-1}$，令 $a_i \gets \max(a_i, b)$。
- `2 $l$ $r$ $b$`：对于每个 $i = l, \dots, {r-1}$，令 $a_i \gets a_i + b$。
- `3 $l$ $r$`：输出 $\sum _ {i = l} ^ {r-1} a_i$。

### 【输入】

输入格式如下：

```
$N$ $Q$
$a_0$ $a_1$ ... $a_{N - 1}$
$\textrm{Query}_0$
$\textrm{Query}_1$
:
$\textrm{Query}_{Q - 1}$
```

### 【输出】

对于每个类型为 `3` 的查询，输出一行一个整数，表示对应区间内元素的和。

### 【输入样例】

```
5 7
1 2 3 4 5
3 0 5
2 2 4 100
3 0 3
0 1 3 10
3 2 5
1 2 5 20
3 0 5
```

### 【输出样例】

```
15
106
119
147
```

### 【数据范围】

- $1 \leq N, Q \leq 200000$
- 在处理查询的过程中始终满足 $\vert a_i \vert \leq 1000000000000$。
- $0 \leq l < r \leq N$

### 【来源】

Library Checker（yosupo06） range_chmin_chmax_add_range_sum
