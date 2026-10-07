// 一本通 2064 【例2.1】交换值
//
// 参考来源（网络题解，已按题面核对后改写，非盲抄）：
//   https://blog.csdn.net/setprecisiona/article/details/128166845
//     （赋值法 / 数学法 / swap(a,b) / 直接用 b a 输出 四种写法，均 AC）
//   https://blog.csdn.net/qq_36455276/article/details/128684977
//     （临时变量 t=a; a=b; b=t; 的标准写法）
//   https://blog.csdn.net/lq1990717/article/details/119843312
//     （临时变量 / 自定义 Swap / 加减数学法 / swap() / 直接输出 多种写法）
//   https://blog.csdn.net/qq_59918355/article/details/121382032
//     （C 语言临时变量写法，printf("%d %d", a, b)）
//   https://blog.csdn.net/weixin_62460981/article/details/122654947
//     （swap(a,b) 写法，交叉印证）
//   官方题面（核对输入输出格式与 1000ms/65536KB 限制）：
//   http://ybt.ssoier.cn:8088/problem_show.php?pid=2064
//
// 思路：读入两个正整数 a、b，借临时变量 t 交换二者的值（使 a 等于原 b、
//   b 等于原 a），再按题面要求输出交换后的 a b。样例：输入 2 3，输出 3 2。
//   题面（及官方 OJ 页）未声明 a、b 的取值范围，故用 64 位 long long 读写，
//   兼容 int 范围及以上（至 ±9.2e18）的输入，避免溢出。
#include <cstdio>

int main() {
    long long a, b;
    if (scanf("%lld %lld", &a, &b) != 2) return 0;

    long long t = a;  // 借助临时变量完成交换
    a = b;
    b = t;

    printf("%lld %lld\n", a, b);
    return 0;
}
