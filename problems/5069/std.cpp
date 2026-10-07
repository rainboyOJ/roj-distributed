// 一本通 2068《【例2.6】鸡兔同笼》标程
//
// 参考来源（网络 C++ 题解，已联网核对、本机编译验证后改写）：
//   1. https://blog.csdn.net/lq1990717/article/details/119998291
//      《信息学奥赛一本通 2068：【例2.6】鸡兔同笼》
//      参考代码：printf("%d %d", (4*x-y)/2, (y-2*x)/2);
//   2. https://blog.csdn.net/zjx120307/article/details/126166824
//      《信息学奥赛一本通——2068：【例2.6】鸡兔同笼》
//      参考代码：ra=(y-2*x)/2; ch=x-ra;
//
// 两来源结论一致（互为等价变形）：设鸡 c 只、兔 r 只，
//   c + r = x, 2c + 4r = y  =>  r = (y-2x)/2, c = x-r = (4x-y)/2。
// 以题面样例验证：x=30, y=90 -> c=15, r=15，与【输出样例】一致。
#include <cstdio>

long long x, y;

int main() {
    scanf("%lld %lld", &x, &y);
    long long r = (y - 2 * x) / 2; // 兔
    long long c = x - r;           // 鸡 = (4*x - y) / 2
    printf("%lld %lld\n", c, r);
    return 0;
}
