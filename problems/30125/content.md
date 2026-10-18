### 【题目描述】

$\gdef\relmiddle#1{\mathrel{}\middle#1\mathrel{}}$


给定一张有 $n$ 个顶点、$m$ 条边的有向图，每个顶点关联一个供给/需求值，每条边关联流量的下界与上界。
第 $v$ 个顶点在 $b_v$ 为正数时拥有 $b_v$ 的供给量，否则拥有 $-b_v$ 的需求量。
第 $e$ 条边从顶点 $s_e$ 指向 $t_e$，流量下界为 $l_e$，流量上界为 $u_e$，单位流量的费用为 $c_e$。

你的任务是求出并输出最小费用 $\mathbf{b}$-流的值 $z$、达到最小值的流 $\mathbf{f}$ 及其对偶 $\mathbf{p}$，即输出满足下列约束的 $z$、$\mathbf{f} = \lbrace f_e\rbrace _ {e = 0 \dots m-1}$ 与 $\mathbf{p} = \lbrace p_v\rbrace _ {v = 0 \dots n-1}$：

- $z = \sum_{e} c_e f_e$
- $l_e \leq f_e \leq u_e$（容量约束）
- $\sum_{e \in \delta^+(v)} f_e - \sum_{e \in \delta^-(v)} f_e = b_v$（流量守恒约束）
- $f_e \gt l_e \Rightarrow c_e + p_{s_e} - p_{t_e} \le 0$（互补松弛条件）
- $f_e \lt u_e \Rightarrow c_e + p_{s_e} - p_{t_e} \ge 0$（互补松弛条件）
- $|p_v| \le 1000000000000000$

其中 $\delta^+(v)$ 是从顶点 $v$ 出发的边集，$\delta^-(v)$ 是指向顶点 $v$ 的边集，即 $\delta^+(v) = \left\lbrace e \relmiddle| s_e = v \right\rbrace$，$\delta^-(v) = \left\lbrace e \relmiddle| t_e = v \right\rbrace$。

如果不存在这样的值，则输出 "infeasible"。

### 【输入】

```
$n$ $m$
$b_0$
 $\vdots$
$b_{n-1}$
$s_0$ $t_0$ $l_0$ $u_0$ $c_0$
 $\vdots$
$s_{m-1}$ $t_{m-1}$ $l_{m-1}$ $u_{m-1}$ $c_{m-1}$
```

### 【输出】

如果问题不可行，输出一行

```
infeasible
```

。否则，输出

```
$z$
$p_0$
 $\vdots$
$p_{n-1}$
$f_0$
 $\vdots$
$f_{m-1}$
```

### 【输入样例】

```
3 5
1
-1
0
0 1 1 2 1
1 2 0 2 2
2 0 -3 5 1
0 2 0 3 -2
2 1 0 1 0
```

### 【输出样例】

```
-2
0
-1
-1
1
0
3
3
0
```

### 【输入样例2】

```
2 1
-1
1
0 0 -1 1 0
```

### 【输出样例2】

```
infeasible
```

### 【输入样例3】

```
2 1
1
0
0 1 -10 10 0
```

### 【输出样例3】

```
infeasible
```

### 【数据范围】

- $0 \le n \leq 100$
- $0 \le m \leq 1000$
- $0 \le s_e \lt n$
- $0 \le t_e \lt n$
- $|b_v| \le 1000000000$
- $|l_e| \le 1000000000$
- $|u_e| \le 1000000000$
- $|c_e| \le 1000000000$
- $l_e \le u_e$
- 所有数值均为整数

注意：

- 输入图中可能含有自环，
- 且结果值可能超过 $2^{64}$。

### 【来源】

Library Checker（yosupo06） min_cost_b_flow

本题为 special judge（输出任意合法解），暂不可本地评测。
