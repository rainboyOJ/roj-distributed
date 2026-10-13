#include <cstdio>
#include <queue>
#include <tuple>
#include <algorithm>
#define eps (1e-4)
#define mp std::make_tuple
#define ld double
using std::tuple;
using std::priority_queue;
const int N=105;
int n, m, sx, sy, tx, ty;
ld s, k, dis[N][N];
int a[N][N];
priority_queue<tuple<ld, int, int> > q;
inline void upt(int x, int y, ld f)
{
	if(a[x][y]||!x|!y||x>n||y>m||dis[x][y]<=f+eps) return;
	dis[x][y]=f;
	q.push(mp(-f, x, y));
}
void dij(void)
{
	for(int i=1; i<=n; ++i) for(int j=1; j<=m; ++j) dis[i][j]=1e9;
	dis[sx][sy]=0;
	q.push(mp(0, sx, sy));
	while(!q.empty())
	{
		auto t=q.top();
		q.pop();
		int x=std::get<1>(t), y=std::get<2>(t);
		if(-std::get<0>(t)!=dis[x][y]) continue;
		ld d=dis[x][y];
		upt(x, y-1, d+1);
		upt(x, y+1, d+1);
		upt(x-1, y, d+k);
		upt(x+1, y, d+k);
	}
}
bool chk(ld c)
{
	k=c;
	dij();
	return s<=dis[tx][ty]+eps;
}
int main()
{
	scanf("%d%d", &n, &m);
	scanf("%d%d%d%d", &sx, &sy, &tx, &ty);
	for(int i=1; i<=n; ++i) for(int j=1; j<=m; ++j) scanf("%d", a[i]+j);
	scanf("%lf", &s);
	ld l=0, r=s;
	while(r-l>eps)
	{
		ld mid=(l+r)/2;
		if(chk(mid)) r=mid;
		else l=mid;
	}
	printf("%.3lf\n", l+(5e-5));
	return 0;
}