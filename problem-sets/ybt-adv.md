---
title: 一本通 · 算法提高篇
description: 《信息学奥赛一本通（C++版）》算法提高篇：252 题，本站收录 252（100%）。
tags: [一本通, 教材配套, 刷题计划, 算法提高篇]
order: 4
items: 252
covered: 252
source: https://ybt.ssoier.cn/index.php
---

按《信息学奥赛一本通（C++版）》在线题库 [ybt.ssoier.cn](https://ybt.ssoier.cn/index.php) 左侧「题库全部题目分类索引」整理的 **算法提高篇**，可对照原书顺序刷题。

## 怎么用这份单子

- **一本通题号** 链接到一本通原题页；**ROJ 收录** 列是站内链接，在本站点开直接看题面；
- ROJ 列为 `—` 表示 ROJ 暂未收录这道题（仍可去一本通原站做）；
- 括号里标注「ROJ 题名」的，表示 ROJ 侧题目名称与一本通不同（多为改名/换译），题面是同一道题；
- **附录 A** 列出 ROJ 中『同题不同编号』的情况，分「已核对」「待核对」两档可信度；
- 一本通题目单共 5 篇（C++编程语言 / 基础算法 / 数据结构基础 / 算法提高篇 / 高手训练篇），可在[题目单列表](/problem-sets)里切换；勾选进度在站内按题号全局共享，跨篇不会丢；
- 在 GitHub 上阅读时，`/problem/…` 是站内路径，需补上 `https://roj.ac.cn` 前缀才能点开。

<!-- ybt:generated:start -->

## 本篇概览

本篇 252 题，本站收录 252（100%）；一本通题目单共 5 篇、895 题。

## 目录

- [一、基础算法(提高篇)](#sec-1)
  - [第1章 贪心算法](#sec-2)
  - [第2章 二分与三分](#sec-3)
  - [第3章 深搜的剪枝技巧](#sec-4)
  - [第4章 广搜的优化技巧](#sec-5)
- [二、字符串算法(提高篇)](#sec-6)
  - [第1章 哈希和哈希表](#sec-7)
  - [第2章 KMP算法](#sec-8)
  - [第3章 trie字典树](#sec-9)
  - [第4章 AC自动机](#sec-10)
- [三、图论(提高篇)](#sec-11)
  - [第1章 最小生成树](#sec-12)
  - [第2章 最短路问题](#sec-13)
  - [第3章 SPFA算法优化](#sec-14)
  - [第4章 差分约束系统](#sec-15)
  - [第5章 强连通分量](#sec-16)
  - [第6章 割点和桥](#sec-17)
  - [第7章 欧拉回路](#sec-18)
- [四、数据结构(提高篇)](#sec-19)
  - [第1章 树状数组](#sec-20)
  - [第2章 RMQ 问题](#sec-21)
  - [第3章 线段树](#sec-22)
  - [第4章 倍增求 LCA](#sec-23)
  - [第5章 树链剖分](#sec-24)
  - [第6章 平衡树 Treap](#sec-25)
- [五、动态规划(提高篇)](#sec-26)
  - [第1章 区间类动态规划](#sec-27)
  - [第2章 树型动态规划](#sec-28)
  - [第3章 数位动态规划](#sec-29)
  - [第4章 状态压缩类动态规划](#sec-30)
  - [第5章 单调队列优化动态规划](#sec-31)
  - [第6章 斜率优化动态规划](#sec-32)
- [六、数学基础(提高篇)](#sec-33)
  - [第1章 快速幂](#sec-34)
  - [第2章 质数](#sec-35)
  - [第3章 约数](#sec-36)
  - [第4章 同余问题](#sec-37)
  - [第5章 矩阵乘法](#sec-38)
  - [第6章 组合数学](#sec-39)
  - [第7章 博弈论](#sec-40)
- [附录 A：同题异号对照](#appendix-a)

<a id="sec-0"></a>
## 算法提高篇

<a id="sec-1"></a>
### 一、基础算法(提高篇)

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1422](https://ybt.ssoier.cn/problem_show.php?pid=1422) | 【例题1】活动安排 | [ROJ 1422](/problem/1422) |
| 2 | [1423](https://ybt.ssoier.cn/problem_show.php?pid=1423) | 【例题2】种树 | [ROJ 1423](/problem/1423) |
| 3 | [1424](https://ybt.ssoier.cn/problem_show.php?pid=1424) | 【例题3】喷水装置 | [ROJ 1424](/problem/1424) |
| 4 | [1425](https://ybt.ssoier.cn/problem_show.php?pid=1425) | 【例题4】加工生产调度 | [ROJ 1425](/problem/1425) |
| 5 | [1426](https://ybt.ssoier.cn/problem_show.php?pid=1426) | 【例题5】智力大冲浪 | [ROJ 1426](/problem/1426) |
| 6 | [1427](https://ybt.ssoier.cn/problem_show.php?pid=1427) | 数列极差 | [ROJ 1427](/problem/1427) |
| 7 | [1428](https://ybt.ssoier.cn/problem_show.php?pid=1428) | 数列分段 | [ROJ 1428](/problem/1428) |
| 8 | [1429](https://ybt.ssoier.cn/problem_show.php?pid=1429) | 线段 | [ROJ 1429](/problem/1429) |
| 9 | [1430](https://ybt.ssoier.cn/problem_show.php?pid=1430) | 家庭作业 | [ROJ 1430](/problem/1430) |
| 10 | [1431](https://ybt.ssoier.cn/problem_show.php?pid=1431) | 钓鱼 | [ROJ 1431](/problem/1431) |
| 11 | [1432](https://ybt.ssoier.cn/problem_show.php?pid=1432) | 糖果传递 | [ROJ 1432](/problem/1432) |
| 12 | [1433](https://ybt.ssoier.cn/problem_show.php?pid=1433) | 【例题1】愤怒的牛 | [ROJ 1433](/problem/1433) |
| 13 | [1434](https://ybt.ssoier.cn/problem_show.php?pid=1434) | 【例题2】Best Cow Fences | [ROJ 1434](/problem/1434) |
| 14 | [1435](https://ybt.ssoier.cn/problem_show.php?pid=1435) | 【例题3】曲线 | [ROJ 1435](/problem/1435) |
| 15 | [1436](https://ybt.ssoier.cn/problem_show.php?pid=1436) | 数列分段II | [ROJ 1436](/problem/1436) |
| 16 | [1437](https://ybt.ssoier.cn/problem_show.php?pid=1437) | 扩散 | [ROJ 1437](/problem/1437) |
| 17 | [1438](https://ybt.ssoier.cn/problem_show.php?pid=1438) | 灯泡 | [ROJ 1438](/problem/1438) |
| 18 | [1439](https://ybt.ssoier.cn/problem_show.php?pid=1439) | 【SCOI2010】传送带 | [ROJ 1439](/problem/1439) |
| 19 | [1440](https://ybt.ssoier.cn/problem_show.php?pid=1440) | 【例题1】数的划分 | [ROJ 1440](/problem/1440) |
| 20 | [1441](https://ybt.ssoier.cn/problem_show.php?pid=1441) | 【例题2】生日蛋糕 | [ROJ 1441](/problem/1441) |
| 21 | [1442](https://ybt.ssoier.cn/problem_show.php?pid=1442) | 【例题3】小木棍 | [ROJ 1442](/problem/1442) |
| 22 | [1443](https://ybt.ssoier.cn/problem_show.php?pid=1443) | 【例题4】Addition Chains | [ROJ 1443](/problem/1443) |
| 23 | [1444](https://ybt.ssoier.cn/problem_show.php?pid=1444) | 埃及分数 | [ROJ 1444](/problem/1444) |
| 24 | [1445](https://ybt.ssoier.cn/problem_show.php?pid=1445) | 平板涂色 | [ROJ 1445](/problem/1445) |
| 25 | [1446](https://ybt.ssoier.cn/problem_show.php?pid=1446) | 素数方阵 | [ROJ 1446](/problem/1446)（ROJ 题名：「一本通 1.3 练习 3」质数方阵） |
| 26 | [1447](https://ybt.ssoier.cn/problem_show.php?pid=1447) | 靶形数独 | [ROJ 1447](/problem/1447) |
| 27 | [1448](https://ybt.ssoier.cn/problem_show.php?pid=1448) | 【例题1】电路维修 | [ROJ 1448](/problem/1448) |
| 28 | [1449](https://ybt.ssoier.cn/problem_show.php?pid=1449) | 【例题2】魔板 | [ROJ 1449](/problem/1449) |
| 29 | [1450](https://ybt.ssoier.cn/problem_show.php?pid=1450) | 【例 3】Knight Moves | [ROJ 1450](/problem/1450) |
| 30 | [1451](https://ybt.ssoier.cn/problem_show.php?pid=1451) | 棋盘游戏 | [ROJ 1451](/problem/1451) |
| 31 | [1452](https://ybt.ssoier.cn/problem_show.php?pid=1452) | Keyboarding | [ROJ 1452](/problem/1452) |
| 32 | [1453](https://ybt.ssoier.cn/problem_show.php?pid=1453) | 移动玩具 | [ROJ 1453](/problem/1453) |
| 33 | [1454](https://ybt.ssoier.cn/problem_show.php?pid=1454) | 山峰和山谷 | [ROJ 1454](/problem/1454) |

<a id="sec-2"></a>
#### 第1章 贪心算法

<a id="sec-3"></a>
#### 第2章 二分与三分

<a id="sec-4"></a>
#### 第3章 深搜的剪枝技巧

<a id="sec-5"></a>
#### 第4章 广搜的优化技巧

<a id="sec-6"></a>
### 二、字符串算法(提高篇)

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1455](https://ybt.ssoier.cn/problem_show.php?pid=1455) | 【例题1】Oulipo | [ROJ 1455](/problem/1455) |
| 2 | [1456](https://ybt.ssoier.cn/problem_show.php?pid=1456) | 【例题2】图书管理 | [ROJ 1456](/problem/1456) |
| 3 | [1457](https://ybt.ssoier.cn/problem_show.php?pid=1457) | Power Strings | [ROJ 1457](/problem/1457) |
| 4 | [1458](https://ybt.ssoier.cn/problem_show.php?pid=1458) | Seek the Name, Seek the Fame | [ROJ 1458](/problem/1458) |
| 5 | [1459](https://ybt.ssoier.cn/problem_show.php?pid=1459) | friends | [ROJ 1459](/problem/1459)（ROJ 题名：「一本通 2.1 练习 3」Friends） |
| 6 | [1460](https://ybt.ssoier.cn/problem_show.php?pid=1460) | A Horrible Poem | [ROJ 1460](/problem/1460) |
| 7 | [1461](https://ybt.ssoier.cn/problem_show.php?pid=1461) | Beads | [ROJ 1461](/problem/1461) |
| 8 | [1462](https://ybt.ssoier.cn/problem_show.php?pid=1462) | Antisymmetry | [ROJ 1462](/problem/1462) |
| 9 | [1463](https://ybt.ssoier.cn/problem_show.php?pid=1463) | 门票 | [ROJ 1463](/problem/1463) |
| 10 | [1464](https://ybt.ssoier.cn/problem_show.php?pid=1464) | 收集雪花 | [ROJ 1464](/problem/1464) |
| 11 | [1465](https://ybt.ssoier.cn/problem_show.php?pid=1465) | 【例题1】剪花布条 | [ROJ 1465](/problem/1465) |
| 12 | [1466](https://ybt.ssoier.cn/problem_show.php?pid=1466) | 【例题2】Power Strings | [ROJ 1466](/problem/1466) |
| 13 | [1467](https://ybt.ssoier.cn/problem_show.php?pid=1467) | Radio Transmission | [ROJ 1467](/problem/1467) |
| 14 | [1468](https://ybt.ssoier.cn/problem_show.php?pid=1468) | OKR-Periods of Words | [ROJ 1468](/problem/1468) |
| 15 | [1469](https://ybt.ssoier.cn/problem_show.php?pid=1469) | 似乎在梦中见过的样子 | [ROJ 1469](/problem/1469) |
| 16 | [1470](https://ybt.ssoier.cn/problem_show.php?pid=1470) | Censoring | [ROJ 1470](/problem/1470) |
| 17 | [1471](https://ybt.ssoier.cn/problem_show.php?pid=1471) | 【例题1】Phone List | [ROJ 1471](/problem/1471) |
| 18 | [1472](https://ybt.ssoier.cn/problem_show.php?pid=1472) | 【例题2】The XOR Largest Pair | [ROJ 1472](/problem/1472) |
| 19 | [1473](https://ybt.ssoier.cn/problem_show.php?pid=1473) | 【例题3】Codechef REBXOR | [ROJ 1473](/problem/1473)（ROJ 题名：「一本通 2.3 例 3」Nikitosh 和异或） |
| 20 | [1474](https://ybt.ssoier.cn/problem_show.php?pid=1474) | Immediate Decodability | [ROJ 1474](/problem/1474) |
| 21 | [1475](https://ybt.ssoier.cn/problem_show.php?pid=1475) | L语言 | [ROJ 1475](/problem/1475) |
| 22 | [1476](https://ybt.ssoier.cn/problem_show.php?pid=1476) | Secret Message 秘密信息 | [ROJ 1476](/problem/1476) |
| 23 | [1477](https://ybt.ssoier.cn/problem_show.php?pid=1477) | 【SCOI2016】背单词 | [ROJ 1477](/problem/1477) |
| 24 | [1478](https://ybt.ssoier.cn/problem_show.php?pid=1478) | The xor-longest Path | [ROJ 1478](/problem/1478)（ROJ 题名：「一本通 2.3 练习 5」The Xor-longest Path） |
| 25 | [1479](https://ybt.ssoier.cn/problem_show.php?pid=1479) | 【例题1】Keywords Search | [ROJ 1479](/problem/1479) |
| 26 | [1480](https://ybt.ssoier.cn/problem_show.php?pid=1480) | 玄武密码 | [ROJ 1480](/problem/1480) |
| 27 | [1481](https://ybt.ssoier.cn/problem_show.php?pid=1481) | Censoring | [ROJ 1481](/problem/1481) |
| 28 | [1482](https://ybt.ssoier.cn/problem_show.php?pid=1482) | 单词 | [ROJ 1482](/problem/1482) |
| 29 | [1483](https://ybt.ssoier.cn/problem_show.php?pid=1483) | 最短母串 | [ROJ 1483](/problem/1483) |
| 30 | [1484](https://ybt.ssoier.cn/problem_show.php?pid=1484) | 病毒 | [ROJ 1484](/problem/1484) |
| 31 | [1485](https://ybt.ssoier.cn/problem_show.php?pid=1485) | 文本生成器 | [ROJ 1485](/problem/1485) |

<a id="sec-7"></a>
#### 第1章 哈希和哈希表

<a id="sec-8"></a>
#### 第2章 KMP算法

<a id="sec-9"></a>
#### 第3章 trie字典树

<a id="sec-10"></a>
#### 第4章 AC自动机

<a id="sec-11"></a>
### 三、图论(提高篇)

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1486](https://ybt.ssoier.cn/problem_show.php?pid=1486) | 【例题1】黑暗城堡 | [ROJ 1486](/problem/1486) |
| 2 | [1487](https://ybt.ssoier.cn/problem_show.php?pid=1487) | 【例 2】北极通讯网络 | [ROJ 1487](/problem/1487) |
| 3 | [1488](https://ybt.ssoier.cn/problem_show.php?pid=1488) | 新的开始 | [ROJ 1488](/problem/1488) |
| 4 | [1489](https://ybt.ssoier.cn/problem_show.php?pid=1489) | 构造完全图 | [ROJ 1489](/problem/1489) |
| 5 | [1490](https://ybt.ssoier.cn/problem_show.php?pid=1490) | 秘密的牛奶运输 | [ROJ 1490](/problem/1490) |
| 6 | [1491](https://ybt.ssoier.cn/problem_show.php?pid=1491) | Tree | [ROJ 1491](/problem/1491) |
| 7 | [1492](https://ybt.ssoier.cn/problem_show.php?pid=1492) | 最小生成树计数 | [ROJ 1492](/problem/1492) |
| 8 | [1493](https://ybt.ssoier.cn/problem_show.php?pid=1493) | 次小生成树 | [ROJ 1493](/problem/1493) |
| 9 | [1494](https://ybt.ssoier.cn/problem_show.php?pid=1494) | 【例 1】Sightseeing Trip | [ROJ 1494](/problem/1494) |
| 10 | [1495](https://ybt.ssoier.cn/problem_show.php?pid=1495) | 【例 2】孤岛营救问题 | [ROJ 1495](/problem/1495)（ROJ 题名：「一本通 3.2 例 2」拯救大兵瑞恩） |
| 11 | [1496](https://ybt.ssoier.cn/problem_show.php?pid=1496) | 【例 3】架设电话线 | [ROJ 1496](/problem/1496) |
| 12 | [1497](https://ybt.ssoier.cn/problem_show.php?pid=1497) | 农场派对 | [ROJ 1497](/problem/1497) |
| 13 | [1498](https://ybt.ssoier.cn/problem_show.php?pid=1498) | Roadblocks | [ROJ 1498](/problem/1498) |
| 14 | [1499](https://ybt.ssoier.cn/problem_show.php?pid=1499) | 最短路计数 | [ROJ 1499](/problem/1499) |
| 15 | [1500](https://ybt.ssoier.cn/problem_show.php?pid=1500) | 新年好 | [ROJ 1500](/problem/1500) |
| 16 | [1501](https://ybt.ssoier.cn/problem_show.php?pid=1501) | 最优贸易 | [ROJ 1501](/problem/1501) |
| 17 | [1502](https://ybt.ssoier.cn/problem_show.php?pid=1502) | 汽车加油行驶问题 | [ROJ 1502](/problem/1502)（ROJ 题名：「一本通 3.2 练习 6」汽车加油行驶） |
| 18 | [1503](https://ybt.ssoier.cn/problem_show.php?pid=1503) | 道路和航线 | [ROJ 1503](/problem/1503) |
| 19 | [1504](https://ybt.ssoier.cn/problem_show.php?pid=1504) |  【例 1】Word Rings | [ROJ 1504](/problem/1504) |
| 20 | [1505](https://ybt.ssoier.cn/problem_show.php?pid=1505) | 【例 2】双调路径 | [ROJ 1505](/problem/1505) |
| 21 | [1506](https://ybt.ssoier.cn/problem_show.php?pid=1506) | 最小圈 | [ROJ 1506](/problem/1506) |
| 22 | [1507](https://ybt.ssoier.cn/problem_show.php?pid=1507) | 虫洞 Wormholes | [ROJ 1507](/problem/1507)（ROJ 题名：「一本通 3.3 练习 2」虫洞） |
| 23 | [1508](https://ybt.ssoier.cn/problem_show.php?pid=1508) | Easy SSSP | [ROJ 1508](/problem/1508) |
| 24 | [1509](https://ybt.ssoier.cn/problem_show.php?pid=1509) | 【例 1】Intervals | [ROJ 1509](/problem/1509) |
| 25 | [1510](https://ybt.ssoier.cn/problem_show.php?pid=1510) | 【例 2】出纳员问题 | [ROJ 1510](/problem/1510) |
| 26 | [1511](https://ybt.ssoier.cn/problem_show.php?pid=1511) | 【SCOI2011】糖果 | [ROJ 1511](/problem/1511) |
| 27 | [1512](https://ybt.ssoier.cn/problem_show.php?pid=1512) | 排队布局 | [ROJ 1512](/problem/1512) |
| 28 | [1513](https://ybt.ssoier.cn/problem_show.php?pid=1513) | 【 例 1】受欢迎的牛 | [ROJ 1513](/problem/1513) |
| 29 | [1514](https://ybt.ssoier.cn/problem_show.php?pid=1514) | 【例 2】最大半连通子图 | [ROJ 1514](/problem/1514) |
| 30 | [1515](https://ybt.ssoier.cn/problem_show.php?pid=1515) | 网络协议 | [ROJ 1515](/problem/1515) |
| 31 | [1516](https://ybt.ssoier.cn/problem_show.php?pid=1516) | 消息的传递 | [ROJ 1516](/problem/1516) |
| 32 | [1517](https://ybt.ssoier.cn/problem_show.php?pid=1517) | 间谍网络 | [ROJ 1517](/problem/1517) |
| 33 | [1518](https://ybt.ssoier.cn/problem_show.php?pid=1518) | 抢掠计划 | [ROJ 1518](/problem/1518) |
| 34 | [1519](https://ybt.ssoier.cn/problem_show.php?pid=1519) | 和平委员会 | [ROJ 1519](/problem/1519) |
| 35 | [1520](https://ybt.ssoier.cn/problem_show.php?pid=1520) | 【 例 1】分离的路径 | [ROJ 1520](/problem/1520) |
| 36 | [1521](https://ybt.ssoier.cn/problem_show.php?pid=1521) | 【 例 2】矿场搭建 | [ROJ 1521](/problem/1521) |
| 37 | [1522](https://ybt.ssoier.cn/problem_show.php?pid=1522) | 网络 | [ROJ 1522](/problem/1522) |
| 38 | [1523](https://ybt.ssoier.cn/problem_show.php?pid=1523) | 嗅探器 | [ROJ 1523](/problem/1523) |
| 39 | [1524](https://ybt.ssoier.cn/problem_show.php?pid=1524) | 旅游航道 | [ROJ 1524](/problem/1524) |
| 40 | [1525](https://ybt.ssoier.cn/problem_show.php?pid=1525) | 电力 | [ROJ 1525](/problem/1525) |
| 41 | [1526](https://ybt.ssoier.cn/problem_show.php?pid=1526) | Blockade | [ROJ 1526](/problem/1526) |
| 42 | [1527](https://ybt.ssoier.cn/problem_show.php?pid=1527) | 【例 1】欧拉回路 | [ROJ 1527](/problem/1527) |
| 43 | [1528](https://ybt.ssoier.cn/problem_show.php?pid=1528) | 【例 2】单词游戏 | [ROJ 1528](/problem/1528) |
| 44 | [1529](https://ybt.ssoier.cn/problem_show.php?pid=1529) | 欧拉回路 | [ROJ 1529](/problem/1529) |
| 45 | [1530](https://ybt.ssoier.cn/problem_show.php?pid=1530) | Ant Trip | [ROJ 1530](/problem/1530) |
| 46 | [1531](https://ybt.ssoier.cn/problem_show.php?pid=1531) | John‘s Trip | [ROJ 1531](/problem/1531)（ROJ 题名：「一本通 3.7 练习 3」John's Trip） |
| 47 | [1532](https://ybt.ssoier.cn/problem_show.php?pid=1532) | 太鼓达人 | [ROJ 1532](/problem/1532) |
| 48 | [1533](https://ybt.ssoier.cn/problem_show.php?pid=1533) | 相框 | [ROJ 1533](/problem/1533) |
| 49 | [1534](https://ybt.ssoier.cn/problem_show.php?pid=1534) | 原始生物 | [ROJ 1534](/problem/1534) |

<a id="sec-12"></a>
#### 第1章 最小生成树

<a id="sec-13"></a>
#### 第2章 最短路问题

<a id="sec-14"></a>
#### 第3章 SPFA算法优化

<a id="sec-15"></a>
#### 第4章 差分约束系统

<a id="sec-16"></a>
#### 第5章 强连通分量

<a id="sec-17"></a>
#### 第6章 割点和桥

<a id="sec-18"></a>
#### 第7章 欧拉回路

<a id="sec-19"></a>
### 四、数据结构(提高篇)

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1535](https://ybt.ssoier.cn/problem_show.php?pid=1535) | 【例 1】数列操作 | [ROJ 1535](/problem/1535) |
| 2 | [1536](https://ybt.ssoier.cn/problem_show.php?pid=1536) | 【例 2】数星星 Stars | [ROJ 1536](/problem/1536) |
| 3 | [1537](https://ybt.ssoier.cn/problem_show.php?pid=1537) | 【例 3】校门外的树 | [ROJ 1537](/problem/1537) |
| 4 | [1538](https://ybt.ssoier.cn/problem_show.php?pid=1538) | 清点人数 | [ROJ 1538](/problem/1538) |
| 5 | [1539](https://ybt.ssoier.cn/problem_show.php?pid=1539) | 简单题 | [ROJ 1539](/problem/1539) |
| 6 | [1540](https://ybt.ssoier.cn/problem_show.php?pid=1540) | 打鼹鼠_二维树状数组 | [ROJ 1540](/problem/1540)（ROJ 题名：「一本通 4.1 练习 3」打鼹鼠） |
| 7 | [1541](https://ybt.ssoier.cn/problem_show.php?pid=1541) | 【例 1】数列区间最大值 | [ROJ 1541](/problem/1541) |
| 8 | [1542](https://ybt.ssoier.cn/problem_show.php?pid=1542) | 【例 2】最敏捷的机器人 | [ROJ 1542](/problem/1542) |
| 9 | [1543](https://ybt.ssoier.cn/problem_show.php?pid=1543) | 【例 3】与众不同 | [ROJ 1543](/problem/1543) |
| 10 | [1544](https://ybt.ssoier.cn/problem_show.php?pid=1544) | 天才的记忆 | [ROJ 1544](/problem/1544) |
| 11 | [1545](https://ybt.ssoier.cn/problem_show.php?pid=1545) | Balanced Lineup | [ROJ 1545](/problem/1545)（ROJ 题名：「一本通 4.2 练习 2」奶牛排队 Balanced Lineup） |
| 12 | [1546](https://ybt.ssoier.cn/problem_show.php?pid=1546) | NOIP2011 选择客栈 | [ROJ 1546](/problem/1546)（ROJ 题名：「一本通 4.2 练习 3」选择客栈） |
| 13 | [1547](https://ybt.ssoier.cn/problem_show.php?pid=1547) | 【 例 1】区间和 | [ROJ 1547](/problem/1547) |
| 14 | [1548](https://ybt.ssoier.cn/problem_show.php?pid=1548) | 【例 2】A Simple Problem with Integers | [ROJ 1548](/problem/1548) |
| 15 | [1549](https://ybt.ssoier.cn/problem_show.php?pid=1549) | 最大数 | [ROJ 1549](/problem/1549) |
| 16 | [1550](https://ybt.ssoier.cn/problem_show.php?pid=1550) | 花神游历各国 | [ROJ 1550](/problem/1550) |
| 17 | [1551](https://ybt.ssoier.cn/problem_show.php?pid=1551) | 维护序列 | [ROJ 1551](/problem/1551) |
| 18 | [1992](https://ybt.ssoier.cn/problem_show.php?pid=1992) | 书架book | [ROJ 1992](/problem/1992) |
| 19 | [1993](https://ybt.ssoier.cn/problem_show.php?pid=1993) | 开关switch | [ROJ 1993](/problem/1993) |
| 20 | [1994](https://ybt.ssoier.cn/problem_show.php?pid=1994) | 音乐会 | [ROJ 1994](/problem/1994) |
| 21 | [1552](https://ybt.ssoier.cn/problem_show.php?pid=1552) | 【例 1】点的距离 | [ROJ 1552](/problem/1552) |
| 22 | [1553](https://ybt.ssoier.cn/problem_show.php?pid=1553) | 【例 2】暗的连锁 | [ROJ 1553](/problem/1553) |
| 23 | [1554](https://ybt.ssoier.cn/problem_show.php?pid=1554) | 【例 3】异象石 | [ROJ 1554](/problem/1554) |
| 24 | [1555](https://ybt.ssoier.cn/problem_show.php?pid=1555) | 【例 4】次小生成树 | [ROJ 1555](/problem/1555) |
| 25 | [1556](https://ybt.ssoier.cn/problem_show.php?pid=1556) | Dis | [ROJ 1556](/problem/1556) |
| 26 | [1557](https://ybt.ssoier.cn/problem_show.php?pid=1557) | 祖孙询问 | [ROJ 1557](/problem/1557) |
| 27 | [1558](https://ybt.ssoier.cn/problem_show.php?pid=1558) | 聚会 | [ROJ 1558](/problem/1558) |
| 28 | [1559](https://ybt.ssoier.cn/problem_show.php?pid=1559) | 跳跳棋 | [ROJ 1559](/problem/1559) |
| 29 | [1560](https://ybt.ssoier.cn/problem_show.php?pid=1560) | 【例 1】树的统计 | [ROJ 1560](/problem/1560) |
| 30 | [1561](https://ybt.ssoier.cn/problem_show.php?pid=1561) | 「HAOI2015」树上操作 | [ROJ 1561](/problem/1561) |
| 31 | [1562](https://ybt.ssoier.cn/problem_show.php?pid=1562) | 「NOI2015」软件包管理器 | [ROJ 1562](/problem/1562) |
| 32 | [1563](https://ybt.ssoier.cn/problem_show.php?pid=1563) | 染色 | [ROJ 1563](/problem/1563) |
| 33 | [1564](https://ybt.ssoier.cn/problem_show.php?pid=1564) | 「SDOI2014」旅行 | [ROJ 1564](/problem/1564) |
| 34 | [1565](https://ybt.ssoier.cn/problem_show.php?pid=1565) | 【例 1】营业额统计 | [ROJ 1565](/problem/1565) |
| 35 | [1566](https://ybt.ssoier.cn/problem_show.php?pid=1566) | 宠物收养所 | [ROJ 1566](/problem/1566) |
| 36 | [1567](https://ybt.ssoier.cn/problem_show.php?pid=1567) | 郁闷的出纳员 | [ROJ 1567](/problem/1567) |
| 37 | [1568](https://ybt.ssoier.cn/problem_show.php?pid=1568) | 普通平衡树 | [ROJ 1568](/problem/1568) |

<a id="sec-20"></a>
#### 第1章 树状数组

<a id="sec-21"></a>
#### 第2章 RMQ 问题

<a id="sec-22"></a>
#### 第3章 线段树

<a id="sec-23"></a>
#### 第4章 倍增求 LCA

<a id="sec-24"></a>
#### 第5章 树链剖分

<a id="sec-25"></a>
#### 第6章 平衡树 Treap

<a id="sec-26"></a>
### 五、动态规划(提高篇)

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1569](https://ybt.ssoier.cn/problem_show.php?pid=1569) | 【 例 1】石子合并 | [ROJ 1569](/problem/1569) |
| 2 | [1570](https://ybt.ssoier.cn/problem_show.php?pid=1570) | 【例 2】能量项链 | [ROJ 1570](/problem/1570) |
| 3 | [1571](https://ybt.ssoier.cn/problem_show.php?pid=1571) | 【例 3】凸多边形的划分 | [ROJ 1571](/problem/1571) |
| 4 | [1572](https://ybt.ssoier.cn/problem_show.php?pid=1572) | 括号配对 | [ROJ 1572](/problem/1572) |
| 5 | [1573](https://ybt.ssoier.cn/problem_show.php?pid=1573) | 分离与合体 | [ROJ 1573](/problem/1573) |
| 6 | [1574](https://ybt.ssoier.cn/problem_show.php?pid=1574) | 矩阵取数游戏 | [ROJ 1574](/problem/1574) |
| 7 | [1575](https://ybt.ssoier.cn/problem_show.php?pid=1575) | 【例 1】二叉苹果树 | [ROJ 1575](/problem/1575) |
| 8 | [1576](https://ybt.ssoier.cn/problem_show.php?pid=1576) | 【例 2】选课 | [ROJ 1576](/problem/1576) |
| 9 | [1577](https://ybt.ssoier.cn/problem_show.php?pid=1577) | 【例 3】数字转换 | [ROJ 1577](/problem/1577) |
| 10 | [1578](https://ybt.ssoier.cn/problem_show.php?pid=1578) | 【例 4】战略游戏 | [ROJ 1578](/problem/1578) |
| 11 | [1579](https://ybt.ssoier.cn/problem_show.php?pid=1579) |  【例 5】皇宫看守 | [ROJ 1579](/problem/1579) |
| 12 | [1580](https://ybt.ssoier.cn/problem_show.php?pid=1580) | 加分二叉树 | [ROJ 1580](/problem/1580) |
| 13 | [1581](https://ybt.ssoier.cn/problem_show.php?pid=1581) | 旅游规划 | [ROJ 1581](/problem/1581) |
| 14 | [1582](https://ybt.ssoier.cn/problem_show.php?pid=1582) | 周年纪念晚会 | [ROJ 1582](/problem/1582) |
| 15 | [1583](https://ybt.ssoier.cn/problem_show.php?pid=1583) | 叶子的染色 | [ROJ 1583](/problem/1583)（ROJ 题名：「一本通 5.2 练习 4」叶子的颜色） |
| 16 | [1584](https://ybt.ssoier.cn/problem_show.php?pid=1584) | 骑士 | [ROJ 1584](/problem/1584) |
| 17 | [1585](https://ybt.ssoier.cn/problem_show.php?pid=1585) |  【例 1】Amount of Degrees | [ROJ 1585](/problem/1585) |
| 18 | [1586](https://ybt.ssoier.cn/problem_show.php?pid=1586) | 【 例 2】数字游戏 | [ROJ 1586](/problem/1586) |
| 19 | [1587](https://ybt.ssoier.cn/problem_show.php?pid=1587) |  【例 3】Windy 数 | [ROJ 1587](/problem/1587) |
| 20 | [1588](https://ybt.ssoier.cn/problem_show.php?pid=1588) | 数字游戏 | [ROJ 1588](/problem/1588) |
| 21 | [1589](https://ybt.ssoier.cn/problem_show.php?pid=1589) | 不要 62 | [ROJ 1589](/problem/1589) |
| 22 | [1590](https://ybt.ssoier.cn/problem_show.php?pid=1590) | 恨 7 不成妻 | [ROJ 1590](/problem/1590) |
| 23 | [1591](https://ybt.ssoier.cn/problem_show.php?pid=1591) | 数字计数 | [ROJ 1591](/problem/1591) |
| 24 | [1592](https://ybt.ssoier.cn/problem_show.php?pid=1592) | 【例 1】国王 | [ROJ 1592](/problem/1592)（ROJ 题名：「一本通 5.4 例 1」骑士） |
| 25 | [1593](https://ybt.ssoier.cn/problem_show.php?pid=1593) | 【例 2】牧场的安排 | [ROJ 1593](/problem/1593) |
| 26 | [1594](https://ybt.ssoier.cn/problem_show.php?pid=1594) | 涂抹果酱 | [ROJ 1594](/problem/1594) |
| 27 | [1595](https://ybt.ssoier.cn/problem_show.php?pid=1595) | 炮兵阵地 | [ROJ 1595](/problem/1595) |
| 28 | [1596](https://ybt.ssoier.cn/problem_show.php?pid=1596) | 动物园 | [ROJ 1596](/problem/1596) |
| 29 | [1597](https://ybt.ssoier.cn/problem_show.php?pid=1597) | 【 例 1】滑动窗口 | [ROJ 1597](/problem/1597) |
| 30 | [1598](https://ybt.ssoier.cn/problem_show.php?pid=1598) | 【 例 2】最大连续和 | [ROJ 1598](/problem/1598) |
| 31 | [1599](https://ybt.ssoier.cn/problem_show.php?pid=1599) | 【 例 3】修剪草坪 | [ROJ 1599](/problem/1599) |
| 32 | [1600](https://ybt.ssoier.cn/problem_show.php?pid=1600) | 【例 4】旅行问题 | [ROJ 1600](/problem/1600) |
| 33 | [1601](https://ybt.ssoier.cn/problem_show.php?pid=1601) | 【例 5】Banknotes | [ROJ 1601](/problem/1601) |
| 34 | [1602](https://ybt.ssoier.cn/problem_show.php?pid=1602) | 烽火传递 | [ROJ 1602](/problem/1602) |
| 35 | [1603](https://ybt.ssoier.cn/problem_show.php?pid=1603) | 绿色通道 | [ROJ 1603](/problem/1603) |
| 36 | [1604](https://ybt.ssoier.cn/problem_show.php?pid=1604) | 理想的正方形 | [ROJ 1604](/problem/1604) |
| 37 | [1605](https://ybt.ssoier.cn/problem_show.php?pid=1605) | 股票交易 | [ROJ 1605](/problem/1605) |
| 38 | [1606](https://ybt.ssoier.cn/problem_show.php?pid=1606) | 【 例 1】任务安排 1 | [ROJ 1606](/problem/1606) |
| 39 | [1607](https://ybt.ssoier.cn/problem_show.php?pid=1607) | 【 例 2】任务安排 2 | [ROJ 1607](/problem/1607) |
| 40 | [1608](https://ybt.ssoier.cn/problem_show.php?pid=1608) | 【 例 3】任务安排 3 | [ROJ 1608](/problem/1608) |
| 41 | [1609](https://ybt.ssoier.cn/problem_show.php?pid=1609) | 【例 4】Cats Transport | [ROJ 1609](/problem/1609) |
| 42 | [1610](https://ybt.ssoier.cn/problem_show.php?pid=1610) | 玩具装箱 | [ROJ 1610](/problem/1610) |
| 43 | [1611](https://ybt.ssoier.cn/problem_show.php?pid=1611) | 仓库建设 | [ROJ 1611](/problem/1611) |
| 44 | [1612](https://ybt.ssoier.cn/problem_show.php?pid=1612) | 特别行动队 | [ROJ 1612](/problem/1612) |
| 45 | [1613](https://ybt.ssoier.cn/problem_show.php?pid=1613) | 打印文章 | [ROJ 1613](/problem/1613) |
| 46 | [1614](https://ybt.ssoier.cn/problem_show.php?pid=1614) | 锯木厂选址 | [ROJ 1614](/problem/1614) |

<a id="sec-27"></a>
#### 第1章 区间类动态规划

<a id="sec-28"></a>
#### 第2章 树型动态规划

<a id="sec-29"></a>
#### 第3章 数位动态规划

<a id="sec-30"></a>
#### 第4章 状态压缩类动态规划

<a id="sec-31"></a>
#### 第5章 单调队列优化动态规划

<a id="sec-32"></a>
#### 第6章 斜率优化动态规划

<a id="sec-33"></a>
### 六、数学基础(提高篇)

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1615](https://ybt.ssoier.cn/problem_show.php?pid=1615) | 【例 1】序列的第 k 个数 | [ROJ 1615](/problem/1615)（ROJ 题名：「一本通 6.1 例 1」序列的### 第 k 个数） |
| 2 | [1616](https://ybt.ssoier.cn/problem_show.php?pid=1616) | A 的 B 次方 | [ROJ 1616](/problem/1616) |
| 3 | [1617](https://ybt.ssoier.cn/problem_show.php?pid=1617) | 转圈游戏 | [ROJ 1617](/problem/1617) |
| 4 | [1618](https://ybt.ssoier.cn/problem_show.php?pid=1618) | 越狱 | [ROJ 1618](/problem/1618) |
| 5 | [1619](https://ybt.ssoier.cn/problem_show.php?pid=1619) |  【例 1】Prime Distance | [ROJ 1619](/problem/1619) |
| 6 | [1620](https://ybt.ssoier.cn/problem_show.php?pid=1620) | 质因数分解 | [ROJ 1620](/problem/1620) |
| 7 | [1621](https://ybt.ssoier.cn/problem_show.php?pid=1621) | 轻拍牛头 | [ROJ 1621](/problem/1621) |
| 8 | [1622](https://ybt.ssoier.cn/problem_show.php?pid=1622) | Goldbach’s Conjecture | [ROJ 1622](/problem/1622)（ROJ 题名：「一本通 6.2 练习 3」Goldbach's Conjecture） |
| 9 | [1623](https://ybt.ssoier.cn/problem_show.php?pid=1623) | Sherlock and His Girlfriend | [ROJ 1623](/problem/1623) |
| 10 | [1624](https://ybt.ssoier.cn/problem_show.php?pid=1624) | 樱花 | [ROJ 1624](/problem/1624) |
| 11 | [1625](https://ybt.ssoier.cn/problem_show.php?pid=1625) |  【例 1】反素数 Antiprime | [ROJ 1625](/problem/1625) |
| 12 | [1626](https://ybt.ssoier.cn/problem_show.php?pid=1626) | 【例 2】Hankson 的趣味题 | [ROJ 1626](/problem/1626) |
| 13 | [1627](https://ybt.ssoier.cn/problem_show.php?pid=1627) | 【例 3】最大公约数 | [ROJ 1627](/problem/1627) |
| 14 | [1628](https://ybt.ssoier.cn/problem_show.php?pid=1628) | X-factor Chain | [ROJ 1628](/problem/1628) |
| 15 | [1629](https://ybt.ssoier.cn/problem_show.php?pid=1629) | 聪明的燕姿 | [ROJ 1629](/problem/1629) |
| 16 | [1630](https://ybt.ssoier.cn/problem_show.php?pid=1630) | SuperGCD | [ROJ 1630](/problem/1630) |
| 17 | [1631](https://ybt.ssoier.cn/problem_show.php?pid=1631) | 【例 1】青蛙的约会 | [ROJ 1631](/problem/1631) |
| 18 | [1632](https://ybt.ssoier.cn/problem_show.php?pid=1632) | 【 例 2】[NOIP2012]同余方程 | [ROJ 1632](/problem/1632) |
| 19 | [1633](https://ybt.ssoier.cn/problem_show.php?pid=1633) | 【例 3】Sumdiv | [ROJ 1633](/problem/1633) |
| 20 | [1634](https://ybt.ssoier.cn/problem_show.php?pid=1634) | 【例 4】曹冲养猪 | [ROJ 1634](/problem/1634) |
| 21 | [1635](https://ybt.ssoier.cn/problem_show.php?pid=1635) | 【例 5】Strange Way to Express Integers | [ROJ 1635](/problem/1635) |
| 22 | [1636](https://ybt.ssoier.cn/problem_show.php?pid=1636) | 【例 6】计算器 | [ROJ 1636](/problem/1636) |
| 23 | [1637](https://ybt.ssoier.cn/problem_show.php?pid=1637) | 荒岛野人 | [ROJ 1637](/problem/1637) |
| 24 | [1638](https://ybt.ssoier.cn/problem_show.php?pid=1638) | 五指山 | [ROJ 1638](/problem/1638) |
| 25 | [1639](https://ybt.ssoier.cn/problem_show.php?pid=1639) | Biorhythms | [ROJ 1639](/problem/1639) |
| 26 | [1640](https://ybt.ssoier.cn/problem_show.php?pid=1640) | C Looooops | [ROJ 1640](/problem/1640) |
| 27 | [1641](https://ybt.ssoier.cn/problem_show.php?pid=1641) |  【例 1】矩阵 A×B | [ROJ 1641](/problem/1641) |
| 28 | [1642](https://ybt.ssoier.cn/problem_show.php?pid=1642) |  【例 2】Fibonacci 第 n 项 | [ROJ 1642](/problem/1642)（ROJ 题名：「一本通 6.5 例 2」Fibonacci ### 第 n 项） |
| 29 | [1643](https://ybt.ssoier.cn/problem_show.php?pid=1643) | 【例 3】Fibonacci 前 n 项和 | [ROJ 1643](/problem/1643) |
| 30 | [1644](https://ybt.ssoier.cn/problem_show.php?pid=1644) | 【例 4】佳佳的 Fibonacci | [ROJ 1644](/problem/1644) |
| 31 | [1645](https://ybt.ssoier.cn/problem_show.php?pid=1645) | Fibonacci | [ROJ 1645](/problem/1645) |
| 32 | [1646](https://ybt.ssoier.cn/problem_show.php?pid=1646) | GT 考试 | [ROJ 1646](/problem/1646) |
| 33 | [1647](https://ybt.ssoier.cn/problem_show.php?pid=1647) | 迷路 | [ROJ 1647](/problem/1647) |
| 34 | [1648](https://ybt.ssoier.cn/problem_show.php?pid=1648) |  【例 1】「NOIP2011」计算系数 | [ROJ 1648](/problem/1648) |
| 35 | [1649](https://ybt.ssoier.cn/problem_show.php?pid=1649) | 【例 2】2^k 进制数 | [ROJ 1649](/problem/1649) |
| 36 | [1650](https://ybt.ssoier.cn/problem_show.php?pid=1650) | 【例 3】组合 | [ROJ 1650](/problem/1650) |
| 37 | [1651](https://ybt.ssoier.cn/problem_show.php?pid=1651) | 【例 4】古代猪文 | [ROJ 1651](/problem/1651) |
| 38 | [1652](https://ybt.ssoier.cn/problem_show.php?pid=1652) | 牡牛和牝牛 | [ROJ 1652](/problem/1652)（ROJ 题名：「一本通 6.6 练习 1」牡牛和牝） |
| 39 | [1653](https://ybt.ssoier.cn/problem_show.php?pid=1653) | 方程的解 | [ROJ 1653](/problem/1653) |
| 40 | [1654](https://ybt.ssoier.cn/problem_show.php?pid=1654) | 车的放置 | [ROJ 1654](/problem/1654) |
| 41 | [1655](https://ybt.ssoier.cn/problem_show.php?pid=1655) | 数三角形 | [ROJ 1655](/problem/1655) |
| 42 | [1656](https://ybt.ssoier.cn/problem_show.php?pid=1656) | Combination | [ROJ 1656](/problem/1656) |
| 43 | [1657](https://ybt.ssoier.cn/problem_show.php?pid=1657) | 序列统计 | [ROJ 1657](/problem/1657) |
| 44 | [1658](https://ybt.ssoier.cn/problem_show.php?pid=1658) | 超能粒子炮 · 改 | [ROJ 1658](/problem/1658) |
| 45 | [1659](https://ybt.ssoier.cn/problem_show.php?pid=1659) | 礼物 | [ROJ 1659](/problem/1659) |
| 46 | [1660](https://ybt.ssoier.cn/problem_show.php?pid=1660) | 网格 | [ROJ 1660](/problem/1660) |
| 47 | [1661](https://ybt.ssoier.cn/problem_show.php?pid=1661) | 有趣的数列 | [ROJ 1661](/problem/1661) |
| 48 | [1662](https://ybt.ssoier.cn/problem_show.php?pid=1662) | 树屋阶梯 | [ROJ 1662](/problem/1662) |
| 49 | [1663](https://ybt.ssoier.cn/problem_show.php?pid=1663) | 【 例 1】取石子游戏 1 | [ROJ 1663](/problem/1663) |
| 50 | [1664](https://ybt.ssoier.cn/problem_show.php?pid=1664) | 【例 2】取石子游戏 2 | [ROJ 1664](/problem/1664) |
| 51 | [1665](https://ybt.ssoier.cn/problem_show.php?pid=1665) | 【例 3】移棋子游戏 | [ROJ 1665](/problem/1665) |
| 52 | [1666](https://ybt.ssoier.cn/problem_show.php?pid=1666) | 取石子游戏 | [ROJ 1666](/problem/1666) |
| 53 | [1667](https://ybt.ssoier.cn/problem_show.php?pid=1667) | 巧克力棒 | [ROJ 1667](/problem/1667) |
| 54 | [1668](https://ybt.ssoier.cn/problem_show.php?pid=1668) | 取石子 | [ROJ 1668](/problem/1668) |
| 55 | [1669](https://ybt.ssoier.cn/problem_show.php?pid=1669) | S-Nim | [ROJ 1669](/problem/1669) |
| 56 | [1670](https://ybt.ssoier.cn/problem_show.php?pid=1670) | 取石子游戏 | [ROJ 1670](/problem/1670) |

<a id="sec-34"></a>
#### 第1章 快速幂

<a id="sec-35"></a>
#### 第2章 质数

<a id="sec-36"></a>
#### 第3章 约数

<a id="sec-37"></a>
#### 第4章 同余问题

<a id="sec-38"></a>
#### 第5章 矩阵乘法

<a id="sec-39"></a>
#### 第6章 组合数学

<a id="sec-40"></a>
#### 第7章 博弈论

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
