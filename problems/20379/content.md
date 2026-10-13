# 第 1 题 Vode (`voe`)

> CSP-S 复赛模拟赛 25 · 时间限制 1.0 s · 空间限制 256 MB · 30 个测试点 · 全文比较（过滤行末空格及文末回车）

**本题使用文件输入输出**：输入文件 `voe.in`，输出文件 `voe.out`。

## 题目描述

As we all very well know, goats and sheep have been fighting for years about the fields they're grazing. After many fierce fights, the goat leader and the sheep leader decided to meet to try to find a peaceful solution to their problem. After many hours of discussion, they agreed that they will play a game for each field and that the winner will get to graze that field.

The game is played such that a total of $N$ animals (that can be goats or sheep) form a circle (the exact order of goats and sheep is an agreement between their leaders). After animal $i$ ($1 \le i \le N-1$), the game is continued by animal $i+1$, and after animal $N$, the game is continued by animal $1$. The animal starting the game can say any positive integer from the interval $[1, K]$, but only if that number is not greater than $M$. If the animal that started the game said the number $j$, then the next animal can say a number in interval $[j+1, j+K]$, but only if that number is not greater than $M$. In other words, each animal can say a number that is greater by minimally $1$, and maximally by $K$ than the number said by the animal before, but only if the new number is not greater than $M$. If an animal must say number $M$, its team (goats or sheep) loses.

If both the goats and the sheep are playing optimally, for each $i$ ($1 \le i \le N$), determine who will win the field if the game is started by the $i^{th}$ animal.

## 输入格式

The first line of input contains $N$, $M$ and $K$ ($1 \le N, M, K \le 5000$), the numbers from the task. The following line contains $N$ numbers, $0$ if the $i^{th}$ animal is a sheep, and $1$ if it's a goat.

## 输出格式

Output $N$ space-separated numbers. For each animal $i$ ($1 \le i \le N$) output $0$ if the sheep will win the field, and $1$ if the goats will win, if the $i^{th}$ animal is starting the game.

## 样例

### 样例 1

输入：

```text
2 9 2
0 1
```

输出：

```text
0 1
```

### 样例 2

输入：

```text
6 499 5
1 0 0 1 1 0
```

输出：

```text
0 1 1 1 1 0
```

### 样例 3

输入：

```text
10 100 10
0 0 0 1 1 1 1 0 1 1
```

输出：

```text
1 1 1 1 1 1 1 1 1 1
```

## 提示

In test cases worth a total of 60% of points, it will hold $1 \le N, M, K \le 500$.

**Clarification of the first test case:**

When a sheep is playing first, it can play like this:

The sheep starts with number 2, after which the goat can say 3 or 4. In both cases, the sheep can say 5, after which the goat can say either 6 or 7. In both cases, the sheep can say 8, after which the goat doesn't have any other choice but 9 and thus losing the game and the field.
