/*
 * 一本通 1814 「方格染色」
 * 题面来源: .ybt-import/staging/1814/content.md
 * 官方题面页: https://ybt.ssoier.cn/problem_show.php?pid=1814
 *            (信息学奥赛一本通 · 高手训练篇 · 六、数学基础(高手训练))
 *
 * 检索说明 (共 4 轮, 未找到可直接改写的公开题解/AC 代码, 故按题面自研):
 *   1. DuckDuckGo (html + lite): 「一本通 1814 方格染色 题解」「"整行涂黑" 方格染色 期望」→ 无有效结果
 *   2. Bing: 「"方格染色" 一本通 1814」→ 无有效结果
 *   3. CSDN 站内 API: 「一本通 1814 方格染色」→ 仅习题集目录页
 *      https://blog.csdn.net/dllglvzhenfeng/article/details/135895208 (只列官方题面链接, 无代码)
 *   4. CSDN 站内 API: 「方格染色 2^{r+c}」「高手训练 方格染色 题解」→ 命中均为 CQOI2017 老C的方块等同名题, 非本题
 *
 * 算法 (期望的线性性 + 子集展开, O(n^2)):
 *   棋盘为 [n]×[n] -> [m] 的均匀随机单射; 选的 k 个数是 [m] 的均匀 k-子集, 二者独立。
 *   记 r = 整行涂黑的行数, c = 整列涂黑的列数, 得分 2^{r+c}。
 *   因为 2^r 等于「黑行集合的子集个数」, 所以
 *     2^{r+c} = Σ_{R⊆[n]} Σ_{C⊆[n]} [R 中每行整行涂黑 ∧ C 中每列整列涂黑]。
 *   取期望, 按 |R|=a, |C|=b 归并 (对称性):
 *     E = Σ_{a=0..n} Σ_{b=0..n} C(n,a)·C(n,b)·f(t),  t = n(a+b) − ab,
 *   其中 t 是 R 的行与 C 的列覆盖的格子数, f(t) = P(指定的 t 个格子全黑):
 *     这 t 个格子的取值构成 [m] 的均匀 t-子集, 全黑 <=> 选的 k 个数包含这 t 个值
 *     f(t) = C(m−t, k−t)/C(m,k) = Π_{i=0}^{t−1} (k−i)/(m−i),  t > k 时为 0。
 *   用 log 前缀和把每个 f(t) 降到 O(1): logf[t] = Σ log(k−i) − log(m−i), f = exp(logf)。
 *   双重循环 O(n^2) (n ≤ 300 → 9.06e4 项)。
 *
 * 数值与精度:
 *   - C(n,a) ≤ C(300,150) ≈ 9.4e88, 用 Pascal 三角以 double 直接算 (无溢出, 乘积 ≤ ~8.8e177)。
 *   - f(t) 下溢为 0 时对应项 < 1e-308, 远小于答案下界 1, 可安全忽略。
 *   - Kahan 求和; 最终相对误差 ~1e-12, 满足题面 1e-6 要求。
 *   - 答案 > 1e99 时截断输出 1e99; 用 %.10e 输出 (相对误差判题)。
 *
 * 编译: g++ -O2 -std=c++17 -o std std.cpp
 * 运行: ./std < problem1.in
 */
#include <cstdio>
#include <cmath>
#include <vector>
#include <algorithm>

int main() {
    long long n, m, k;
    if (scanf("%lld %lld %lld", &n, &m, &k) != 3) return 1;

    const int N = (int)n;
    const long long T = n * n;              /* t 的最大值 = n^2 (a=b=n) */

    /* logf[t] = ln f(t), 仅对 t <= min(n^2, k) 有意义; t > k 时 f(t) = 0 */
    std::vector<double> logf((size_t)T + 1, 0.0);
    long long tmax = std::min(T, k);
    for (long long t = 1; t <= tmax; ++t)
        logf[t] = logf[t - 1] + log((double)(k - t + 1)) - log((double)(m - t + 1));

    /* 组合数 C(n,a) (double, 最大约 9.4e88) */
    std::vector<std::vector<double> > C(N + 1, std::vector<double>(N + 1, 0.0));
    for (int i = 0; i <= N; ++i) {
        C[i][0] = 1.0;
        for (int j = 1; j <= i; ++j)
            C[i][j] = C[i - 1][j - 1] + C[i - 1][j];
    }

    /* Kahan 求和 */
    double sum = 0.0, comp = 0.0;
    for (int a = 0; a <= N; ++a) {
        for (int b = 0; b <= N; ++b) {
            long long t = (long long)n * a + (long long)n * b - (long long)a * b;
            if (t > k) continue;                    /* f(t) = 0 */
            double f = exp(logf[t]);
            double term = C[N][a] * C[N][b] * f;
            double y = term - comp;
            double s = sum + y;
            comp = (s - sum) - y;
            sum = s;
        }
    }

    if (sum > 1e99) sum = 1e99;
    printf("%.10e\n", sum);
    return 0;
}
