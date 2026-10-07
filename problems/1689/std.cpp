// 一本通 1689 堆排问题
// 参考来源：未检索到公开 AC 代码（自研实现，正确性论证见 gen-report.md）。
// 参考题面：http://ybt.ssoier.cn:8088/problem_show.php?pid=1689
//
// 算法：状态压缩 BFS
//  - N <= 16，F_i 互不相同。把权值按"最大->0, 次大->1, ..."离散化，
//    用 uint64（4 bit/位）表示整棵树的权值排列状态。
//  - 大根堆性质：父结点权值 > 子结点权值，等价于父结点编码值 < 子结点编码值。
//    满足堆性质的排列不唯一，因此 BFS 每次取出状态就检查堆性质，
//    首次满足时的深度即最少交换次数。
//  - 转移为 M 种交换方式（同一方式可重复使用）。
//  - 复杂度：状态数 <= N!；visited 用 unordered_map。
#include <cstdio>
#include <cstring>
#include <vector>
#include <queue>
#include <unordered_map>
#include <algorithm>
using namespace std;

int N, M;
int fa[20];
int Fv[20];              // 权值 -> 0..N-1 的编码（最大权值编码为 0）
vector<int> ch[20];      // 每个结点的孩子
int eu[130], ev[130];

// 检查编码状态下的堆性质：父编码 < 子编码（父权值 > 子权值）
bool isHeap(uint64_t s) {
    for (int i = 1; i <= N; i++) {
        if (fa[i] == 0) continue;
        int pi = 4 * (fa[i] - 1), ci = 4 * (i - 1);
        if (((s >> pi) & 15ULL) > ((s >> ci) & 15ULL)) return false;
    }
    return true;
}

int main() {
    scanf("%d %d", &N, &M);
    for (int i = 1; i <= N; i++) scanf("%d", &fa[i]);
    for (int i = 1; i <= N; i++) scanf("%d", &Fv[i]);
    for (int i = 0; i < M; i++) scanf("%d %d", &eu[i], &ev[i]);

    // 权值离散化：最大权值 -> 0，最小 -> N-1
    {
        vector<pair<int,int>> a;
        for (int i = 1; i <= N; i++) a.push_back({Fv[i], i});
        sort(a.begin(), a.end());
        for (int r = 0; r < N; r++) Fv[a[r].second] = N - 1 - r;
    }

    uint64_t start = 0;
    for (int i = 1; i <= N; i++) start |= (uint64_t)Fv[i] << (4 * (i - 1));

    if (isHeap(start)) { printf("0\n"); return 0; }

    unordered_map<uint64_t, int> dist;
    dist.reserve(1 << 20);
    queue<uint64_t> q;
    dist[start] = 0;
    q.push(start);
    int ans = -1;
    while (!q.empty()) {
        uint64_t s = q.front(); q.pop();
        int d = dist[s];
        for (int i = 0; i < M; i++) {
            int u = eu[i], v = ev[i];
            int su = 4 * (u - 1), sv = 4 * (v - 1);
            uint64_t a = (s >> su) & 15ULL, b = (s >> sv) & 15ULL;
            uint64_t t = (s & ~(15ULL << su) & ~(15ULL << sv))
                       | (b << su) | (a << sv);
            if (isHeap(t)) { ans = d + 1; goto done; }
            if (!dist.count(t)) {
                dist[t] = d + 1;
                q.push(t);
            }
        }
    }
done:
    printf("%d\n", ans);
    return 0;
}
