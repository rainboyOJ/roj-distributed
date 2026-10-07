---
title: 一本通 · 基础算法
description: 《信息学奥赛一本通（C++版）》基础算法篇：167 题，本站收录 167（100%）。
tags: [一本通, 教材配套, 刷题计划, 基础算法]
order: 2
items: 167
covered: 167
source: https://ybt.ssoier.cn/index.php
---

按《信息学奥赛一本通（C++版）》在线题库 [ybt.ssoier.cn](https://ybt.ssoier.cn/index.php) 左侧「题库全部题目分类索引」整理的 **基础算法篇**，可对照原书顺序刷题。

## 怎么用这份单子

- **一本通题号** 链接到一本通原题页；**ROJ 收录** 列是站内链接，在本站点开直接看题面；
- ROJ 列为 `—` 表示 ROJ 暂未收录这道题（仍可去一本通原站做）；
- 括号里标注「ROJ 题名」的，表示 ROJ 侧题目名称与一本通不同（多为改名/换译），题面是同一道题；
- **附录 A** 列出 ROJ 中『同题不同编号』的情况，分「已核对」「待核对」两档可信度；
- 一本通题目单共 5 篇（C++编程语言 / 基础算法 / 数据结构基础 / 算法提高篇 / 高手训练篇），可在[题目单列表](/problem-sets)里切换；勾选进度在站内按题号全局共享，跨篇不会丢；
- 在 GitHub 上阅读时，`/problem/…` 是站内路径，需补上 `https://roj.ac.cn` 前缀才能点开。

<!-- ybt:generated:start -->

## 本篇概览

本篇 167 题，本站收录 167（100%）；一本通题目单共 5 篇、895 题。

## 目录

- [第一章 高精度计算](#sec-1)
- [第二章 数据排序](#sec-2)
- [第三章 递推算法](#sec-3)
- [第四章 递归算法](#sec-4)
- [第五章 搜索与回溯算法](#sec-5)
- [第六章 贪心算法](#sec-6)
- [第七章 分治算法](#sec-7)
- [第八章 广度优先搜索算](#sec-8)
- [第九章 动态规划](#sec-9)
  - [第一节 动态规划的基本模型](#sec-10)
  - [第二节 背包问题](#sec-11)
  - [第三节 动态规划经典题目](#sec-12)
- [附录 A：同题异号对照](#appendix-a)

<a id="sec-0"></a>
## 基础算法

<a id="sec-1"></a>
### 第一章 高精度计算

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [2127](https://ybt.ssoier.cn/problem_show.php?pid=2127) | 【例1.2】高精度加法 | [ROJ 2127](/problem/2127) |
| 2 | [1307](https://ybt.ssoier.cn/problem_show.php?pid=1307) | 【例1.3】高精度乘法 | [ROJ 1307](/problem/1307) |
| 3 | [1308](https://ybt.ssoier.cn/problem_show.php?pid=1308) | 【例1.5】高精除 | [ROJ 1308](/problem/1308) |
| 4 | [1309](https://ybt.ssoier.cn/problem_show.php?pid=1309) | 【例1.6】回文数(Noip1999) | [ROJ 1309](/problem/1309) |
| 5 | [1168](https://ybt.ssoier.cn/problem_show.php?pid=1168) | 大整数加法 | [ROJ 1168](/problem/1168) |
| 6 | [1169](https://ybt.ssoier.cn/problem_show.php?pid=1169) | 大整数减法 | [ROJ 1169](/problem/1169) |
| 7 | [1170](https://ybt.ssoier.cn/problem_show.php?pid=1170) | 计算2的N次方 | [ROJ 1170](/problem/1170) |
| 8 | [1171](https://ybt.ssoier.cn/problem_show.php?pid=1171) | 大整数的因子 | [ROJ 1171](/problem/1171) |
| 9 | [1172](https://ybt.ssoier.cn/problem_show.php?pid=1172) | 求10000以内n的阶乘 | [ROJ 1172](/problem/1172) |
| 10 | [1173](https://ybt.ssoier.cn/problem_show.php?pid=1173) | 阶乘和 | [ROJ 1173](/problem/1173) |
| 11 | [1174](https://ybt.ssoier.cn/problem_show.php?pid=1174) | 大整数乘法 | [ROJ 1174](/problem/1174) |
| 12 | [1175](https://ybt.ssoier.cn/problem_show.php?pid=1175) | 除以13 | [ROJ 1175](/problem/1175) |
| 13 | [2128](https://ybt.ssoier.cn/problem_show.php?pid=2128) | 高精度乘法（II） | [ROJ 2128](/problem/2128) |

<a id="sec-2"></a>
### 第二章 数据排序

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1310](https://ybt.ssoier.cn/problem_show.php?pid=1310) | 【例2.2】车厢重组 | [ROJ 1310](/problem/1310) |
| 2 | [1311](https://ybt.ssoier.cn/problem_show.php?pid=1311) | 【例2.5】求逆序对 | [ROJ 1311](/problem/1311) |
| 3 | [1176](https://ybt.ssoier.cn/problem_show.php?pid=1176) | 谁考了第k名 | [ROJ 1176](/problem/1176) |
| 4 | [1177](https://ybt.ssoier.cn/problem_show.php?pid=1177) | 奇数单增序列 | [ROJ 1177](/problem/1177) |
| 5 | [1178](https://ybt.ssoier.cn/problem_show.php?pid=1178) | 成绩排序 | [ROJ 1178](/problem/1178) |
| 6 | [1179](https://ybt.ssoier.cn/problem_show.php?pid=1179) | 奖学金 | [ROJ 1179](/problem/1179) |
| 7 | [1180](https://ybt.ssoier.cn/problem_show.php?pid=1180) | 分数线划定 | [ROJ 1180](/problem/1180) |
| 8 | [1181](https://ybt.ssoier.cn/problem_show.php?pid=1181) | 整数奇偶排序 | [ROJ 1181](/problem/1181) |
| 9 | [1182](https://ybt.ssoier.cn/problem_show.php?pid=1182) | 合影效果 | [ROJ 1182](/problem/1182) |
| 10 | [1183](https://ybt.ssoier.cn/problem_show.php?pid=1183) | 病人排队 | [ROJ 1183](/problem/1183) |
| 11 | [1184](https://ybt.ssoier.cn/problem_show.php?pid=1184) | 明明的随机数 | [ROJ 1184](/problem/1184) |
| 12 | [1185](https://ybt.ssoier.cn/problem_show.php?pid=1185) | 单词排序 | [ROJ 1185](/problem/1185) |
| 13 | [1186](https://ybt.ssoier.cn/problem_show.php?pid=1186) | 出现次数超过一半的数 | [ROJ 1186](/problem/1186) |
| 14 | [1187](https://ybt.ssoier.cn/problem_show.php?pid=1187) | 统计字符数 | [ROJ 1187](/problem/1187) |

<a id="sec-3"></a>
### 第三章 递推算法

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1312](https://ybt.ssoier.cn/problem_show.php?pid=1312) | 【例3.4】昆虫繁殖 | [ROJ 1312](/problem/1312) |
| 2 | [1313](https://ybt.ssoier.cn/problem_show.php?pid=1313) | 【例3.5】位数问题 | [ROJ 1313](/problem/1313) |
| 3 | [1314](https://ybt.ssoier.cn/problem_show.php?pid=1314) | 【例3.6】过河卒(Noip2002) | [ROJ 1314](/problem/1314) |
| 4 | [1188](https://ybt.ssoier.cn/problem_show.php?pid=1188) | 菲波那契数列(2) | [ROJ 1188](/problem/1188) |
| 5 | [1189](https://ybt.ssoier.cn/problem_show.php?pid=1189) | Pell数列 | [ROJ 1189](/problem/1189) |
| 6 | [1190](https://ybt.ssoier.cn/problem_show.php?pid=1190) | 上台阶 | [ROJ 1190](/problem/1190) |
| 7 | [1191](https://ybt.ssoier.cn/problem_show.php?pid=1191) | 流感传染 | [ROJ 1191](/problem/1191) |
| 8 | [1192](https://ybt.ssoier.cn/problem_show.php?pid=1192) | 放苹果 | [ROJ 1192](/problem/1192) |
| 9 | [1193](https://ybt.ssoier.cn/problem_show.php?pid=1193) | 吃糖果 | [ROJ 1193](/problem/1193) |
| 10 | [1194](https://ybt.ssoier.cn/problem_show.php?pid=1194) | 移动路线 | [ROJ 1194](/problem/1194) |
| 11 | [1195](https://ybt.ssoier.cn/problem_show.php?pid=1195) | 判断整除 | [ROJ 1195](/problem/1195) |
| 12 | [1196](https://ybt.ssoier.cn/problem_show.php?pid=1196) | 踩方格 | [ROJ 1196](/problem/1196) |
| 13 | [1197](https://ybt.ssoier.cn/problem_show.php?pid=1197) | 山区建小学 | [ROJ 1197](/problem/1197) |

<a id="sec-4"></a>
### 第四章 递归算法

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1315](https://ybt.ssoier.cn/problem_show.php?pid=1315) | 【例4.5】集合的划分 | [ROJ 1315](/problem/1315) |
| 2 | [1316](https://ybt.ssoier.cn/problem_show.php?pid=1316) | 【例4.6】数的计数(Noip2001) | [ROJ 1316](/problem/1316) |
| 3 | [1198](https://ybt.ssoier.cn/problem_show.php?pid=1198) | 逆波兰表达式 | [ROJ 1198](/problem/1198) |
| 4 | [1199](https://ybt.ssoier.cn/problem_show.php?pid=1199) | 全排列 | [ROJ 1199](/problem/1199) |
| 5 | [1200](https://ybt.ssoier.cn/problem_show.php?pid=1200) | 分解因数 | [ROJ 1200](/problem/1200) |
| 6 | [1201](https://ybt.ssoier.cn/problem_show.php?pid=1201) | 菲波那契数列 | [ROJ 1201](/problem/1201) |
| 7 | [1202](https://ybt.ssoier.cn/problem_show.php?pid=1202) | Pell数列 | [ROJ 1202](/problem/1202) |
| 8 | [1203](https://ybt.ssoier.cn/problem_show.php?pid=1203) | 扩号匹配问题 | [ROJ 1203](/problem/1203) |
| 9 | [1204](https://ybt.ssoier.cn/problem_show.php?pid=1204) | 爬楼梯 | [ROJ 1204](/problem/1204) |
| 10 | [1205](https://ybt.ssoier.cn/problem_show.php?pid=1205) | 汉诺塔问题 | [ROJ 1205](/problem/1205) |
| 11 | [1206](https://ybt.ssoier.cn/problem_show.php?pid=1206) | 放苹果 | [ROJ 1206](/problem/1206) |
| 12 | [1207](https://ybt.ssoier.cn/problem_show.php?pid=1207) | 求最大公约数问题 | [ROJ 1207](/problem/1207) |
| 13 | [1208](https://ybt.ssoier.cn/problem_show.php?pid=1208) | 2的幂次方表示 | [ROJ 1208](/problem/1208) |
| 14 | [1209](https://ybt.ssoier.cn/problem_show.php?pid=1209) | 分数求和 | [ROJ 1209](/problem/1209) |
| 15 | [1210](https://ybt.ssoier.cn/problem_show.php?pid=1210) | 因子分解 | [ROJ 1210](/problem/1210) |
| 16 | [1211](https://ybt.ssoier.cn/problem_show.php?pid=1211) | 判断元素是否存在 | [ROJ 1211](/problem/1211) |

<a id="sec-5"></a>
### 第五章 搜索与回溯算法

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [2110](https://ybt.ssoier.cn/problem_show.php?pid=2110) | 【例5.1】素数环 | [ROJ 2110](/problem/2110) |
| 2 | [1317](https://ybt.ssoier.cn/problem_show.php?pid=1317) | 【例5.2】组合的输出 | [ROJ 1317](/problem/1317) |
| 3 | [1318](https://ybt.ssoier.cn/problem_show.php?pid=1318) | 【例5.3】自然数的拆分 | [ROJ 1318](/problem/1318) |
| 4 | [1212](https://ybt.ssoier.cn/problem_show.php?pid=1212) | LETTERS | [ROJ 1212](/problem/1212) |
| 5 | [1213](https://ybt.ssoier.cn/problem_show.php?pid=1213) | 八皇后问题 | [ROJ 1213](/problem/1213) |
| 6 | [1214](https://ybt.ssoier.cn/problem_show.php?pid=1214) | 八皇后 | [ROJ 1214](/problem/1214) |
| 7 | [1215](https://ybt.ssoier.cn/problem_show.php?pid=1215) | 迷宫 | [ROJ 1215](/problem/1215) |
| 8 | [1216](https://ybt.ssoier.cn/problem_show.php?pid=1216) | 红与黑 | [ROJ 1216](/problem/1216) |
| 9 | [1217](https://ybt.ssoier.cn/problem_show.php?pid=1217) | 棋盘问题 | [ROJ 1217](/problem/1217) |
| 10 | [1218](https://ybt.ssoier.cn/problem_show.php?pid=1218) | 取石子游戏 | [ROJ 1218](/problem/1218) |
| 11 | [1219](https://ybt.ssoier.cn/problem_show.php?pid=1219) | 马走日 | [ROJ 1219](/problem/1219) |
| 12 | [1220](https://ybt.ssoier.cn/problem_show.php?pid=1220) | 单词接龙 | [ROJ 1220](/problem/1220) |
| 13 | [1221](https://ybt.ssoier.cn/problem_show.php?pid=1221) | 分成互质组 | [ROJ 1221](/problem/1221) |
| 14 | [1222](https://ybt.ssoier.cn/problem_show.php?pid=1222) | 放苹果 | [ROJ 1222](/problem/1222) |

<a id="sec-6"></a>
### 第六章 贪心算法

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1319](https://ybt.ssoier.cn/problem_show.php?pid=1319) | 【例6.1】排队接水 | [ROJ 1319](/problem/1319) |
| 2 | [1320](https://ybt.ssoier.cn/problem_show.php?pid=1320) | 【例6.2】均分纸牌(Noip2002) | [ROJ 1320](/problem/1320) |
| 3 | [1321](https://ybt.ssoier.cn/problem_show.php?pid=1321) | 【例6.3】删数问题(Noip1994) | [ROJ 1321](/problem/1321) |
| 4 | [1322](https://ybt.ssoier.cn/problem_show.php?pid=1322) | 【例6.4】拦截导弹问题(Noip1999) | [ROJ 1322](/problem/1322) |
| 5 | [1323](https://ybt.ssoier.cn/problem_show.php?pid=1323) | 【例6.5】活动选择 | [ROJ 1323](/problem/1323) |
| 6 | [1324](https://ybt.ssoier.cn/problem_show.php?pid=1324) | 【例6.6】整数区间 | [ROJ 1324](/problem/1324) |
| 7 | [1223](https://ybt.ssoier.cn/problem_show.php?pid=1223) | An Easy Problem | [ROJ 1223](/problem/1223) |
| 8 | [1224](https://ybt.ssoier.cn/problem_show.php?pid=1224) | 最大子矩阵 | [ROJ 1224](/problem/1224) |
| 9 | [1225](https://ybt.ssoier.cn/problem_show.php?pid=1225) | 金银岛 | [ROJ 1225](/problem/1225) |
| 10 | [1226](https://ybt.ssoier.cn/problem_show.php?pid=1226) | 装箱问题 | [ROJ 1226](/problem/1226) |
| 11 | [1227](https://ybt.ssoier.cn/problem_show.php?pid=1227) | Ride to Office | [ROJ 1227](/problem/1227) |
| 12 | [1228](https://ybt.ssoier.cn/problem_show.php?pid=1228) | 书架 | [ROJ 1228](/problem/1228) |
| 13 | [1229](https://ybt.ssoier.cn/problem_show.php?pid=1229) | 电池的寿命 | [ROJ 1229](/problem/1229) |
| 14 | [1230](https://ybt.ssoier.cn/problem_show.php?pid=1230) | 寻找平面上的极大点 | [ROJ 1230](/problem/1230) |
| 15 | [1231](https://ybt.ssoier.cn/problem_show.php?pid=1231) | 最小新整数 | [ROJ 1231](/problem/1231) |
| 16 | [1232](https://ybt.ssoier.cn/problem_show.php?pid=1232) | Crossing River | [ROJ 1232](/problem/1232) |
| 17 | [1233](https://ybt.ssoier.cn/problem_show.php?pid=1233) | 接水问题 | [ROJ 1233](/problem/1233) |

<a id="sec-7"></a>
### 第七章 分治算法

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1325](https://ybt.ssoier.cn/problem_show.php?pid=1325) | 【例7.4】 循环比赛日程表 | [ROJ 1325](/problem/1325) |
| 2 | [1326](https://ybt.ssoier.cn/problem_show.php?pid=1326) | 【例7.5】 取余运算（mod） | [ROJ 1326](/problem/1326) |
| 3 | [1327](https://ybt.ssoier.cn/problem_show.php?pid=1327) | 【例7.6】黑白棋子的移动 | [ROJ 1327](/problem/1327) |
| 4 | [1328](https://ybt.ssoier.cn/problem_show.php?pid=1328) | 【例7.7】光荣的梦想 | [ROJ 1328](/problem/1328) |
| 5 | [1234](https://ybt.ssoier.cn/problem_show.php?pid=1234) | 2011 | [ROJ 1234](/problem/1234) |
| 6 | [1235](https://ybt.ssoier.cn/problem_show.php?pid=1235) | 输出前k大的数 | [ROJ 1235](/problem/1235) |
| 7 | [1236](https://ybt.ssoier.cn/problem_show.php?pid=1236) | 区间合并 | [ROJ 1236](/problem/1236) |
| 8 | [1237](https://ybt.ssoier.cn/problem_show.php?pid=1237) | 求排列的逆序数 | [ROJ 1237](/problem/1237) |
| 9 | [1238](https://ybt.ssoier.cn/problem_show.php?pid=1238) | 一元三次方程求解 | [ROJ 1238](/problem/1238) |
| 10 | [1239](https://ybt.ssoier.cn/problem_show.php?pid=1239) | 统计数字 | [ROJ 1239](/problem/1239) |
| 11 | [1240](https://ybt.ssoier.cn/problem_show.php?pid=1240) | 查找最接近的元素 | [ROJ 1240](/problem/1240) |
| 12 | [1241](https://ybt.ssoier.cn/problem_show.php?pid=1241) | 二分法求函数的零点 | [ROJ 1241](/problem/1241) |
| 13 | [1242](https://ybt.ssoier.cn/problem_show.php?pid=1242) | 网线主管 | [ROJ 1242](/problem/1242) |
| 14 | [1243](https://ybt.ssoier.cn/problem_show.php?pid=1243) | 月度开销 | [ROJ 1243](/problem/1243) |
| 15 | [1244](https://ybt.ssoier.cn/problem_show.php?pid=1244) | 和为给定数 | [ROJ 1244](/problem/1244) |
| 16 | [1245](https://ybt.ssoier.cn/problem_show.php?pid=1245) | 不重复地输出数 | [ROJ 1245](/problem/1245) |
| 17 | [1246](https://ybt.ssoier.cn/problem_show.php?pid=1246) | 膨胀的木棍 | [ROJ 1246](/problem/1246) |
| 18 | [1247](https://ybt.ssoier.cn/problem_show.php?pid=1247) | 河中跳房子 | [ROJ 1247](/problem/1247) |

<a id="sec-8"></a>
### 第八章 广度优先搜索算

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1329](https://ybt.ssoier.cn/problem_show.php?pid=1329) | 【例8.2】细胞 | [ROJ 1329](/problem/1329) |
| 2 | [1330](https://ybt.ssoier.cn/problem_show.php?pid=1330) | 【例8.3】最少步数 | [ROJ 1330](/problem/1330) |
| 3 | [1248](https://ybt.ssoier.cn/problem_show.php?pid=1248) | Dungeon Master | [ROJ 1248](/problem/1248) |
| 4 | [1249](https://ybt.ssoier.cn/problem_show.php?pid=1249) | Lake Counting | [ROJ 1249](/problem/1249) |
| 5 | [1250](https://ybt.ssoier.cn/problem_show.php?pid=1250) | The Castle | [ROJ 1250](/problem/1250) |
| 6 | [1251](https://ybt.ssoier.cn/problem_show.php?pid=1251) | 仙岛求药 | [ROJ 1251](/problem/1251) |
| 7 | [1252](https://ybt.ssoier.cn/problem_show.php?pid=1252) | 走迷宫 | [ROJ 1252](/problem/1252) |
| 8 | [1253](https://ybt.ssoier.cn/problem_show.php?pid=1253) | 抓住那头牛 | [ROJ 1253](/problem/1253) |
| 9 | [1254](https://ybt.ssoier.cn/problem_show.php?pid=1254) | 走出迷宫 | [ROJ 1254](/problem/1254) |
| 10 | [1255](https://ybt.ssoier.cn/problem_show.php?pid=1255) | 迷宫问题 | [ROJ 1255](/problem/1255) |
| 11 | [1256](https://ybt.ssoier.cn/problem_show.php?pid=1256) | 献给阿尔吉侬的花束 | [ROJ 1256](/problem/1256) |
| 12 | [1257](https://ybt.ssoier.cn/problem_show.php?pid=1257) | Knight Moves | [ROJ 1257](/problem/1257) |

<a id="sec-9"></a>
### 第九章 动态规划

<a id="sec-10"></a>
#### 第一节 动态规划的基本模型

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1258](https://ybt.ssoier.cn/problem_show.php?pid=1258) | 【例9.2】数字金字塔 | [ROJ 1258](/problem/1258) |
| 2 | [1259](https://ybt.ssoier.cn/problem_show.php?pid=1259) | 【例9.3】求最长不下降序列 | [ROJ 1259](/problem/1259) |
| 3 | [1260](https://ybt.ssoier.cn/problem_show.php?pid=1260) | 【例9.4】拦截导弹(Noip1999) | [ROJ 1260](/problem/1260) |
| 4 | [1261](https://ybt.ssoier.cn/problem_show.php?pid=1261) | 【例9.5】城市交通路网 | [ROJ 1261](/problem/1261)（ROJ 题名：【例9.5】城市交通网络） |
| 5 | [1262](https://ybt.ssoier.cn/problem_show.php?pid=1262) | 【例9.6】挖地雷 | [ROJ 1262](/problem/1262) |
| 6 | [1263](https://ybt.ssoier.cn/problem_show.php?pid=1263) | 【例9.7】友好城市 | [ROJ 1263](/problem/1263) |
| 7 | [1264](https://ybt.ssoier.cn/problem_show.php?pid=1264) | 【例9.8】合唱队形 | [ROJ 1264](/problem/1264) |
| 8 | [1265](https://ybt.ssoier.cn/problem_show.php?pid=1265) | 【例9.9】最长公共子序列 | [ROJ 1265](/problem/1265) |
| 9 | [1266](https://ybt.ssoier.cn/problem_show.php?pid=1266) | 【例9.10】机器分配 | [ROJ 1266](/problem/1266) |
| 10 | [1281](https://ybt.ssoier.cn/problem_show.php?pid=1281) | 最长上升子序列 | [ROJ 1281](/problem/1281) |
| 11 | [1282](https://ybt.ssoier.cn/problem_show.php?pid=1282) | 最大子矩阵 | [ROJ 1282](/problem/1282) |
| 12 | [1283](https://ybt.ssoier.cn/problem_show.php?pid=1283) | 登山 | [ROJ 1283](/problem/1283) |
| 13 | [1284](https://ybt.ssoier.cn/problem_show.php?pid=1284) | 摘花生 | [ROJ 1284](/problem/1284) |
| 14 | [1285](https://ybt.ssoier.cn/problem_show.php?pid=1285) | 最大上升子序列和 | [ROJ 1285](/problem/1285) |
| 15 | [1286](https://ybt.ssoier.cn/problem_show.php?pid=1286) | 怪盗基德的滑翔翼 | [ROJ 1286](/problem/1286) |
| 16 | [1287](https://ybt.ssoier.cn/problem_show.php?pid=1287) | 最低通行费 | [ROJ 1287](/problem/1287) |
| 17 | [1288](https://ybt.ssoier.cn/problem_show.php?pid=1288) | 三角形最佳路径问题 | [ROJ 1288](/problem/1288) |
| 18 | [1289](https://ybt.ssoier.cn/problem_show.php?pid=1289) | 拦截导弹 | [ROJ 1289](/problem/1289) |

<a id="sec-11"></a>
#### 第二节 背包问题

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1267](https://ybt.ssoier.cn/problem_show.php?pid=1267) | 【例9.11】01背包问题 | [ROJ 1267](/problem/1267) |
| 2 | [1268](https://ybt.ssoier.cn/problem_show.php?pid=1268) | 【例9.12】完全背包问题 | [ROJ 1268](/problem/1268) |
| 3 | [1269](https://ybt.ssoier.cn/problem_show.php?pid=1269) | 【例9.13】庆功会 | [ROJ 1269](/problem/1269) |
| 4 | [1270](https://ybt.ssoier.cn/problem_show.php?pid=1270) | 【例9.14】混合背包 | [ROJ 1270](/problem/1270) |
| 5 | [1271](https://ybt.ssoier.cn/problem_show.php?pid=1271) | 【例9.15】潜水员 | [ROJ 1271](/problem/1271) |
| 6 | [1272](https://ybt.ssoier.cn/problem_show.php?pid=1272) | 【例9.16】分组背包 | [ROJ 1272](/problem/1272) |
| 7 | [1273](https://ybt.ssoier.cn/problem_show.php?pid=1273) | 【例9.17】货币系统 | [ROJ 1273](/problem/1273) |
| 8 | [1290](https://ybt.ssoier.cn/problem_show.php?pid=1290) | 采药 | [ROJ 1290](/problem/1290) |
| 9 | [1291](https://ybt.ssoier.cn/problem_show.php?pid=1291) | 数字组合 | [ROJ 1291](/problem/1291) |
| 10 | [1292](https://ybt.ssoier.cn/problem_show.php?pid=1292) | 宠物小精灵之收服 | [ROJ 1292](/problem/1292) |
| 11 | [1293](https://ybt.ssoier.cn/problem_show.php?pid=1293) | 买书 | [ROJ 1293](/problem/1293) |
| 12 | [1294](https://ybt.ssoier.cn/problem_show.php?pid=1294) | Charm Bracelet | [ROJ 1294](/problem/1294) |
| 13 | [1295](https://ybt.ssoier.cn/problem_show.php?pid=1295) | 装箱问题 | [ROJ 1295](/problem/1295) |
| 14 | [1296](https://ybt.ssoier.cn/problem_show.php?pid=1296) | 开餐馆 | [ROJ 1296](/problem/1296) |
| 15 | [2003](https://ybt.ssoier.cn/problem_show.php?pid=2003) | 高效工作 | [ROJ 5018](/problem/5018)（ROJ 题号 5018） |

<a id="sec-12"></a>
#### 第三节 动态规划经典题目

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1274](https://ybt.ssoier.cn/problem_show.php?pid=1274) | 【例9.18】合并石子 | [ROJ 1274](/problem/1274) |
| 2 | [1275](https://ybt.ssoier.cn/problem_show.php?pid=1275) | 【例9.19】乘积最大 | [ROJ 1275](/problem/1275) |
| 3 | [1276](https://ybt.ssoier.cn/problem_show.php?pid=1276) | 【例9.20】编辑距离 | [ROJ 1276](/problem/1276) |
| 4 | [1277](https://ybt.ssoier.cn/problem_show.php?pid=1277) | 【例9.21】方格取数 | [ROJ 1277](/problem/1277) |
| 5 | [1278](https://ybt.ssoier.cn/problem_show.php?pid=1278) | 【例9.22】复制书稿(book) | [ROJ 1278](/problem/1278) |
| 6 | [1279](https://ybt.ssoier.cn/problem_show.php?pid=1279) | 【例9.23】橱窗布置(flower) | [ROJ 1279](/problem/1279) |
| 7 | [1280](https://ybt.ssoier.cn/problem_show.php?pid=1280) | 【例9.24】滑雪 | [ROJ 1280](/problem/1280) |
| 8 | [1297](https://ybt.ssoier.cn/problem_show.php?pid=1297) | 公共子序列 | [ROJ 1297](/problem/1297) |
| 9 | [1298](https://ybt.ssoier.cn/problem_show.php?pid=1298) | 计算字符串距离 | [ROJ 1298](/problem/1298) |
| 10 | [1299](https://ybt.ssoier.cn/problem_show.php?pid=1299) | 糖果 | [ROJ 1299](/problem/1299) |
| 11 | [1300](https://ybt.ssoier.cn/problem_show.php?pid=1300) | 鸡蛋的硬度 | [ROJ 1300](/problem/1300) |
| 12 | [1301](https://ybt.ssoier.cn/problem_show.php?pid=1301) | 大盗阿福 | [ROJ 1301](/problem/1301) |
| 13 | [1302](https://ybt.ssoier.cn/problem_show.php?pid=1302) | 股票买卖 | [ROJ 1302](/problem/1302) |
| 14 | [1303](https://ybt.ssoier.cn/problem_show.php?pid=1303) | 鸣人的影分身 | [ROJ 1303](/problem/1303) |
| 15 | [1304](https://ybt.ssoier.cn/problem_show.php?pid=1304) | 数的划分 | [ROJ 1304](/problem/1304) |
| 16 | [1305](https://ybt.ssoier.cn/problem_show.php?pid=1305) | Maximum sum | [ROJ 1305](/problem/1305) |
| 17 | [1306](https://ybt.ssoier.cn/problem_show.php?pid=1306) | 最长公共子上升序列 | [ROJ 1306](/problem/1306) |

<a id="appendix-a"></a>
## 附录 A：同题异号对照

下表的题目在本篇中没有同题号的记录，但 ROJ 的其他题号下可能有同一道题（同一道经典题被多个题库收录、题号各不相同）。做题时任选其一即可。

### A.1 已核对（同一场真题，年份与组别一致）

（无）

### A.2 待核对（题目同名）

同名不等于同题（比如两本书里都有叫「最大公约数」的题），刷题前请先对照题面。

（无）

<!-- ybt:generated:end -->

## 数据来源与更新

- 分类树与题目标题抓取自 [ybt.ssoier.cn](https://ybt.ssoier.cn/index.php)（快照：`scripts/ybt_catalog.json`）；ROJ 收录情况取自本仓库 `problems/*/config.json`。
- 表格区（`<!-- ybt:generated:start -->` 与 `<!-- ybt:generated:end -->` 之间）由 `python3 scripts/gen_ybt_list.py` 重新生成，引言、笔记等区块外内容可手工修改。
