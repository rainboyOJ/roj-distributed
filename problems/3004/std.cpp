// std.cpp：区间最大和 —— 倍增（二进制跳跃）做法。
// 思路：
//   1. 先求前缀和 sum[i] = A[1] + ... + A[i]，则 "sum[i] <= T" 具有二分性（A[i] 为正，sum 严格递增）；
//   2. 从位置 0 出发，从大到小尝试跳 2^i 个位置，跳完之后仍满足 sum[pos] <= T 才真的跳；
//   3. 最后停留的位置就是最大的 k。每个询问 O(log N)，总复杂度 O(N + Q log N)。
#include <cstdio>

const int MAXN = 100005;

int n, q;
long long sum[MAXN]; // sum[i] = A[1] + ... + A[i]，sum[0] = 0

// 得到最大的 k，使得 2^k <= n
int get_max_k(int n)
{
    int maxk = 0;
    while ((1 << (maxk + 1)) <= n)
        maxk++;
    return maxk;
}

// 检查跳到位置 pos 之后是否仍然可行（前缀和不超过 T）
bool check(int pos, long long T)
{
    return sum[pos] <= T;
}

// 从位置 0 开始向右跳，求最后一个满足 sum[pos] <= T 的位置
int jump(long long T)
{
    int k = get_max_k(n);
    int x = 0;
    for (int i = k; i >= 0; i--) {
        int len = (1 << i); // 本轮尝试的跳跃长度是 2^i
        int pos = x + len;  // 跳过去之后的位置
        if (pos <= n && check(pos, T)) {
            x = pos; // 不越界且不超过 T 才真的跳
        }
    }
    return x;
}

int main()
{
    scanf("%d %d", &n, &q);
    for (int i = 1; i <= n; i++) {
        long long a;
        scanf("%lld", &a);
        sum[i] = sum[i - 1] + a; // 前缀和，注意 A[i] 最大 1e9，要用 long long
    }
    while (q--) {
        long long T;
        scanf("%lld", &T);
        printf("%d\n", jump(T));
    }
    return 0;
}
