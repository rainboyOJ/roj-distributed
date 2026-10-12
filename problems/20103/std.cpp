#include <iostream>
#include <cstdio>
#include <cmath>
#include <algorithm>
#include <vector>
#include <set>
#include <fstream>
#include <string>
#include <chrono>
#include <random>
using namespace std;

#define endl '\n'
#define int long long
#define PII pair<int, int>
#define PIII pair<int, pair<int, int>>
#define x first
#define y second

const int N = 55;
const int MAX_STATES = 1 << 20;

int n, m;
int color[N], weight[N];           // 节点颜色和权重
int graph[N][N];                   // 邻接矩阵
int color_count[N];                // 每种颜色的出现次数
int dp[N][MAX_STATES];             // 动态规划数组
int color_id[N];                   // 重复颜色的新编号
int unique_colors;                 // 重复颜色的数量

void solve() {
    // freopen("sample2.in", "r", stdin);
    // freopen("sample2.out", "w", stdout);
    // 输入数据
    cin >> n >> m;
    
    // 读取颜色并统计出现次数
    for (int i = 1; i <= n; i++) {
        cin >> color[i];
        color_count[color[i]]++;
    }
    
    // 读取权重并为重复颜色分配新编号
    for (int i = 1; i <= n; i++) {
        cin >> weight[i];
        if (color_count[i] > 1) {
            color_id[i] = unique_colors++;
        }
    }
    
    // 读取图的边
    for (int i = 1; i <= m; i++) {
        int u, v;
        cin >> u >> v;
        graph[u][v] = 1;
    }
    
    // Floyd算法计算可达性
    for (int k = 1; k <= n; k++) {
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                if (i != j) {
                    graph[i][j] |= (graph[i][k] & graph[k][j]);
                }
            }
        }
    }
    
    // 初始化第一个节点的状态
    if (color_count[color[1]] == 1) {
        dp[1][0] = weight[color[1]];
    } else {
        dp[1][1LL << color_id[color[1]]] = weight[color[1]];
    }
    
    // 动态规划：枚举所有节点对和状态
    for (int i = 1; i <= n; i++) {
        for (int j = i + 1; j <= n; j++) {
            if (!graph[i][j]) continue;  // 不可达则跳过
            
            for (int state = 0; state < (1LL << unique_colors); state++) {
                if (color_count[color[j]] == 1) {
                    // 单次出现的颜色，直接转移
                    dp[j][state] = max(dp[j][state], dp[i][state] + weight[color[j]]);
                } else if (!(state & (1LL << color_id[color[j]]))) {
                    // 重复颜色且未访问过，更新状态
                    int new_state = state | (1LL << color_id[color[j]]);
                    dp[j][new_state] = max(dp[j][new_state], dp[i][state] + weight[color[j]]);
                }
            }
        }
    }
    
    // 输出每个节点的最大价值
    for (int i = 1; i <= n; i++) {
        int max_value = 0;
        for (int state = 0; state < (1LL << unique_colors); state++) {
            max_value = max(max_value, dp[i][state]);
        }
        cout << max_value << endl;
    }
}

signed main() {
    ios::sync_with_stdio(0);
    cin.tie(0), cout.tie(0);
    
    int T = 1;
    // cin >> T;
    while (T--) {
        solve();
    }
    return 0;
}
