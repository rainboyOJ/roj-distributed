#include <bits/stdc++.h>
#include "september.h"
using namespace std;
int clear[5][100010], deg[5][100010];
int solve(int N, int M, std::vector<int> F, std::vector<std::vector<int>> S) {
vector<int> cnt(N);
int t[5] = {}, ans = 0, sm = 0;
for (int i = 0; i < N; ++i)
for (int j = 0; j < M; ++j)
clear[ j][i] = deg[ j][i] = 0;
for (int i : F)
for (int j = 0; j < M; ++j)
if (i != -1)
deg[ j][i]++;
for (int i = 0; i < N - 1; ++i) {
for (int j = 0; j < M; ++j) {
++cnt[S[ j][i]];
if (cnt[S[ j][i]] == 1)
++sm;
if (cnt[S[ j][i]] == M)
--sm;
deg[ j][F[S[ j][i]]]--;
if (deg[ j][S[ j][i]])
++t[ j];
if (clear[ j][F[S[ j][i]]] && deg[ j][F[S[ j][i]]] == 0)
--t[ j];
clear[ j][S[ j][i]] = 1;
//cout<<i<<' '<<j<<' '<<t[ j]<<endl;
}
int flag = 1;
for (int j = 0; j < M; ++j)
if (t[ j])
flag = 0;
if (flag && !sm)
ans++;
}
return ans;
}


