// 一本通 1418《猴子选大王》标程
//
// 题意：N 只猴子围成一圈（编号 1..N），每只猴子对应一个报数次数 Xi（1 ≤ Xi ≤ 100）。
//       从第 1 号猴子开始，报数到当前报数次数对应的那个猴子出队，再从下一位继续从 1
//       开始报数，如此循环直到只剩下一只猴子，输出它的编号。
// 数据范围（有来源依据）：N ≤ 1e6；每个 Xi ≤ 100。
// 参考来源（网络 C++ 题解，经本机编译、样例与对拍验证后改写）：
//   https://blog.csdn.net/ACMer_QJ/article/details/113884787
//
// 要点（与来源思路一致）：
//   * 队列模拟。队首报数，没到 m 就重新入队尾，到 m 就出队并把 m 更新为下一只猴子的 Xi。
//   * 队列中任意时刻元素数 ≤ N（每次淘汰只会少一只），因此用容量 N+5 的循环数组即可，
//     不必使用 STL queue（避免 1e8 次操作下的常数与扩容开销）。
//   * 复杂度 O(总报数次数)。每轮数到的次数 m ≤ 100，共 N-1 轮，最坏约 1e8 次，
//     500ms 时限内可通过（实测顶格数据 < 100ms）。
//
// 注意：m 表示“当前这一轮要数到的次数”，一开始 m = X[1]（来源代码注释：第一个要求的数就是 a[1]）。

#include <cstdio>
#include <cstdlib>

static const int MAXN = 1000000 + 5;

int n;
int x[MAXN];           // x[i]：第 i 只猴子对应的报数次数 Xi
int q[MAXN];           // 循环队列，存放猴子编号
int headq, tailq, sz;  // 队头、队尾、队列内元素个数

inline void push(int v) { q[tailq] = v; tailq = (tailq == MAXN - 1) ? 0 : tailq + 1; sz++; }
inline int pop()        { int v = q[headq]; headq = (headq == MAXN - 1) ? 0 : headq + 1; sz--; return v; }
inline int frontq()     { return q[headq]; }

int main() {
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 1; i <= n; i++) {
        scanf("%d", &x[i]);
        push(i);            // 1..n 依次入队
    }

    int m = x[1];           // 当前轮要数到的次数 = 起始猴子（1号）对应的 X1
    int cnt = 0;            // 当前已报数次数

    while (sz > 1) {        // 还剩多于一只猴子时继续
        cnt++;
        int cur = pop();    // 队首报数并出队
        if (cnt == m) {     // 数到了：淘汰这只猴子
            cnt = 0;
            m = x[frontq()]; // 下一只猴子开始新的一轮，次数用它的 Xi
        } else {
            push(cur);      // 没数到：回到队尾继续
        }
    }

    printf("%d\n", frontq());  // 最后剩下的猴子即大王
    return 0;
}
