### 【题目描述】

有 $T$ 组测试数据。

对于每组测试数据，给定两个非负整数 $A$ 和 $B$。
请计算 Nim 积 $A \otimes B$。

非负整数的 Nim 和与 Nim 积递归定义如下：

- $a \oplus b = \operatorname{mex}(\lbrace a' \oplus b \mid a' < a \rbrace \cup \lbrace a \oplus b' \mid b' < b \rbrace)$
- $a \otimes b = \operatorname{mex}\lbrace (a' \otimes b) \oplus (a \otimes b') \oplus (a' \otimes b') \mid a' < a,\thinspace b' < b \rbrace$

### 【输入】

```
$T$
$A_0$ $B_0$
 $\vdots$
$A_{T-1}$ $B_{T-1}$
```

### 【输出】

```
$\mathit{answer}_0$
 $\vdots$
$\mathit{answer}_{T-1}$
```

### 【输入样例】

```
11
5 0
5 1
5 2
5 3
5 4
5 5
5 6
5 7
5 8
3141 5926
18446744073709551615 18446744073709551615
```

### 【输出样例】

```
0
5
10
15
2
7
8
13
3
14994
11290409524105353207
```

### 【数据范围】

- $1 \le T \le 1000000$
- $0 \le A < 2^{64}$
- $0 \le B < 2^{64}$

### 【来源】

Library Checker（yosupo06） nim_product_64
