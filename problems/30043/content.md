### 【题目描述】

给定一个长度为 $N$ 的整数序列 $a_0, a_1, \ldots, a_{N-1}$。依次处理以下 $Q$ 个查询：

- `0 $k$ $v$`：令 $a[k] \gets v$；
- `1 $l$ $r$ $x$`：输出 $x$ 在 $a_{l}, a_{l+1}, \ldots, a_{r-1}$ 中出现的次数。

### 【输入】

```
$N$ $Q$
$a_0$ $a_1$ $\cdots$ $a_{N-1}$
$\mathrm{query}_0$
$\vdots$
$\mathrm{query}_{Q-1}$
```

### 【输出】

对每个 `1 $l$ $r$ $x$` 查询，输出一行一个整数，表示 $x$ 在 $a_{l}, a_{l+1}, \ldots, a_{r-1}$ 中的出现次数。

### 【输入样例】

```
5 6
3 7 1 2 1
1 1 5 1
1 3 3 0
1 0 4 3
0 1 1
1 0 5 1
1 0 5 123456789
```

### 【输出样例】

```
2
0
1
3
0
```

### 【数据范围】

- $0 \leq N \leq 200000$
- $0 \leq Q \leq 200000$
- $0 \leq a_i \leq 1000000000$
- $0 \leq k < N$
- $0 \leq v \leq 1000000000$
- $0 \leq l \leq r \leq N$
- $0 \leq x \leq 1000000000$

### 【来源】

Library Checker（yosupo06） point_set_range_frequency
