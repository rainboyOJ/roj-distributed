#include <iostream>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <string>
#include <bitset>
#include <vector>
#include <set>
#include <map>
#include <queue>
#include <algorithm>
#include <sstream>
#include <stack>
#include <iomanip>
using namespace std;
#define pb push_back
#define mp make_pair
typedef pair<int, int> pii;
typedef long long ll;
typedef double ld;
typedef vector<int> vi;
#define fi first
#define se second
#define fe first

#define FO(x) {freopen(#x".in","r",stdin);freopen(#x".out","w",stdout);}


#define Edg int M=0,fst[SZ],vb[SZ],nxt[SZ];void ad_de(int a,int b){++M;nxt[M]=fst[a];fst[a]=M;vb[M]=b;}void adde(int a,int b){ad_de(a,b);ad_de(b,a);}


#define Edgc int M=0,fst[SZ],vb[SZ],nxt[SZ],vc[SZ];void ad_de(int a,int b,int c){++M;nxt[M]=fst[a];fst[a]=M;vb[M]=b;vc[M]=c;}void adde(int a,int b,int c){ad_de(a,b,c);ad_de(b,a,c);}
#define es(x,e) (int e=fst[x];e;e=nxt[e])
#define esb(x,e,b) (int e=fst[x],b=vb[e];e;e=nxt[e],b=vb[e])

#define VIZ {printf("digraph G{\n"); for(int i=1;i<=n;i++) for es(i,e) printf("%d->%d;\n",i,vb[e]); puts("}");}

#define VIZ2 {printf("graph G{\n"); for(int i=1;i<=n;i++) for es(i,e) if(vb[e]>=i)printf("%d--%d;\n",i,vb[e]); puts("}");}
#define SZ 666666
char S[SZ];
int sn;
int f[2][2][2][2][16][16];
const int MOD = 1000000007;
#define add(a,b) ((a)+=(b))%=MOD

int main() {
	freopen("binary.in", "r", stdin);
	freopen("binary.out", "w", stdout);
	scanf("%s", S + 1);
	sn = strlen(S + 1);
	f[0][0][0][0][0][0] = 1;
	for (int i = 1; i <= sn; ++i) {
		int c = i & 1, b = !c;
		memset(f[c], 0, sizeof f[c]);
		for (int j = 0; j < 2; ++j) {
			for (int s = 0; s < 2; ++s) {
				for (int r = 0; r < 2; ++r) {
					for (int k = 0; k < 16; ++k) {
						for (int g = 0; g < 16; ++g) {
							if (!f[b][j][s][r][k][g])
								continue;
							add(f[c][j][s][r][k][g],
							    f[b][j][s][r][k][g]);
							{
								int jj = j, ss = s, rr = r, kk = k;
								if (S[i] == '1')
									ss ^= 1;
								else
									jj ^= 1, rr ^= ss;
								if (rr & 1)
									kk |= 1 << (jj + jj + ss);
								int F = 0;
								for (int p = 0; p < 4; ++p)
									if (kk & (1 << p)) {
										int h = rr + 1 + (p % 2) * (jj + p / 2);
										h &= 1;
										if (h)
											F = 1;
									}
								int cb;
								if (!F)
									cb = 0;
								else
									cb = 1 << (jj + jj + ss);
								add(f[c][jj][ss][rr][kk][g | cb],
								    f[b][j][s][r][k][g]);
							}
						}
					}
				}
			}
		}
	}
	ll ans = 0;
	for (int j = 0; j < 2; ++j) {
		for (int s = 0; s < 2; ++s) {
			for (int r = 0; r < 2; ++r) {
				for (int k = 0; k < 16; ++k) {
					for (int g = 0; g < 16; ++g) {
						if (!f[sn & 1][j][s][r][k][g])
							continue;
						int F = 1e9;
						if (r & 1)
							F = min(F, 1);
						else {
							for (int p = 0; p < 4; ++p)
								if (k & (1 << p)) {
									int h = 1 + (p % 2) * (j + p / 2);
									h &= 1;
									if (h)
										F = min(F, 2);
								}
						}
						for (int p = 0; p < 4; ++p)
							if (g & (1 << p)) {
								int h = (p % 2) * (j + p / 2);
								h &= 1;
								if (h)
									F = min(F, 3);
							}
						if (F > 5e8)
							F = 0;
						ans += F * (ll)f[sn & 1][j][s][r][k][g] % MOD;
						ans %= MOD;
					}
				}
			}
		}
	}
	ans = (ans % MOD + MOD) % MOD;
	printf("%lld\n", ans);
}
