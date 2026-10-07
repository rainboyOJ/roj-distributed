// 一本通 1681《统计方案》标程
// 算法：折半搜索（meet in the middle）+ 费马小定理求逆元
// 思路来源（AC 代码改写）：
//   https://www.cnblogs.com/huangchenyan/p/11254762.html
//   （CSDN 转载镜像：https://blog.csdn.net/weixin_30932215/article/details/101673455）
//   该文为 XJOI 同题《统计方案》，题面与数据范围（n<=32, p<=1e9 质数, c<=1e9,
//   a[i]<p）与一本通 1681 完全一致。
//
// 对来源代码的修改与隐患修复（以题面为准）：
// 1. 原代码 dfs2 中 lower_bound 未命中时直接解引用迭代器，可能解引用 end()（UB，
//    最坏崩溃）。改为命中才累加（it != t.end() && it->first == sum）。
// 2. 原代码答案累加用 int/ll 混用且 `ans=(ans-1)%mod` 在 ans==0 时会得到负数，
//    改为 (ans - 1 + MOD) % MOD，保证非负。
// 3. 原代码 dfs1 对空集（sum=1）也调用 pow(sum,p-2)*c，本题 1<=p（p 为质数故 p>=2），
//    空集乘积 1 合法可求逆；但空集与空集配对会被统计（对应“至少取一个数”被违反），
//    故最后当 c==1 时需减去 1（双方都取空集的方案）。该逻辑保留，细节修正见 2。
// 4. p=2 等小质数、a[i] 可能等于 0 的情况：题面保证 a[i]<p 且 p 质数，a[i]>=1，
//    但输入未绝对排除 a[i]==0（防御性处理：乘积遇 0 直接归 0，不影响正确性）。
// 5. 输入 a[i] 读入后先 %p（防御超范围输入）。
// 6. c>=p 直接输出 0（余数不可能 >=p，题面 c 可达 1e9 而 p 最小 2）。
// 7. 使用 long long 全程（乘积中途取模防溢出），快速幂求逆元 a^(p-2) mod p。
//
// 复杂度：两半各 2^(n/2) 个乘积（n=32 时各 65536），前半排序去重 O(2^(n/2) log)，
// 后半每个乘积一次快速幂 O(log p) + 二分 O(log)，总约 65536*30*2 ≈ 4e6 次运算，1s 内轻松通过。

#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

typedef long long ll;
const ll MOD = 1000000007LL;

int n;
ll p, c;
ll a[40];

ll qpow(ll x, ll e, ll mod) { // 快速幂（费马小定理求逆元：x^(p-2) mod p）
    ll r = 1 % mod;
    x %= mod;
    while (e > 0) {
        if (e & 1) r = (__int128)r * x % mod; // __int128 防 (r*x) 溢出：r,x < 1e9，乘积 < 1e18 其实 ll 可容纳，双保险
        x = (__int128)x * x % mod;
        e >>= 1;
    }
    return r;
}

vector<ll> sLeft; // 前半：每个乘积 x 对应的“另一半需要”的值 c * x^{-1} mod p
vector< pair<ll,ll> > tab; // (需要值, 出现次数)，排序去重

void dfsLeft(int x, int r, ll prod) { // 枚举 [1..r] 的每个子集乘积
    if (x > r) {
        // 需要 prod * b ≡ c (mod p)，即 b ≡ c * prod^{-1}
        // prod 与 p 互质时（p 质数、prod%=p 且 prod!=0）逆元存在；
        // prod==0 时乘积必为 0，只有 c==0 才可能配对，此时另一半需含 0 因子，
        //   为统一处理：prod==0 且 c==0 时需要 b 任意（含 0 或不含 0 均可）——
        //   这种情况无法用单一目标值表达，但题面 a[i]<p 且为正整数，a[i]>=1，
        //   prod==0 仅在防御性输入（a[i]==0）时出现；正常数据不会触发。
        //   防御处理：prod==0 时跳过记录（与正常数据无交集）。
        if (prod == 0) return;
        ll need = qpow(prod, p - 2, p) * (c % p) % p;
        sLeft.push_back(need);
        return;
    }
    dfsLeft(x + 1, r, prod);                 // 不选 a[x]
    dfsLeft(x + 1, r, prod * a[x] % p);      // 选 a[x]
}

ll ans = 0;

void dfsRight(int x, int l, int r, ll prod) { // 枚举后半 [l..r] 的每个子集乘积并匹配
    if (x > r) {
        vector< pair<ll,ll> >::iterator it =
            lower_bound(tab.begin(), tab.end(), make_pair(prod, (ll)0));
        if (it != tab.end() && it->first == prod) // 修复：原代码可能解引用 end()
            ans = (ans + it->second) % MOD;
        return;
    }
    dfsRight(x + 1, l, r, prod);
    dfsRight(x + 1, l, r, prod * a[x] % p);
}

int main() {
    if (scanf("%d %lld %lld", &n, &p, &c) != 3) return 0;
    for (int i = 1; i <= n; i++) {
        if (scanf("%lld", &a[i]) != 1) a[i] = 1;
        a[i] %= p; // 防御：保证 a[i] < p
    }
    if (c >= p) { // 余数不可能 >= p（含 p<=1e9 < c<=1e9 的情况）
        printf("0\n");
        return 0;
    }
    int half = n / 2;
    dfsLeft(1, half, 1);
    sort(sLeft.begin(), sLeft.end());
    // 去重统计每个“需要值”出现次数
    for (size_t i = 0; i < sLeft.size(); ) {
        size_t j = i;
        while (j < sLeft.size() && sLeft[j] == sLeft[i]) j++;
        tab.push_back(make_pair(sLeft[i], (ll)(j - i)));
        i = j;
    }
    dfsRight(half + 1, half + 1, n, 1);
    // 双方都取空集（乘积 1）被统计了 1 次，对应“至少取一个数”被违反：
    // 仅当 1 ≡ c (mod p)，即 c % p == 1 时，需减去这 1 个方案。
    if (c % p == 1) ans = (ans - 1 + MOD) % MOD; // 修复：防负数
    printf("%lld\n", ans % MOD);
    return 0;
}
