// 一本通 2127《【例1.2】高精度加法》 标程（C++17, stdin -> stdout）
//
// 参考来源 URL（思路与原参考实现，已按本题题面改写）：
//   https://www.cnblogs.com/ECJTUACM-873284962/p/6509887.html
//     《信息学奥赛一本通算法（C++版）基础算法：高精度计算》 — Angel_Kitty（2017-03-06）
//     同文镜像（同一份代码）：https://developer.aliyun.com/article/333680
//   参考代码要点：把数串倒序存入整型数组 -> 逐位相加并传递进位 -> 跳过最高位的 0 -> 倒序输出。
//
// 题面（以本题面为准）：输入两行，每行是一个不超过 100 位的非负整数，输出两数之和。
// 由此推出的关键语义（与参考代码相比的差异/加固）：
//   1) 和最多 101 位（100 位全 9 + 100 位全 9 或 100 位全 9 + 1 会产生最高位进位），
//      故数组/缓冲必须能容纳 101+ 位；参考代码用固定 100 长度数组在顶格进位上会越界。
//   2) 输入是非负整数，允许出现 0；结果为 0 时必须输出单个 `0`，不能输出空行。
//   3) 输出不能有前导零；为稳健起见，对输入中的前导零（黑盒数据若出现）做规范化处理。
//
// 算法：O(len) 按位模拟竖式加法（低位对齐，逐位相加 + 进位），下标从低位往高位处理。
#include <algorithm>
#include <cstdio>
#include <string>
#include <vector>

int main() {
    // 缓冲预留到 100000 位，远超题面 100 位上限（多余容量仅为稳健性，不影响语义）
    const int LIMIT = 100000;
    std::vector<char> buf(LIMIT + 1, 0);

    // 读入两个非空 token（题面为两行；按 token 读入可容忍行尾 \r 与多余空白）
    if (scanf("%100000s", buf.data()) != 1) return 0;
    std::string A(buf.data());
    if (scanf("%100000s", buf.data()) != 1) return 0;
    std::string B(buf.data());

    // 去前导零并规范化：全零 -> "0"
    auto norm = [](const std::string &s) -> std::string {
        size_t p = s.find_first_not_of('0');
        if (p == std::string::npos) return std::string("0");
        return s.substr(p);
    };
    A = norm(A);
    B = norm(B);

    // 倒序存入数字数组（最低位在 index 0）
    std::vector<int> a(A.size()), b(B.size());
    for (size_t i = 0; i < A.size(); ++i) a[i] = A[A.size() - 1 - i] - '0';
    for (size_t i = 0; i < B.size(); ++i) b[i] = B[B.size() - 1 - i] - '0';

    size_t n = std::max(a.size(), b.size());
    std::vector<int> c;
    c.reserve(n + 1);
    int carry = 0;  // 进位，最后一位可能仍为 1（最高位进位）
    for (size_t i = 0; i < n || carry; ++i) {
        int s = carry;
        if (i < a.size()) s += a[i];
        if (i < b.size()) s += b[i];
        c.push_back(s % 10);
        carry = s / 10;
    }

    // 倒序输出（天然无前导零；c 非空，最小情形输出 "0"）
    std::string out;
    out.reserve(c.size());
    for (size_t i = c.size(); i-- > 0;) out += char('0' + c[i]);
    fputs(out.c_str(), stdout);
    fputc('\n', stdout);
    return 0;
}
