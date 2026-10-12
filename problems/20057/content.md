# Bent Paths

![](https://s21.ax1x.com/2025/07/22/pVGmnb9.png)

如图，在平面直角坐标系 $xOy$ 中，有点 $A_1(1,0),A_2(1,1),A_3(-1,1),A_4(-1,-1),\\A_5(2,-1),\ldots$，它们描述了前路。你需要支持 $2$ 种询问：

- 格式 `1 n`，询问点 $A_n$ 的坐标。
- 格式 `2 l r`，询问折线段 $A_lA_{l+1}A_{l+2}\dots A_{r-1}A_r$ 的长度。

共有 $q$ 个询问。

## 输入格式

第一行一个整数 $q$，表示询问总数。
	
接下来 $q$ 行，每行一个询问。

## 输出格式

对于每一个询问，输出对应的值，**每行一个**。

## 样例

### 输入样例 1

```plain
3
1 9
2 1 9
1 2020
```

### 输出样例 1

```plain
3 -2
24
-505 -505
```

### 样例 1 说明

- 对于询问 1，有 $A_9(3,-2)$。
- 对于询问 2，折线段的长度 $=A_1A_2+A_2A_3+\dots+A_8A_9=24$。

### 样例 2

见选手目录下的 $\textit{\textbf{seek/seek2.in}}$ 与 $\textit{\textbf{seek/seek2.ans}}$。
	
该样例与测试数据 $1\sim 2$ 满足同样的约束条件。
	
### 样例 3

见选手目录下的 $\textit{\textbf{seek/seek3.in}}$ 与 $\textit{\textbf{seek/seek3.ans}}$。
	
该样例与测试数据 $3\sim 5$ 满足同样的约束条件。
	
### 样例 4

见选手目录下的 $\textit{\textbf{seek/seek4.in}}$ 与 $\textit{\textbf{seek/seek4.ans}}$。
	
该样例与测试数据 $6\sim 10$ 满足同样的约束条件。
	
### 样例 5

见选手目录下的 $\textit{\textbf{seek/seek5.in}}$ 与 $\textit{\textbf{seek/seek5.ans}}$。
	
该样例与测试数据 $11\sim 20$ 满足同样的约束条件。

## 数据规模与约定

![](https://s1.ax1x.com/2022/08/13/vtQrxe.png)

**特殊性质 A**：仅含有询问 1。

对于 $100\%$ 的数据，都有 $1\le n\le 10^9$，$1\le l< r\le 10^6$，$1\le q\le 10^5$。
