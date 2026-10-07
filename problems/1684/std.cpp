// 一本通 1684《翻转序列》标程
// 参考来源（思路/代码）: https://blog.csdn.net/w15251243789/article/details/101431061
//   （原博转载自 https://www.cnblogs.com/wzztabaorz/articles/11410549.html）
//
// 算法：迭代加深 + IDA* 估价函数。
//   设当前序列相邻两项 a[i], a[i+1] 中 |a[i]-a[i+1]| != 1 的对数（坏邻接数）为 h。
//   一次前缀翻转只改变「翻转块末端与后继之间」这一处邻接关系（块内邻接只是方向反转，
//   差的绝对值不变），因此每次操作至多把坏邻接数减少 1，故 h 是剩余步数的可采纳下界。
//   h == 0 时整个排列必为 1..n 升序（因为序列是 1..n 的排列，相邻差全为 1 只能对应升序）。
//   在深度上限 deep 内做 DFS，用 "tot + h > deep" 剪枝，并跳过与上一步相同的翻转（纯撤销）。
//
// 题面数据范围：t = 5，n <= 23。最坏翻转数不超过 16（pancake number P(23) = 16），
// 该 IDA* 在本范围内可快速收敛。
#include <iostream>
#include <algorithm>
#include <cstdlib>
using namespace std;

static int n;
static int a[25];
static bool found;
static int deep;

// 当前已用步数 tot，上一步翻转长度 p（0 表示无上一步）。
static void dfs(int tot, int p) {
    if (found) return;

    // 估价：坏邻接数 h。
    int h = 0;
    for (int i = 1; i < n; ++i) {
        if (abs(a[i] - a[i + 1]) != 1) ++h;
    }
    if (tot + h > deep) return;  // IDA* 剪枝（必须先剪，保证不超过当前深度上限）

    bool sorted = true;
    for (int i = 1; i <= n; ++i) {
        if (a[i] != i) { sorted = false; break; }
    }
    if (sorted) {            // 升序达成
        found = true;
        return;
    }

    // 翻转前 i 个元素（i>=2，跳过与上一步相同长度的翻转，避免纯撤销）。
    for (int i = 2; i <= n; ++i) {
        if (i == p) continue;
        reverse(a + 1, a + 1 + i);
        dfs(tot + 1, i);
        reverse(a + 1, a + 1 + i);
        if (found) return;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    if (!(cin >> t)) return 0;
    while (t--) {
        cin >> n;
        for (int i = 1; i <= n; ++i) cin >> a[i];
        found = false;
        int ans = 0;
        for (deep = 0; deep <= 50; ++deep) {
            dfs(0, 0);
            if (found) { ans = deep; break; }
        }
        cout << ans << '\n';
    }
    return 0;
}
