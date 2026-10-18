### 【题目描述】

给定一个大小为 $N$ 的排列 $P_0, P_1, \cdots, P_{N-1}$，输出与该排列对应的**公共区间分解树**。本题中各项定义如下。

- **区间**（interval）是指可以表示为 $\lbrace i\in \mathbb{Z}\ |\ l \leq i \leq r\rbrace $ 的集合，其中 $l$ 和 $r$ 为整数（$\ 0 \leq l \leq r <N$）。我们把这样的**区间**记为**区间** $\[l, r\]$。
- **连通区间**是指满足 $\lbrace P_i\ |\ l \leq i \leq r\rbrace$ 也是**区间**的**区间** $\[l, r\]$。
- **强区间**是指满足以下条件的**连通区间** $I$：对任意**连通区间** $J$，都有 $I \subset J$、$J \subset I$、$I \cap J =\emptyset$ 之一成立。
- **公共区间分解树**是以全体**强区间**为元素、按包含关系这一偏序构成的 Hasse 图所表示的有根树。
- **线性节点**是指这样的顶点：当其儿子按照左端点 $l$ 升序排列时，任意连续若干个儿子的并都是**连通区间**。
- **素节点**是指不是**线性节点**的顶点。

### 【输入】

```
$N$
$P_0\ P_1\ P_2\ \cdots P_{N-1}$
```

### 【输出】

```
$X$
$p_0\ l_0\ r_0\ S_0$
$p_1\ l_1\ r_1\ S_1$
$\vdots$
$p_2\ l_{X-1}\ r_{X-1}\ S_{X-1}$
```

$X$ 是**公共区间分解树**中的顶点数。$p_i$（$p_i < i$）是第 $i$ 个顶点的父亲顶点的编号，若第 $i$ 个顶点是树根则 $p_i=-1$。$\[l_i,r_i\]$ 是第 $i$ 个顶点对应的**区间**，若第 $i$ 个顶点是**线性节点**则 $S_i$ 为 "linear"，若是**素节点**则 $S_i$ 为 "prime"。

### 【输入样例】

```
3
0 1 2
```

### 【输出样例】

```
4
-1 0 2 linear
0 0 0 linear
0 1 1 linear
0 2 2 linear
```

### 【输入样例2】

```
4
0 2 1 3
```

### 【输出样例2】

```
6
-1 0 3 linear
0 0 0 linear
0 1 2 linear
2 1 1 linear
2 2 2 linear
0 3 3 linear
```

### 【输入样例3】

```
10
8 0 9 2 1 4 6 5 7 3
```

### 【输出样例3】

```
16
-1 0 9 prime
0 0 0 linear
0 1 1 linear
0 2 2 linear
0 3 9 linear
4 3 4 linear
5 3 3 linear
5 4 4 linear
4 5 9 linear
8 5 8 linear
9 5 5 linear
9 6 7 linear
11 6 6 linear
11 7 7 linear
9 8 8 linear
8 9 9 linear
```

### 【数据范围】

- $1 \leq N \leq 500000$
- $0 \leq P_i < N$
- $P_i \neq P_j (i \neq j)$

### 【来源】

Library Checker（yosupo06） common_interval_decomposition_tree

本题为 special judge（输出任意合法解），暂不可本地评测。
