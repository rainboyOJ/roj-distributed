### 【题目描述】

给定多项式 $\displaystyle f(x) = \sum_{i=0}^{N-1} a_i x^i \in \mathbb{Z}[x]$ 以及整数 $p_0, p_1, \ldots, p_{N-1}$。

求 $b_0, b_1, \ldots, b_{N-1}$，使得 $\displaystyle f(x) = \sum_{i=0}^{N-1} b_i \prod_{j=0}^{i-1} (x-p_j)$，并将它们模 $998244353$ 输出。

### 【输入】

```
$N$
$a_0$ $a_1$ $\cdots$ $a_{N-1}$
$p_0$ $p_1$ $\cdots$ $p_{N-1}$
```

### 【输出】

```
$b_0$ $b_1$ $\cdots$ $b_{N-1}$
```

### 【输入样例】

```
5
1 10 100 1000 10000
0 1 2 3 4
```

### 【输出样例】

```
1 11110 73100 61000 10000
```

### 【数据范围】

- $0 \leq N \leq 131072$
- $0 \leq a_i, p_i \lt 998244353$

### 【来源】

Library Checker（yosupo06） conversion_from_monomial_basis_to_newton_basis
