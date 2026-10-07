// 一本通 1687《积水问题》标程
//
// 题目等价于二维接雨水（LeetCode 407 Trapping Rain Water II）的推广：
// 外围是“无限大且高度为 0”的区域，因此每个格子的积水高度为：
//     water[i][j] = level[i][j] - h[i][j]
// 其中 level[i][j] 是“逃逸水位”：从 (i,j) 到外围的所有路径中，
// 路径上最大地形高度的最小值（minimax path）。外围视为高度 0 的虚拟点，
// 边界格子的逃逸水位为 max(h[i][j], 0)。
//
// 用多源 Dijkstra 求解 minimax：把所有边界格子以 max(h,0) 入堆，
// 每次弹出当前水位最小的格子，向四个方向松弛：
//     nd = max(curLevel, h[ni][nj])
// 若 nd 能降低邻居的水位则更新并入堆。最终 water = level - h。
//
// 参考来源：本题公开题解稀缺，算法思想改写自 LeetCode 407 Trapping Rain Water II
//   https://leetcode.com/problems/trapping-rain-water-ii/
// 以及洛谷 P1318 积水问题（一维）的二维推广思路。
// 已自行编译并通过题面样例验证。

#include <cstdio>
#include <queue>
#include <vector>
#include <algorithm>
using namespace std;

typedef long long ll;

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    if (n <= 0 || m <= 0) return 0; // 无格子，无输出

    vector<vector<ll>> h(n, vector<ll>(m));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j)
            scanf("%lld", &h[i][j]);

    const ll INF = (1LL << 62);
    vector<vector<ll>> level(n, vector<ll>(m, INF));
    vector<vector<char>> done(n, vector<char>(m, 0));

    // 小根堆： (水位, 格子编号 i*m+j)
    typedef pair<ll, int> Node;
    priority_queue<Node, vector<Node>, greater<Node>> pq;
    auto id = [&](int i, int j) { return i * m + j; };

    // 边界格子：逃逸水位为 max(h, 0)（外围高度为 0）
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            if (i == 0 || i == n - 1 || j == 0 || j == m - 1) {
                level[i][j] = max(h[i][j], 0LL);
                pq.push(make_pair(level[i][j], id(i, j)));
            }
        }
    }

    const int di[4] = {1, -1, 0, 0};
    const int dj[4] = {0, 0, 1, -1};

    while (!pq.empty()) {
        Node cur = pq.top();
        pq.pop();
        ll d = cur.first;
        int x = cur.second;
        int i = x / m, j = x % m;
        if (done[i][j]) continue;
        done[i][j] = 1;

        for (int k = 0; k < 4; ++k) {
            int ni = i + di[k], nj = j + dj[k];
            if (ni < 0 || ni >= n || nj < 0 || nj >= m) continue;
            if (done[ni][nj]) continue;
            ll nd = max(d, h[ni][nj]);
            if (nd < level[ni][nj]) {
                level[ni][nj] = nd;
                pq.push(make_pair(nd, id(ni, nj)));
            }
        }
    }

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            if (j) putchar(' ');
            printf("%lld", level[i][j] - h[i][j]);
        }
        putchar('\n');
    }
    return 0;
}
