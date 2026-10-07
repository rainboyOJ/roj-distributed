// 一本通 1750《取数字》标程  —— 自研（未找到公开题解）
// 题目页（已核对题面/样例一致）：http://ybt.ssoier.cn:8088/problem_show.php?pid=1750
//   （该页题面正文为空，仅样例 3 / 1 2 3 -> 3 3 4 可核对，与 staging/content.md 完全一致）
// 来源说明：CSDN / 博客园 / 必应 / 搜狗 / 360 多次检索
//   「一本通 1750 取数字」「ybtoj1750」「取数字 围成一圈 轮流 空位」
//   「"每步只能选那些旁边至少有一个空位的数"」「"本题测评时开栈"」等特征句，
//   均未检索到本题题解或 AC 代码（ybt 官方 OJ 该题 382 次提交仅 29 通过，无公开代码），
//   故本标程为自研实现，依据为下面第 1 节的推导 + 题面样例验证。
//
// ---------------------------------------------------------------------------
// 1. 结论（自研推导，已用题面样例逐点验证）
//    固定第一步取 a[i] 后，剩余数构成线性序列
//        C = (a[i+1], a[i+2], ..., a[i-1])          （长度 N-1）
//    由于"空位"始终是含 i 的连续弧，"旁边至少有一个空位"的候选恰好是剩余
//    区间的两个端点；题面规定"有多个时选较大的"，于是整个过程完全确定：
//    每次取走当前区间的较大端点（两端比较）。
//    记取数顺序为 x0,x1,...（x0 是第二个人取走的），
//        D = x0 - x1 + x2 - x3 + ...（交错和）
//    设 S = Σa_i。后手取的是偶数位，先手（除第一步外）取奇数位，故
//        后手得分 = (ΣC + D)/2 ，先手得分 = S - 后手得分 = (S + a[i] - D)/2
//    （已核样例：N=3,a=[1,2,3] -> 3,3,4）
//
// 2. 复杂度
//    本标程对每个起点 O(N) 模拟，总复杂度 O(N^2)。
//    满分做法（N≤300000，题目标签"数据结构"，题面注明"本题测评时开栈"）
//    未能在本轮时间内自研得到，故此处为 O(N^2) 实现；
//    data.py 因此按"标程可承受规模"分层（详见 gen-report.md 的未决问题）。
// ---------------------------------------------------------------------------
#include <cstdio>
#include <cstdlib>
#include <vector>

using namespace std;

static inline int readInt(long long &x) {
    int c = getchar();
    while (c != '-' && (c < '0' || c > '9')) {
        if (c == EOF) return 0;
        c = getchar();
    }
    int neg = 0;
    if (c == '-') { neg = 1; c = getchar(); }
    x = 0;
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = getchar(); }
    if (neg) x = -x;
    return 1;
}

int main() {
    long long Nll;
    if (!readInt(Nll)) return 0;
    int N = (int)Nll;
    vector<long long> a(N);
    long long S = 0;
    for (int i = 0; i < N; i++) { readInt(a[i]); S += a[i]; }

    // 把圆环复制成 2N 的线性数组，则第 i 个起点对应的 C 是 A2[i+1 .. i+N-1]
    vector<long long> A2(2 * N);
    for (int j = 0; j < 2 * N; j++) A2[j] = a[j % N];

    for (int i = 0; i < N; i++) {
        int l = i + 1, r = i + N - 1;      // N==1 时 l>r，D=0，答案=a[0]
        long long D = 0;
        if (l <= r) {
            // 两端各缓存一个当前值：每步只需重新读入被取走那一侧的新端点（少一半访存）
            int al = A2[l], ar = A2[r];
            // 成对展开：每对贡献 (x0 - x1)；奇数个元素时最后剩一个，符号为 +1
            while (l < r) {
                if (al > ar) { D += al; ++l; al = A2[l]; } else { D += ar; --r; ar = A2[r]; }
                if (al > ar) { D -= al; ++l; al = A2[l]; } else { D -= ar; --r; ar = A2[r]; }
            }
            if (l == r) D += al;            // 此时 al == ar == A2[l]
        }
        printf("%lld\n", (S + a[i] - D) / 2);
    }
    return 0;
}
