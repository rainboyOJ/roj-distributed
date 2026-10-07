// 一本通 1818《树上取石子》标程 (std.cpp)
//
// 来源说明（详见 gen-report.md "来源" 一节）：
//   按任务要求用题面特征句（"Alice希望在让Bob取得尽可能少的前提下，自己取得最多"、
//   "一本通 1818 树上取石子 题解"）在 必应 / DuckDuckGo / 搜狗 / 360 / 博客园站内搜
//   做了 4 轮检索：必应对中文整句只做分词（返回"一""树"等字典页），
//   搜狗/360/博客园站内搜全部跳人机验证（验证码页），DuckDuckGo 无结果。
//   仅从搜狗快照看到存在一篇博客园随笔标题「信息学奥赛 一本通1818：树上取石子」
//   （正文含"原题链接"），但直连 URL 被验证码拦截，未能取到正文。
//   因此本题标程为**依题面 + 【样例解释】自行推导**，并用题面样例验证（输出 7 16，与样例一致）。
//
// 模型（博弈 DP）：
//   把根记为 depth 0。谁取结点 u 完全由 depth(u) 的奇偶决定：
//     偶数深度 -> Alice 取，奇数深度 -> Bob 取（根由 Alice 先取，且每次只能往下走一层）。
//   设 solve(u) = 从"当前玩家取走 u"开始、直到走到某个叶子结束的子博弈中
//     (Alice 得石总数, Bob 得石总数)。
//   - u 为叶子：depth 偶 -> (num[u], 0)；depth 奇 -> (0, num[u])。
//   - depth(u) 偶：Alice 取 u，随后 **Bob** 在 u 的儿子里挑一个继续。
//     Bob 的偏好是「先让自己尽可能多，再让 Alice 尽可能少」，
//     故 v* = argmax over children ( B[v] , -A[v] )（字典序，先 B 后 -A）；
//     solve(u) = ( num[u] + A[v*], B[v*] )。
//   - depth(u) 奇：Bob 取 u，随后 **Alice** 在 u 的儿子里挑一个继续。
//     Alice 的偏好是「先让 Bob 尽可能少，再让自己尽可能多」，
//     故 v* = argmin over children ( B[v] , -A[v] )；
//     solve(u) = ( A[v*], num[u] + B[v*] )。
//   两人比较的是**最终总量**，但已经取定的石子在剩余子博弈中是常数，
//   对最终总量的字典序偏好等价于对子树结果的字典序偏好，故上式自洽。
//   答案 = solve(root)。
//
// 实现要点：
//   - O(n) 时间；n <= 1e5，用显式栈做先序遍历（父在子前）再逆序做 DP，避免链状数据递归爆栈。
//   - 儿子用链式前向星（head/nxt/to）存储，避免 vector 数组开销。
//   - 根 = 入度为 0 的结点（题面保证是有向树）。
//   - num[i] <= 1e4、路径和 <= 1e5*1e4 = 1e9 < 2^31，仍用 long long 保存。
//   - 平局处理按题面偏好的第二关键字，与【样例解释】一致（样例中 Bob 在 2/3 间
//     都以 16 取平，靠第二关键字"Alice 更少"选 3）。
#include <cstdio>
#include <vector>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    std::vector<int> num(n + 1);
    for (int i = 1; i <= n; ++i) scanf("%d", &num[i]);

    std::vector<int> head(n + 1, -1), nxt(n + 1, 0), to(n + 1, 0), indeg(n + 1, 0);
    int m = 0;
    for (int e = 1; e < n; ++e) {
        int u, v;
        if (scanf("%d %d", &u, &v) != 2) break;
        to[m] = v;
        nxt[m] = head[u];
        head[u] = m++;
        ++indeg[v];
    }

    int root = 1;
    for (int i = 1; i <= n; ++i)
        if (indeg[i] == 0) { root = i; break; }

    // 先序遍历（父结点一定先于子结点入列）
    std::vector<int> order;
    order.reserve(n);
    std::vector<int> stk;
    stk.reserve(n);
    stk.push_back(root);
    while (!stk.empty()) {
        int u = stk.back();
        stk.pop_back();
        order.push_back(u);
        for (int e = head[u]; e != -1; e = nxt[e]) stk.push_back(to[e]);
    }

    // 深度奇偶：0 = Alice 取，1 = Bob 取
    std::vector<char> par(n + 1, 0);
    for (size_t i = 0; i < order.size(); ++i) {
        int u = order[i];
        for (int e = head[u]; e != -1; e = nxt[e]) par[to[e]] = (char)(par[u] ^ 1);
    }

    std::vector<long long> A(n + 1, 0), B(n + 1, 0);
    for (int i = (int)order.size() - 1; i >= 0; --i) {
        int u = order[i];
        int best = -1;
        if (par[u] == 0) {
            // Alice 取 u，Bob 选儿子：max (B, -A)
            for (int e = head[u]; e != -1; e = nxt[e]) {
                int v = to[e];
                if (best == -1 || B[v] > B[best] || (B[v] == B[best] && A[v] < A[best]))
                    best = v;
            }
            if (best == -1) { A[u] = num[u]; B[u] = 0; }
            else { A[u] = num[u] + A[best]; B[u] = B[best]; }
        } else {
            // Bob 取 u，Alice 选儿子：min (B, -A)
            for (int e = head[u]; e != -1; e = nxt[e]) {
                int v = to[e];
                if (best == -1 || B[v] < B[best] || (B[v] == B[best] && A[v] > A[best]))
                    best = v;
            }
            if (best == -1) { A[u] = 0; B[u] = num[u]; }
            else { A[u] = A[best]; B[u] = num[u] + B[best]; }
        }
    }

    printf("%lld %lld\n", A[root], B[root]);
    return 0;
}
