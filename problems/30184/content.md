### 【题目描述】

设 $\widetilde{r}$ 是满足 $-1 < \widetilde{r} < 1$ 且 $\widetilde{r} \equiv r \pmod{998244353}$ 的有理数。
给定整数 $r$ 和 $d$，计算

$$\sum_{i=0}^{\infty} \widetilde{r}^i i^d$$

对 $998244353$ 取模的结果。
在本题的数据范围内，答案是有定义的。
规定 $0^0 = 1$。

### 【输入】

输入包含两个整数 $r$ 和 $d$。

```
$r$ $d$
```

### 【输出】

输出答案。

```
$\mathit{answer}$
```

### 【输入样例】

```
499122177 5
```

### 【输出样例】

```
1082
```

### 【数据范围】

- $0 \le r < 998244353$
- $r \ne 1$
- $0 \le d \le 10000000$

### 【来源】

Library Checker（yosupo06） sum_of_exponential_times_polynomial_limit
