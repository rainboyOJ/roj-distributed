/**
 * Author by Rainboy blog: https://rainboylv.com github: https://github.com/rainboylvx
 * rbook: -> https://rbook.roj.ac.cn  https://rbook2.roj.ac.cn
 * rainboy的学习导航网站: https://idx.roj.ac.cn
 * create_at: 2026-10-08 10:20
 * update_at: 2026-10-08 10:20
 */
// 3058《双栈排序》：冲突图 + 二分染色 + 贪心模拟，构造字典序最小的操作序列。
//
// 关键点：
//  1. 冲突条件：i < j 且 P_i < P_j 且存在 k > j 使 P_k < P_i  ⟺  两者不能同栈。
//     用后缀最小值 pre 与否：填 <=> minSuf[j+1] < P_i。
//  2. 冲突图不是二分图 ⟹ 输出 0。
//  3. 二分染色时，每个连通块里**下标最小**的点染成 1（S1），
//     这样能让 'a' 尽量靠前，得到字典序最小。
//  4. 模拟时按 a < b < c < d 的顺序贪心尝试；压栈需保持栈内自底向上递减。
//
// ⚠ 输入格式：**多组数据**
//     第一行 T（组数），随后 T 组，每组一行 n，一行 n 个数的排列。
//   （题库题面「输入格式」一节只写了「第一行是一个整数 n」，漏了 T —— 以数据为准。）
//
// 本文件同时作为 data/ 的生成器：cd data && ../std < twostackK.in > twostackK.out
#include <cstdio>
#include <cstring>
#include <queue>
#include <vector>

const int MAXN = 1005;

static int p[MAXN];
static int minSuf[MAXN];
static int color[MAXN];
static std::vector<int> adj[MAXN];
static int st1[MAXN], st2[MAXN];
static char ops[2 * MAXN + 5];

static int solveOne(int n) {
    for (int i = 1; i <= n; ++i) {
        adj[i].clear();
        color[i] = 0;
    }

    // 后缀最小值
    minSuf[n + 1] = 1 << 30;
    for (int i = n; i >= 1; --i)
        minSuf[i] = p[i] < minSuf[i + 1] ? p[i] : minSuf[i + 1];

    // 冲突图：i < j、P_i < P_j、且 j 之后还有比 P_i 小的
    for (int i = 1; i <= n; ++i)
        for (int j = i + 1; j <= n; ++j)
            if (p[i] < p[j] && minSuf[j + 1] < p[i]) {
                adj[i].push_back(j);
                adj[j].push_back(i);
            }

    // 二分染色；每个连通块下标最小的点染 1
    for (int s = 1; s <= n; ++s) {
        if (color[s]) continue;
        color[s] = 1;
        std::queue<int> q;
        q.push(s);
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (size_t t = 0; t < adj[u].size(); ++t) {
                int v = adj[u][t];
                if (color[v]) {
                    if (color[v] == color[u]) return 0;  // 非二分图
                } else {
                    color[v] = 3 - color[u];
                    q.push(v);
                }
            }
        }
    }

    // 贪心模拟：a < b < c < d
    int t1 = 0, t2 = 0, ptr = 1, want = 1, cnt = 0;
    while (want <= n) {
        if (ptr <= n && color[ptr] == 1 && (t1 == 0 || st1[t1] > p[ptr])) {
            st1[++t1] = p[ptr]; ops[cnt++] = 'a'; ++ptr;
        } else if (t1 && st1[t1] == want) {
            --t1; ops[cnt++] = 'b'; ++want;
        } else if (ptr <= n && color[ptr] == 2 && (t2 == 0 || st2[t2] > p[ptr])) {
            st2[++t2] = p[ptr]; ops[cnt++] = 'c'; ++ptr;
        } else if (t2 && st2[t2] == want) {
            --t2; ops[cnt++] = 'd'; ++want;
        } else {
            return 0;  // 理论上不可达
        }
    }
    ops[cnt] = '\0';
    return cnt;
}

int main() {
    int T;
    if (scanf("%d", &T) != 1) return 0;
    for (int tc = 0; tc < T; ++tc) {
        int n;
        if (scanf("%d", &n) != 1) break;
        for (int i = 1; i <= n; ++i) scanf("%d", &p[i]);
        int cnt = solveOne(n);
        if (cnt == 0) {
            printf("0\n");
        } else {
            for (int i = 0; i < cnt; ++i) printf("%c%c", ops[i], i + 1 == cnt ? '\n' : ' ');
        }
    }
    return 0;
}
