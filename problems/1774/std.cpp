// 一本通 1774 《大逃杀》
//
// 来源（网络检索）：
//   博客园 · betablewaloot《1774：大逃杀》
//   https://www.cnblogs.com/betablewaloot/p/12247208.html
//   （检索路径：Brave 搜「一本通 1774 大逃杀」命中该博文；Bing/百度/CSDN/博客园站内搜索
//     均被反爬或索引缺失，故以该博文题解为依据，按其思路改写。）
//
// 依据（题面）：n,T<=300 的树，点 i 有资源 w_i（>=0，取到即得）与敌人耗时 t_i（>=0，
//   到达即必须花费，不能无视），边双向耗时 c，可从任意点空降，总时间 T，求结束时最大武力值。
//
// 算法（原文思路，树形背包）：定义三态（下标为“恰好用 j 时间”，值取 max）：
//   f[u][j]：从 u 出发，进入子树内并回到 u，最大收益（闭回路）；
//   g[u][j]：从 u 出发，进入子树内，终点为子树内任意点，最大收益（一条开口链）；
//   h[u][j]：从子树内任意点出发，经过 u，终点为子树内任意点，最大收益（u 为“最高点”，
//            两条开口链在此汇合）。
//   初值：若 t[u]<=T，f[u][t[u]]=g[u][t[u]]=h[u][t[u]]=w[u]。
//   合并儿子 v（边权 c）时做 0/1 背包，令 shen=j-k-c（再减去一次 c 表示往返），转移见代码。
//   答案 = 所有点的 f/g/h 在所有时间上的最大值。
//   （原文仅在“有儿子的点”的儿子合并循环里更新 ans，会漏掉单点最优；此处改为取遍所有点
//     与所有时间，语义更完整，且对样例与各特殊点结果不变。）
//
// 与独立推导的等价性：另一独立模型为「连通点集 S 的最小耗时 = Σt_i + 2E(S) - diam(S)」，
//   自研 DP 与该博文解法在样例及 t13=∞/w13=0/t13=0 等变体上结果一致，互为佐证。
#include <cstdio>
#include <algorithm>
using namespace std;

const int N = 305;
int f[N][N], g[N][N], h[N][N], last[N], sz, w[N], t[N], n, T, ans;
struct Edge { int dao, ne, quan; } a[N << 1];

void add(int x, int y, int z) {
    a[++sz].dao = y; a[sz].quan = z; a[sz].ne = last[x]; last[x] = sz;
}

// f: 下去了回来, g: 下去了不回来, h: 从下头来（经过 now）
void dfs(int now, int fa) {
    if (t[now] > T) return;          // 该点敌人耗时已超过总时间，无法到达，剪枝
    for (int i = last[now]; i; i = a[i].ne) {
        if (a[i].dao == fa) continue;
        dfs(a[i].dao, now);
        for (int j = T; j >= t[now]; j--) {
            for (int k = j - a[i].quan; k >= t[now]; k--) {
                int h1 = f[now][k], h2 = g[now][k], h3 = h[now][k]; // k: 此前用掉的时间
                int shen = j - k - a[i].quan;                        // 剩余给子树 v 的时间
                if (shen >= t[a[i].dao]) {
                    g[now][j] = max(g[now][j], h1 + g[a[i].dao][shen]);
                    h[now][j] = max(h[now][j], h2 + g[a[i].dao][shen]);
                }
                shen -= a[i].quan;                                   // 往返再减去一次边权
                if (shen >= t[a[i].dao]) {
                    g[now][j] = max(g[now][j], h2 + f[a[i].dao][shen]);
                    f[now][j] = max(f[now][j], f[a[i].dao][shen] + h1);
                    h[now][j] = max(h[now][j], h3 + f[a[i].dao][shen]);
                    h[now][j] = max(h[now][j], h[a[i].dao][shen] + h1);
                }
            }
        }
    }
}

int main() {
    if (scanf("%d %d", &n, &T) != 2) return 0;
    for (int i = 1; i <= n; i++) scanf("%d", &w[i]);
    for (int i = 1; i <= n; i++) {
        scanf("%d", &t[i]);
        if (t[i] <= T) f[i][t[i]] = g[i][t[i]] = h[i][t[i]] = w[i];
    }
    for (int i = 1, x, y, z; i <= n - 1; i++) {
        scanf("%d %d %d", &x, &y, &z);
        add(x, y, z); add(y, x, z);
    }
    dfs(1, 0);
    for (int u = 1; u <= n; u++)
        for (int j = 0; j <= T; j++)
            ans = max(ans, max(f[u][j], max(g[u][j], h[u][j])));
    printf("%d\n", ans);
    return 0;
}
