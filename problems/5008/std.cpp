// 1672 游戏通关 —— 标准程序
// 算法：贪心（按奖励 W 从大到小依次决策）+ 并查集维护"每个时限下最晚的空闲时间槽"。
//   每个任务耗时 1 个单位时间，任务 i 必须在时刻 T_i 前完成，即占用槽 1..T_i 中的一个。
//   按 W 降序考虑任务：用并查集 find(T) 找到 <= T 的最大未占用槽位并占用之；
//   若 find(T)==0 说明该时限内已无空槽，放弃该任务。经典"任务调度+并查集"贪心，最优性可交换证明。
// 参考来源（网络题解，思路改写、代码重新实现并经样例/对拍验证）：
//   1. https://blog.csdn.net/qq_43857314/article/details/110391219
//      《【信息学奥赛一本通——高手训练】游戏通关 | 贪心、并查集》（贪心按奖励降序 + 并查集占槽）
//   2. https://blog.csdn.net/qq_36230375/article/details/136382077
//      《信息学奥赛一本通高手训练 1672：游戏通关 贪心算法》（按期限排序 + 大根堆的等价做法）
#include <cstdio>
#include <algorithm>
using namespace std;

const int MAXT = 200000; // 题面 T_i <= 200000

struct Task {
    int t, w;
};

bool cmp_w_desc(const Task &x, const Task &y) {
    return x.w > y.w;
}

Task a[200005];
int fa[MAXT + 5];

// 返回 <= x 的最大未占用槽位；0 表示无可用槽
int find(int x) {
    if (x <= 0)
        return 0;
    return fa[x] == x ? x : (fa[x] = find(fa[x]));
}

int main() {
    int n;
    scanf("%d", &n);
    for (int i = 0; i < n; i++)
        scanf("%d %d", &a[i].t, &a[i].w);
    for (int i = 0; i <= MAXT; i++)
        fa[i] = i;
    sort(a, a + n, cmp_w_desc);
    long long ans = 0;
    for (int i = 0; i < n; i++) {
        int t = a[i].t > MAXT ? MAXT : a[i].t;
        int s = find(t);
        if (s == 0) // 无空闲槽，跳过该任务
            continue;
        ans += a[i].w;
        fa[s] = find(s - 1); // 占用槽 s
    }
    printf("%lld\n", ans);
    return 0;
}
