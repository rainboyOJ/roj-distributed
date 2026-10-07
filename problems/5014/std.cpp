// 一本通 1678《独木桥》标程 (C++17, stdin -> stdout)
//
// 参考来源（思路）：
//   [1] https://blog.csdn.net/sz_165394732/article/details/83685222
//       （ssoj2910: 独木桥(bridge) 题解：相遇折返等价于穿过对方；任意时刻
//         每个人按初始位置排序的名次不变 -> 问题化为求 t 秒后两个有序数组
//         {右移者+t} 与 {左移者-t} 合并后的第 rank 小值）
//   [2] https://blog.csdn.net/qq_20057783/article/details/83720481
//       （2910: 独木桥(bridge)：号码牌交换思路与 AC 代码）
//
// 与来源代码的差异 / 来源隐患修复：
//   来源[2]的 AC 代码全程使用 int，其中 t*2、p+t 等中间量最大可达 2*10^9，
//   已贴近 int32 上限(2147483647)，属于溢出隐患；本实现所有运算使用
//   long long，彻底规避。实现上也不采用来源[2]的“二分轮回+分类讨论”
//   （分支繁多易错），而是采用来源[1]的名次不变结论 + 两个有序数组的
//   第 r 小划分二分，正确性更容易论证（详见 gen-report.md）。
//
// 算法：
//   1) 相遇折返 <=> 互相穿过但交换身份（经典等价，速度相同的点只会相向相遇），
//      因此任意时刻占据的位置多重集 = { p_i + t (d_i=1) } ∪ { p_i - t (d_i=0) }。
//   2) 折返模型中点与点永不穿越，按初始位置排序的名次不变；初始名次为 r 的孩子
//      在 t 秒后位于该多重集的第 r 小值处。
//   3) 每个询问用“两个有序数组划分”二分求第 r 小，O(log n)。
// 总复杂度 O((n + q) log n)，n,q <= 2*10^5。

#include <cstdio>
#include <cstdlib>
#include <vector>
#include <algorithm>
using namespace std;

const int MAXN = 200005;

int n, q, a, b;          // a/b: 右移者/左移者个数
int R[MAXN], L[MAXN];     // 右移者/左移者的初始位置（按位置升序存放）
int rk[MAXN];             // rk[k]: 孩子 k 按初始位置排序的名次（1 起）

// 求 {R[i]+t} ∪ {L[j]-t} 的第 r 小（R、L 各自升序，r 从 1 起）
static inline long long kth(long long t, int r) {
    // 左半部分取 R 的前 i 个与 L 的前 j=r-i 个，i 的可行区间：
    int lo = max(0, r - b), hi = min(a, r);
    // 谓词 h(i) = (j==0) || (i==a) || ( L[j-1]-t <= R[i]+t )
    // 随 i 增大 L[j-1] 递减、R[i] 递增 => h 单调（假->真），二分找最小真 i。
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        int j = r - mid;
        bool h = (j == 0 || mid == a ||
                  (long long)L[j - 1] - t <= (long long)R[mid] + t);
        if (h) hi = mid; else lo = mid + 1;
    }
    int i = lo, j = r - i;
    const long long NEG = -0x3f3f3f3f3f3f3f3fLL;  // -inf 哨兵
    long long ans = NEG;
    if (i > 0) ans = max(ans, (long long)R[i - 1] + t);
    if (j > 0) ans = max(ans, (long long)L[j - 1] - t);
    return ans;
}

int main() {
    scanf("%d", &n);
    vector<pair<int, int>> ps(n);   // (初始位置, 孩子编号)
    static int d[MAXN];
    for (int i = 0; i < n; i++) {
        scanf("%d", &ps[i].first);
        ps[i].second = i;
    }
    for (int i = 0; i < n; i++) scanf("%d", &d[i]);
    sort(ps.begin(), ps.end());
    a = b = 0;
    for (int i = 0; i < n; i++) {
        int id = ps[i].second;
        rk[id] = i + 1;
        if (d[id] == 1) R[a++] = ps[i].first;
        else            L[b++] = ps[i].first;
    }
    scanf("%d", &q);
    while (q--) {
        int k; long long t;
        scanf("%d %lld", &k, &t);
        printf("%lld\n", kth(t, rk[k]));
    }
    return 0;
}
