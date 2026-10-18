### 【题目描述】

给定一个形式幂级数 $f(x) = \sum_{i=0}^{N-1} a_i x^i \in \mathbb{Q}[[x]]$，其中 $a_0 = 0$。

求 $\exp(f(x)) = \sum_{i=0}^{\infty} b_i x^i$ 的前 $N$ 项。

也就是说，求 $g(x) = \sum_{i=0}^{N-1} b_i x^i \in \mathbb{Q}[[x]]$，使得

$$g(x) \equiv \sum_{k=0}^{N-1} \frac{f(x)^k}{k!} \pmod{x^N}.$$

输出各系数对 $998244353$ 取模后的结果。

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
0 1 2 3 4
```

### 【输出样例】

```
1 1 499122179 166374064 291154613
```

### 【数据范围】

- $1 \leq N \leq 500000$
- $0 \leq a_i < 998244353$
- $a_0 = 0$

### 【来源】

Library Checker（yosupo06） exp_of_formal_power_series
