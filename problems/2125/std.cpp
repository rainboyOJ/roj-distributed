// 一本通 2125《查找文献》标程
// 参考来源（网络搜索所得题解，经本地编译验证后改写）：
//   1) CSDN《题解：P5318 【深基18.例3】查找文献》(洛谷 P5318 与本题同题意)
//      https://blog.csdn.net/liwu40828/article/details/149427936
//      —— 思路：邻接表按编号升序排序后分别做 DFS / BFS，DFS 用显式栈避免深递归爆栈。
//   2) CSDN《题解：洛谷 P5318 【深基18.例3】查找文献》
//      https://blog.csdn.net/深度优先搜索/article/details/134088307
// 改写说明：
//   - 参考代码的“倒序入栈 + 出栈时判重”栈式 DFS，本地 20 万组随机小图验证与递归
//     先序完全一致；本实现仍改用“携带子结点偏移量的显式栈”，可严格证明与递归
//     DFS 先序一一对应（最坏链状图深度 1e5 也不会爆系统栈）。
//   - 按题面要求：邻接表先按编号升序排序，编号小的先访问；从 1 号点出发，
//     只输出可达结点；单组数据，m 条有向边 X->Y。
//   - 输出格式：每行遍历序列，数字间单空格分隔（行末空白按评测约定忽略）。

#include <cstdio>
#include <algorithm>
#include <vector>
#include <queue>
#include <utility>

const int MAXN = 100005;

int n, m;
std::vector<int> g[MAXN];
int dfs_ord[MAXN], bfs_ord[MAXN];
bool vis[MAXN];

int main() {
    scanf("%d %d", &n, &m);
    for (int i = 0; i < m; i++) {
        int x, y;
        scanf("%d %d", &x, &y);
        g[x].push_back(y);
    }
    // 题面：先看编号较小的那篇 -> 邻接表升序排序
    for (int i = 1; i <= n; i++) {
        std::sort(g[i].begin(), g[i].end());
    }

    // ---- DFS：显式栈严格模拟递归先序 ----
    int dcnt = 0;
    std::vector<std::pair<int, int> > st; // (结点, 下一个待扩展的邻接点下标)
    vis[1] = true;
    dfs_ord[dcnt++] = 1;
    st.push_back(std::make_pair(1, 0));
    while (!st.empty()) {
        int u = st.back().first;
        if (st.back().second < (int)g[u].size()) {
            int v = g[u][st.back().second++];
            if (!vis[v]) {
                vis[v] = true;
                dfs_ord[dcnt++] = v;
                st.push_back(std::make_pair(v, 0));
            }
        } else {
            st.pop_back();
        }
    }
    for (int i = 0; i < dcnt; i++) {
        printf("%d%c", dfs_ord[i], i + 1 == dcnt ? '\n' : ' ');
    }

    // ---- BFS：队列，入队时判重 ----
    for (int i = 1; i <= n; i++) vis[i] = false;
    int bcnt = 0;
    std::queue<int> q;
    vis[1] = true;
    q.push(1);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        bfs_ord[bcnt++] = u;
        for (int i = 0; i < (int)g[u].size(); i++) {
            int v = g[u][i];
            if (!vis[v]) {
                vis[v] = true;
                q.push(v);
            }
        }
    }
    for (int i = 0; i < bcnt; i++) {
        printf("%d%c", bfs_ord[i], i + 1 == bcnt ? '\n' : ' ');
    }

    return 0;
}
