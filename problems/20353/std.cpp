#include<algorithm>
#include<cstring>
#include<cstdio>
#include<iostream>
using namespace std;
typedef long long ll;

const int N=1e6+15;
const int inf=1e9+7;
int n,m;
ll S;
struct node
{
	int k,b;
}a[N];
inline ll read()
{
	char ch=getchar();
	ll s=0,f=1;
	while (ch<'0'||ch>'9') {if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9') {s=(s<<3)+(s<<1)+ch-'0';ch=getchar();}
	return s*f;
}
namespace task_1
{
	ll ans=inf;
	void dfs(int x,int res,ll k,ll b)
	{	
		if (res>m) return;
		if (x==n+1) 
		{	
			//printf("%d %d %lld %lld\n",x,res,k,b);
			if (k<=0) if (b>=S) ans=0;
			if (k>0) ans=min(ans,(S-b-1)/k+1);
			return;
		}
		dfs(x+1,res+1,k+a[x].k,b+a[x].b);
		dfs(x+1,res,k,b);
	}
	void main()
	{
		dfs(1,0,0,0);
		printf("%lld\n",ans);
	}
}
namespace task_2
{
	ll now[N];
	bool check(int x)
	{
		int cnt=0;
		for (int i=1;i<=n;i++)
		{
			ll p=1ll*x*a[i].k+a[i].b;
			if (p>0) now[++cnt]=p; 
		}
		sort(now+1,now+1+cnt);
		ll o=0;
		for (int i=cnt;i>=max(1,cnt-m+1);i--)
		{
			o+=now[i];
		}
		return o>=S;
	}
	void main()
	{
		int l=0,r=inf;
		while (l<r)
		{
			int mid=l+r>>1;
			if (check(mid)) r=mid;
			else l=mid+1;
		}
		printf("%d\n",l);
	}
}
namespace task_3
{
	void main()
	{
		puts("0");
	}
}
int main()
{
//	freopen("merchant.in","r",stdin);
//	freopen("merchant.out","w",stdout);
	n=read();m=read();S=read();
	bool fl1=0,fl2=0;
	for (int i=1;i<=n;i++)
	{
		a[i].k=read();a[i].b=read();	
		if (a[i].k>0) fl1=1;
		if (a[i].k<0) fl2=1;
	}
	if (n<=20) {task_1::main();return 0;}
	if (fl1==1&&fl2==0) {task_2::main();return 0;}
	if (fl1==0&&fl2==1) {task_3::main();return 0;}
	task_2::main();
	return 0;
}
