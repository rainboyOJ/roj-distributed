// 一本通 1701《最大值》标程
//
// 解法来源：无公开解法来源（检索 CSDN 站内 / Bing / DuckDuckGo / 百度 /
// 搜狗 均未返回可用 AC 代码，本实现为依据题面自研，经对拍验证）。
// 同型题参考（仅用于交叉确认思路）：Codeforces Gym 101317F "Maximization"
// https://codeforces.com/gym/101317 （本题疑似其汉化版）。
//
// 题意：选 x ∈ [0,2^n)，依次异或 a_1..a_m；对手在恰一个时刻（含刚选完数
// 时与最后）把当前值 v 变为 f(v) = (floor(2v/2^n)+2v) mod 2^n。
// 对 b∈{0,1} 有 (b+2v) mod 2^n = (2v mod 2^n) + b，故 f 恰为 n 位循环左
// 移 1 位 rol。最大化最坏终值，并统计取得最大值的初值数量。
//
// 推导：设对手在第 i 步（已异或 a_1..a_i，i=0..m）施加 rol，记
//   p_i = a_1^..^a_i（p_0=0），suf_i = a_{i+1}^..^a_m（suf_m=0）。
// 由于 rol 只是位重排，与异或可交换：rol(u^v) = rol(u)^rol(v)，故
//   T_i(x) = rol(x ^ p_i) ^ suf_i = rol(x) ^ (rol(p_i) ^ suf_i) ≜ y ^ C_i
// 其中 y = rol(x)。rol 是双射，x 与 y 一一对应。问题化为经典模型：
//   给定 m+1 个数 C_0..C_m，求 y 使 min_i (y^C_i) 最大，并统计 y 个数。
//
// 算法：把 C_i 建成深度 n 的二进制字典树（高位到低位）。y^C 的第 k 位为 1
// ⟺ y 在该位与 C 同向。递归（迭代实现）：
//   - 单子树非空：该位 min 值 = 1，y 被迫走异侧，贡献 2^k，低位递归同侧；
//   - 双子树非空：该位 min 值 = 0（对手选异侧），y 选侧 w 时低位由异侧
//     子树继续决定，两制取 max；相等时两侧 y 第 k 位相反、不相交，计数相加。
// 复杂度 O(m·n)，结点数 ≤ (m+1)·n ≈ 3e6。
#include <cstdio>
#include <vector>
#include <array>
#include <algorithm>
using namespace std;

typedef long long ll;

int n, m;
vector<array<int,2> > ch;

void insertC(int c) {
    int u = 0;
    for (int k = n - 1; k >= 0; --k) {
        int b = (c >> k) & 1;
        if (!ch[u][b]) {
            ch[u][b] = (int)ch.size();
            ch.push_back({0, 0});
        }
        u = ch[u][b];
    }
}

int main() {
    scanf("%d %d", &n, &m);
    vector<int> a(m);
    for (int i = 0; i < m; ++i) scanf("%d", &a[i]);
    ch.reserve((size_t)(m + 1) * n + 2);
    ch.push_back({0, 0});

    vector<int> pre(m + 1, 0), suf(m + 1, 0);
    for (int i = 1; i <= m; ++i) pre[i] = pre[i - 1] ^ a[i - 1];
    for (int j = m - 1; j >= 0; --j) suf[j] = suf[j + 1] ^ a[j];

    int fullMask = (1 << n) - 1;
    for (int i = 0; i <= m; ++i) {
        int p = pre[i];
        int rp = ((p << 1) & fullMask) | (p >> (n - 1));   // rol(p_i)
        insertC(rp ^ suf[i]);
    }
    int tot = (int)ch.size();

    // 结点按层分组（迭代 DFS）
    vector<int> dep(tot, -1);
    dep[0] = 0;
    vector<vector<int> > levels(n + 1);
    {
        vector<int> st = {0};
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            levels[dep[u]].push_back(u);
            for (int w = 0; w < 2; ++w)
                if (ch[u][w]) { dep[ch[u][w]] = dep[u] + 1; st.push_back(ch[u][w]); }
        }
    }

    // 自底向上：fVal[u] / fCnt[u] = 子树 u（剩 r 位）的 max_y min 值与计数
    vector<ll> fVal(tot, 0), fCnt(tot, 0);
    for (int d = n; d >= 0; --d) {
        int r = n - d;
        ll bit = (r >= 1) ? (1LL << (r - 1)) : 0;
        for (int u : levels[d]) {
            if (d == n) { fVal[u] = 0; fCnt[u] = 1; continue; }
            int c0 = ch[u][0], c1 = ch[u][1];
            if (!c0 || !c1) {
                int c = c0 ? c0 : c1;
                fVal[u] = bit + fVal[c];   // 该位 min = 1，y 走异侧（唯一）
                fCnt[u] = fCnt[c];
            } else {
                // 该位 min = 0；y 选侧 w 时低位由异侧决定
                if (fVal[c0] > fVal[c1]) {
                    fVal[u] = fVal[c0]; fCnt[u] = fCnt[c0];
                } else if (fVal[c1] > fVal[c0]) {
                    fVal[u] = fVal[c1]; fCnt[u] = fCnt[c1];
                } else {
                    fVal[u] = fVal[c0];
                    fCnt[u] = fCnt[c0] + fCnt[c1];
                }
            }
        }
    }

    printf("%lld\n%lld\n", fVal[0], fCnt[0]);
    return 0;
}
