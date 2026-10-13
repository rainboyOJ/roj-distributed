#include<cstring>
#include<algorithm>
#include<cstdio>
#include<iostream>
#include<vector>
using namespace std;
typedef long long ll;

const int N=2e5+15;
const int M=5e3+15;
const ll inf=1e15;
int n,m,k,a,b;
int v[N],A[N],B[N],vis1[N],vis2[N];
ll dp[M][M];
vector <ll> p1,p2,p3,p4;
inline int read()
{
	char ch=getchar();
	int s=0,f=1;
	while (ch<'0'||ch>'9') {if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9') {s=(s<<3)+(s<<1)+ch-'0';ch=getchar();}
	return s*f;
}
namespace task_1{
	void main()
	{
		ll ans=inf;
		int S=1<<n;
		for (int i=1;i<S;i++)
		{
			int cnt1=0,cnt2=0;
			ll now=0;
			for (int j=0;j<n;j++)
				if (i&(1<<j)) 
				{
					now+=v[j+1];
					if (vis1[j+1]) cnt1++;
					if (vis2[j+1]) cnt2++;
				}
			if (cnt1>=k&&cnt2>=k) ans=min(ans,now);
		}
		if (ans==inf) puts("-1");else printf("%lld\n",ans);
	}
}
int main()
{
	freopen("b.in","r",stdin);
	freopen("b.out","w",stdout);
	n=read();m=read();k=read();
	for (int i=1;i<=n;i++) v[i]=read();
	a=read();
	for (int i=1;i<=a;i++) A[i]=read();
	b=read();
	for (int i=1;i<=b;i++) B[i]=read();
	for (int i=1;i<=a;i++) vis1[A[i]]=1;
	for (int i=1;i<=b;i++) vis2[B[i]]=1; 
	//if (n<=20) {task_1::main();return 0;}
	for (int i=1;i<=n;i++) 
	{
		if (vis1[i]&&vis2[i]) p1.push_back(i);//都喜欢的 
		else if (vis1[i]) p2.push_back(v[i]);//A喜欢的 
		else if (vis2[i]) p3.push_back(v[i]);//B喜欢的 
		else p4.push_back(v[i]);
	}
	sort(p2.begin(),p2.end());
	sort(p3.begin(),p3.end());
	sort(p4.begin(),p4.end());
	for (int i=0;i<=n;i++)	
		for (int j=0;j<=m;j++) dp[i][j]=inf;
	dp[0][0]=0;
	for (int i=1;i<=p1.size();i++)	
		for (int j=0;j<=i;j++)
		{
			dp[i][j]=min(dp[i-1][j],dp[i-1][j-1]+v[p1[i-1]]);
		}
	ll ans=inf;
	int n1=p1.size(),n2=p2.size(),n3=p3.size(),n4=p4.size();
	//printf("%lld\n",dp[1][1]);
	//printf("qq%d %d\n",v[p2[0]],v[p3[0]]);
	/*for (int i=0;i<n1;i++) printf("%d ",p1[i]);
	printf("\n");*/
	/*for (int i=0;i<n2;i++) printf("%d ",p2[i]);
	printf("\n");
	for (int i=0;i<n3;i++) printf("%d ",p3[i]);
	printf("\n");
	for (int i=0;i<n4;i++) printf("%d ",p4[i]);
	printf("\n\n");*/
	//printf("qq%d %d %d %d\n",n1,n2,n3,n4);
	for (int i=0;i<=n1;i++)
	{
		ll re=dp[n1][i];
		int cnt=i,pp=0;
		//if (i==2) printf("qq%d\n",k-i);
		if (k-i>n2) continue;
		if (k-i>n3) continue;
		for (int j=1;j<=k-i;j++) {re+=1ll*p2[j-1];re+=1ll*p3[j-1];cnt+=2;++pp;}
		//printf("%d %d\n",i,cnt);
		if (cnt>m) continue;
		//printf("%d %d %lld\n",dp[n1][i],cnt,re);
		if (cnt==m) {ans=min(ans,re);continue;}
		int pos2=pp+1,pos3=pp+1,pos4=1;
		while (cnt<=m)
		{	
			++cnt;
			if (cnt>m) break;
			//if (i==2) printf("%d %d %d\n",pos2,pos3,pos4);
			int now=1e9+7,key;
			if (pos2<=n2&&pos2) if (now>p2[pos2-1])  {now=p2[pos2-1];key=2;}
			if (pos3<=n3&&pos3) if (now>p3[pos3-1])  {now=p3[pos3-1];key=3;}
			if (pos4<=n4&&pos4) if (now>p4[pos4-1])  {now=p4[pos4-1];key=4;}
			if (now==1e9+7) break;
			re+=1ll*now;
			if (key==2) pos2++;
			else if (key==3) pos3++;
			else if (key==4) pos4++;
		}
		//if (i==2) printf("%lld\n",re);
		//printf("%d %lld\n",i,ans);
		ans=min(ans,re); 
	}
	if (ans==inf) puts("-1");else printf("%lld\n",ans);
	return 0;
}
