// 一本通 1809《日食》 标准程序 std.cpp
//
// 题面：S1=A, S2=B, Si=(X*S(i-1)+Y*S(i-2)+Z) mod P (i>=3)，P 为质数。
//       每次询问 [L,R] 中有多少个 i 使 Si==C。T<=2, Q<=2e4, L,R<=1e18,
//       0<=A,B,X,Y,Z,C<P<=10007, P 质数。
//
// 来源说明（按要求做了 3 轮联网检索，均未取得可引用的公开题解代码，故按题面自研）：
//   R1 题面特征句精确搜索（Bing）：
//      q="第$i$天有一个特征值" 日食 一本通 → 返回跳转页(101KB, 0 条可用结果)
//   R2 CSDN 站内搜索：q="一本通 1809 题解" → 返回 6KB 壳页，无结果条目
//   R3 Bing：q="Lyra 日食 一本通"、q="一本通 1809 日食 题解" → 各 ~100KB，<h2> 结果数 0
//      （另：题面特征词「作为滋滋国最具智慧的人」「Lyra」均无命中）
//   结论：本题题面为「一本通·高手训练」自有题，网络无公开题解；算法为自研推导，
//   正确性以 ① 题面样例逐行一致（两组均手工复核）② data.py 中的闭式可验证数据点
//   （见下）作为依据。数据点 8-1 / 10-1 / 10-2 / 2-1 / 2-2 / 3-2 的答案可由手算闭式
//   公式独立给出，std 输出与之逐一相符。
//
// 算法（自研推导）：
//   记状态 State_k=(S_k, S_(k+1))，答案 = cnt(R) - cnt(L-1)，
//   cnt(n)=#{1<=i<=n : S_i==C}，其中 i=1 的贡献是 [A==C]，i>=2 时 S_i 是
//   State_(i-1) 的第二分量。
//
//   * Y!=0：转移 f(a,b)=(b, X*b+Y*a+Z mod P) 在 P^2 个状态上是双射
//     （逆映射 a=Y^{-1}(c-X*b-Z) mod P 唯一），故从 State_1=(A,B) 出发是纯循环，
//     循环长度 lam<=P^2，无前导段。
//     把 f 看作仿射映射 g=(M, t)，M=[[0,1],[Y,X]]（det=-Y!=0 可逆），t=(0,Z)：
//       f(v) = M v + t,  g^k = (M^k, (sum_{i<k} M^i) t).
//     lam 的求法：GL_2(F_p) 的指数整除 N0=p(p^2-1)=p(p-1)(p+1)（对 p=2 亦成立），
//     故 ord(M)|N0；对 N0 的每个素因子 q 反复用 M^(N/q)==I 判定除掉 q，得 ord(M)=n1。
//     又 g^(n1*p)=I（M^n1=I 且平移项为 p*...=0），故 g 的阶整除 n1*p，
//     而 lam 整除 g 的阶；于是对 n1*p 的每个素因子 q 反复用
//       g^((n1*p)/q)(State_1)==State_1
//     判定除掉 q，即得 lam。全程 O(polylog)，不需要 O(P^2) 枚举。
//     随后只需在循环上扫一遍 lam 步：得到整周期内 S_i==C 的个数 cycleCount，
//     并在需要的位置记录前缀计数。每个查询的 (n-1)=full*lam+rem，
//     cnt 的第二部分 = full*cycleCount + (循环内前 rem 步的计数)，
//     rem 对全部查询去重后在同一次扫描里打点。
//
//   * Y==0：递推退化为 S_i = X*S_(i-1)+Z (i>=3)，即 v_t=S_(t+2) 是 [0,P) 上的
//     一阶仿射迭代（v_0=B）。用 O(P) 找前导段 mu 与循环 lam，前缀计数闭式求解。
//
//   复杂度：Y!=0 时 O(lam + Q log Q)（lam<=P^2，单步为预乘表+条件减法），
//           Y==0 时 O(P + Q)；空间 O(P+Q)。P=10007 最坏 lam≈1.0e8，T=2 约 2e8 步。
//
// 依据：题面 content.md；样例输出与 std 逐行一致。

#include <cstdio>
#include <cstdlib>
#include <vector>
#include <algorithm>
using namespace std;
typedef long long ll;

static const int MAXP = 10020;
static int mulX[MAXP], mulY[MAXP];

// ---------- 快速读入 ----------
static char ibuf[1 << 25];
static int ipos = 0, ilen = 0;
static inline int gc() {
    if (ipos == ilen) {
        ilen = (int)fread(ibuf, 1, sizeof(ibuf), stdin);
        ipos = 0;
        if (ilen <= 0) return -1;
    }
    return ibuf[ipos++];
}
static inline ll readInt() {
    int c = gc();
    while (c != -1 && (c < '0' || c > '9') && c != '-') c = gc();
    ll sgn = 1;
    if (c == '-') { sgn = -1; c = gc(); }
    ll v = 0;
    while (c >= '0' && c <= '9') { v = v * 10 + (c - '0'); c = gc(); }
    return v * sgn;
}

// ---------- 2x2 矩阵与仿射映射 (x -> M x + t) mod p ----------
struct Mat { ll a, b, c, d; };
static inline Mat mmul(const Mat &x, const Mat &y, ll p) {
    return Mat{ (x.a * y.a + x.b * y.c) % p, (x.a * y.b + x.b * y.d) % p,
                (x.c * y.a + x.d * y.c) % p, (x.c * y.b + x.d * y.d) % p };
}
static Mat mpow(Mat x, ll e, ll p) {
    Mat r{ 1, 0, 0, 1 };
    while (e) { if (e & 1) r = mmul(r, x, p); x = mmul(x, x, p); e >>= 1; }
    return r;
}
static inline bool isI(const Mat &x, ll p) {
    return x.a % p == 1 && x.b % p == 0 && x.c % p == 0 && x.d % p == 1;
}
struct Aff { Mat m; ll t0, t1; };
static inline Aff amul(const Aff &A, const Aff &B, ll p) {   // A o B
    Mat m = mmul(A.m, B.m, p);
    ll t0 = (A.m.a * B.t0 + A.m.b * B.t1 + A.t0) % p;
    ll t1 = (A.m.c * B.t0 + A.m.d * B.t1 + A.t1) % p;
    return Aff{ m, t0, t1 };
}
static Aff apow(Aff g, ll e, ll p) {
    Aff r{ Mat{ 1, 0, 0, 1 }, 0, 0 };
    while (e) { if (e & 1) r = amul(r, g, p); g = amul(g, g, p); e >>= 1; }
    return r;
}
static inline void aapply(const Aff &g, ll a, ll b, ll p, ll &na, ll &nb) {
    na = (g.m.a * a + g.m.b * b + g.t0) % p;
    nb = (g.m.c * a + g.m.d * b + g.t1) % p;
}
static vector<ll> distinctPrimes(ll n) {
    vector<ll> f;
    for (ll q = 2; q * q <= n; q++)
        if (n % q == 0) { f.push_back(q); while (n % q == 0) n /= q; }
    if (n > 1) f.push_back(n);
    return f;
}

int main() {
    int T = (int)readInt();
    if (T <= 0) return 0;
    while (T--) {
        ll A = readInt(), B = readInt(), X = readInt(), Y = readInt(),
           Z = readInt(), P = readInt(), C = readInt(), Q = readInt();

        for (int i = 0; i < (int)P; i++) {
            mulX[i] = (int)((X * i) % P);
            mulY[i] = (int)((Y * i) % P);
        }

        vector<ll> Ls(Q), Rs(Q);
        for (int i = 0; i < Q; i++) { Ls[i] = readInt(); Rs[i] = readInt(); }

        ll base = (A == C) ? 1 : 0;   // i=1 的贡献

        if (Y == 0) {
            // ---- 一阶仿射递推：v_0=B, v_(t+1)=(X*v_t+Z) mod P, S_(t+2)=v_t ----
            vector<int> vis((size_t)P, -1);
            vector<int> vals;
            vals.reserve((size_t)P + 2);
            int v = (int)(B % P);
            int idx = 0;
            while (vis[v] == -1) {
                vis[v] = idx;
                vals.push_back(v);
                v = (int)(((ll)X * v + Z) % P);
                idx++;
            }
            int mu = vis[v];
            int lam = idx - mu;
            vector<int> preCum(mu + 1, 0), cycCum(lam + 1, 0);
            for (int t = 0; t < mu; t++) preCum[t + 1] = preCum[t] + (vals[t] == C ? 1 : 0);
            for (int u = 0; u < lam; u++) cycCum[u + 1] = cycCum[u] + (vals[mu + u] == C ? 1 : 0);

            auto countV = [&](ll x) -> ll {          // #{0<=t<=x : v_t==C}
                if (x < 0) return 0;
                ll total = x + 1;
                if (total <= mu) return preCum[(size_t)total];
                ll rest = total - mu;
                return (ll)preCum[mu] + (rest / lam) * cycCum[lam] + cycCum[rest % lam];
            };
            auto cnt = [&](ll n) -> ll {
                if (n <= 0) return 0;
                ll r = base;
                if (n >= 2) r += countV(n - 2);
                return r;
            };
            for (int i = 0; i < Q; i++) printf("%lld\n", cnt(Rs[i]) - cnt(Ls[i] - 1));
        } else {
            // ---- Y!=0：状态双射，纯循环；用仿射映射的阶求循环长度 lam ----
            Mat M{ 0, 1, Y % P, X % P };
            ll N0 = P * (P - 1) * (P + 1);           // ord(M) | N0
            vector<ll> primes = distinctPrimes(P - 1);
            {
                vector<ll> t = distinctPrimes(P + 1);
                for (ll q : t) primes.push_back(q);
            }
            primes.push_back(P);
            sort(primes.begin(), primes.end());
            primes.erase(unique(primes.begin(), primes.end()), primes.end());

            ll n1 = N0;                              // ord(M)
            for (ll q : primes)
                while (n1 % q == 0 && isI(mpow(M, n1 / q, P), P)) n1 /= q;

            Aff g{ M, 0, Z % P };
            ll lam = n1 * P;                         // g^(n1*P)=I, lam | n1*P
            for (ll q : primes) {
                while (lam % q == 0) {
                    Aff h = apow(g, lam / q, P);
                    ll na, nb; aapply(h, A, B, P, na, nb);
                    if (na == A && nb == B) lam /= q; else break;
                }
            }

            // 收集需要的循环内余数位置 m%lam（m=n-1）
            vector<ll> rems;
            rems.reserve((size_t)(2 * Q));
            for (int i = 0; i < Q; i++) {
                ll n1q = Rs[i], n2q = Ls[i] - 1;
                if (n1q >= 2) { ll r = (n1q - 1) % lam; if (r > 0) rems.push_back(r); }
                if (n2q >= 2) { ll r = (n2q - 1) % lam; if (r > 0) rems.push_back(r); }
            }
            sort(rems.begin(), rems.end());
            rems.erase(unique(rems.begin(), rems.end()), rems.end());
            vector<ll> part(rems.size(), 0);

            // 单次扫描循环：k=1..lam，State_k=(S_k,S_(k+1))，h(k)=[S_(k+1)==C]
            ll cum = 0, cycleCount = 0;
            {
                int x = (int)A, y = (int)B;
                size_t ptr = 0;
                for (ll k = 1; k <= lam; k++) {
                    cum += (y == C) ? 1 : 0;
                    while (ptr < rems.size() && rems[ptr] == k) { part[ptr] = cum; ptr++; }
                    int z = mulX[y] + mulY[x] + (int)Z;
                    if (z >= P) z -= (int)P;
                    if (z >= P) z -= (int)P;
                    x = y; y = z;
                }
                cycleCount = cum;
            }
            auto partial = [&](ll r) -> ll {
                if (r == 0) return 0;
                size_t pos = (size_t)(lower_bound(rems.begin(), rems.end(), r) - rems.begin());
                return part[pos];
            };
            auto cnt = [&](ll n) -> ll {
                if (n <= 0) return 0;
                ll r = base;
                if (n >= 2) {
                    ll m = n - 1;
                    r += (m / lam) * cycleCount + partial(m % lam);
                }
                return r;
            };
            for (int i = 0; i < Q; i++) printf("%lld\n", cnt(Rs[i]) - cnt(Ls[i] - 1));
        }
    }
    return 0;
}
