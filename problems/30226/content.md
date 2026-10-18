### 【题目描述】

对于字符串 $X = X _ 0 X _ 1 X _ 2 \cdots$，我们用 $X[a,b)$ 表示它的子串 $X _ a X _ {a+1} \cdots X _ {b-1}$。

给定一个长度为 $N$ 的字符串 $S = S _ 0 S _ 1 S _ 2 \cdots S _ {N-1}$。请找出一个整数数组 $0 = a _ 0 \lt a _ 1 \lt a _ 2 \lt \ldots \lt a _ k = N$，使得 $S[a _ 0 , a _ 1) , S[a _ 1 , a _ 2) , \ldots , S[a _ {k-1} , a _ k)$ 是 $S$ 的 Lyndon 分解。

### 【输入】

```
$S$
```

### 【输出】

```
$a _ 0$ $a _ 1$ $a _ 2$ $\cdots$ $a _ k$
```

### 【输入样例】

```
babaabaab
```

### 【输出样例】

```
0 1 3 6 9
```

### 【输入样例2】

```
ababacaca
```

### 【输出样例2】

```
0 8 9
```

### 【数据范围】

- $1 \leq N \leq 500000$
- $S$ 的每个字符均为小写英文字母。

### 【来源】

Library Checker（yosupo06） lyndon_factorization
