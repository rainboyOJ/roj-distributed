#include<bits/stdc++.h>

using namespace std;
signed main(){
    int ans=0;
for(int i=1;i<=5;i++)
	for(int j=i;j<=i;j++)
		for(int k=j;k<=5;k++)
			ans+=k;
cout<<ans<<endl;
    return 0;
}
