// 一本通 1773《消息传递》标准程序 (std)
// ---------------------------------------------------------------------------
// 题意：给定一棵树（1 号点为国王/根，输入给出每个点的直接上级），
//       用 1 单位时间把消息告诉某一个人，之后每个单位时间内任意已收到消息
//       的人可把消息告诉其一个直接上级或直接下属。求消息传遍全树的最短时间，
//       以及所有能达到该最短时间的起点编号（升序）。
//
// 同源经典题：洛谷 P2018《消息传递》（题面文字一致）。
// 参考题解（C++ 代码，用于核对算法与 +1 语义）：
//   https://blog.csdn.net/weixin_34253539/article/details/94661196
//   （原文转载自 https://www.cnblogs.com/third2333/p/7098684.html）
//   该题解做法：对每个起点做一次树形 DP，dp[u]=max(排序后第 k 大 + k)，
//   答案 = min dp + 1。此做法 O(N^2)，仅适合 N<=1000 的原始数据。
//
// 本 std 采用等价的「换根 DP」把复杂度降到 O(N log N)，以适配本题 N<=200000：
//   记 D(u->v) = 删去边 (u,v) 后含 v 的分量、以 v 为起点把该分量全部告知
//               所需的时间（v 在时刻 0 已收到消息）。
//   递推：设 v 的邻居（除 u 外）对应值 D(v->w)，
//         按值降序排第 k 大者安排在第 k 个单位时间告知，
//         D(u->v) = max_k ( k + D(v->w)_sorted_desc[k] )，无邻居则为 0。
//   全局答案 ans(v) = 以 v 为起点、对其全部邻居套用同一公式（不删边）。
//   最终输出 min_v ans(v) + 1（+1 为最初告诉起点本人的 1 单位时间）
//   与所有达到最小值的 v。
//   两次遍历：先自底向上求 D(parent->child)（down），再自顶向下求
//   D(child->parent)（up），后者用前缀/后缀最值 O(deg) 处理「去掉某个儿子」。
// ---------------------------------------------------------------------------
#include <cstdio>
#include <vector>
#include <algorithm>
#include <climits>
#include <utility>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    vector<vector<int>> adj(n + 1);
    for (int i = 2; i <= n; i++) {
        int x;
        scanf("%d", &x);            // i 的直接上级
        adj[i].push_back(x);
        adj[x].push_back(i);
    }

    if (n == 1) {                  // 只有国王一人
        printf("1\n1\n");
        return 0;
    }

    // BFS 定根（根 = 1），得到 parent 与 BFS 序
    vector<int> parent(n + 1, 0), order;
    order.reserve(n);
    vector<char> vis(n + 1, 0);
    order.push_back(1);
    vis[1] = 1;
    for (size_t h = 0; h < order.size(); h++) {
        int u = order[h];
        for (int w : adj[u]) {
            if (!vis[w]) {
                vis[w] = 1;
                parent[w] = u;
                order.push_back(w);
            }
        }
    }

    vector<int> down(n + 1, 0), up(n + 1, 0), ans(n + 1, 0);
    vector<int> vals;

    // 第一遍：逆 BFS 序，求 down[v] = D(parent[v] -> v)（只含 v 的子树分量）
    for (int idx = n - 1; idx >= 0; idx--) {
        int v = order[idx];
        vals.clear();
        for (int w : adj[v])
            if (w != parent[v]) vals.push_back(down[w]);
        sort(vals.begin(), vals.end(), greater<int>());
        int T = 0;
        for (size_t k = 0; k < vals.size(); k++)
            T = max(T, (int)(k + 1) + vals[k]);
        down[v] = T;
    }

    // 第二遍：BFS 序，求每个点为起点的答案，并顺带求出 up[child] = D(child -> parent)
    vector<pair<int, int>> items;
    for (int idx = 0; idx < n; idx++) {
        int p = order[idx];
        items.clear();
        for (int w : adj[p]) {
            int val = (w == parent[p]) ? up[p] : down[w];
            items.push_back(make_pair(val, w));
        }
        sort(items.begin(), items.end(), [](const pair<int, int>& a, const pair<int, int>& b) {
            if (a.first != b.first) return a.first > b.first;
            return a.second < b.second;
        });
        int m = (int)items.size();
        vector<int> P(m + 1, 0), S(m + 2, 0);   // P[k]=max_{i<=k}(i+val_i)
        for (int k = 1; k <= m; k++)
            P[k] = max(P[k - 1], k + items[k - 1].first);
        for (int k = m; k >= 1; k--)            // S[k]=max_{i>=k}((i-1)+val_i)
            S[k] = max(S[k + 1], (k - 1) + items[k - 1].first);
        ans[p] = P[m];                          // 全部邻居参与
        for (int r = 1; r <= m; r++) {          // 去掉第 r 个邻居（只对儿子需要）
            int w = items[r - 1].second;
            if (w == parent[p]) continue;
            up[w] = max(P[r - 1], S[r + 1]);
        }
    }

    int mi = INT_MAX;
    for (int i = 1; i <= n; i++) mi = min(mi, ans[i]);
    printf("%d\n", mi + 1);
    bool first = true;
    for (int i = 1; i <= n; i++) {
        if (ans[i] == mi) {
            if (!first) printf(" ");
            printf("%d", i);
            first = false;
        }
    }
    printf("\n");
    return 0;
}
