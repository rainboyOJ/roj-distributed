// 一本通 1816《取石子》 std
// 题面出处：http://ybt.ssoier.cn:8088/problem_show.php?pid=1816
// 来源说明：博客园/CSDN/搜索引擎共 4 轮检索均未找到公开 AC 代码（站点均为 JS 反爬或
//           无此题解），故本文件为**自研实现**；正确性依据见 gen-report.md：
//           数学推导 + 小规模游戏树穷举 + 单堆 Grundy DP 对照，全部一致。
//
// 算法（记 M = a+b）：
//   1) 若存在 a <= x_i <= b：先手直接取空该堆，立即获胜 -> Alice。
//   2) 否则把局面等价化简为"禁止落点 [a,b]"的公平组合游戏（把一堆留在 [a,b] 等于送对手
//      立即获胜，属自杀着法，可从着法集合中删去，胜负不变）：
//        - x_i < a            : 死堆，Grundy 0
//        - b < x_i < M        : 一步可杀，Grundy 1
//        - x_i >= M, r = x_i mod M：
//            a == 1 : Grundy = r
//            a >= 2 : r < a       -> 0
//                     r >= M - a  -> 1
//                     否则        -> 2 + (r - a) / a
//   3) Alice 胜 <=> 各堆 Grundy 异或和非 0。
//   该值域下 x_i <= 1e9，M <= 2e9，r 只需一次取模，单组 O(n)，总 O(sum n)。
#include <cstdio>
typedef long long ll;

int main() {
    int t;
    if (scanf("%d", &t) != 1) return 0;
    while (t--) {
        ll n, a, b;
        if (scanf("%lld %lld %lld", &n, &a, &b) != 3) return 0;
        ll xr = 0;
        bool alice = false;
        for (ll i = 0; i < n; i++) {
            ll x;
            scanf("%lld", &x);
            if (a <= x && x <= b) {      // 一步取空该堆，立即获胜
                alice = true;
                continue;
            }
            if (x < a) continue;         // 死堆：Grundy 0
            if (x < a + b) {             // b < x < M：一步可杀 -> 1
                xr ^= 1;
                continue;
            }
            ll M = a + b, r = x % M;
            if (a == 1) {
                xr ^= r;
            } else if (r < a) {
                /* Grundy 0 */
            } else if (r >= M - a) {
                xr ^= 1;
            } else {
                xr ^= 2 + (r - a) / a;
            }
        }
        puts((alice || xr) ? "Alice" : "Bob");
    }
    return 0;
}
