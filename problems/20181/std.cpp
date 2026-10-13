#include <bits/stdc++.h>
#define B 233
#define mod 1004535809
#define maxn 500005
using namespace std;
int H1[maxn][20], H2[maxn][20], bs[20], n, q, pre[maxn];
char s[maxn];
int main() {
    scanf("%d%d%s", &n, &q, s);
    bs[19] = B;
    for (int i = 19; i; i--) bs[i - 1] = 1ll * bs[i] * bs[i] % mod;
    for (int j = 0; j < 20; j++)
        if ((1 << j) <= n) {
            pre[0] = s[0];
            for (int i = 1; i < n; i++) pre[i] = (1ll * pre[i - 1] * bs[j] + s[i]) % mod;
            H1[0][j] = pre[(1 << j) - 1];
            for (int i = 1; i + (1 << j) <= n; i++)
                H1[i][j] = (pre[i + (1 << j) - 1] - pre[i - 1] * 795936783ll % mod + mod) % mod;
        }
    for (int i = 0; i < n; i++) H2[i][0] = s[i];
    for (int j = 1; j < 20; j++)
        for (int i = 0; i + (1 << j) <= n; i++)
            H2[i][j] = (H2[i][j - 1] * 1ll * bs[j] + H2[i + (1 << j - 1)][j - 1]) % mod;
    for (int p, k; q--; printf("%d\n", (p + (1 << k) <= n) && (H1[p][k] == H2[p][k]))) scanf("%d%d", &p, &k);
}