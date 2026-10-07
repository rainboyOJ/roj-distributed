// 一本通 1742 导线问题（《信息学奥赛一本通 · 高手训练篇》四、数据结构）
//
// 来源：
//   本题与经典题「降雷皇」题面逐字一致（哈蒙 / 导线 / 电光 / 电阻 / 123456789 / n<=1e5,
//   电阻值<=1e5），故以下两份公开题解即本题依据：
//     1) 「降雷皇」题解（cnblogs / butterflydew，2018-11-01）
//        https://www.cnblogs.com/butterflydew/p/9889096.html
//     2) 「2022.01.23 高手训练自训 ybt1742 导线问题」（CSDN / zhuyingye_123456，2022-01-23）
//        https://blog.csdn.net/zhuyingye_123456/article/details/122656500
//   两份题解算法一致：值域上用线段树维护 (最长长度, 方案数)，按“下标位置”计数。
//
// 题意：
//   求序列 a[1..n] 的最长严格上升子序列长度 L；若 type=1，再输出长度恰为 L 的严格上升
//   子序列个数（对 123456789 取模）。计数口径 = 按下标位置计数：同一取值出现在不同位置视为
//   不同方案（与原题/公开题解一致；见 gen-report.md 的样例与手算校验）。
//
// 算法：
//   令 dp[i] = 以 i 结尾的 LIS 信息 (len, cnt)：
//       best    = 值域上「取值严格小于 a[i]」的 (最大 len, 该 len 下的方案和)
//       dp[i]   = (best.len + 1, best.cnt)
//   随后把 dp[i] 合并到值域位置 a[i]（同 len 累加方案数，更长则覆盖）。
//   答案 = 值域全局合并结果。
//
//   实现用树状数组（BIT）维护值域上的可合并信息 (len, cnt)：merge 取 len 较大者，
//   len 相等时方案数相加（取模），len 全为 0 时代表“空序列”，方案数保持 1（哨兵）。
//   合并满足结合律/交换律且以 (0,1) 为单位元，故 BIT 前缀合并正确。
//
//   值域先离散化（lower_bound 定位），因此对任意整数取值范围（含重复、含 0/负值、或远大于
//   1e5 的值）都成立；严格上升即查询 rank-1 的前缀。
//   复杂度 O(n log n)，空间 O(n)。n<=1e5，1s 限制下余量充足。
//
// 编译：g++ -O2 -std=c++17 -o std std.cpp

#include <algorithm>
#include <cstdio>
#include <vector>
using namespace std;

static const int MOD = 123456789;

// 值域上的可合并信息：最长长度 + 该长度下的方案数
struct Node {
    int len;  // 最长严格上升子序列长度
    int cnt;  // 达到该长度的方案数（已取模）
};

// 单位元 / 哨兵：len==0 表示“空序列”，1 种方案（不选任何导线）
static const Node IDENT{0, 1};

// 合并：长度大者胜；长度相等则方案数相加；两侧都是空序列时方案数仍为 1
static inline Node mergeNode(const Node &x, const Node &y) {
    if (x.len > y.len) return x;
    if (y.len > x.len) return y;
    if (x.len == 0) return IDENT;  // 都是空序列（未使用的值域区间）
    int c = x.cnt + y.cnt;
    if (c >= MOD) c -= MOD;
    Node r;
    r.len = x.len;
    r.cnt = c;
    return r;
}

int main() {
    int n = 0, type = 0;
    if (scanf("%d %d", &n, &type) != 2) return 0;

    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        if (scanf("%d", &a[i]) != 1) a[i] = 0;
    }

    // 离散化：rank ∈ [1, K]，取值严格小于 a[i] 等价于 rank ∈ [1, rank(a[i])-1]
    vector<int> vals(a);
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    const int K = (int)vals.size();

    vector<Node> bit(K + 1, IDENT);  // BIT 节点 = 其覆盖叶子当前值的合并结果

    auto update = [&](int pos, const Node &v) {
        for (int i = pos; i <= K; i += i & (-i)) bit[i] = mergeNode(bit[i], v);
    };
    auto query = [&](int pos) {  // 前缀 [1, pos] 的合并结果
        Node res = IDENT;
        for (int i = pos; i > 0; i -= i & (-i)) res = mergeNode(res, bit[i]);
        return res;
    };

    for (int i = 0; i < n; i++) {
        int r = (int)(lower_bound(vals.begin(), vals.end(), a[i]) - vals.begin()) + 1;
        Node best = query(r - 1);  // 取值严格小于 a[i] 的部分
        Node cur;
        cur.len = best.len + 1;
        cur.cnt = best.cnt;
        update(r, cur);
    }

    Node ans = query(K);
    printf("%d\n", ans.len);
    if (type == 1) printf("%d\n", ans.cnt);
    return 0;
}
