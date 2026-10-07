// 一本通 1799 《数列》
// ---------------------------------------------------------------------------
// 来源/依据：
//   网络检索（Bing/CSDN/博客园）在本环境下均被反爬拦截，未能取到可直接引用的
//   题解代码，故按“检索 3-4 轮无果即自研”规则自行推导，并用题面两个样例验证。
//
// 推导：
//   记 d_i = a_{i+1} - a_i。条件 (a_k-a_{k-2})(a_{k-1}-a_{k-2}) < 0 等价于
//   (d_{k-1}+d_k)*d_{k-1} < 0，即相邻差 d_{k-1}, d_k 异号且 |d_k| > |d_{k-1}|。
//   于是差的符号交错、绝对值严格递增。
//   设 b_i = |d_i|，b_1 < b_2 < ... < b_{L}（L = m-1 ≥ 2 为步数）。
//   部分和 P_0=0,P_1,P_2,... 中“峰”严格递增、“谷”严格递减，故极值就是最后
//   一个峰与最后一个谷，它们相邻，跨度 span = b_L（最大幅度）。
//   给定形状（b 序列）后，平移到 [1,n] 的方案数为 n - b_L；两种取向（先升/
//   先降）各贡献一份。span = b_L = s 的形状数 = 从 {1..s-1} 选 L-1 个
//   (b_1..b_{L-1}) 并令 b_L=s，对 L=2..s 求和 = sum_{j=1}^{s-1} C(s-1,j) = 2^{s-1}-1。
//   因此
//     f(n) = 2 * sum_{s=2}^{n-1} (2^{s-1}-1)(n-s)
//          = 2^{n+1} - 4n - (n-1)(n-2)。
//   样例校验：n=3 -> 2；n=666 -> 805846404（与题面一致）。
//
// 数据范围 n ≤ 10^5000：以字符串读入，用 Fermat 小定理 2^{n+1} ≡ 2^{(n+1) mod (p-1)}
// (mod p)，多项式部分按 n mod p 计算。p = 1e9+7 为素数。
// ---------------------------------------------------------------------------
#include <iostream>
#include <string>
using namespace std;

static const long long MOD = 1000000007LL;

static long long modString(const string &s, long long m) {
    long long r = 0;
    for (char c : s) r = (r * 10 + (c - '0')) % m;
    return r;
}

static long long pw(long long b, long long e, long long m) {
    long long r = 1 % m; b %= m;
    while (e > 0) { if (e & 1) r = r * b % m; b = b * b % m; e >>= 1; }
    return r;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    if (!(cin >> s)) return 0;
    // 去掉可能的前导零（题目保证 n>=3，这里仅作健壮性处理）
    size_t pos = s.find_first_not_of('0');
    if (pos == string::npos) s = "0"; else s = s.substr(pos);

    long long np  = modString(s, MOD);      // n mod p
    long long nm1 = modString(s, MOD - 1);  // n mod (p-1)
    long long exp = (nm1 + 1) % (MOD - 1);  // (n+1) mod (p-1)

    long long pow2 = pw(2, exp, MOD);
    long long term = 4 * np % MOD;
    long long prod = ((np - 1 + MOD) % MOD) * ((np - 2 + MOD) % MOD) % MOD;
    long long ans = ((pow2 - term - prod) % MOD + MOD) % MOD;
    cout << ans << '\n';
    return 0;
}
