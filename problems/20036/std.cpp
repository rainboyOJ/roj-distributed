#include <bits/stdc++.h>

using namespace std;

#define ll long long

#define fst ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);

int main()
{
    fst
    ll n; cin >> n;
    ll ans = 0;
    for (ll i = 0; i * i <= n; i += 2) {
        ll x = i * i; bool ok = 1;
        while (x) {
            if ((x % 10) & 1) {
                ok = 0;
                break;
            }
            x /= 10;
        }
        ans += ok;
    }
    cout << ans;
    return 0;
}
