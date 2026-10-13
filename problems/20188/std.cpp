#include<bits/stdc++.h>
using namespace std;
const int mod=998244353;
int n;
string s;
stack<int>st;
int cnt=0;
char c[500010];
bool leaf[500010];
int L[500010],R[500010]; // à¨o? 
int son[500010][2]; 
int num[500010],id[500010];
int build(int l,int r){
	if(R[l]==r)return build(l+1,r-1);
	if(l==r){
		leaf[cnt]=true;
		id[cnt]=num[l];
		return cnt++;
	}
	if(r-l+1==3){
		int a=build(l,l),b=build(r,r);
		son[cnt][0]=a;son[cnt][1]=b;
		c[cnt]=s[l+1];
		return cnt++;
	}
	int pos=-1;
	for(int i=l;i<=r;i++){
		if(s[i]=='('){
			pos=i;
			break;
		}
	}
	if(pos==l){
		int a=build(pos+1,R[pos]-1),b=build(R[pos]+2,r);
		son[cnt][0]=a;son[cnt][1]=b;
		c[cnt]=s[R[pos]+1];
		return cnt++;
	}
	if(R[pos]==r){
		int a=build(l,pos-2),b=build(pos+1,R[pos]-1);
		son[cnt][0]=a;son[cnt][1]=b;
		c[cnt]=s[pos-1];
		return cnt++;
	}
}
inline void upd(int &x,int y){x=(x+y)%mod;}
int dp[500010][2];
void dfs(int x){
	if(leaf[x]){
		dp[x][0]=dp[x][1]=1;
		return;
	}
	int a=son[x][0],b=son[x][1];
	dfs(a);
	dfs(b);
	for(int i=0;i<2;i++)for(int j=0;j<2;j++){
		if(c[x]=='|')upd(dp[x][i|j],1ll*dp[a][i]*dp[b][j]%mod);
		if(c[x]=='&')upd(dp[x][i&j],1ll*dp[a][i]*dp[b][j]%mod);
		if(c[x]=='^')upd(dp[x][i^j],1ll*dp[a][i]*dp[b][j]%mod);
	}
}
int ans[500010];
int f[500010];
void dfs2(int x){
	if(leaf[x]){
		ans[id[x]]=f[x];
		return;
	}
	int a=son[x][0],b=son[x][1];
	for(int i=0;i<2;i++){
		if(c[x]=='|'){
			if((i|0)!=(i|1)){
				upd(f[a],1ll*f[x]*dp[b][i]%mod);
				upd(f[b],1ll*f[x]*dp[a][i]%mod);
			}
		}
		if(c[x]=='&'){
			if((i&0)!=(i&1)){
				upd(f[a],1ll*f[x]*dp[b][i]%mod);
				upd(f[b],1ll*f[x]*dp[a][i]%mod);
			}
		}
		if(c[x]=='^'){
			if((i^0)!=(i^1)){
				upd(f[a],1ll*f[x]*dp[b][i]%mod);
				upd(f[b],1ll*f[x]*dp[a][i]%mod);
			}
		}
	}
	dfs2(a);
	dfs2(b);
}
inline int ksm(int x,int k){
	if(k==0)return 1;
	int res=ksm(x,k/2);
	res=1ll*res*res%mod;
	if(k&1)res=1ll*res*x%mod;
	return res;
} 
int main(){
	freopen("binary.in","r",stdin);
	freopen("binary.out","w",stdout);
	ios::sync_with_stdio(false);cin.tie(0);cout.tie(0);
	cin>>n>>s;
	if(n==1){
		cout<<"1\n";
		return 0;
	}
	for(int i=0;i<(int)s.size();i++)if(s[i]=='x')num[i]=cnt++;
	cnt=0;
	memset(L,-1,sizeof(L));
	memset(R,-1,sizeof(R));
	for(int i=0;i<(int)s.size();i++){	
		if(s[i]=='(')st.push(i);
		else if(s[i]==')'){
			R[st.top()]=i;
			L[i]=st.top();
			st.pop();
		}
	}
	memset(son,-1,sizeof(son));
	int r=build(0,(int)s.size()-1);
	dfs(r);
	f[r]=1;
	dfs2(r);
	int tot=ksm(2,n-1);
	for(int i=0;i<n;i++){
		int res=1ll*ans[i]*ksm(tot,mod-2)%mod;
		cout<<res<<"\n";
	}
	return 0;
}