#include <map>
#include <cstdio>
#include <vector>
#include <algorithm>

using ll = long long;
const ll mod = 1E+9 + 7;
const int maxn = 1E+5 + 5;

inline ll fsp(ll a, ll b, ll res = 1) {
	for(a %= mod; b; a = a * a % mod, b >>= 1)
		b & 1 && (res = res * a % mod); return res;
}

int n, m, k, r;
namespace Sub0 {
	int b[2];
	inline void main() {
		for(int i = 1, x; i <= r; ++i)
			scanf("%*d%*d%d", &x), b[x] |= 1;
		printf("%d\n", 2 - b[0] - b[1]);
	}
}

namespace Sub1 {
	struct Point { int x, y, z; } p[maxn];

	std::vector<int> to[2][maxn << 1];

	int col[maxn << 1];
	inline bool DFS(int u, int c) {
		col[u] = c;
		for(int v : to[0][u]) {
			if(~col[v] && col[v] != c) return false;
			if(!~col[v] && !DFS(v, c)) return false;
		}

		for(int v : to[1][u]) {
			if(~col[v] && col[v] == c) return false;
			if(!~col[v] && !DFS(v, c ^ 1)) return false;
		}
		return true;
	}

	int totx, bucx[maxn];
	int toty, bucy[maxn];
	inline void main() {
		bucx[totx = 1] = 1;
		bucy[toty = 1] = 1;
		for(int i = 1; i <= r; ++i) {
			scanf("%d%d%d", &p[i].x, &p[i].y, &p[i].z);
			bucx[++totx] = p[i].x, bucy[++toty] = p[i].y;
		}

		std::sort(bucx + 1, bucx + totx + 1);
		totx = std::unique(bucx + 1, bucx + totx + 1) - bucx - 1;
		std::sort(bucy + 1, bucy + toty + 1);
		toty = std::unique(bucy + 1, bucy + toty + 1) - bucy - 1;

		for(int i = 1; i <= r; ++i) {
			p[i].x = std::lower_bound(bucx + 1, bucx + totx + 1, p[i].x) - bucx;
			p[i].y = std::lower_bound(bucy + 1, bucy + toty + 1, p[i].y) - bucy;
		}
		
		ll ans = 0;
		for(int o : { 0, 1 }) {
			for(int i = 1; i <= totx + toty; ++i) to[0][i].clear(), to[1][i].clear();

			to[0][1].push_back(totx + 1);
			to[0][totx + 1].push_back(1);
			for(int i = 1; i <= r; ++i) {
				int c = p[i].z ^ o ^ (bucx[p[i].x] - 1 & bucy[p[i].y] - 1 & 1);
				to[c][p[i].x].push_back(p[i].y + totx);
				to[c][p[i].y + totx].push_back(p[i].x);
			}

			std::fill(col, col + totx + toty + 1, -1);

			int cnt = 0;
			for(int i = 1; i <= totx + toty; ++i) if(!~col[i]) {
				if(!DFS(i, 1)) goto fail;
				++cnt;
			}
			(ans += fsp(2, n + m - totx - toty + cnt - 1)) %= mod;
			fail:;
		}
		printf("%lld\n", (ans + mod) % mod);
	}
}

namespace Sub2 {
	std::map<int, bool> M[2];

	bool b[2], f[2];
	inline void main() {
		for(int i = 1, x, y, z; i <= r; ++i) {
			scanf("%d%d%d", &x, &y, &z);
			if(M[0].count(x) && M[0][x] ^ (y & 1) ^ z) b[0] = 1;
			else M[0][x] = (y & 1) ^ z;
			if(M[1].count(y) && M[1][y] ^ (x & 1) ^ z) b[1] = 1;
			else M[1][y] = (x & 1) ^ z;

			f[(x + y & 1) ^ z] = 1;
		}

		ll ans = 0;
		if(!b[0]) (ans += fsp(2, n - M[0].size())) %= mod;
		if(!b[1]) (ans += fsp(2, m - M[1].size())) %= mod;
		(ans -= 2 - f[0] - f[1]) %= mod;
		printf("%lld\n", (ans + mod) % mod);
	}
}

int main() {
	scanf("%d%d%d%d", &n, &m, &k, &r);
	if(k == 0) Sub0::main();
	if(k == 1) Sub1::main();
	if(k == 2) Sub2::main();
}