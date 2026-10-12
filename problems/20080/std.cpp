#include <bits/stdc++.h>

using namespace std;

constexpr int N = 5e7, mod = 998244353;

uint64_t c[N + 1];

int main() {
  uint64_t n, m, t; cin >> n >> m;
  t = m;
  for (int i = 3; i <= n; ++i) {
    c[i] = c[i - 1] * m;
    if (i % 2) {
      t = t * m % mod;
      c[i] = c[i] + t + mod - c[i / 2 + 1];
    }
    c[i] %= mod;
  }
  cout << c[n];
}
/*
abacaba k=1
abacaba k=3
重复计数
 
 
如果有一个k>n/2 成立，那么一定有一个k<n/2成立。 

*/
