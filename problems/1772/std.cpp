// 一本通 1772《动漫排序》
// 来源说明：本题为「信息学奥赛一本通 · 高手训练篇·五、动态规划(高手训练)」原题，
//   网络检索（Bing/百度/洛谷/CSDN 站内，关键词「一本通 1772 动漫排序 题解」、
//   题面特征句「小W最近迷上了日本动漫」「一部动漫的所有后继都必须排在它的后面」）
//   均未命中可用的公开题解/AC 代码（详见 gen-report.md 的检索记录），故本标程为
//   依据题面自研实现，并用题面样例（输入 1/5/... → 输出 2）验证通过。
//
// 题意：给定一棵以 1 为根的树，每个点的孩子已按「喜爱度从大到小」给出固定顺序。
//   求满足 ① 祖先必须排在子孙前面；② 同一父亲的孩子们按给定顺序出现
//   的 n 元排列个数，答案 mod 10007（10007 为质数）。
//
// 算法（树形 DP + 组合数，O(n)）：
//   设 f(u) = 子树 u 内部满足限制的排列数（子树内自成序列，u 必须最先出现），
//      sz(u) = 子树大小，孩子依次为 c1..ck，n_i = sz(c_i)，N_i = n_i + n_{i+1} + ... + n_k。
//   把子树 u 的排列看成「u + 把 k 个子树的合法序列拼接起来」：
//     每个子树的序列本身是 P_{c_i} 的线性扩展（其首元素必为 c_i），
//     拼接时只额外要求根的顺序 c1 < c2 < ... < ck（即各序列首元素出现的先后顺序）。
//   记 Cnt(n1..nk) 为「由 k 个长度 n_i 的序列洗牌、且首元素出现顺序为 1,2,...,k」的
//     洗牌方式数（与序列内容无关，只与长度有关），则
//       f(u) = Cnt(n1..nk) * prod_i f(c_i)。
//   Cnt 的递推：整串的前缀 1^m（m>=1，因为第 1 个序列的首元素必须最靠前）之后，
//     剩余部分是 (n1-m) 个「1 号序列的元素」插入到 (n2..nk) 的合法洗牌中，
//     且插在剩余部分首位的元素不能是 1 号序列的（否则与「前缀长度 m」重复计数），
//     故 Cnt(n1..nk) = Cnt(n2..nk) * sum_{m=1..n1} C(N-m-1, n1-m)
//                    = Cnt(n2..nk) * C(N-1, n1-1)      （Hockey-stick 恒等式）
//     其中 N = n1+...+nk；k=1 时 Cnt=1（也恰等于 C(N-1, n1-1)=C(n1-1,n1-1)=1）。
//   即 Cnt(n1..nk) = prod_{i=1}^{k} C(N_i - 1, n_i - 1)，
//   所以 f(u) = prod_{i=1}^{k} [ f(c_i) * C(N_i - 1, sz(c_i) - 1) ]。
//   答案 = f(1) mod 10007。
//   手算校验：题面样例中 f(1) = C(3,0)*C(2,1) = 2，与样例输出一致。
//
// 复杂度：每组数据 O(n)，n <= 1000；模数 10007 为质数且 > n，组合数用阶乘+费马小定理求逆元。

#include <cstdio>
#include <vector>

using namespace std;

const int MOD = 10007;
const int MAXN = 1005;  // 题面 n <= 1000，留安全余量

static long long fact[MAXN];
static long long inv_fact[MAXN];

static long long mod_pow(long long a, long long e) {
    long long r = 1 % MOD;
    a %= MOD;
    while (e > 0) {
        if (e & 1) r = r * a % MOD;
        a = a * a % MOD;
        e >>= 1;
    }
    return r;
}

static long long comb(int a, int b) {
    if (b < 0 || b > a || a < 0) return 0;
    return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD;
}

int main() {
    // 预处理阶乘与逆元（上限按题面上限 1000 开，多留余量）
    fact[0] = 1;
    for (int i = 1; i < MAXN; i++) fact[i] = fact[i - 1] * i % MOD;
    inv_fact[MAXN - 1] = mod_pow(fact[MAXN - 1], MOD - 2);
    for (int i = MAXN - 1; i >= 1; i--) inv_fact[i - 1] = inv_fact[i] * i % MOD;

    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T--) {
        int n;
        if (scanf("%d", &n) != 1) break;
        vector<vector<int> > ch(n + 1);
        for (int i = 1; i <= n; i++) {
            int tot;
            scanf("%d", &tot);
            ch[i].reserve(tot);
            for (int j = 0; j < tot; j++) {
                int x;
                scanf("%d", &x);
                ch[i].push_back(x);
            }
        }

        // 以 1 为根做非递归后序遍历（n <= 1000，避免深链递归爆栈）
        vector<int> order;
        order.reserve(n);
        vector<int> it(n + 1, 0);
        vector<char> vis(n + 1, 0);
        vector<int> stk;
        stk.reserve(n);
        vis[1] = 1;
        stk.push_back(1);
        while (!stk.empty()) {
            int u = stk.back();
            if (it[u] < (int)ch[u].size()) {
                int c = ch[u][it[u]++];
                if (c >= 1 && c <= n && !vis[c]) {
                    vis[c] = 1;
                    stk.push_back(c);
                }
            } else {
                order.push_back(u);
                stk.pop_back();
            }
        }

        vector<int> sz(n + 1, 0);
        vector<long long> f(n + 1, 1);
        // order 是后序遍历序列：孩子先于父亲入列，故按顺序正着处理即可自底向上
        for (size_t idx = 0; idx < order.size(); idx++) {
            int u = order[idx];
            long long total = 0;  // 所有孩子子树大小之和
            for (size_t j = 0; j < ch[u].size(); j++) total += sz[ch[u][j]];
            long long res = 1;
            long long rem = total;  // N_i：孩子 i 及其右侧兄弟的子树大小之和
            for (size_t j = 0; j < ch[u].size(); j++) {
                int c = ch[u][j];
                res = res * f[c] % MOD;
                res = res * comb((int)rem - 1, sz[c] - 1) % MOD;
                rem -= sz[c];
            }
            sz[u] = (int)total + 1;
            f[u] = res;
        }
        printf("%lld\n", f[1] % MOD);
    }
    return 0;
}
