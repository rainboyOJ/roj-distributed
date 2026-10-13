/*
Things to notice:
1. do not calculate useless values
2. do not use similar names
 
Things to check:
1. submit the correct file
2. time (it is log^2 or log)
3. memory
4. prove your naive thoughts 
5. long long
6. corner case like n=0,1,inf or n=m
7. check if there is a mistake in the ds or other tools you use
8. fileio in some oi-contest

9. module on time 
10. the number of a same divisor in a math problem
11. multi-information and queries for dp and ds problems
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long
#define fi first
#define se second
#define pii pair<long long,long long>
#define mp make_pair
#define pb push_back
const int mod=998244353;
const int inf=0x3f3f3f3f;
const int INF=1e18;
mt19937 rnd(time(0));
struct Random_array
{
	int a[2000005],in[2000005],n,has;
	void init()
	{
		n=has=0;
	}
	void rebuild()
	{
		int j=0;
		for(int i=1;i<=n;i++) if(in[i]) j++,a[j]=a[i],in[j]=1;
		n=has=j;
	}
	void add(int x)
	{
		a[++n]=x,has++,in[n]=1;
	}
	int query()
	{
		int x=1+rnd()%n;
		while(!in[x]) x=1+rnd()%n;
		has--,in[x]=0;
		int res=a[x];
		if(has<n/2) rebuild();
		return res;
	}
}O,E;
void random_small(vector <int> vec)
{
	while(1)
	{
		O.init(),E.init();
		for(int i=0;i<vec.size();i++)
		{
			if(vec[i]%2==0) E.add(vec[i]);
			else O.add(vec[i]);
		}
		vector <pii > ans;
		ans.clear();
		while(O.has+E.has>=2)
		{
			if(O.has==1&&E.has==1) break;
			int tag=-1;
			if(O.has>=2&&E.has>=2) tag=rnd()%2;
			else if(O.has>=2) tag=0;
			else tag=1;
			if(tag==0)
			{
				int u=O.query();
				int v=O.query();
				ans.pb(mp(u,v));
				if(((u+v)/2)%2==1) O.add((u+v)/2);
				else E.add((u+v)/2);
			}
			else
			{
				int u=E.query();
				int v=E.query();
				ans.pb(mp(u,v));
				if(((u+v)/2)%2==1) O.add((u+v)/2);
				else E.add((u+v)/2);
			}
		}
		if(O.has+E.has==1)
		{
			for(int i=0;i<ans.size();i++) cout<<ans[i].fi<<" "<<ans[i].se<<"\n";
			return;
		}
	}
}
int construct_same(vector <int> vec)
{
	vector <int> v[2];
	v[0].clear(),v[1].clear();
	for(int i=0;i<vec.size();i++) v[(vec[i]%4)/2].pb(vec[i]);
	while(v[0].size()+v[1].size()>=2)
	{
		if(v[0].size()>=2)
		{
			int x=v[0][v[0].size()-1];
			v[0].pop_back();
			int y=v[0][v[0].size()-1];
			v[0].pop_back();
			cout<<x<<" "<<y<<"\n";
			x=(x+y)/2;
			v[(x%4)/2].pb(x);
		}
		else if(v[1].size()>=2)
		{
			int x=v[1][v[1].size()-1];
			v[1].pop_back();
			int y=v[1][v[1].size()-1];
			v[1].pop_back();
			cout<<x<<" "<<y<<"\n";
			x=(x+y)/2;
			v[(x%4)/2].pb(x);
		}
		else 
		{
			cout<<v[0][0]<<" "<<v[1][0]<<"\n";
			return (v[0][0]+v[1][0])/2;
		}
	}
	return (v[0].size()?v[0][0]:v[1][0]);
}
pii find_diff(vector <int> v,int i)
{
	int f1=0,f2=0;
	for(int j=0;j<v.size();j++)
	{
		if(v[j]&(1LL<<i)) f1=j;
		else f2=j;
	}
	return mp(f1,f2);
}
int n,a[2500005];
void solve()
{
	cin>>n;
	for(int i=1;i<=n;i++) cin>>a[i];
	vector <int> v[2];
	v[0].clear(),v[1].clear();
	for(int i=1;i<=n;i++) v[a[i]%2].pb(a[i]);
	if(v[0].size()==n) 
	{
		construct_same(v[0]);
		return;
	}
	if(v[1].size()==n)
	{
		construct_same(v[1]);
		return;
	}
	int min_d=inf;
	for(int i=1;i<60;i++)
	{
		int f1=0,f2=0;
		for(int j=0;j<v[0].size();j++)
		{
			if(v[0][j]&(1LL<<i)) f1=1;
			else f2=1;
		}
		if(f1&&f2)
		{
			min_d=i;
			break;
		} 
	}
//	cout<<v[0].size()<<" "<<min_d<<"\n";
	if(v[0].size()>=min_d+1)
	{
		for(int i=min_d;i>=2;i--)
		{
			pii t=find_diff(v[0],i);
			if(t.fi>t.se) swap(t.fi,t.se);
			int x=v[0][t.fi],y=v[0][t.se];
			cout<<x<<" "<<y<<"\n";
			v[0].erase(v[0].begin()+t.fi),v[0].erase(v[0].begin()+t.se-1);
			v[0].pb((x+y)/2);
		}
		pii t=find_diff(v[0],1);
		if(t.fi>t.se) swap(t.fi,t.se);
		int x=v[0][t.fi],y=v[0][t.se];
//		cout<<x<<" "<<y<<"\n";
		v[0].erase(v[0].begin()+t.fi),v[0].erase(v[0].begin()+t.se-1);
		int z=(v[0].size()?construct_same(v[0]):-1);
		int w=construct_same(v[1]);
		vector <int> vec;
		vec.clear();
		vec.pb(x),vec.pb(y),vec.pb(w);
		if(z!=-1) vec.pb(z);
		random_small(vec);
		return;
	}
	swap(v[0],v[1]);
	min_d=inf;
	for(int i=1;i<60;i++)
	{
		int f1=0,f2=0;
		for(int j=0;j<v[0].size();j++)
		{
			if(v[0][j]&(1LL<<i)) f1=1;
			else f2=1;
		}
		if(f1&&f2)
		{
			min_d=i;
			break;
		} 
	}
//	cout<<"... "<<v[0].size()<<" "<<min_d<<"\n";
	if(v[0].size()>=min_d+1)
	{
		for(int i=min_d;i>=2;i--)
		{
			pii t=find_diff(v[0],i);
			if(t.fi>t.se) swap(t.fi,t.se);
			int x=v[0][t.fi],y=v[0][t.se];
			cout<<x<<" "<<y<<"\n";
			v[0].erase(v[0].begin()+t.fi),v[0].erase(v[0].begin()+t.se-1);
			v[0].pb((x+y)/2);
		}
		pii t=find_diff(v[0],1);
		if(t.fi>t.se) swap(t.fi,t.se);
		int x=v[0][t.fi],y=v[0][t.se];
//		cout<<x<<" "<<y<<"\n";
		v[0].erase(v[0].begin()+t.fi),v[0].erase(v[0].begin()+t.se-1);
		int z=(v[0].size()?construct_same(v[0]):-1);
		int w=construct_same(v[1]);
		vector <int> vec;
		vec.clear();
		vec.pb(x),vec.pb(y),vec.pb(w);
		if(z!=-1) vec.pb(z);
		random_small(vec);
		return;
	}
	cout<<"-1\n";
}
signed main()
{
	freopen("meow.in","r",stdin);
	freopen("meow.out","w",stdout);
	ios::sync_with_stdio(0);
	cin.tie(0);
	int _=1;
	cin>>_;
	while(_--) solve();
	return 0;
}