#include<bits/stdc++.h>
using namespace std;
#define ll unsigned int

unordered_map<ll,int>mp[(1<<6)];
int p[10];
char s[10];
int have,n,m;
long long ans;
void dfs(int pos,int val)
{
    if(pos>=m)
    {
        int has=0;
        for(int i=0;i<m;i++)
        {
            if(!(have&p[i]))
                continue;
            if((val&p[i]))
                has=has*31+s[i];
            else
                has=has*31+'?';
        }
        ans+=mp[have][has];
        return ;
    }
    if(!(have&p[pos]))
        dfs(pos+1,val);
    else
    {
        for(int i=0;i<=1;i++)
            dfs(pos+1,(val|(i==0?0:p[pos])));
    }
}
int main()
{
    p[0]=1;
    for(int i=1;i<=6;i++)
        p[i]=p[i-1]*2;
    scanf("%d%d",&n,&m);
    int maxn=(1<<m),has;
    for(int i=1;i<=n;i++)
    {
        scanf("%s",s);
        have=0;
        for(int j=0;j<m;j++)
            if(s[j]!='?')
                have|=p[j];
        dfs(0,0);
        for(int i=0;i<maxn;i++)
        {
            has=0;
            for(int j=0;j<m;j++)
            {
                if((i&p[j]))
                    has=has*31+s[j];
            }
            mp[i][has]++;
        }
    }
    printf("%lld\n",ans);
    return 0;
}