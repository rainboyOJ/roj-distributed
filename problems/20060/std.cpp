#include <bits/stdc++.h>
#define fst first
#define snd second
#define fore(i,a,b) for(int i=a,ThxDem=b;i<ThxDem;++i)
#define pb push_back
#define ALL(s) s.begin(),s.end()
#define FIN ios_base::sync_with_stdio(0);cin.tie(0);cout.tie(0)
#define SZ(s) int(s.size())
using namespace std;
typedef long long ll;
typedef pair<int,int> ii;

const int MAXN=2e5+10;
vector<ll> dp[MAXN];
ll INF=4e18;

ll solve(int n, int rem){
	if(!n) return rem==0;
	
	if(rem>=SZ(dp[n])) dp[n].resize(rem+1,-1);
	ll &r=dp[n][rem];
	if(r>=0)return r;
	r=0;
	
	//poner el i-esimo ahora
	fore(i,0,min(n,rem+1)){
		r=min(INF, r+solve(n-1,rem-i));
		if(r==INF)break;
	}
	
	return r;
}

int main(){FIN;
	int n; ll k; cin>>n>>k;
	
	int rem=0;
	while(solve(n,rem)<k) k-=solve(n,rem),rem++;
	vector<int> ans;
	
	vector<int> v(n);
	fore(i,0,n) v[i]=n-i-1;
	
	while(n){
		fore(i,0,min(n,rem+1)){
			if(solve(n-1,rem-i)<k) k-=solve(n-1,rem-i);
			else{
				ans.pb(v[SZ(v)-i-1]);
				v.erase(v.end()-i-1);
				n--;
				rem-=i;
				break;
			}
		}
	}
	
	for(auto x:ans)cout<<x+1<<" ";cout<<"\n";
}
