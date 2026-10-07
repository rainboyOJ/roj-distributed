// 一本通 1992《书架book》标程
//
// 本题即 [ZJOI2006]Book 书架（BZOJ1861 / 洛谷 P2596）：维护一个从上到下的书的序列，
// 支持 Top / Bottom / Insert / Ask / Query 五种操作。
//
// 参考来源（网络题解，思路改写、代码重新实现并经样例/对拍验证，非盲抄）：
//   1. https://blog.csdn.net/rose_max/article/details/80095224
//      《[bzoj1861][Splay]Book 书架》—— Splay 按下标（序列位置）建树，记 pos[] 映射
//      书编号 -> 树节点；Top/Bottom/Insert 用“删点后插入到指定位置”实现；Ask 为 splay
//      到根后取左子树 size；Query 为查中序第 k 个。
//   2. https://www.cnblogs.com/luyouqi233/p/8137278.html
//      《BZOJ1861:[ZJOI2006]书架——题解》—— 同思路 Splay 序列维护（含完整题面与
//      数据范围 n,m<=80000，用于交叉核对题面）。
//   3. https://blog.csdn.net/patrickpwq/article/details/86775124
//      《【ZJOI2006】书架（Splay/树状数组+二分）》—— Insert 用“splay 到根后与
//      前驱/后继交换键值与 pos”的简洁写法（本 std 采用），并给出树状数组+二分的
//      独立做法用于交叉验证。
//
// 算法：数组版 Splay 维护序列（节点键 = 书编号，中序遍历 = 书架从上到下）。
//   - pos[v]：书 v 当前所在树节点编号；key[x]：节点 x 存的书编号（与 pos 互为逆映射）。
//   - 建树：按初始书架顺序沿右链插入，天然有序，无需 splay。
//   - Top s：把 pos[s] splay 到根；若有左子树（上面的书），则找到其“后继”
//     （右子树最左节点）并把左子树整体挂到后继左儿子处 —— 等价于把书 s 移到最前。
//   - Bottom s：对称，把右子树挂到“前驱”（左子树最右节点）的右儿子处。
//   - Insert s t（t∈{-1,0,1}）：splay 到根后与其后继/前驱节点交换 key 与 pos
//     （结构不动，最稳）；t=0 无操作。
//   - Ask s：splay 到根，输出左子树 size。
//   - Query s：中序第 s 个节点，输出其 key。
// 复杂度 O((n+m) log n)；n,m <= 8e4，实测最大点 < 0.05 s。
#include <cstdio>
#include <utility>
using std::swap;

const int N = 80005;

int n, m, root, cnt;
int ch[N][2], fa[N], sz[N], key[N], pos[N];

inline bool which(int x) { return ch[fa[x]][1] == x; }
inline void pushup(int x) { sz[x] = sz[ch[x][0]] + sz[ch[x][1]] + 1; }

inline void rotate(int x) {
    int y = fa[x], z = fa[y], k = which(x), w = ch[x][k ^ 1];
    ch[y][k] = w; if (w) fa[w] = y;
    if (z) ch[z][which(y)] = x;
    fa[x] = z;
    ch[x][k ^ 1] = y; fa[y] = x;
    pushup(y); pushup(x);
}

inline void splay(int x, int goal) { // 旋到 goal 的儿子处（goal==0 即根）
    while (fa[x] != goal) {
        int y = fa[x], z = fa[y];
        if (z != goal) rotate(which(x) == which(y) ? y : x);
        rotate(x);
    }
    if (!goal) root = x;
}

inline int kth(int k) { // 中序第 k 个节点（1-based）
    int x = root;
    while (true) {
        if (k <= sz[ch[x][0]]) { x = ch[x][0]; continue; }
        if (k == sz[ch[x][0]] + 1) return x;
        k -= sz[ch[x][0]] + 1;
        x = ch[x][1];
    }
}

inline int newNode(int f, int v) { // 键为 v 的节点，父亲 f
    int x = ++cnt;
    fa[x] = f; ch[x][0] = ch[x][1] = 0; sz[x] = 1;
    key[x] = v; pos[v] = x;
    return x;
}

int main() {
    scanf("%d %d", &n, &m);

    // 建树：沿右链按初始顺序插入（右链天然中序有序），最后自底向上补齐 size
    {
        int v; scanf("%d", &v);
        root = newNode(0, v);
        int r = root;
        for (int i = 2; i <= n; i++) {
            scanf("%d", &v);
            int x = newNode(r, v);
            ch[r][1] = x;
            r = x;
        }
        while (r) { pushup(r); r = fa[r]; } // 右链祖先的 size 自底向上修复
    }

    char op[16];
    for (int i = 0, s, t; i < m; i++) {
        scanf("%s %d", op, &s);
        if (op[0] == 'T') {            // Top S
            int x = pos[s];
            splay(x, 0);
            if (!ch[x][0]) continue;   // 已在最上
            if (!ch[x][1]) {           // 无右子树：左子树整体变右子树
                ch[x][1] = ch[x][0];
                ch[x][0] = 0;
                pushup(x);
            } else {
                int y = ch[x][1];
                while (ch[y][0]) y = ch[y][0];   // 后继
                fa[ch[x][0]] = y;
                ch[y][0] = ch[x][0];
                ch[x][0] = 0;
                splay(y, 0);                    // 维护沿途 size
                splay(x, 0);
                pushup(x);
                splay(x, 0);
            }
        } else if (op[0] == 'B') {     // Bottom S
            int x = pos[s];
            splay(x, 0);
            if (!ch[x][1]) continue;   // 已在最下
            if (!ch[x][0]) {           // 无左子树：右子树整体变左子树
                ch[x][0] = ch[x][1];
                ch[x][1] = 0;
                pushup(x);
            } else {
                int y = ch[x][0];
                while (ch[y][1]) y = ch[y][1];   // 前驱
                fa[ch[x][1]] = y;
                ch[y][1] = ch[x][1];
                ch[x][1] = 0;
                splay(y, 0);
                splay(x, 0);
                pushup(x);
                splay(x, 0);
            }
        } else if (op[0] == 'I') {     // Insert S T
            scanf("%d", &t);
            if (t == 0) continue;
            int x = pos[s];
            splay(x, 0);
            int y;
            if (t == 1) {              // 与后继（紧邻其下的书）交换
                y = ch[x][1];
                while (ch[y][0]) y = ch[y][0];
            } else {                    // t == -1：与前驱（紧邻其上的书）交换
                y = ch[x][0];
                while (ch[y][1]) y = ch[y][1];
            }
            swap(key[x], key[y]);
            pos[key[x]] = x;
            pos[key[y]] = y;
            splay(y, 0);                // 让路径上的 size 保持正确
        } else if (op[0] == 'A') {     // Ask S
            int x = pos[s];
            splay(x, 0);
            printf("%d\n", sz[ch[x][0]]);
        } else {                       // Query S
            printf("%d\n", key[kth(s)]);
        }
    }
    return 0;
}
