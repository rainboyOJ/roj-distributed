#include <cstdio>

int main(){
    int a, b, c;
    scanf("%d %d %d", &a, &b, &c);
    // 总成绩 = A*20% + B*30% + C*50%
    // A、B、C 均为 10 的整数倍，故 (2A + 3B + 5C)/10 恒为整数
    printf("%d\n", (a * 2 + b * 3 + c * 5) / 10);
    return 0;
}
