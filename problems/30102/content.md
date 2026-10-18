### 【题目描述】

给定一个 $N$ 个顶点、$M$ 条边的简单无向图。第 $i$ 条边为 $\lbrace u_i, v_i\rbrace$。

求出该图的色数 $C$。

### 【输入】

```
$N$ $M$
$u_0$ $v_0$
$u_1$ $v_1$
:
$u_{M - 1}$ $v_{M - 1}$
```

### 【输出】

```
$C$
```

### 【输入样例】

```
5 7
0 1
0 2
0 4
1 3
2 3
2 4
3 4
```

### 【输出样例】

```
3
```

### 【输入样例2】

```
20 0
```

### 【输出样例2】

```
1
```

### 【数据范围】

- $1 \leq N \leq 20$
- $0 \leq M \leq \frac{N(N-1)}{2}$
- $0 \leq u_i, v_i < N$
- $u_i \neq v_i$
- $\lbrace u_i, v_i\rbrace \neq \lbrace u_j, v_j\rbrace$

### 【来源】

Library Checker（yosupo06） chromatic_number
