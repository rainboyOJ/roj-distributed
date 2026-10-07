// 一本通 1707《敲键盘》标程（C++17）
// ---------------------------------------------------------------------------
// 算法：AC 自动机 + 模意义高斯消元，求「首次出现任一模式串」时已输入字符数的期望。
//   设 X[u] = 从 AC 自动机状态 u（尚未命中任何模式串）出发，还需要输入的字符数期望。
//   对非终止态 u：X[u] = 1 + (1/26) * Σ_{c∈[a,z]} X[δ(u,c)]，其中 δ(u,c) 为终止态时该项取 0
//   （到达终止态即停止，不再继续输入）。两边乘 26 整理为
//       26*X[u] - Σ_{c: δ(u,c) 非终止} X[δ(u,c)] = 26
//   即线性方程组；对质数模 1e9+7 做高斯消元，答案 = X[root]。
//   终止态自身不设未知量（其「期望」按 0 参与方程），故矩阵规模 = 非终止状态数 ≤ 1+Σ|S_i| ≤ 151。
//
// 数据范围（题面【提示】）：1 ≤ T ≤ 50，1 ≤ n ≤ 15，|S_i| ≤ 10，字符集 = 26 个小写字母。
// 复杂度：O(T * 151^3)，实测顶格（T=50, n=15, |S_i|=10, 151 个状态）约 0.3s，远低于 2000ms。
//
// 来源情况（如实记录）：
//   1) 本题无公开题解/AC 代码：CSDN 站内搜索「一本通 1707 题解」「一本通 1707 敲键盘」
//      （https://so.csdn.net/api/v3/search?q=一本通 1707 题解）仅命中一本通高手训练题解目录页
//      https://blog.csdn.net/qq_36230375/article/details/136483654
//      （确认 1707《敲键盘》属「高手(二) 字符串算法 · 第4章 AC自动机」，目录无题解正文）；
//      Bing 检索同样无本题解法正文。故 std 为按题面自研推导实现（等价经典题的解法思路作参考）。
//   2) 同型经典题（约束、模数与本题完全一致，本题即其移植版本）：
//      「Magic boy Bi Luo with his excited string problem」(HDU 5836 / ifrog 1025)：
//      给出 ≤15 个长度 ≤10 的小写字母串，每次等概率写一个字母，写到出现任一给定串为止，
//      求已写长度的期望 mod 1e9+7。参考题解 URL：
//        - https://blog.csdn.net/kg20006/article/details/52561822
//          （AC自动机+期望DP+高斯消元；其中明写「≤15 个字母串、每串 ≤10、答案 mod 1e9+7」）
//        - https://blog.csdn.net/qwb492859377/article/details/52452508 （自动机+高斯消元 ifrog1025）
//        - https://blog.csdn.net/ra100fdm/article/details/118224001 （GYM103119B 期望+ACAM+高斯消元）
//      本文件按上述方程自行重写（高斯消元为自实现的模消元，未照抄参考代码），
//      并用独立的 Python Fraction 精确有理数消元对题面 4 个样例与自造小数据做过交叉验证
//      （见 gen-report.md 第 3 节）。
// ---------------------------------------------------------------------------

#include <cstdio>
#include <cstring>
#include <queue>
using namespace std;

typedef long long ll;
const ll MOD = 1000000007LL;
const int ALPHA = 26;
const int MAXNODE = 160; // 1 + 15*10 = 151，留裕量

int ch[MAXNODE][ALPHA];    // trie 儿子
int fail_[MAXNODE];
int go_[MAXNODE][ALPHA];   // 补全后的 DFA 转移（失配跳转）
bool term_[MAXNODE];       // 该状态后缀（含自身）是否命中某个模式串
int nodes;

static inline ll pw(ll b, ll e) {
    ll r = 1;
    b %= MOD;
    while (e) {
        if (e & 1) r = r * b % MOD;
        b = b * b % MOD;
        e >>= 1;
    }
    return r;
}

ll A[MAXNODE][MAXNODE + 1]; // 增广矩阵
ll x_[MAXNODE];
int idOf[MAXNODE];          // 自动机状态 -> 未知量下标（-1 = 终止态，不设未知量）
int nVar;

void resetState(int u) {
    memset(ch[u], 0, sizeof(ch[u]));
    fail_[u] = 0;
    term_[u] = false;
}

void buildTrie(int n) {
    nodes = 1;
    resetState(0);
    for (int i = 0; i < n; ++i) {
        static char s[32];
        scanf("%s", s);
        int u = 0;
        for (int j = 0; s[j]; ++j) {
            int c = s[j] - 'a';
            if (!ch[u][c]) {
                ch[u][c] = nodes;
                resetState(nodes);
                ++nodes;
            }
            u = ch[u][c];
        }
        term_[u] = true;
    }
    // BFS：求 fail，并补全 DFA 转移
    queue<int> q;
    for (int c = 0; c < ALPHA; ++c) {
        if (ch[0][c]) {
            int v = ch[0][c];
            fail_[v] = 0;
            go_[0][c] = v;
            q.push(v);
        } else {
            go_[0][c] = 0;
        }
    }
    while (!q.empty()) {
        int u = q.front(); q.pop();
        if (term_[fail_[u]]) term_[u] = true; // fail 链传播
        for (int c = 0; c < ALPHA; ++c) {
            if (ch[u][c]) {
                int v = ch[u][c];
                fail_[v] = go_[fail_[u]][c];
                go_[u][c] = v;
                q.push(v);
            } else {
                go_[u][c] = go_[fail_[u]][c];
            }
        }
    }
}

ll solve() {
    nVar = 0;
    for (int u = 0; u < nodes; ++u) idOf[u] = term_[u] ? -1 : nVar++;
    for (int i = 0; i < nVar; ++i) {
        for (int j = 0; j <= nVar; ++j) A[i][j] = 0;
        A[i][i] = 26;
        A[i][nVar] = 26;
    }
    for (int u = 0; u < nodes; ++u) {
        if (idOf[u] < 0) continue;
        int i = idOf[u];
        for (int c = 0; c < ALPHA; ++c) {
            int v = go_[u][c];
            if (idOf[v] >= 0) {
                A[i][idOf[v]] = (A[i][idOf[v]] - 1 + MOD) % MOD;
            }
        }
    }
    // 前向消元
    for (int col = 0; col < nVar; ++col) {
        int piv = -1;
        for (int r = col; r < nVar; ++r)
            if (A[r][col]) { piv = r; break; }
        if (piv < 0) continue;
        if (piv != col)
            for (int j = col; j <= nVar; ++j) { ll t = A[col][j]; A[col][j] = A[piv][j]; A[piv][j] = t; }
        ll inv = pw(A[col][col], MOD - 2);
        for (int r = col + 1; r < nVar; ++r) {
            if (!A[r][col]) continue;
            ll f = A[r][col] * inv % MOD;
            for (int j = col; j <= nVar; ++j) {
                A[r][j] = (A[r][j] - f * A[col][j]) % MOD;
                if (A[r][j] < 0) A[r][j] += MOD;
            }
        }
    }
    // 回代
    for (int i = nVar - 1; i >= 0; --i) {
        ll s = A[i][nVar];
        for (int j = i + 1; j < nVar; ++j) {
            if (A[i][j]) s = (s - A[i][j] * x_[j]) % MOD;
        }
        s %= MOD; if (s < 0) s += MOD;
        x_[i] = s * pw(A[i][i], MOD - 2) % MOD;
    }
    return x_[idOf[0]];
}

int main() {
    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T--) {
        int n;
        if (scanf("%d", &n) != 1) break;
        buildTrie(n);
        printf("%lld\n", solve());
    }
    return 0;
}
