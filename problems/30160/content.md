### 【题目描述】

设质数依次为 $p_0 < p_1 < p_2 < \cdots$（即 $p_0 = 2$，$p_1 = 3$，$p_2 = 5$，以此类推）。

给定整数 $N$、$A$ 和 $B$。
求 $\pi(N)$（不超过 $N$ 的质数个数），
并对满足 $p_{Ai+B} \le N$ 的非负整数 $i$，输出 $p_{Ai+B}$。

### 【输入】

```
$N$ $A$ $B$
```

### 【输出】

```
$\pi(N)$ $X$
$p_{B}$ $p_{A+B}$ $\cdots$ $p_{A(X-1)+B}$
```

### 【输入样例】

```
100 3 1
```

### 【输出样例】

```
25 8
3 11 19 31 43 59 71 83
```

### 【数据范围】

- $1 \le N \le 500000000$
- $0 \le B < A \le N$
- $0 \le X \le 1000000$，其中 $X = \#\lbrace i \in \mathbb{Z}\_{\ge 0} \mid p_{Ai+B} \le N \rbrace$

### 【来源】

Library Checker（yosupo06） enumerate_primes
