// 一本通 1698 字符串匹配
// 参考来源（网络公开题解，已改写为 C++17 并经样例+暴力对拍自证正确性）：
//   [KMP] 一本通(ybt.ssoier.cn:8088) 1698 字符串匹配 - CSDN博客
//   https://blog.csdn.net/weixin_30784141/article/details/98445534
// 算法：广义 KMP。
//   “匹配”= s 的子串 w 与 t 之间存在双射 f：w[i]=t[j] 当且仅当 w 中第 i 个位置
//   的字符与 t 中第 j 个位置的字符对应（单射满射，即一一对应）。
//   令 a[i] = i - (字符 s[i] 上一次出现位置，无则取 0)，b 同理。
//   则 w 与 t 匹配  <=>  对所有 k: (a[l+k]==k+1 ? 0 : a[l+k]) == (b[k+1]==k+1 ? 0 : b[k+1])。
//   在此“字符等于 0 或相等”的字符集上做 KMP，匹配位置即为答案。
//   复杂度 O(n + m)，n,m,C <= 1e6，T = 3。
#include <cstdio>
#include <cstring>

#define N 1000005
#define C 1000005

int p[N], a[N], b[N], last[C], ans[N];

inline void read(int &x) {
    char c = getchar();
    for (x = 0; c < '0' || c > '9'; c = getchar());
    for (; c >= '0' && c <= '9'; c = getchar()) x = x * 10 + c - '0';
}

// 出现位置距离越界（超过当前已匹配长度 l）时视作 0
inline int jdg(int x, int l) { return x < l ? x : 0; }
inline bool eq(int x, int y, int l) { return jdg(x, l) == jdg(y, l); }

void work() {
    int n, m, i, j, x;
    read(n); read(m);
    memset(p, 0, sizeof p);
    memset(last, 0, sizeof last);
    for (i = 1; i <= n; i++) {
        read(x);
        a[i] = i - last[x];
        last[x] = i;
    }
    memset(last, 0, sizeof last);
    for (i = 1; i <= m; i++) {
        read(x);
        b[i] = i - last[x];
        last[x] = i;
    }
    // KMP 失配函数
    for (i = 1, j = 0; i < m; i++) {
        while (j && !eq(b[i + 1], b[j + 1], j + 1)) j = p[j];
        if (eq(b[i + 1], b[j + 1], j + 1)) j++;
        p[i + 1] = j;
    }
    // KMP 匹配
    int cnt = 0;
    for (i = 0, j = 0; i < n; i++) {
        while (j && !eq(a[i + 1], b[j + 1], j + 1)) j = p[j];
        if (eq(a[i + 1], b[j + 1], j + 1)) j++;
        if (j == m) {
            ans[++cnt] = i + 2 - m;
            j = p[j];
        }
    }
    printf("%d\n", cnt);
    for (i = 1; i <= cnt; i++) printf("%d ", ans[i]);
    putchar('\n');
}

int main() {
    int t, c, i;
    read(t); read(c);
    for (i = 1; i <= t; i++) work();
    return 0;
}
