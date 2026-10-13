#include<bits/stdc++.h>

using namespace std;

const int MX=2005,inf=0x3f3f3f3f;

int n,K;
int a[MX];

bool ava(int w){
	set<pair<int,int>, greater<pair<int, int> > > res;
	for(int i=1;i<=n;i++)res.insert(make_pair(a[i], i));
	int t=0;
	while(!res.empty()){
		t++;
		if(t>K)break;
		int rs=w;
		while(true){
			set<pair<int, int>, greater<pair<int, int> > >::iterator it=res.lower_bound(make_pair(rs, inf));
			if(it==res.end())break;
			rs-=it->first;
			res.erase(it);
		}
	}
	return t<=K;
}

int main(){
	freopen("trans.in","r",stdin);
	freopen("trans.out","w",stdout);
	ios::sync_with_stdio(false);
	cin>>n>>K;
	for(int i=1;i<=n;i++)cin>>a[i];
	int LB=0,UB=0;
	for(int i=1;i<=n;i++){
		LB=max(LB,a[i]);
		UB+=a[i];
	}
	int l=LB,r=UB;
	while(l<r){
		int mid=(l+r)/2;
		if(ava(mid)){
			r=mid;
		}else{
			l=mid+1;
		}
	}
	int ans=0;
	for(int i=max(LB,l-LB);i<=l;i++){
		if(ava(i)){
			ans=i;break;
		}
	}
	cout<<ans<<endl;
	cerr<<clock()<<endl;
	return 0;
}