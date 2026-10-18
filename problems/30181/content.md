### 【题目描述】

整数序列 $(a_i)$ 满足以下线性递推式：

$$a_{i} \equiv \sum_{j=1}^{d} c_j a_{i - j} \pmod{998244353},\  i\geq d$$

给定 $a_0,a_1,\ldots,a_{d-1}$，请输出 $a_k \bmod 998244353$。

### 【输入】

```
$d$ $k$
$a_0$ $a_1$ $\ldots$ $a_{d-1}$
$c_1$ $c_2$ $\ldots$ $c_d$
```

### 【输出】

```
$a_k$
```

### 【输入样例】

```
2 5
1 1
1 1
```

### 【输出样例】

```
8
```

### 【数据范围】

- $1 \leq d \leq 100000$
- $0 \leq k \leq 1000000000000000000$
- $0 \leq a_i \lt 998244353\ (0 \leq i \leq d-1)$
- $0 \leq c_i \lt 998244353\ (1 \leq i \leq d)$

### 【来源】

Library Checker（yosupo06） kth_term_of_linearly_recurrent_sequence
