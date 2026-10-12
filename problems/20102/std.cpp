#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
#include <cstring>

using namespace std;

const int MAX_A = 200 * 500 + 5;  // 最大可能的 sum_a，a_i 最大为 200，节点数最多为 500
const int INF = INT_MAX;

struct Edge {
    int to, a, b, next;
} edges[2005];

int head[505], edge_cnt;

void add_edge(int u, int v, int a, int b) {
    edges[edge_cnt] = {v, a, b, head[u]};
    head[u] = edge_cnt++;
}

int dp[MAX_A + 1][505];  // dp[sum_a][u] 表示到达 u 且 ∑a_i = sum_a 时最小的 ∑b_i 值

void solve() {
    int N, M;
    cin >> N >> M;

    // 初始化链式前向星
    memset(head, -1, sizeof(head));
    edge_cnt = 0;
    
    for (int i = 0; i < M; i++) {
        int u, v, a, b;
        cin >> u >> v >> a >> b;
        add_edge(u, v, a, b);
    }

    // dp[sum_a][u] 表示到达 u 且 ∑a_i = sum_a 时最小的 ∑b_i 值
    for (int i = 0; i <= MAX_A; i++) {
        for (int j = 0; j <= N; j++) {
            dp[i][j] = INF;  // 初始化为无穷大
        }
    }
    dp[0][1] = 0;  // 从节点 1 出发，∑a_i = 0 时 ∑b_i = 0

    for (int sum_a = 0; sum_a <= MAX_A; sum_a++) {
        for (int u = 1; u <= N; u++) {
            if (dp[sum_a][u] == INF) continue;  // 如果当前状态不可达，则跳过
            for (int i = head[u]; i != -1; i = edges[i].next) {
                int v = edges[i].to;
                int a = edges[i].a;
                int b = edges[i].b;
                int new_sum_a = sum_a + a;
                if (new_sum_a <= MAX_A) {
                    dp[new_sum_a][v] = min(dp[new_sum_a][v], dp[sum_a][u] + b);
                }
            }
        }
    }

    // 查找最优解
    long long best_product = LLONG_MAX;
    int best_a = INF;
    int best_b = INF;

    for (int sum_a = 0; sum_a <= MAX_A; sum_a++) {
        if (dp[sum_a][N] != INF) {
            int sum_b = dp[sum_a][N];
            long long product = (long long)sum_a * sum_b;
            
            // 比较性能值，优先选择性能值更小的路径，若相等则选择 ∑a_i 更小的路径
            if (product < best_product || (product == best_product && sum_a < best_a)) {
                best_product = product;
                best_a = sum_a;
                best_b = sum_b;
            }
        }
    }

    // 输出结果
    cout << best_a << " " << best_b << endl;
}

int main() {
    solve();
    
    return 0;
}
