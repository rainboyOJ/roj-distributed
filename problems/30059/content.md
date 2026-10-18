### 【题目描述】

设 $S$ 为一个空的整数集合。依次处理以下 $Q$ 个查询：

- `0 x`：若 $x$ 不在 $S$ 中，则将 $x$ 插入 $S$；
- `1 x`：若 $x$ 在 $S$ 中，则将 $x$ 从 $S$ 中删除；
- `2 x`：求 $\min_{i \in S}(i \oplus x)$，其中 $\oplus$ 表示按位异或。

### 【输入】

```
$Q$
$\mathrm{Query}_0$
$\mathrm{Query}_1$
$\mathrm{Query}_2$
$\hspace{15pt} \vdots$
$\mathrm{Query}_{Q - 1}$
```

### 【输出】

对每个 `2 x` 查询，输出一行一个整数，表示 $\min_{i \in S}(i \oplus x)$。

### 【输入样例】

```
6
0 6
0 7
2 5
1 7
1 10
2 7
```

### 【输出样例】

```
2
1
```

### 【数据范围】

- $1 \leq Q \leq 500000$
- $0 \le x \lt 2^{30}$
- 处理 `2 x` 类型的查询时，$S$ 不为空。

### 【来源】

Library Checker（yosupo06） set_xor_min
