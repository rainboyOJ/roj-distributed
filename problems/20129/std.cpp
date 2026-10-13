#include <bits/stdc++.h>
using namespace std;
namespace INPUT_SPACE {
const int S = (1 << 20) + 5;
char B[S], *H, *T;
inline int gc() {
if (H == T)
T = (H = B) + fread(B, 1, S, stdin);
return (H == T) ? EOF : *H++;
}
inline unsigned int inn() {
unsigned int x, ch;
while ((ch = gc()) < '0' || ch > '9')
;
x = ch^'0';
while ((ch = gc()) >= '0' && ch <= '9')
x = x * 10 + (ch^'0');
return x;
}
} using INPUT_SPACE::inn;
constexpr int N0{3007}, P(1e9 + 7);
constexpr int UP{0}, RIGHT{1}, DOWN{2}, LEFT{3};
constexpr int dx[4] = {-1, 0, 1, 0}, dy[4] = {0, 1, 0, -1};
// 上 右 下 左
struct E {
int to, r;
int ad;
// E(int to,int r,int ad):to{to},r{r},ad{ad}{}
// E():E(0,0,0){}
};
struct Node {
// 原矩阵逆时针旋转时，lz 需要顺时针旋转（画图理解）
E
e[4];
// inline void init(){e[0]=e[1]=e[2]=e[3]=E();}
} lis[N0 * N0];
struct Info {
int i, r;
int s;
Info(int i, int r, int s): i{i}, r{r}, s{s} {}
// Info():Info(0,0,0){}
};
int n, q, nc, id[N0][N0], begr[N0], endr[N0], begc[N0], endc[N0];
int val[N0][N0];
inline void add(int &a, int b) {
if ((a += b) >= P)

a -= P;
}
inline bool inm(int x, int y) {
return x >= 0 && x <= n + 1 && y >= 0 && y <= n + 1;
}
void get(int beg, int d, int l, int r,
vector<Info> &buf) { // 提取从 beg 开始跳 [l,r] 步到达的结点
buf.clear();
int rs{0};
int vs{0};
for (int i{beg}, j{0}; j <= r; ++j) {
if ( j >= l && j <= r)
buf.emplace_back(i, rs, vs);
auto e = lis[i].e[(d + rs) & 3];
rs = (rs + e.r) & 3;
add(vs, e.ad);
i = e.to;
}
}
void init() {
for (int i{0}; i <= n + 1; ++i)
for (int j{0}; j <= n + 1; ++j)
id[i][ j] = ++nc;
for (int i{0}; i <= n + 1; ++i)
begr[i] = id[i][0], endr[i] = id[i][n + 1];
for (int i{0}; i <= n + 1; ++i)
begc[i] = id[0][i], endc[i] = id[n + 1][i];
for (int i{1}; i <= n; ++i)
for (int j{1}, v{1}; j <= n; ++j)
v = 1ll * v * (i + 1) % 998244353, val[i][ j] = v;
for (int i{0}; i <= n + 1; ++i)
for (int j{0}; j <= n + 1; ++j) {
for (int d : {
0, 1, 2, 3
}) {
int tx{i + dx[d]}, ty{ j + dy[d]};
if (inm(tx, ty)) {
lis[id[i][ j]].e[d].to = id[tx][ty];
lis[id[i][ j]].e[d].ad = (val[tx][ty] - val[i][ j] + P) % P;
}
}
}
}
int _getans() {
int ret{0}, mul{1};
for (int i{1}; i <= n; ++i) {
vector<Info> line;

get(begr[i], RIGHT, 1, n, line);
for (auto t : line) {
mul = 12345ll * mul % P;
ret = (ret + 1ll * mul * int(t.s)) % P;
}
}
return ret;
}
void doop(int t, int x1, int y1, int x2, int y2, int d) {
if (t == 1 && x1 == x2 && y1 == y2)
return;
vector<Info> up, down, left, right, upx, downx, leftx, rightx;
get(begr[x1 - 1], RIGHT, y1, y2, upx);
get(begr[x1], RIGHT, y1, y2, up);
get(begr[x2], RIGHT, y1, y2, down);
get(begr[x2 + 1], RIGHT, y1, y2, downx);
get(begc[y1 - 1], DOWN, x1, x2, leftx);
get(begc[y1], DOWN, x1, x2, left);
get(begc[y2], DOWN, x1, x2, right);
get(begc[y2 + 1], DOWN, x1, x2, rightx);
auto adde = [](const Info & u, const Info & v, int d) {
lis[u.i].e[(d + u.r) & 3] = E{v.i, (v.r - u.r + 4) & 3, (v.s - u.s + P) % P};
};
if (t == 1) {
int len{x2 - x1 + 1};
for (auto &t : up)
++t.r;
for (auto &t : down)
++t.r;
for (auto &t : left)
++t.r;
for (auto &t : right)
++t.r;
for (int i{0}; i < len; ++i) {
adde(upx[i], right[i], DOWN), adde(right[i], upx[i], UP);
adde(leftx[i], up[len - 1 - i], RIGHT), adde(up[len - 1 - i], leftx[i], LEFT);
adde(downx[i], left[i], UP), adde(left[i], downx[i], DOWN);
adde(rightx[i], down[len - 1 - i], LEFT), adde(down[len - 1 - i], rightx[i], RIGHT);
}
} else {
for (auto &t : up)
add(t.s, d);
for (auto &t : down)
add(t.s, d);

for (auto &t : left)
add(t.s, d);
for (auto &t : right)
add(t.s, d);
for (int i{0}; i < y2 - y1 + 1; ++i) {
adde(upx[i], up[i], DOWN), adde(up[i], upx[i], UP);
adde(downx[i], down[i], UP), adde(down[i], downx[i], DOWN);
}
for (int i{0}; i < x2 - x1 + 1; ++i) {
adde(leftx[i], left[i], RIGHT), adde(left[i], leftx[i], LEFT);
adde(rightx[i], right[i], LEFT), adde(right[i], rightx[i], RIGHT);
}
}
}
int main() {
n = inn(), q = inn();
init();
while (q--) {
int t = inn(), x1 = inn(), y1 = inn(), x2 = inn(), y2 = inn(), d{0};
if (t == 2)
d = inn();
doop(t, x1, y1, x2, y2, d);
}
printf("%d\n", _getans());
return 0;
}


