// 一本通 1421 Floyd 标程
// 解法来源：CSDN 题解 https://blog.csdn.net/hejx0412/article/details/122021862 （1421：Floyd）
// 思路：Floyd 全源最短路，不可达置 INF=1e16，最后按题面程序求 S ^= Dis(i,j)+f
// 复杂度：O(n^3)，n<=500，1s 内可通过
#include <cstdio>
#include <cstring>
#include <algorithm>
using namespace std;

const long long INF = (long long)1e16;

int n, m;
long long dis[505][505];

int main() {
    scanf("%d %d", &n, &m);
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            dis[i][j] = (i == j) ? 0 : INF;
    for (int i = 0; i < m; i++) {
        int s, t;
        long long d;
        scanf("%d %d %lld", &s, &t, &d);
        if (d < dis[s][t]) dis[s][t] = d; // 可能有重边，取最小
    }
    // Floyd：只在两端可达时松弛，避免 INF 溢出
    for (int k = 1; k <= n; k++)
        for (int i = 1; i <= n; i++) {
            if (dis[i][k] == INF) continue;
            for (int j = 1; j <= n; j++) {
                if (dis[k][j] == INF) continue;
                if (dis[i][k] + dis[k][j] < dis[i][j])
                    dis[i][j] = dis[i][k] + dis[k][j];
            }
        }
    long long S = 0, f = (long long)1e16;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            S ^= dis[i][j] + f;
    printf("%lld\n", S);
    return 0;
}
