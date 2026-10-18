### 【题目描述】

给定一个形式幂级数 $f(x) = \sum_{i=0}^{N-1} a_i x^i \in \mathbb{F}\_{998244353}[[x]]$，其中 $a_0 \ne 0$。
求 $\frac{1}{f(x)} = \sum_{i=0}^{\infty} b_i x^i$ 的前 $N$ 项。
换言之，求出 $g(x) = \sum_{i=0}^{N-1} b_i x^i \in \mathbb{F}\_{998244353}[[x]]$，使得

$$f(x) g(x) \equiv 1 \pmod{x^N}.$$

### 【输入】

```
$N$
$a_0$ $a_1$ $\cdots$ $a_{N - 1}$
```

### 【输出】

```
$b_0$ $b_1$ $\cdots$ $b_{N - 1}$
```

### 【输入样例】

```
5
5 4 3 2 1
```

### 【输出样例】

```
598946612 718735934 862483121 635682004 163871793
```

### 【数据范围】

- $1 \leq N \leq 500000$
- $0 \leq a_i < 998244353$
- $a_0 \neq 0$

### 【来源】

Library Checker（yosupo06） inv_of_formal_power_series
