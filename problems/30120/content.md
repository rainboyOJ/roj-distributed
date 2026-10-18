### 【题目描述】

给定一个由 $N$ 个顶点和 $M$ 条边构成的简单带权无向图 $G$。
第 $i$ 条边为 $\lbrace u_i, v_i \rbrace$，权值为 $w_i$。

设 $H$ 为在图 $G$ 上添加一个新顶点 $N$ 以及 $N$ 条新边后得到的图。
第 $i$ 条边为 $\lbrace i, N \rbrace$，权值为 $a_i$。

依次处理以下 $Q$ 个查询：

- 把边 $\lbrace x_i,N \rbrace$ 的权值改为 $y_i$，并输出 $H$ 的全局最小割大小。

### 【输入】

```
$N$ $M$ $Q$
$a_0$ $a_1$ $\ldots$ $a_{N-1}$
$u_0$ $v_0$ $w_0$
$u_1$ $v_1$ $w_1$
$\vdots$
$u_{M-1}$ $v_{M-1}$ $w_{M-1}$
$x_0$ $y_0$
$x_1$ $y_1$
$\vdots$
$x_{Q-1}$ $y_{Q-1}$
```

### 【输出】

对每个查询，输出一行一个整数，表示 $H$ 的全局最小割大小。

### 【输入样例】

```
4 4 11
0 0 0 1
0 1 1
1 2 2
2 3 3
3 0 0
3 0
0 5
1 5
2 5
3 5
0 0
0 5
1 0
1 5
2 0
2 5
```

### 【输出样例】

```
0
1
2
3
6
1
6
3
6
5
6
```

### 【输入样例2】

```
4 0 6
0 1 2 3
0 0
0 4
1 5
2 6
3 7
0 3
```

### 【输出样例2】

```
0
1
2
3
4
3
```

### 【数据范围】

- $1 \le N \le 4000$
- $0 \le M \le \min ( \frac{N(N-1)}{2} , 4000 )$
- $1 \le Q \le 200000$
- $0 \le a_i \le 1000000000$
- $0 \le u_i, v_i \lt N$
- $u_i \neq v_i$
- $\lbrace u_i, v_i \rbrace \neq \lbrace u_j, v_j \rbrace \  (i \neq j)$
- $0 \le w_i \le 1000000000$
- $0 \le x_i \lt N$
- $0 \le y_i \le 1000000000$

### 【来源】

Library Checker（yosupo06） global_minimum_cut_of_dynamic_star_augmented_graph
