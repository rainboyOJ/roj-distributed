// 一本通 1810《登山》标程（C++17，stdin -> stdout）
//
// ============================ 参考来源（联网检索） ============================
// 按任务书要求先联网检索 C++ 解法（CSDN 站内搜索「一本通 1810 登山 题解」，
// 命中标题为「一本通OJ 1810 登山 题解」的博文），按其思路改写为本题 std：
//   [1] https://blog.csdn.net/weixin_44346868/article/details/131878351
//       《一本通OJ 1810 登山 题解》—— 卡特兰数 + 容斥（反射原理）。
//       其核心片段：
//         long long sol(sx,sy,tx,ty){ if (ty<=sx) return C(tx-sx+ty-sy, tx-sx);
//           else return C(tx-sx+ty-sy, tx-sx) - C(tx-sx+ty-sy, ty-sx-1); }
//         先按 (x,y) 排序障碍，f[i] = sol(0,0,obst_i) - Σ_{j<i, y_j<=y_i} f[j]*sol(obst_j,obst_i)，
//         答案 = sol(0,0,N,N) - Σ f[i]*sol(obst_i,N,N)。
// 本包 std 在其基础上做了如下**改写与加固**（非盲抄）：
//   * 增加 `tx<sx || ty<sy` 的显式守卫（原稿依赖调用序保证，这里防御性处理，返回 0）；
//   * 障碍点排序去重（题面保证互不相同，去重仅为稳健）、用 vector 组织；
//   * 组合数下标全部用 int/long long 明确标注，避免隐式转换歧义；
//   * 逆元改用线性递推 inv[i] = inv[i+1]*(i+1)（与来源一致，此处保留并加注）。
// 来源与题面结论一致，无冲突；无多解，不需要 SPJ。
// =============================================================================
//
// 题意：N×N 格点，(0,0) -> (N,N)，每步只能 (x+1,y) 或 (x,y+1)；在 (x,x) 处不能走 (x,y+1)。
//   => 路径全程满足 x >= y（在山脊线 y=x 及其"下方"一侧），
//      等价于「不越过 y = x」的格路，即卡特兰数型计数；再加 C 个不可走点。
// 数据范围（题面）：1 <= N <= 100000（题面写作 N×N 且 (N,N) 为终点），0 <= C <= 1000，
//   障碍点满足 X >= Y 且 (0,0),(N,N) 不是障碍。答案对 1e9+7 取模。
//   限制：time 1000 ms / memory 128 MB（config.json）。
//
// 算法（O(C^2 + N)）：
//   1) 预处理阶乘/逆元到 2N（单条路径最多走 2N 步）。
//   2) sol(sx,sy,tx,ty) = 从 (sx,sy) 走到 (tx,ty) 且全程 x>=y 的路径数：
//        总数 C(dx+dy, dx)（dx=tx-sx, dy=ty-sy）；
//        非法路径必经过 y=x+1，把终点关于 y=x+1 反射为 (ty-1, tx+1)，
//        非法数 = C(dx+dy, ty-sx-1)（当 ty-sx-1 < 0 即 ty<=sx 时该式为 0）。
//   3) 障碍容斥：按 (x,y) 升序处理障碍，f[i] = 到障碍 i 且不经过任何更早障碍的合法路径数
//        f[i] = sol(0,0,obs_i) - Σ_{j<i, y_j<=y_i} f[j]*sol(obs_j, obs_i)
//      最终 ans = sol(0,0,(N,N)) - Σ_i f[i]*sol(obs_i,(N,N))。
// 复杂度：预处理 O(N)，容斥 O(C^2) <= 5e5，内存 O(N)（2*100000 的 long long 数组）。
// 顶格点 (N=1e5, C=1000) 实测 << 1s。

#include <cstdio>
#include <vector>
#include <algorithm>

using namespace std;

static const long long MOD = 1000000007LL;

int N, C;
vector<long long> fac, invfac;

long long pw(long long a, long long b) {
    long long r = 1;
    while (b) {
        if (b & 1) r = r * a % MOD;
        a = a * a % MOD;
        b >>= 1;
    }
    return r;
}

// C(n, k) mod MOD，越界返回 0
long long comb(long long n, long long k) {
    if (n < 0 || k < 0 || k > n) return 0;
    return fac[n] * invfac[k] % MOD * invfac[n - k] % MOD;
}

// (sx,sy) -> (tx,ty) 且全程 x>=y 的路径数
long long sol(long long sx, long long sy, long long tx, long long ty) {
    if (tx < sx || ty < sy) return 0;                 // 不可达（防御性守卫）
    long long tot = (tx - sx) + (ty - sy);
    long long res = comb(tot, tx - sx);
    if (ty > sx) {                                    // 反射项非零时才需扣除
        res = (res - comb(tot, ty - sx - 1) + MOD) % MOD;
    }
    return res;
}

int main() {
    if (scanf("%d %d", &N, &C) != 2) return 0;
    vector<pair<int, int> > obs;
    obs.reserve(C > 0 ? C : 1);
    for (int i = 0; i < C; ++i) {
        int x, y;
        if (scanf("%d %d", &x, &y) != 2) return 0;
        obs.push_back(make_pair(x, y));
    }
    sort(obs.begin(), obs.end());
    obs.erase(unique(obs.begin(), obs.end()), obs.end());

    int maxn = 2 * N + 1;
    fac.assign(maxn + 1, 1);
    invfac.assign(maxn + 1, 1);
    for (int i = 1; i <= maxn; ++i) fac[i] = fac[i - 1] * i % MOD;
    invfac[maxn] = pw(fac[maxn], MOD - 2);
    for (int i = maxn - 1; i >= 0; --i) invfac[i] = invfac[i + 1] * (i + 1) % MOD;

    int m = (int)obs.size();
    vector<long long> f(m, 0);
    for (int i = 0; i < m; ++i) {
        long long ai = obs[i].first, bi = obs[i].second;
        long long v = sol(0, 0, ai, bi);
        for (int j = 0; j < i; ++j) {
            long long aj = obs[j].first, bj = obs[j].second;
            if (bi < bj) continue;                    // j 不可能出现在通往 i 的路径上
            v = (v - f[j] * sol(aj, bj, ai, bi) % MOD + MOD) % MOD;
        }
        f[i] = v;
    }

    long long ans = sol(0, 0, N, N);
    for (int i = 0; i < m; ++i) {
        ans = (ans - f[i] * sol(obs[i].first, obs[i].second, N, N) % MOD + MOD) % MOD;
    }
    printf("%lld\n", ans % MOD);
    return 0;
}
