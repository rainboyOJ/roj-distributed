// 一本通 1798 《递推数列》
// ---------------------------------------------------------------------------
// 题面 (content.md):
//   f(i) = ( a*f(i-1) + b ) / ( c*f(i-1) + d )  (mod p)
//   给定 f(0),a,b,c,d,n,p, 求 f(n); 多组数据 (t 组).
//   1<=t<=1e4, 0<=n<=1e18, 2<=p<=1e9,
//   0<=|f(0)|,|a|,|b|,|c|,|d|<p, 保证除法时逆元一定存在.
//
// 做法 (自研, 依据题面递推式):
//   这是 (模 p 下的) 莫比乌斯变换, 可用 2x2 矩阵快速幂.
//   令 u_0 = f(0), v_0 = 1,  M = [[a,b],[c,d]].
//   定义 (u_i,v_i)^T = M^i (u_0,v_0)^T, 则归纳可证 f(i) = u_i * inv(v_i) (mod p):
//     f(1) = (a*f0+b)/(c*f0+d) = u_1/v_1;
//     若 f(i-1)=u_{i-1}/v_{i-1}, 则
//     f(i) = (a*u_{i-1}+b*v_{i-1}) / (c*u_{i-1}+d*v_{i-1}) = u_i/v_i.
//   故 (u_n,v_n) = M^n (f(0),1), 答案 = u_n * inv(v_n) mod p.
//   n=0 时答案即 f(0) mod p.
//   逆元用扩展欧几里得 (p 不要求是素数, 只要 gcd(v_n,p)=1, 题面保证).
//   乘法安全: p<=1e9<2^30, 单乘积 <2^60, 两项求和 <2^61, 不溢出 long long.
//
// 复杂度: O(t log n), t=1e4, n<=1e18 => 约 4.8e6 次模乘, 远低于 1s.
//
// 来源说明: 检索 3 轮 (Bing / CSDN 站内) 未找到该题精确同源代码,
//   题面为公开的标准莫比乌斯变换+矩阵快速幂模型, 故按题面递推式自研实现.
//   题面样例 "1 / 54 40 11 39 -40 66 73" => "54" 已编译验证通过.
// ---------------------------------------------------------------------------
#include <cstdio>
#include <cstdlib>
using namespace std;
typedef long long ll;

static ll p;

static inline ll norm(ll x) { x %= p; if (x < 0) x += p; return x; }

struct Mat { ll m[2][2]; };

static Mat mul(const Mat &A, const Mat &B) {
    Mat C;
    for (int i = 0; i < 2; ++i)
        for (int j = 0; j < 2; ++j) {
            ll s = 0;
            for (int k = 0; k < 2; ++k) s += A.m[i][k] * B.m[k][j] % p;
            C.m[i][j] = s % p;
        }
    return C;
}

static Mat mpow(Mat A, unsigned long long e) {
    Mat R;
    R.m[0][0] = 1; R.m[0][1] = 0;
    R.m[1][0] = 0; R.m[1][1] = 1;
    while (e) {
        if (e & 1) R = mul(R, A);
        A = mul(A, A);
        e >>= 1;
    }
    return R;
}

static ll exgcd(ll a, ll b, ll &x, ll &y) {
    if (b == 0) { x = 1; y = 0; return a; }
    ll g = exgcd(b, a % b, y, x);
    y -= a / b * x;
    return g;
}

// 要求 gcd(a,p)==1 (题面保证)
static ll inv(ll a) {
    ll x, y;
    exgcd(norm(a), p, x, y);
    return norm(x);
}

int main() {
    int t;
    if (scanf("%d", &t) != 1) return 0;
    while (t--) {
        ll f0, a, b, c, d, n, pp;
        scanf("%lld %lld %lld %lld %lld %lld %lld", &f0, &a, &b, &c, &d, &n, &pp);
        p = pp;
        f0 = norm(f0); a = norm(a); b = norm(b); c = norm(c); d = norm(d);
        if (n == 0) { printf("%lld\n", f0); continue; }
        Mat M; M.m[0][0] = a; M.m[0][1] = b;
               M.m[1][0] = c; M.m[1][1] = d;
        Mat R = mpow(M, (unsigned long long)n);
        ll u = (R.m[0][0] * f0 + R.m[0][1]) % p;
        ll v = (R.m[1][0] * f0 + R.m[1][1]) % p;
        printf("%lld\n", u * inv(v) % p);
    }
    return 0;
}
