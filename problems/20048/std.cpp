#include<bits/stdc++.h>
using namespace std;

typedef unsigned long long ull;
typedef long long ll;
typedef long double db;
typedef pair<int,int> pii;
typedef pair<ll,ll> pll;
#define fi first
#define se second


const int N = 1e5+5;

int n,a[N],b[N],f[N],x;
signed main(){
    ios::sync_with_stdio(false); cin.tie(0u); cout.tie(0u);
	cin >> n;
    memset(f,0x3f3f3f3f,sizeof(f));
	for (int i = 1;i <= n; i++){
        cin >> x;
        a[x] = i;
    } 
	for (int i = 1;i <= n; i++){
        cin >> x;
        b[n-i+1] = a[x];
    }
	for (int i = 1; i <= n; i++) f[lower_bound(f+1,f+n+1,b[i])-f] = b[i];
    cout << lower_bound(f+1, f+n+1, f[0])-f-1 << endl;
    return 0;
}