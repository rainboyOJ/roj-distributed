#include <cassert>
#include <bits/stdc++.h>

std::mt19937 hua(20041115);

const int N = 1005;

int n, m, sx, sy, tx, ty;
const int dx[5] = { 1, 0, -1, 0, 0x3f3f3f3f };
const int dy[5] = { 0, 1, 0, -1, 0x3f3f3f3f };
const char* dir = "RDLU"; // Polish character??
int st[N][N];
bool vis[N][N];

int get_id(int x, int y) {
	for (int i = 0; i < 4; ++i)
			if (dx[i] == x && dy[i] == y)
				return i;
	throw;
}
int parse_en(char ch) {
	// I don't understand Polish
	if (ch == 'R')
		return 0;
	if (ch == 'D')
		return 1;
	if (ch == 'L')
		return 2;
	if (ch == 'U')
		return 3;
	throw;
}
bool inside(int lx, int rx, int ly, int ry, int x, int y) {
	return lx <= x && x <= rx && ly <= y && y <= ry;
}
bool ok(int lx, int rx, int ly, int ry, int x, int y) {
	return inside(lx, rx, ly, ry, x, y) && !vis[x][y];
}

bool dfs(int lx, int rx, int ly, int ry, int sx, int sy, int tx, int ty, int steps) {
	if (sx == tx && sy == ty) {
		if (steps == 1)
			return true;
		return false;
	}
	if (steps == 1)
		return false;
	for (int o = 0; o < 4; ++o) {
		int nx = sx + dx[o], ny = sy + dy[o];
		if (!ok(lx, rx, ly, ry, nx, ny))
			continue;
		st[sx][sy] = o;
		vis[nx][ny] = true;
		if (dfs(lx, rx, ly, ry, nx, ny, tx, ty, steps - 1))
			return true;
		vis[nx][ny] = false;
	}
	return false;
}

int cur_x, cur_y;
void set_dir(int x1, int y1, int x2, int y2, bool visited = false) {
	//printf("set dir %d %d %d %d\n", x1, y1, x2, y2);
	assert(cur_x == x1);
	assert(cur_y == y1);
	st[x1][y1] = get_id(x2 - x1, y2 - y1);
	if (vis[x2][y2] != visited) {
		throw;
	}
	vis[x2][y2] = true;
	cur_x = x2, cur_y = y2;
}
void cancel(int x, int y) {
	if (!vis[x][y]) {
		throw;
	}
	int nx = x + dx[st[x][y]];
	int ny = y + dy[st[x][y]];
	vis[nx][ny] = false;
	st[x][y] = 0;
}
void move(int lx, int rx, int ly, int ry, int dx, int dy, bool mode) {
	/* mode:
			0: move one step
			1: keep moving
	*/
	//fprintf(stderr, "move %d %d %d %d %d %d %d\n", lx, rx, ly, ry, dx, dy, mode);
	//fprintf(stderr, "curx = %d, cury = %d\n", cur_x, cur_y);
	int o = get_id(dx, dy);
	if (mode == false) {
		set_dir(cur_x, cur_y, cur_x + dx, cur_y + dy);
	}
	else {
		while (ok(lx, rx, ly, ry, cur_x + dx, cur_y + dy)) {
			set_dir(cur_x, cur_y, cur_x + dx, cur_y + dy);
		}
	}
}

void solve(int lx, int rx, int ly, int ry, int sx, int sy, int tx, int ty) {
	if (rx - lx + 1 <= 6 && ry - ly + 1 <= 6) {
		//for (int cx = lx; cx <= rx; ++cx)
		//	for (int cy = ly; cy <= ry; ++cy)
		//		assert(!vis[cx][cy]);
		if (!dfs(lx, rx, ly, ry, sx, sy, tx, ty, (rx - lx + 1) * (ry - ly + 1))) {
			puts("NIE"); // gg
			exit(0);
		}

		return;
	}
	auto go = [&](int dx, int dy, bool mode) {
		move(lx, rx, ly, ry, dx, dy, mode);
	};
	auto gogo = [&](char ch, int len) {
		int o = parse_en(ch);
		assert(len >= -1);
		int total_steps = 0;
		if (len == -1) {
			while (ok(lx, rx, ly, ry, cur_x + dx[o], cur_y + dy[o])) {
				++total_steps;
				go(dx[o], dy[o], false);
			}
			return total_steps;
		}
		else {
			for (int i = 0; i < len; ++i) {
				go(dx[o], dy[o], false);
			}
			return len;
		}
	};
	auto extend_path = [&](std::string s) {
		bool mode = false;
		for (auto ch : s) {
			int o = parse_en(ch);
			go(dx[o], dy[o], mode);
			mode = !mode;
		}
	};
	auto remake = [&](int x, int y) {
		cancel(x, y);
		cur_x = x, cur_y = y;
	};
	auto bounded = [&](int lx, int rx, int ly, int ry) {
		return inside(lx, rx, ly, ry, sx, sy) 
			&& inside(lx, rx, ly, ry, tx, ty);
	};
	auto ensure = [&](int x0, int y0) {
		if (x0 != cur_x || y0 != cur_y) {
			// ��
			throw;
		}
	};
	auto ensure_R = [&](int x0, int x1, int y0, int y1) {
		if (!(x0 <= cur_x && cur_x <= x1 && y0 <= cur_y && cur_y <= y1)) {
			throw;
		}
	};
	auto validate_shrink = [&](int l, int r) {
		return r - l + 1 > 6;
	};
	if (validate_shrink(lx, rx) && bounded(lx + 2, rx, ly, ry)) {
		// Case 1A: Left Free
		solve(lx + 2, rx, ly, ry, sx, sy, tx, ty);
		bool ok = false;
		for (int j = ly; j <= ry; ++j) {
			if (dy[st[lx + 2][j]] == 1) {
				assert(j < ry);
				remake(lx + 2, j);
				extend_path("LULDRUR");
				ensure(lx + 2, j + 1);
				ok = true;
				break;
			}
			else if (dy[st[lx + 2][j]] == -1) {
				assert(j > ly);
				remake(lx + 2, j);
				extend_path("LDLURDR");
				ensure(lx + 2, j - 1);
				ok = true;
				break;
			}
		}
		assert(ok);
	}
	else if (validate_shrink(lx, rx) && bounded(lx, rx - 2, ly, ry)) {
		// Case 1B: Right Free
		solve(lx, rx - 2, ly, ry, sx, sy, tx, ty);
		bool ok = false;
		for (int j = ly; j <= ry; ++j) {
			if (dy[st[rx - 2][j]] == 1) {
				remake(rx - 2, j);
				extend_path("RURDLUL");
				ensure(rx - 2, j + 1);
				ok = true;
				break;
			}
			else if (dy[st[rx - 2][j]] == -1) {
				remake(rx - 2, j);
				extend_path("RDRULDL");
				ensure(rx - 2, j - 1);
				ok = true;
				break;
			}
		}
		assert(ok);
	}
	else if (validate_shrink(ly, ry) && bounded(lx, rx, ly + 2, ry)) {
		// Case 1C: Up Free
		solve(lx, rx, ly + 2, ry, sx, sy, tx, ty);
		bool ok = false;
		for (int j = lx; j <= rx; ++j) {
			if (dx[st[j][ly + 2]] == -1) {
				remake(j, ly + 2);
				extend_path("URULDRD");
				ensure(j - 1, ly + 2);
				ok = true;
				break;
			}
			else if (dx[st[j][ly + 2]] == 1) {
				remake(j, ly + 2);
				extend_path("ULURDLD");
				ensure(j + 1, ly + 2);
				ok = true;
				break;
			}
		}
		assert(ok);
	}
	else if (validate_shrink(ly, ry) && bounded(lx, rx, ly, ry - 2)) {
		// Case 1D: Down Free
		solve(lx, rx, ly, ry - 2, sx, sy, tx, ty);
		bool ok = false;
		for (int j = lx; j <= rx; ++j) {
			if (dx[st[j][ry - 2]] == -1) {
				remake(j, ry - 2);
				extend_path("DRDLURU");
				ensure(j - 1, ry - 2);
				ok = true;
				break;
			}
			else if (dx[st[j][ry - 2]] == 1) {
				remake(j, ry - 2);
				extend_path("DLDRULU");
				ensure(j + 1, ry - 2);
				ok = true;
				break;
			}
		}
		assert(ok);
	}
	// Case 2-5: keep moving until the length of each border <= 6
	else if (validate_shrink(lx, rx) && inside(lx, lx, ly, ry, sx, sy)) {
		// Case 2A: left bound
		// Note that (ry - ly + 1) >= 4
		cur_x = sx, cur_y = sy;
		if (sy == ry) {
			// Case 2AA
			gogo('U', -1);
			gogo('R', 1);
			gogo('D', -1);
			gogo('R', 1);
			ensure_R(lx + 2, rx, ly, ry);
			solve(lx + 2, rx, ly, ry, cur_x, cur_y, tx, ty);
		}
		else if (sy + 1 == ry) {
			// Case 2AB
			gogo('D', 1);
			gogo('R', 1);
			gogo('U', 2);
			gogo('L', 1);
			gogo('U', -1);
			gogo('R', 1);
			gogo('D', -1);
			gogo('R', 1);	
			ensure_R(lx + 2, rx, ly, ry);
			solve(lx + 2, rx, ly, ry, cur_x, cur_y, tx, ty);
		}
		else {
			// Case 2AC
			int len = gogo('U', -1);
			gogo('R', 1);
			gogo('D', len + 1);
			gogo('L', 1);
			gogo('D', -1);
			gogo('R', 1);
			gogo('U', -1);
			gogo('R', 1);
			ensure_R(lx + 2, rx, ly, ry);
			solve(lx + 2, rx, ly, ry, cur_x, cur_y, tx, ty);
		}
	}
	else if (validate_shrink(lx, rx) && inside(lx + 1, lx + 1, ly, ry, sx, sy)) {
		// Case 2B: left strip
		cur_x = sx, cur_y = sy;
		if (sy == ry) {
			// Case 2BA
			gogo('L', 1);
			gogo('U', -1);
			gogo('R', 1);
			gogo('D', -1);
			gogo('R', 1);
			ensure_R(lx + 2, rx, ly, ry);
			solve(lx + 2, rx, ly, ry, cur_x, cur_y, tx, ty);
		}
		else {
			// Case 2BB
			gogo('U', -1);
			gogo('L', 1);
			gogo('D', -1);
			gogo('R', 1);
			gogo('U', -1);
			gogo('R', 1);
			ensure_R(lx + 2, rx, ly, ry);
			solve(lx + 2, rx, ly, ry, cur_x, cur_y, tx, ty);
		}
	}
	else if (validate_shrink(lx, rx) && inside(rx, rx, ly, ry, sx, sy)) {
		// Case 3A: right bound
		cur_x = sx, cur_y = sy;
		if (sy == ry) {
			// Case 2AA
			gogo('U', -1);
			gogo('L', 1);
			gogo('D', -1);
			gogo('L', 1);
			ensure_R(lx, rx - 2, ly, ry);
			solve(lx, rx - 2, ly, ry, cur_x, cur_y, tx, ty);
		}
		else if (sy + 1 == ry) {
			// Case 2AB
			gogo('D', 1);
			gogo('L', 1);
			gogo('U', 2);
			gogo('R', 1);
			gogo('U', -1);
			gogo('L', 1);
			gogo('D', -1);
			gogo('L', 1);
			ensure_R(lx, rx - 2, ly, ry);
			solve(lx, rx - 2, ly, ry, cur_x, cur_y, tx, ty);
		}
		else {
			// Case 2AC
			int len = gogo('U', -1);
			gogo('L', 1);
			gogo('D', len + 1);
			gogo('R', 1);
			gogo('D', -1);
			gogo('L', 1);
			gogo('U', -1);
			gogo('L', 1);
			ensure_R(lx, rx - 2, ly, ry);
			solve(lx, rx - 2, ly, ry, cur_x, cur_y, tx, ty);
		}
	}	
	else if (validate_shrink(lx, rx) && inside(rx - 1, rx - 1, ly, ry, sx, sy)) {
		// Case 3B: right strip
		cur_x = sx, cur_y = sy;
		if (sy == ry) {
			// Case 3BA
			gogo('R', 1);
			gogo('U', -1);
			gogo('L', 1);
			gogo('D', -1);
			gogo('L', 1);
			ensure_R(lx, rx - 2, ly, ry);
			solve(lx, rx - 2, ly, ry, cur_x, cur_y, tx, ty);
		}
		else {
			// Case 3BB
			gogo('U', -1);
			gogo('R', 1);
			gogo('D', -1);
			gogo('L', 1);
			gogo('U', -1);
			gogo('L', 1);
			ensure_R(lx, rx - 2, ly, ry);
			solve(lx, rx - 2, ly, ry, cur_x, cur_y, tx, ty);
		}
	}
	else if (validate_shrink(ly, ry) && inside(lx, rx, ly, ly, sx, sy)) {
		// Case 4A: Up bound
		cur_x = sx, cur_y = sy;
		if (sx == rx) {
			// Case 4AA
			gogo('L', -1);
			gogo('D', 1);
			gogo('R', -1);
			gogo('D', 1);
			ensure_R(lx, rx, ly + 2, ry);
			solve(lx, rx, ly + 2, ry, cur_x, cur_y, tx, ty);
		}
		else if (sx + 1 == rx) {
			gogo('R', 1);
			gogo('D', 1);
			gogo('L', 2);
			gogo('U', 1);
			gogo('L', -1);
			gogo('D', 1);
			gogo('R', -1);
			gogo('D', 1);
			ensure_R(lx, rx, ly + 2, ry);
			solve(lx, rx, ly + 2, ry, cur_x, cur_y, tx, ty);
		}
		else {
			int steps = gogo('L', -1);
			gogo('D', 1);
			gogo('R', steps + 1);
			gogo('U', 1);
			gogo('R', -1);
			gogo('D', 1);
			gogo('L', -1);
			gogo('D', 1);
			ensure_R(lx, rx, ly + 2, ry);
			solve(lx, rx, ly + 2, ry, cur_x, cur_y, tx, ty);
		}
	}
	else if (validate_shrink(ly, ry) && inside(lx, rx, ly + 1, ly + 1, sx, sy)) {
		// Case 4B: Up strip
		cur_x = sx, cur_y = sy;
		if (sx == rx) {
			gogo('U', 1);
			gogo('L', -1);
			gogo('D', 1);
			gogo('R', -1);
			gogo('D', 1);
			ensure_R(lx, rx, ly + 2, ry);
			solve(lx, rx, ly + 2, ry, cur_x, cur_y, tx, ty);
		}
		else {
			gogo('L', -1);
			gogo('U', 1);
			gogo('R', -1);
			gogo('D', 1);
			gogo('L', -1);
			gogo('D', 1);
			ensure_R(lx, rx, ly + 2, ry);
			solve(lx, rx, ly + 2, ry, cur_x, cur_y, tx, ty);
		}
	}
	else if (validate_shrink(ly, ry) && inside(lx, rx, ry, ry, sx, sy)) {
		// Case 5A: Down bound
		cur_x = sx, cur_y = sy;
		if (sx == rx) {
			// Case 5A
			gogo('L', -1);
			gogo('U', 1);
			gogo('R', -1);
			gogo('U', 1);
			ensure_R(lx, rx, ly, ry - 2);
			solve(lx, rx, ly, ry - 2, cur_x, cur_y, tx, ty);
		}
		else if (sx + 1 == rx) {
			gogo('R', 1);
			gogo('U', 1);
			gogo('L', 2);
			gogo('D', 1);
			gogo('L', -1);
			gogo('U', 1);
			gogo('R', -1);
			gogo('U', 1);
			ensure_R(lx, rx, ly, ry - 2);
			solve(lx, rx, ly, ry - 2, cur_x, cur_y, tx, ty);
		}
		else {
			int steps = gogo('L', -1);
			gogo('U', 1);
			gogo('R', steps + 1);
			gogo('D', 1);
			gogo('R', -1);
			gogo('U', 1);
			gogo('L', -1);
			gogo('U', 1);
			ensure_R(lx, rx, ly, ry - 2);
			solve(lx, rx, ly, ry - 2, cur_x, cur_y, tx, ty);
		}
	}
	else if (validate_shrink(ly, ry) && inside(lx, rx, ry - 1, ry - 1, sx, sy)) {
		// Case 4B: Up strip
		cur_x = sx, cur_y = sy;
		if (sx == rx) {
			gogo('D', 1);
			gogo('L', -1);
			gogo('U', 1);
			gogo('R', -1);
			gogo('U', 1);
			ensure_R(lx, rx, ly, ry - 2);
			solve(lx, rx, ly, ry - 2, cur_x, cur_y, tx, ty);
		}
		else {
			gogo('L', -1);
			gogo('D', 1);
			gogo('R', -1);
			gogo('U', 1);
			gogo('L', -1);
			gogo('U', 1);
			ensure_R(lx, rx, ly, ry - 2);
			solve(lx, rx, ly, ry - 2, cur_x, cur_y, tx, ty);
		}
	}
	else {
		puts("TBD");
		exit(0);
	}
}

void check_NIE() {
	int steps = n * m - 1;
	int parity = (sx ^ sy) ^ (tx ^ ty);
	if ((steps & 1) != (parity & 1)) {
		fprintf(stderr, "gg1\n");
		puts("NIE");
		exit(0);
	}
	if (steps % 2 == 0) {
		if ((sx ^ sy) & 1) {
		fprintf(stderr, "gg2\n");
			puts("NIE");
			exit(0);
		}
	}
}

void construct_solution() {
	while (sx != tx || sy != ty) {
		int o = st[sx][sy];
		putchar(dir[o]);
		sx += dx[o];
		sy += dy[o];
	}
}

int main() {
	std::ios::sync_with_stdio(false);
	std::cin >> n >> m >> sx >> sy >> tx >> ty;
	check_NIE();
	vis[sx][sy] = 1;
	st[tx][ty] = 4;
	solve(1, n, 1, m, sx, sy, tx, ty);
	construct_solution();
}