#include<cstdio>
#include<algorithm>
using namespace std;
int n,m,x,y,ans,sum,k,z,a[1000001];
int main(){
	scanf("%d%d",&n,&m);
	for(int j=1;j<=m;j++){
    		scanf("%d%d%d",&x,&y,&z);
    		a[x]+=z;a[y]+=z;
	}
	sort(a+1,a+1+n);
	for(int i=n;i>=1;i-=2)
    		ans+=a[i]-a[i-1];
	printf("%d",ans/2);
	return 0;
}
