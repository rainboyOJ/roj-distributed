### 【题目描述】

给定一个 $N$ 元多项式

$$s(x _ 0, x _ 1, \dots, x _ {N - 1}) = \sum _ {i = 0} ^ {2 ^ N - 1} b _ i \prod _ {k = 0} ^ {N - 1} x _ k ^ {i _ k} \in \mathbb{F} _ {998244353} \lbrack x _ 0, x _ 1, \dots, x _ {N - 1} \rbrack$$

其中，$i_k$ 表示将 $i$ 表示为二进制数时第 $2 ^ k$ 位上的数字。

请输出 $c _ 0, c _ 1, \dots, c _ {2 ^ N - 1}$（$0 \leq c _ i < 998244353$），使其满足

$$\sum _ {m = 0} ^ N \frac{s(x _ 0, x _ 1, \dots, x _ {N - 1})^m}{m!} \equiv \sum _ {i = 0} ^ {2 ^ N - 1} c _ i \prod _ {k = 0} ^ {N - 1} x _ k ^ {i _ k} \pmod{(x _ 0 ^ 2, x _ 1 ^ 2, \dots, x _ {N - 1} ^ 2)}$$

。

### 【输入】

输入格式如下：

```text
$N$
$b_0$ $b_1$ $\cdots$ $b_{2^N-1}$
```

### 【输出】

输出格式如下：

```text
$c_0$ $c_1$ $\cdots$ $c_{2^N-1}$
```

### 【输入样例】

```
3
0 6 7 8 9 10 11 12
```

### 【输出样例】

```
1 6 7 50 9 64 74 598
```

### 【数据范围】

- $0 \leq N \leq 20$
- $0 \leq b_i < 998244353$
- $b_0 = 0$

### 【来源】

Library Checker（yosupo06） exp_of_set_power_series
