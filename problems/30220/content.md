### 【题目描述】

给定整数 $M$、一个 $N$ 元多项式 $\displaystyle s(x _ 0, x _ 1, \dots, x _ {N - 1}) = \sum _ {i = 0} ^ {2 ^ N - 1} a _ i \prod _ {k = 0} ^ {N - 1} x _ k ^ {i _ k} \in \mathbb{F} _ {998244353} \lbrack x _ 0, x _ 1, \dots, x _ {N - 1} \rbrack$ 以及 $\mathbb{F} _ {998244353}$ 中元素构成的序列 $(w _ 0, \ldots, w _ {2 ^ N - 1})$。其中 $i_k$ 表示把 $i$ 写成二进制时 $2 ^ k$ 位的数字。

对每个 $m=0,1,\ldots,M-1$，计算 $\sum _ {i=0} ^ {2 ^ N - 1} w_ib_i$，其中 $b_i$ 由下式定义：$s(x _ 0, x _ 1, \dots, x _ {N - 1})^m \equiv \sum _ {i = 0} ^ {2 ^ N - 1} b _ i \prod _ {k = 0} ^ {N - 1} x _ k ^ {i _ k} \pmod{(x _ 0 ^ 2, x _ 1 ^ 2, \dots, x _ {N - 1} ^ 2)}$。

### 【输入】

```
$N$ $M$
$a _ 0$ $a _ 1$ $\cdots$ $a _ {2^N-1}$
$w _ 0$ $w _ 1$ $\cdots$ $w _ {2^N-1}$
```

### 【输出】

```
$\mathrm{ans}_0$ $\mathrm{ans}_1$ $\cdots$ $\mathrm{ans}_{M-1}$
```

### 【输入样例】

```
2 10
1 2 3 4
5 6 7 8
```

### 【输出样例】

```
5 70 231 488 841 1290 1835 2476 3213 4046
```

### 【数据范围】

- $0 \leq N \leq 20$
- $0 \leq M \leq 100000$
- $0 \leq a_i, w_i \lt 998244353$

### 【来源】

Library Checker（yosupo06） power_projection_of_set_power_series
