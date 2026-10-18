### 【题目描述】

给定一个形式幂级数 $f(x) = \sum_{i=0}^{N-1} a_i x^i \in \mathbb{Q}[[x]]$，其中 $a_0 = 1$。

计算 $\log(f(x)) = \sum_{i=0}^{\infty} b_i x^i$ 的前 $N$ 项。
换句话说，求 $g(x) = \sum_{i=0}^{N-1} b_i x^i \in \mathbb{Q}[[x]]$，满足 $b_0 = 0$ 且

$$f(x) \equiv \sum_{k=0}^{N-1} \frac{g(x)^k}{k!} \pmod{x^N}.$$ 

输出模 $998244353$ 意义下的系数。

### 【输入】

输入格式如下：

```
$N$
$a_0$ $a_1$ $\cdots$ $a_{N - 1}$
```

### 【输出】

输出格式如下：

```
$b_0$ $b_1$ $\cdots$ $b_{N - 1}$
```

### 【输入样例】

```
5
1 1 499122179 166374064 291154613
```

### 【输出样例】

```
0 1 2 3 4
```

### 【数据范围】

- $1 \leq N \leq 500000$
- $0 \leq a_i < 998244353$
- $a_0 = 1$

### 【来源】

Library Checker（yosupo06） log_of_formal_power_series
