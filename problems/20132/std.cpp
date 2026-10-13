#include <cassert>
#include <bits/stdc++.h>
using namespace std;
#define int long long
#define rep(i,j,k) for(int i=( j);i<=(k);i++)
#define per(i,j,k) for(int i=( j);i>=(k);i--)
#define pb push_back
#define mp make_pair
#define fi first
#define se second
typedef vector<int> vi;
typedef pair<int, int> pi;
const int N = 2e5 + 20, inf0 = 1e18, inf1 = 4e18;
int n, k, q;
array<int, 5> a[N];
int f[N];
inline int dis(const int &x, const int &y) {
return y >= x ? y - x : y - x + k;
}
vi Merge(const vi &A, const vi &B) {
assert(A.size() > 0 && B.size() > 0);
vi res{A[0] + B[0]};
auto it0 = A.begin() + 1, it1 = B.begin() + 1;
while (it0 != A.end() || it1 != B.end()) {
int dA = (it0 == A.end() ? -inf1 : *it0 - *prev(it0));
int dB = (it1 == B.end() ? -inf1 : *it1 - *prev(it1));
if (dA > dB) {
res.pb(dA);
it0++;
} else {
res.pb(dB);
it1++;
}
}
rep(i, 1, (int)res.size() - 1) {
res[i] += res[i - 1];
}
return res;
}
void chmax(vi &a, const vi &b) {
rep(i, 0, (int)min(a.size(), b.size()) - 1) {
if (b[i] > a[i]) {
a[i] = b[i];
}
}
}
struct info {
vi w[5][5];
int len;
};

info operator+(const info &A, const info &B) {
info res;
res.len = A.len + B.len;
rep(i, 0, k - 1) {
rep( j, 0, k - 1) {
int sz = max(0ll, res.len - dis(i, j)) / k + 1;
res.w[i][ j].resize(sz);
fill(res.w[i][ j].begin(), res.w[i][ j].end(), -inf0);
rep(t, 0, k - 1) {
vi Get = Merge(A.w[i][t], B.w[t][ j]);
if (dis(i, t) + dis(t, j) >= k) {
Get.insert(Get.begin(), -inf0);
}
chmax(res.w[i][ j], Get);
}
rep(t, 0, k - 1) {
vi Get = Merge(A.w[i][t], B.w[(t + 1) % k][ j]);
if (dis(i, t) + 1 + dis((t + 1) % k, j) >= k) {
Get.insert(Get.begin(), -inf0);
}
chmax(res.w[i][ j], Get);
}
}
}
return res;
};
info solve(int l, int r) {
if (r - l <= 50) {
info res;
res.len = r - l + 1;
vector<vi> f(k, vi(res.len + 1, -inf0));
rep(D, 0, k - 1) {
f[D][0] = a[l][D];
rep(i, l + 1, r) {
per( j, i - l, 1) {
f[D][ j] = max(f[D][ j], f[D][ j - 1]) + a[i][(D + j) % k];
}
f[D][0] += a[i][D];
}
}
rep(i, 0, k - 1) {
rep( j, 0, k - 1) {
int D = dis(i, j);
int sz = max(0ll, res.len - D) / k + 1;
res.w[i][ j].resize(sz);
rep(t, 0, sz - 1) {
res.w[i][ j][t] = f[i][D + t * k];
}
}
}

return res;
}
if (l == r) {
info res;
res.len = 1;
rep(i, 0, k - 1) {
rep( j, 0, k - 1) {
res.w[i][ j] = (vi) {
i == j ? a[l][i] : -inf0
};
}
}
return res;
}
int mid = (l + r) / 2;
return solve(l, mid) + solve(mid + 1, r);
}
signed main() {
freopen("division.in", "r", stdin);
freopen("division.out", "w", stdout);
ios::sync_with_stdio(0);
cin.tie(0);
cout.tie(0);
cin >> n >> k >> q;
rep(i, 0, k - 1) {
rep( j, 1, n) {
cin >> a[ j][i];
}
}
info Get = solve(1, n);
rep(i, 1, q) {
int m;
cin >> m;
assert((int)Get.w[0][(m - 1) % k].size() > (m - 1) / k);
cout << Get.w[0][(m - 1) % k][(m - 1) / k] << '\n';
}
return 0;
}


