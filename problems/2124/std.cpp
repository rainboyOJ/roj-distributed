// 2124 图的遍历
// 题意：N 个点 M 条边的有向图，对每个点 v 求 A(v) = 从 v 出发能到达的编号最大的点。
//
// 参考来源（网络搜索所得 C++ 题解，思路改写如下）：
//   1) CSDN《洛谷 P3916 图的遍历(vector存图，反向建边，dfs)》
//      https://blog.csdn.net/yxrzibinanhai/article/details/107508649
//      思路：反向建边后，从编号最大的点 N 开始倒序遍历，沿途给未染色的点
//      打上"当前最大编号"的标记；被标记为 x 的点表示它在原图中能到达的最大点是 x。
//   2) 洛谷 P3916 图的遍历（与本题同一题面，反向建图 + DFS 是主流解法）
//      https://www.luogu.com.cn/problem/P3916
//   3) 一本通官方题面（用于核对输入输出格式与数据范围）
//      http://ybt.ssoier.cn:8088/problem_show.php?pid=2124
//
// 改写说明：参考代码为递归 DFS，N=1e5 的链状数据递归深度可达 1e5，可能爆系统栈；
// 此处改为显式栈的迭代 DFS，算法思路与参考来源一致。C++17。

#include <cstdio>
#include <vector>

const int MAXN = 100005;

std::vector<int> rg[MAXN]; // 反向图：原图边 (u,v) 存为 rg[v].push_back(u)
int ans[MAXN];

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    for (int i = 0; i < m; ++i) {
        int u, v;
        scanf("%d %d", &u, &v);
        rg[v].push_back(u); // 反向建边
    }
    std::vector<int> stk;
    for (int v = n; v >= 1; --v) {
        if (ans[v]) continue;   // 已被更大的编号染色
        ans[v] = v;
        stk.push_back(v);
        while (!stk.empty()) {
            int x = stk.back();
            stk.pop_back();
            for (size_t i = 0; i < rg[x].size(); ++i) {
                int y = rg[x][i];
                if (!ans[y]) {
                    ans[y] = v;
                    stk.push_back(y);
                }
            }
        }
    }
    for (int i = 1; i <= n; ++i)
        printf("%d%c", ans[i], i == n ? '\n' : ' ');
    return 0;
}
