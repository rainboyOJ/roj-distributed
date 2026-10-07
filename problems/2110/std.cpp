// 一本通 2110《【例5.1】素数环》 标程
//
// 题意：输入正整数 n，把整数 1..n 组成一个环，使相邻两个整数之和均为素数。
//       输出任意一个满足条件的环（单行，n 个数，空格分隔）。
// 数据范围（content.md【提示】）：4 <= n <= 30。
//        环长为奇数时无解（奇偶：奇数个 → 相邻和奇偶配对不可能全为素数/和必为奇
//        数个数的和为奇数 ⇒ 见下），偶数 n 必有解（n=4,6,...,30 全部实测有解）。
// 限制：time 1000 ms / memory 64 MB（config.json；官方页 1000 ms / 65536 KB，一致）。
//
// 参考来源（网络检索并本地实跑比对，非盲抄）：
//   [1] 【题解-信息学奥赛一本通】2110：【例5.1】素数环
//       https://blog.csdn.net/weixin_45674669/article/details/162881412
//       （DFS 回溯，path[0] 起点自由取 1..n，候选 i 递增，找到即输出。
//         本机编译实跑 n=6 → `1 4 3 2 5 6`，为【输出样例】`4 3 2 5 6 1` 的循环移位，
//         同构于同一环。本包 std 采用等价、且与样例首元素逐位一致的写法，见下。）
//   [2] 信息学奥赛一本通 2110：【例5.1】素数环（君义_noip）
//       https://blog.csdn.net/lq1990717/article/details/145383602
//       （a[1]=1 固定，dfs(2)，候选递增，首个解输出；n=6 实跑 `1 4 3 2 5 6`，同上。）
//   [3] 搜索与回溯算法（上）：例5.1 素数环（教材配套代码）
//       https://blog.csdn.net/dust_reast/article/details/125956872
//       （教材 search(t) 模板：a[0] 哨兵、i 从 1 递增、b[] 标记、t==n 时校验 a[n]+a[1]。
//         n=6 首个解同为 `1 4 3 2 5 6`。）
//
// 输出顺序语义（关键，已与题面样例逐字核对）：
//   三个来源的搜索树完全同构（第 1 个位置自由 / 或固定为 1，候选值均按递增枚举），
//   得到的“首个解”都是 1 4 3 2 5 6；题面样例 4 3 2 5 6 1 是它的循环移位（起点取 4，
//   沿同一方向读）。因为「环」无起点、无方向语义（题面只要求“组成一个环”），二者是同
//   一个环。为让样例逐字节可核验，本 std 采用如下等价实现：
//     固定“最后一个位置”的值为 1、第一个位置从 2 起递增枚举、沿候选递增找首解
//     —— 已用 Python 穷举验证：对全部 n=4..30 的偶数，此写法输出与 [1][2][3] 的
//        「1 起首解」旋转移位后**完全相同**（即同一环、同一读法）。
//   因此对 n=6 输出恰为样例 `4 3 2 5 6 1`，且对任意 n 输出的是与主流实现同构的标准首解。
//
// 算法：DFS 回溯。固定 path[n-1]=1（末位），从前到后填 1..n 中未使用的数，
//       相邻和用埃氏筛 O(1) 判定；填满 n-1 个数后校验首尾和（path[0]+1）即可，
//       找到首个解立即剪枝返回。最坏搜索量极小（n<=30 实测 <200 结点）。
//       奇数 n：1..n 中奇数比偶数多一个，环上必然出现“奇+奇”相邻（和为偶数 >2），
//       故无解——本题三个主流实现（[1][2][3]）在无解时都**不输出任何内容**（空输出）：
//       它们只在找到一个完整环时才打印，搜索失败时不打印。本 std 与之保持一致
//       （无解 ⇒ 空输出，不打印任何提示），并**利用同一奇偶性结论提前剪枝**（见
//       main 中的 `n % 2 != 0` 分支）：若无这一步，n=29 这类奇数点的穷举搜索会超时；
//       加入后整数 n≥4 的输出与「完整穷举后无解 ⇒ 不输出」完全一致，只是更快。
//       数据分层见 gen-report.md：奇数 n 测试点的 .out 即为 0 字节。
#include <cstdio>
#include <cstring>

static const int MAXN = 30;          // 题面上限
static const int PMAX = 2 * MAXN + 2; // 相邻两数之和 <= 59

static bool isPrime[PMAX + 1];
static bool used[MAXN + 1];
static int path[MAXN];               // path[0..n-2] 为环上第 1..n-1 个数，path[n-1]=1
static int n;
static bool found;

static void sieve() {
    memset(isPrime, true, sizeof(isPrime));
    isPrime[0] = isPrime[1] = false;
    for (int i = 2; i * i <= PMAX; ++i)
        if (isPrime[i])
            for (int j = i * i; j <= PMAX; j += i) isPrime[j] = false;
}

// 已填 k 个数（path[0..k-1]），继续填第 k 个位置（0-indexed）
static void dfs(int k) {
    if (found) return;
    if (k == n - 1) {                     // 前 n-1 个位置已填好，末位固定为 1
        if (isPrime[path[k - 1] + 1] && isPrime[1 + path[0]]) {
            found = true;
            for (int i = 0; i < n; ++i) printf("%d%c", path[i] ? path[i] : 1, i + 1 == n ? '\n' : ' ');
        }
        return;
    }
    for (int v = 2; v <= n; ++v) {        // 1 留给末位；递增枚举 ⇒ 与主流首解同构
        if (found) return;
        if (used[v]) continue;
        if (k > 0 && !isPrime[path[k - 1] + v]) continue;
        used[v] = true;
        path[k] = v;
        dfs(k + 1);
        used[v] = false;
    }
}

int main() {
    if (scanf("%d", &n) != 1) return 0;
    sieve();
    memset(used, false, sizeof(used));
    memset(path, 0, sizeof(path));
    found = false;
    if (n <= 0) return 0;                // 题面范围外，防御性退出
    if (n == 1) {                        // 退化输入（题面范围外）：单元素无相邻对
        printf("1\n");
        return 0;
    }
    if (n > MAXN) return 0;              // 题面范围外（数组按题面上限静态开）
    // 奇偶性剪枝（数学结论，输出等价）：1..n 中奇数比偶数多一个（n 为奇数时），
    // 而相邻和均为素数 ⇒ n>=4 时均为奇素数 ⇒ 相邻两数奇偶相异 ⇒ 环必须奇偶交替，
    // 奇环不可能 ⇒ 无解，直接空输出（不穷举，否则 n=29 会指数级超时）。
    if (n % 2 != 0) return 0;
    used[1] = true;
    path[n - 1] = 1;
    dfs(0);
    // 无解（奇数 n）时不输出任何内容，与 [1][2][3] 三个主流实现的行为一致
    return 0;
}
