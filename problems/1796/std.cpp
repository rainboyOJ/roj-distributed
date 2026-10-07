// 一本通 1796《斐波那契串》 标准程序 (std)
// ---------------------------------------------------------------------------
// 题面（.ybt-import/staging/1796/content.md）：
//   S[0]="0", S[1]=? , S[i]=S[i-2]+S[i-1]（字符串连接）。
//   给定 N,M,P 与长度 M 的 0/1 串 T，求 T 在 S[N] 中的出现次数 mod P。
//
// 【题面笔误 / 样例为准】content.md 写 “S[1]="0"”，但若 S[0]=S[1]="0" 则所有 S[i]
//   全为 0，样例 T="101" 出现次数恒为 0，与样例输出 8 矛盾。
//   按样例反推，正确初值为 S[0]="0", S[1]="1"（本题即经典 Fibonacci word，
//   与 0-index 的 F[0]=0,F[1]=1 对应）。取 S[1]="1" 时 S[7]="101011010110110101101"
//   中 "101" 恰出现 8 次，与样例一致，故采用 S[1]="1"。
//   —— 见 gen-report.md「题面冲突」一节。
//
// 【算法】O(M + log N)
//   记 f[i] = T 在 S[i] 中的出现次数。S[i]=S[i-2]S[i-1]，故
//       f[i] = f[i-2] + f[i-1] + cross[i],
//   其中 cross[i] 为“跨越拼接缝”的出现次数：起点在 S[i-2] 内、终点在 S[i-1] 内，
//   只由 S[i-2] 末尾 M-1 个字符与 S[i-1] 开头 M-1 个字符决定。
//   长度 len(S[i]) 按斐波那契增长，取最小的 K 使 len(S[K]) >= M-1（K = O(log M)）。
//   于是对任意 j >= K，suffix_{M-1}(S[j]) 恒等于 suffix_{M-1}(S[K])（因为 S[j] 以 S[j-1] 结尾）；
//   而 prefix_{M-1}(S[j]) = prefix_{M-1}(S[j-2])（j>=K+2），故前缀按下标奇偶稳定成两个常量。
//   综合得：对 i >= K+3，cross[i] 只随 i 的奇偶取两个定值 cEven / cOdd。
//   于是把前 K+3 项直接构造字符串并统计，之后用 (f[i],f[i-1],1) 的两步转移矩阵
//        [2 1 cEven+cOdd]
//        [1 1 cOdd     ]
//        [0 0 1        ]
//   快速幂到 f[N]（mod P）。M=1 时 cross 恒为 0，退化为纯斐波那契计数，同样适用。
//
// 【来源 / 依据】未检索到本题公开题解（见 gen-report.md §来源），本程序为自研实现：
//   推导依据为“斐波那契串前后缀稳定 + 边界跨界计数 + 线性递推矩阵快速幂”这一经典套路；
//   正确性以题面样例（N=7,M=3,P=100,T="101" -> 8，且该点强制走矩阵快速幂分支）验证。
// ---------------------------------------------------------------------------
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;
typedef long long ll;
typedef __int128 lll;

static ll P;

// KMP 失配函数
static vector<int> prefixFunction(const string &s) {
    int n = (int)s.size();
    vector<int> pi(n, 0);
    for (int i = 1; i < n; i++) {
        int j = pi[i - 1];
        while (j > 0 && s[i] != s[j]) j = pi[j - 1];
        if (s[i] == s[j]) j++;
        pi[i] = j;
    }
    return pi;
}

// T 在 s 中的出现次数（允许重叠），O(|s|+|T|)
static ll countOcc(const string &s, const string &T) {
    int m = (int)T.size();
    if (m == 0 || (int)s.size() < m) return 0;
    vector<int> pi = prefixFunction(T);
    ll c = 0;
    int j = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        while (j > 0 && s[i] != T[j]) j = pi[j - 1];
        if (s[i] == T[j]) j++;
        if (j == m) { c++; j = pi[j - 1]; }
    }
    return c;
}

// 跨越拼接缝的出现次数：
//   左块末尾 M-1 字符为 tail，右块开头 M-1 字符为 head；
//   计数 k∈[1,M-1] 使 T[0,k) == tail 的后 k 字符 且 T[k,M) == head 的前 M-k 字符。
// 用两次 KMP 求 border 链，O(M)。
static ll crossOcc(const string &tail, const string &head, const string &T) {
    int M = (int)T.size();
    if (M <= 1) return 0;
    vector<char> A(M, 0), B(M, 0); // A[k]: T 前 k 字符是 tail 后缀；B[k]: T 后 M-k 字符是 head 前缀

    // U = T + '#' + tail，border 链给出所有 k 使 T[0,k) 为 tail 后缀
    {
        string U = T + "#" + tail;
        vector<int> pi = prefixFunction(U);
        int k = pi[(int)U.size() - 1];
        while (k > 0) { if (k < M) A[k] = 1; k = pi[k - 1]; }
    }
    // V = head + '#' + T，border 链给出所有 j 使 head 前 j 字符 == T 后 j 字符，令 k = M-j
    {
        string V = head + "#" + T;
        vector<int> pi = prefixFunction(V);
        int j = pi[(int)V.size() - 1];
        while (j > 0) {
            int k = M - j;
            if (k >= 1 && k <= M - 1) B[k] = 1;
            j = pi[j - 1];
        }
    }
    ll c = 0;
    for (int k = 1; k <= M - 1; k++) if (A[k] && B[k]) c++;
    return c;
}

struct Mat { ll a[3][3]; };

static Mat mul(const Mat &x, const Mat &y) {
    Mat r;
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++) {
            lll s = 0;
            for (int k = 0; k < 3; k++) s += (lll)x.a[i][k] * y.a[k][j];
            r.a[i][j] = (ll)(s % P);
        }
    return r;
}

static Mat matPow(Mat b, ll e) {
    Mat r;
    for (int i = 0; i < 3; i++) for (int j = 0; j < 3; j++) r.a[i][j] = (i == j);
    while (e > 0) {
        if (e & 1) r = mul(r, b);
        b = mul(b, b);
        e >>= 1;
    }
    return r;
}

int main() {
    ll N;
    int M;
    if (!(cin >> N >> M >> P)) return 0;
    string T;
    cin >> T;

    // 构造 S[0..]，直到找到最小 K 使 |S[K]| >= M-1（且不超过 N）
    vector<string> S;
    S.push_back("0"); // S[0]
    S.push_back("1"); // S[1]（按样例修正，见头注）
    int K = -1;
    if ((int)S[0].size() >= M - 1) K = 0;
    else if ((int)S[1].size() >= M - 1) K = 1;
    while (K == -1 && (ll)(S.size() - 1) < N) {
        int c = (int)S.size() - 1;
        S.push_back(S[c - 1] + S[c]);
        if ((int)S.back().size() >= M - 1) K = c + 1;
    }
    if (K == -1) { // |S[N]| < M-1 < M，必无出现
        cout << 0 << "\n";
        return 0;
    }
    if ((ll)K >= N) { // 直接统计 S[N]
        cout << countOcc(S[N], T) % P << "\n";
        return 0;
    }

    // 需要字符串直到 min(N, K+3)（保证 cross 稳定性所需的 S[K+2],S[K+3] 齐备）
    ll need = min(N, (ll)K + 3);
    while ((ll)(S.size() - 1) < need) {
        int c = (int)S.size() - 1;
        S.push_back(S[c - 1] + S[c]);
    }
    int L = (int)need;

    vector<ll> f(L + 1);
    for (int i = 0; i <= L; i++) f[i] = countOcc(S[i], T) % P;

    if (N <= L) { cout << f[N] % P << "\n"; return 0; }

    // 稳定后的前后缀常量
    int tailLen = min(M - 1, (int)S[K].size());
    string sufK = S[K].substr(S[K].size() - tailLen);
    string prefEven, prefOdd;
    for (int idx = K + 2; idx <= K + 3; idx++) {
        int plen = min(M - 1, (int)S[idx].size());
        string p = S[idx].substr(0, plen);
        if (idx % 2 == 0) prefEven = p; else prefOdd = p;
    }
    // i 偶 => i-1 奇 => 右块前缀为奇下标常量；反之亦然
    ll cEven = crossOcc(sufK, prefOdd, T) % P;
    ll cOdd  = crossOcc(sufK, prefEven, T) % P;

    // 令 s 为偶数起点，已知 f[s], f[s-1]
    ll s;
    if (L % 2 == 0) {
        s = L;
    } else {
        ll cL1 = ((L + 1) % 2 == 0) ? cEven : cOdd;
        f.push_back((f[L] + f[L - 1] + cL1) % P);
        s = L + 1;
    }
    ll fe = f[s], fm = f[s - 1];

    Mat M2;
    M2.a[0][0] = (2) % P; M2.a[0][1] = (1) % P; M2.a[0][2] = (cEven + cOdd) % P;
    M2.a[1][0] = (1) % P; M2.a[1][1] = (1) % P; M2.a[1][2] = cOdd % P;
    M2.a[2][0] = 0;       M2.a[2][1] = 0;       M2.a[2][2] = 1 % P;

    ll m = N - s;
    ll k = m / 2;
    Mat R = matPow(M2, k);
    ll v0 = (ll)(((lll)R.a[0][0] * fe + (lll)R.a[0][1] * fm + R.a[0][2]) % P);
    ll v1 = (ll)(((lll)R.a[1][0] * fe + (lll)R.a[1][1] * fm + R.a[1][2]) % P);

    ll ans;
    if (m % 2 == 0) ans = v0;                       // f[s+2k] = f[N]
    else ans = (v0 + v1 + cOdd) % P;                // N 为奇：f[N]=f[N-1]+f[N-2]+cOdd
    ans = ((ans % P) + P) % P;
    cout << ans << "\n";
    return 0;
}
