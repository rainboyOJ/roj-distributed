// 一本通 2123《图的存储与访问》标程（目标 ROJ 题号 2123）
//
// 题意：给出 N 个点、M 条边的有向图，K 次询问；每次询问给出 (X, Y)，求从点 X 出发能否
//       抵达点 Y。能抵达输出 Yes，否则输出 No（共 K 行）。
// 输入输出：stdin -> stdout。第 1 行 N M K；接下来 M 行，每行两个整数 U V 表示有向边
//       (U, V)（只有 U -> V 这一个方向；题面未禁止重边/自环，本实现自然支持）；
//       接下来 K 行，每行两个整数 X Y 表示询问。
//
// 参考来源（均已用 curl 实取正文逐行核对；本文件为**改写**实现，非盲抄）：
//   [1] 官方 OJ 页（题面 / 样例 / 限制 1000 ms / 65536 KB 的唯一权威口径）
//       http://ybt.ssoier.cn:8088/problem_show.php?pid=2123
//       —— 实测题面「对于 100% 的数据，1 <= N, M <= 10^3」；提交数 6942 / 通过数 2887。
//          题面**未声明** K 的上限（见 gen-report.md 风险点 2）。
//   [2] CSDN《2123：图的存储与访问》
//       https://blog.csdn.net/2301_81426214/article/details/148474054
//       —— 思路：连边时注意「这是有向图，只有从 Ui 到 Vi 这么一个方向」；对每个起点 st 调
//          一次 BFS 预处理 ok[st][v]（从 st 出发的可达节点），BFS 里先置 ok[st][st] = 1
//          （「每个节点可以到达自身」）；询问时查 ok[x][y] 为 1 输出 Yes，否则 No。
//          同文另有转载版（正文与该文逐字一致）：
//          https://blog.csdn.net/2301_82266829/article/details/155660886
//   [3] CSDN《图的存储与访问（信息学奥赛一本通- P2123）》
//       https://blog.csdn.net/sinat_39159613/article/details/156366955
//       —— 另一种落法：对**每次询问**从 x 出发 DFS（链式前向星邻接表），dfs(k) 一进门先判
//          k == y 则输出 Yes 并剪枝返回；每次询问清空 vis、起点先置 vis[x] = 1 防环，
//          搜完仍未到 y 输出 No。与 [2] 结论一致（有向、单向、x == y 判 Yes）。
//
// 本标程相对来源的改写点：
//   1. 采用 [2] 的「先对每个起点预处理可达集」思路（K 次询问 O(1) 回答，与 K 的大小无关，
//      比 [3] 的「每次询问重新 DFS」稳），但把实现换成 cstdio + 手写链式前向星 + 手写数组
//      队列，不用 <bits/stdc++.h>、不用 vector / queue，风格对齐 problems/1000/std.cpp；
//   2. 对每个起点都独立重跑 BFS（不能因为 reach[s][s] 已被别的起点标过就跳过该起点——
//      那样只会得到别的起点可达集的子集，是错的）；
//   3. 输入读取带返回值检查，并对越界下标做防御（题面保证点编号 1..N，越界属于非规格输入）
//      —— 空输入 / 截断输入不越界、不崩溃。
//
// 复杂度：时间 O(N * (N + M) + K)（传递闭包），空间 O(N^2 + N + M)。
//   N, M <= 10^3 时闭包部分约 2 * 10^6 次基本操作；顶格数据实测 < 5 ms（限制 1000 ms）。
//
// x == y 的语义说明（详见 gen-report.md 风险点 3）：本实现把「从 x 出发抵达 y」理解为路径长度
//   可为零，故 reach[x][x] 恒为 true（与来源 [2] 的 ok[st][st] = 1、来源 [3] 一进门判 k == y
//   完全一致，也是传递闭包/可达性的通行约定）。本包数据只在与「长度 >= 1」的读法结论一致的
//   情形下出现 x == y 的询问（即该点在自环上或处于环中），因此数据不依赖这处语义选择。

#include <cstdio>
#include <cstring>

static const int MAXN = 1005;   // 点数上限 10^3（题面「1 <= N, M <= 10^3」），留少量余量
static const int MAXM = 1005;   // 边数上限同上

static int head[MAXN];          // 链式前向星：head[u] 为 u 的第一条出边编号（0 表示无）
static int nxt[MAXM];           // 同起点的下一条出边编号
static int to[MAXM];            // 出边指向的点
static int ecnt;                // 已存边数

static bool reach[MAXN][MAXN];  // reach[s][v]：从 s 出发能否抵达 v（约 1 MB，远小于 64 MB）
static int que[MAXN];           // 手写 BFS 队列（每点最多入队一次）

static void addEdge(int u, int v) {
    ++ecnt;
    to[ecnt] = v;
    nxt[ecnt] = head[u];
    head[u] = ecnt;
}

int main() {
    int n, m, k;
    if (scanf("%d %d %d", &n, &m, &k) != 3) return 0;   // 空输入直接结束

    memset(head, 0, sizeof(head));
    ecnt = 0;
    for (int i = 0; i < m; ++i) {
        int u, v;
        if (scanf("%d %d", &u, &v) != 2) break;         // 截断输入：安全退出读边
        if (u < 1 || u > n || v < 1 || v > n) continue; // 防御：题面保证编号在 1..N
        if (ecnt >= MAXM) continue;                     // 防御：题面保证 M <= 10^3
        addEdge(u, v);                                  // 有向边，只存 u -> v 的方向
    }

    // 对每个起点 s 做一次 BFS，预处理「从 s 出发可达的点集」（起点可达自身，路径长度 0）
    for (int s = 1; s <= n; ++s) {
        int qh = 0, qt = 0;
        reach[s][s] = true;
        que[qt++] = s;
        while (qh < qt) {
            int u = que[qh++];
            for (int e = head[u]; e; e = nxt[e]) {
                int v = to[e];
                if (!reach[s][v]) {
                    reach[s][v] = true;
                    que[qt++] = v;
                }
            }
        }
    }

    for (int i = 0; i < k; ++i) {
        int x, y;
        if (scanf("%d %d", &x, &y) != 2) break;         // 截断输入：安全退出读询问
        printf("%s\n", (x >= 1 && x <= n && y >= 1 && y <= n && reach[x][y]) ? "Yes" : "No");
    }
    return 0;
}
