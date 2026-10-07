// 一本通 1753《区间连通性》 标程
// -----------------------------------------------------------------------------
// 题目来源：信息学奥赛一本通 · 高手训练篇 · 四、数据结构(高手训练)
//   官方 OJ 页面：http://ybt.ssoier.cn:8088/problem_show.php?pid=1753
//   （页面标题「1753：区间连通性」，限制 1000ms / 256MB）
//
// 题面：依次执行 n 个操作。操作 1 x y 向集合中加入区间 (x,y)，保证新加入的区间
//       长度严格大于此前所有区间；操作 2 a b 询问第 a 个区间与第 b 个区间之间是否
//       存在一条路径。两区间 (a,b)、(c,d) 相邻当且仅当 c<a<d 或 c<b<d。
//
// 依据：网上未检索到本题（一本通 1753）的公开题解，故自研。
//
// 语义说明（关键）：
//   题面把「两个区间」记为 (a,b)、(c,d)，并给出条件 c<a<d 或 c<b<d（(a,b) 的一个
//   端点落在 (c,d) 的开区间内）。该条件对「(a,b) 与 (c,d) 是否相邻」而言是对称的：
//   两区间只要**交叠长度 > 0**，就必有一个端点严格落在对方开区间内
//     · 交错（相交但互不包含）：双向都满足；
//     · 包含（(a,b)⊂(c,d) 或 (c,d)⊂(a,b)）：内层的一个端点落在外层开区间内。
//   反之，若两区间只「端点相切」（如 (1,5) 与 (5,11)）或不相交，则没有任何端点严格
//   落在对方开区间内，二者不相邻。因此「可达」关系即标准的区间相交连通性：
//   **两区间连通 ⟺ 两区间的交集长度 > 0**（端点相切不算）。
//
// 算法：
//   并查集维护连通块；由于同一连通块内所有区间的并集恰是一段连续的线段（区间相交
//   图的连通分量其并集无空隙），用一个有序集合按左端点维护各连通块的「线段 [L,R]」。
//   加入新区间 (x,y) 时，凡与该线段正长度相交（L<y 且 R>x）的线段都与新点合并，
//   合并后线段取并集；被合并的线段从集合中删除（每条线段只被删除一次）。
//   查询即判断两区间并查集根是否相同。
//   复杂度 O(n log n)。
//
// 说明：本题的「新加入区间长度严格大于此前所有区间」这一条件对上述（无向）连通性
//   建模并非必需，但它保证了区间集合的良好结构（也用于数据构造）。若评测方采用
//   「有向可达」语义，则需另做处理，见 gen-report.md 的风险说明。
#include <cstdio>
#include <vector>
#include <map>
#include <algorithm>
#include <utility>
using namespace std;
typedef long long ll;

// 并查集（路径压缩 + 按大小合并）
struct DSU {
    vector<int> p, sz;
    void init(int n) { p.resize(n + 1); sz.assign(n + 1, 1); for (int i = 0; i <= n; i++) p[i] = i; }
    int find(int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; }
    void uni(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return;
        if (sz[a] < sz[b]) swap(a, b);
        p[b] = a; sz[a] += sz[b];
    }
};

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    DSU dsu; dsu.init(n + 1);

    // 连通块线段：左端点 L -> (右端点 R, 该块的并查集代表元)
    map<ll, pair<ll, int> > segs;

    int cnt = 0; // 已加入的区间个数
    for (int i = 0; i < n; i++) {
        int op; ll x, y;
        scanf("%d %lld %lld", &op, &x, &y);
        if (op == 1) {
            cnt++;
            ll nl = x, nr = y;
            // 找到第一个可能与 (x,y) 正长度相交的线段
            map<ll, pair<ll, int> >::iterator it = segs.upper_bound(x); // 第一个 L > x
            if (it != segs.begin()) {
                map<ll, pair<ll, int> >::iterator pit = prev(it);
                if (pit->second.first > x) it = pit; // 该线段包含 x（R>x）
            }
            // 自 it 起，所有满足 L < y 的线段都与 (x,y) 相交（R > x 自动成立）
            while (it != segs.end() && it->first < y) {
                nl = min(nl, it->first);
                nr = max(nr, it->second.first);
                dsu.uni(cnt, it->second.second);
                it = segs.erase(it);
            }
            segs[nl] = make_pair(nr, dsu.find(cnt));
        } else {
            int a = (int)x, b = (int)y;
            puts(dsu.find(a) == dsu.find(b) ? "YES" : "NO");
        }
    }
    return 0;
}
