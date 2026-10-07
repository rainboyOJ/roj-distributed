// 一本通 1781《死亡之树》标程（目标 ROJ 题号 1781）
//
// 【题意】
//   给定 n 个点、m 条无向边的简单图（保证无重边），n<=10, m<=45。
//   若图中「若干个点与连接它们的边」组成一棵恰含 n 个节点、k 个叶子的树，称为死亡之树。
//   求不同的死亡之树棵数。
//   - 叶子定义：度数为 1 的节点。
//   - 两棵树相同：点集与边集完全相同（摆放/旋转画法不同不改变这棵树）。
//   因此本题所求 = 图 G 中「恰好含 k 个叶子」的**生成树**（点集为全体 n 个点）的棵数（按标号计数）。
//   —— 与两个样例吻合：K3,k=2 → 3（3 条路径）；K4,k=3 → 4（4 个星形）。
//
// 【标程来源】
//   原题出处（博客园，题面文字与本题 content.md 逐字一致）：
//     https://www.cnblogs.com/rabbit1103/p/9754970.html
//     （rabbit1103《死亡之树》，含题意、样例、数据范围 n<=10 与状压 DP 代码）
//   同文 CSDN 转载（同款代码，可交叉核对）：
//     https://blog.csdn.net/weixin_34146805/article/details/94736605
//   本题即上述「死亡之树」（小蛤 向树专题发起攻击），非改编题；原始解法即
//   f[点集][叶子集] 的状压 DP（原文复杂度标注 O(4^N + N^2*3^N)）。
//   本文件在读懂原解后**重写**为 C++17 风格（数组下标 0-based、显式边界处理、
//   加注释说明去重原理），逻辑与原解一致，并用闭式结论（Cayley n^{n-2}、
//   K_n 的哈密顿路 n!/2、星形 n）交叉验证，见 gen-report.md。
//
// 【解法与正确性】
//   f[mask][leaf] = 点集为 mask、叶子集合恰为 leaf 的树的棵数。
//   关键去重：规定「每次加入的新点必须是当前树中编号最小的叶子」。
//   于是枚举新树叶子集中编号最小的点 j（j = lowbit(leaf)），j 是最后加入的点；
//   设它在树中唯一邻居为 k（k 的度数在加入 j 后 >=2，故 k 不是新树的叶子，即 k∉leaf），
//   去掉 j 得到旧树，旧树叶子集有两种可能：
//     (a) k 在旧树中度数 >=2：叶子集不变 → leaf\{j}
//     (b) k 在旧树中度数 ==1（叶子）：加入 j 后升为 2 度不再是叶子 → leaf\{j}∪{k}
//   即 f[mask][leaf] = Σ_{j=min(leaf)} Σ_{k∈mask\leaf, (j,k)∈E} ( f[mask\j][leaf\j] + f[mask\j][leaf\j∪{k}] )
//   2 点情形（一条边）不满足「k∉leaf」（两点都是叶子），作为 base 单独置 f[{x,y}][{x,y}]=1。
//   由于「按最小编号叶子逐步剥离」对每棵树给出唯一的剥离序列，每棵树恰被计一次，无重无漏。
//   复杂度 Σ_mask 2^{|mask|}·n = O(n·3^n) <= 10·59049 ≈ 6e5，n<=10 时远小于 1s。
//   答案 = Σ_{|leaf|=k} f[full][leaf]。
//
// 编译：g++ -O2 -std=c++17 -o std std.cpp
// 运行：std < problem1.in

#include <cstdio>

static int n, m, K;
static int adj[12][12];              // 邻接矩阵，1 表示有边
static long long f[1 << 10][1 << 10]; // f[点集][叶子集]

int main() {
    if (scanf("%d %d %d", &n, &m, &K) != 3) return 0;
    for (int i = 0; i < m; i++) {
        int a, b;
        scanf("%d %d", &a, &b);
        --a; --b;                     // 转 0-based
        adj[a][b] = adj[b][a] = 1;    // 无向图（题面保证无重边）
    }

    const int full = (1 << n) - 1;

    // 按 mask 从小到大递推：mask 去掉一个点后必更小，故顺序正确
    for (int mask = 1; mask <= full; mask++) {
        if (__builtin_popcount(mask) == 2) {          // base：恰两点且相邻
            int x = __builtin_ctz(mask);
            int y = __builtin_ctz(mask ^ (1 << x));
            if (adj[x][y]) f[mask][mask] = 1;         // 一条边：两点都是叶子
            continue;
        }
        for (int leaf = mask; leaf; leaf = (leaf - 1) & mask) {
            int j = __builtin_ctz(leaf);              // 最后加入的点 = 编号最小的叶子
            int jb = 1 << j;
            int rest = mask ^ jb;                     // 旧树的点集
            int oldLeaf = leaf ^ jb;                  // 情形 (a)：k 原非叶子
            for (int k = 0; k < n; k++) {
                int kb = 1 << k;
                if (!(mask & kb) || (leaf & kb)) continue;  // k ∈ mask \ leaf
                if (!adj[j][k]) continue;                   // (j,k) 必须是图中的边
                f[mask][leaf] += f[rest][oldLeaf]              // (a) k 度 >=2
                               + f[rest][oldLeaf | kb];        // (b) k 原是叶子
            }
        }
    }

    long long ans = 0;
    for (int leaf = 1; leaf <= full; leaf++)
        if (__builtin_popcount(leaf) == K) ans += f[full][leaf];
    printf("%lld\n", ans);
    return 0;
}
