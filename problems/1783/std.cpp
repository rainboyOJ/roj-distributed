// 一本通 1783《矩阵填数》 标程（目标 ROJ 题号 1783）
//
// 题意：给定 h×w 矩阵，每格填 1..m 的整数；给出 n 个子矩阵及其“最大值 = v”的限制，
//       求满足全部限制的填数方案数 mod 1e9+7。多组数据（T ≤ 5）。
//       范围：T ≤ 5，1 ≤ h,w,m ≤ 10000，1 ≤ v ≤ m，1 ≤ n ≤ 10。
//
// 同源题判定：本题即 【FJOI2017】矩阵填数（BZOJ 5010 / 洛谷 P3813），题面逐字一致。
//
// 参考来源（思路与 AC 代码，均经本机编译 + 题面样例验证后**改写**，非盲抄）：
//   1. https://blog.csdn.net/dingqiongliang0363/article/details/102168451
//      《P3813 [FJOI2017] 矩阵填数（组合数学）》
//      —— 给出完整 AC 代码：坐标/子集状压 + 交集面积 ist[mask]、并集面积 uni[mask]
//         （子集容斥），按 v 排序后分组，对每组做“至少一个格子取到 v”的容斥。
//         本标程的骨架与此一致。
//   2. https://blog.csdn.net/neweryyy/article/details/117934911
//      《P3813 [FJOI2017] 矩阵填数（容斥原理）》—— 复述同一容斥思路。
//   3. https://blog.csdn.net/weixin_30779691/article/details/96691009
//      《[luogu P3813] [FJOI2017] 矩阵填数 解题报告（容斥原理）》—— 同上。
//   4. 洛谷题面 https://www.luogu.com.cn/problem/P3813 （用于核对题意与样例：
//      输入样例输出 28 / 76475，与本题 content.md 完全一致）。
//
// 算法（容斥 + 状压，O(3^n + n·2^n·log MOD)，n ≤ 10 秒过）：
//   记 U(c) = min{ v_i : 子矩阵 i 覆盖格子 c }（未被任何限制覆盖时 U(c) = m）。
//   则“每格 ≤ 所属限制的 v”给出基础计数 ∏_c U(c)；“最大值恰为 v_i”等价于：
//   子矩阵 i 内至少有一个 U(c) = v_i 的格子取到值 v_i（U(c) < v_i 的格子取不到 v_i）。
//   把格子按 U(c) 的值分层，各层涉及的格子互不相交 ⇒ 各层独立相乘。
//   对某一层（值 = v，涉及格子集合 A_v = 被本层子矩阵覆盖、且不被任何更小 v 覆盖的格子）：
//     |A_v| = uni[本层∪更早层] - uni[更早层]；
//     对任意子集 W：令 tot = |∪_{i∈W} (S_i \ 更早层)|，
//     则“W 中每个子矩阵都没有格子取到 v”的方案数 = v^(|A_v|-tot)·(v-1)^tot；
//     层内答案 = Σ_W (-1)^|W| · 上式（容斥，0^0 约定为 1）。
//   未被任何限制覆盖的格子有 m 种取值，作为初始因子 m^(h·w - uni[full])。
//
// 实现要点/与来源 1 的差异：
//   - 来源 1 用 `if(a[i].v==a[i+1].v) continue;` 判组边界，会访问 a[n]（越界读未初始化值，
//     跨组测试时可能误合并分组）。本标程改为**显式 while 收集等值组**，行为确定。
//   - 来源 1 用 `uni[i] += (±1)*ist[j]` 直接累加并集（依赖 ll 溢出/无符号语义不明确处，
//     且 uni 未清零）；本标程显式以 long long 求和并逐测试点重算，语义清晰。
//   - 交集面积用 long long（h·w ≤ 1e8），指数同样 long long，避免 int 溢出。

#include <cstdio>
#include <algorithm>
using namespace std;

typedef long long ll;
static const ll MOD = 1000000007LL;

// 快速幂（0^0 约定为 1，符合容斥中 (v-1)^0 的取值）
static ll pw(ll x, ll y) {
    x %= MOD;
    if (x < 0) x += MOD;
    ll r = 1;
    while (y > 0) {
        if (y & 1) r = r * x % MOD;
        x = x * x % MOD;
        y >>= 1;
    }
    return r;
}

struct Rect {
    ll x1, y1, x2, y2, v;
};

static Rect a[16];            // 限制子矩阵，n ≤ 10
static ll ist[1 << 10];       // ist[mask]：mask 中所有子矩阵的交集面积（空则为 0）
static ll uni[1 << 10];       // uni[mask]：mask 中所有子矩阵的并集面积
static int pc[1 << 10];       // popcount

int main() {
    for (int i = 1; i < (1 << 10); ++i) pc[i] = pc[i >> 1] + (i & 1);

    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T--) {
        ll h, w;
        int m, n;
        scanf("%lld %lld %d %d", &h, &w, &m, &n);
        for (int i = 0; i < n; ++i)
            scanf("%lld %lld %lld %lld %lld",
                  &a[i].x1, &a[i].y1, &a[i].x2, &a[i].y2, &a[i].v);

        // 按 v 升序：保证“更早的层”就是“v 更小的层”
        sort(a, a + n, [](const Rect &A, const Rect &B) { return A.v < B.v; });

        const int full = (1 << n) - 1;

        // 子集交集面积
        for (int mask = 1; mask <= full; ++mask) {
            ll x1 = 1, y1 = 1, x2 = h, y2 = w;
            bool nul = false;
            for (int j = 0; j < n; ++j) {
                if (!((mask >> j) & 1)) continue;
                x1 = max(x1, a[j].x1);
                y1 = max(y1, a[j].y1);
                x2 = min(x2, a[j].x2);
                y2 = min(y2, a[j].y2);
                if (x1 > x2 || y1 > y2) { nul = true; break; }
            }
            ist[mask] = nul ? 0 : (x2 - x1 + 1) * (y2 - y1 + 1);
        }

        // 子集并集面积（容斥：Σ (-1)^(|J|+1) |∩_{j∈J} S_j|）
        uni[0] = 0;
        for (int mask = 1; mask <= full; ++mask) {
            ll s = 0;
            for (int sub = mask; sub > 0; sub = (sub - 1) & mask) {
                if (pc[sub] & 1) s += ist[sub];
                else             s -= ist[sub];
            }
            uni[mask] = s;
        }

        // 未被任何限制覆盖的格子：U(c) = m，任意取值
        ll ans = pw((ll)m, h * w - uni[full]);

        // 按 v 分层，逐层容斥
        int ls = 0;  // 所有 v 更小的限制的掩码
        for (int i = 0; i < n; ) {
            int j = i, nw = 0;
            while (j < n && a[j].v == a[i].v) { nw |= (1 << j); ++j; }
            ll v = a[i].v;

            ll sum = uni[nw | ls] - uni[ls];       // |A_v|
            ll re = pw(v, sum);                    // W = ∅ 项
            for (int u = nw; u > 0; u = (u - 1) & nw) {
                ll tot = uni[u | ls] - uni[ls];    // |∪_{i∈u} T_i|
                ll k = pw(v - 1, tot) * pw(v, sum - tot) % MOD;
                if (pc[u] & 1) re = (re - k + MOD) % MOD;
                else           re = (re + k) % MOD;
            }
            ans = ans * re % MOD;
            ls |= nw;
            i = j;
        }

        printf("%lld\n", ans);
    }
    return 0;
}
