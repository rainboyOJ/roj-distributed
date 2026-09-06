#include <cstdio>
#include <map>

#define ll long long
#define N 500010

using namespace std;

inline ll rd();

ll n, m, p[N];
int a;

map <ll, int> M;

ll trans(ll x){
	ll t = (x - 1) / m, y = x - (ll)t * m;
	return (ll)t * m + (m - y + 1);
}

void Solve(){
	M.clear();
	scanf("%d %lld %lld\n", &a, &n, &m);
	for(int i = 1 ; i <= a ; i++){
		scanf("%lld", &p[i]);
		M[p[i]] = 1;
	}
	for(int i = 1 ; i <= a ; i++)
		if(!M[trans(p[i])]){
			puts("No");
			return;
		}
	puts("Yes");
}
int main(){
	int T; scanf("%d", &T);
	while(T--)
		Solve();
	return 0;
}
inline ll rd(){
	char c;
	bool flag = 0;
	while((c = getchar()) < '0' || c > '9')
	    if(c == '-') flag = 1;
	ll res = c - '0';
	while((c = getchar()) >= '0' && c <= '9')
	    res = (res << 3) + (res << 1) + c - '0';
	return flag ? -res : res;
}