#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    string s, t;
    cin >> s >> t;
    string u = s;
    if (!s.empty()) u[0] = s[0];
    u[1] = s[1];
    for (int i = 2; i < n; ++i) {
        if (s[i] == '1' && s[i-1] == '0' && s[i-2] == '0') u[i] = '0';
        else u[i] = s[i];
    }
    cout << (u == t ? "YES" : "NO") << '\n';
    return 0;
}
