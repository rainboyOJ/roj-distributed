### 【题目描述】

给定一个有 $N$ 个变量、$M$ 个子句的 2-SAT 问题。判断它是否可满足，若可满足则构造出一组变量的赋值。

### 【输入】

2-SAT 问题以 [DIMACS 格式](https://www.cs.ubc.ca/~babic/doc/dimacs_cnf.pdf) 给出。请参见样例。

```
p cnf $N$ $M$
$a_1$ $b_1$ 0
$a_2$ $b_2$ 0
:
$a_M$ $b_M$ 0
```

### 【输出】

若输入可满足，按如下方式输出：

```
s SATISFIABLE
v $x_1$ $x_2$ ... $x_N$ 0
```

若第 $i$ 个变量为真，则 $x_i = i$；若为假，则 $x_i = -i$。

若输入不可满足，按如下方式输出：

```
s UNSATISFIABLE
```

### 【输入样例】

```
p cnf 5 6
1 2 0
-3 -1 0
-4 -3 0
2 -5 0
5 -2 0
1 4 0
```

### 【输出样例】

```
s SATISFIABLE
v -1 2 -3 4 5 0
```

该样例的含义如下：

$$
    (x_1 \lor x_2) \land
    (\lnot x_3 \lor \lnot x_1) \land
    (\lnot x_4 \lor \lnot x_3) \land
    (x_2 \lor \lnot x_5) \land
    (x_5 \lor \lnot x_2) \land
    (x_1 \lor x_4)
$$

### 【输入样例2】

```
p cnf 2 4
1 2 0
1 -2 0
-1 2 0
-1 -2 0
```

### 【输出样例2】

```
s UNSATISFIABLE
```

### 【数据范围】

- $1 \leq N \leq 500,000$
- $1 \leq M \leq 500,000$

### 【来源】

Library Checker（yosupo06） two_sat

本题为 special judge（输出任意合法解），暂不可本地评测。
