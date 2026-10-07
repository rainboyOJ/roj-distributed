// 一本通 1819《字符串游戏》标程（C++17）
//
// 来源依据：
//   题面（k 轮、输者先手下一轮、最后一轮胜者赢、S 中串的前缀为合法串）与三组样例
//   （输出依次 HY wins! / HY wins! / Teacher wins!）与 Codeforces 455B "A Lot of Games"
//   完全一致（同题面、同样例），判定为同源经典题，按该题公认解法自研实现。
//   检索记录：Bing / DuckDuckGo / CSDN 站内搜 / grep.app / GitHub code API 均被反爬
//   或无相关结果，未取到现成 AC 代码（详见 gen-report.md）。
//
// 算法（trie 上的公平组合游戏）：
//   建 trie。对结点 u（轮到 u 的行动者视角）：
//     win[u]  = 该行动者能否强行赢下本轮
//     lose[u] = 该行动者能否强行输掉本轮（对手也全力想输 = 最坏情况下的「求败」能力）
//   叶子（无路可走）时：win = false，lose = true（本轮直接输）。
//   内部结点：win[u]  = ∃ 子 v 使 !win[v]   （走到对手必败点）
//             lose[u] = ∃ 子 v 使 !lose[v]  （走到对手「无法求败」的点，即对手被迫取胜）
//   结论（推理见 gen-report.md）：
//     !win[root]              -> 每轮先手必败，输者仍是先手，Teacher 赢满 k 轮
//     win[root] && lose[root] -> 先手每轮可自选胜负：先连输 k-1 轮再赢第 k 轮 => HY 胜（任意 k）
//     win[root] && !lose[root] -> 每轮先手必胜且无法求败，胜负交替 => HY 胜 iff k 为奇数
//
// 输入：多组数据到 EOF（第一行 n,k；随后 n 行字符串）
// 输出：每组一行 "HY wins!" 或 "Teacher wins!"
#include <array>
#include <cstdio>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n, k;
    while (cin >> n >> k) {
        // 动态 trie：结点数 <= 本组所有串长度和 + 1（上限 1e5+1，无固定数组越界风险）
        vector<array<int, 26>> ch(1);
        ch[0].fill(-1);

        string s;
        for (long long i = 0; i < n; ++i) {
            cin >> s;
            int cur = 0;
            for (char c : s) {
                int x = c - 'a';
                if (ch[cur][x] == -1) {
                    ch.push_back({});
                    ch.back().fill(-1);
                    ch[cur][x] = (int)ch.size() - 1;
                }
                cur = ch[cur][x];
            }
        }

        int m = (int)ch.size();
        vector<char> win(m, 0), lose(m, 0);

        // 迭代式先序遍历（父在子前），逆序即为「子先于父」的后序，避免深链爆栈
        vector<int> order;
        order.reserve(m);
        vector<int> stk;
        stk.reserve(m);
        stk.push_back(0);
        while (!stk.empty()) {
            int u = stk.back();
            stk.pop_back();
            order.push_back(u);
            for (int c = 0; c < 26; ++c)
                if (ch[u][c] != -1) stk.push_back(ch[u][c]);
        }
        for (int i = m - 1; i >= 0; --i) {
            int u = order[i];
            bool leaf = true;
            for (int c = 0; c < 26; ++c) {
                int v = ch[u][c];
                if (v == -1) continue;
                leaf = false;
                if (!win[v]) win[u] = 1;
                if (!lose[v]) lose[u] = 1;
            }
            if (leaf) lose[u] = 1;  // win 保持 0
        }

        if (!win[0])
            cout << "Teacher wins!\n";
        else if (lose[0])
            cout << "HY wins!\n";
        else
            cout << ((k % 2 == 1) ? "HY wins!\n" : "Teacher wins!\n");
    }
    return 0;
}
