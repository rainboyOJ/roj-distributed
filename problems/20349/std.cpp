#include<algorithm>
#include<cstring>
#include<cstdio>
#include<iostream>
using namespace std;
typedef long long ll;

const int N=1e5+15;
int n,q;
int x[N];
inline int read()
{
	char ch=getchar();
	int s=0,f=1;
	while (ch<'0'||ch>'9') {if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9') {s=(s<<3)+(s<<1)+ch-'0';ch=getchar();}
	return s*f;
}
namespace task1
{
	ll calc(int l)
	{
		int L=0,R=l;
		ll re=0;
		for (int i=1;i<=n;i++)
		{
			if (x[i]>=L&&x[i]<=R) continue;
			if (x[i]<L) 
			{
				re+=L-x[i];
				L=x[i];R=L+l;
			}
			if (x[i]>R)
			{
				re+=x[i]-R;
				R=x[i];L=R-l;
			}
		}
		return re;
	}
	void main()
	{
		for (int i=1;i<=n;i++) x[i]=read();
		while (q--)
		{
			int l=read();
			printf("%lld\n",calc(l));
		}
	}
}
namespace task2
{
	void main()
	{
		while (q--)
		{
			int l=read();
			if (x[1]>=0) {printf("%lld\n",max(0,x[n]-l));continue;}
			printf("%lld\n",-x[1]+max(x[n]-x[1]-l,0));
		}
	}
}
int main()
{
	freopen("z.in","r",stdin);
	freopen("z.out","w",stdout);
	n=read();q=read();
	if (n<=1000||q==0) {task1::main();return 0;} 
	bool flag=true;
	for (int i=1;i<=n;i++) 
	{
		x[i]=read();
		if (i>=2&&x[i]<x[i-1]) flag=false;
	}
	if (flag) task2::main();
	return 0;
}
