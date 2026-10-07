// 一本通 1735《环上计数》标程（目标 ROJ 题号 1735，C++17, stdin -> stdout）
//
// 题意：多组数据，每组给一张 n 个点 m 条边的无向图（点从 0 开始编号，保证无重边、
//       无自环，不保证连通）。求两个量：
//         ans1 = 不在任何一个简单环上的边数；
//         ans2 = 在至少两个简单环上的边数。
//       读到 "0 0" 结束；每组输出一行 "ans1 ans2"。
//       范围：1 <= n <= 10000, 1 <= m <= 100000；time 1000 ms / memory 32 MB。
//
// 算法（Tarjan 边栈求点双连通分量（块），O(n + m) 每组）：
//   关键结论 1：边不在任何简单环上 <=> 该边是桥（割边）。
//     判据 low[v] > dfn[u]（u 为 DFS 树中 v 的父点），计 ans1。
//   关键结论 2：设点双（块）内有 n_b 个点、m_b 条边，则
//     * m_b = n_b 时块必为一个简单环（2-连通 + 度数全 = 2），每条边恰在 1 个简单环上；
//     * m_b > n_b 时块内每条边至少在 2 个简单环上；
//     * m_b = n_b - 1 时块只有一条边（桥），不含环。
//     因此 ans2 = Σ_{块 m_b > n_b} m_b，逐块统计边数与去重后的点数即可。
//     依据：2-连通图中任意两条边同属某个简单环；m_b > n_b 时对块内任一边 e，取不在
//     同一环上的另一条边 g，可得到两个不同的过 e 的简单环（多篇题解同结论，见下）。
//   实现：Tarjan 用显式栈迭代（n 可达 1e4，避免深链递归爆栈）；边按对存储（2k, 2k+1），
//     用「父边编号 ^ 1」跳过回边；点双点数用时间戳数组 vmark 去重统计（不用 std::set，
//     省内存，内存限制仅 32 MB）；每组数据重置数组，内存 O(n + m)。
//
// 来源（题面同源原题 + 公开题解 AC 代码；标注「已实取正文」者为本次实际抓取并逐行核对）：
//   [0] 题面同源原题：HDU 3394 Railway  https://acm.hdu.edu.cn/showproblem.php?pid=3394
//       «已实取正文»：描述 roads/railways、输出 no need to build 与 clash、
//       样例 8 10 -> 1 5、n(0<n<=10000) m(0<=m<=100000) 无重边无自环、多组到 0 0 ——
//       与本目录 content.md 的输入/输出/样例/约束完全一致（原题来自 The 5th Guangting
//       Cup Central China Invitational Programming Contest, author momodi@whu）。
//   [1] 一本通官方 OJ 本题页：http://ybt.ssoier.cn:8088/problem_show.php?pid=1735
//       «已实取正文»：题名《环上计数》、时间 1000 ms / 内存 32768 KB、样例与数据规模，
//       与 content.md / config.json 一致（实测 242 提交 / 24 通过）。
//   [2] https://blog.csdn.net/qq_35577488/article/details/109677687
//       《HDU3394Railway-点双，结论》«已实取正文»：给出核心结论「点双中边数 > 点数
//       => 每条边至少处于两个简单环上」+ 点=边+1 / 点=边 / 点<边 三分讨论 + AC 代码。
//   [3] https://blog.csdn.net/u013480600/article/details/31770443
//       《HDU 3394 Railway(点双连通分量+桥)》«已实取正文»：桥计 ans1；
//       m_b > n_b 的块边数计 ans2（本标程结构与之一致）。
//   [4] https://blog.csdn.net/fsss_7/article/details/52950360 《hdu3394Railway》
//       «已实取正文»：同一结论（"一个点联通分量中边>点"）+ AC 代码。
//   [5] CSDN 站内搜索（接口 https://so.csdn.net/api/v3/search）以题面特征句
//       「不在任何一个简单环上」「至少两个简单环」检索：命中上述 [2][3][4] 及更多同题解，
//       未见一本通 1735 的独立题解；Bing/博客园检索亦未命中。
//   各来源结论相互一致，并以题面样例（8 10 -> 1 5）与 42 组手推闭式答案验证
//   （见 gen-report.md 的分层表与自检输出）。
//
// 本标程相对来源代码的改写点：来源多为链式前向星 + 递归（或近递归展开）实现，
// 本标程重写为「显式栈迭代 DFS + 边对编号（跳过父边用 ^1）+ 时间戳点去重（不用
// std::set，内存 32 MB 更稳）」并补齐多组数据重置；数组按上限 ×1.5 开。

#include <cstdio>
#include <cstring>

static const int MAXN = 15000;        // 题面上限 n <= 1e4，按 ×1.5 安全系数开
static const int MAXM = 150000;       // 题面上限 m <= 1e5，按 ×1.5 安全系数开（有向边 2*MAXM）

static int head[MAXN];                // 邻接表头（-1 表示空）
static int eto[2 * MAXM];             // 边对 2k / 2k+1：互为反向边
static int enxt[2 * MAXM];
static int dfn[MAXN], low[MAXN];
static int vmark[MAXN];               // 点双点数去重的时间戳
static int estack[2 * MAXM];          // 边栈（存有向边编号）
static int fu[MAXN], fe[MAXN], fit[MAXN];  // 迭代 DFS 的帧：点、入父边、当前邻接指针

int main() {
    int n, m;
    while (scanf("%d %d", &n, &m) == 2) {
        if (n == 0 && m == 0) break;

        int ec = 0;
        for (int i = 0; i < n; ++i) head[i] = -1;
        for (int i = 0; i < m; ++i) {
            int u, v;
            scanf("%d %d", &u, &v);
            eto[ec] = v; enxt[ec] = head[u]; head[u] = ec++;
            eto[ec] = u; enxt[ec] = head[v]; head[v] = ec++;
        }

        for (int i = 0; i < n; ++i) { dfn[i] = 0; vmark[i] = 0; }
        int timer = 0, stk = 0, ts = 0;
        long long ans1 = 0, ans2 = 0;   // ans2 为边数之和，最坏 1e5，long long 保险

        for (int s = 0; s < n; ++s) {
            if (dfn[s] || head[s] == -1) continue;   // 孤立点不构成块
            dfn[s] = low[s] = ++timer;
            int fm = 1;
            fu[0] = s; fe[0] = -1; fit[0] = head[s];

            while (fm > 0) {
                int idx = fm - 1;
                int u = fu[idx];
                int it = fit[idx];
                if (it != -1) {
                    fit[idx] = enxt[it];                 // 先推进游标
                    if (it == (fe[idx] ^ 1)) continue;   // 跳过父边（其反向边）
                    int v = eto[it];
                    if (!dfn[v]) {                       // 树边：压边后进入
                        estack[stk++] = it;
                        dfn[v] = low[v] = ++timer;
                        fu[fm] = v; fe[fm] = it; fit[fm] = head[v]; ++fm;
                    } else if (dfn[v] < dfn[u]) {        // 回边（只从较深端取一次）
                        estack[stk++] = it;
                        if (dfn[v] < low[u]) low[u] = dfn[v];
                    }
                } else {                                 // u 的邻接表走完
                    --fm;                                // 弹出 u（此时 idx == fm）
                    int pe = fe[idx];
                    if (fm > 0) {
                        int p = fu[fm - 1];
                        if (low[u] < low[p]) low[p] = low[u];
                        if (low[u] >= dfn[p]) {          // 找到一个点双（块）
                            if (low[u] > dfn[p]) ++ans1; // 桥
                            int ecnt = 0, vcnt = 0;
                            ++ts;
                            for (;;) {
                                int e = estack[--stk];
                                ++ecnt;
                                int a = eto[e ^ 1], b = eto[e];
                                if (vmark[a] != ts) { vmark[a] = ts; ++vcnt; }
                                if (vmark[b] != ts) { vmark[b] = ts; ++vcnt; }
                                if (e == pe) break;
                            }
                            if (ecnt > vcnt) ans2 += ecnt;   // 边数 > 点数 => 每条边 >= 2 环
                        }
                    }
                }
            }
        }
        printf("%lld %lld\n", ans1, ans2);
    }
    return 0;
}
