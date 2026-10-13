# 第 4 题 Garaža (`garaa`)

> 时间限制 1.0 s · 空间限制 256 MB · 12 个测试点 · 全文比较（过滤行末空格及文末回车）

**本题使用文件输入输出**：输入文件 `garaa.in`，输出文件 `garaa.out`。

## 题目描述

Lately, Slavko's been studying sequences of natural numbers. He finds a sequence interesting if the greatest common divisor of all the elements from the sequence is greater than 1.

Yesterday, he found a sequence consisting of N natural numbers in his garage. Since he was really bored, he decided to keep himself occupied by asking simple queries. Each query can be one of the two types:

1. Change the value at position X in the sequence to V.

2. Determine the number of interesting contiguous subarrays contained in the interval [L, R] of the sequence.

## 输入格式

The first line of input contains the numbers N and Q ($1 \le N, Q \le 10^5$), representing the number of elements in the sequence and the number of queries, respectively.

The following line contains N natural numbers $A_i$ ($1 \le A_i \le 10^9$) that represent the numbers in the initial sequence.

Each of the following Q lines contains a query of the following form:

- The first number in the line can be 1 or 2 and represents the type of the query.
- If the query is of type 1, two numbers follow, X ($1 \le X \le N$) and V ($1 \le V \le 10^9$) from the task.
- If the query is of type 2, two numbers follow, L and R ($1 \le L \le R \le N$) that represent the left and right interval boundary.

## 输出格式

For each query of type 2, output the number of interesting contiguous subarrays from the task.

## 样例

### 样例 1

输入：

```text
5 1
8 4 3 9 1
2 2 5
```

输出：

```text
4
```

### 样例 2

输入：

```text
5 3
2 3 6 4 1
2 1 4
1 3 1
2 3 5
```

输出：

```text
6
1
```

### 样例 3

输入：

```text
4 3
2 2 2 2
2 1 4
1 2 3
2 1 4
```

输出：

```text
10
5
```

## 提示

Clarification of the first test case:

The interval from the $2_{nd}$ to the $5_{th}$ position consists of numbers (4, 3, 9, 1). In it, the following are interesting contiguous subarrays (denoted with square brackets):
[4] 3 9 1, 4 [3] 9 1, 4 3 [9] 1, 4 [3 9] 1
