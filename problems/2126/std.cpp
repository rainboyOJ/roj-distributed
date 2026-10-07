// 一本通 2126《[USACO19OPEN] Milk Factory》 标程
//
// 题意：N 个加工站（1..N，1<=N<=100）、N-1 条单向传送带；题面括号注明这些通道
//       「用最小数量连接所有站」 ⇒ 无向结构是一棵树。求**最小的** i，使得从其他
//       每个加工站出发都能沿有向边走（可经过中间站）到达 i；不存在则输出 -1。
//
// 参考来源（思路/改写依据，非盲抄；来源与题面冲突时以题面为准）：
//   [1] 【[USACO19OPEN] Milk Factory（信息学奥赛一本通- P2126）】
//       https://blog.csdn.net/sinat_39159613/article/details/156414552
//       （给出「逆向建图 + 从 1..N 逐个点做反图 DFS 计数、第一个能访问到全部 N 个点的
//         就是答案，全都不行输出 -1」的定义式做法，并指出反图的意义：原图 a->b 存成
//         反图 b->a，「谁能到我这」变成「我能反着走到谁」。本标程即按该定义式做法改写。）
//   [2] 【[USACO19OPEN] Milk Factory 题解：反向建图与出度判断解决有向图终点问题】
//       https://blog.csdn.net/weixin_30225755/article/details/165258937
//       （明确指出「唯一出度为 0 的点」只是一般有向图的**必要**条件，必须再从该点做
//         反图 DFS 验证能覆盖全部 N 个点；给出了「唯一出度为 0 的点却不可达」的反例
//         1->3, 2->1, 4->5, 5->4。本标程不依赖该必要条件，故对一般有向图也正确。）
//   [3] USACO 官方分析（Analysis by Brian Dean）
//       https://usaco.org/current/data/sol_factory_bronze_open19.html
//       （官方代码：无向结构是树时「答案 = 唯一出度为 0 的点，否则 -1」；该页同时给出
//         题面保证 N-1 条边构成树，官方对 N=1 输出 1。）
//   [4] 【[USACO19OPEN] Milk Factory B（洛谷 P1700）参考代码】
//       https://blog.csdn.net/rogeliu/article/details/143645256
//       （链式前向星反向建图 + 逐点枚举 DFS，同样收敛于同一做法。）
//   交叉核对：上述 4 份来源与 USACO 官方题面（cpid=940）、一本通题面 content.md
//   在「答案定义 / 输出 -1 / 输出最小 i」上完全一致，未发现冲突。
//
// 算法（定义式判定，严格按题面）：
//   反向建图 rev[b] = { a : 原图存在 a->b }。
//   枚举 i = 1..N（升序天然满足「最小」），在反图上从 i 做一次栈式 DFS，统计能到达 i
//   的点数（含 i 自身，空路径）；若达到 N，说明所有加工站都能到达 i，输出 i 并结束；
//   全部 i 都不满足则输出 -1。
//   复杂度 O(N*(N+M)) = O(N^2)（N<=100 时最坏约 100*199 次访问，远低于 1s）。
//   该做法**不依赖**「输入无向结构是树」这一保证，对任意有向图都严格符合题面定义，
//   比官方「唯一 sink ⟹ 答案」的写法更稳健（见 [2] 的反例）。
//
// 边界：N=1 时没有任何通道，「其他加工站」集合为空，条件真空成立，输出 1
//       （与官方分析代码一致；见 gen-report.md 风险点 2）。
// 输入：第一行 N，之后 N-1 行 a b（1<=a,b<=N，a!=b），空格分隔，stdin。
// 输出：一行，答案 i 或 -1，stdout。
#include <algorithm>
#include <cstdio>
#include <vector>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;  // 保证 1<=N<=100

    std::vector<std::vector<int> > rev(n + 1);  // 反图邻接表
    for (int i = 0; i < n - 1; ++i) {
        int a, b;
        scanf("%d %d", &a, &b);  // 传送带 a -> b，反图存 b -> a
        rev[b].push_back(a);
    }

    std::vector<int> vis(n + 1, 0), stk;
    stk.reserve(n);
    for (int i = 1; i <= n; ++i) {          // 升序枚举 ⇒ 首次命中即「最小的 i」
        std::fill(vis.begin(), vis.end(), 0);
        int cnt = 0;                        // 反图从 i 出发能访问到的点数
        stk.clear();
        stk.push_back(i);
        vis[i] = 1;
        while (!stk.empty()) {
            int u = stk.back();
            stk.pop_back();
            ++cnt;
            for (size_t k = 0; k < rev[u].size(); ++k) {
                int v = rev[u][k];
                if (!vis[v]) {
                    vis[v] = 1;
                    stk.push_back(v);
                }
            }
        }
        if (cnt == n) {                     // 所有加工站都能到达 i
            printf("%d\n", i);
            return 0;
        }
    }
    printf("-1\n");
    return 0;
}
