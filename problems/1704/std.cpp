// 一本通 1704《奇特的猫》标程
//
// 参考来源（思路为本文件作者自研，未找到现成 AC 代码）：
//   题意与编辑距离性质参考：信息学奥赛一本通题面（见 content.md）
//   无公开解法来源；算法正确性由 work/brute.cpp 对拍验证。
//
// 题意要点：
//   每天给出一串按键（ASCII 值，退格为 8）。光标永远在串尾，
//   退格删除末尾字符。集合 S 为该天所有出现过的串（含空串）。
//   串之间编辑距离 d(P,Q)=|P|+|Q|-2*LCP(P,Q)。
//   把 S 建成一棵 Trie（S 天然前缀封闭），于是 d 就是树上距离。
//   |S| 即 Trie 结点数 n。
//
//   第 1 天：答案 = 集合内两两距离之和 W。
//   第 2 天：min/max 由选取 A0、B0 决定。
//   第 3 天：min/max 由选取 A0、B0、B1、C0 决定。
//
//   记 D[v] = v 到 S 中所有点的距离和。树形 DP（换根）可在 O(n) 内
//   算出 W、Dmin、Dmax；第 3 天的最大值中的 max(d(b0,b1)) 项用
//   一次自底向上 DP 在 O(n) 内解决。整体 O(|S|) 时间、O(|S|) 空间。
#include <iostream>
#include <vector>
#include <string>
#include <climits>
#include <algorithm>
#include <unordered_map>
#include <cstdio>
#include <cstdlib>
using namespace std;

// 快速读入：一次性把 stdin 读进内存后手工解析。
// 三天的按键数总和可达到 6e6 量级，iostream 逐字读入在 1s 限制下不稳。
static void readAllKeys(vector<vector<int>>& keys) {
    vector<char> data;
    data.reserve(1 << 24);
    char tmp[1 << 20];
    size_t r;
    while ((r = fread(tmp, 1, sizeof(tmp), stdin)) > 0)
        data.insert(data.end(), tmp, tmp + r);
    keys.assign(3, vector<int>());
    size_t i = 0, sz = data.size();
    int day = 0;
    while (day < 3 && i < sz) {
        while (i < sz && data[i] != '\n') {
            while (i < sz && (data[i] == ' ' || data[i] == '\r' || data[i] == '\t')) ++i;
            if (i < sz && data[i] != '\n') {
                int x = 0;
                while (i < sz && data[i] >= '0' && data[i] <= '9') {
                    x = x * 10 + (data[i] - '0');
                    ++i;
                }
                keys[day].push_back(x);
            }
        }
        if (i < sz && data[i] == '\n') ++i;
        ++day;
    }
}

struct Node {
    int parent;
    int depth;
    int firstChild;
    int nextSibling;
    unsigned char ch;
    int sz;
    long long D;
    Node() : parent(-1), depth(0), firstChild(-1), nextSibling(-1), ch(0), sz(0), D(0) {}
};

struct Tree {
    vector<Node> t;
    int n;
    long long W;     // 集合内两两距离之和
    long long Dmin;  // min D[v]
    long long Dmax;  // max D[v]

    void build(const vector<int>& keys) {
        t.clear();
        t.reserve(keys.size() + 1);
        t.push_back(Node());  // 根 = 空串
        // (父结点, 字符) -> 孩子结点，保证 O(1) 查找，避免菊花树退化
        unordered_map<long long, int> childId;
        childId.reserve(keys.size() * 2 + 1);
        int cur = 0;
        for (int k : keys) {
            if (k == 8) {  // 退格：回父结点
                if (cur != 0) cur = t[cur].parent;
            } else {
                unsigned char c = (unsigned char)k;
                long long key = (long long)cur * 256 + c;
                auto it = childId.find(key);
                int child;
                if (it == childId.end()) {
                    int id = (int)t.size();
                    t.push_back(Node());
                    t[id].parent = cur;
                    t[id].depth = t[cur].depth + 1;
                    t[id].ch = c;
                    // 头插到孩子链表
                    t[id].nextSibling = t[cur].firstChild;
                    t[cur].firstChild = id;
                    childId.emplace(key, id);
                    child = id;
                } else {
                    child = it->second;
                }
                cur = child;
            }
        }
        n = (int)t.size();

        // 先序遍历（父结点一定先于子孙）
        vector<int> order;
        order.reserve(n);
        vector<int> st;
        st.reserve(n);
        st.push_back(0);
        while (!st.empty()) {
            int v = st.back();
            st.pop_back();
            order.push_back(v);
            for (int c = t[v].firstChild; c != -1; c = t[c].nextSibling) st.push_back(c);
        }

        // 子树大小（逆序：孩子先于父）
        for (int i = n - 1; i >= 0; --i) {
            int v = order[i];
            int s = 1;
            for (int c = t[v].firstChild; c != -1; c = t[c].nextSibling) s += t[c].sz;
            t[v].sz = s;
        }

        // W = 每条边两端的结点数之积之和
        W = 0;
        long long tot = n;
        for (int v = 1; v < n; ++v) {
            W += (long long)t[v].sz * (tot - t[v].sz);
        }

        // D[根] = 所有结点深度之和；换根求全部 D
        long long d0 = 0;
        for (int v = 0; v < n; ++v) d0 += t[v].depth;
        t[0].D = d0;
        for (int v : order) {
            for (int c = t[v].firstChild; c != -1; c = t[c].nextSibling) {
                t[c].D = t[v].D + tot - 2LL * t[c].sz;
            }
        }

        Dmin = LLONG_MAX;
        Dmax = LLONG_MIN;
        for (int v = 0; v < n; ++v) {
            Dmin = min(Dmin, t[v].D);
            Dmax = max(Dmax, t[v].D);
        }
    }
};

int main() {
    vector<vector<int>> keys;
    readAllKeys(keys);
    Tree A;
    A.build(keys[0]);
    long long WA = A.W;
    int nA = A.n;
    long long DAmin = A.Dmin, DAmax = A.Dmax;

    long long day1 = WA;
    A.t.clear();
    A.t.shrink_to_fit();

    Tree B;
    B.build(keys[1]);
    long long WB = B.W;
    int nB = B.n;
    long long DBmin = B.Dmin, DBmax = B.Dmax;

    long long day2min = WA + WB + 1LL * nA * nB + 1LL * nB * DAmin + 1LL * nA * DBmin;
    long long day2max = WA + WB + 1LL * nA * nB + 1LL * nB * DAmax + 1LL * nA * DBmax;

    Tree C;
    C.build(keys[2]);
    long long WC = C.W;
    int nC = C.n;
    long long DCmin = C.Dmin, DCmax = C.Dmax;
    C.t.clear();
    C.t.shrink_to_fit();

    long long base = WA + WB + WC + 1LL * nA * nB + 1LL * nB * nC + 2LL * nA * nC;
    long long day3min = base + 1LL * (nB + nC) * DAmin + 1LL * (nA + nB) * DCmin +
                        1LL * (nA + nC) * DBmin;

    // 第 3 天最大值中的 max_{b0,b1} [nA*D_B[b0] + nC*D_B[b1] + nA*nC*d(b0,b1)]
    // = max_{x,y in B} [f[x] + g[y] - 2*L*depth(lca(x,y))]
    //   其中 f[x]=nA*D_B[x]+L*depth[x], g[x]=nC*D_B[x]+L*depth[x], L=nA*nC。
    long long L = 1LL * nA * nC;
    int nb = B.n;
    vector<long long> best0(nb), best1(nb);
    long long maxpair = LLONG_MIN;

    vector<int> order;
    order.reserve(nb);
    {
        vector<int> st;
        st.reserve(nb);
        st.push_back(0);
        while (!st.empty()) {
            int v = st.back();
            st.pop_back();
            order.push_back(v);
            for (int c = B.t[v].firstChild; c != -1; c = B.t[c].nextSibling) st.push_back(c);
        }
    }

    for (int i = nb - 1; i >= 0; --i) {
        int v = order[i];
        long long fv = 1LL * nA * B.t[v].D + L * B.t[v].depth;
        long long gv = 1LL * nC * B.t[v].D + L * B.t[v].depth;
        long long b0 = fv;
        long long b1 = gv;
        long long curbest = fv + gv;  // x = y = v
        long long max0 = LLONG_MIN, max1 = LLONG_MIN;
        for (int c = B.t[v].firstChild; c != -1; c = B.t[c].nextSibling) {
            // 一端为 v，另一端在子树 c 中
            curbest = max(curbest, fv + best1[c]);
            curbest = max(curbest, best0[c] + gv);
            // 两端分别来自两个不同孩子子树
            if (max0 != LLONG_MIN) curbest = max(curbest, max0 + best1[c]);
            if (max1 != LLONG_MIN) curbest = max(curbest, max1 + best0[c]);
            max0 = max(max0, best0[c]);
            max1 = max(max1, best1[c]);
            b0 = max(b0, best0[c]);
            b1 = max(b1, best1[c]);
        }
        best0[v] = b0;
        best1[v] = b1;
        curbest -= 2LL * L * B.t[v].depth;
        maxpair = max(maxpair, curbest);
    }

    long long day3max = base + 1LL * (nB + nC) * DAmax + 1LL * (nA + nB) * DCmax + maxpair;

    cout << day1 << " " << day1 << "\n";
    cout << day2min << " " << day2max << "\n";
    cout << day3min << " " << day3max << "\n";
    return 0;
}
