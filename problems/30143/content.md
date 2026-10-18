### 【题目描述】

给定 $N \times N$ 的矩阵 $M = (a_{ij})$。输出 $\mathrm{det}(M) \bmod 2$。

在矩阵的输入与输出中，请把每一行看作由其各个分量（$0$ 或 $1$）连接而成的字符串。

### 【输入】

```
$N$
$a_{11}a_{12} \cdots a_{1N}$
$a_{21}a_{22} \cdots a_{2N}$
$\vdots$
$a_{N1}a_{N2} \cdots a_{NN}$
```

### 【输出】

输出一行一个整数，即 $\mathrm{det}(M) \bmod 2$。

### 【输入样例】

```
3
110
010
111
```

### 【输出样例】

```
1
```

### 【输入样例2】

```
3
100
011
111
```

### 【输出样例2】

```
0
```

### 【数据范围】

- $1 \leq N \leq 4096$
- $a_{ij} \in \lbrace 0,1\rbrace$

### 【来源】

Library Checker（yosupo06） matrix_det_mod_2
