### 【题目描述】

给定一张简单无向图，包含 $N$ 个顶点和 $M$ 条边。
第 $i$ 条边为 $\lbrace u_i, v_i \rbrace$。
每个顶点有一个整数值，第 $i$ 个顶点的值为 $x_i$。

若三个顶点 $a, b, c\ (a \lt b \lt c)$ 之间由 $\lbrace a, b \rbrace, \lbrace a, c \rbrace, \lbrace b, c \rbrace$ 三条边相连，则称它们构成一个三角形。
求所有三角形的 $x_a x_b x_c$ 之和，并对 $998244353$ 取模后输出。

### 【输入】

输入按以下格式给出。

```
$N$ $M$
$x_0$ $x_1$ $\ldots$ $x_{N-1}$
$u_0$ $v_0$
$u_1$ $v_1$
$\vdots$
$u_{M-1}$ $v_{M-1}$
```

### 【输出】

```
$A$
```

### 【输入样例】

```
4 5
1 2 3 4
0 3
2 0
2 1
2 3
1 3
```

### 【输出样例】

```
36
```

$0, 2, 3$ 与 $1, 2, 3$ 构成三角形。
$1 \cdot 3 \cdot 4 + 2 \cdot 3 \cdot 4 \bmod 998244353$ 的结果为 $36$，故输出 $36$。

### 【数据范围】

- $1 \le N \le 100000$
- $1 \le M \le 100000$
- $0 \le x_i \lt 998244353$
- $0 \le u_i \lt N$
- $0 \le v_i \lt N$
- $u_i \neq v_i$
- $\lbrace u_i, v_i \rbrace \neq \lbrace u_j, v_j \rbrace \ (i \neq j)$

### 【来源】

Library Checker（yosupo06） enumerate_triangles
