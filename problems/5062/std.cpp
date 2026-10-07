// 一本通 2061 【例1.2】梯形面积
//
// 参考来源（网络题解，已按题面核对后改写，非盲抄）：
//   https://blog.csdn.net/qiaoweichen/article/details/119361023
//   https://blog.csdn.net/alexwang211/article/details/145233813
//   https://blog.csdn.net/m0_74116287/article/details/127195003
//   https://blog.csdn.net/dongchenlzm/article/details/133825719
//   https://blog.csdn.net/qq_29887971/article/details/127182463
//
// 思路：题图中梯形上底 a = 15、下底 b = 25（单位：cm）。
//   阴影部分是以 a 为底、顶点在下底右端点的三角形，其高等于梯形的高 h：
//       (1/2) * a * h = 150  =>  h = 2 * 150 / 15 = 20
//   梯形面积：
//       S = (a + b) * h / 2 = (15 + 25) * 20 / 2 = 400
//   按题面要求保留两位小数输出 400.00。
//
// 题面【输入】为（无），本程序不读取任何输入。
#include <cstdio>

int main() {
    const double a = 15.0;      // 上底
    const double b = 25.0;      // 下底
    const double shaded = 150.0; // 阴影三角形面积

    double h = 2.0 * shaded / a;   // 梯形的高
    double s = (a + b) * h / 2.0;  // 梯形面积

    printf("%.2f\n", s);
    return 0;
}
