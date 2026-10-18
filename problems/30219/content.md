### 【题目描述】

给定多项式 $\displaystyle f(x) = \sum _ {i = 0} ^ {M - 1} a _ i x ^ i \in \mathbb{F} _ {998244353} \lbrack x \rbrack$ 以及一个 $N$ 元多项式 $\displaystyle s(x _ 0, x _ 1, \dots, x _ {N - 1}) = \sum _ {i = 0} ^ {2 ^ N - 1} b _ i \prod _ {k = 0} ^ {N - 1} x _ k ^ {i _ k} \in \mathbb{F} _ {998244353} \lbrack x _ 0, x _ 1, \dots, x _ {N - 1} \rbrack$。

其中 $i_k$ 表示将 $i$ 写成二进制时第 $2 ^ k$ 位上的数字。

输出 $c _ 0, c _ 1, \dots, c _ {2 ^ N - 1} ~ (0 \leq c _ i \lt 998244353)$，使其满足

$$f(s(x _ 0, x _ 1, \dots, x _ {N - 1})) \equiv \sum _ {i = 0} ^ {2 ^ N - 1} c _ i \prod _ {k = 0} ^ {N - 1} x _ k ^ {i _ k} \pmod{(x _ 0 ^ 2, x _ 1 ^ 2, \dots, x _ {N - 1} ^ 2)}$$

。

### 【输入】

```
$M$ $N$
$a_0$ $a_1$ $\cdots$ $a_{M-1}$
$b_0$ $b_1$ $\cdots$ $b_{2^N-1}$
```

### 【输出】

```
$c_0$ $c_1$ $\cdots$ $c_{2^N-1}$
```

### 【输入样例】

```
4 3
1 2 3 4
5 6 7 8 9 10 11 12
```

### 【输出样例】

```
586 1992 2324 7948 2988 10124 11590 39264
```

### 【数据范围】

- $0 \leq M \leq 100000$
- $0 \leq N \leq 20$
- $0 \leq a_i, b_i \lt 998244353$

### 【来源】

Library Checker（yosupo06） polynomial_composite_set_power_series
