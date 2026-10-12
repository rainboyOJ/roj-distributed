#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <cstring>
#include <cmath>
#include <set>
#include <map>
#include <stack>
#include <queue>
#include <deque>

using namespace std;

#define int long long
#define ll long long
typedef vector<int> vi;
typedef vector<string> vs;
typedef pair<int, int> pi;
#define F first
#define S second
#define pb push_back
#define sz(a) a.size()
#define Print(a) for(auto x : a) {cout << x << " ";} cout << endl;
#define all(x) (x).begin(), (x).end()
#define rall(x) (x).rbegin(), (x).rend()
#define allr(x) (x).rbegin(), (x).rend()
#define endl "\n"
#define YES cout << "YES\n";
#define NO cout << "NO\n";

const int MOD = 1e9;

void solve() {
    int n, k; cin >> n >> k;
    if (n<k) {
        cout << 1 << endl;
        return;
    }

    vi a(n+1, 0);
    for(int i = 0; i < k; i++) {
        a[i] = 1;
    }

    queue<int> q;
    int sum = k;
    for(int i = k; i <= n; i++) {
        a[i] = sum;
        sum = (sum+a[i]-a[i-k]+MOD)%MOD;
    }

    cout << a[n] << endl;
}

int32_t main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);

    //freopen("wtf.in", "r", stdin);
    int t = 1;
    //cin >> t;
    while(t--) {
        solve();
    }
}
