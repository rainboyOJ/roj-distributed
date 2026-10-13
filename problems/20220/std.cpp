#include<bits/stdc++.h>
using namespace std;
typedef unsigned long long ull;
ull pop_back(stack<pair<ull,int> >& stk,ull c){
	ull ans=0;
	while(c>0){
		pair<ull,int> x=stk.top(); stk.pop();
		ull d=min(c,x.first);
		x.first-=d;
		c-=d;
		if(x.first>0) stk.push(x);
		ans+=1llu*d*x.second;
	}
	return ans;
}
int main(){
	int n; scanf("%d",&n);
	vector<int> c(n);
	int x,y,z,m[2]; scanf("%d%d%d%d%d%d%d",&x,&y,&z,&m[0],&m[1],&c[0],&c[1]);
	for(int i=2;i<n;++i) c[i]=(1ll*c[i-1]*x+1ll*c[i-2]*y+z)%m[i%2]+1;
//	for(int i=0;i<n;++i) cerr<<c[i]<<" ";
	stack<pair<ull,int> > stk;
	stk.push(make_pair((ull)1e18,0));
	stk.push(make_pair(1,1));
	ull ans=0;
	ull ss1=0,ss2=0;
	for(int i=0;i<n;++i){
		if(~i&1){
			ss1+=c[i];
			stk.push(make_pair(c[i],1));
		}else{
			ss2+=c[i];
			pop_back(stk,1);
			ans+=pop_back(stk,c[i]-1);
			int t=stk.top().second;
			ans+=pop_back(stk,1);
			stk.push(make_pair(1,t+1));
//			printf("<%lld>",ans);
		}
	}
	printf("%lld\n",ans);
//	cerr<<ss1<<" "<<ss2<<endl;
	return 0;
}