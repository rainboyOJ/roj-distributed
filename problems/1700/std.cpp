// 一本通 1700《PFS集合》标程
// 参考来源 URL:
//   https://blog.csdn.net/weixin_45714303/article/details/120117401
// 原思路: 把所有串插入 trie(26 叉字典树)。PFS 集合的判定与 trie 结构一一对应:
//   - 空集合法(贡献 1);
//   - 一个非空子集合法 当且仅当 不存在一个串是另一个串的前缀。
// 在 trie 上做树形 DP: 对每个节点 p, 令 f[p] = 以 p 为根的子树(即所有以
// 「根到 p 路径」为公共前缀的串)中, 可选出的合法子集个数(每个子集由若干
// 被标记为单词结尾的节点组成)。
//   - 若 p 自身是某个单词的结尾(vis[p]=1), 则选了 p 就不能再选子树中的任何
//     单词结尾(否则成前缀), 因此贡献为 1(只选 p 本身); 不选 p 时贡献为
//     子树的自由组合 ∏ f[child]。
//   - 若 p 不是结尾, 则贡献为 ∏ f[child]。
// 于是 f[p] = (∏ f[child]) + (vis[p] ? 1 : 0)。
// 由于题目要求的是「原集合的子集中是 PFS 集合的子集个数」, 空集也算一种,
// 答案恰为 f[root], 对 9191 取模。
// 复杂度 O(总字符数 * 26), 字符串总长 <= 50000*50 = 2.5e6, 在时限内。
#include <iostream>
#include <string>
#include <cstring>
using namespace std;

static const int MOD = 9191;
static const int MAXN = 50000 * 50 + 10;

struct Trie {
    int ch[MAXN][26];
    bool endp[MAXN];
    int tot;
    Trie() : tot(0) {
        memset(ch, 0, sizeof(ch));
        memset(endp, 0, sizeof(endp));
    }
    void insert(const string& s) {
        int p = 0;
        for (char c : s) {
            int x = c - 'a';
            if (!ch[p][x]) ch[p][x] = ++tot;
            p = ch[p][x];
        }
        endp[p] = true;
    }
};

static Trie trie;
static long long f[MAXN];

void dfs(int p) {
    long long prod = 1;
    for (int i = 0; i < 26; ++i) {
        int v = trie.ch[p][i];
        if (!v) continue;
        dfs(v);
        prod = prod * f[v] % MOD;
    }
    f[p] = (prod + (trie.endp[p] ? 1 : 0)) % MOD;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    string s;
    for (int i = 0; i < n; ++i) {
        cin >> s;
        trie.insert(s);
    }
    dfs(0);
    cout << f[0] << '\n';
    return 0;
}
