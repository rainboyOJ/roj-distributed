
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tt;
  cin >> tt;
  while (tt--) {
    int n;
    cin >> n;
    if (n <= 5) {
      cout << n / 2 + 1 << '\n';
      for (int i = 0; i < n; i++) {
        cout << (i + 3) / 2 << " \n"[i == n - 1];
      }
    } else {
      cout << 4 << '\n';
      for (int i = 0; i < n; i++) {
        cout << i % 4 + 1 << " \n"[i == n - 1];
      }
    }
  }
  return 0;
}

