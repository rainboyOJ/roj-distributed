// 一本通 1743《数羊》标程（C++17，stdin -> stdout）
//
// ============================ 参考来源（联网检索） ============================
// 本题按任务书要求先联网检索 C++ 解法。先直接检索题面原文（"小明每天晚上都在数羊"、
// "吵闹程度"、"一本通 1743 数羊" 等，CSDN / 博客园 / 牛客 / 洛谷 / Bing / 百度多路，
// 均未检索到针对 ybt 1743 的公开题解；同名 "数羊" 题（JZOJ5809、牛客 NC217902）
// 经核对均为不同题，不能作为来源）。随后按**题目本质**检索 —— 本题即「统计排列中
// i<j<k 且 a[i]<a[k]<a[j] 的三元组个数」（经典 132 计数），等价于 HDU 4000
// 「Fruit Ninja」（题面逐字相同："how many (x,y,z) can you find such that
// x < z < y"，即 i<j<k、a[i]<a[k]<a[j]），据此找到公开题解并按题面口径改写：
//   [1] https://blog.csdn.net/qq_41661919/article/details/86616531
//       《HDU 4000 Fruit Ninja（树状数组求逆序对、正序对 应用）》——
//       核心恒等式：对每个位置 i，设 pre_i = 左侧比 a[i] 小的个数、
//       last_i = 右侧比 a[i] 大的个数，则
//         ans = Σ_i [ C(last_i, 2) − pre_i * last_i ]。
//       解释：单调递增序对 (i,j,k), a[i]<a[j]<a[k]（123）或以 a[i] 为最小者的
//       全部右侧单调对共 C(last_i,2) 个；其中 a[i]<a[j]<a[k] 型（123 型）
//       有 pre_j * last_j 个（对每个 j 统计），两类相减即得 132 型。
//       来源特别提示「最终答案按交换律可化为所有加项之和减所有减项之和」，
//       故可在一次倒序遍历中累加，无需修改原式。
//   [2] https://blog.csdn.net/lanshan1111/article/details/86621294
//       《HDU4000 Fruit Ninja利用树状数组计数+组合数学》——同一恒等式
//       （"从右边比他大的数中挑选两个……然后用 sum1-sum2 即可"），
//       另给出 HDU 4000 官方样例答案（Case #1: 10, Case #2: 1），
//       本 std 对这两组样例逐字节复现通过（见 gen-report.md）。
//   来源结论一致、与题面定义一致，无冲突。
// 本 std 为在 [1][2] 恒等式基础上的**自写实现**（第一遍正序 BIT 求 pre[i]，
// 第二遍倒序 BIT 求 last[i] 并同一循环累加答案），未盲抄来源代码。
// =============================================================================
//
// 题面数据范围：第一行 N；第二行 N 个互不相同的正整数，是 1..N 的排列。
//   20%: N<=100；40%: N<=1000；60%: N<=100000；100%: N<=200000。
// 限制：1000 ms / 256 MB（config.json，与官方页 1000 ms / 262144 KB 一致）。
//
// 算法（O(N log N)，树状数组/树状数 BIT）：
//   记 pre_i  = #{ p < i : a[p] < a[i] }（左侧比它小的个数）
//       last_i = #{ p > i : a[p] > a[i] }（右侧比它大的个数）
//   答案 = Σ_i [ C(last_i,2) − pre_i * last_i ]
//   推导：
//     * C(last_i,2)：以 a[i] 为最小元素、在右侧任取两个比它大的元素所成的
//       三元组 (i,j,k)，a[i]<a[j], a[i]<a[k]，共 C(last_i,2) 个；
//       其中 j/k 的大小分两种：a[j]<a[k]（123 型，不符）与 a[j]>a[k]（132 型，符合）。
//     * 123 型的个数 = Σ_j pre_j * last_j（对中间元素 j 计数：左侧有条
//       pre_j 种选 i、右侧有 last_j 种选 k；132 型在按 i 计数时被算了 1 次，
//       按 j 计数时不会被算，故 132 型总数 = Σ_i C(last_i,2) − Σ_j pre_j*last_j，
//       而 Σ_j pre_j*last_j 也能写成在 i 的循环里用 pre_i*last_i 累加 —— 这正是
//       来源 [1] 提示的「交换律化简」，两项都只是标量求和，可同一遍完成。
//   实现：正序遍历 BIT（按值）得 pre_i 并累加 s1=Σ C(last_i,2)、s2=Σ pre_i*last_i。
//   需要先知道 last_i：倒序也可，但更简单做法是正序时先只求 pre_i 存起来，
//   再用「右侧比它大的个数 = (N-i) 个右侧元素中大于 a[i] 的个数」——
//   注意不能直接用 (N-i) 减「右侧比它小的个数」，因为右侧还有比它大的；
//   这里用两次遍历：第一次正序求 pre_i（存数组），第二次倒序求 last_i
//   （倒序 BIT：已插入的是右侧元素，查询「大于 a[i] 的个数」= 已插入总数 − 查询<=a[i]）。
//   两遍都是 O(N log N)，常数小；答案最大 C(200000,3) ≈ 1.33e15，
//   中间量 pre_i*last_i <= 1e10、累加 Σ 可能到 ~4e14 级别，必须 long long
//   （long long 上限 9.2e18，余量充足）。
//
// 复杂度：时间 O(N log N)（N=2e5 时两遍 BIT 约 2*2e5*18 次操作 + 一次排序，
//         远低于 1000 ms），空间 O(N)（BIT 与计数/压缩数组，约 4 * 200002 * 4B
//         ≈ 3.2 MB << 256 MB）。
//
// 健壮性（可选压缩，计划允许项）：题面【提示】保证第二行是 1..N 的排列，此时
//   可直接以值作 BIT 下标；为防评测数据意外越界，先按值排序求 rank（离散化），
//   对所有输入都只用 1..N 的下标访问 BIT，不会越界；合法输入下行为完全一致。

#include <algorithm>
#include <cstdio>

typedef long long ll;

const int MAXN = 200005;  // 题面上限 2e5 的安全余量（+5）

int n;
int a[MAXN];          // 原始输入
int vals[MAXN];       // 排序副本（离散化用）
int b[MAXN];          // 离散化后的值（rank，1..n）
int bit[MAXN];        // 树状数组（按 1..n 建）
ll pre[MAXN];         // pre[i]：左侧比 a[i] 小的个数

inline int lowbit(int x) { return x & (-x); }

void add(int x) {
    for (; x <= n; x += lowbit(x)) bit[x]++;
}

int sum(int x) {  // 前缀和：rank <= x 的已插入个数
    int s = 0;
    for (; x > 0; x -= lowbit(x)) s += bit[x];
    return s;
}

int main() {
    if (scanf("%d", &n) != 1) return 0;

    for (int i = 1; i <= n; i++) {
        scanf("%d", &a[i]);
        vals[i] = a[i];
    }

    // 离散化：b[i] = a[i] 在全体输入值中的排名（1..n）
    std::sort(vals + 1, vals + n + 1);
    for (int i = 1; i <= n; i++)
        b[i] = int(std::lower_bound(vals + 1, vals + n + 1, a[i]) - vals);

    // 第一遍：正序，求 pre[i]（左侧比它小的个数）
    for (int i = 1; i <= n; i++) {
        pre[i] = sum(b[i] - 1);
        add(b[i]);
    }

    // 第二遍：倒序，插入的是「右侧元素」，可同时求 last[i] 并累加答案
    for (int i = 1; i <= n; i++) bit[i] = 0;  // 清空 BIT（C 风格数组，重新置零）
    ll ans = 0;
    int inserted = 0;
    for (int i = n; i >= 1; i--) {
        // 右侧比 a[i] 大的个数 = 已插入总数 − 已插入中 <= a[i] 的个数
        ll last = inserted - sum(b[i]);
        ans += last * (last - 1) / 2 - pre[i] * last;
        add(b[i]);
        inserted++;
    }

    printf("%lld\n", ans);
    return 0;
}
