#include <cassert>
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
int n,dirt;
struct Line
{
	int k,b;
};
struct SegTree
{
	int t[800015],tag[800015];
void pushdown(int id)
{
	if(tag[id])
	{
		t[id<<1]+=tag[id],t[id<<1|1]+=tag[id];
		tag[id<<1]+=tag[id],tag[id<<1|1]+=tag[id];
		tag[id]=0;
	}
}
void update_add(int id,int l,int r,int x,int y,int d)
{
	if(x<=l&&r<=y)
	{
		tag[id]+=d,t[id]+=d;
		return;
	}
	int mid=(l+r)>>1;
	pushdown(id);
	if(x<=mid) update_add(id<<1,l,mid,x,y,d);
	if(y>mid) update_add(id<<1|1,mid+1,r,x,y,d);
	t[id]=min(t[id<<1],t[id<<1|1]);
}
void update(int i,int x,int y,int tp)
{
	if(tp==0)
	{
		update_add(1,1,n,i,n,-x);
		update_add(1,1,n,i,n,y);
	}
	else
	{
		update_add(1,1,n,1,i,-x);
		update_add(1,1,n,1,i,y);
	}
}
}st;
struct Lichao
{
Line p[2000005];
int t[5000005];
int ls[5000005],rs[5000005];
int idx,tid;
void init()
{
	idx=0,tid=1;
	ls[1]=0,rs[1]=0,t[1]=0;
	p[0].k=1,p[0].b=-INF;
}
int add_line(int k,int b)
{
	p[++idx].k=k,p[idx].b=b;
	return idx;
}
int get_y(int id,int x)
{
	return p[id].k*x+p[id].b;
}
void update(int &id,int l,int r,int lid)
{
	if(!id) id=++tid,t[id]=0,ls[id]=rs[id]=0;
	int mid=(l+1000000+r+1000000)/2-1000000;
	if(get_y(lid,mid)>get_y(t[id],mid)) swap(lid,t[id]);
	if(get_y(lid,l)>get_y(t[id],l)) update(ls[id],l,mid,lid);
	if(get_y(lid,r)>get_y(t[id],r)) update(rs[id],mid+1,r,lid);	
}
void insert(int &id,int l,int r,int x,int y,int lid)
{
	if(!id) id=++tid,t[id]=0,ls[id]=rs[id]=0;
	if(x<=l&&r<=y)
	{
		update(id,l,r,lid);
		return;
	}
	int mid=(l+1000000+r+1000000)/2-1000000;
	if(x<=mid) insert(ls[id],l,mid,x,y,lid);
	if(y>mid) insert(rs[id],mid+1,r,x,y,lid);
}
int query(int id,int l,int r,int x)
{
	assert(l<=x&&x<=r);
	if(!id) return -INF;
	int mid=(l+r)/2;
	int res=get_y(t[id],x);
	if(l==r) return res;
	if(x<=mid) res=max(res,query(ls[id],l,mid,x));
	else res=max(res,query(rs[id],mid+1,r,x));
	return res;
}
}lt;
int A[200005];
int a[200005],b[200005],c[200005],d[200005],e[200005],f[200005],ps[200005],ss[200005],pspm[200005],pssm[200005];

vector <pii > stk;
vector <double > pnt;
double get(pii x,pii y)
{
	if(x.fi==y.fi) return (x.se>y.se?-1e18:1e18);
	return 1.0*(y.se-x.se)/(x.fi-y.fi);
}
void ins(pii li)
{
	if(!stk.size()) stk.pb(li),pnt.pb(-1e18);
	else
	{
		while(stk.size()>1&&get(li,stk.back())<pnt.back()) stk.pop_back(),pnt.pop_back();
		pnt.pb(get(li,stk.back())),stk.pb(li);
	}
}
double inter(pii l1,pii l2)
{
	return 1.0*(l2.se-l1.se)/(l1.fi-l2.fi);
}
int query(pii li)
{
	if(!stk.size()) return INF;
	pnt.pb(1e18);
	int L=0,R=pnt.size()-2,res=0;
	while(L<=R)
	{
		int mid=(L+R)>>1;
		double tmp=inter(stk[mid],li);
		if(pnt[mid]<=tmp&&tmp<=pnt[mid+1]) 
		{
			res=mid;
			break;
		}
		if(tmp>pnt[mid+1]) L=mid+1;
		else R=mid-1;
	}
	pnt.pop_back();
	return ceil(inter(stk[res],li));
}


pii divide(int l,int r)
{
	if(l>=r) return mp(-1,-1);
	int mid=(l+r)>>1;
	for(int i=mid+1,s=0;i<=r;i++) s+=A[i],a[i]=s;
	lt.init();
	int rt=1;
	for(int i=mid+1,s=0,sum=0;i<=r;i++)
	{
		s+=(i-mid)*A[i];
		sum+=A[i];
		int K=i-mid,B=s;
		B-=K*sum;
		int lid=lt.add_line(-K,-B);
		lt.insert(rt,-n,n,-n,n,lid);
		b[i]=lt.query(rt,-n,n,sum);
		b[i]=max(b[i],-(pssm[i+1]-ps[i]+s));
	}
	for(int i=mid,s=0,sum=0;i>=l;i--)
	{
		sum+=A[i],s+=sum;
		d[i]=s;
	}
	lt.init();
	
	stk.clear(),pnt.clear();
	for(int i=mid,sum=0,tag=0;i>=l;i--)
	{
		sum+=A[i],tag+=sum;
		int K=(i+1),B=sum-tag;
		ins(mp(-K,-B));
		e[i]=query(mp(-i,tag+ps[i-1]));
	}
	for(int i=mid;i>=l;i--) f[i]=ps[i-1];
	vector <array<int,4> > vec;
	vec.clear();
	for(int i=l;i<=mid;i++) if(pspm[i-1]>=0) vec.pb({e[i],0,i});
	for(int i=mid+1;i<=r;i++) vec.pb({a[i],1,i});
	sort(vec.begin(),vec.end());
	lt.init();
	for(int i=0;i<vec.size();i++)
	{
		int u=vec[i][2];
		if(vec[i][1]==0) 
		{
			int K=mid-u+1,B=d[u]+f[u];
			int lid=lt.add_line(K,B);
			lt.insert(rt,-n,n,-n,n,lid);
		}
		else
		{
			int tmp=lt.query(rt,-n,n,a[u]);
			if(tmp>=b[u])
			{
				int v=-1;
				for(int j=0;j<i;j++) if(vec[j][1]==0)
				{
					v=vec[j][2];
					int K=mid-v+1,B=d[v]+f[v];
					if(K*a[u]+B==tmp) break;
				}
				assert(v!=-1);
				return mp(v,u);
			}
		}
	}
	
	pii tmp=divide(l,mid);
	if(tmp.fi!=-1) return tmp;
	tmp=divide(mid+1,r);
	if(tmp.fi!=-1) return tmp;
	return mp(-1,-1);
}
vector <array<int,3> > chk()
{
	memset(st.t,0,sizeof(st.t));
	memset(st.tag,0,sizeof(st.tag));
	for(int i=1;i<=n;i++) st.update(i,0,A[i],0);
	for(int i=1,s=0;i<=n;i++)
	{
		s+=A[i];
		st.update(i,A[i],s,0);
		if(st.t[1]>=0)
		{
			vector <array<int,3> > vec;
			vec.pb({2,1,i});
			vec.pb({2,1,n});
			return vec;
		}
	}
	
	memset(st.t,0,sizeof(st.t));
	memset(st.tag,0,sizeof(st.tag));
	for(int i=1;i<=n;i++) st.update(i,0,A[i],1);
	for(int i=n,s=0;i>=1;i--)
	{
		s+=A[i];
		st.update(i,A[i],s,1);
		if(st.t[1]>=0)
		{
			vector <array<int,3> > vec;
			vec.pb({3,i,n});
			vec.pb({3,1,n});
			return vec;
		}
	}
	
	memset(pssm,0x3f,sizeof(pssm)),memset(pspm,0x3f,sizeof(pspm));
	for(int i=1;i<=n;i++) ps[i]=ps[i-1]+A[i],pspm[i]=pssm[i]=ps[i];
	for(int i=1;i<=n;i++) ss[i]=ss[i+1]+A[i];
	for(int i=2;i<=n;i++) pspm[i]=min(pspm[i-1],pspm[i]);
	for(int i=n-1;i>=1;i--) pssm[i]=min(pssm[i+1],pssm[i]);
	pii tmp=divide(1,n);
	vector <array<int,3> > vec;
	for(int i=0;i<100;i++) vec.pb({-1,-1,-1});
	if(tmp.fi==-1) return vec;
	vec.clear();
	vec.pb({3,tmp.fi,tmp.se}),vec.pb({2,1,n});
	return vec;
}
void solve()
{
	cin>>n>>dirt;
	for(int i=1;i<=n;i++) cin>>A[i];
	bool ok=1;
	for(int i=1;i<=n;i++) ok&=(A[i]>=0);
	if(ok) 
	{
		cout<<"0\n";
		return;
	}
	ok=1;
	for(int i=1,s=0;i<=n;i++) s+=A[i],ok&=(s>=0);
	if(ok)
	{
		cout<<"1\n";
		cout<<2<<" "<<1<<" "<<n<<"\n";
		return;
	}
	ok=1;
	for(int i=n,s=0;i>=1;i--) s+=A[i],ok&=(s>=0);
	if(ok)
	{
		cout<<"1\n";
		cout<<3<<" "<<1<<" "<<n<<"\n";
		return;
	}
	
	for(int i=1;i<=n;i++) A[i]*=-1;
	ok=1;
	for(int i=1;i<=n;i++) ok&=(A[i]>=0);
	if(ok) 
	{
		cout<<"1\n1\n";
		return;
	}
	ok=1;
	for(int i=1,s=0;i<=n;i++) s+=A[i],ok&=(s>=0);
	if(ok)
	{
		cout<<"2\n1\n";
		cout<<2<<" "<<1<<" "<<n<<"\n";
		return;
	}
	ok=1;
	for(int i=n,s=0;i>=1;i--) s+=A[i],ok&=(s>=0);
	if(ok)
	{
		cout<<"2\n1\n";
		cout<<3<<" "<<1<<" "<<n<<"\n";
		return;
	}
	for(int i=1;i<=n;i++) A[i]*=-1;
	vector <array<int,3> > v1=chk();
	reverse(A+1,A+1+n);
	vector <array<int,3> > v2=chk();
	for(int i=0;i<v2.size();i++) 
	{
		if(v2[i][0]==2) v2[i][0]=3;
		else if(v2[i][0]==3) v2[i][0]=2;
		v2[i][1]=n-v2[i][1]+1,v2[i][2]=n-v2[i][2]+1;
		swap(v2[i][1],v2[i][2]);
	}
	reverse(A+1,A+1+n);
	for(int i=1;i<=n;i++) A[i]*=-1;
	vector <array<int,3> > v3=chk();
	v3.insert(v3.begin(),{1,-1,-1});
	reverse(A+1,A+1+n);
	vector <array<int,3> > v4=chk();
	v4.insert(v4.begin(),{1,-1,-1});
	for(int i=0;i<v4.size();i++) 
	{
		if(v4[i][0]==2) v4[i][0]=3;
		else if(v4[i][0]==3) v4[i][0]=2;
		v4[i][1]=n-v4[i][1]+1,v4[i][2]=n-v4[i][2]+1;
		swap(v4[i][1],v4[i][2]);
	}
	vector <array<int,3> > ans;
	for(int i=0;i<100;i++) ans.pb({-1,-1,-1});
	if(v1.size()<ans.size()) ans=v1;
	if(v2.size()<ans.size()) ans=v2;
	if(v3.size()<ans.size()) ans=v3;
	if(v4.size()<ans.size()) ans=v4;
	cout<<ans.size()<<"\n";
	for(int i=0;i<ans.size();i++) 
	{
		cout<<ans[i][0];
		if(ans[i][0]!=1) cout<<" "<<ans[i][1]<<" "<<ans[i][2];
		cout<<"\n";
	}
}
signed main()
{
	freopen("presuffix.in","r",stdin);
	freopen("presuffix.out","w",stdout);
	ios::sync_with_stdio(0);
	cin.tie(0);
	int _=1;
//	cin>>_;
	while(_--) solve();
	return 0;
}