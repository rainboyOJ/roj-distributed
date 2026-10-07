// 一本通 1994《音乐会》标程
// 题意：n 条区间标记（5 种乐器 P/V/C/D/B，左闭右闭时间区间），
//       m 次单点询问，输出该时刻所有演奏中的乐器（按 PVCDB 顺序，无则 None）。
// 做法：对每种乐器维护差分数组，区间 [l,r] 加 1；前缀和还原后 O(1) 回答单点询问。
//       hh:mm:ss 直接折成秒：t = h*3600 + m*60 + s。
// 数据范围：0<=hh<=9, 0<=mm<=59, 0<=ss<=59, 1<=n,m<=20000，
//           故最大秒为 9*3600+59*60+59 = 35999。
// 参考来源：
//   https://www.cnblogs.com/lyc-lb-blogs/p/14969873.html
//   https://blog.csdn.net/qq_69908563/article/details/127331535
#include <cstdio>
#include <cstring>

const int MAXT = 36000 + 5; // 秒 0..35999，差分需要 r+1 位

int diff[5][MAXT + 2];
int playing[5][MAXT];
const char* name = "PVCDB";

inline int to_sec(int h, int m, int s) {
    return h * 3600 + m * 60 + s;
}

inline int read_time() {
    int h, m, s;
    scanf("%d:%d:%d", &h, &m, &s);
    return to_sec(h, m, s);
}

int main() {
    int n, m;
    scanf("%d", &n);
    for (int i = 0; i < n; ++i) {
        int l = read_time();
        int r = read_time();
        char op[4];
        scanf("%s", op);
        int id;
        switch (op[0]) {
            case 'P': id = 0; break;
            case 'V': id = 1; break;
            case 'C': id = 2; break;
            case 'D': id = 3; break;
            case 'B': id = 4; break;
            default:  id = -1; break;
        }
        if (id < 0) continue;
        diff[id][l] += 1;
        diff[id][r + 1] -= 1;
    }

    // 前缀和还原每个时刻每种乐器的演奏状态
    for (int id = 0; id < 5; ++id) {
        int cur = 0;
        for (int t = 0; t < MAXT; ++t) {
            cur += diff[id][t];
            playing[id][t] = cur;
        }
    }

    scanf("%d", &m);
    for (int i = 0; i < m; ++i) {
        int t = read_time();
        bool any = false;
        for (int id = 0; id < 5; ++id) {
            if (playing[id][t] > 0) {
                any = true;
                putchar(name[id]);
            }
        }
        if (!any) printf("None");
        putchar('\n');
    }
    return 0;
}
