#include <stdio.h>
#include <algorithm>
#include <numeric>
typedef unsigned int uint;
typedef unsigned long long ull;
constexpr uint mod(998244353);
constexpr uint power(uint x, uint y) {
uint s(1);
while (y > 0) {
if (y & 1) {
s = ull(s) * x % mod;
}
x = ull(x) * x % mod;
y >>= 1;
}
return s;
}
constexpr ull rpower(const uint &x, uint y) {
ull s(1);
while (y--) {
s *= x;
}
return s;
}
constexpr uint phi(uint x) {
uint s(1);
for (uint i = 2; i * i <= x; i++) {
if (x % i == 0) {
x /= i, s *= i - 1;
while (x % i == 0) {
x /= i, s *= i;
}
}
}
if (x > 1) {
s *= x - 1;
}
return s;
}
void solve() {
uint m, a, b, c, d;
scanf("%u%u%u%u%u", &m, &a, &b, &c, &d);
const ull l(a && b ? rpower(m, std::gcd(a, b) - 1) : 0), r(c &&
d ? rpower(m, std::gcd(c, d) - 1) : 0), p(r - l);
const uint x(m >> __builtin_ctz(m));

uint ans(0);
for (uint i = 1; i * i <= x; i++) {
if (x % i == 0) {
ans = (ans + ull(phi(i)) * power(2, p * (m / i) % (mod - 1))) % mod;
if (i * i != x) {
ans = (ans + ull(phi(x / i)) * power(2, p * (m / (x / i)) % (mod - 1))) % mod;
}
}
}
ans = ull(ans) * power(m, mod - 2) % mod;
printf("%u\n", ans);
}
int main() {
int t;
scanf("%d", &t);
while (t--) {
solve();
}
return 0;
}


