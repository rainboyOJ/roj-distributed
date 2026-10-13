#include <bits/stdc++.h>
using namespace std;
#define ll long long
const int N=1e5+5,mod=998244353;
inline void Add(int &a,int b){a+=(a+b>=mod)?b-mod:b;}
inline void Dec(int &a,int b){a-=(a-b<0)?b-mod:b;}
ll a[N],b[N],c[N];
int cnt[N];
#define mp make_pair
#define pli pair<ll,int>
#define fi first
#define se second
priority_queue<pli> q;
inline ll calc(ll x,ll t){
	ll y=x/t,z=x-y*t;
	return y*y*(t-z)+(y+1)*(y+1)*z;
}
int n,m,ans;
int main(){
	scanf("%d%d",&n,&m);
	for(int i=1;i<=n;++i)scanf("%lld",&a[i]);
	int d=0;
	for(int i=1;i<=n;++i){
		scanf("%lld",&b[i]);
		if(a[i]!=b[i])++d;
		c[i]=abs(a[i]-b[i]);
		ans=(ans+1ll*c[i]*c[i])%mod;
		if(c[i]>1){
			q.push(mp(1ll*c[i]*c[i]-calc(c[i],2),i));
			cnt[i]=2;
		}
	}
	if(d>m){puts("-1");return 0;}
	m-=d;
	pli cur;
	for(;m&&!q.empty();--m){
		cur=q.top();q.pop();
		Dec(ans,cur.fi%mod);
		if(cnt[cur.se]==c[cur.se])continue;
		q.push(mp(calc(c[cur.se],cnt[cur.se])-calc(c[cur.se],cnt[cur.se]+1),cur.se));
		++cnt[cur.se];
	}
	printf("%d\n",ans);
	return 0;
}