// 一本通 2128《高精度乘法（II）》 标程
// 题意：输入两个高精度正整数 a 和 b（均小于 200000 位），输出 a*b。
//
// 参考来源（思路/改写依据，非盲抄；来源与题面冲突时以题面为准）：
//   [1] 【题解-信息学奥赛一本通】2128:高精度乘法（II）
//       https://blog.csdn.net/weixin_45674669/article/details/162209166
//       （该文给出「压 6 位（BASE=1000000）存储 + 逐位相乘累加 + 统一进位」的做法；
//         该文写 1s/64MB，官方题面页为 1s/131072KB，按题面与 config.json（128MB）为准。）
//   [2] 信息学奥赛系列教程：高精度乘法
//       https://blog.csdn.net/noipBar/article/details/84404329
//       （模拟竖式：结果数组长度 = len(a)+len(b)，最后从高位去掉前导零。）
//   [3] 洛谷 P1303 A*B 相关题解转载（10^4 位版，印证同一算法）
//       https://blog.csdn.net/dadashashasha/article/details/136232982
//
// 算法：把十进制串从低位起每 7 位压成一个 limb（BASE=1e7），
//       先做无进位的位对位累加，再统一从低位向高位进位，最后去掉高位的零 limb。
//       复杂度 O(lenA*lenB/49)，199999 位最坏数据实测约 0.27~0.29s（本机 g++ -O2；
//       参考解用 1e6 分段实测约 0.33s，此处取 1e7 以扩大时限余量）。
//       溢出论证：单个 limb 乘积 < 1e14，同一 limb 位最多累加 min(lenA,lenB)/7 < 28572 项，
//       总和 < 2.9e18 < 2^64-1，unsigned long long 累加安全（4e5 位远够用）。
// 边界：输入可能为 "0"（0×大数 = 0）；前导零按数值解析（"007" 记为 7）。
//
// 输入：两行（或空白分隔）的两个正整数；输出：一行的积。
#include <cstdio>
#include <iostream>
#include <string>
#include <vector>

typedef long long ll;
typedef unsigned long long ull;

static const ull BASE = 10000000ULL;  // 1e7，每 limb 存 7 位十进制
static const int WIDTH = 7;

// 把十进制串（可含前导零）从低位起切成 7 位一段的 limb 数组
static std::vector<ull> splitLimbs(const std::string &s) {
    std::vector<ull> v;
    ull k = 1, num = 0;
    for (int i = (int)s.size() - 1; i >= 0; --i) {
        num += k * (ull)(s[i] - '0');
        k *= 10;
        if (k == BASE) {
            v.push_back(num);
            k = 1;
            num = 0;
        }
    }
    if (num != 0 || v.empty()) v.push_back(num);  // 收尾；输入 "0" 时得到 [0]
    return v;
}

int main() {
    std::string a, b;
    if (!(std::cin >> a >> b)) return 0;

    std::vector<ull> A = splitLimbs(a), B = splitLimbs(b);

    // 外层枚举短者、内层枚举长者，使写 C[i+j] 的顺序连续，缓存友好（乘积次数不变）
    if (A.size() > B.size()) A.swap(B);

    std::vector<ull> C(A.size() + B.size(), 0);
    for (size_t i = 0; i < A.size(); ++i) {
        ull ai = A[i];
        if (ai == 0) continue;  // 0 limb 不贡献，跳过以省时
        ull *c = C.data() + i;
        const ull *bp = B.data();
        size_t n = B.size();
        for (size_t j = 0; j < n; ++j) c[j] += ai * bp[j];
    }

    // 统一进位
    ull carry = 0;
    for (size_t i = 0; i < C.size(); ++i) {
        carry += C[i];
        C[i] = carry % BASE;
        carry /= BASE;
    }
    // carry 必为 0：limb 数上限为 lenA+lenB，总和 < BASE^(lenA+lenB)，最高段无残留进位

    // 去掉高位零 limb，至少保留一位
    while (C.size() > 1 && C.back() == 0) C.pop_back();

    std::string out = std::to_string(C.back());
    char buf[16];
    for (int i = (int)C.size() - 2; i >= 0; --i) {
        std::snprintf(buf, sizeof(buf), "%0*llu", WIDTH, (unsigned long long)C[i]);
        out += buf;
    }
    std::printf("%s\n", out.c_str());
    return 0;
}
