// 一本通 1812《网格》标程
// 参考来源（检索结论）：
//   本题为“一本通 · 高手训练篇 · 六、数学基础”第 1812 题，题面来源标注见 candidate.json。
//   网络检索（CSDN 站内搜索 / 必应 / 百度 / 搜狗，关键词含题面特征句
//   “相邻点之间的距离不小于”“网格 1812 题解”及样例输出 490260662）均未命中可用的
//   本题 C++ 题解；故本标程为**自研推导**实现，并用题面全部 6 组样例逐一验证。
// 题意：网格 [0,W]x[0,H] 上有 (W+1)*(H+1) 个格点。选出 N 个互不相同的格点，要求它们
//       共线，且在该直线上相邻两点（按直线上顺序）的欧氏距离 >= D。求方案数 mod 1e9。
// 解法（组合计数，O(W*H*min(W/a,H/b)) 级别）：
//   任取一组合法的 N 个共线点，按直线上顺序排序。设其所在直线的**本原方向向量**为
//   (a,b)（gcd(a,b)=1），相邻两点的“指标差”为 k_1..k_{N-1}（均 >= K），则
//     - 相邻点距离 = k_i * sqrt(a^2+b^2)，要求 >= D  =>  k_i >= K,
//       其中 K = min{ k>=1 : k^2*(a^2+b^2) >= D^2 }（用平方避免浮点误差）。
//     - 首个点 p 与末个点 q = p + M*(a,b)，M = k_1+...+k_{N-1} >= (N-1)*K。
//     - 对固定的方向与固定的 M，p 的合法位置数为 (W+1-M|a|)*(H+1-M|b|)
//       （要求 M|a|<=W 且 M|b|<=H，否则为 0）。
//     - 把 M 拆成 (N-1) 个 >=K 的整数 k_i 的方案数 = C(M-(N-1)K + N-2, N-2)。
//   于是：答案 = Σ_{无向本原方向} Σ_{M>=(N-1)K} C(...) * (W+1-M|a|)*(H+1-M|b|)。
//   无向方向取代表元：水平 (1,0)、竖直 (0,1) 各计一次；斜率为正 (a,b),a,b>=1 与
//   斜率为负 (a,-b) 关于 y 轴对称，计数相同，故斜向部分乘 2。
//   特判 N=1：任取 1 个格点即可，答案 = (W+1)*(H+1)。
// 模数 1e9 **不是质数**，无法用费马小定理求逆元，故用杨辉三角打表求组合数（数值均 <1e9，
//   直接模 1e9 相加即可，无需逆元）。
// 溢出：单项 = C(<=1e9) * (<=501*501) < 2.6e14，long long 足够。
// I/O：scanf/printf（stdin→stdout），与仓库 problems/1000/std.cpp 风格一致。
#include <cstdio>
#include <algorithm>
using namespace std;
typedef long long ll;

const ll MOD = 1000000000LL;  // 题面模数 1,000,000,000（非质数）
const int MAXC = 1100;        // 组合数上标上限（M<=W<=500 且 N-2<=48，留足裕量）
const int MAXK = 55;          // 组合数下标上限（N-2<=48，留裕量）

static ll C[MAXC + 1][MAXK + 1];  // 杨辉三角 mod 1e9

// 手写 gcd，避免 __gcd（libstdc++ 专有）在 libc++ 下不可用
static int gcd_int(int x, int y) {
    while (y) { int t = x % y; x = y; y = t; }
    return x;
}

int main() {
    // 预处理组合数 C[i][j] = C(i,j) mod 1e9，j 只到 MAXK
    for (int i = 0; i <= MAXC; i++) {
        C[i][0] = 1 % MOD;
        int lim = min(i, MAXK);
        for (int j = 1; j <= lim; j++) {
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD;
        }
    }

    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T--) {
        int N, W, H, D;
        scanf("%d %d %d %d", &N, &W, &H, &D);

        if (N == 1) {  // 单个格点：任选一点即可（(W+1)*(H+1) 种）
            printf("%lld\n", (ll)(W + 1) * (H + 1) % MOD);
            continue;
        }

        ll ans = 0;
        ll DD = (ll)D * D;

        // 方向 (a,b)（a,b>=0 且不同时为 0，代表一条无向直线的方向）的贡献
        //   K  : 指标差下限
        //   Mx : M 的上限（受 x 方向跨度约束；a==0 时无约束）
        //   My : M 的上限（受 y 方向跨度约束；b==0 时无约束）
        auto contrib = [&](int a, int b) -> ll {
            ll s2 = (ll)a * a + (ll)b * b;   // |direction|^2
            int K = 1;
            while ((ll)K * K * s2 < DD) K++;  // 最小 k>=1 使 k^2*s2 >= D^2
            ll base = (ll)(N - 1) * K;        // M 的下限
            ll Mx = (a == 0) ? (ll)1e18 : (ll)W / a;
            ll My = (b == 0) ? (ll)1e18 : (ll)H / b;
            ll Mmax = min(Mx, My);
            ll res = 0;
            for (ll M = base; M <= Mmax; M++) {
                ll idx = M - base + (N - 2);          // 组合数上标
                if (idx > MAXC) break;                // 理论上不会发生
                ll ways = C[idx][N - 2];              // 拆分数
                ll px = (ll)(W + 1) - M * a;          // p 的 x 可选数
                ll py = (ll)(H + 1) - M * b;          // p 的 y 可选数
                if (px <= 0 || py <= 0) continue;
                res = (res + ways % MOD * (px % MOD) % MOD * (py % MOD)) % MOD;
            }
            return res;
        };

        // 水平方向 (1,0) 与竖直方向 (0,1)：各为一条无向方向
        ans = (ans + contrib(1, 0)) % MOD;
        ans = (ans + contrib(0, 1)) % MOD;

        // 斜向方向：正斜率 (a,b) 与负斜率 (a,-b) 对称，计数相同 => 乘 2
        for (int a = 1; a <= W; a++) {
            for (int b = 1; b <= H; b++) {
                if (gcd_int(a, b) != 1) continue;     // 只取本原方向
                if ((ll)a * (N - 1) > W) continue;    // M>=N-1 时需 M*a<=W 才可能非零
                if ((ll)b * (N - 1) > H) continue;
                ll c = contrib(a, b);
                if (c) ans = (ans + 2 * c) % MOD;
            }
        }

        printf("%lld\n", ans % MOD);
    }
    return 0;
}
