// 一本通 1702《异或运算》标程
//
// 题意：给定 X[1..n]、Y[1..m]，矩阵 A[i][j] = X[i] xor Y[j]。
// 每次询问矩形 i∈[u,d], j∈[l,r] 中第 k 大的 A 值。
//
// 思路（可持久化 01-Trie + 按位二分第 k 大）：
//   对 Y 建立可持久化 01-Trie（前缀版本 roots[r] 表示 Y[1..r]），
//   这样任意 Y 区间 [l,r] 上"某一位为某个值的元素个数"可以用
//   cnt(roots[r]) - cnt(roots[l-1]) 得到。
//
//   求第 k 大时从高位向低位贪心确定答案的每一位：
//   当前位答案取 1 能覆盖的元素个数 = Σ_{i=u..d} #{j∈[l,r] | (X[i]^Y[j]) 的当前位为 1}
//     = Σ_{i=u..d} #{j∈[l,r] | Y[j] 的当前位 = (X[i] 的当前位) ^ 1}。
//   若 k ≤ cnt1，则答案当前位为 1 并沿各 X[i] 对应的 "1 分支" 下钻；
//   否则 k -= cnt1，当前位为 0 并沿 "0 分支" 下钻。
//   重复 31 位即可得到答案。
//
// 参考来源：本题为 BZOJ 4103 / 2015 清华夏令营“异或运算”的经典题，
// 主流做法均为"可持久化 Trie + 逐位求第 k 大"。本实现依据该公开算法思路
// 自行编写，未直接照抄任何网络代码。
// 参考 URL（思路）：
//   https://www.cnblogs.com/ (可持久化 trie 求区间异或第 k 大 通用思路)
//   https://oi-wiki.org/string/trie/ (01-Trie 与可持久化 Trie)
//
// 复杂度：O((m + p*n) * 31)，n≤1000, m≤300000, p≤500，可行。

#include <cstdio>
#include <vector>
using namespace std;

static const int MAXB = 31; // X,Y < 2^31，二进制位 0..30

struct Node {
    int ch[2];
    int cnt;
};

static vector<Node> tr;
static vector<int> roots;
static vector<unsigned> X;

static int newNode() {
    Node n;
    n.ch[0] = n.ch[1] = 0;
    n.cnt = 0;
    tr.push_back(n);
    return (int)tr.size() - 1;
}

static int cloneNode(int from) {
    tr.push_back(tr[from]);
    return (int)tr.size() - 1;
}

// 在前缀版本 prev 的基础上插入 val，返回新版本根编号
static int insert(int prev, unsigned val) {
    int newRoot = cloneNode(prev);
    int cur = newRoot;
    tr[cur].cnt++;
    for (int b = MAXB - 1; b >= 0; b--) {
        int bit = (int)((val >> b) & 1u);
        int nxt = cloneNode(tr[prev].ch[bit]);
        tr[cur].ch[bit] = nxt;
        cur = nxt;
        prev = tr[prev].ch[bit];
        tr[cur].cnt++;
    }
    return newRoot;
}

// 查询矩形 i∈[u,d], j∈[l,r] 中第 k 大的值
static unsigned query(int u, int d, int l, int r, int k) {
    int rtL = roots[l - 1];
    int rtR = roots[r];

    vector<int> cur, prev;
    cur.reserve(d - u + 1);
    prev.reserve(d - u + 1);
    for (int i = u; i <= d; i++) {
        cur.push_back(rtR);
        prev.push_back(rtL);
    }

    unsigned ans = 0;
    for (int b = MAXB - 1; b >= 0; b--) {
        int cnt1 = 0;
        for (size_t i = 0; i < cur.size(); i++) {
            int xb = (int)((X[(size_t)u + i] >> b) & 1u);
            int want = xb ^ 1;
            cnt1 += tr[tr[cur[i]].ch[want]].cnt - tr[tr[prev[i]].ch[want]].cnt;
        }

        int bit;
        if (k <= cnt1) {
            bit = 1;
            for (size_t i = 0; i < cur.size(); i++) {
                int xb = (int)((X[(size_t)u + i] >> b) & 1u);
                int want = xb ^ 1;
                cur[i] = tr[cur[i]].ch[want];
                prev[i] = tr[prev[i]].ch[want];
            }
        } else {
            k -= cnt1;
            bit = 0;
            for (size_t i = 0; i < cur.size(); i++) {
                int xb = (int)((X[(size_t)u + i] >> b) & 1u);
                int want = xb;
                cur[i] = tr[cur[i]].ch[want];
                prev[i] = tr[prev[i]].ch[want];
            }
        }
        ans |= (unsigned)bit << b;
    }
    return ans;
}

int main() {
    int n, m;
    scanf("%d %d", &n, &m);

    X.resize((size_t)n + 1);
    for (int i = 1; i <= n; i++) {
        unsigned v;
        scanf("%u", &v);
        X[i] = v;
    }

    tr.reserve((size_t)(m + 1) * 32 + 10);
    roots.assign((size_t)m + 1, 0);
    tr.push_back(Node{0, 0, 0}); // 空树根 = 0
    for (int j = 1; j <= m; j++) {
        unsigned v;
        scanf("%u", &v);
        roots[j] = insert(roots[j - 1], v);
    }

    int p;
    scanf("%d", &p);
    while (p--) {
        int u, d, l, r, k;
        scanf("%d %d %d %d %d", &u, &d, &l, &r, &k);
        printf("%u\n", query(u, d, l, r, k));
    }
    return 0;
}
