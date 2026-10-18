### 【题目描述】

给定 $N$ 个矩形：第 $i$ 个矩形表示为

$$\lbrace (x,y):l_i \leq x \leq r_i,d_i \leq y \leq u_i \rbrace$$

输出这些矩形并集的面积。

### 【输入】

输入格式如下：

```text
$N$
$l_0$ $d_0$ $r_0$ $u_0$
$l_1$ $d_1$ $r_1$ $u_1$
$\vdots$
$l_{N-1}$ $d_{N-1}$ $r_{N-1}$ $u_{N-1}$
```

### 【输出】

输出这些矩形并集的面积。

### 【输入样例】

```
3
1 1 2 5
2 1 5 2
1 2 2 5
```

### 【输出样例】

```
7
```

### 【数据范围】

- $1 \leq N \leq 500000$
- $0 \leq l_i < r_i \leq 1000000000$
- $0 \leq d_i < u_i \leq 1000000000$

### 【来源】

Library Checker（yosupo06） area_of_union_of_rectangles
