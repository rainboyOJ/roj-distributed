// 一本通 2035《【例5.2】平移数据》标程（stdin -> stdout，C++17）
//
// 参考来源（2025 本轮实测抓取正文/代码块，非盲抄搜索摘要）：
//   [1] 官方题面（语义/样例/限制核对）
//       http://ybt.ssoier.cn:8088/problem_show.php?pid=2035
//       时间限制 1000 ms、内存限制 65536 KB（与 config.json 的 time=1000/memory=64 一致）；
//       正文（JS pshow 原文）与 content.md 逐字一致：
//       「将$a$数组中第一个元素移到数组末尾,其余数据依次往前平移一个位置。」
//       「第一行为数组$a$的元素个数(数组元素个数小于$50$)；第二行为$n$个小于$1000$的正整数。」
//       「平移后的数组元素，每个数用一个空格隔开。」样例 10 / 1..10 -> 2 3 4 5 6 7 8 9 10 1
//   [2] CSDN · 君义_noip《信息学奥赛一本通 2035：【例5.2】平移数据》
//       https://blog.csdn.net/lq1990717/article/details/121545043
//       给出三种解法：解法1「temp=a[1]; for(i=2..n) a[i-1]=a[i]; a[n]=temp;」（真正改变数组）；
//       解法2「输入时错位」；解法3「不改变数组：for(i=2..n) cout<<a[i]<<' '; cout<<a[1];」
//   [3] CSDN · qq_40802813《【信奥赛一本通】2035：【例5.2】平移数据（详细代码）》
//       https://blog.csdn.net/qq_40802813/article/details/119887713
//       b=a[0]; for(i=0;i<n;i++) a[i]=a[i+1]; a[n-1]=b;（0 基下方左移一位、首元素置尾）
//   [4] CSDN · 墨衍《信奥赛一本通 C++题解 2035【例5.2】平移数据》
//       https://blog.csdn.net/xiang20100794/article/details/123458363
//       N=1010；cin>>n; 读 a[0..n-1]; t=a[0]; for(i=0;i<n-1;i++) a[i]=a[i+1]; a[n-1]=t;
//   [5] CSDN · wzq_wzq123《信息学奥赛一本通C++语言-----2035：【例5.2】平移数据》
//       https://blog.csdn.net/wzq_wzq123/article/details/122925725
//       C 风格：scanf("%d",&n); tmp=a[0]; 左移；a[n-1]=tmp; printf("%d ",a[i]);
//   [6] CSDN · strawberrytreea《信息学奥赛一本通（c++）：2035：【例5.2】平移数据》
//       https://blog.csdn.net/strawberrytreea/article/details/124361423
//       思路「定义一个中间变量 t 等于第一个数，然后数组依次向前挪一位，最后一位等于 t」
//   [7] CSDN · 2402_84298973《平移数据（信息学奥赛一本通-2035）》
//       https://blog.csdn.net/2402_84298973/article/details/146230312
//       1 基：h=nums[1]; for(i=2..n) nums[i-1]=nums[i]; nums[n]=h;（含题面「数组元素个数小于50」）
//   [8] CSDN · meterochan《2035：【例5.2】平移数据 ------ 信息学奥赛高级题库》
//       https://blog.csdn.net/meterochan/article/details/136284211
//       复述题面与限制（1000 ms / 65536 KB）并对齐数组指针用法
//   [9] CSDN · m0_73220913《信息学奥赛一本通答案dj平移数据2035》
//       https://blog.csdn.net/m0_73220913/article/details/129387116
//       与 [7] 相同的 1 基左移写法（a[i-1]=a[i]; a[n]=t）
//
// 来源结论核对：九个来源的算法**完全一致**（左旋一位：保存 a[已取首元素]，其余元素整体前移一格，
// 首元素写到末位），差异仅在（a）0 基/1 基下标；（b）是否真正改变数组（[2] 解法3 只改输出顺序）；
// （c）行末是否多一个空格（[2][4][5][6][7][9] 是「每元素后跟一个空格」，行末多一个）。
// 题面「每个数用一个空格隔开」严格解读支持**无行末空格**；仓库评测器用 diff -b 忽略行尾空白，
// 两种口径均通过。本标程取严格写法。**无来源冲突，题面无歧义，未触发「停下报告」。**
//
// 本题相对来源的改写点：
//   1. 数组容量 105（题面 n<50 留一倍余量），并在读入循环里以 `i < n && i < MAXN` 防御越界（题面
//      保证不触发，仅避免 UB），对齐 problems/1000/std.cpp 的 C 风格 scanf/printf 输入输出；
//   2. 左移循环写成 `for (i = 1; i < n; ++i) a[i-1] = a[i];`（对齐 [2] 解法1 / [3] / [4] 的 0 基
//      语义），最后 `a[n-1] = t` 把首元素放到末位；
//   3. 输出用「先判断再输出」保证元素间**单个空格、行末无多余空格**，末尾补一个 '\n'；
//   4. n<=0 或读不到 n 时安全退出（输出 0 字节），与题面 n>=1 不冲突，属防御性处理；
//   5. 数值范围按题面「小于 1000 的正整数」（1..999）设计，int 足够，无溢出风险。
//
// 编译：g++ -O2 -std=c++17 -Wall -Wextra std.cpp -o std
// 用法：./std < problem1.in

#include <cstdio>

int main() {
    const int MAXN = 105;  // 题面 n<50，留余量防越界
    int a[MAXN];
    int n;

    if (scanf("%d", &n) != 1) return 0;  // 空输入：安全退出
    if (n <= 0) return 0;                // 题面保证 n>=1，防御性处理

    int m = (n < MAXN) ? n : MAXN;       // 题面保证 n<MAXN，此处仅为健壮性
    for (int i = 0; i < m; ++i) {
        if (scanf("%d", &a[i]) != 1) return 0;  // 输入不完整：安全退出
    }

    // 左旋一位：首元素暂存，其余依次前移，首元素写到末位
    int t = a[0];
    for (int i = 1; i < m; ++i) a[i - 1] = a[i];
    a[m - 1] = t;

    // 输出：元素之间单个空格，行末无多余空格
    for (int i = 0; i < m; ++i) {
        if (i) putchar(' ');
        printf("%d", a[i]);
    }
    putchar('\n');
    return 0;
}
