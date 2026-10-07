---
title: 一本通 · 数据结构基础
description: 《信息学奥赛一本通（C++版）》数据结构基础篇：76 题，本站收录 76（100%）。
tags: [一本通, 教材配套, 刷题计划, 数据结构基础]
order: 3
items: 76
covered: 76
source: https://ybt.ssoier.cn/index.php
---

按《信息学奥赛一本通（C++版）》在线题库 [ybt.ssoier.cn](https://ybt.ssoier.cn/index.php) 左侧「题库全部题目分类索引」整理的 **数据结构基础篇**，可对照原书顺序刷题。

## 怎么用这份单子

- **一本通题号** 链接到一本通原题页；**ROJ 收录** 列是站内链接，在本站点开直接看题面；
- ROJ 列为 `—` 表示 ROJ 暂未收录这道题（仍可去一本通原站做）；
- 括号里标注「ROJ 题名」的，表示 ROJ 侧题目名称与一本通不同（多为改名/换译），题面是同一道题；
- **附录 A** 列出 ROJ 中『同题不同编号』的情况，分「已核对」「待核对」两档可信度；
- 一本通题目单共 5 篇（C++编程语言 / 基础算法 / 数据结构基础 / 算法提高篇 / 高手训练篇），可在[题目单列表](/problem-sets)里切换；勾选进度在站内按题号全局共享，跨篇不会丢；
- 在 GitHub 上阅读时，`/problem/…` 是站内路径，需补上 `https://roj.ac.cn` 前缀才能点开。

<!-- ybt:generated:start -->

## 本篇概览

本篇 76 题，本站收录 76（100%）；一本通题目单共 5 篇、895 题。

## 目录

- [第一章 栈](#sec-1)
- [第二章 队列](#sec-2)
- [第三章 树](#sec-3)
  - [第一节 树及二叉树](#sec-4)
  - [第二节 堆及其应用](#sec-5)
- [第四章 图论算法](#sec-6)
  - [第一节 图的遍历](#sec-7)
  - [第二节 最短路径算法](#sec-8)
  - [第三节 图的连通性问题](#sec-9)
  - [第四节 并查集](#sec-10)
  - [第五节 最小生成树](#sec-11)
  - [第六节 拓扑排序与关键路径](#sec-12)
- [附录 A：同题异号对照](#appendix-a)

<a id="sec-0"></a>
## 数据结构基础

<a id="sec-1"></a>
### 第一章 栈

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1331](https://ybt.ssoier.cn/problem_show.php?pid=1331) | 【例1-2】后缀表达式的值 | [ROJ 1331](/problem/1331) |
| 2 | [1353](https://ybt.ssoier.cn/problem_show.php?pid=1353) | 表达式括号匹配(stack) | [ROJ 1353](/problem/1353) |
| 3 | [1354](https://ybt.ssoier.cn/problem_show.php?pid=1354) | 括弧匹配检验 | [ROJ 1354](/problem/1354) |
| 4 | [1355](https://ybt.ssoier.cn/problem_show.php?pid=1355) | 字符串匹配问题(strs) | [ROJ 1355](/problem/1355) |
| 5 | [1356](https://ybt.ssoier.cn/problem_show.php?pid=1356) | 计算(calc) | [ROJ 1356](/problem/1356) |
| 6 | [1357](https://ybt.ssoier.cn/problem_show.php?pid=1357) | 车厢调度(train) | [ROJ 1357](/problem/1357) |
| 7 | [1358](https://ybt.ssoier.cn/problem_show.php?pid=1358) | 中缀表达式值(expr) | [ROJ 1358](/problem/1358) |

<a id="sec-2"></a>
### 第二章 队列

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1332](https://ybt.ssoier.cn/problem_show.php?pid=1332) | 【例2-1】周末舞会 | [ROJ 1332](/problem/1332) |
| 2 | [1333](https://ybt.ssoier.cn/problem_show.php?pid=1333) | 【例2-2】Blah数集 | [ROJ 1333](/problem/1333) |
| 3 | [1334](https://ybt.ssoier.cn/problem_show.php?pid=1334) | 【例2-3】围圈报数 | [ROJ 1334](/problem/1334) |
| 4 | [1335](https://ybt.ssoier.cn/problem_show.php?pid=1335) | 【例2-4】连通块 | [ROJ 1335](/problem/1335) |
| 5 | [1359](https://ybt.ssoier.cn/problem_show.php?pid=1359) | 围成面积 | [ROJ 1359](/problem/1359) |
| 6 | [1360](https://ybt.ssoier.cn/problem_show.php?pid=1360) | 奇怪的电梯(lift) | [ROJ 1360](/problem/1360) |
| 7 | [1361](https://ybt.ssoier.cn/problem_show.php?pid=1361) | 产生数(Produce) | [ROJ 1361](/problem/1361) |
| 8 | [1362](https://ybt.ssoier.cn/problem_show.php?pid=1362) | 家庭问题(family) | [ROJ 1362](/problem/1362) |
| 9 | [1418](https://ybt.ssoier.cn/problem_show.php?pid=1418) | 猴子选大王 | [ROJ 1418](/problem/1418) |

<a id="sec-3"></a>
### 第三章 树

<a id="sec-4"></a>
#### 第一节 树及二叉树

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1336](https://ybt.ssoier.cn/problem_show.php?pid=1336) | 【例3-1】找树根和孩子 | [ROJ 1336](/problem/1336) |
| 2 | [1337](https://ybt.ssoier.cn/problem_show.php?pid=1337) | 【例3-2】单词查找树 | [ROJ 1337](/problem/1337) |
| 3 | [1338](https://ybt.ssoier.cn/problem_show.php?pid=1338) | 【例3-3】医院设置 | [ROJ 1338](/problem/1338) |
| 4 | [1339](https://ybt.ssoier.cn/problem_show.php?pid=1339) | 【例3-4】求后序遍历 | [ROJ 1339](/problem/1339) |
| 5 | [1340](https://ybt.ssoier.cn/problem_show.php?pid=1340) | 【例3-5】扩展二叉树 | [ROJ 1340](/problem/1340) |
| 6 | [1363](https://ybt.ssoier.cn/problem_show.php?pid=1363) | 小球(drop) | [ROJ 1363](/problem/1363) |
| 7 | [1364](https://ybt.ssoier.cn/problem_show.php?pid=1364) | 二叉树遍历(flist) | [ROJ 1364](/problem/1364) |
| 8 | [1365](https://ybt.ssoier.cn/problem_show.php?pid=1365) | FBI树(fbi) | [ROJ 1365](/problem/1365) |
| 9 | [1366](https://ybt.ssoier.cn/problem_show.php?pid=1366) | 二叉树输出(btout) | [ROJ 1366](/problem/1366) |
| 10 | [1367](https://ybt.ssoier.cn/problem_show.php?pid=1367) | 查找二叉树(tree_a) | [ROJ 1367](/problem/1367) |
| 11 | [1368](https://ybt.ssoier.cn/problem_show.php?pid=1368) | 对称二叉树(tree_c) | [ROJ 1368](/problem/1368) |
| 12 | [2141](https://ybt.ssoier.cn/problem_show.php?pid=2141) | 公司下属 | [ROJ 2141](/problem/2141) |
| 13 | [2142](https://ybt.ssoier.cn/problem_show.php?pid=2142) | 树边匹配 | [ROJ 2142](/problem/2142) |

<a id="sec-5"></a>
#### 第二节 堆及其应用

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1369](https://ybt.ssoier.cn/problem_show.php?pid=1369) | 合并果子(fruit) | [ROJ 1369](/problem/1369) |
| 2 | [1370](https://ybt.ssoier.cn/problem_show.php?pid=1370) | 最小函数值(minval) | [ROJ 1370](/problem/1370) |
| 3 | [1371](https://ybt.ssoier.cn/problem_show.php?pid=1371) | 看病 | [ROJ 1371](/problem/1371) |
| 4 | [1372](https://ybt.ssoier.cn/problem_show.php?pid=1372) | 小明的账单 | [ROJ 1372](/problem/1372) |
| 5 | [1373](https://ybt.ssoier.cn/problem_show.php?pid=1373) | 鱼塘钓鱼(fishing） | [ROJ 1373](/problem/1373) |

<a id="sec-6"></a>
### 第四章 图论算法

<a id="sec-7"></a>
#### 第一节 图的遍历

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1341](https://ybt.ssoier.cn/problem_show.php?pid=1341) | 【例题】一笔画问题 | [ROJ 1341](/problem/1341) |
| 2 | [2123](https://ybt.ssoier.cn/problem_show.php?pid=2123) | 图的存储与访问 | [ROJ 2123](/problem/2123) |
| 3 | [2124](https://ybt.ssoier.cn/problem_show.php?pid=2124) | 图的遍历 | [ROJ 2124](/problem/2124) |
| 4 | [2125](https://ybt.ssoier.cn/problem_show.php?pid=2125) | 查找文献 | [ROJ 2125](/problem/2125) |
| 5 | [2126](https://ybt.ssoier.cn/problem_show.php?pid=2126) | [USACO19OPEN] Milk Factory | [ROJ 2126](/problem/2126) |
| 6 | [1374](https://ybt.ssoier.cn/problem_show.php?pid=1374) | 铲雪车(snow) | [ROJ 1374](/problem/1374) |
| 7 | [1375](https://ybt.ssoier.cn/problem_show.php?pid=1375) | 骑马修栅栏(fence) | [ROJ 1375](/problem/1375) |

<a id="sec-8"></a>
#### 第二节 最短路径算法

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1342](https://ybt.ssoier.cn/problem_show.php?pid=1342) | 【例4-1】最短路径问题 | [ROJ 1342](/problem/1342) |
| 2 | [1343](https://ybt.ssoier.cn/problem_show.php?pid=1343) | 【例4-2】牛的旅行 | [ROJ 1343](/problem/1343) |
| 3 | [1344](https://ybt.ssoier.cn/problem_show.php?pid=1344) | 【例4-4】最小花费 | [ROJ 1344](/problem/1344) |
| 4 | [1345](https://ybt.ssoier.cn/problem_show.php?pid=1345) | 【例4-6】香甜的黄油 | [ROJ 1345](/problem/1345) |
| 5 | [1376](https://ybt.ssoier.cn/problem_show.php?pid=1376) | 信使(msner) | [ROJ 1376](/problem/1376) |
| 6 | [1377](https://ybt.ssoier.cn/problem_show.php?pid=1377) | 最优乘车(travel) | [ROJ 1377](/problem/1377) |
| 7 | [1378](https://ybt.ssoier.cn/problem_show.php?pid=1378) | 最短路径(shopth) | [ROJ 1378](/problem/1378) |
| 8 | [1379](https://ybt.ssoier.cn/problem_show.php?pid=1379) | 热浪(heatwv) | [ROJ 1379](/problem/1379) |
| 9 | [1380](https://ybt.ssoier.cn/problem_show.php?pid=1380) | 分糖果(candy) | [ROJ 1380](/problem/1380) |
| 10 | [1381](https://ybt.ssoier.cn/problem_show.php?pid=1381) | 城市路(Dijkstra) | [ROJ 1381](/problem/1381) |
| 11 | [1382](https://ybt.ssoier.cn/problem_show.php?pid=1382) | 最短路(Spfa) | [ROJ 1382](/problem/1382) |
| 12 | [1419](https://ybt.ssoier.cn/problem_show.php?pid=1419) | SPFA(II) | [ROJ 1419](/problem/1419) |
| 13 | [1420](https://ybt.ssoier.cn/problem_show.php?pid=1420) | Dijkastra(II) | [ROJ 1420](/problem/1420) |
| 14 | [1421](https://ybt.ssoier.cn/problem_show.php?pid=1421) | Floyd | [ROJ 1421](/problem/1421) |

<a id="sec-9"></a>
#### 第三节 图的连通性问题

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1383](https://ybt.ssoier.cn/problem_show.php?pid=1383) | 刻录光盘(cdrom) | [ROJ 1383](/problem/1383) |
| 2 | [1384](https://ybt.ssoier.cn/problem_show.php?pid=1384) | 珍珠(bead) | [ROJ 1384](/problem/1384) |

<a id="sec-10"></a>
#### 第四节 并查集

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1346](https://ybt.ssoier.cn/problem_show.php?pid=1346) | 【例4-7】亲戚(relation) | [ROJ 1346](/problem/1346) |
| 2 | [1347](https://ybt.ssoier.cn/problem_show.php?pid=1347) | 【例4-8】格子游戏 | [ROJ 1347](/problem/1347) |
| 3 | [1385](https://ybt.ssoier.cn/problem_show.php?pid=1385) | 团伙(group) | [ROJ 1385](/problem/1385) |
| 4 | [1386](https://ybt.ssoier.cn/problem_show.php?pid=1386) | 打击犯罪(black) | [ROJ 1386](/problem/1386) |
| 5 | [1387](https://ybt.ssoier.cn/problem_show.php?pid=1387) | 搭配购买(buy) | [ROJ 1387](/problem/1387) |
| 6 | [1388](https://ybt.ssoier.cn/problem_show.php?pid=1388) | 家谱(gen) | [ROJ 1388](/problem/1388) |
| 7 | [1389](https://ybt.ssoier.cn/problem_show.php?pid=1389) | 亲戚 | [ROJ 1389](/problem/1389) |
| 8 | [1390](https://ybt.ssoier.cn/problem_show.php?pid=1390) | 食物链【NOI2001】 | [ROJ 1390](/problem/1390) |

<a id="sec-11"></a>
#### 第五节 最小生成树

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1348](https://ybt.ssoier.cn/problem_show.php?pid=1348) | 【例4-9】城市公交网建设问题 | [ROJ 1348](/problem/1348) |
| 2 | [1349](https://ybt.ssoier.cn/problem_show.php?pid=1349) | 【例4-10】最优布线问题 | [ROJ 1349](/problem/1349) |
| 3 | [1350](https://ybt.ssoier.cn/problem_show.php?pid=1350) | 【例4-11】最短网络(agrinet) | [ROJ 1350](/problem/1350) |
| 4 | [1351](https://ybt.ssoier.cn/problem_show.php?pid=1351) | 【例4-12】家谱树 | [ROJ 1351](/problem/1351) |
| 5 | [1391](https://ybt.ssoier.cn/problem_show.php?pid=1391) | 局域网(net) | [ROJ 1391](/problem/1391) |
| 6 | [1392](https://ybt.ssoier.cn/problem_show.php?pid=1392) | 繁忙的都市(city) | [ROJ 1392](/problem/1392) |
| 7 | [1393](https://ybt.ssoier.cn/problem_show.php?pid=1393) | 联络员(liaison) | [ROJ 1393](/problem/1393) |
| 8 | [1394](https://ybt.ssoier.cn/problem_show.php?pid=1394) | 连接格点(grid) | [ROJ 1394](/problem/1394) |

<a id="sec-12"></a>
#### 第六节 拓扑排序与关键路径

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1352](https://ybt.ssoier.cn/problem_show.php?pid=1352) | 【例4-13】奖金 | [ROJ 1352](/problem/1352) |
| 2 | [1395](https://ybt.ssoier.cn/problem_show.php?pid=1395) | 烦人的幻灯片(slides) | [ROJ 1395](/problem/1395) |
| 3 | [1396](https://ybt.ssoier.cn/problem_show.php?pid=1396) | 病毒(virus) | [ROJ 1396](/problem/1396) |

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
