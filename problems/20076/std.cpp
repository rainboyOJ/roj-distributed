#include<bits/stdc++.h>
#define LL long long
#define CPPname using namespace std
CPPname;
int tong[76],n,tamp;
int main(){
	cin>>n;
	for(int i=1;i<=n;i++){
		cin>>tamp;
		tong[tamp]++;// 使用桶进行储存 
	}
	tamp=0;//计算是第几大的 
	for(int i=75/* 题目中保证每个分数在 75 以下 */;i>=0/* 题目中保证每个分数在 0 以上 */;i--){
		if(tong[i]!=0)tamp++;
		if(tamp==3){
			cout<<i<<" "<<tong[i];
			return 0;
		} 
	}
	return 0;
}

