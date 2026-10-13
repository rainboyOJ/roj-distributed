# 第 1 题 Alias (`alias`)

> 时间限制 1.0 s · 空间限制 256 MB · 7 个测试点 · 全文比较（过滤行末空格及文末回车）

**本题使用文件输入输出**：输入文件 `alias.in`，输出文件 `alias.out`。

## 题目描述

Novak 和 Rafael 正在玩一个简化版的《Alias》游戏。Novak 需要让 Rafael 猜出一个词，但不能直接说出这个词。Rafael 的头脑中有一个包含 $n$ 个单词的数据库，并且某些单词之间有 $m$ 条关联。单词 $x$ 和 $y$ 之间的关联带有时间 $t$，表示如果 Rafael 想起或听到了单词 $x$，那么在 $t$ 毫秒后他会想起单词 $y$。

Novak 和 Rafael 将进行 $q$ 轮游戏。在每一轮中，Novak 想知道：如果他说出单词 $a$，Rafael 将在多少毫秒后第一次想起单词 $b$？各轮游戏之间相互独立。

## 输入格式

第一行包含两个整数 $n$（$2 \le n \le 1000$）和 $m$（$1 \le m \le 1000$），分别表示单词数量和关联数量。

接下来的 $m$ 行，每行描述一条关联，包含两个不同的单词 $x_i$ 和 $y_i$，以及一个整数 $t_i$（$1 \le t_i \le 10^9$）。单词由最多 20 个小写字母组成。Rafael 数据库中的所有单词至少会出现一次。某些单词对之间可能存在多条关联。

下一行包含一个整数 $q$（$1 \le q \le 1000$），表示游戏轮数。

接下来的 $q$ 行，每行包含两个不同的单词 $a_i$ 和 $b_i$，分别表示第 $i$ 轮中 Novak 会说的单词，以及 Rafael 需要想起的单词。这两个单词都出现在 Rafael 的数据库中。

## 输出格式

输出 $q$ 行。第 $i$ 行输出第 $i$ 轮所需的时间（单位为毫秒），如果 Rafael 永远无法想起该单词，则输出 `Roger`。

## 样例

### 样例 1

输入：

```text
3 2
novak goat 1
goat simulator 3
2
novak simulator
simulator goat
```

输出：

```text
4
Roger
```

### 样例 2

输入：

```text
3 3
kile legend 4
legend beer 5
beer kile 6
2
kile beer
legend kile
```

输出：

```text
9
11
```

### 样例 3

输入：

```text
4 5
rafael me 5
me ow 6
ow ausopenfinal 2012
ausopenfinal me 2
rafael ausopenfinal 2
3
rafael me
me rafael
ow me
```

输出：

```text
4
Roger
2014
```

## 提示

### 样例 1 解释：

在第一轮中，Novak 会说单词 `novak`。1 毫秒后，Rafael 会想起单词 `goat`，再过 3 毫秒后，他会想起目标单词 `simulator`。在第二轮中，Novak 会说单词 `simulator`，但 Rafael 不会再想起任何其他单词。

## 数据规模与约定

在 20 分的测试数据中，满足 $1 \le n \le 10$。
在另外 20 分的测试数据中，满足 $1 \le m \le 100$。

## 说明

**

**

Translated by DeepSeek-V3
