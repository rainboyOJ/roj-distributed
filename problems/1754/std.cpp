// 一本通 1754《栈的维护》 标程（C++17）
// ---------------------------------------------------------------------------
// 来源（网络检索 + 改写）：
//   [1] https://www.cnblogs.com/yiqiAtiya/p/13915970.html
//       （博客园「一本通1754：栈的维护」）
//       检索依据：题面特征句「从前有个栈，一开始是空的」+ 题名「栈的维护」，
//       经搜狗命中该篇；文中给出线段树做法与合并/查询函数。
//   [2] 搜狗同页另命中「信息学奥赛题库 - 栈的维护（少儿编程）」，题面一致，
//       佐证本题为题库公开题、无 Special Judge、答案唯一。
//
// 题意：m 个操作（k=0 压入 v；k=1 从栈顶弹出 v 个，不足则清空），
//       随后 q 次单点修改某个操作的两个参数，每次修改后输出依次执行全部操作
//       后栈中剩余元素之和。m,q <= 2e5，v <= 1e4。
//
// 算法（线段树）：把“从右向左扫描、维护未匹配弹出数（缺口）”这一过程做成可合并的段。
//   对一段操作，定义其在“无外部缺口”时：
//     cnt = 最终保留的 push 个数（即该段自身的剩余栈大小）；
//     r   = 未能被本段 push 抵消、需要继续向左侧弹出的个数（缺口）；
//     sum = 最终保留的 push 之和。
//   合并左右两段（左 L 右 R）：
//     r   = rL + max(0, rR - cntL)
//     cnt = cntR + max(0, cntL - rR)
//     sum = sumR + g(L, rR)      // g(node, x) = node 在“进入缺口 x”下保留的 push 之和
//   其中 g 沿线段树单条链下推：若 x>=cnt 则 0；x<=0 则 sum；
//   否则 R 子树先吸收缺口，剩余缺口进入被 rR 截断后的 L。
//   单点修改 O(log^2 m)（每次 pushup 调用一次 O(log m) 的 g），
//   根结点的 sum 即答案。sum 与缺口 r 用 long long（上限约 2e5*1e4=2e9，逼近 int 边界）。
// ---------------------------------------------------------------------------
#include <cstdio>
#include <algorithm>
using namespace std;

typedef long long ll;

const int MAXN = 200000 + 5;
const int MAXNODE = MAXN << 2;

int m, q;
int  K[MAXN];        // 操作类型：0 压入，1 弹出
ll   V[MAXN];        // 操作参数：k=0 时为入栈值，k=1 时为弹出个数

int  cnt[MAXNODE];   // 该段无外部缺口时保留的 push 个数
ll   del[MAXNODE];   // 该段未能抵消、需向左继续弹出的个数（缺口）
ll   sum[MAXNODE];   // 该段无外部缺口时保留的 push 之和

// g(node=k, need)：结点 k 在“进入缺口 need”下最终保留的 push 之和
ll query(int k, ll need) {
    if (need <= 0)      return sum[k];          // 无缺口，全部保留
    if ((ll)cnt[k] <= need) return 0;           // 缺口吃光本段全部保留元素
    int ls = k << 1, rs = k << 1 | 1;
    if (cnt[rs] >= need)                        // 缺口在右子树内被吃光
        return (sum[k] - sum[rs]) + query(rs, need);
    // 右子树被全部吃掉，剩余缺口进入“被 del[rs] 截断后的左子树”
    return query(ls, need - cnt[rs] + del[rs]);
}

void pushup(int k) {
    int ls = k << 1, rs = k << 1 | 1;
    del[k] = del[ls] + max(0LL, del[rs] - (ll)cnt[ls]);
    cnt[k] = cnt[rs] + (int)max(0LL, (ll)cnt[ls] - del[rs]);
    sum[k] = sum[rs] + query(ls, del[rs]);
}

void build(int k, int l, int r) {
    if (l == r) {
        if (K[l] == 1) { del[k] = V[l]; cnt[k] = 0; sum[k] = 0; }
        else           { del[k] = 0;    cnt[k] = 1; sum[k] = V[l]; }
        return;
    }
    int mid = (l + r) >> 1;
    build(k << 1, l, mid);
    build(k << 1 | 1, mid + 1, r);
    pushup(k);
}

void modify(int k, int l, int r, int pos, int kk, ll vv) {
    if (l == r) {
        if (kk == 1) { del[k] = vv; cnt[k] = 0; sum[k] = 0; }
        else         { del[k] = 0;  cnt[k] = 1; sum[k] = vv; }
        return;
    }
    int mid = (l + r) >> 1;
    if (pos <= mid) modify(k << 1, l, mid, pos, kk, vv);
    else            modify(k << 1 | 1, mid + 1, r, pos, kk, vv);
    pushup(k);
}

int main() {
    if (scanf("%d %d", &m, &q) != 2) return 0;
    for (int i = 1; i <= m; ++i) {
        int kk; ll vv;
        scanf("%d %lld", &kk, &vv);
        K[i] = kk; V[i] = vv;
    }
    build(1, 1, m);
    for (int i = 0; i < q; ++i) {
        int c, kk; ll vv;
        scanf("%d %d %lld", &c, &kk, &vv);
        modify(1, 1, m, c, kk, vv);
        printf("%lld\n", sum[1]);
    }
    return 0;
}
