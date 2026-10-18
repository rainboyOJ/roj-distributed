### 【题目描述】

给定形式幂级数 $f(x) = \sum_{i=0}^{N-1} a_i x^i \in \mathbb{F}\_{998244353}[[x]]$，其中 $a_0 = 0, a_1 \neq 0$。

求 $f^{\langle -1 \rangle}(x) = \sum_{i=0}^{\infty} b_i x^i$（其中 $b_0 = 0$）的前 $N$ 项。

换言之，求 $g(x) = \sum_{i=0}^{N-1} b_i x^i \in \mathbb{F}\_{998244353}[[x]]$，使得

$$
f(g(x)) \equiv g(f(x)) \equiv x \pmod{x^{N}}
$$

输出各系数对 $998244353$ 取模的结果。

### 【输入】

第一行包含一个整数 $N$。第二行包含 $N$ 个整数 $a_0\ a_1\ \cdots\ a_{N-1}$。

### 【输出】

输出 $b_0\ b_1\ \cdots\ b_{N-1}$。

### 【输入样例】

```
5
0 1 2 3 4
```

### 【输出样例】

```
0 1 998244351 5 998244339
```

### 【数据范围】

- $2 \leq N \leq 8000$
- $0 \leq a_i < 998244353$
- $a_0 = 0$
- $a_1 \neq 0$

### 【来源】

Library Checker（yosupo06） compositional_inverse_of_formal_power_series
