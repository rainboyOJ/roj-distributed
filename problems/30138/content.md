### 【题目描述】

求两个 $\mathbb{F}_2$ 向量空间 $X = \langle u_0, \ldots, u_{n-1}\rangle$ 和 $Y = \langle v_0, \ldots, v_{m-1}\rangle$ 的交集的一个基。具体来说，求一个向量集合 $B = \lbrace w_0, \ldots, w_{k-1} \rbrace$，使其满足：

- 线性无关（对于任意子集 $S = \lbrace s_0, \ldots, s_{l-1}\rbrace\subseteq B$，若 $s_0 \oplus \cdots \oplus s_{l-1} = 0$，则 $S = \emptyset$）。
- 张成 $X \cap Y$（对于任意 $a \in X \cap Y$，存在 $B$ 的一个子集 $S = \lbrace s_0, \ldots, s_{l-1}\rbrace$，使得 $s_0 \oplus \cdots \oplus s_{l-1} = a$。此外，$B \subseteq X \cap Y$）。

每个测试包含 $T$ 组测试数据。

### 【输入】

第一行包含一个整数 $T$。

接下来每组测试数据包含以下内容：

```text
n u_0 u_1 $\cdots$ u_{n - 1}
m v_0 v_1 $\cdots$ v_{m - 1}
```

### 【输出】

对于每组测试数据，输出一行：

```text
k w_0 w_1 $\cdots$ w_{k - 1}
```

### 【输入样例】

```
9
2 1 2
3 1 2 4
3 7 3 1
2 3 1
1 2
2 1 3
1 2
2 3 1
2 3 4
3 1 5 3
3 31 4 15
4 92 65 35 89
3 1 2 4
0
0
3 1 2 4
0
0
```

### 【输出样例】

```
2 1 2
2 3 1
1 2
1 2
2 4 3
0
0
0
0
```

### 【数据范围】

- $1 \leq T \leq 100000$
- $0 \leq n, m \leq 30$
- $0 \leq u_i, v_i \leq 2^{30} - 1$
- $u_0, \ldots, u_{n-1}$ 关于异或运算线性无关。
- $v_0, \ldots, v_{m-1}$ 关于异或运算线性无关。

### 【来源】

Library Checker（yosupo06） intersection_of_f2_vector_spaces

本题为 special judge（输出任意合法解），暂不可本地评测。
