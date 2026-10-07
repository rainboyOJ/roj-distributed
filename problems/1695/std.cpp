// 1695《独特的树叶》（原型：[JSOI2016] 独特的树叶 / BZOJ4754 / 洛谷P4323 / LOJ2072）
// 做法：树哈希 + 换根（reroot）DP，O(n)。
//
//   哈希定义（u 的子树，以 u 为根，mix = splitmix64 强混淆双射）：
//       f(u) = mix(siz(u)) + Σ_{v 是 u 的孩子} mix(f(v))
//   聚合用“求和”（可撤销：减去 mix(f(v)) 即可），孩子贡献过 mix 后是
//   雪崩良好的 64 位随机值，不存在 XOR 聚合“相等孩子互相抵消”的结构性退化。
//
//   1. 树 A（n 个点）：一次 DFS 求 f；再自顶向下换根得到以每个点为根的整树哈希
//      fullA[r]，全部插入哈希表 S。
//      换根（u 的原父为 p，v 是 u 原根意义下的孩子，N 为整树大小）：
//        cut(p,u) 后 p 所在分量（以 p 为根）：F = mix(N - siz(u)) + full(p) - mix(N) - mix(f(u))
//        full(u) = mix(N) + f(u) - mix(siz(u)) + mix(F)
//   2. 树 B（n+1 个点）：取一个度 > 1 的点为根同样处理；对 B 的每个叶子 x（父 u），
//      删掉 x 后以 u 为根的 n 个点的树哈希：
//        H = full(u) - mix(n+1) + mix(n) - mix(f(x))
//      （叶子 x 的子树哈希 f(x) = mix(1) 与割边后分量哈希一致）
//      H ∈ S 则 x 是候选答案，取最小编号。
//
//   正确性：两棵有根树同构 ⇒ 哈希相等（必要条件逐层成立）；非同构树哈希相等仅为
//   splitmix64 求和的随机碰撞，单次比较概率 ~2^-64，n=1e5 时总碰撞期望 < 1e-9。
//
// 参考来源（思路参考；网络流传的 XOR 版哈希在“相同孩子抵消”结构上会假阳性，
// 本文件为自行推导的 sum+splitmix 正确实现，见 gen-report.md 对拍记录）：
//   https://blog.csdn.net/element_hero/article/details/80616126 （树哈希+换根，P4323 题解）
//   https://blog.csdn.net/aijiu8213/article/details/102209754 （转载自 https://www.cnblogs.com/akoasm/p/10140479.html ）
//   题目原型：洛谷 P4323 / BZOJ4754 / LOJ2072
// 注意：n=1 时 A 为空树、B 为单边，删掉任一点均得单点树，答案输出 1。

#include <cstdio>
#include <cstring>

typedef unsigned long long ull;

const int MAXN = 100005;

int n;
int headA[MAXN], nxtA[MAXN << 1], toA[MAXN << 1], cntA;
int headB[MAXN], nxtB[MAXN << 1], toB[MAXN << 1], cntB;
int szA[MAXN], szB[MAXN];
ull fA[MAXN], fB[MAXN];   /* 原根意义下的子树哈希 */
ull fullA[MAXN], fullB[MAXN]; /* 以每个点为根的整树哈希 */
int degB[MAXN];
int parA[MAXN], ordA[MAXN], cntOrdA;
int parB[MAXN], ordB[MAXN], cntOrdB;

inline ull mix(ull x) { /* splitmix64 finalizer */
    x += 0x9e3779b97f4a7c15ULL;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}

/* 开放寻址哈希表（比 unordered_set 更快更稳） */
const int HBITS = 21; /* 2^21 = 2097152 > 2*MAXN */
const int HSIZE = 1 << HBITS;
ull hkey[HSIZE];
char hused[HSIZE];

inline void hinsert(ull x) {
    int h = (int)((x ^ (x >> 32)) & (HSIZE - 1));
    while (hused[h]) {
        if (hkey[h] == x) return;
        h = (h + 1) & (HSIZE - 1);
    }
    hused[h] = 1;
    hkey[h] = x;
}
inline bool hfind(ull x) {
    int h = (int)((x ^ (x >> 32)) & (HSIZE - 1));
    while (hused[h]) {
        if (hkey[h] == x) return true;
        h = (h + 1) & (HSIZE - 1);
    }
    return false;
}

/* 通用：非递归求 parent / DFS 序（父先于子），防 1e5 链上爆栈 */
void dfsOrder(const int *head, const int *nxt, const int *to, int root, int *par, int *order, int &cnt) {
    int top = 0;
    static int stk[MAXN];
    cnt = 0;
    stk[top++] = root;
    par[root] = 0;
    while (top) {
        int u = stk[--top];
        order[cnt++] = u;
        for (int e = head[u]; e; e = nxt[e]) {
            int v = to[e];
            if (v == par[u]) continue;
            par[v] = u;
            stk[top++] = v;
        }
    }
}

void buildA() {
    dfsOrder(headA, nxtA, toA, 1, parA, ordA, cntOrdA);
    for (int i = cntOrdA - 1; i >= 0; --i) {
        int u = ordA[i];
        int s = 1;
        ull h = 0;
        for (int e = headA[u]; e; e = nxtA[e]) {
            int v = toA[e];
            if (v == parA[u]) continue;
            s += szA[v];
            h += mix(fA[v]);
        }
        szA[u] = s;
        fA[u] = mix((ull)s) + h;
    }
}

void collectA() {
    /* ordA 自顶向下换根：fullA[u] = 以 u 为根的整树（n 个点）哈希 */
    fullA[1] = fA[1];
    for (int i = 0; i < cntOrdA; ++i) {
        int u = ordA[i];
        hinsert(fullA[u]);
        for (int e = headA[u]; e; e = nxtA[e]) {
            int v = toA[e];
            if (v == parA[u]) continue;
            /* cut(u,v) 后 u 所在分量（以 u 为根，n - siz(v) 个点）：
               = fullA[u] 去掉 v 的孩子贡献、大小项改为 n - siz(v) */
            ull F = fullA[u] - mix((ull)n) - mix(fA[v]) + mix((ull)(n - szA[v]));
            fullA[v] = mix((ull)n) + (fA[v] - mix((ull)szA[v])) + mix(F);
        }
    }
}

int rootB;
void buildB() {
    dfsOrder(headB, nxtB, toB, rootB, parB, ordB, cntOrdB);
    for (int i = cntOrdB - 1; i >= 0; --i) {
        int u = ordB[i];
        int s = 1;
        ull h = 0;
        for (int e = headB[u]; e; e = nxtB[e]) {
            int v = toB[e];
            if (v == parB[u]) continue;
            s += szB[v];
            h += mix(fB[v]);
        }
        szB[u] = s;
        fB[u] = mix((ull)s) + h;
    }
}

int ans;
void solveB() {
    /* ordB 自顶向下换根：fullB[u] = 以 u 为根的整树（n+1 个点）哈希 */
    fullB[rootB] = fB[rootB];
    for (int i = 0; i < cntOrdB; ++i) {
        int u = ordB[i];
        for (int e = headB[u]; e; e = nxtB[e]) {
            int v = toB[e];
            if (v == parB[u]) continue;
            if (degB[v] == 1) {
                /* 删掉叶子 v 后以 u 为根的整树（n 个点）哈希 */
                ull H = fullB[u] - mix((ull)(n + 1)) - mix(fB[v]) + mix((ull)n);
                if (hfind(H) && v < ans) ans = v;
            } else {
                ull F = fullB[u] - mix((ull)(n + 1)) - mix(fB[v]) + mix((ull)(n + 1 - szB[v]));
                fullB[v] = mix((ull)(n + 1)) + (fB[v] - mix((ull)szB[v])) + mix(F);
            }
        }
    }
}

int main() {
    scanf("%d", &n);
    cntA = 0;
    for (int i = 0; i < n - 1; ++i) {
        int x, y;
        scanf("%d %d", &x, &y);
        ++cntA; toA[cntA] = y; nxtA[cntA] = headA[x]; headA[x] = cntA;
        ++cntA; toA[cntA] = x; nxtA[cntA] = headA[y]; headA[y] = cntA;
    }
    cntB = 0;
    for (int i = 0; i < n; ++i) {
        int x, y;
        scanf("%d %d", &x, &y);
        ++cntB; toB[cntB] = y; nxtB[cntB] = headB[x]; headB[x] = cntB;
        ++cntB; toB[cntB] = x; nxtB[cntB] = headB[y]; headB[y] = cntB;
        ++degB[x];
        ++degB[y];
    }

    if (n == 1) {
        /* A 为空树，B 只有两个点一条边，删掉任意一点都得到单点树 */
        printf("1\n");
        return 0;
    }

    buildA();
    collectA();

    /* B 的根取一个度 > 1 的点（n>=2 时 B 有 n+1>=3 个点，必存在度 >= 2 的点） */
    rootB = 1;
    for (int v = 1; v <= n + 1; ++v)
        if (degB[v] > 1) { rootB = v; break; }

    ans = n + 2; /* 题面保证有解，此为保险初值 */
    buildB();
    solveB();

    printf("%d\n", ans);
    return 0;
}
