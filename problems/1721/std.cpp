// 一本通 1721《最小边权和》标程
//
// 题意：n 个点 m 条边的有向图，每条边权 w 互不相同；q 组询问 (a,b,c)：
//       求从 a 走到 b、恰好/至多经过不超过 c 条边、且路上边权非降序的最小边权和；
//       无解输出 -1。
// 数据范围：n<=150, m<=5000, q<=1000, w<=5000；time 1000ms / memory 512MB。
//
// 参考来源（联网检索命中，均为本题同源题面 + 同一解法，本机改写并做样例验证 + 对拍）：
//   1. https://blog.csdn.net/qq_34991215/article/details/100185826
//      《最小边权和 (带限制条件的最短路，动态规划)》——题面（含样例 8 9 3 / 17 6 -1、
//      数据范围 n<=150,m<=5000,q<=1000,w<=5000）与本题逐字一致，属同一道题（一本通 1721）。
//      做法：把边按 w 升序排序，f[i][j][k] = i 到 j 走不超过 k 条边且边权非降序的最小代价，
//      逐边松弛 f[i][v][j] = min(f[i][v][j], f[i][u][j-1] + w)，最后对 k 做前缀 min，
//      询问 O(1)（c 取 min(c,n)）。
//   2. https://blog.csdn.net/ronaldo7_zyb/article/details/106192135
//      《『毒瘤算法系列5』最小边权和(Bellman-ford式DP)》——同一模型与同一转移（把边
//      按权值从小到大插入，"插入顺序即行走顺序"）。
//   另有目录页 https://blog.csdn.net/qq_36230375/article/details/136483654
//      《信息学奥赛一本通高手训练 题解目录》（确认本题属高手训练篇图论章节）。
//
// 关键论证（本标程对来源实现的两点加固）：
//   * 排序后逐边 DP 的完备性：走路上边权非降序，且题面保证边权两两不同 => 走路用到的边在
//     "按 w 升序" 的插入顺序下恰与行走顺序一致，故每条可行走路都被 DP 枚举到。
//   * c 的截断：边权非负，去掉走路中的环（取子序列）后仍满足非降序且代价不增，故最小代价
//     一定可由简单路径取到，走路长度 <= n-1。因此 min(c,n) 是正确的询问上界（题面未给 c 上限）。
//   * 自环/平行边：DP 允许同一自环被连续多次使用（对应真实合法走路），不会低估；非自环情形
//     无别名问题。
//   * 等权加固（题面保证 w 互不相同，本标程额外兜底）：把同权边分组后对组内边做
//     min(|group|,n) 轮松弛（分层图上的 Bellman-Ford），使得即使出现等权边、需要按任意
//     顺序串接同权边时也不会漏解；权值互不相同时每组只有 1 条边，退化为来源实现。
//   * 判无解：INF = 0x3f3f3f3f，真实答案 <= 149*5000 = 745000，而"INF 污染值"最小也有 1e9，
//     故以 1e8 为阈值判 -1 是安全的。

#include <cstdio>
#include <cstring>
#include <algorithm>
using namespace std;

namespace fastio {
static const int BUFSZ = 1 << 16;
static char buf[BUFSZ];
static int len = 0, pos = 0;
inline int gc() {
    if (pos == len) {
        len = (int)fread(buf, 1, BUFSZ, stdin);
        pos = 0;
        if (len <= 0) return -1;
    }
    return buf[pos++];
}
static inline int readInt() {
    int c = gc();
    while (c != -1 && (c < '0' || c > '9') && c != '-') c = gc();
    bool neg = false;
    if (c == '-') { neg = true; c = gc(); }
    int x = 0;
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = gc(); }
    return neg ? -x : x;
}
}  // namespace fastio

static const int MAXN = 150;
static const int MAXM = 5000;
static const int INF = 0x3f3f3f3f;
static const int JUNK_THRESHOLD = 100000000;  // 真实答案 <= 745000，超过即视为不可达

struct Edge {
    int u, v, w;
};
static Edge e[MAXM];

// f[i][j][k]：i 到 j，用不超过 k 条边、边权非降序的最小边权和
static int f[MAXN + 1][MAXN + 1][MAXN + 1];

int main() {
    using namespace fastio;
    int n = readInt(), m = readInt(), q = readInt();
    for (int i = 0; i < m; i++) {
        e[i].u = readInt();
        e[i].v = readInt();
        e[i].w = readInt();
    }
    // 按边权升序插入：插入顺序即"行走顺序"（题面保证 w 两两不同）
    sort(e, e + m, [](const Edge& x, const Edge& y) { return x.w < y.w; });

    memset(f, 0x3f, sizeof(f));
    for (int i = 1; i <= n; i++) f[i][i][0] = 0;  // 0 条边：自己到自己，代价 0

    // 逐边松弛；同权边（题面保证不出现，此处加固）整组多轮松弛
    for (int k = 0; k < m;) {
        int g = k;
        while (g < m && e[g].w == e[k].w) g++;
        int rounds = g - k;
        if (rounds > n) rounds = n;
        for (int r = 0; r < rounds; r++) {
            for (int t = k; t < g; t++) {
                const int u = e[t].u, v = e[t].v, w = e[t].w;
                for (int i = 1; i <= n; i++) {
                    int* fv = f[i][v];
                    const int* fu = f[i][u];
                    for (int j = 1; j <= n; j++) {
                        int cand = fu[j - 1] + w;
                        if (cand < fv[j]) fv[j] = cand;
                    }
                }
            }
        }
        k = g;
    }
    // 前缀 min：f[i][j][k] 表示"不超过 k 条边"
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++) {
            int* row = f[i][j];
            for (int k = 1; k <= n; k++)
                if (row[k - 1] < row[k]) row[k] = row[k - 1];
        }

    // 询问 O(1)
    static char out[1 << 16];
    int olen = 0;
    for (int t = 0; t < q; t++) {
        int a = readInt(), b = readInt(), c = readInt();
        if (c > n) c = n;   // 走路长度 <= n-1，截断不影响答案
        if (c < 0) c = 0;
        int ans = f[a][b][c];
        if (ans > JUNK_THRESHOLD) {
            out[olen++] = '-';
            out[olen++] = '1';
        } else {
            char tmp[16];
            int p = 0;
            if (ans == 0) tmp[p++] = '0';
            while (ans > 0) { tmp[p++] = char('0' + ans % 10); ans /= 10; }
            while (p > 0) out[olen++] = tmp[--p];
        }
        out[olen++] = '\n';
        if (olen > (1 << 15)) { fwrite(out, 1, olen, stdout); olen = 0; }
    }
    if (olen) fwrite(out, 1, olen, stdout);
    return 0;
}
