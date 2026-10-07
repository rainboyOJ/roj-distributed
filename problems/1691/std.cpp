// 一本通 1691《文章评分》：统计长度为 n 的小写串中，本质不同的长度为 m 的子串个数。
// 解法：双模哈希 + 排序去重（O(n log n)）。
// 参考来源（思路与结构参考，代码自行改写为 C++17、修去原帖笔误后重写验证）：
//   https://blog.csdn.net/ssl_hzb/article/details/83443171  （【字符串哈希】SSL_1211 好文章，双哈希）
//   https://blog.csdn.net/weixin_30362801/article/details/99026020 （同题 Pascal 双哈希+排序解法）
// 本题即 SSL 1211「好文章」（nodgd 文章评分），题面与数据范围一致。
// 正确性说明：双独立模哈希（mod 各约 1e9）碰撞概率上限约 (n-m+1)^2/(p1*p2) < 2e5^2/1e18 < 5e-8，
// 实际远小于此；若要求绝对正确可用后缀数组/后缀自动机，本题哈希足以通过。

#include <cstdio>
#include <cstring>
#include <algorithm>
using namespace std;

typedef long long ll;
typedef unsigned long long ull;

const ll MOD1 = 1000000007LL;
const ll MOD2 = 998244353LL;
const ll B1 = 131LL;
const ll B2 = 137LL;

const int MAXN = 200005;

int n, m;
char s[MAXN];
ll pow1[MAXN], pow2[MAXN];   // base 的幂
ll h1[MAXN], h2[MAXN];       // 前缀哈希
ll key1[MAXN], key2[MAXN];   // 每个长度为 m 的窗口的双哈希值
int idx[MAXN];

ll qpow(ll a, ll b, ll mod) {
    ll r = 1; a %= mod;
    while (b) {
        if (b & 1) r = r * a % mod;
        a = a * a % mod;
        b >>= 1;
    }
    return r;
}

// 比较函数：按 (key1, key2) 字典序
bool cmp(int a, int b) {
    if (key1[a] != key1[b]) return key1[a] < key1[b];
    return key2[a] < key2[b];
}

int main() {
    if (scanf("%d %d", &n, &m) != 2) return 0;
    if (scanf("%s", s + 1) != 1) s[1] = 0;

    pow1[0] = pow2[0] = 1;
    for (int i = 1; i <= n; i++) {
        pow1[i] = pow1[i - 1] * B1 % MOD1;
        pow2[i] = pow2[i - 1] * B2 % MOD2;
        // 字母映射到 1..26（'a'->1），避免前导零导致的哈希歧义
        ll c = s[i] - 'a' + 1;
        h1[i] = (h1[i - 1] * B1 + c) % MOD1;
        h2[i] = (h2[i - 1] * B2 + c) % MOD2;
    }

    int cnt = n - m + 1; // 窗口数
    ll invB1m = qpow(B1, m, MOD1); // 仅占位，排序法不需要逆元
    (void)invB1m;

    for (int i = 1; i + m - 1 <= n; i++) {
        int r = i + m - 1;
        key1[i] = (h1[r] - h1[i - 1] * pow1[m] % MOD1 + MOD1 * 2) % MOD1;
        key2[i] = (h2[r] - h2[i - 1] * pow2[m] % MOD2 + MOD2 * 2) % MOD2;
        idx[i] = i;
    }

    sort(idx + 1, idx + cnt + 1, cmp);

    ll ans = 0;
    for (int i = 1; i <= cnt; i++) {
        if (i == 1 || key1[idx[i]] != key1[idx[i - 1]] || key2[idx[i]] != key2[idx[i - 1]])
            ans++;
    }
    printf("%lld\n", ans);
    return 0;
}
