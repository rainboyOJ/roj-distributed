// std.cpp：矩形覆盖计数（静态）
// 离线扫描线 + 树状数组：
//   每个矩形 [l,r) x [d,u) 拆成两个事件：
//     x = l 处对 y 区间 [d,u) 加 1，x = r 处对 y 区间 [d,u) 减 1。
//   把询问点按 x 排序后与事件一起扫描，
//   树状数组维护 y 轴上的差分数组，单点前缀和就是该点被覆盖次数。
// 复杂度 O((N + M) log (N + M))。
#include <bits/stdc++.h>
using namespace std;

const int MAXEV = 400010; // 事件上限：2N 个矩形事件 + M 个询问
const int MAXY = 400010;  // y 离散化上限：2N 个端点 + M 个询问点

struct Event {
    int x;    // 事件发生的 x 坐标
    int kind; // 0 = 矩形事件，1 = 询问
    int w;    // 矩形事件的权值：x = l 处 +1，x = r 处 -1
    int l, r; // 矩形事件的 y 区间 [l, r)
    int y;    // 询问点的 y
    int id;   // 询问编号，按输入顺序输出
};

int n, m;
Event ev[MAXEV];
int ev_cnt;

int ys[MAXY]; // 所有 y 坐标（矩形端点 + 询问点），离散化用
int ys_cnt;

int ans[MAXEV]; // 每个询问的答案

// 按 x 升序；同 x 先处理矩形事件（x == l 时矩形已覆盖，x == r 时矩形不覆盖）
bool cmp_event(Event a, Event b) {
    if (a.x != b.x) return a.x < b.x;
    return a.kind < b.kind;
}

// ---- 树状数组：区间加（差分）+ 单点查询 ----
int bit[MAXY];
int bit_n;

void bit_add(int i, int v) {
    for (; i <= bit_n; i += i & -i) bit[i] += v;
}

// 前缀和：y 离散化坐标 <= i 的覆盖次数
int bit_sum(int i) {
    int s = 0;
    for (; i > 0; i -= i & -i) s += bit[i];
    return s;
}

// 离散化数组中第一个 >= v 的位置（1 起始）
int lower_id(int v) {
    return lower_bound(ys + 1, ys + ys_cnt + 1, v) - ys;
}

void add_event(int x, int w, int l, int r) {
    ev[ev_cnt].x = x;
    ev[ev_cnt].kind = 0;
    ev[ev_cnt].w = w;
    ev[ev_cnt].l = l;
    ev[ev_cnt].r = r;
    ev_cnt++;
}

void read_input() {
    scanf("%d %d", &n, &m);
    for (int i = 0; i < n; i++) {
        int l, d, r, u;
        scanf("%d %d %d %d", &l, &d, &r, &u);
        add_event(l, +1, d, u); // 进入矩形
        add_event(r, -1, d, u); // 离开矩形
        ys[++ys_cnt] = d;
        ys[++ys_cnt] = u;
    }
    for (int i = 0; i < m; i++) {
        int x, y;
        scanf("%d %d", &x, &y);
        ev[ev_cnt].x = x;
        ev[ev_cnt].kind = 1;
        ev[ev_cnt].y = y;
        ev[ev_cnt].id = i;
        ev_cnt++;
        ys[++ys_cnt] = y;
    }
}

void solve() {
    // y 坐标离散化
    sort(ys + 1, ys + ys_cnt + 1);
    ys_cnt = unique(ys + 1, ys + ys_cnt + 1) - (ys + 1);
    bit_n = ys_cnt;

    sort(ev, ev + ev_cnt, cmp_event);

    for (int i = 0; i < ev_cnt; i++) {
        if (ev[i].kind == 0) {
            // 矩形事件：y 区间 [l, r) 加 w（差分：两个端点打标记）
            bit_add(lower_id(ev[i].l), ev[i].w);
            bit_add(lower_id(ev[i].r), -ev[i].w);
        } else {
            // 询问：该点覆盖次数 = y 处的前缀和
            ans[ev[i].id] = bit_sum(lower_id(ev[i].y));
        }
    }
}

int main() {
    read_input();
    solve();
    for (int i = 0; i < m; i++) printf("%d\n", ans[i]);
    return 0;
}
