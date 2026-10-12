#include <iostream>
#include <vector>

using namespace std;
using LL = long long;

const int kN = 1e6+7;
const int kL = 18;

int n, a[kN], b[kN];
LL ans;
vector<int> sd;

void C(vector<int> &d1, vector<int> &d2, bool w) {
  for (int i = 0; i < kL; ++i) {
    int c11 = 0, c12 = 0;
    for (int j : d1) {
      c11 += (w ? b[j] : a[j]) >> i & 1;
    }
    for (int j : d2) {
      c12 += (w ? b[j] : a[j]) >> i & 1;
    }
    ans += (1LL * c11 * (d2.size() - c12) + 1LL * (d1.size() - c11) * c12) << i;
  }
}
void S(int p, vector<int> &d) {
  if (d.empty()) {
    return;
  }
  if (p == -1) {
    for (int i = 0; i < kL; ++i) {
      int c1 = 0;
      for (int j : d) {
        c1 += a[j] >> i & 1;
      }
      ans += 1LL * c1 * (d.size() - c1) << i;
    }
    return;
  }
  vector<int> l[2][2];
  for (int i : d) {
    l[a[i] >> p & 1][b[i] >> p & 1].push_back(i);
  }
  C(l[0][0], l[0][1], 0);
  C(l[0][0], l[1][0], 1);
  C(l[1][1], l[0][1], 1);
  C(l[1][1], l[1][0], 0);
  for (int i : l[1][1]) {
    l[0][0].push_back(i);
  }
  for (int i : l[1][0]) {
    l[0][1].push_back(i);
  }
  S(p - 1, l[0][0]), S(p - 1, l[0][1]);
}

int main() {
  ios_base::sync_with_stdio(0), cin.tie(0);
  cin >> n;
  for (int i = 1; i <= n; ++i) {
    cin >> a[i];
    sd.push_back(i);
  }
  for (int i = 1; i <= n; ++i) {
    cin >> b[i];
  }
  S(kL - 1, sd);
  cout << ans;
  return 0;
}
