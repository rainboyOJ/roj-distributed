// 一本通 1740《星空穿越》 标程（C++17，stdin -> stdout，多组数据）
//
// 来源：用题面特征句在 bing / CSDN 站内搜索 / 洛谷 / 博客园等渠道精确检索，
// 未找到本题任何公开题解或参考代码，故本标程为**依据题面自研**（检索记录见
// gen-report.md「来源」一节）。
//
// 题意：无向简单图，边带标记 c_e∈{0,1}（c=1 表示该通道当前被经过奇数次）。
// 安排尽量少的行走 P_1..P_K（路径可重复经过边/点），使每条边被走过的总次数
// ≡ c_e (mod 2)。
//
// 算法：令 S={e | c_e=1}。对每个连通块 C，设 T_C = S∩C 中度为奇数的顶点集
// （|T_C| 为偶数），则
//     K_min = Σ_C ( |T_C| > 0 ? |T_C|/2 : [S_C ≠ ∅] )
// 下界：一次行走只在其两端点处贡献度奇偶变化，故 C 内至少 |T_C|/2 条行走；
// 若 S_C≠∅ 而 T_C=∅，则至少 1 条（否则什么都走不了）。
// 上界（构造）：取 C 的生成树 T*（每树边取 2 份），令多重边集
// M = S_C ∪ 2·T*，则 M 连通且奇度点恰为 T_C。
//   · T_C=∅：M 有欧拉回路 → 1 条行走（顺路兜进任意欧拉子图）。
//   · T_C≠∅：加虚点 X 与 T_C 各点连 1 条边，全图偶度且连通，从 X 出发求
//     欧拉回路；回路每次经过 X 即切开，恰得 |T_C|/2 条路径，端点都在 T_C。
// 总长 Σ l_i ≤ Σ_C(|S_C| + 2(n_C-1) + |T_C|/2) = O(n+m)，远小于 5×10^6 限制。
// 复杂度 O(n+m) + 输出 O(n+m)，Σn,Σm ≤ 5×10^5（2s / 512MB 无压力）。
//
#include <cstdio>
#include <cstring>
#include <vector>
#include <algorithm>

using namespace std;

/* ── 输入缓冲（fread 快读） ── */
static const int IN_BUF_SZ = 1 << 16;
static char inBuf[IN_BUF_SZ];
static int inPos = 0, inLen = 0;

static inline int gc() {
    if (inPos == inLen) {
        inLen = (int)fread(inBuf, 1, IN_BUF_SZ, stdin);
        inPos = 0;
        if (inLen <= 0) return -1;
    }
    return (unsigned char)inBuf[inPos++];
}

static inline int readInt() {
    int c = gc();
    while (c >= 0 && c <= ' ') c = gc();
    int x = 0;
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = gc(); }
    return x;
}

/* ── 输出缓冲（逐数字写入，缓冲满即 flush） ── */
static const int OUT_BUF_SZ = 1 << 20;
static char outBuf[OUT_BUF_SZ];
static int outPos = 0;

static inline void outFlush() {
    if (outPos) { fwrite(outBuf, 1, outPos, stdout); outPos = 0; }
}
static inline void outChar(char ch) {
    if (outPos == OUT_BUF_SZ) outFlush();
    outBuf[outPos++] = ch;
}
static inline void outInt(int x) {
    char tmp[12];
    int t = 0;
    if (x == 0) tmp[t++] = '0';
    while (x > 0) { tmp[t++] = (char)('0' + x % 10); x /= 10; }
    while (t > 0) outChar(tmp[--t]);
}

int main() {
    int T = readInt();
    if (T < 0) T = 0;

    /* 跨测试用例复用缓冲，避免重复分配 */
    vector<int> eu, ev, ec, pdeg;                       // 边表、顶点奇偶度
    vector<int> cnt, gOff, gTo, gEid, gCur;             // G 的 CSR 邻接
    vector<int> comp, compStart, verts, parEdge, stk;   // 连通块 / 生成树
    vector<char> isTree;
    vector<int> eStart, eCur2, eOrder;                  // 边按连通块分组
    vector<char> compHasS;
    vector<int> loc, locInv;
    vector<int> mu, mv;                                 // M 的边（局部编号）
    vector<int> nbr, tw;                                // 邻点 / 孪生位置
    vector<char> hUsed;
    vector<int> off, ptr, seq, seg;

    for (int tc = 0; tc < T; tc++) {
        int n = readInt(), m = readInt();
        eu.assign(m, 0); ev.assign(m, 0); ec.assign(m, 0);
        pdeg.assign(n, 0);
        for (int i = 0; i < m; i++) {
            int a = readInt() - 1, b = readInt() - 1, c = readInt();
            eu[i] = a; ev[i] = b; ec[i] = c;
            pdeg[a] ^= c; pdeg[b] ^= c;
        }

        /* ── G 的 CSR 邻接 ── */
        cnt.assign(n, 0);
        for (int i = 0; i < m; i++) { cnt[eu[i]]++; cnt[ev[i]]++; }
        gOff.assign(n + 1, 0);
        for (int v = 0; v < n; v++) gOff[v + 1] = gOff[v] + cnt[v];
        gTo.assign(2 * m, 0); gEid.assign(2 * m, 0);
        gCur.assign(gOff.begin(), gOff.end());
        for (int i = 0; i < m; i++) {
            int a = eu[i], b = ev[i];
            gTo[gCur[a]] = b; gEid[gCur[a]++] = i;
            gTo[gCur[b]] = a; gEid[gCur[b]++] = i;
        }

        /* ── 连通块划分（迭代 DFS）+ 生成树（parEdge） ── */
        comp.assign(n, -1);
        parEdge.assign(n, -1);
        compStart.clear();
        verts.clear();
        stk.clear();
        int ncomp = 0;
        for (int s = 0; s < n; s++) {
            if (comp[s] != -1) continue;
            compStart.push_back((int)verts.size());
            comp[s] = ncomp;
            stk.push_back(s);
            while (!stk.empty()) {
                int v = stk.back(); stk.pop_back();
                verts.push_back(v);
                for (int q = gOff[v]; q < gOff[v + 1]; q++) {
                    int to = gTo[q];
                    if (comp[to] == -1) {
                        comp[to] = ncomp;
                        parEdge[to] = gEid[q];
                        stk.push_back(to);
                    }
                }
            }
            ncomp++;
        }
        compStart.push_back((int)verts.size());

        /* ── 边按连通块计数排序，便于逐块取边 ── */
        eStart.assign(ncomp + 1, 0);
        for (int i = 0; i < m; i++) eStart[comp[eu[i]] + 1]++;
        for (int c = 0; c < ncomp; c++) eStart[c + 1] += eStart[c];
        eCur2.assign(eStart.begin(), eStart.end());
        eOrder.assign(m, 0);
        for (int i = 0; i < m; i++) { int c = comp[eu[i]]; eOrder[eCur2[c]++] = i; }

        isTree.assign(m, 0);
        for (int v = 0; v < n; v++) if (parEdge[v] >= 0) isTree[parEdge[v]] = 1;
        (void)isTree;
        compHasS.assign(ncomp, 0);
        for (int i = 0; i < m; i++) if (ec[i]) compHasS[comp[eu[i]]] = 1;

        /* ── 第一遍：K = Σ_C ( |T_C|>0 ? |T_C|/2 : [S_C≠∅] ) ── */
        int totalK = 0;
        for (int c = 0; c < ncomp; c++) {
            if (!compHasS[c]) continue;
            int nT = 0;
            for (int idx = compStart[c]; idx < compStart[c + 1]; idx++)
                if (pdeg[verts[idx]]) nT++;
            totalK += (nT > 0 ? nT / 2 : 1);
        }
        outInt(totalK); outChar('\n');

        /* ── 第二遍：逐连通块构造，Hierholzer 输出路径 ── */
        loc.assign(n, -1);
        for (int c = 0; c < ncomp; c++) {
            if (!compHasS[c]) continue;
            int vBeg = compStart[c], vEnd = compStart[c + 1];
            int nC = vEnd - vBeg;
            int nT = 0;
            for (int idx = vBeg; idx < vEnd; idx++) if (pdeg[verts[idx]]) nT++;

            locInv.resize(nC);
            for (int idx = vBeg; idx < vEnd; idx++) {
                int v = verts[idx];
                loc[v] = idx - vBeg;
                locInv[idx - vBeg] = v;
            }

            /* M 的边表（局部编号）：树边 2 份 + S 边 1 份 + 虚点边 1 份 */
            mu.clear(); mv.clear();
            for (int idx = vBeg; idx < vEnd; idx++) {
                int v = verts[idx];
                int pe = parEdge[v];
                if (pe >= 0) {
                    int u = (eu[pe] == v) ? ev[pe] : eu[pe];
                    mu.push_back(loc[u]); mv.push_back(loc[v]);
                    mu.push_back(loc[u]); mv.push_back(loc[v]);
                }
            }
            for (int e = eStart[c]; e < eStart[c + 1]; e++) {
                int i = eOrder[e];
                if (ec[i]) { mu.push_back(loc[eu[i]]); mv.push_back(loc[ev[i]]); }
            }
            const int X = (nT > 0) ? nC : -1;
            if (X >= 0)
                for (int idx = vBeg; idx < vEnd; idx++)
                    if (pdeg[verts[idx]]) { mu.push_back(X); mv.push_back(idx - vBeg); }

            /* 按「局部顶点」建邻接（CSR）：X 视为独立顶点；
               nbr[k] = 位置 k 一端通向的邻点，tw[k] = 该边另一端在 nbr 中的位置 */
            int mvtx = nC + (X >= 0 ? 1 : 0);
            int me = (int)mu.size();
            off.assign(mvtx + 1, 0);
            for (int i = 0; i < me; i++) { off[mu[i] + 1]++; off[mv[i] + 1]++; }
            for (int v = 0; v < mvtx; v++) off[v + 1] += off[v];
            ptr.assign(off.begin(), off.end());
            nbr.assign(2 * me, 0);
            tw.assign(2 * me, 0);
            for (int i = 0; i < me; i++) {
                int p = ptr[mu[i]]++, q = ptr[mv[i]]++;
                nbr[p] = mv[i]; tw[p] = q;
                nbr[q] = mu[i]; tw[q] = p;
            }

            /* Hierholzer 迭代求欧拉回路（起点 base） */
            auto hierholzer = [&](int base, vector<int> &outSeq) {
                outSeq.clear();
                hUsed.assign(2 * me, 0);
                ptr.assign(off.begin(), off.end());
                seg.clear(); seg.push_back(base);
                while (!seg.empty()) {
                    int v = seg.back();
                    int chosen = -1;
                    while (ptr[v] < off[v + 1]) {
                        int i = ptr[v]++;
                        if (!hUsed[i]) { chosen = i; break; }
                    }
                    if (chosen == -1) {
                        outSeq.push_back(v);
                        seg.pop_back();
                    } else {
                        hUsed[chosen] = 1; hUsed[tw[chosen]] = 1;
                        seg.push_back(nbr[chosen]);
                    }
                }
                // outSeq 为回路顶点序列（逆序），首尾相同
                reverse(outSeq.begin(), outSeq.end());
            };

            if (X < 0) {
                /* T_C=∅：M 有欧拉回路，输出 1 条行走 */
                hierholzer(0, seq);
                int L = (int)seq.size();
                outInt(L);
                for (int i = 0; i < L; i++) { outChar(' '); outInt(locInv[seq[i]] + 1); }
                outChar('\n');
            } else {
                /* T_C≠∅：从 X 出发的欧拉回路，按 X 切开成 |T_C|/2 条路径；
                   seq 为回路顶点序列（seq[0]=seq.back()=X），两处 X 之间的
                   实顶点段就是一条路径，虚点 X 不输出。 */
                hierholzer(X, seq);
                int prev = 0;
                for (int i = 1; i < (int)seq.size(); i++) {
                    if (seq[i] != X) continue;
                    int l = prev + 1, r = i - 1;
                    if (l <= r) {
                        int L = r - l + 1;
                        outInt(L);
                        for (int j = l; j <= r; j++) { outChar(' '); outInt(locInv[seq[j]] + 1); }
                        outChar('\n');
                    }
                    prev = i;
                }
            }
        }
    }
    outFlush();
    return 0;
}
