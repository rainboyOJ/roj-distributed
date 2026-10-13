/*
Things to notice:
1. do not calculate useless values
2. do not use similar names
 
Things to check:
1. submit the correct file
2. time (it is log^2 or log)
3. memory
4. prove your naive thoughts 
5. long long
6. corner case like n=0,1,inf or n=m
7. check if there is a mistake in the ds or other tools you use
8. fileio in some oi-contest

9. module on time 
10. the number of a same divisor in a math problem
11. multi-information and queries for dp and ds problems
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long
#define fi first
#define se second
#define pii pair<long long,long long>
#define mp make_pair
#define pb push_back
const int mod=998244353;
const int inf=0x3f3f3f3f;
const int INF=1e18;
int n;
char s[5005];
int dp[5005][5005];
void solve()
{
	cin>>n;
	cin>>(s+1);
	dp[0][0]=1;
	for(int i=0;i<n;i++) for(int j=0;j<=i;j++)
	{
		dp[i+1][j]=(dp[i+1][j]+dp[i][j])%mod;
		if(s[i+1]!='('&&j) dp[i+1][j-1]=(dp[i+1][j-1]+dp[i][j])%mod;
		if(s[i+1]!=')') dp[i+1][j+1]=(dp[i+1][j+1]+dp[i][j])%mod; 
	}
	cout<<dp[n][0]<<"\n";
}
signed main()
{
	freopen("bracket.in","r",stdin);
	freopen("bracket.out","w",stdout);
//	ios::sync_with_stdio(0);
//	cin.tie(0);
	int _=1;
//	cin>>_;
	while(_--) solve();
	return 0;
} 