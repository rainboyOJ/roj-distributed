// 一本通 2141《公司下属》 标程（C++17, stdin -> stdout）
//
// 题意：公司有 n 名员工，编号 1..n，员工 1 是总经理。输入给出 n-1 个整数，
//       依次表示员工 2、3、…、n 的直接上司编号。输出每位员工的下属总人数
//       （含间接下属，不含本人），即「以该员工为根的子树的节点数 - 1」。
// 限制：1 <= n <= 2*10^5。
//
// 参考来源（网络题解，已改写，均与题面样例一致，无冲突）：
//   [1] https://blog.csdn.net/sinat_39159613/article/details/158702678
//       《公司下属（信息学奥赛一本通- P2141）》：
//       链式前向星建「上司 -> 下属」单向边，从根 1 递归后序遍历，
//       sz[x] = 1 + Σ sz[child]，答案即 sz[x]-1，时间 O(n)。
//   [2] https://blog.csdn.net/weixin_33178839/article/details/167060734
//       《信息学奥赛一本通P2141公司下属：递归后序遍历统计子树》：
//       同一公式 f[u] = Σ (f[v] + 1)，并指出链状数据递归会爆栈。
//   [3] https://blog.csdn.net/weixin_45674669/article/details/163312531
//       《【题解-信息学奥赛一本通】2141：公司下属》：同上的 dfs 写法。
//
// 本标程的改写：思路与参考题解一致（子树大小 - 1），但实现上不递归，
//   1) 用孩子链表建树；2) 从根 1 做 BFS 得到「父亲一定排在孩子之前」的访问序；
//   3) 逆序把每个节点的子树大小累加给它的父亲。
// 复杂度同为 O(n)，且在 n=2*10^5 的链状（深度最大）数据上不使用系统栈，
// 不受递归深度限制影响。

#include <cstdio>
#include <vector>

using namespace std;

namespace {

const int BUF_SIZE = 1 << 16;
char inBuf[BUF_SIZE];
int inPos = 0, inLen = 0;

inline int readChar() {
    if (inPos == inLen) {
        inLen = (int)fread(inBuf, 1, BUF_SIZE, stdin);
        inPos = 0;
        if (inLen <= 0) return -1;
    }
    return inBuf[inPos++];
}

// 读入一个非负整数（本题输入均为正整数，函数兼容末尾无空白的情况）
inline int readInt() {
    int c = readChar();
    while (c != -1 && (c < '0' || c > '9')) c = readChar();
    if (c == -1) return -1;
    int x = 0;
    while (c >= '0' && c <= '9') {
        x = x * 10 + (c - '0');
        c = readChar();
    }
    return x;
}

char outBuf[BUF_SIZE];
int outPos = 0;

inline void flushOut() {
    if (outPos > 0) {
        fwrite(outBuf, 1, outPos, stdout);
        outPos = 0;
    }
}

inline void writeChar(char c) {
    if (outPos == BUF_SIZE) flushOut();
    outBuf[outPos++] = c;
}

inline void writeInt(int x) {
    char tmp[12];
    int len = 0;
    if (x == 0) {
        writeChar('0');
        return;
    }
    while (x > 0) {
        tmp[len++] = char('0' + x % 10);
        x /= 10;
    }
    while (len > 0) writeChar(tmp[--len]);
}

}  // namespace

int main() {
    int n = readInt();
    if (n <= 0) return 0;  // 空输入保护

    vector<int> boss(n + 1, 0);      // boss[i]：员工 i 的直接上司（根为 0）
    vector<int> head(n + 1, 0);      // 孩子链表头
    vector<int> nxt(1, 0);           // 链表后继（下标从 1 开始）
    vector<int> child(1, 0);         // 边的终点（孩子编号）

    int edgeCnt = 0;
    for (int i = 2; i <= n; ++i) {
        int p = readInt();           // 员工 i 的直接上司
        boss[i] = p;
        child.push_back(i);
        nxt.push_back(head[p]);
        head[p] = ++edgeCnt;
    }

    // 从根 1 做 BFS：得到父先于子的访问序（合法输入下恰好访问全部 n 个点）
    vector<int> order;
    order.reserve(n);
    order.push_back(1);
    for (size_t qh = 0; qh < order.size(); ++qh) {
        int u = order[qh];
        for (int e = head[u]; e != 0; e = nxt[e]) order.push_back(child[e]);
    }

    // 逆序累加子树大小：孩子先算完，再把自己的整棵子树报给父亲
    vector<int> sz(n + 1, 1);
    for (size_t i = order.size(); i-- > 0;) {
        int u = order[i];
        if (u != 1) sz[boss[u]] += sz[u];
    }

    // 输出每位员工的下属人数 = 子树大小 - 1（顺序 1..n，空格分隔）
    for (int i = 1; i <= n; ++i) {
        if (i > 1) writeChar(' ');
        writeInt(sz[i] - 1);
    }
    writeChar('\n');
    flushOut();
    return 0;
}
