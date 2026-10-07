// 一本通 2059《【例3.11】买笔》— 标程（C++17，stdin -> stdout）
//
// 参考来源（网络题解，均已逐条联网核对原文后改写，非盲抄）：
//   [1] CSDN · Cs_erle《信息学奥赛一本通 2059：【例3.11】买笔》（if/else 链写法）
//       https://blog.csdn.net/cs_erle/article/details/123120659
//   [2] CSDN · mydream8《信息学奥赛一本通（2059：【例3.11】买笔）》（switch 写法）
//       https://blog.csdn.net/mydream8/article/details/121916358
//   [3] CSDN · lq1990717《信息学奥赛一本通 2059：【例3.11】买笔》
//       （明言原题条件欠缺，补假设「剩余班费 x>0；笔数确定时尽量多买更贵的笔」）
//       https://blog.csdn.net/lq1990717/article/details/120771010
//   [4] CSDN · flower_vegetable（d = x%4 的三分支写法）
//       https://blog.csdn.net/flower_vegetable/article/details/119425462
//   [5] CSDN · weixin_62460981（switch 写法）
//       https://blog.csdn.net/weixin_62460981/article/details/124243751
//   [6] CSDN · lixuean0408（x %= 4 后的 switch 写法）
//       https://blog.csdn.net/lixuean0408/article/details/140557950
//   官方题面（核对输入输出格式与 1000 ms / 65536 KB 限制）：
//       http://ybt.ssoier.cn:8088/problem_show.php?pid=2059
//
// 题意：x 元全部花掉买单价 4/5/6 元的笔，要求笔数尽量多且无剩余钱，
//       按「6 元笔数、5 元笔数、4 元笔数」的顺序输出，空格隔开。
//
// 思路（六个来源结论一致，与题面样例 10 -> 1 0 1 相符）：
//   要笔数最多就尽可能买最便宜的 4 元笔，先取 k = x / 4 支，令 r = x % 4：
//     r = 0：不动                    -> (n6, n5, n4) = (0, 0, k)
//     r = 1：1 支 4 元换成 1 支 5 元  -> (0, 1, k-1)，笔数仍为 k
//     r = 2：1 支 4 元换成 1 支 6 元  -> (1, 0, k-1)，笔数仍为 k
//            （同笔数还可用 2 支 5 元凑；样例 10 -> 1 0 1 裁定「同笔数优先买贵的」，
//              来源 [3] 的补充假设与此一致）
//     r = 3：2 支 4 元换成 1 支 5 元 + 1 支 6 元 -> (1, 1, k-2)，笔数仍为 k
//
// 注 1：来源 [3] 写作 if (x > 4) 才计算，会把 x = 4 误判成「不买笔」（4 元恰好可买
//       1 支 4 元笔）；本标程改为 x >= 4，修正该边界。
// 注 2：x ∈ {1,2,3,7} 时 4/5/6 元三种笔无法恰好凑出 x 元（7 = 4a+5b+6c 无解），
//       题面未定义此时的输出；本包测试数据刻意不含这些值（见 gen-report.md 风险点），
//       标程对其兜底输出 "0 0 0" 仅为避免负数/未定义行为，并非题面语义。
//
// 复杂度 O(1)，输入范围 4 <= x <= 10^6（本包自定工作范围，见 gen-report.md）时
// 计数最大 250000，用 long long 冗余安全。
#include <cstdio>

int main() {
    long long x;
    if (scanf("%lld", &x) != 1) return 0;

    long long n6 = 0, n5 = 0, n4 = 0;  // 6 元、5 元、4 元笔的数目
    if (x >= 4 && x != 7) {
        long long k = x / 4;  // 笔数上限（每支最低 4 元）
        switch (x % 4) {
            case 0:
                n4 = k;
                break;
            case 1:
                n5 = 1;
                n4 = k - 1;
                break;
            case 2:
                n6 = 1;
                n4 = k - 1;
                break;
            case 3:
                n6 = 1;
                n5 = 1;
                n4 = k - 2;
                break;
        }
    }

    printf("%lld %lld %lld\n", n6, n5, n4);
    return 0;
}
