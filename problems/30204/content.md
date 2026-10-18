### 【题目描述】

给定整数 $N, a, r$ 以及整数序列 $y_0, y_1, ..., y_{N - 1}$。
保证对于 $0\leq i < j \leq N-1$，有 $ar^i\not\equiv ar^j\pmod{998244353}$。

请计算多项式 $f(x) = \sum_{i = 0}^{N - 1} c_i x^i\in \mathbb{Z}[x]$，使得对于每个 $i$ 都满足 $f(ar^i) \equiv y_i \pmod{998244353}$。

此外，必须满足 $0 \leq c_i < 998244353$。

### 【输入】

```text
$N$ $a$ $r$
$y_0$ $y_1$ ... $y_{N-1}$
```

### 【输出】

```text
$c_0$ $c_1$ ... $c_{N -1}$
```

### 【输入样例】

```
4 2 10
17 1241 120401 12004001
```

### 【输出样例】

```
1 2 3 0
```

### 【输入样例2】

```
1 0 0
100
```

### 【输出样例2】

```
100
```

### 【数据范围】

- $0 \leq N \leq 524288$
- $0 \leq a < 998244353$
- $0 \leq r < 998244353$
- $0 \leq y_i < 998244353$
- $ar^i\not\equiv ar^j\pmod{998244353}$（$0\leq i < j \leq N-1$）

### 【来源】

Library Checker（yosupo06） polynomial_interpolation_on_geometric_sequence
