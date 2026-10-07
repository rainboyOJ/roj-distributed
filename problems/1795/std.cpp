// ============================================================================
// 一本通 1795《散步》 标程
// ----------------------------------------------------------------------------
// 【题目】数轴上从原点出发，n 个单位时间（每步 ±1），每次离家的时间不能超过 m，
//         n 个时间后正好回到家，求方案数 mod 1e9+7。2<=n<=1e9, 2<=m<=100, n,m 均为偶数。
//
// 【来源 / 依据】
//   * 题目与限制核对：信息学奥赛一本通在线评测系统 1795：散步
//     http://ybt.ssoier.cn:8088/problem_show.php?pid=1795
//     （页面确认：时间限制 1000 ms，内存 262144 KB，样例 4 2 -> 4）
//   * 网络检索（Bing / CSDN 站内搜 / 博客园站内搜，共 4 轮，关键词包括
//     "ztxz16"、"每次离家的时间不能超过"、一本通 1795 题解、高手训练 散步 矩阵等）
//     均未找到本题可用的 AC 代码或题解，故按题面自行推导算法（见下），
//     并用题面两个样例（4 2 -> 4，10 6 -> 184）验证通过。
//
// 【算法推导】
//   一次「离家」= 一段从 0 出发、途中不再回到 0、最后回到 0 的连续走法（一次远足）。
//   长为 2j 的远足数 f(2j) = 2 * Catalan(j-1)：
//     首步 ±1（2 种），其余 2j-2 步是从 ±1 出发、不触碰 0 回到 ±1 的走法，
//     平移后即长度 2j-2 的非负走法数 = Catalan(j-1)。
//   令 g(n) = 长度为 n 的合法方案数，按最后一次远足的长度分解：
//     g(0)=1,  g(n)= sum_{j=1..min(d,n/2)} f(2j) * g(n-2j),  d = m/2.
//   令 h(t)=g(2t)，则 h(0)=1, h(t)= sum_{j=1..d} c_j h(t-j)，c_j = 2*Catalan(j-1) mod p，
//   这是 d 阶常系数线性递推（d = m/2 <= 50），用 d×d 伴随矩阵快速幂：
//     A = [[c_1..c_d],[1,0..0],[0,1,0..],...],   h(t) = (A^t)[0][0].
//   复杂度 O(d^3 log n) <= 50^3 * 30 ≈ 3.8e6，远低于 1s。
//   校验：n=4,m=2 -> h(2)=2^2=4 ✓；n=10,m=6 -> d=3, c=[2,2,4],
//         h(5)=2*60+2*20+4*6=184 ✓（与题面样例一致）。
// ============================================================================

#include <cstdio>
#include <cstring>
using namespace std;

typedef long long ll;

const ll MOD = 1000000007LL;
const int MAXD = 55;   // m<=100 -> d=m/2<=50，留安全余量

int d;                 // 递推阶数 = m/2
ll c[MAXD];            // 递推系数 c[j] = f(2*(j+1)) = 2*Catalan(j)

struct Mat {
    ll a[MAXD][MAXD];
    Mat() { memset(a, 0, sizeof(a)); }
};

Mat mul(const Mat &x, const Mat &y) {
    Mat r;
    for (int i = 0; i < d; i++)
        for (int k = 0; k < d; k++) {
            if (!x.a[i][k]) continue;
            ll v = x.a[i][k];
            for (int j = 0; j < d; j++)
                r.a[i][j] = (r.a[i][j] + v * y.a[k][j]) % MOD;
        }
    return r;
}

Mat mpow(Mat base, ll e) {
    Mat r;
    for (int i = 0; i < d; i++) r.a[i][i] = 1;
    while (e) {
        if (e & 1) r = mul(r, base);
        base = mul(base, base);
        e >>= 1;
    }
    return r;
}

// 快速幂（用于求逆元/幂）
ll qpow(ll a, ll b) {
    ll r = 1; a %= MOD;
    while (b) { if (b & 1) r = r * a % MOD; a = a * a % MOD; b >>= 1; }
    return r;
}

int main() {
    ll n, m;
    if (scanf("%lld %lld", &n, &m) != 2) return 0;
    d = (int)(m / 2);

    // Catalan(j) = C(2j,j)/(j+1)，j = 0..d-1，用阶乘+逆元计算
    // c[j] = 2 * Catalan(j)
    ll fact[2 * MAXD + 5], inv_fact[2 * MAXD + 5];   // 需到 (2d)!，d<=50 -> 100
    fact[0] = 1;
    for (int i = 1; i <= 2 * d; i++) fact[i] = fact[i - 1] * i % MOD;
    inv_fact[2 * d] = qpow(fact[2 * d], MOD - 2);
    for (int i = 2 * d; i >= 1; i--) inv_fact[i - 1] = inv_fact[i] * i % MOD;

    for (int j = 0; j < d; j++) {
        // Catalan(j) = (2j)! / (j! (j+1)!)
        ll cat = fact[2 * j] * inv_fact[j] % MOD * inv_fact[j + 1] % MOD;
        c[j] = 2 * cat % MOD;
    }

    // 伴随矩阵：第一行 c[0..d-1]，次对角线为 1
    Mat A;
    for (int j = 0; j < d; j++) A.a[0][j] = c[j];
    for (int i = 1; i < d; i++) A.a[i][i - 1] = 1;

    ll t = n / 2;                 // n 为偶数
    Mat P = mpow(A, t);
    printf("%lld\n", P.a[0][0] % MOD);
    return 0;
}
