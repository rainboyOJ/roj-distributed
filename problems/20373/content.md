# 第 3 题 Zvijezda (`zvijezda`)

> CSP-S 复赛模拟赛 23 · 时间限制 1.0 s · 空间限制 256 MB · 30 个测试点 · 全文比较（过滤行末空格及文末回车）

**本题使用文件输入输出**：输入文件 `zvijezda.in`，输出文件 `zvijezda.out`。

## 题目描述

Mirko and Slavko are spending their free time playing with polygons and watching a new season of *The Biggest Loser*. Mirko recently drew a convex polygon with an even number of vertices $N$. Slavko then considered each pair of opposite sides (two sides are opposite if there are $\frac{N}{2} - 1$ sides between them), drew straight lines that lie on those sides and colored them along with the part of the plane that lies between them and contains the polygon. Finally, Mirko found a set of $Q$ points and decided to challenge Slavko to answer for each point whether it lies in the colored or uncolored part of the plane. The new episode of *The Biggest Loser* is about to start and Slavko doesn't have the time to answer Mirko's queries. Can you help him?

## 输入格式

The first line contains an integer $T$ which is used as a parameter for generating Mirko's queries. This number can be either 0 or 1.

The second line contains an even integer $N$ from the task description.

Each of the next $N$ lines contains two integers $X_i$, $Y_i$ ($0 \le |X_i|, |Y_i| \le 10^9$) which represent one of the polygon's vertices. You can assume that the vertices are given in the counter - clockwise order and that no three successive vertices are collinear.

The next line contains an integer $Q$ from the task description.

Each of the next $Q$ lines contains two integers $A_i$, $B_i$ ($0 \le |A_i|, |B_i| \le 2 \cdot 10^{18}$) which are used as parameters for generating the point in the $i$ - th of Mirko's queries.

Let $X_i$ be equal to the number of points in the first $i$ (inclusive) of Mirko's queries that lie in the colored part of the plane. Naturally, $X_0 = 0$. The point of Mirko's $i$ - th query should then be generated as:

$$P_i = (A_i \oplus (T \cdot X_{i-1}^3), B_i \oplus (T \cdot X_{i-1}^3))$$

where $\oplus$ represents the bitwise xor operation.

## 输出格式

The $i$ - th line of output should contain the word DA (YES in Croatian) if the point from $i$ - th of Mirko's queries lies in the colored part of the plane. Otherwise, the $i$ - th line should contain the word NE (NO in Croatian).

## 样例

### 样例 1

输入：

```text
0
4
1 1
5 1
4 3
2 2
4
3 2
2 4
6 2
4 5
```

输出：

```text
DA
NE
DA
NE
```

### 样例 2

输入：

```text
0
6
-1 -1
2 -1
3 3
2 4
1 4
-2 1
6
2 2
3 0
1 -6
2 6
-5 5
5 10
```

输出：

```text
DA
DA
NE
NE
NE
NE
```

### 样例 3

输入：

```text
1
6
-1 -1
2 -1
3 3
2 4
1 4
-2 1
6
2 2
3 0
1 -6
2 6
-5 5
5 10
```

输出：

```text
DA
DA
DA
NE
NE
NE
```

## 提示

### 数据规模及约定

本题采用捆绑测试。

| Subtask | Scores | Constraints |
| --- | --- | --- |
| 1 | 20 | $1 \le n, q \le 2000$，$T = 0$ |
| 2 | 30 | $1 \le n, q \le 10^5$，$T = 0$ |
| 3 | 60 | $1 \le n, q \le 10^5$，$T = 1$ |

此外，对于 100% 的数据，$0 \le |x_i|, |y_i| \le 10^9$，$0 \le |a_i|, |b_i| \le 2 \times 10^{18}$。

### 说明

**

**
