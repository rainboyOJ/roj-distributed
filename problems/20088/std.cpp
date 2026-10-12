// #include <bits/stdc++.h>
// using namespace std;

// #define int long long

// const int N = 2e5 + 10;
// int n, k, a[N], ans = 0, flag = 0, sum = 0;

// void dfs(int cur = 1, int num = 0, int tot = 0) {
// 	if (num >= k) {
// 		ans = max(ans, tot ^ sum);
// 		return;
// 	}
// 	if (cur > n) return;
// 	dfs(cur + 1, num + 1, tot ^ a[cur]);
// 	dfs(cur + 1, num, tot);
// }

// signed main() {
// 	ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
// 	cin >> n >> k;
// 	for (int i = 1; i <= n; i++) cin >> a[i];
// 	if (k >= (n + 1) / 2) {
// 		k = n - k;
// 		flag = 1;
// 	}
// 	if (flag)
// 		for (int i = 1; i <= n; i++) sum ^= a[i];
// 	else sum = 0;
// 	dfs();
// 	cout << ans << endl;
// 	return 0;
// }

#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef long double ld;
typedef pair<int, int> Pii;
typedef pair<int, ll> Pil;
typedef pair<ll, ll> Pll;
typedef pair<ll, int> Pli;
typedef vector<vector<ll>> Mat;
#define fi first
#define se second
const ll MOD = 1e9 + 7;
const ll MOD2 = 998244353;
const ll MOD3 = 1812447359;
const ll INF = 1ll << 62;
const double PI = 2 * asin(1);
void yes() { printf("yes\n"); }
void no() { printf("no\n"); }
void Yes() { printf("Yes\n"); }
void No() { printf("No\n"); }
void YES() { printf("YES\n"); }
void NO() { printf("NO\n"); }

int n, k;
ll a[int(2e5 + 5)];

ll ans = 0, total = 0;

void solve(int idx, int cnt, ll val) {
  if (cnt == k) {
    ans = max(ans, val);
    return;
  }
  if (cnt + k == n) {
    ans = max(ans, total ^ val);
    return;
  }
  if (idx > n) {
    return;
  }

  solve(idx + 1, cnt + 1, val ^ a[idx]);
  solve(idx + 1, cnt, val);

  return;
}

int main() {
  cin >> n >> k;
  for (int i = 1; i <= n; i++) {
    cin >> a[i];
    total = total ^ a[i];
  }

  solve(1, 0, 0);
  cout << ans << endl;

  return 0;
}
