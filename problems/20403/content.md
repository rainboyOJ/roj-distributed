# 第 1 题 零花钱 (`deparac`)

> 时间限制 1.0 s · 空间限制 256 MB · 104 个测试点 · 全文比较（过滤行末空格及文末回车）

**本题使用文件输入输出**：输入文件 `deparac.in`，输出文件 `deparac.out`。

## 题目描述

Mother Antonija has earned $N$ euros and must spend all of it as soon as possible. She may keep a portion of the money for herself, but the remaining amount must be equally distributed to her two sons over several days.

First, she chooses a non-negative integer $k$ ($0 \le k \le N$) to keep for herself. The remaining amount of $N - k$ euros is then distributed to the sons over $d$ days. Mother Antonija may also choose not to distribute anything to her sons, which corresponds to the case when $N = k$ and $d = 0$.

If the money is distributed, it is done so that each day both sons receive the same amount of money. If one son receives $x$ euros on a given day, the other son also receives $x$ euros, where $x$ must be a positive integer. In total, each son must receive the same total amount of money.

Two distributions are considered different if at least one of the following holds:

- the chosen amount $k$ is different
- the number of days $d$ is different
- there exists at least one day on which the amounts received by the sons differ (i.e., the sequence of daily payments is not identical).

Your task is to determine the number of different ways in which the mother can distribute the money. Since the number of ways can be very large, output the result modulo $10^9 + 7$.

## 输入格式

The first line contains a natural number $n$ ($1 \le n \le 10^{15}$), the number from the problem statement.

## 输出格式

Print a single number - the number of ways in which mother Antonija can distribute the money.

## 样例

### 样例 1

输入：

```text
4
```

输出：

```text
4
```

### 样例 2

输入：

```text
5
```

输出：

```text
4
```

### 样例 3

输入：

```text
793
```

输出：

```text
137435472
```

## 提示

**Clarification of the first example:** We consider all possible values of the number $k$:

$k = 4$ $\to$ the mother keeps all the money, so the only distribution is the one where the sons receive no money.

$k = 2$ $\to$ 2 euros remain to be distributed to the sons. The only valid distribution is $d = 1$, where each son receives 1 euro.

$k = 0$ $\to$ 4 euros remain to be distributed to the sons. There are two valid distributions:

$d = 1$ $\to$ each son receives 2 euros

$d = 2$ $\to$ each day, each son receives 1 euro

$k = 1$ and $k = 3$ $\to$ there is no way to divide the remaining amount so that both sons receive the same positive integer amount each day.

In total, there are $1 + 1 + 2 = 4$ different ways of distribution.

**Scoring**

| Subtask | Points | Constraints |
| --- | --- | --- |
| 1 | 12 | $n \le 10$ |
| 2 | 17 | $n \le 1000$ |
| 3 | 36 | $n \le 10^6$ |
| 4 | 5 | No additional constraints. |
