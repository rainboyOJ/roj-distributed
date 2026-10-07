// 一本通 1726《矩阵》标程（C++17，stdin -> stdout）
//
// ============================ 参考来源（联网检索） ============================
// 检索路径：
//   ① 题面特征句精确检索「有一个n×m的矩阵，初始每个格子的权值都为0，可以对矩阵执行两种操作」
//      （CSDN 站内搜索 API）⇒ 直接命中同题题解，并交叉定位到 **BZOJ 4500《矩阵》**；
//      BZOJ 4500 的题面与本题逐字相同（同样的 T≤5、1≤n,m,k≤1000、k≤n×m，同样的
//      Yes/No 样例），可确认本题 = BZOJ 4500 被《一本通·高手训练》收录后的编号 1726。
//      另据《信息学奥赛一本通高手训练 题解目录》
//      https://blog.csdn.net/qq_36230375/article/details/136483654 ，
//      1726《矩阵》位于「高手(三) 图论 · 第4章 差分约束系统」（1724 小K的农场、1725 账本核算、
//      1726 矩阵、1727 魔棒、1728 构造序列），与 BZOJ 4500 的差分约束定位一致。
//   ② 官方页实抓 http://ybt.ssoier.cn:8088/problem_show.php?pid=1726
//      标题「1726：矩阵」，限制 2000 ms / 262144 KB（与 config.json 的 2000 ms / 256 MB 一致），
//      样例与 content.md 完全相同 ⇒ 题面无误读。
//   ③ CSDN 站内搜「一本通 1726 题解」「ybtoj 1726 矩阵」均无独立题解（本题无公开一本通题解），
//      故按下述同题（BZOJ 4500）公开题解改写，头注已注明来路。
//
//   [1] https://blog.csdn.net/liyong1009s/article/details/103581952  《BZOJ 4500: 矩阵 带权并查集》
//   [2] https://blog.csdn.net/weixin_30307267/article/details/99117598
//       《BZOJ.4500.矩阵(差分约束 SPFA判负环 / 带权并查集)》（转载自
//        http://www.cnblogs.com/SovietPower/p/10755363.html）—— 同文给两套代码：
//         · 差分约束：r_i + c_j = k ⟹ r_i - (-c_j) ≤ k 且 -c_j - r_i ≤ -k，建边跑 SPFA 判负环；
//         · 带权并查集：全是"相等关系"，属十分特殊的差分约束，可直接带权并查集合并/判矛盾
//           （该文并注明"这题和 BZOJ1202 是一模一样的"）。
//   [3] https://blog.csdn.net/jpwang8/article/details/83590156  《bzoj4500 矩阵 差分约束系统》
//       —— 同题同建模：把 r_i + c_j = c 化为 r_i - (-c_j) ≤ c 与 -c_j - r_i ≤ -c 两条三角不等式。
//   [4] https://blog.csdn.net/weixin_30362233/article/details/101507919 《【BZOJ 4500】矩阵》
//       —— 同题，指出环上的约束相加必须为 0 才可能满足（本包 No 型数据的"矛盾环证书"即源于此）。
//   [5] https://blog.csdn.net/weixin_30756499/article/details/98551025 《bzoj4500:矩阵【差分约束】》
//       —— 同题，强调"矛盾 ⟺ 环上权值和不为 0"，与 [4] 一致。
//   以上来源结论一致、与题面一致，无冲突；本标程系按题面自行改写（改用 long long、1-indexed
//   固定根方向、增量式 64 位读入），并已用题面样例与分层数据核对，非盲抄。
// ============================================================================
//
// 题意与建模（content.md 明文）：
//   记第 i 行所在的"整行加 1 次数 − 整行减 1 次数"为 r_i（可为任意整数，因为加减可以互相抵消，
//   故操作序列是否存在 ⟺ 是否存在整数 r_i, c_j），第 j 列同记为 c_j。则每个限制 (x,y,c) 就是
//       r_x + c_j = c 。
//   这是"全等值关系"的线性系统，可行性 = 是否存在整数解。做法（来源 [1][2] 的带权并查集）：
//     把每一行、每一列看成一个点（行点 1..n，列点 n+1..n+m），并令列点 n+j 的"点值"取 -c_j，
//     则限制化为「点值(x) − 点值(n+y) = c」这种**带符号差值等式**，正是带权并查集能维护的形式：
//       · 同一集合内：检查 值(x) − 值(n+y) == c，不等 ⇒ 矛盾 ⇒ No；
//       · 不同集合：合并两棵并查集树，新根到新父的偏移 = c + val[y'] − val[x']。
//   （等价说法：二部图上每条"格点约束"是一条边，可行 ⟺ 每个连通分量能一致地赋点值，
//      ⟺ 任一闭合交替走法的交替和全为 0。）
//   正确性：约束全为整数等式，解在有理数域存在则最短路/并查集给出的偏移皆为整数，故整数可解性
//   与实数可解性一致；矛盾判据（环上差值之和 ≠ 0）等价于无解。
//
// 数据范围（content.md 【输入】【提示】）：T ≤ 5；1 ≤ n,m,k ≤ 1000 且 k ≤ n×m；
//   c 的区间题面未给（只写"整数 c"），标程用 long long 承载（见 gen-report.md 风险点）。
// 复杂度：每组 O((n+m) + k·α)，T ≤ 5、n+m ≤ 2000、k ≤ 1000 ⇒ 远低于 2000 ms；
//   内存 O(n+m) ≤ 2000 个 long long ≈ 32 KB ≪ 256 MB。

#include <cstdio>

typedef long long ll;

const int MAXV = 2005;  // n + m <= 2000

int fa[MAXV];
ll val[MAXV];  // val[x] = 值(x) − 值(父亲(x))；路径压缩后即 值(x) − 值(根(x))

// 带权并查集：返回根，并顺带把 val[x] 压缩为 值(x) − 值(根)
int find(int x)
{
    if (fa[x] == x) return x;
    int p = fa[x];          // 必须在递归前记下父亲：递归后 val[p] 已是压缩值
    fa[x] = find(p);
    val[x] += val[p];
    return fa[x];
}

int main()
{
    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T-- > 0)
    {
        int n, m, k;
        if (scanf("%d %d %d", &n, &m, &k) != 3) return 0;

        const int tot = n + m;
        for (int i = 1; i <= tot; ++i) { fa[i] = i; val[i] = 0; }

        bool ok = true;
        for (int t = 0; t < k; ++t)
        {
            int x, y;
            ll c;
            scanf("%d %d %lld", &x, &y, &c);
            if (!ok) continue;  // 已判矛盾也须把本组输入读完

            const int a = x;        // 行点
            const int b = n + y;    // 列点（其点值取 −c_j）
            int ra = find(a), rb = find(b);
            if (ra == rb)
            {
                // 同集合：值(a) − 值(b) 必须恰好等于 c
                if (val[a] - val[b] != c) ok = false;
            }
            else
            {
                // 合并：令 fa[ra] = rb；需 值(a) − 值(b) = c
                //   值(a) = val[a] + 值(ra)，值(b) = val[b] + 值(rb)
                //   ⇒ val[ra] = 值(ra) − 值(rb) = c + val[b] − val[a]
                fa[ra] = rb;
                val[ra] = c + val[b] - val[a];
            }
        }
        puts(ok ? "Yes" : "No");
    }
    return 0;
}
