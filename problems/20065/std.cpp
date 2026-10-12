#include <bits/stdc++.h>
#define rep(i,x,y) for(int i=x; i<=y; ++i)
#define repd(i,x,y) for(int i=x; i>=y; --i)
#define mid ((l + r) >> 1)
#define lch (rt << 1)
#define rch (rt << 1 | 1)

using namespace std;

void solve()
{
    int n, k;
    cin >> n >> k;
    //怎么快速求解一个数二进制下最低位为1对应的权值 
    if ((n & -n) <= k) cout << "Alice\n";
    else cout << "Bob\n";
}

int main()
{
	int x=17;
	cout<<(x&-x)<<endl;
	x=14;
	cout<<(x&-x)<<endl;
	x=10;
	cout<<(x&-x)<<endl;
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--)
        solve();

    return 0;
}
/*
k=1
双方每次都只能取一个石头
n的奇偶性
如果n是奇数，一定是Alice获胜
如果n是偶数，一定是Bob获胜
k=2
Alice第一轮有两种取石头的办法，分别是取1或2个
Alice什么时候第一轮会取一个
Alice取一个石头的时候，后续所有人都只能取一个石头
当n是奇数的时候，Alice第一轮会取一个，Alice获胜
n是偶数的时候，Alice第一轮一定会取2个
Bob可以取1个也可以取2个
Bob取一个的时候,n此时依然是偶数,Alice获胜
Bob取2个
当n是奇数的时候，Alice第一轮会取一个，Alice获胜
当n是偶数，双方每次都只会取2个,只需要判定n/2的奇偶性 
k更大的一些情况 
k=3
Alice第一轮有3种取法
1,2,3 
如果Alice第一轮取3个
Bob只能取1或3个
Alice只能取1或3个
每一轮Alice和Bob都只能取奇数个
假设n是奇数,Alice一定获胜  一定要减去奇数个奇数 
当n是偶数的时候，Bob一定获胜 
偶数个奇数 偶数 

k=4
n是奇数 Alice获胜
n/2是奇数 Alice获胜
n/2一定是偶数，n是4的倍数
第一轮Alice取了4个
第二轮Bob可以取1,2,4中的一个 -> Bob只能取4个
n/4是奇数，Alice获胜

k=5 -> n是奇数
k=6 -> n/2是奇数 Alice获胜
可以归纳证明
如果k=9
n是奇数
n/2是奇数
n/4是奇数
n/8是奇数 Alice 获胜
否则是Bob获胜
k=17
 
 




*/

