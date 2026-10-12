#include <iostream>
#include <string>
#include <cmath>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        string r;
        cin >> r;
        long long ans = 0;
        int len = r.size();
        
        for (int i = 0; i < len; ++i) {
            int digit = r[len - 1 - i] - '0';
            ans += 1LL * digit * (1LL << i);  
        }
        cout << ans << '\n';
    }
    return 0;
}
