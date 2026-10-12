#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const int N = 3e6;
ll cnt[N], sum = 0, ans = 0;
int n;
string s;

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
	cin >> n >> s;
    int cur = 4 * n;
    cnt[cur] = 1;
    for (int i = 0; i < n; i++) {
        if (s[i] == '0') {
        	cur++;
        	sum += cnt[cur - 2];
        } else {
            for(int j = 0; j < 3; j++) sum -= cnt[cur - 2 - j];
            cur -= 3;
        }
        ans += sum + cnt[cur + 1];
        cnt[cur]++;
    }
    cout << ans << endl;
    return 0;
}
