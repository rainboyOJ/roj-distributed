// 一本通 1792 小P的牧场 —— 标准解 (std)
// 来源依据：
//   本题与 BZOJ 3437「小P的牧场」同源（题面逐句一致，样例 4 / 2 4 2 4 / 3 1 4 2 -> 9 相同）。
//   参考题解：https://blog.csdn.net/anheku1562/article/details/101308524
//             （bzoj3437 小P的牧场，斜率优化 DP）
//   检索路径：CSDN 站内搜「小P的牧场」命中 bzoj3437 题解，据此确认同源并按经典斜率优化改写。
//
// 题意：n 个牧场自西向东排列。某些牧场建控制站（花费 a_i）。
//   一个控制站 i 控制“i 直到它西边第一个控制站（不含）”的所有牧场；
//   被控制牧场 k 的花费 = (控制它的控制站位置 - k) * b_k。求最小总花费。
//   （为使所有牧场被控制，最东边 n 必须建站，故答案为 f[n]。）
//
// DP：f[i] 表示在 i 建站、且 i 之前（含 i 自身覆盖范围）均处理完毕的最小花费，
//     规定 i 之前的所有牧场由“i 右边最近的控制站”控制。
//   f[i] = a_i + i*(S1[i]-S1[j]) - (S2[i]-S2[j]) + f[j]   （j 为 i 西边第一个控制站）
//   其中 S1[i]=sum b_k, S2[i]=sum k*b_k。
//   整理：f[i] = a_i + i*S1[i] - S2[i] + min_j ( f[j] + S2[j] - i*S1[j] )
//   令 Y[j]=f[j]+S2[j], X[j]=S1[j]（严格递增），查询斜率 i 单调递增 → 单调队列维护下凸壳。
//   复杂度 O(n)。
#include <cstdio>
#include <algorithm>
using namespace std;

typedef long long ll;
const int MAXN = 1000005;

int n;
ll a[MAXN], S1[MAXN], S2[MAXN], f[MAXN];
int q[MAXN];

// 快速读入
static inline ll readInt() {
    int c = getchar();
    while (c != '-' && (c < '0' || c > '9')) c = getchar();
    ll sgn = 1;
    if (c == '-') { sgn = -1; c = getchar(); }
    ll x = 0;
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = getchar(); }
    return sgn * x;
}

static inline ll Y(int j) { return f[j] + S2[j]; }
static inline ll X(int j) { return S1[j]; }

// 下凸壳：j<k<m，若 slope(j,k) >= slope(k,m) 则 k 无用（弹掉）
static inline bool bad(int j, int k, int m) {
    // (Y(k)-Y(j))/(X(k)-X(j)) >= (Y(m)-Y(k))/(X(m)-X(k))
    // 分母均 > 0（b_i > 0 故 S1 严格递增）
    return (Y(k) - Y(j)) * (X(m) - X(k)) >= (Y(m) - Y(k)) * (X(k) - X(j));
}

// 队首决策：若 k 优于 j（j<k）则弹出 j：Y(k)-Y(j) <= i*(X(k)-X(j))
static inline bool frontWorse(int j, int k, ll i) {
    return (Y(k) - Y(j)) <= i * (X(k) - X(j));
}

int main() {
    n = (int)readInt();
    for (int i = 1; i <= n; ++i) a[i] = readInt();
    for (int i = 1; i <= n; ++i) {
        ll b = readInt();
        S1[i] = S1[i - 1] + b;
        S2[i] = S2[i - 1] + b * i;
    }

    int head = 0, tail = 0;
    q[tail++] = 0;          // 虚拟起点：j=0，f[0]=S1[0]=S2[0]=0
    f[0] = 0;

    for (int i = 1; i <= n; ++i) {
        while (head + 1 < tail && frontWorse(q[head], q[head + 1], i)) ++head;
        int j = q[head];
        f[i] = f[j] + S2[j] - (ll)i * S1[j] + (ll)i * S1[i] - S2[i] + a[i];
        while (head + 1 < tail && bad(q[tail - 2], q[tail - 1], i)) --tail;
        q[tail++] = i;
    }

    printf("%lld\n", f[n]);
    return 0;
}
