// 一本通 1708《无限链计数》标程（C++17）
// 来源：https://www.cnblogs.com/betablewaloot/p/12158505.html （博客园 AC 代码，已改编重写）
// 思路：建禁止串 AC 自动机，取非终止结点间的转移图。
//   1) Tarjan 缩 SCC：某 SCC 内部边数 > 点数（非简单环）→ -1；
//      内部边数 == 点数 → 该 SCC 是一个「环」（panh=1）。
//   2) DAG 上拓扑 DP 数「以环开头、以环结尾」的路径数：
//      路径上环数 ≥3 → -1；答案 = 所有环 SCC 的路径计数之和。
#include <cstdio>
#include <cstring>
#include <queue>
#include <algorithm>
using namespace std;

const int N = 10005;
const int E = 60005;

int t, m, cnt = 0;
int er[N][6], fail[N];
bool pan[N]; // 终止（含 fail 传递）

int dfn[N], low[N], timer = 0, st[N], top = 0;
bool instk[N], book[N];
int sccOf[N], siz = 0, dian[N], bian[N], panh[N];

// 邻接表1：原图（非终止转移）
int head1[N], size1;
struct Edge { int to, ne; } aa[E];
void add1(int x, int y) { aa[++size1] = {y, head1[x]}; head1[x] = size1; }
// 邻接表2：SCC 缩点图
int head2[N], size2, ru[N];
struct Edge2 { int to, ne; } b[E];
void add2(int x, int y) { b[++size2] = {y, head2[x]}; head2[x] = size2; ru[y]++; }

char c[15];

void insert() {
    int len = (int)strlen(c), now = 0;
    for (int i = 0; i < len; i++) {
        int idx = c[i] - 'a';
        if (!er[now][idx]) er[now][idx] = ++cnt;
        now = er[now][idx];
    }
    pan[now] = true;
}

void get_fail() {
    static queue<int> que;
    for (int i = 0; i < t; i++)
        if (er[0][i]) que.push(er[0][i]);
    while (!que.empty()) {
        int now = que.front(); que.pop();
        pan[now] |= pan[fail[now]];
        for (int i = 0; i < t; i++) {
            if (er[now][i]) {
                fail[er[now][i]] = er[fail[now]][i];
                que.push(er[now][i]);
            } else {
                er[now][i] = er[fail[now]][i];
            }
        }
    }
}

void tarjan(int now) {
    dfn[now] = low[now] = ++timer;
    st[++top] = now; instk[now] = true;
    for (int i = head1[now]; i; i = aa[i].ne) {
        int v = aa[i].to;
        if (!dfn[v]) {
            tarjan(v);
            low[now] = min(low[now], low[v]);
        } else if (instk[v]) {
            low[now] = min(low[now], dfn[v]);
        }
    }
    if (low[now] == dfn[now]) {
        siz++;
        int k;
        do {
            k = st[top--];
            instk[k] = false;
            sccOf[k] = siz;
            dian[siz]++;
        } while (k != now);
    }
}

int main() {
    scanf("%d %d", &t, &m);
    for (int i = 0; i < m; i++) {
        scanf("%s", c);
        insert();
    }
    get_fail();
    // 建图：非终止结点、非终止转移
    for (int i = 0; i <= cnt; i++) {
        if (pan[i]) continue;
        for (int j = 0; j < t; j++) {
            if (pan[er[i][j]]) continue;
            add1(i, er[i][j]);
        }
    }
    for (int i = 0; i <= cnt; i++)
        if (!dfn[i] && !pan[i]) tarjan(i);
    // 缩点
    for (int i = 0; i <= cnt; i++) {
        if (pan[i]) continue;
        for (int e = head1[i]; e; e = aa[e].ne) {
            int v = aa[e].to;
            if (sccOf[i] != sccOf[v]) add2(sccOf[i], sccOf[v]);
            else bian[sccOf[i]]++;
        }
    }
    for (int i = 1; i <= siz; i++) {
        if (bian[i] > dian[i]) { printf("-1\n"); return 0; }
        if (bian[i] == dian[i]) panh[i] = 1; // 简单环
    }
    // 拓扑 DP
    static queue<int> que;
    static int f[N], ge[N];
    for (int i = 1; i <= siz; i++)
        if (ru[i] == 0) { que.push(i); ge[i] = panh[i]; }
    while (!que.empty()) {
        int now = que.front(); que.pop();
        if (ge[now] >= 3) { printf("-1\n"); return 0; }
        if (panh[now]) f[now]++;
        for (int e = head2[now]; e; e = b[e].ne) {
            int v = b[e].to;
            f[v] += f[now];
            ge[v] = max(ge[v], ge[now] + panh[v]);
            if (--ru[v] == 0) que.push(v);
        }
    }
    long long ans = 0;
    for (int i = 1; i <= siz; i++) if (panh[i]) ans += f[i];
    printf("%lld\n", ans);
    return 0;
}
