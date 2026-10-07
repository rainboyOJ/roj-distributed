// 一本通 1752《纪念碑》标程
//
// 题意：n×m 的方格土地（左下角格子 (1,1)，右上角格子 (n,m)），有 p 个矩形建筑物
//       （第 i 个左下角 (x1,y1)、右上角 (x2,y2)，占据格子 x∈[x1,x2], y∈[y1,y2]）。
//       求不覆盖任何建筑物的最大正方形的边长（格子数）。
//
// 算法：二分答案 L + 扫描线求矩形面积并（数据结构）
//   存在性单调：若存在 L×L 空正方形，则其子正方形给出 (L-1)×(L-1) 空正方形，
//   故可二分最大 L。
//   判定 check(L)：L×L 正方形的左上角 (lx,ly) 取值范围为
//       lx∈[1, n-L+1], ly∈[1, m-L+1]，记作「可行域」W×H（W=n-L+1,H=m-L+1）。
//   一个建筑物 (x1,y1,x2,y2) 会「禁止」所有满足
//       [lx,lx+L-1]∩[x1,x2]≠∅ 且 [ly,ly+L-1]∩[y1,y2]≠∅
//   的左上角，即 (lx,ly) ∈ [x1-L+1, x2] × [y1-L+1, y2]（再与可行域求交）。
//   于是「存在空正方形」⇔ 这 p 个「禁止矩形」的面积并 < W×H。
//   面积并用「按 x 扫描 + 线段树维护 y 方向被覆盖总长」在 O(p log p) 内求出。
//   总复杂度 O(p log p · log min(n,m))，空间 O(p)。
//
//   优化：建筑物的排序在二分前一次性完成（按 x1 / x2 / y1 / y2 各排一次），
//   之后每次 check 只做线性归并（clamp 是单调的，不破坏有序性），
//   避免了每轮 O(p log p) 的重复排序。扫描中面积一旦达到 W×H 立即返回 false。
//
// 输入输出：stdin -> stdout。题面「每一组数据」但未给组数 T，样例为单组，
//   故按「读到 EOF 为止」处理，每组输出一行答案（兼容单组与多组两种口径）。
//
// 参考来源：
//   * 题面：本目录 content.md（与官方 OJ http://ybt.ssoier.cn:8088/problem_show.php?pid=1752 一致）。
//   * 网络检索：本次任务环境下 Bing / Baidu / 360 / DuckDuckGo / Mojeek / cnblogs / CSDN
//     站内搜均返回反爬校验页或无关结果，GitHub 相关仓库（ThreebodyDarkforest/YBT、
//     PhantomPixel-0418/ybtCode 等）中不含 1752/高手训练篇代码，未能取到公开题解。
//     **故本标程为自研实现**（算法思路：二分答案 + 矩形面积并扫描线，属该题型的标准做法），
//     已在题面样例上验证输出 3，详见 gen-report.md。
//
// 编译：g++ -O2 -std=c++17 -Wall -Wextra std.cpp -o std

#include <cstdio>
#include <climits>
#include <vector>
#include <algorithm>
#include <utility>
using namespace std;

typedef long long ll;

static int n, m, p;
static vector<int> X1, Y1, X2, Y2;
static vector<int> ordX1, ordX2, ordY1, ordY2;  // 按 x1/x2/y1/y2 排序的建筑物下标

// ---- 线段树（维护 y 方向被覆盖总长）----
static vector<int> cnt;   // 覆盖次数标记
static vector<int> cov;   // 该节点覆盖的 y 长度（<= 1e6，int 足够）
static vector<int> bd;    // 坐标压缩后的边界，size = K+1（<= 1e6+1）

static inline void pull(int node, int l, int r) {
    if (cnt[node] > 0)      cov[node] = bd[r] - bd[l];
    else if (r - l == 1)    cov[node] = 0;
    else                    cov[node] = cov[node << 1] + cov[node << 1 | 1];
}

static void update(int node, int l, int r, int ql, int qr, int v) {
    if (ql <= l && r <= qr) { cnt[node] += v; pull(node, l, r); return; }
    int mid = (l + r) >> 1;
    if (ql < mid) update(node << 1, l, mid, ql, qr, v);
    if (qr > mid) update(node << 1 | 1, mid, r, ql, qr, v);
    pull(node, l, r);
}

// ---- 判定：是否存在 L×L 空正方形 ----
static vector<int> A, B;
static vector<int> ayIdx, byIdx, AX, BX, addList, remList;

static bool check(int L) {
    if (L == 0) return true;
    ll W = (ll)n - L + 1, H = (ll)m - L + 1;
    if (W < 1 || H < 1) return false;
    ll Hb = H + 1;  // y 边界上界（点空间 [1..H] -> 边界空间 [1..H+1]）

    // 1) 生成 y 边界候选：A = clamp(y1-L+1)，B = clamp(y2)+1（各自单调）
    A.resize(p); B.resize(p);
    for (int k = 0; k < p; ++k) {
        int i = ordY1[k];
        ll v = (ll)Y1[i] - L + 1; if (v < 1) v = 1; if (v > Hb) v = Hb;
        A[k] = v;
    }
    for (int k = 0; k < p; ++k) {
        int i = ordY2[k];
        ll v = (ll)Y2[i] + 1; if (v < 1) v = 1; if (v > Hb) v = Hb;
        B[k] = v;
    }

    // 2) 线性归并 + 去重，并补入 1 与 Hb
    bd.clear();
    bd.push_back(1);
    {
        size_t ia = 0, ib = 0;
        while (ia < (size_t)p || ib < (size_t)p) {
            ll va = ia < (size_t)p ? A[ia] : LLONG_MAX;
            ll vb = ib < (size_t)p ? B[ib] : LLONG_MAX;
            ll v = min(va, vb);
            if (bd.back() != v) bd.push_back(v);
            if (va <= vb) ++ia; else ++ib;
        }
        if (bd.back() != Hb) bd.push_back(Hb);
    }
    int K = (int)bd.size() - 1;

    // 3) 每个建筑物 y 区间在压缩坐标下的下标（利用 A/B 有序，指针扫描 O(p+K)）
    ayIdx.resize(p); byIdx.resize(p);
    {
        int ptr = 0;
        for (int k = 0; k < p; ++k) { ll v = A[k]; while (bd[ptr] < v) ++ptr; ayIdx[ordY1[k]] = ptr; }
        ptr = 0;
        for (int k = 0; k < p; ++k) { ll v = B[k]; while (bd[ptr] < v) ++ptr; byIdx[ordY2[k]] = ptr; }
    }

    // 4) 计算每个建筑物在 x 方向的禁止区间
    AX.resize(p); BX.resize(p);
    for (int i = 0; i < p; ++i) {
        ll ax = (ll)X1[i] - L + 1; if (ax < 1) ax = 1;
        ll bx = (ll)X2[i];         if (bx > W) bx = W;
        AX[i] = (int)ax; BX[i] = (int)bx;
    }

    // 5) 事件序列（active 且保持各自有序）
    addList.clear(); remList.clear();
    for (int k = 0; k < p; ++k) {
        int i = ordX1[k];
        if (AX[i] <= BX[i] && ayIdx[i] < byIdx[i]) addList.push_back(i);
    }
    for (int k = 0; k < p; ++k) {
        int i = ordX2[k];
        if (AX[i] <= BX[i] && ayIdx[i] < byIdx[i]) remList.push_back(i);
    }

    // 6) 扫描线
    cnt.assign(4 * K + 4, 0);
    cov.assign(4 * K + 4, 0);
    ll total = W * H;
    ll area = 0, prevX = 1;
    size_t ja = 0, jr = 0;
    while (ja < addList.size() || jr < remList.size()) {
        ll xa = ja < addList.size() ? (ll)AX[addList[ja]] : LLONG_MAX;
        ll xr = jr < remList.size() ? (ll)BX[remList[jr]] + 1 : LLONG_MAX;
        ll cur = min(xa, xr);
        if (cur > prevX) {
            if (cov[1] < H) return true;   // 存在未被覆盖的列 -> 存在空正方形
            area += (cur - prevX) * cov[1];
            if (area >= total) return false;  // 可行域已被完全覆盖
            prevX = cur;
        }
        while (ja < addList.size() && (ll)AX[addList[ja]] == cur) {
            int i = addList[ja]; update(1, 0, K, ayIdx[i], byIdx[i], +1); ++ja;
        }
        while (jr < remList.size() && (ll)BX[remList[jr]] + 1 == cur) {
            int i = remList[jr]; update(1, 0, K, ayIdx[i], byIdx[i], -1); ++jr;
        }
    }
    area += ((ll)(W + 1) - prevX) * cov[1];  // 收尾（cov[1] 此时应为 0）
    return area < total;
}

int main() {
    while (scanf("%d %d %d", &n, &m, &p) == 3) {
        X1.assign(p, 0); Y1.assign(p, 0); X2.assign(p, 0); Y2.assign(p, 0);
        for (int i = 0; i < p; ++i) {
            int a, b, c, d;
            scanf("%d %d %d %d", &a, &b, &c, &d);
            if (a > c) swap(a, c);   // 容错：题面保证左下/右上，仍做规范化
            if (b > d) swap(b, d);
            X1[i] = a; Y1[i] = b; X2[i] = c; Y2[i] = d;
        }

        // 预先排序，供二分中线性归并复用
        ordX1.resize(p); ordX2.resize(p); ordY1.resize(p); ordY2.resize(p);
        for (int i = 0; i < p; ++i) ordX1[i] = ordX2[i] = ordY1[i] = ordY2[i] = i;
        sort(ordX1.begin(), ordX1.end(), [](int a, int b){ return X1[a] < X1[b]; });
        sort(ordX2.begin(), ordX2.end(), [](int a, int b){ return X2[a] < X2[b]; });
        sort(ordY1.begin(), ordY1.end(), [](int a, int b){ return Y1[a] < Y1[b]; });
        sort(ordY2.begin(), ordY2.end(), [](int a, int b){ return Y2[a] < Y2[b]; });

        int lo = 0, hi = min(n, m), ans = 0;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (check(mid)) { ans = mid; lo = mid + 1; }
            else hi = mid - 1;
        }
        printf("%d\n", ans);
    }
    return 0;
}
