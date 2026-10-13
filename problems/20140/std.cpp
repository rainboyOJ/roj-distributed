#include<bits/stdc++.h>
using namespace std;
char s[100],t[100];
string f[100],g[100],ans;
int n;
int main(){
    freopen("xiao.in","r",stdin);
    freopen("xiao.out","w",stdout);
	scanf("%s%s",s+1,t+1);n=strlen(s+1);
	for(int i=1;i<=n;i++){
		for(int j=i;j--;){
			string now1=f[j]+s[i],now2=g[j]+t[i];
			if(now1>f[j+1])f[j+1]=now1,g[j+1]=now2;
			else if(now1==f[j+1]&&now2>g[j+1])g[j+1]=now2;
		}
	}
	for(int i=1;i<=n;i++)ans=max(ans,f[i]+g[i]);
	printf("%s\n",ans.c_str());
	return 0;
}