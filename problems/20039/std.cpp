#include<bits/stdc++.h>
using namespace std;
const int maxn = 5010; 
int f[2][maxn];
const int mod = 1e7 + 7;
inline void add(int i,int l,int r,int d)
{
	f[i][l] += d;
	if(f[i][l] >= mod) f[i][l] -= mod;
	f[i][r + 1] -= d;
	if(f[i][r + 1] < 0) f[i][r + 1] += mod;
}
signed main()
{
	ios::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	int n;
	cin >> n;
	for(int i = 1;i <= n;i++)
	{
		for(int j = 0;j <= n;j++) f[(i + 1) & 1][j] = 0; 
		for(int j = 2;j <= i + 1;j++) add((i + 1) & 1,j,j,1);
		for(int j = 2;j <= i;j++) add((i + 1) & 1,2,j + 1,f[i & 1][j]);
		for(int j = 1;j <= n;j++)
		{
			f[(i + 1) & 1][j] += f[(i + 1) & 1][j - 1];
			if (f[(i + 1) & 1][j] >= mod) f[(i + 1) & 1][j] -= mod;
		}
	}
	int ans = 0;
	for(int i = 2;i <= n;i++)
	{
		ans += f[n & 1][i];
		if(ans >= mod) ans -= mod;
	}
	cout << ans + 1 << '\n';
	return 0;
}
