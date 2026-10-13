#include <bits/stdc++.h>
using namespace std ;

typedef long long LL ;

#define clr( a , x ) memset ( a , x , sizeof a )

const int MAXN = 42 ;
const int mod = 1e9 + 7 ;

char buf[1000000] ;
int len ;
int p[MAXN], c[MAXN] ;
int L[MAXN], R[MAXN], odd[MAXN], even[MAXN] ;
int dp[MAXN][MAXN][2] ;
pair < int, int > nxt[MAXN][MAXN][2] ;
int ans[MAXN], tmp[MAXN] ;
int rt[MAXN], col[MAXN] ;
int idx[MAXN] ;
int use[MAXN] ;
int n, m ;
int T ;

int F ( int x ) {
	if ( p[x] == x )
		return x ;
	int res = F ( p[x] ) ;
	c[x] ^= c[p[x]] ;
	return p[x] = res ;
}

int upd ( int x, int y, int o, int n ) {
	if ( dp[y][x][o] == 0 )
		return 0 ;
	int m = y - x ;
	for ( int i = x ; i <= y ; ++ i ) {
		tmp[i] = nxt[y][i][o].first ;
		o = nxt[y][i][o].second ;
	}
	return 1 ;
}

void up ( int ok ) {
	if ( !ok )
		return ;
	for ( int i = 1 ; i <= n ; ++ i ) {
		if ( tmp[i] > ans[i] )
			return ;
		if ( tmp[i] < ans[i] ) {
			for ( int j = 1 ; j <= n ; ++ j ) {
				ans[j] = tmp[j] ;
			}
			return ;
		}
	}
}

void add ( int x ) {
	if ( x / 10 )
		add ( x / 10 ) ;
	buf[len ++] = x % 10 + '0' ;
}

int main() {
	freopen("parity.in", "r", stdin);
	freopen("parity.out", "w", stdout);
	scanf ( "%d%d", &n, &m ) ;
	for ( int i = 0 ; i <= n ; ++ i ) {
		p[i] = i ;
		c[i] = 0 ;
		use[i] = 0 ;
	}
	for ( int i = 1 ; i <= n ; ++ i ) {
		scanf ( "%d%d", &L[i], &R[i] ) ;
		int tmp = R[i] - L[i] + 1 ;
		odd[i] = tmp / 2 + ( tmp % 2 == 1 && R[i] % 2 == 1 ) ;
		even[i] = tmp / 2 + ( tmp % 2 == 1 && R[i] % 2 == 0 ) ;
	}
	for ( int i = 1 ; i <= n ; ++ i ) {
		for ( int j = 1 ; j <= n + 1 ; ++ j ) {
			dp[i][j][0] = dp[i][j][1] = 0 ;
			nxt[i][j][0] = make_pair ( mod, mod ) ;
			nxt[i][j][1] = make_pair ( mod, mod ) ;
		}
	}
	for ( int i = 1 ; i <= n ; ++ i ) {
		dp[i][i + 1][0] = 1 ;
		for ( int j = i ; j >= 1 ; -- j ) {
			dp[i][j][0] = ( 1LL * dp[i][j + 1][1] * odd[j] + 1LL * dp[i][j + 1][0] * even[j] ) % mod ;
			dp[i][j][1] = ( 1LL * dp[i][j + 1][0] * odd[j] + 1LL * dp[i][j + 1][1] * even[j] ) % mod ;
		}
		for ( int j = 1 ; j <= i ; ++ j ) {
			if ( dp[i][j + 1][1] && odd[j] ) {
				nxt[i][j][0] = min ( nxt[i][j][0], make_pair ( L[j] + ( L[j] % 2 == 0 ), 1 ) ) ;
			}
			if ( dp[i][j + 1][0] && even[j] ) {
				nxt[i][j][0] = min ( nxt[i][j][0], make_pair ( L[j] + ( L[j] % 2 == 1 ), 0 ) ) ;
			}
			if ( dp[i][j + 1][0] && odd[j] ) {
				nxt[i][j][1] = min ( nxt[i][j][1], make_pair ( L[j] + ( L[j] % 2 == 0 ), 0 ) ) ;
			}
			if ( dp[i][j + 1][1] && even[j] ) {
				nxt[i][j][1] = min ( nxt[i][j][1], make_pair ( L[j] + ( L[j] % 2 == 1 ), 1 ) ) ;
			}
		}
	}
	int ok = 1 ;
	for ( int i = 1 ; i <= m ; ++ i ) {
		int u, v, w, x, y ;
		scanf ( "%d%d%d", &u, &v, &w ) ;
		-- u ;
		x = F ( u ) ;
		y = F ( v ) ;
		use[u] = use[v] = 1 ;
		if ( x != y ) {
			if ( x < y )
				swap ( x, y ) ;
			p[x] = y ;
			c[x] = ( c[u] - c[v] + 2 + w ) % 2 ;
		} else if ( ( c[u] ^ c[v] ) != w )
			ok = 0 ;
	}
	if ( !ok ) {
		buf[len ++] = '0' ;
		buf[len ++] = '\n' ;
		buf[len ++] = '-' ;
		buf[len ++] = '1' ;
		buf[len ++] = '\n' ;
		return 0;
	}
	int cnt = 0, tot = 0, uns = 0;
	for ( int i = 0 ; i <= n ; ++ i )
		if ( use[i] ) {
			if ( F ( i )  == i )
				rt[cnt ++] = i ;
			idx[tot ++] = i ;
		} else
			uns++;
	int res = 0, OK = 0 ;
	for ( int i = 1 ; i <= n ; ++ i ) {
		ans[i] = mod ;
	}
	for ( int s = 0 ; s < 1 << cnt ; ++ s ) {
		if ( cnt && rt[0] == 0 && s % 2 )
			continue ;
		col[0] = 0 ;
		for ( int i = 0 ; i < cnt ; ++ i ) {
			col[rt[i]] = s >> i & 1 ;
		}
		int ans = 1, j = 0, ok = 1 ;
		for ( int o = ( rt[0] == 0 ) ; o < tot ; ++ o ) {
			int i = idx[o], x = p[i] ;
			if ( x != i )
				col[i] = col[x] ^ c[x] ^ c[i] ;
			ans = 1LL * ans * dp[i][j + 1][col[j] ^ col[i]] % mod ;
			ok &= upd ( j + 1, i, col[j] ^ col[i], j ) ;
			if ( !ok )
				break ;
			j = i ;
		}
		if ( ok && j < n ) {
			ans = 1LL * ans * ( dp[n][j + 1][0] + dp[n][j + 1][1] ) % mod ;
			int a = upd ( j + 1, n, 0, j ) ;
			up ( ok && a ) ;
			int b = upd ( j + 1, n, 1, j ) ;
			up ( ok && b ) ;
			ok &= a | b ;
		} else
			up ( ok ) ;
		if ( ok )
			OK = 1 ;
		res = ( res + ans ) % mod ;
	}
	if ( !OK ) {
		buf[len ++] = '0' ;
		buf[len ++] = '\n' ;
		buf[len ++] = '-' ;
		buf[len ++] = '1' ;
		buf[len ++] = '\n' ;
	} else {
		add ( res ) ;
		buf[len ++] = '\n' ;
		for ( int i = 1 ; i <= n ; ++ i ) {
			add ( ans[i] ) ;
			buf[len ++] = i < n ? ' ' : '\n' ;
		}
	}
	buf[len] = 0;
	printf("%s", buf);
}
