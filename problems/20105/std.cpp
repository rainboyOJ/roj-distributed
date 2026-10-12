#include<cstdio>
#include<cstring>
using namespace std;
const int N=1000005;
int main(){
	int T;
	scanf("%d",&T);
	while(T--){
		char buf[N],tmp[N],res[N];
		scanf("%s",buf+1);
		int len=strlen(buf+1),p=0;
		for(int i=1;i<=len;++i)
			if(buf[i]!='a')tmp[++p]=buf[i];
		if(p==0){
			puts(buf+1);
			continue;
		}
		if(p&1){
			puts("No solution!");
			continue;
		}
		bool ok=1;
		for(int i=1,j=p/2+1;j<=p;++i,++j)
			if(tmp[i]!=tmp[j]){
				puts("No solution!");
				ok=0;
				break;
			}
		if(ok){
			int cnt=0,q=0,r=0;
			for(int i=1;i<=len;++i){
				if(buf[i]!='a')++cnt;
				if(cnt==p/2+1){
					for(int j=i;j<=len;++j)
						if(buf[j]=='a'){
							ok=0;
							break;
						}
					break;
				}
				res[++q]=buf[i];
			}
			if(ok){
				for(int i=1;i<=q;++i)putchar(res[i]);
				putchar('\n');
			}
			else puts("No solution!");
		}
	}
}