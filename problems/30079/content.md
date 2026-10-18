### 【题目描述】

给定整数 $n,k,q$ 与质数 $m$，输出 $\binom{n}{k}_q \bmod m$。

其中 $\binom{n}{k}_q$ 表示 $q$-二项式系数。关于 $q$-二项式系数的定义，见 [Gaussian binomial coefficient](https://en.wikipedia.org/wiki/Gaussian_binomial_coefficient)。

本题包含 $T$ 组询问，且所有询问中的 $q$ 与 $m$ 均固定不变。

### 【输入】

```
$T\ m\ q$
$n_0\ k_0$
$n_1\ k_1$
$\vdots$
$n_{T-1}\ k_{T-1}$
```

### 【输出】

每行输出一个 $\binom{n}{k}_q \bmod m$。

### 【输入样例】

```
7 998244353 1
6 0
6 1
6 2
6 3
6 4
6 5
6 6
```

### 【输出样例】

```
1
6
15
20
15
6
1
```

### 【输入样例2】

```
7 998244353 2
6 0
6 1
6 2
6 3
6 4
6 5
6 6
```

### 【输出样例2】

```
1
63
651
1395
651
63
1
```

### 【输入样例3】

```
7 998244353 0
6 0
6 1
6 2
6 3
6 4
6 5
6 6
```

### 【输出样例3】

```
1
1
1
1
1
1
1
```

### 【数据范围】

- $1 \leq T \leq 1000000$
- $1 \leq m \leq 1073741824$
- $m$ 是质数
- $0\leq q \lt m$
- $0 \leq n, k \lt \min(m, 10000000)$

### 【来源】

Library Checker（yosupo06） q_binomial_coefficient_prime_mod
