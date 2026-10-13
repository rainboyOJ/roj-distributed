# Merchant

merchant.cpp/in/out

- 时间限制：1.0s
- 空间限制：512MB

## 题目描述

有 $n$ 个物品，第 $i$ 个物品有两个属性 $k_i, b_i$，表示它在时刻 $x$ 的价值为 $k_i \times x + b_i$。

当前处于时刻 0，你可以选择不超过 $m$ 个物品，使得存在某个整数时刻 $t,\ t \ge 0$，你选择的所有物品的总价值大于等于 $S$。

给出 $S$，求 $t$ 的最小值。

## 输入格式

从文件 `merchant.in` 中读入数据。

第一行三个整数 $n, m, S$。

接下来 $n$ 行，第 $i$ 行两个整数 $k_i, b_i$。

## 输出格式

输出到文件 `merchant.out` 中。

一行一个整数表示答案。

## 样例 1 输入

```text
3 2 100
3 9
-2 50
4 1
```

## 样例 1 输出

```text
13
```

## 样例 1 解释

选择 1, 3 号物品。

## 样例 2 输入

```text
3 2 100
-1 49
-2 50
1 -998244353
```

## 样例 2 输出

```text
998244453
```

## 样例 2 解释

选择 3 号物品。

## 样例 3

见选手目录下的 `merchant/merchant3.in` 与 `merchant/merchant3.ans`。

## 样例 4

见选手目录下的 `merchant/merchant4.in` 与 `merchant/merchant4.ans`。

## 数据范围

对于所有数据，有 $1 \le m \le n \le 10^6$，$-10^9 \le b_i \le 10^9$，$-10^6 \le k_i \le 10^6$，$0 \le S \le 10^{18}$。数据保证有解，且答案不超过 $10^9$。

- Subtask 1 (22%)：$n \le 20$。
- Subtask 2 (36%)：$n \le 10^5$，$0 \le k_i \le 10^4$。
- Subtask 3 (8%)：$k_i \le 0$。
- Subtask 4 (12%)：$n \le 10^5$。
- Subtask 5 (22%)：没有特殊的约束。
