### 【题目描述】

第二类斯特林数 $S(n, k)$ 定义为下式中的系数：
$$x^n = \sum_{k=0}^n S(n, k) x (x - 1) \cdots (x - (k - 1)).$$

给定两个整数 $N,K$。
对于 $K \le n \le N$，计算 $S(n, K) \bmod 998244353$。

### 【输入】

```
$N$ $K$
```

### 【输出】

```
$S(K, K)$ $\cdots$ $S(N, K)$
```

### 【输入样例】

```
6 3
```

### 【输出样例】

```
1 6 25 90
```

### 【数据范围】

- $0 \le K \le N \le 500000$

### 【来源】

Library Checker（yosupo06） stirling_number_of_the_second_kind_fixed_k
