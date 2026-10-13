#include <iostream>
#include <cstdio>
#include <algorithm>
#define ll long long
#define mod 1000000007
using namespace std;

int n;
ll l[1005], r[1005];

inline ll mpow ( ll a, ll b ) {
	ll ans = 1;
	for ( ; b; b >>= 1, a = a * a % mod )
		if ( b & 1 )
			ans = ans * a % mod;
	return ans;
}

int main ( ) {
	freopen("sequence.in", "r", stdin);
	freopen("sequence.out", "w", stdout);
	scanf ( "%d", &n );
	ll sum = 1, MI = 0, MA = 0;
	for ( int i = 1; i <= n; i ++ ) {
		scanf ( "%lld%lld", &l[i], &r[i] );
		sum = sum * ( r[i] - l[i] + 1 ) % mod;
		MI = max( l[i], MI );
		MA = max( MA, r[i] );
	}
	ll ans = 0;
	for ( ll h = MI; h <= MA; h ++ ) {
		ll sum1 = 1, sum2 = 1;
		for ( int i = 1; i <= n; i ++ ) {
			ll L = l[i], R = min ( h, r[i] );
			L = h - L + 1, R = h - R + 1;
			sum1 = ( L + R ) * ( L - R + 1 ) / 2 * sum1 % mod;
		}
		for ( int i = 1; i <= n; i ++ ) {
			ll L = l[i], R = min ( h - 1, r[i] );
			L = h - L + 1, R = h - R + 1;
			sum2 = ( L + R ) * ( L - R + 1 ) / 2 * sum2 % mod;
		}
		ans = ( ans + ( sum1 - sum2 + mod ) % mod ) % mod;
	}
	ans = ans * mpow( sum, mod - 2 ) % mod;
	printf ( "%lld\n", ans );
	return 0;
}