#include <bits/stdc++.h>
using namespace std;
typedef __int128 i128;
typedef unsigned long long ull;
typedef long long ll;
const int N = 3e5 + 5;
mt19937 rnd(114514);
#define mytz __builtin_ctzll
inline bool jac(ull a, ull b) {
bool ans = 0;
while (1) {
a %= b;
if (a == 1)
return ans;
short az = mytz(a), o = az & 1 & (((b * b - 1) & 15) != 0);
a >>= az;
ans ^= o;
if (a == 1)
return ans;
ans ^= (((a - 1) * (b - 1)) & 7) != 0, a ^= b ^= a ^= b;
}
return ans;
}
i128 a[N];
ull st[N];
const int B = 40, limcnt = 50, lim = 1e5;
int cnt, o[100], n, ptr[N], p[100];
vector<int> pm;
inline i128 read() {
char ch = getchar();
i128 ans = 0;
while (!isdigit(ch))
ch = getchar();
while (isdigit(ch)) {
ans = ans * 10 + ch - 48, ch = getchar();
}
return ans;
}
vector<int> vec[N], pv;
inline bool isprime(int x) {
for (int i : pm) {
if (i * i > x)
return 1;
if (x % i == 0)
return 0;
}
return 1;
}

bool tag[N], inv[100];
inline void initprime(int A, int B) {
for (int i = 2; i * i <= 40000; ++i)
if (!tag[i])
for (int j = i * i; j <= 40000; j += i)
tag[ j] = 1;
for (int i = 2; i <= 40000; ++i)
if (!tag[i])
pm.push_back(i);
while (cnt <= limcnt) {
int p = (rnd() % (B - A + 1) + A) * 2 + 1;
if (isprime(p))
o[++cnt] = p;
}
}
int main() {
initprime(5e7, 5e8);
cin >> n;
for (int i = 1; i <= n; ++i)
a[i] = read();
for (int i = 1; i <= limcnt && pv.size() < B; ++i)
if (!inv[i])
pv.push_back(o[i]);
ll ans = 0;
vector<ull> pl;
st[0] = 0;
pl.push_back(st[0]);
for (int i = 1; i <= n; ++i) {
ull z = 1;
for (auto j : pv)
st[i] |= jac(a[i] % j, j) * z, z <<= 1;
st[i] ^= st[i - 1];
pl.push_back(st[i]);
}
sort(pl.begin(), pl.end());
pl.erase(unique(pl.begin(), pl.end()), pl.end());
for (int i = 0; i <= n; ++i)
st[i] = lower_bound(pl.begin(), pl.end(), st[i]) - pl.begin() + 1, vec[st[i]].push_back(i);
vector<pair<int, int>> res;
for (int i = 0; i < n; ++i) {
ptr[st[i]]++;
ans += (int)vec[st[i]].size() - ptr[st[i]];
for (int j = ptr[st[i]]; j < (int)vec[st[i]].size() && res.size() < lim; ++j)
res.push_back(make_pair(i + 1, vec[st[i]][ j]));
}

cout << ans << '\n';
for (auto i : res)
cout << i.first << ' ' << i.second << '\n';
}


