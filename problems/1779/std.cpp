// 一本通 1779《第K小数》 标程（C++17）
// ---------------------------------------------------------------------------
// 题目身份与来源（网络检索结果，均已实取正文核对）：
//   [1] 官方题面页（权威口径，实测 time 1000 ms / memory 262144 KB，
//       提交 184 / 通过 60）：http://ybt.ssoier.cn:8088/problem_show.php?pid=1779
//   [2] 同源原题：JZOJ P3458《密码》/【NOIP2013模拟9.29】密码，
//       https://blog.csdn.net/ssl_qyh0ice/article/details/81104827
//       题面「给你一个长度不超过17的由0~9组成的无前导0的字符串S，S中的数字排列组成的
//       无前导零的能被17整除的整数中字典序第K小的那个数就是密码」，数据范围
//       「40%: |S|<=12, K<=2*10^6；100%: |S|<=17, K<=17!」，与本题【提示】逐字一致；
//       样例也完全一致（2242223 2 -> 2242232；17 1 -> 17）。
//       => 可判定 一本通 1779 与 JZOJ P3458 同源（同一题），故本题有公开解法。
//   [3] 其余同题解（同一 JZOJ 题，交叉印证）：【NOIP2013模拟9.29】密码
//       https://blog.csdn.net/eric1561759334/article/details/81104576
//       https://blog.csdn.net/weixin_30566063/article/details/95748886
//
// 来源 [2] 给出的做法：把每个数位当作**位置**做二进制状压 DP（2^17 * 17），
//   最后按每个数字的重数除以 (重数)! 把「按位置的排列数」折算成「不同字符串数」。
//
// 本标程改写点（等价、更直接，避免阶乘折算）：
//   状态直接用**数字重数（multiset）** 表示，而非「选了哪些位置」。设
//     H(S)[t] = 用重数 S 里的数字能拼出的**不同字符串**中，数值 ≡ t (mod 17) 的个数。
//   按最低位递推：X = 10*X' + d（X' 为重数 S\{d} 的排列），
//     X ≡ t  <=>  X' ≡ (t-d) * 10^{-1} (mod 17)，10^{-1} ≡ 12 (mod 17)，
//   故 H(S)[t] = Σ_{d 在 S 中} H(S\{d})[ (t-d)*12 mod 17 ]，H(∅)[0] = 1。
//   由于只按**数字取值**枚举分支，相同数字不会被重复计数，天然得到「不同字符串数」，
//   无需来源 [2] 的除以重数阶乘。状态数 = ∏(c_i+1)（对 |S|<=17 至多约 1.8 万）。
//
// 求解：从高位到低位贪心。固定前缀值 p（mod 17）、剩余重数 R（|R|=m），
//   在当前位置试放数字 d（首位不得为 0），该分支的方案数
//     cnt = H(R\{d})[ (-(p*10+d) * 10^{m-1}) mod 17 ]，
//   若 K > cnt 则 K -= cnt 试下一个 d，否则定下 d 继续下一位。
//
// 复杂度：状态数 * 17 * 10，|S|=17 时约 3e6 次加法，远低于 1000 ms 限制。
// 输出：一行，即第 K 小数（数据保证有解）。
// ---------------------------------------------------------------------------
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <array>
#include <unordered_map>

using namespace std;
typedef long long ll;

static const int MOD = 17;
static const int INV10 = 12;              // 10 * 12 = 120 ≡ 1 (mod 17)

static unordered_map<uint64_t, array<ll, MOD> > memo;

// 把 10 个数字的重数（每个 <= 17）打包成 64 位 key
static inline uint64_t encode(const int c[10]) {
    uint64_t k = 0;
    for (int i = 0; i < 10; i++) k = (k << 5) | (uint64_t)c[i];
    return k;
}

// 返回 H(c)[0..16]
static array<ll, MOD> H(const int c[10]) {
    uint64_t key = encode(c);
    unordered_map<uint64_t, array<ll, MOD> >::iterator it = memo.find(key);
    if (it != memo.end()) return it->second;

    array<ll, MOD> res;
    for (int t = 0; t < MOD; t++) res[t] = 0;

    bool empty = true;
    for (int d = 0; d < 10; d++) if (c[d]) { empty = false; break; }

    if (empty) {
        res[0] = 1;
    } else {
        for (int d = 0; d < 10; d++) {
            if (!c[d]) continue;
            int nc[10];
            memcpy(nc, c, sizeof(nc));
            nc[d]--;
            array<ll, MOD> sub = H(nc);
            for (int t = 0; t < MOD; t++) {
                int src = (int)((ll)(((t - d) % MOD + MOD) % MOD) * INV10 % MOD);
                res[t] += sub[src];
            }
        }
    }
    memo[key] = res;
    return res;
}

int main() {
    char s[64];
    ll K;
    if (scanf("%s %lld", s, &K) != 2) return 0;

    int n = (int)strlen(s);
    int c[10];
    for (int i = 0; i < 10; i++) c[i] = 0;
    for (int i = 0; i < n; i++) c[s[i] - '0']++;

    ll pow10mod[24];
    pow10mod[0] = 1;
    for (int i = 1; i <= n; i++) pow10mod[i] = pow10mod[i - 1] * 10 % MOD;

    char ans[64];
    int alen = 0;
    int p = 0;                              // 已固定前缀 mod 17

    for (int i = 0; i < n; i++) {
        int m = 0;                          // 剩余数字个数
        for (int d = 0; d < 10; d++) m += c[d];

        bool placed = false;
        for (int d = 0; d < 10; d++) {
            if (!c[d]) continue;
            if (i == 0 && d == 0) continue; // 无前导零
            int np = (p * 10 + d) % MOD;
            int need = (int)((ll)((MOD - np) % MOD) * pow10mod[m - 1] % MOD);
            c[d]--;
            array<ll, MOD> sub = H(c);
            c[d]++;
            ll cnt = sub[need];
            if (K > cnt) {
                K -= cnt;
            } else {
                ans[alen++] = (char)('0' + d);
                p = np;
                c[d]--;
                placed = true;
                break;
            }
        }
        if (!placed) break;                 // 题面保证有解，理论不可达
    }

    ans[alen] = '\0';
    printf("%s\n", ans);
    return 0;
}
