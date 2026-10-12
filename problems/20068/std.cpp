#include <bits/stdc++.h>

using namespace std;

const int N = 405;

int n, sx, sy, ex, ey;
char s[N];
bool a[N][N][N];
int f[N][N][N];
queue<array<int, 3> > q;
int dx[] = {0, -1, 0, 1, 0};
int dy[] = {1, 0, -1, 0, 0};

inline int to(int x, int d) { return (x + d + n) % n; }

inline bool is(int x, int y) {
	return x >= 0 && y >= 0 && x < n && y < n;
}

int main()
{
	
	scanf("%d%d%d%d%d", &n, &sx, &sy, &ex, &ey);
	sx--, sy--, ex--, ey--;
	for (int i = 0; i < n; i++) {
		scanf("%s", s);
		for (int j = 0; j < n; j++) {
			if (s[j] == '#') {
				for (int k = 0; k < n; k++) {
					a[k][i][j] = 1;
				}
			} 
			if (s[j] == 'U') {
				for (int k = 0; k < n; k++) {
					a[k][to(i, -k)][j] = 1;
				}
			}
			if (s[j] == 'D') {
				for (int k = 0; k < n; k++) {
					a[k][to(i, k)][j] = 1;
				}
			}
			if (s[j] == 'L') {
				for (int k = 0; k < n; k++) {
					a[k][i][to(j, -k)] = 1;
				}
			}
			if (s[j] == 'R') {
				for (int k = 0; k < n; k++) {
					a[k][i][to(j, k)] = 1;
				}
			}
		}
	}
	memset(f, -1, sizeof(f));
	f[0][sx][sy] = 0;
	q.push({0, sx, sy});
	while (!q.empty()) {
		auto now = q.front(); q.pop();
		int r = now[0], x = now[1], y = now[2];
//		printf("%d %d %d : %d\n", r, x + 1, y + 1, f[r][x][y]);
//		if (x == ex && y == ey) {
//			printf("%d\n", f[r][x][y]);
//			return 0;
//		}
		for (int i = 0; i < 5; i++) {
			int nr = (r + 1) % n, nx = x + dx[i], ny = y + dy[i];
			if (!is(nx, ny)) continue;
			if (a[r][nx][ny]) continue;
			if (nx == ex && ny == ey) {
				printf("%d\n", f[r][x][y] + 1);
				return 0;
			}
			if (a[r][nx][ny] || a[nr][nx][ny]) continue;
			if (~f[nr][nx][ny]) continue;
			f[nr][nx][ny] = f[r][x][y] + 1;
			q.push({nr, nx, ny});
		}
	}
	puts("-1");
	return 0;
}
