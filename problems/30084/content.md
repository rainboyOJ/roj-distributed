### 【题目描述】

第二类斯特林数 $S(n, k)$ 定义为下列恒等式中的系数：
$$x^n = \sum_{k=0}^n S(n, k) x (x - 1) \cdots (x - (k - 1)).$$

给定一个整数 $N$。
请计算对于 $0 \le k \le N$ 的 $S(N, k) \bmod 998244353$。

### 【输入】

```
$N$
```

### 【输出】

```
$S(N, 0)$ $\cdots$ $S(N, N)$
```

### 【输入样例】

```
5
```

### 【输出样例】

```
0 1 15 25 10 1
```

### 【数据范围】

- $0 \leq N \leq 500000$

### 【来源】

Library Checker（yosupo06） stirling_number_of_the_second_kind
