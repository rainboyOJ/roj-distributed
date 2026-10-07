#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
using namespace std;

// 题意：给定只含数字、逗号、问号的串，把 ? 替换成数字或逗号，
// 使得结果合法（逗号分隔的正整数序列严格递增，无前导 0，首尾无逗号），
// 且整串字典序最小（',' < '0' < ... < '9'）。无解输出 impossible。

static int n;
static string pat;

// 数字串比较：先比长度，再比字典序（假设无前导 0）
static int cmpNum(const string &a, const string &b) {
    if (a.size() != b.size()) return a.size() < b.size() ? -1 : 1;
    if (a == b) return 0;
    return a < b ? -1 : 1;
}

// 在 pat[s, e) 上填出长度 L=e-s 的合法数字（首位非 0），
// 若 hasLower 为真则要求数值 > lower，返回最小的这种数字串；无解返回空串。
static string minVal(int s, int e, const string &lower, bool hasLower) {
    int L = e - s;
    if (L <= 0) return string();

    // 先构造“最小的匹配数字”（忽略 lower）
    string mn(L, '0');
    for (int i = 0; i < L; i++) {
        char c = pat[s + i];
        if (c == '?') {
            mn[i] = (i == 0) ? '1' : '0';
        } else if (c >= '0' && c <= '9') {
            if (i == 0 && c == '0') return string();  // 前导 0
            mn[i] = c;
        } else {
            return string();  // 数字段里出现 ','（固定）
        }
    }

    if (!hasLower) return mn;
    int Lab = (int)lower.size();
    if (L > Lab) return mn;        // 位数更多，必然更大
    if (L < Lab) return string();  // 位数更少，不可能更大
    if (cmpNum(mn, lower) > 0) return mn;

    // 同位数：找最小的匹配数字 > lower。
    // 枚举“第一个比 lower 大的位置 j”，要取最靠右的 j（这样数最小）。
    for (int j = L - 1; j >= 0; j--) {
        bool ok = true;
        for (int i = 0; i < j; i++) {
            char p = pat[s + i];
            if (p != '?' && p != lower[i]) { ok = false; break; }
        }
        if (!ok) continue;

        char pj = pat[s + j];
        int lo = lower[j] - '0';
        int d = -1;
        for (int dd = lo + 1; dd <= 9; dd++) {
            if (j == 0 && dd == 0) continue;
            if (pj != '?' && (pj - '0') != dd) continue;
            d = dd;
            break;
        }
        if (d < 0) continue;

        string t(L, '0');
        for (int i = 0; i < j; i++) t[i] = lower[i];
        t[j] = (char)('0' + d);
        for (int i = j + 1; i < L; i++) {
            char p = pat[s + i];
            t[i] = (p == '?') ? '0' : p;
        }
        if (t[0] == '0') continue;
        return t;
    }
    return string();
}

// 当前 pat（含已固定的前缀）是否还能补全为合法串。
// best[c+1] = 在逗号位置 c（c=-1 为虚拟起点）处，前面已形成的最后一个数的
// 最小可能值；只保留最小值即可（更小对后续只会更有利）。
static bool feasible() {
    int N = n + 1;  // 下标 0..n，对应逗号位置 -1..n-1
    vector<char> vis(N, 0);
    vector<string> best(N);
    vis[0] = 1;  // 虚拟起点，无下界

    for (int c = -1; c < n; c++) {
        int idx = c + 1;
        if (!vis[idx]) continue;
        bool hasLower = (c >= 0);
        const string &lower = best[idx];
        int s = c + 1;  // 下一个数字从 s 开始
        for (int e = s + 1; e <= n; e++) {
            if (e < n) {
                if (pat[e] != '?' && pat[e] != ',') continue;  // 这里要放逗号
            }
            string v = minVal(s, e, lower, hasLower);
            if (v.empty()) continue;
            if (e == n) return true;  // 最后一个数合法，整体可行
            int nidx = e + 1;         // 新逗号位置 e
            if (!vis[nidx] || cmpNum(v, best[nidx]) < 0) {
                vis[nidx] = 1;
                best[nidx] = v;
            }
        }
    }
    return false;
}

int main() {
    int T;
    if (scanf("%d", &T) != 1) return 0;
    char buf[256];
    while (T--) {
        if (scanf("%255s", buf) != 1) break;
        pat = buf;
        n = (int)pat.size();

        if (!feasible()) {
            puts("impossible");
            continue;
        }

        string ans = pat;
        for (int i = 0; i < n; i++) {
            if (pat[i] != '?') continue;  // 固定字符必须保留
            bool done = false;
            for (char ch : string(",0123456789")) {
                string bak = pat;
                pat[i] = ch;
                if (feasible()) {
                    ans[i] = ch;
                    done = true;
                    break;
                }
                pat = bak;
            }
            (void)done;  // 初始可行保证这里一定 done
        }
        printf("%s\n", ans.c_str());
    }
    return 0;
}
