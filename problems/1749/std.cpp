// 一本通 1749《矩阵求和》标程 (C++17, stdin -> stdout)
//
// 来源情况（检索记录见 gen-report.md 第一节）：
//   题面特征句（"矩阵C由数组A，B生成"、公式 "C_ij=A_i*B_j+i*B_j+A_i*j+i*j"、
//   "F[k] 为矩阵C的所有大小为k*k的子矩阵的值的和"）在 博客园/CSDN/Bing 均未检索到
//   本题公开题解，故本标程为**自研**：由题面恒等变换化简 + 经典「所有长度子区间
//   最大值之和」单调栈技术（该子技术在 OI 中为通用技巧，非本题专有）。
//
// ---------------------------------------------------------------------------
// 推导
//   1) C_{ij} = A_i*B_j + i*B_j + A_i*j + i*j = (A_i + i) * (B_j + j)。
//      令 X_i = A_i + i，Y_j = B_j + j，则 C_{ij} = X_i * Y_j。
//   2) 数据范围 0 <= A_i,B_i <= 1e7 且 i,j >= 1，故 X_i,Y_j > 0，
//      于是 k*k 子矩阵（行窗 [i,i+k-1]、列窗 [j,j+k-1]）的最大值
//        = (max_{p in 行窗} X_p) * (max_{q in 列窗} Y_q)
//      （正数乘积取最大 = 两因子分别取最大），行与列互不影响。
//   3) 因此 F[k] = (sum_i 行窗长度 k 的 max X) * (sum_j 列窗长度 k 的 max Y)
//               = SX[k] * SY[k]，其中 S[k] = 数组所有长度 k 子区间最大值之和。
//
//   S[k] 的 O(n) 计算：
//     对每个位置 p，用单调栈求 L[p] = 左侧最近的「严格大于」X_p 的位置（无则 0），
//     R[p] = 右侧最近的「大于等于」X_p 的位置（无则 n+1）。
//     记 a = p - L[p]，b = R[p] - p。则 X_p 恰是区间 [s,e] 的「最右最大值」当且仅当
//     L[p] < s <= p <= e < R[p]（每个区间恰有一个这样的 p，互不重不漏）。
//     故 X_p 对长度 k 的贡献次数
//        cnt_p(k) = min(k, a, b, a+b-k)   (1 <= k <= a+b-1)，否则 0。
//     cnt_p 关于 k 分段线性：
//        k ∈ [1, m]       : cnt = k           (m = min(a,b))
//        k ∈ [m+1, M]     : cnt = m           (M = max(a,b))
//        k ∈ [M+1, a+b-1] : cnt = a+b-k
//     用两个差分数组 P、Q 做「区间加常数」，使 f(k) = (prefixP[k]) * k + prefixQ[k]，
//     最后前缀和一次即可得到所有 S[k]。（斜率 +1 段 -> 加 P；常数段 -> 加 Q；
//     斜率 -1 段 -> 同时加 Q 常数与 P 的 -X。）
//
//   复杂度 O(n)，空间 O(n)。n = 1e5 时远低于 1s / 128MB。
// ---------------------------------------------------------------------------
#include <cstdio>
#include <vector>
#include <algorithm>

using namespace std;

static const long long MOD = 1000000007LL;

// 返回 S[1..n]：数组 X 所有长度 k 的子区间最大值之和 (mod MOD)
static vector<long long> sumOfWindowMaxima(const vector<long long> &X, int n) {
    vector<int> L(n + 1), R(n + 1);
    vector<int> st;
    st.reserve(n + 1);

    // 左侧最近的严格大于 X[i]
    for (int i = 1; i <= n; ++i) {
        while (!st.empty() && X[st.back()] <= X[i]) st.pop_back();
        L[i] = st.empty() ? 0 : st.back();
        st.push_back(i);
    }
    st.clear();
    // 右侧最近的大于等于 X[i]
    for (int i = n; i >= 1; --i) {
        while (!st.empty() && X[st.back()] < X[i]) st.pop_back();
        R[i] = st.empty() ? n + 1 : st.back();
        st.push_back(i);
    }

    vector<long long> P(n + 3, 0), Q(n + 3, 0);  // 差分数组
    auto addP = [&](int l, int r, long long v) {
        if (l > r || v == 0) return;
        v %= MOD;
        P[l] = (P[l] + v) % MOD;
        P[r + 1] = (P[r + 1] - v + MOD) % MOD;
    };
    auto addQ = [&](int l, int r, long long v) {
        if (l > r || v == 0) return;
        v %= MOD;
        Q[l] = (Q[l] + v) % MOD;
        Q[r + 1] = (Q[r + 1] - v + MOD) % MOD;
    };

    for (int p = 1; p <= n; ++p) {
        long long x = X[p] % MOD;
        int a = p - L[p];
        int b = R[p] - p;
        int m = min(a, b), M = max(a, b);
        int len = a + b - 1;  // cnt_p(k) > 0 的最大 k
        addP(1, m, x);                                        // cnt = k
        addQ(m + 1, M, x * (m % MOD) % MOD);                  // cnt = m
        addQ(M + 1, len, x * ((long long)(a + b) % MOD) % MOD); // cnt = a+b-k
        addP(M + 1, len, (MOD - x) % MOD);
    }

    vector<long long> S(n + 1, 0);
    long long sp = 0, sq = 0;
    for (int k = 1; k <= n; ++k) {
        sp = (sp + P[k]) % MOD;
        sq = (sq + Q[k]) % MOD;
        S[k] = (sp * (long long)(k % MOD) + sq) % MOD;
    }
    return S;
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<long long> A(n + 1), B(n + 1), X(n + 1), Y(n + 1);
    for (int i = 1; i <= n; ++i) {
        if (scanf("%lld", &A[i]) != 1) return 0;
        X[i] = A[i] + i;
    }
    for (int i = 1; i <= n; ++i) {
        if (scanf("%lld", &B[i]) != 1) return 0;
        Y[i] = B[i] + i;
    }

    vector<long long> SX = sumOfWindowMaxima(X, n);
    vector<long long> SY = sumOfWindowMaxima(Y, n);

    for (int k = 1; k <= n; ++k) {
        long long ans = SX[k] * SY[k] % MOD;
        if (k == n) printf("%lld\n", ans);
        else printf("%lld ", ans);
    }
    return 0;
}
