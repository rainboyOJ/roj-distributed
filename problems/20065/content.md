### 问题描述

有 $n$ 堆石头，Alice 和 Bob 轮流选取，Alice 先手取第一轮，Bob 取第二轮，Alice 取第三轮以此类推，每轮选取的石头个数不能超过 $k$ 个且至少取一个，取到最后一个石头的人胜利。

此外提出了额外一条规则，从第二轮开始，每个人选的石子数必须是前一轮的因数。

假设两人绝顶聪明，试输出最终谁会胜利。

### 输入格式

第一行包含 $1$ 个正整数 $T$。

之后 $T$ 行，每行给出两个正整数 $n,k$。

### 输出格式

输出共 $T$ 行。对于每组数据，若 Alice 有必胜策略，则输出 Alice ，否则输出 Bob。

### 样例输入

```text
20
3 2
4 3
5 1
998 888
242 131
80 160
80 40
80 16
80 32
80 48
12 4
13 11
12 3
25 29
3 13
19 28
13 24
1 22
16 28
29 6
```

### 样例输出

```text
Alice
Bob
Alice
Alice
Alice
Alice
Alice
Alice
Alice
Alice
Alice
Alice
Bob
Alice
Alice
Alice
Alice
Alice
Alice
Alice
```

### 评测数据规模

对于 $30\%$ 的数据，$k \leq 1$​​。

对于 $60\%$ 的数据，$k \leq 2$。

对于所有测评数据，$1 \le T \leq 10^6,1 \leq n,k \leq 10^9$。
