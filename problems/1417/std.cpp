// std.cpp：最大利润(Maximum Profit) —— AOJ ALDS1_1_D
// 思路：只允许先买后卖（j > i），求 R[j] - R[i] 的最大值。
//   从左往右扫一遍，边扫边记录「到目前为止见过的最小价格」min_price，
//   那么以当前时刻卖出能获得的最大利润就是 R[i] - min_price，
//   用它对答案取最大值即可。每个元素只处理一次，O(n)。
// 注意：价格一路下跌时答案会是负数，所以初值要设得足够小。
#include <cstdio>

int main()
{
    int n;
    scanf("%d", &n);

    long long min_price;   // 到目前为止出现过的最小价格
    long long price;
    scanf("%lld", &price);
    min_price = price;

    long long ans = -2000000000LL; // 答案可能为负，初值要足够小
    for (int i = 1; i < n; i++) {
        scanf("%lld", &price);
        // 先算利润，再更新最小值，保证买入时刻严格早于卖出时刻
        long long profit = price - min_price;
        if (profit > ans)
            ans = profit;
        if (price < min_price)
            min_price = price;
    }

    printf("%lld\n", ans);
    return 0;
}
