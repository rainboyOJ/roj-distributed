// 一本通 1738《圆桌聚会》标程（C++17）
// 自研构造（欧拉回路线图归约，对应题解目录「第7章 欧拉回路」）：
//   座位圈 x_0..x_{2n-1} 需满足 x_{i+1} ∈ {2x_i, 2x_i+1} mod 2n。
//   构造多重图 H：顶点 Z_n，弧 a_y（y=0..2n-1）：尾 ⌊y/2⌋ → 头 y mod n。
//   每顶点入度=出度=2，存在欧拉回路；且 x→y 相邻 ⟺ a_x 的头 = a_y 的尾。
//   故 H 的欧拉回路的弧标号序列即合法座位圈（线图 Hamilton 圈 ⟺ 原图欧拉回路）。
//   Hierholzer 迭代实现 O(n) 防爆栈；快速输出。
#include <cstdio>
#include <vector>
using namespace std;

static char outbuf[1 << 23];
static int outpos = 0;

inline void writeInt(long long x) {
    if (outpos > (1 << 23) - 32) { fwrite(outbuf, 1, outpos, stdout); outpos = 0; }
    char tmp[20];
    int len = 0;
    if (x == 0) tmp[len++] = '0';
    while (x > 0) { tmp[len++] = char('0' + x % 10); x /= 10; }
    while (len--) outbuf[outpos++] = tmp[len];
}

int main() {
    static char line[64];
    while (fgets(line, sizeof(line), stdin)) {
        long long n = 0;
        {
            char *p = line;
            while (*p && (*p < '0' || *p > '9')) p++;
            while (*p >= '0' && *p <= '9') { n = n * 10 + (*p - '0'); p++; }
        }
        if (n <= 0) continue;

        static vector<char> nxt;   // 每顶点已用出弧数（0..2）
        nxt.assign((size_t)n, 0);
        static vector<long long> inc;   // 栈：进入当前顶点的弧号（起点为 -1）
        static vector<long long> path;  // 弹出的弧号（逆访问序）
        inc.clear(); path.clear();
        inc.reserve(2 * n + 4); path.reserve(2 * n + 4);

        inc.push_back(-1);   // (起点顶点 0 的入弧 = -1)
        while (!inc.empty()) {
            long long a = inc.back();
            int v = (a == -1) ? 0 : (int)(a % n);
            if (nxt[v] < 2) {
                long long y = 2LL * v + nxt[v];
                nxt[v]++;
                inc.push_back(y);
            } else {
                path.push_back(a);
                inc.pop_back();
            }
        }
        // path 为逆访问序（含开头的 -1），反转去掉 -1 即为欧拉回路弧序列
        long long firstFlag = 1;
        for (long long i = (long long)path.size() - 1; i >= 0; i--) {
            if (path[i] == -1) continue;
            if (!firstFlag) outbuf[outpos++] = ' ';
            firstFlag = 0;
            writeInt(path[i]);
        }
        outbuf[outpos++] = '\n';
    }
    if (outpos) fwrite(outbuf, 1, outpos, stdout);
    return 0;
}
