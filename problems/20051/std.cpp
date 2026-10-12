#include<bits/stdc++.h>
using namespace std;
int n;
double a[100005];
int main(){
    freopen("village2.in","r",stdin);
    freopen("village2.out","w",stdout);
    cin>>n;
    for(int i=1;i<=n;i++)cin>>a[i];
    sort(a+1,a+n+1);
    double ans=2e9;
    for(int i=2;i<n;i++){
        ans=min(ans,(a[i+1]-a[i-1])/2);
    }
    printf("%.1f",ans);
}