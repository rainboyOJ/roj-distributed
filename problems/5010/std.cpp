// 一本通 1674《堆蛋糕》标程
// 参考来源（思路：贪心 + 出现次数桶 + 三个单调下降指针）：
//   https://blog.csdn.net/qq_43857314/article/details/110501479
//   【信息学奥赛一本通——高手训练】堆蛋糕 | 贪心、三指针（作者：一只酷酷光儿 CoolGuang）
// 本文件为独立改写实现（自定快读、数组布局、循环结构），并在小数据上与
// 暴力搜索 / 朴素堆贪心 / 数学枚举三种独立实现做了上万组对拍验证。
//
// 题意：n 个圆柱蛋糕，半径 R_i（高度相同），每三层按半径从上往下严格递增堆成
//       一个“好蛋糕”，求最多能堆出多少个三层蛋糕。
// 数据范围：n ≤ 3e6，R_i ≤ n（题面明确保证）。
//
// 算法：设 cnt[r] 为半径 r 的蛋糕个数，b[k] 为出现次数恰好为 k 的不同半径种数。
//       贪心：每个好蛋糕从当前剩余数量最多的三种半径中各取一个（每次各减 1），
//       这等价于每次取计数多重集的前三大各减一，可证明与最优解一致
//       （交换论证：任一最优方案可调整成每轮取前三大，不减少总数；
//       另由 Hall 型条件 ans=T 可行 iff sum_r min(cnt_r,T) >= 3T 且 T 轮内
//       每轮三种不同半径可取，二者给出相同的最大 T）。
//       实现上用三个从大到小游动的指针 x >= y >= z 在 b[] 上各完成一次取数
//       （b[x]-- 等），一轮取完后再把 x-1 / y-1 / z-1 回填（延后回填保证
//       同一轮不会重复取同一种半径），ans++。
//       任一指针无法取到（落到 0）即无法再组成三个不同的半径，结束。
// 复杂度：O(n)（读入 O(n)，指针单调不回升，总移动 O(n)）。
// 内存：cnt/bucket 两个 int[3e6] + 边读边计数，约 24MB，远小于 256MB 限制。

#include <cstdio>

typedef long long ll;

const int MAXV = 3000006;   // R_i <= n <= 3e6（题面保证），留少量余量

static int cnt[MAXV];         // cnt[r]: 半径为 r 的蛋糕个数
static int bucket[MAXV + 8];  // bucket[k]: 出现次数恰为 k 的半径种数

/* 快读：非负整数（EOF 安全） */
static inline int readInt() {
    int c = getchar_unlocked();
    while (c != '-' && (c < '0' || c > '9')) {
        if (c == -1) return 0;
        c = getchar_unlocked();
    }
    int sgn = 1;
    if (c == '-') { sgn = -1; c = getchar_unlocked(); }
    int x = 0;
    while (c >= '0' && c <= '9') {
        x = x * 10 + (c - '0');
        c = getchar_unlocked();
    }
    return x * sgn;
}

int main() {
    int n = readInt();
    int mxR = 0;
    for (int i = 0; i < n; ++i) {
        int r = readInt();
        ++cnt[r];
        if (r > mxR) mxR = r;
    }
    int lim = n > mxR ? n : mxR;   // 题面保证 R_i <= n；取 max 以防数据轻微越界
    int mx = 0;
    for (int r = 1; r <= lim; ++r) {
        if (cnt[r]) {
            ++bucket[cnt[r]];
            if (cnt[r] > mx) mx = cnt[r];
        }
    }
    /* 三个指针 x >= y >= z，各在 bucket 上取一个非空桶（即取一种半径） */
    int x = mx, y = mx, z = mx;
    ll ans = 0;
    while (x > 0 && y > 0 && z > 0) {
        while (x > 0 && bucket[x] == 0) --x;
        if (x == 0) break;
        --bucket[x];
        while (y > 0 && bucket[y] == 0) --y;
        if (y == 0) break;
        --bucket[y];
        while (z > 0 && bucket[z] == 0) --z;
        if (z == 0) break;
        --bucket[z];
        /* 三种半径各取走一个蛋糕：次数 -1（延后回填；减到 0 则消失） */
        if (x > 1) ++bucket[x - 1];
        if (y > 1) ++bucket[y - 1];
        if (z > 1) ++bucket[z - 1];
        ++ans;
    }
    printf("%lld\n", ans);
    return 0;
}
