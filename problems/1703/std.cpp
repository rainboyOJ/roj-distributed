// 一本通 1703《量子纠缠》标程（自研）
//
// 题意建模：
//   信息集 S 是数字串（0~9）的集合。操作：
//     1 s    : 把串 s 加入 S（对应 trie 上节点标记 final）
//     2 s    : 询问 s 是否属于 S
//     3 a b  : 令 a、b 互相纠缠
//   纠缠 a b 的定义是：对任意后缀 X，a+X 属于 S 当且仅当 b+X 属于 S。
//   这正是 Myhill-Nerode 意义下的“右语言等价”。因此可以把每个串看成
//   trie 中的一个状态，纠缠操作 = 把两个状态合并（union-find），并且
//   合并后的状态对每个字符 c 的出边也必须合并（右同余闭包）。
//
// 算法：并查集 + trie 合并。
//   每个节点存 ch[10] 与 fin 标记；find 做路径压缩。
//   merge(p,q)：递归合并 p、q 的 10 条出边，再合并 fin 标记，最后 union。
//   trie 深度受 L<=50 限制，递归深度安全。
//
// 参考来源：无公开 AC 题解（网络检索未找到本题现成解法），
//           依据题面自研（DFA 等价状态合并 / 并查集 + trie）。
//
#include <iostream>
#include <string>
#include <vector>
#include <utility>
#include <cstring>
using namespace std;

struct Node {
    int ch[10];
    bool fin;
    Node() {
        memset(ch, 0, sizeof(ch));
        fin = false;
    }
};

static vector<Node> nd;
static vector<int> fa;

static int newNode() {
    nd.emplace_back();
    fa.push_back((int)fa.size()); // fa[new] = its own index
    return (int)fa.size() - 1;
}

// 迭代 + 路径压缩，避免深链递归爆栈
static int findRoot(int x) {
    int r = x;
    while (fa[r] != r) r = fa[r];
    while (fa[x] != x) {
        int p = fa[x];
        fa[x] = r;
        x = p;
    }
    return r;
}

static void mergeNode(int x, int y) {
    vector<pair<int,int>> stk;
    stk.push_back({x, y});
    while (!stk.empty()) {
        auto pr = stk.back();
        stk.pop_back();
        int a = findRoot(pr.first);
        int b = findRoot(pr.second);
        if (a == b) continue;
        // 先合并等价类，再用 find 打破前缀纠缠形成的环
        fa[b] = a;
        nd[a].fin = nd[a].fin || nd[b].fin;
        for (int c = 0; c < 10; ++c) {
            int da = nd[a].ch[c];
            int db = nd[b].ch[c];
            if (da && db) {
                if (findRoot(da) != findRoot(db)) {
                    stk.push_back({da, db});
                }
            } else if (!da && db) {
                nd[a].ch[c] = db;
            }
        }
    }
}

// 沿 trie 找串 s 对应节点，不存在返回 -1
static int getNode(const string& s) {
    int cur = 0;
    for (char ch : s) {
        int c = ch - '0';
        int nxt = nd[cur].ch[c];
        if (!nxt) return -1;
        cur = findRoot(nxt);
    }
    return cur;
}

// 确保串 s 的路径存在，返回末节点（原始 id）
static int ensureNode(const string& s) {
    int cur = 0;
    for (char ch : s) {
        int c = ch - '0';
        int nxt = nd[cur].ch[c];
        if (!nxt) {
            nxt = newNode();
            nd[cur].ch[c] = nxt;
            cur = nxt;
        } else {
            cur = findRoot(nxt);
        }
    }
    return cur;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    nd.emplace_back(); // root = 0
    fa.push_back(0);

    int m;
    cin >> m;

    string op, s, a, b;
    for (int i = 0; i < m; ++i) {
        cin >> op;
        if (op[0] == '1') {
            cin >> s;
            int v = ensureNode(s);
            nd[findRoot(v)].fin = true;
        } else if (op[0] == '2') {
            cin >> s;
            int v = getNode(s);
            if (v == -1) {
                cout << 0 << '\n';
            } else {
                cout << (nd[findRoot(v)].fin ? 1 : 0) << '\n';
            }
        } else { // '3'
            cin >> a >> b;
            int va = ensureNode(a);
            int vb = ensureNode(b);
            mergeNode(va, vb);
        }
    }
    return 0;
}
