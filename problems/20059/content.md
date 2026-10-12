# Dynamic Insertion

给定一个非严格递增的数组 $\{a_n\}$（下标从 $1$ 开始），描述了这个色块序列，每次该数组会发生如下“融合”变换：

- 若数组长度为 $l$，对于每个 $1\le i<l$，在 $a_i,a_{i+1}$ 之间插入一个新数 $\left\lfloor\dfrac{a_i+a_{i+1}}2\right\rfloor$。

其中 $\lfloor x\rfloor$ 表示对 $x$ 向下取整。

你需要回答 $q$ 组询问，每次询问第 $k$ 次“融合”变换后是否存在色块 $x$。

## 输入格式

第一行两个整数 $n,q$，表示初始数组长度和询问组数。

接下来一行 $n$ 个整数，表示原始的数组 $a$。

接下来 $q$ 行，每行两个数 $k,x$，描述每组询问。

## 输出格式

对于每组询问，输出仅一行一个字符串。若存在，输出 `Yes`；否则，输出 `No`（大小写敏感）。

## 样例

### 输入样例 1

```plain
2 2
1 10
2 3
2 4
```

### 输出样例 1

```plain
Yes
No
```

### 样例 1 说明

对于数组 $a=[1,10]$，依次进行变换：

- 第一次变换后，变成 $[1,\underline{\textbf5},10]$。

- 第二次变换后，变成 $[1,\underline{\textbf3},5,\underline{\textbf7},10]$。

容易发现两次变换后，$3$ 在数组中，$4$ 不在数组中。

### 样例 2

见选手目录下的 $\textit{\textbf{juncture/juncture2.in}}$ 与 $\textit{\textbf{juncture/juncture2.ans}}$。
	
该样例与测试数据 $1\sim 5$ 满足同样的约束条件。

### 样例 3

见选手目录下的 $\textit{\textbf{juncture/juncture3.in}}$ 与 $\textit{\textbf{juncture/juncture3.ans}}$。
	
该样例与测试数据 $6\sim 9$ 满足同样的约束条件。

### 样例 4

见选手目录下的 $\textit{\textbf{juncture/juncture4.in}}$ 与 $\textit{\textbf{juncture/juncture4.ans}}$。
	
该样例与测试数据 $13\sim 20$ 满足同样的约束条件。

## 数据规模与约定

![](https://s1.ax1x.com/2022/08/14/vUlLm4.png)

对于 $100\%$ 的数据，$1\le n\le 10^3$，$1\le q\le 5\times 10^5$，$1\le k\le 10^6$，$1\le a_i\le 10^{18}$，且对于 $1\le i<j\le n$，必定满足 $a_i\le a_j$。
