#include<bits/stdc++.h>
#define LL long long
using namespace std;
const LL N=3e5+5;
char c[N];
LL n,lst[N],f[N],ans;
int main()
{
    freopen("bessie3.in","r",stdin);
    freopen("bessie3.out","w",stdout);
	scanf("%s",c+1);
	n=strlen(c+1);
	for(int i=1;i<=n;i++)
	{
		if(c[i]=='b')lst[1]=i;
		if(c[i]=='e')lst[2]=lst[1],lst[6]=lst[5];
		if(c[i]=='s')lst[4]=lst[3],lst[3]=lst[2];
		if(c[i]=='i')lst[5]=lst[4];
		f[i]=f[lst[6]-1]+lst[6];
	}
	for(int i=1;i<=n;i++)
	{
		ans+=f[i];
	}
	printf("%lld",ans);
	return 0;
}
