### 【题目描述】

给定两个形式幂级数 $f(x) = \sum_{i=0}^{N-1} a_i x^i \in \mathbb{F}_{998244353}[[x]]$ 与 $g(x) = \sum_{i=0}^{N-1} b_i x^i \in \mathbb{F}_{998244353}[[x]]$，其中 $b_0 = 0$。

求出 $f(g(x)) = \sum_{i=0}^{\infty} c_i x^i$ 的前 $N$ 项。

也就是说，求出 $h(x) = \sum_{i=0}^{N-1} c_i x^i \in \mathbb{F}_{998244353}[[x]]$，使得

$$h(x) \equiv \sum_{i=0}^{N-1} a_i g(x)^i \pmod{x^N}.$$

### 【输入】

```
$N$
$a_0$ $a_1$ $\cdots$ $a_{N - 1}$
$b_0$ $b_1$ $\cdots$ $b_{N - 1}$
```

### 【输出】

```
$c_0$ $c_1$ $\cdots$ $c_{N - 1}$
```

### 【输入样例】

```
5
5 4 3 2 1
0 1 2 3 4
```

### 【输出样例】

```
5 4 11 26 59
```

### 【数据范围】

- $1 \leq N \leq 131072$
- $0 \leq a_i, b_i < 998244353$
- $b_0 = 0$

### 【来源】

Library Checker（yosupo06） composition_of_formal_power_series_large
