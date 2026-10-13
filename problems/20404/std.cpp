#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main()
{
  string T;
  int K;
  cin >> T >> K;
  int N = T.size();

  sort(T.begin(),T.end());
  int zera = 0;
  while (T[zera] == '0') zera++;
  for(int i = 0; i < K; i++) T[i] = T[i + zera];
  for(int i = K; i < K + zera; i++) T[i] = '0';

  vector<vector<int>> A(K);
  int j = 0;
  for(int i = 0; i < N; i++) {
    A[j].push_back((int)(T[i] - '0'));
    j = (j + 1) % K;
  }
  long long ans = 0;
  for(int j = 0; j < K; j++) {
    long long x = 0;
    for(int q = 0; q < (int)A[j].size(); q++)
      x = 10 * x + A[j][q];
    ans += x;
  }
  cout << ans << "\n";
}
