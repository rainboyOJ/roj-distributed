// 一本通 1705《DNA序列》标程
// 算法：AC 自动机（所有禁止子串建 Trie + fail 指针）建 DFA，
//       在自动机的"安全状态"上构造转移矩阵，矩阵快速幂求长度为 n 的合法串个数，模 100000。
// 本题数据范围与 POJ 2778 DNA Sequence 完全一致（m<=10, n<=2e9, |s|<=10, 字符集 ACTG, 模 100000），
// 属同一题目的移植版本，思路与经典解法（AC 自动机 + 矩阵快速幂）一致。
// 参考来源（思路与实现风格参考，代码为本人按题面重写并自行验证）：
//   - POJ 2778 题解（AC自动机+矩阵乘法）：https://blog.csdn.net/haut_ykc/article/details/77007786
//   - POJ 2778 题解（AC自动机+dp）：https://blog.csdn.net/siofive/article/details/38693883
// 说明：未找到一本通 1705 的现成公开 AC 代码；按同型经典题 POJ 2778 改写，
//       样例与 >=100 组随机对拍（与暴力对照）均通过（见 gen-report.md）。

#include <cstdio>
#include <cstring>
#include <queue>
#include <string>
#include <vector>
using namespace std;

typedef long long ll;
const ll MOD = 100000;
const int ALPHA = 4;
const int MAXNODE = 205; // m<=10, |s|<=10 => 最多 1+100 个节点，留裕量

int ch[MAXNODE][ALPHA];      // Trie 转移（build 后即 DFA goto 表）
int fail_[MAXNODE];          // fail 指针
bool danger[MAXNODE];        // 该状态的后缀（含自身）是否出现禁止子串
int n_nodes;

int c2i(char c) {
    switch (c) {
        case 'A': return 0;
        case 'C': return 1;
        case 'T': return 2;
        case 'G': return 3;
    }
    return -1;
}

int m;
ll n;

// 矩阵：size x size，元素模 MOD
struct Mat {
    int sz;
    ll a[MAXNODE][MAXNODE];
    Mat() { sz = 0; memset(a, 0, sizeof(a)); }
};

Mat mul(const Mat &x, const Mat &y) {
    Mat r;
    r.sz = x.sz;
    for (int i = 0; i < x.sz; i++)
        for (int k = 0; k < x.sz; k++) {
            if (!x.a[i][k]) continue;
            ll v = x.a[i][k];
            for (int j = 0; j < y.sz; j++)
                r.a[i][j] = (r.a[i][j] + v * y.a[k][j]) % MOD;
        }
    return r;
}

int main() {
    if (scanf("%d %lld", &m, &n) != 2) return 0;

    n_nodes = 1; // 节点 0 为根
    memset(ch[0], 0, sizeof(ch[0]));
    memset(danger, 0, sizeof(danger));

    vector<string> pats;
    for (int i = 0; i < m; i++) {
        char buf[64];
        if (scanf("%63s", buf) != 1) buf[0] = 0;
        string s(buf);
        pats.push_back(s);
        int cur = 0;
        for (size_t j = 0; j < s.size(); j++) {
            int v = c2i(s[j]);
            if (v < 0) continue; // 非法字符忽略（题面保证仅 ACTG）
            if (!ch[cur][v]) {
                ch[cur][v] = n_nodes;
                memset(ch[n_nodes], 0, sizeof(ch[n_nodes]));
                n_nodes++;
            }
            cur = ch[cur][v];
        }
        danger[cur] = true;
    }

    // BFS 建 fail 指针；沿 fail 继承 danger 标记（后缀包含禁止串）
    queue<int> q;
    fail_[0] = 0;
    for (int c = 0; c < ALPHA; c++) {
        int v = ch[0][c];
        if (v) {
            fail_[v] = 0;
            q.push(v);
        }
    }
    while (!q.empty()) {
        int u = q.front(); q.pop();
        if (danger[fail_[u]]) danger[u] = true;
        for (int c = 0; c < ALPHA; c++) {
            int &v = ch[u][c];
            if (v) {
                fail_[v] = ch[fail_[u]][c];
                q.push(v);
            } else {
                v = ch[fail_[u]][c];
            }
        }
    }

    // 安全状态：danger=false 的状态（不含任何禁止子串的后缀）
    // 转移矩阵 M[u][v] += 1 当且仅当 u 安全且从 u 经一个字符到达 v 且 v 安全
    int S = n_nodes;
    vector<int> id(S, -1); // 原状态 -> 压缩编号
    int K = 0;
    for (int u = 0; u < S; u++)
        if (!danger[u]) id[u] = K++;

    Mat M;
    M.sz = K;
    for (int u = 0; u < S; u++) {
        if (danger[u]) continue;
        for (int c = 0; c < ALPHA; c++) {
            int v = ch[u][c];
            if (!danger[v]) M.a[id[u]][id[v]]++;
        }
    }

    // 答案 = (M^n)[0][*] 之和（0 为起始状态，且根必安全：空串不含任何非空禁止子串）
    if (K == 0) { printf("0\n"); return 0; }

    Mat res;
    res.sz = K;
    for (int i = 0; i < K; i++) res.a[i][i] = 1; // 单位矩阵
    ll e = n;
    while (e) {
        if (e & 1) res = mul(res, M);
        M = mul(M, M);
        e >>= 1;
    }
    ll ans = 0;
    for (int j = 0; j < K; j++) ans = (ans + res.a[id[0]][j]) % MOD;
    printf("%lld\n", ans);
    return 0;
}
