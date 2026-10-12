#include <bits/stdc++.h>

using namespace std;

#define ll long long

const int N = 5e5 + 10;

int n, a[N << 1], b[N << 1];

int main()
{
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);
    cin >> n;
    vector<int> q;
    ll ans = 0;
    for (int i = 1; i <= 2 * n; i++) cin >> a[i] >> b[i], q.push_back(b[i] - a[i]), ans += a[i];
    sort (q.begin(), q.end());
    for (int i = q.size() - 1, j = 1; i >= 0 && j <= n; i--, j++) ans += q[i];
    cout << ans;
    return 0;
}
