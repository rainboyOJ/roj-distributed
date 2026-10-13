# 子序列计数

### 题目信息

时间限制:  `1s`

空间限制: `256M`

输入文件: `count.in`

输出文件: `count.out`

### 题目描述
众所周知，一个长度为 $n$ 的序列共有 $2^n-1$ 个不同的非空子序列，现给出一个长度为 $n$ 的序列 $a_1, a_2, \dots, a_n$，其中 $0 \leq a_i<2^m$，且 $a_i$ 互不相同

定义 $a$ 的一个子序列 $p=a_{p_1}a_{p_2}\dots a_{p_k}$ 是合法的，当且仅当：

1. $1\leq p_1 < p_2 < \dots < p_k \leq n$
2. $\forall 1 \leq i \leq k-3, a_{p_i} \oplus a_{p_{i+1}} \oplus a_{p_{i+2}} \oplus a_{p_{i+3}}\neq s$，其中 $\oplus$ 表示异或

请问对于 $a$，有多少个合法的非空子序列？请输出答案 $\bmod\ 998244353$ 之后的结果即可

注：长度小于 4 的非空子序列都是合法的。

### 输入格式
第一行三个正整数 $n, m, s$，其中 $n$ 表示序列 $a$ 的长度，$m$ 表示 $a_i$ 的范围，$s$ 的含义如题面所示

接下来一行 $n$ 个**互不相同**的非负整数 $a_i$

### 输出格式
一行一个整数表示答案 $\bmod\ 998244353$ 之后的结果

### 样例
#### 样例输入 1
```plain
5 3 3
2 3 4 7 6
```

#### 样例输出 1
```plain
30
```

### 数据范围
$\begin{aligned} & 1 \leq n \leq 4000,1 \leq m \leq 12,0 \leq a_i, s<2^m \\ & \text { subtask } 1(15 p t s): n \leq 10, m \leq 4 \\ & \text { subtask2(20pts) : } n \leq 60, m \leq 6 \\ & \text { subtask } 3(25 p t s): n \leq 200, m \leq 8 \\ & \text { subtask } 4(25 p t s): n \leq 1000, m \leq 10 \\ & \text { subtask } 5(15 p t s): n \leq 4000, m \leq 12\end{aligned}$
