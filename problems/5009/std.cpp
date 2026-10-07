// 一本通 1673《楼间跳跃》标程
//
// 思路来源（贪心 + 优先队列，等价于“鱼塘钓鱼”的升级版）：
//   1) https://blog.csdn.net/qq_36230375/article/details/136399431
//      信息学奥赛一本通高手训练 1673：楼间跳跃 贪心算法
//   2) https://blog.csdn.net/qq_45776662/article/details/107064392
//      楼间跳跃----贪心复习
// 题意/数据范围以任务书题目描述为准；代码为自行改写（C++17，stdin->stdout，快速读入）。
//
// 核心结论：价值相同的楼层等价于“每层一件、价值 v_i 的物品”。
// 到达第 k 栋楼需 k-1 次跳跃；进入每栋楼时落点所在层可免费取 1 件，
// 楼内每再多取 1 件需 1 单位时间。若在前缀 1..k 中每栋至少取 1 件、
// 合计取 T 件，则总时间恰为 T-1。因此问题化为：总件数不超过 m+1 时，
// 在某个前缀中每栋先取 1 件，其余件数按“每件价值 v_i”贪心选最大的，
// 用小根堆维护已选楼层的价值并淘汰最小值。
// 时间复杂度 O(n log n)。

#include <cstdio>
#include <queue>
#include <vector>
using namespace std;

static const int BUFSZ = 1 << 20;
static char ibuf[BUFSZ];
static int ipos = 0, ilen = 0;

static inline char getc() {
    if (ipos == ilen) {
        ilen = (int)fread(ibuf, 1, BUFSZ, stdin);
        ipos = 0;
        if (ilen == 0) return 0;
    }
    return ibuf[ipos++];
}

template <typename T>
static inline void readInt(T& x) {
    char c;
    do { c = getc(); } while (c != '-' && (c < '0' || c > '9'));
    int neg = 0;
    if (c == '-') { neg = 1; c = getc(); }
    x = 0;
    while (c >= '0' && c <= '9') {
        x = x * 10 + (c - '0');
        c = getc();
    }
    if (neg) x = -x;
}

struct Node {
    long long h;  // 额外可取件数（h_i - 1）
    long long v;  // 每件价值
};

struct Cmp {
    bool operator()(const Node& a, const Node& b) const {
        return a.v > b.v;  // 小根堆：价值最小的在堆顶
    }
};

int main() {
    long long n, m;
    readInt(n);
    readInt(m);
    ++m;  // 总件数预算 = 原时间 + 1

    long long ans = 0;    // 最优价值
    long long sum = 0;    // 当前策略总价值
    long long cnt = 0;    // 当前已选的“额外件”总数
    priority_queue<Node, vector<Node>, Cmp> pq;

    for (long long i = 1; i <= n; ++i) {
        long long h, v;
        readInt(h);
        readInt(v);

        // 到达第 i 栋至少需要 i 件（每栋 1 件），预算不足则更远的楼必然不可达
        if (i > m) break;

        sum += v;          // 进入第 i 栋，落点层免费取 1 件
        long long extra = h - 1;
        if (extra > 0) {
            sum += extra * v;
            cnt += extra;
            pq.push(Node{extra, v});
        }

        long long budget = m - i;  // 扣除每栋强制 1 件后，剩余的件数预算
        // 价值最小的整栋额外件可以被整体淘汰
        while (!pq.empty() && cnt - pq.top().h >= budget) {
            cnt -= pq.top().h;
            sum -= pq.top().h * pq.top().v;
            pq.pop();
        }
        // 若仍超出预算，则只淘汰最小值中的一部分
        if (cnt > budget) {
            long long over = cnt - budget;
            ans = max(ans, sum - pq.top().v * over);
        } else {
            ans = max(ans, sum);
        }
    }

    printf("%lld\n", ans);
    return 0;
}
