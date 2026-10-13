#include<bits/stdc++.h>
using namespace std;
int a,b;
long double ans;
int main(){
    freopen("island.in","r",stdin);
    freopen("island.out","w",stdout);
	scanf("%d%d",&a,&b);
	for(int i=1;i<=a;i++)ans+=1.0/(2*i-1);
	for(int i=1;i<=b;i++)ans+=1.0/(2*a+i);
	printf("%.12Lf\n",ans);
	return 0;
}