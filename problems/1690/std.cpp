// 一本通 1690《棋盘问题》标程
// 本题与 POJ 3985 "Knight's Problem" 同题（题面、样例、数据范围一致）。
// 思路来源（改写自）：
//   CSDN Sure 《POJ 3985 Knight's Problem bfs + 剪枝》
//   https://blog.csdn.net/flying_stones_sure/article/details/8021446
// 思路：在无限棋盘上做 BFS。裸 BFS 状态过多，剪枝：一条最优路径总可以调整成
//   离「起点-终点连线」不超过单步最大长度 sqrt(D) 的路径，因此只把满足该条件的
//   点入队（另保留起点/终点附近半径 sqrt(D) 的球内点，避免退化）。手写开散列判重。
// 数据范围：T<20，坐标 [-5000,5000]，n<=10，1<=x,y<=10（向量分量非负）。
#include <cstdio>
#include <cstring>
#include <queue>
#include <algorithm>
using namespace std;

typedef long long ll;

static inline ll Sqr(ll x) { return x * x; }

// 剪枝后最坏状态量约 (dx+dy)*sqrt(2)*2*sqrt(D)，D<=200，约 40 万；开大到 100 万留足余量。
const int MAXM = 1000000;
const int PRIME = 999983;

struct Edge {
    int x, y, nxt;
};
Edge edge[MAXM];
int head[PRIME];
int idx;

int vecx[12], vecy[12];
int n;
int sx, sy, tx, ty;
ll D;      // max |v|^2，即单步最大长度的平方
ll A, B, C; // 起点-终点连线 Ax + By + C = 0

static inline void init_hash() {
    memset(head, -1, sizeof(head));
    idx = 0;
}

static inline int hash_xy(int x, int y) {
    ll h = ((ll)x << 16) ^ (ll)y;
    h %= PRIME;
    if (h < 0) h += PRIME;
    return (int)h;
}

static inline bool try_add(int x, int y) {
    int h = hash_xy(x, y);
    for (int e = head[h]; e != -1; e = edge[e].nxt) {
        if (edge[e].x == x && edge[e].y == y) return false;
    }
    edge[idx] = {x, y, head[h]};
    head[h] = idx++;
    return true;
}

static inline bool valid(int x, int y) {
    // 起点/终点附近保留一个半径 sqrt(D) 的球，处理极端情况。
    if (Sqr((ll)x - sx) + Sqr((ll)y - sy) <= D) return true;
    if (Sqr((ll)x - tx) + Sqr((ll)y - ty) <= D) return true;
    // 投影必须落在「起点-终点」线段内（不越过头尾）。
    if ((ll)(tx - sx) * (x - sx) + (ll)(ty - sy) * (y - sy) < 0) return false;
    if ((ll)(sx - tx) * (x - tx) + (ll)(sy - ty) * (y - ty) < 0) return false;
    // 到连线的距离平方 <= D。
    if (Sqr(A * (ll)x + B * (ll)y + C) <= D * (Sqr(A) + Sqr(B))) return true;
    return false;
}

struct Node {
    int x, y, step;
};

static int bfs() {
    queue<Node> q;
    q.push({sx, sy, 0});
    try_add(sx, sy);
    while (!q.empty()) {
        Node cur = q.front();
        q.pop();
        if (cur.x == tx && cur.y == ty) return cur.step;
        for (int i = 0; i < n; i++) {
            int xx = cur.x + vecx[i];
            int yy = cur.y + vecy[i];
            if (valid(xx, yy) && try_add(xx, yy)) {
                q.push({xx, yy, cur.step + 1});
            }
        }
    }
    return -1;
}

int main() {
    int T;
    scanf("%d", &T);
    while (T--) {
        scanf("%d %d %d %d", &sx, &sy, &tx, &ty);
        scanf("%d", &n);
        D = 0;
        bool all_non_neg = true;
        for (int i = 0; i < n; i++) {
            scanf("%d %d", &vecx[i], &vecy[i]);
            D = max(D, Sqr(vecx[i]) + Sqr(vecy[i]));
            if (vecx[i] < 0 || vecy[i] < 0) all_non_neg = false;
        }
        A = (ll)ty - sy;
        B = (ll)sx - tx;
        C = (ll)sy * tx - (ll)sx * ty;

        // 向量分量全非负时，目标在起点左/下方必然不可达，可快速判掉。
        if (all_non_neg && (tx < sx || ty < sy)) {
            puts("IMPOSSIBLE");
            continue;
        }

        init_hash();
        int ans = bfs();
        if (ans < 0) puts("IMPOSSIBLE");
        else printf("%d\n", ans);
    }
    return 0;
}
