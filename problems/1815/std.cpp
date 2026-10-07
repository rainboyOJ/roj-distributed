/*
 * 一本通 1815 「放石子」
 * 题面来源: .ybt-import/staging/1815/content.md
 * 官方题面页: https://ybt.ssoier.cn/problem_show.php?pid=1815
 *            (信息学奥赛一本通 · 高手训练篇 · 六、数学基础(高手训练))
 *
 * 检索说明 (第 1 轮即命中同题 AC 代码, 本文件为按其改写并整理注释):
 *   1. CSDN 站内搜索 API「一本通 1815 放石子」→ 命中
 *      https://blog.csdn.net/weixin_44346868/article/details/103465983
 *      《放石子's 题解》, 作者自述「来自信息学奥赛一本通 T1815」, 题面与本 content.md
 *      完全一致, 并附完整 AC 代码 (SG + 异或线性基 + bitset), 本 std 按其算法重写。
 *   2. 该题解亦指出题面歧义: 「对于每条满足颜色 e∈S 的出边 i」未写明是点 x 的出边,
 *      需按「x 的出边」理解 (题解中自加的括号), 否则题目无法作答。本实现按此理解,
 *      与官方样例一致 (样例答案 1)。
 *
 * 算法 (SG 定理 + 异或线性基, 逆拓扑序):
 *   - q 颗石子互相独立 (每步只动一颗) → 答案 = XOR_{石子 p} sg[p]; 非 0 先手胜, 否则后手胜。
 *   - 出度为 0 的点: 无操作 → sg = 0。
 *   - 对点 x, 对每个颜色 c 记
 *       h_c = XOR_{x->u 且颜色为 c 的每条边} sg[u]
 *     (一次操作若选 c∈S, 则同色所有出边终点都落子, 局面 = 这些子局面的和 → XOR)。
 *     一次操作选颜色集 S 后得到的局面 SG 值 = XOR_{c∈S} h_c, 故 x 的可达 SG 值集合
 *     = span{h_c} (GF(2) 线性子空间), 于是 sg[x] = mex(span{h_c})。
 *   - 线性基按最高位主元插入 (每个基向量最高位即其主元位, 主元互异):
 *       * 若位置 0..j-1 全为主元, 则 0..2^j-1 全在 span 中 (归纳: 基向量 b_j=2^j XOR r,
 *         r<2^j 已在 span → 2^j 在 span, 子空间对 XOR 封闭);
 *       * 若位置 j 非主元, 则 2^j ∉ span (任何基向量子集的 XOR 最高位 = 所用最大主元 ≠ j)。
 *     故 mex(span) = 2^{j*}, j* = 最小非主元位置 (即题解做法: 找最小线性无关位并置 1)。
 *   - 位宽估计: sg[x] = 2^{e(x)}; e(x) = k 要求 x 有 e 为 0..k-1 的出边终点 (各至少一条,
 *     且不同 e 的终点互异), 于是 outdeg(x) ≥ e(x) ≥ ... 归纳得 e(x) ≤ outdeg(x) ≤ n-1,
 *     即 sg < 2^n (n ≤ 200 → 200 位)。本实现取 W = 512 位 (题面上限 × 2.56 安全系数)。
 *     (附带结论: m 给定时 e 的实际可达上界约 sqrt(2m) ≈ 99 (m=5000), 数据 problem9/10
 *      专门构造到 2^99 量级; 由 outdeg(x) ≥ e(x) 与 "出边条数求和 ≤ m" 即得该界。)
 *   - 复杂度: 每个 (点, 颜色) 对至多插入一次, 每次插入 O(n/64) 次 W/64 位异或
 *     → 最坏 O(m · n²/64), n=200, m=5000 时 < 1e7 次字操作, 远低于 1s 限制。
 *
 * 编译: g++ -O2 -std=c++17 -o std std.cpp
 * 运行: ./std < problem1.in   (输出 1/0 一行)
 */
#include <cstdio>
#include <bitset>
#include <queue>
#include <unordered_map>
#include <vector>
using namespace std;

static const int W = 512;              /* 位宽: n ≤ 200 按题面上限 ×2.56 安全系数 */
typedef bitset<W> BS;

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 1;

    /* 反图: rev[t] 存 (起点 s, 颜色 c), 对应原边 s->t; 便于逆拓扑序自底向上处理 */
    vector<vector<pair<int, int> > > rev(n + 1);
    vector<int> outdeg(n + 1, 0);
    for (int i = 0; i < m; ++i) {
        int s, t, c;
        if (scanf("%d %d %d", &s, &t, &c) != 3) return 1;
        rev[t].push_back(make_pair(s, c));
        ++outdeg[s];
    }

    /* ex[x][c] = XOR_{x->u 颜色为 c} sg[u] (同色多边逐条异或累积) */
    vector<unordered_map<int, BS> > ex(n + 1);
    vector<BS> sg(n + 1);              /* 默认全 0 (出度为 0 的点) */

    /* 逆拓扑序 (Kahn): 初值 = 原图出度为 0 的点 (无操作, sg = 0) */
    queue<int> que;
    vector<int> deg = outdeg;
    for (int i = 1; i <= n; ++i)
        if (deg[i] == 0) que.push(i);

    vector<BS> basis(W);
    vector<char> pivot(W);
    while (!que.empty()) {
        int x = que.front();
        que.pop();
        if (outdeg[x] > 0) {
            /* 插入线性基, 找最小非主元位置 j*, 令 sg[x] = 2^{j*} = mex(span) */
            for (int i = 0; i < W; ++i) pivot[i] = 0;
            for (unordered_map<int, BS>::iterator it = ex[x].begin(); it != ex[x].end(); ++it) {
                BS v = it->second;
                for (int i = W - 1; i >= 0; --i) {
                    if (!v[i]) continue;
                    if (!pivot[i]) { pivot[i] = 1; basis[i] = v; break; }
                    v ^= basis[i];
                }
            }
            for (int j = 0; j < W; ++j)
                if (!pivot[j]) { sg[x].set(j); break; }
        }
        /* x 已求出 sg[x]: 回传给它所有原图前驱 y (原边 y->x, 颜色 z) */
        for (size_t k = 0; k < rev[x].size(); ++k) {
            int y = rev[x][k].first, z = rev[x][k].second;
            ex[y][z] ^= sg[x];
            if (--deg[y] == 0) que.push(y);
        }
    }

    int qn;
    if (scanf("%d", &qn) != 1) return 1;
    BS total;
    for (int i = 0; i < qn; ++i) {
        int a;
        if (scanf("%d", &a) != 1) return 1;
        total ^= sg[a];
    }
    printf("%d\n", total.any() ? 1 : 0);
    return 0;
}
