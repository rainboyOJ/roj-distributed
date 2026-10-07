// 题目：一本通 1680《序列》
// 参考来源（思路/解法）：
//   https://blog.csdn.net/qingfeixueyue/article/details/123188528
//   《信息学奥赛一本通高手训练 1680：序列》
//
// 改写说明：
//   原博客代码固定预处理到 1.4e6 并直接累加，无法直接覆盖本题 100% 数据
//   N<=1e9（且其 C 语言代码被站点打码、可读性差）。
//   本实现按同一 Golomb 序列递推思路改写为 C++17：预处理到 S(n) 首次超过 1e9
//   （约 4.4e5 项），并用前缀和 + 二分定位实现 O(log n) 单点查询，复杂度
//   O(T log n)，可轻松满足 T<=2000, N<=1e9 的限制。
//
// 题目含义：
//   序列 a = 1,2,2,3,3,4,4,4,5,...，其中 a[n] 表示整数 n 在该序列中出现的
//   次数（即 Golomb 序列）。设 last(x) = x 最后一次出现的位置 = a[1]+...+a[x]。
//   求 last(last(N)) mod (10^9+7)。
//
// 递推：a[1]=1, a[2]=2, a[n+1] = 1 + a[n+1-a[a[n]]]。

#include <cstdio>
#include <vector>
using namespace std;

static const long long MOD = 1000000007LL;
static const long long INV2 = 500000004LL;  // 2 在 mod 1e9+7 下的逆元

int main() {
    const long long NMAX = 1000000000LL;

    // 下标从 1 开始；S[i] = a[1]+...+a[i] = last(i)。
    // 块 k（值恰好为 k 的位置）覆盖 (S[k-1]+1 .. S[k])，共 a[k] 个位置。
    vector<long long> a(3), S(3), P(3);
    a[1] = 1; a[2] = 2;
    S[1] = 1; S[2] = 3;

    int n = 2;
    while (S[n] < NMAX) {
        long long gn = a[n];
        a.push_back(1 + a[n + 1 - a[gn]]);
        ++n;
        S.push_back(S[n - 1] + a[n]);
    }
    const int K = n;  // S[K] >= NMAX，覆盖所有可能的 N

    // P[k] = sum_{i=1..k} i * (块 i 内所有位置编号之和)  (mod MOD)
    // 块 i 内位置编号之和 blockSum(i) = (S[i-1]+1 + S[i]) * a[i] / 2。
    auto blockSum = [&](int i) -> long long {
        return (((S[i - 1] + 1 + S[i]) % MOD) *
                (a[i] % MOD) % MOD) * INV2 % MOD;
    };
    P[0] = 0;
    P[1] = 1 % MOD * blockSum(1) % MOD;
    P[2] = (P[1] + 2 % MOD * blockSum(2) % MOD) % MOD;
    for (int k = 3; k <= K; ++k) {
        P.push_back((P[k - 1] + (long long)k % MOD * blockSum(k) % MOD) % MOD);
    }

    // last(x) mod MOD：定位 x 所在块 g，last(x) = S[g-1] + g*(x-S[g-1])，
    // 答案 = sum_{i<g} i*blockSum(i) + g * (S[g-1]+1 + ... + x)。
    auto query = [&](long long x) -> long long {
        int lo = 1, hi = K;
        while (lo < hi) {
            int mid = (lo + hi) >> 1;
            if (S[mid] >= x) hi = mid;
            else lo = mid + 1;
        }
        long long g = lo;
        long long cnt = x - S[g - 1];
        long long tail = ((S[g - 1] + 1 + x) % MOD) * (cnt % MOD) % MOD * INV2 % MOD;
        return (P[g - 1] + g % MOD * tail) % MOD;
    };

    int Tn;
    scanf("%d", &Tn);
    while (Tn--) {
        long long N;
        scanf("%lld", &N);
        // 答案 = sum_{v=1..N} v*a[v] (mod MOD)，直接由块前缀和 query(N) 得到。
        printf("%lld\n", query(N));
    }
    return 0;
}
