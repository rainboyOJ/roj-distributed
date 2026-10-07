// 一本通 2051《【例3.1】偶数》—— 标程（C++17，stdin -> stdout）
//
// 题意：读入一个正整数 a，若 a 为偶数输出 yes，否则什么也不输出。
//
// 参考来源（本包 worker 于本轮联网逐篇抓取原文核对，均为同一解法：
//   「读入整数 a；a % 2 == 0 时输出 yes，否则不输出任何内容」）：
//   [1] https://blog.csdn.net/ffsdfg/article/details/127190524
//       《信息学奥赛一本通：2051：【例3.1】偶数》
//         int a; scanf("%d",&a); if(a%2==0) printf("yes");
//   [2] https://blog.csdn.net/zzzxwcx/article/details/129183687
//       《信息学奥赛一本通 2051：【例3.1】偶数》
//         int n; cin>>n; if(n%2==0){ cout<<"yes"; return 0; }
//   [3] https://blog.csdn.net/lvcheng0309/article/details/117677089
//       《信息学奥赛一本通（2051：【例3.1】偶数）》
//         int a; scanf("%d",&a); if(a%2==0) printf("yes\n");
//   [4] https://blog.csdn.net/bbbb8989/article/details/127595586
//       《一本通2051；偶数》
//         int a; scanf("%d",&a); if(a%2==0) printf("yes\n");
//   [5] https://www.cnblogs.com/hgtudhfj/articles/17840258.html
//       《2051：【例3.1】偶数》koqwji（博客园）
//         long long a; cin>>a; if(a%2==0 && a>=0) cout<<"yes";
//   [6] https://blog.csdn.net/Flower_vegetable/article/details/119083397
//       《信息学奥赛一本通-2051：【例3.1】偶数》
//         int a; scanf("%d",&a); if(a%2==0) printf("yes");
//   [7] https://blog.csdn.net/lixuean0408/article/details/140231245
//       《信息学奥赛一本通第2051题》
//         scanf("%d",&a); if((a%2)==0){ printf("yes"); }
//   [8] https://blog.csdn.net/earthzhang2021/article/details/154361405
//       《【2051】【例3.1】偶数》
//         if (a % 2 == 0) { printf("yes\n"); }
//   官方题面（本轮实测可访问，用于核对样例与限制）：
//       http://ybt.ssoier.cn:8088/problem_show.php?pid=2051
//       （时间限制 1000 ms，内存限制 65536 KB，样例 12 -> yes）
//
// 多来源结论一致，无冲突；以题面为准：偶数打印 yes，奇数什么都不输出
// （注意：不是打印 no，也不是打印空行——奇数时输出必须是 0 字节）。
//
// 本实现为本包改写（scanf/printf 风格，参考 problems/1000/std.cpp）：
//   - 用 long long 读入，是全部 int 版网络题解的超集（自定数据范围见 data.py），
//     避免自定上界附近任何溢出歧义；
//   - 输出 yes 后跟一个换行符 \n（题面【输出样例】中 yes 独占一行；语料惯例
//     输出行以 \n 结尾，见 problems/5006、.ybt-import/staging/2066）；
//   - 奇数分支不输出任何字节，符合「什么也不输出」；
//   - 不使用浮点，不存在 -0.00 / 定宽格式类风险。

#include <cstdio>

int main() {
    long long a;
    if (scanf("%lld", &a) != 1) return 0;  // 无输入时静默退出
    if (a % 2 == 0) {
        printf("yes\n");
    }
    return 0;
}
