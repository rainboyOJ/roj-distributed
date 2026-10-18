### 【题目描述】

带符号的第一类斯特林数 $s(n, k)$ 定义为恒等式
$$x (x - 1) \cdots (x - (n - 1)) = \sum_{k=0}^n s(n, k) x^k$$
中的系数。

给定两个整数 $N,K$。
对于所有 $K \le n \le N$，计算 $s(n, K) \bmod 998244353$。

### 【输入】

```
$N$ $K$
```

### 【输出】

```
$s(K, K)$ $\cdots$ $s(N, K)$
```

### 【输入样例】

```
6 3
```

### 【输出样例】

```
1 998244347 35 998244128
```

### 【数据范围】

- $0 \le K \le N \le 500000$

### 【来源】

Library Checker（yosupo06） stirling_number_of_the_first_kind_fixed_k
