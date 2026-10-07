// 一本通 2048《【例5.18】串排序》标程
// 题意：读入 n (1<=n<=20) 个国家名（每个名字长度不超过 20），按字母顺序升序输出。
// 做法：std::string 读入，std::sort 按字典序（逐字符 ASCII 比较）排序后逐行输出。
//   网络上的 AC 题解用 strcmp + 冒泡/选择排序或 std::sort，比较规则一致
//   （逐字符 ASCII，即 "字典序"），本标程与题面样例一致。
// 参考来源（网络题解，已按题面自行改写并编译验证，非盲抄）：
//   1) https://blog.csdn.net/2402_84298973/article/details/146282718
//      《串排序（信息学奥赛一本通-2048）》：直接 sort(str+1, str+1+n) 后输出；
//   2) https://blog.csdn.net/qq_40790042/article/details/120063471
//      《一本通：2048：【例5.18】串排序》：冒泡排序 + strcmp 比较；
//   3) https://blog.csdn.net/wzq_wzq123/article/details/124522507
//      《信息学奥赛一本通C++语言-----2048：【例5.18】串排序》：选择排序 + strcmp 比较。
//   三个来源算法结论一致，与题面一致，无冲突。
#include <algorithm>
#include <iostream>
#include <string>

int main() {
    int n;
    std::cin >> n;
    std::string name[25];  // n <= 20
    for (int i = 0; i < n; ++i)
        std::cin >> name[i];
    std::sort(name, name + n);
    for (int i = 0; i < n; ++i)
        std::cout << name[i] << '\n';
    return 0;
}
