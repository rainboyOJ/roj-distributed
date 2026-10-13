#include<bits/stdc++.h>
#define rep(i,a,b) for(int i=a;i<=b;i++)
#define lint long long
using namespace std;
int main()
{
	int T; scanf("%d",&T);
	while(T--)
	{
		lint l,r,ans=0; scanf("%lld%lld",&l,&r);
		for(lint s=1,t;s<=r;s=t+1)
		{
			t=r/(r/s);
			if(s<l) t=min(t,(l-1)/((l-1)/s));
			if(r/s-(l-1)/s>1) ans=max(ans,t);
		}
		printf("%lld\n",ans);
	}
	return 0;
}
