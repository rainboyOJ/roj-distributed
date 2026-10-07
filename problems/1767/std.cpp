// 一本通 1767《字符合并》标程
//
// 题意：长度 n 的 01 串，每次可将相邻的 k 个字符合并成 1 个新字符并得分，
//       新字符与分数由这 k 个字符（看作 k 位二进制数 i，最高位为最左字符）查表给出。
//       求能获得的最大分数。
//
// 判定为经典题同源：[HAOI2016] 字符合并（BZOJ 4565 / 洛谷 P3736），
// 输入格式、数据范围（n<=300, 2<=k<=8, 2^k 行 c_i/w_i, w_i<=1e9）与本题完全一致。
//
// 算法：区间 DP + 状压（O(n^2 * (n/(k-1)) * 2^(k-1))，n<=300,k<=8 实测 <1s）
//   记 len(l,r)=r-l+1，该区间经过任意次合并后长度固定为 ((len-1) mod (k-1)) + 1。
//   f[l][r][S] = 把 a[l..r] 合并成 01 串 S（|S| = 该区间最终长度）能得到的最大分数。
//   基态：f[i][i][a[i]] = 0。
//   转移：把 S 的最右一位看成由后缀 [mid+1,r] 合并成的单个字符，
//         前缀 [l,mid] 合并成 |S|-1 个字符；为使 [mid+1,r] 最终长度为 1，
//         需 (r-mid-1) mod (k-1) == 0，故 mid 从 r-1 每次减 (k-1)。
//         - 若该区间最终长度 > 1：f[l][r][S<<1|b] = max(f[l][mid][S] + f[mid+1][r][b])。
//         - 若该区间最终长度 == 1（(len-1) mod (k-1) == 0）：此时 [l,mid] 恰有 k-1 个字符，
//           与后缀 1 个字符拼成 k 位后立即合并：
//             f[l][r][c] = max(f[l][mid][S] + f[mid+1][r][b] + w[S<<1|b])。
//   答案：因 w_i>=1，合并只会加分，把整串合并到最短（长度 ((n-1) mod (k-1))+1）最优，
//         故 ans = max_S f[1][n][S]。
//   内存：状态只用到 <= k-1 位（< 2^(k-1)），故第三维开 2^(k-1)（k<=8 时为 128），
//         避免原题解开 2^k 导致的 ~190MB 占用（本实现 n=300,k=8 约 93MB）。
//
// 参考来源（已联网检索，按题面改写并自行编译验证）：
//   1) https://blog.csdn.net/pythonyx/article/details/122448377
//      《P3736 [HAOI2016]字符合并 题解》：给出完整区间状压 DP 代码
//      （mid 以 k-1 为步长倒序枚举、末尾 k 位再合并、答案取 max_S f[1][n][S]），
//      本标程与之同构。
//   2) https://blog.csdn.net/cqbzlydd/article/details/111240741
//      《【题解】「HAOI2016」字符合并》：同样指出"区间最终长度 = (len-1)%(k-1)+1"、
//      "枚举时可 K-1 格地跳"，答案亦取 max_S dp[1][n][S]。
//   3) https://blog.csdn.net/weixin_44118043/article/details/113190228
//      《[HAOI2016]字符合并 牛客（区间dp）》：同一思路的佐证。
#include <cstdio>
#include <cstring>
#include <algorithm>

typedef long long ll;

const int MAXN = 305;          // n <= 300，留安全系数
const int MAXK = 8;
const int MAXS = 1 << (MAXK - 1);   // 状态位数 <= k-1 <= 7，故状态数 <= 128

int n, k;
int a[MAXN];
int c[1 << MAXK];              // 合并结果字符
ll  w[1 << MAXK];              // 合并得分
ll  f[MAXN][MAXN][MAXS];       // f[l][r][S]

const ll NEG = -1e18;

int main()
{
    scanf("%d %d", &n, &k);
    for (int i = 1; i <= n; i++) scanf("%d", &a[i]);
    int tot = 1 << k;
    for (int i = 0; i < tot; i++) scanf("%d %lld", &c[i], &w[i]);

    const int km1 = k - 1;
    const int smax = 1 << km1;

    for (int i = 0; i <= n; i++)
        for (int j = 0; j <= n; j++)
            for (int s = 0; s < smax; s++)
                f[i][j][s] = NEG;

    for (int i = 1; i <= n; i++) f[i][i][a[i]] = 0;

    for (int len = 2; len <= n; len++) {
        int t = (len - 1) % km1;            // 0 表示该区间最终长度为 1（需再合并一次）
        for (int l = 1; l + len - 1 <= n; l++) {
            int r = l + len - 1;
            if (t == 0) {
                // 最终长度 1：前缀 [l,mid] 恰 k-1 个字符 + 后缀 1 个字符，再合并
                ll g0 = NEG, g1 = NEG;
                int lim = 1 << km1;
                for (int mid = r - 1; mid >= l; mid -= km1) {
                    for (int S = 0; S < lim; S++) {
                        ll base = f[l][mid][S];
                        if (base <= NEG / 2) continue;
                        ll vr0 = f[mid + 1][r][0];
                        if (vr0 > NEG / 2) {
                            int id = S << 1;
                            ll val = base + vr0 + w[id];
                            if (c[id] == 0) { if (val > g0) g0 = val; }
                            else            { if (val > g1) g1 = val; }
                        }
                        ll vr1 = f[mid + 1][r][1];
                        if (vr1 > NEG / 2) {
                            int id = (S << 1) | 1;
                            ll val = base + vr1 + w[id];
                            if (c[id] == 0) { if (val > g0) g0 = val; }
                            else            { if (val > g1) g1 = val; }
                        }
                    }
                }
                f[l][r][0] = g0;
                f[l][r][1] = g1;
            } else {
                // 最终长度 t+1（>1）：把后缀 1 个字符拼到前缀状态之后
                int lim = 1 << t;           // 前缀 [l,mid] 的字符数恰为 t
                for (int mid = r - 1; mid >= l; mid -= km1) {
                    for (int S = 0; S < lim; S++) {
                        ll base = f[l][mid][S];
                        if (base <= NEG / 2) continue;
                        ll vr0 = f[mid + 1][r][0];
                        if (vr0 > NEG / 2) {
                            int id = S << 1;
                            ll val = base + vr0;
                            if (val > f[l][r][id]) f[l][r][id] = val;
                        }
                        ll vr1 = f[mid + 1][r][1];
                        if (vr1 > NEG / 2) {
                            int id = (S << 1) | 1;
                            ll val = base + vr1;
                            if (val > f[l][r][id]) f[l][r][id] = val;
                        }
                    }
                }
            }
        }
    }

    ll ans = NEG;
    for (int s = 0; s < smax; s++) ans = std::max(ans, f[1][n][s]);
    printf("%lld\n", ans);
    return 0;
}
