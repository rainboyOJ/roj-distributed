### 【题目描述】

给定 $N \times M$ 的矩阵 $A$ 和 $M \times K$ 的矩阵 $B$，输出 $C = AB \bmod 2$。

输入与输出矩阵时，请把每一行视为由其各分量（$0$ 或 $1$）拼接而成的字符串。

### 【输入】

```
$N\ M\ K$
$a_{11}a_{12} \cdots a_{1M}$
$a_{21}a_{22} \cdots a_{2M}$
$\vdots$
$a_{N1}a_{N2} \cdots a_{NM}$
$b_{11}b_{12} \cdots b_{1K}$
$b_{21}b_{22} \cdots b_{2K}$
$\vdots$
$b_{M1}b_{M2} \cdots b_{MK}$
```

### 【输出】

```
$c_{11}c_{12} \cdots c_{1K}$
$c_{21}c_{22} \cdots c_{2K}$
$\vdots$
$c_{N1}c_{N2} \cdots c_{NK}$
```

### 【输入样例】

```
2 2 2
11
10
10
11
```

### 【输出样例】

```
01
10
```

### 【输入样例2】

```
1 2 3
10
101
010
```

### 【输出样例2】

```
101
```

### 【输入样例3】

```
1 1 1
0
0
```

### 【输出样例3】

```
0
```

### 【数据范围】

- $1 \leq N,M,K \leq 4096$
- $a_{ij},b_{ij} \in \lbrace 0,1\rbrace$

### 【来源】

Library Checker（yosupo06） matrix_product_mod_2
