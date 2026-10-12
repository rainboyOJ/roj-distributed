#include<bits/stdc++.h>
#define ll long long
using namespace std;

const int maxn = 510;
const int mod  = 998244353;
inline void add(int &a,const int &b){ a+=b;if(a>=mod)a-=mod; }
inline void sub(int &a,const int &b){ a-=b;if(a<0)a+=mod; }

int n;
int a[maxn],L[maxn],R[maxn];
int f[maxn][maxn],g1[maxn][maxn],g0[maxn][maxn];

int main()
{
	ios_base::sync_with_stdio(false);
	
	cin>>n;
	for(int i=1;i<=n;i++)
	{
		int x; cin>>x;
		a[x]=1;
	}
	
	for(int i=1;i<=500;i++) 
	{
		L[i]=L[i-1];
		if(a[i]) L[i]=i;
	}
	R[501]=501;
	for(int i=500;i>=1;i--)
	{
		R[i]=R[i+1];
		if(a[i]) R[i]=i;
	}
	
	int ans=0;
	for(int i=500;i>=1;i--) if(R[i]!=501)
	{
		{
			int top=L[500];
			int h=top-i;
			if(i>h)
			{
				add(f[i][h],1);
			}
		}
		for(int h=0;h<i;h++) 
		{
			add(g0[i][h],g0[i+1][h]);
			if(h>0) add(g1[i][h],g1[i+1][h-1]);
			
			add(f[i][h],g0[i][h]);
			add(f[i][h],g1[i][h]);
			
			add(ans,f[i][h]);
		//	cerr<<i<<"  "<<h<<" : "<<f[i][h]<<endl;
			
			int nexi=L[i-1];
			if(nexi>0)
			{
				//    i->j		j<=nexi
				
				// h' = nexi-j
				
				//1:  h'<=h  ---->  j>=nexi-h
				add(g0[nexi][h],f[i][h]);
				if(nexi-h>0) sub(g0[nexi-h][h],f[i][h]);
				//2:  h > h  ---->  j< nexi-h
				if(nexi-h>0) add(g1[nexi-h][h],f[i][h]);
			}
		}
	}
	
	add(ans,1);
	cout<<ans<<endl;
	
	return 0;
}

