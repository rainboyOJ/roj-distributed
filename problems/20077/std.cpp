#include<cstdio>
#include<queue>
#include<vector>
using namespace std;
const int R=1e5+10,dx[4]={1,-1,0,0},dy[4]={0,0,1,-1};
vector<char>e[R]; vector<bool>vis[R];
int main() {
  int r,c; scanf("%d %d",&r,&c);
  for(int i=0;i<r;i++) {
  	char ch;
  	for(int j=0;j<c;j++) {
  	  scanf(" %c",&ch);
  	  e[i].push_back(ch),vis[i].push_back(false);
	}
  }
  int a,b; scanf("%d %d",&a,&b);
  int sum=0; queue<pair<int,int> >q;
  q.push(make_pair(a,b)),vis[a][b]=true;
  while(!q.empty()) {
  	pair<int,int>p=q.front(); q.pop();
  	int x=p.first,y=p.second;
  	//printf("%d %d ",x,y);
  	if(e[x][y]=='S') sum++;
  	if(e[x][y]=='M') sum+=5;
  	if(e[x][y]=='L') sum+=10;
  	for(int i=0;i<4;i++) {
  	  int xx=x+dx[i],yy=y+dy[i];
  	  if(xx>=0&&xx<r&&yy>=0&&yy<c&&e[xx][yy]!='*'&&!vis[xx][yy])
		q.push(make_pair(xx,yy)),vis[xx][yy]=true;
	}
  }
  printf("%d",sum);
  return 0;
}
