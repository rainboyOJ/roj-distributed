---
title: 一本通 · 高手训练篇
description: 《信息学奥赛一本通（C++版）》高手训练篇：149 题，本站收录 149（100%）。
tags: [一本通, 教材配套, 刷题计划, 高手训练篇]
order: 5
items: 149
covered: 149
source: https://ybt.ssoier.cn/index.php
---

按《信息学奥赛一本通（C++版）》在线题库 [ybt.ssoier.cn](https://ybt.ssoier.cn/index.php) 左侧「题库全部题目分类索引」整理的 **高手训练篇**，可对照原书顺序刷题。

## 怎么用这份单子

- **一本通题号** 链接到一本通原题页；**ROJ 收录** 列是站内链接，在本站点开直接看题面；
- ROJ 列为 `—` 表示 ROJ 暂未收录这道题（仍可去一本通原站做）；
- 括号里标注「ROJ 题名」的，表示 ROJ 侧题目名称与一本通不同（多为改名/换译），题面是同一道题；
- **附录 A** 列出 ROJ 中『同题不同编号』的情况，分「已核对」「待核对」两档可信度；
- 一本通题目单共 5 篇（C++编程语言 / 基础算法 / 数据结构基础 / 算法提高篇 / 高手训练篇），可在[题目单列表](/problem-sets)里切换；勾选进度在站内按题号全局共享，跨篇不会丢；
- 在 GitHub 上阅读时，`/problem/…` 是站内路径，需补上 `https://roj.ac.cn` 前缀才能点开。

<!-- ybt:generated:start -->

## 本篇概览

本篇 149 题，本站收录 149（100%）；一本通题目单共 5 篇、895 题。

## 目录

- [一、基础算法(高手训练)](#sec-1)
  - [第1章 贪心算法](#sec-2)
  - [第2章 二分与三分](#sec-3)
  - [第3章 深搜](#sec-4)
  - [第4章 广搜](#sec-5)
- [二、字符串算法(高手训练)](#sec-6)
  - [第1章 哈希表](#sec-7)
  - [第2章 KMP算法](#sec-8)
  - [第3章 Trie树](#sec-9)
  - [第4章 AC自动机](#sec-10)
- [三、图论(高手训练)](#sec-11)
  - [第1章 最小生成树](#sec-12)
  - [第2章 最短路径](#sec-13)
  - [第3章 SPFA算法的优化](#sec-14)
  - [第4章 差分约束系统](#sec-15)
  - [第5章 强连通分量](#sec-16)
  - [第6章 割点和桥](#sec-17)
  - [第7章 欧拉回路](#sec-18)
- [四、数据结构(高手训练)](#sec-19)
  - [第1章 树状数组](#sec-20)
  - [第2章 RMQ问题](#sec-21)
  - [第3章 线段树](#sec-22)
  - [第4章 倍增求LCA](#sec-23)
  - [第5章 树链剖分](#sec-24)
- [五、动态规划(高手训练)](#sec-25)
  - [第1章 区间类动态规划](#sec-26)
  - [第2章 树形动态规划](#sec-27)
  - [第3章 数位动态规划](#sec-28)
  - [第4章 状态压缩类动态规划](#sec-29)
  - [第5章 单调队列优化动态规划](#sec-30)
  - [第6章 斜率优化动态规划](#sec-31)
- [六、数学基础(高手训练)](#sec-32)
  - [第1章 快速幂矩乘](#sec-33)
  - [第2章 素数约数](#sec-34)
  - [第3章 同余问题](#sec-35)
  - [4章 组合数学](#sec-36)
  - [第5章 博弈论](#sec-37)
- [附录 A：同题异号对照](#appendix-a)

<a id="sec-0"></a>
## 高手训练篇

<a id="sec-1"></a>
### 一、基础算法(高手训练)

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1671](https://ybt.ssoier.cn/problem_show.php?pid=1671) | 扑克牌 | [ROJ 5007](/problem/5007)（ROJ 题号 5007） |
| 2 | [1672](https://ybt.ssoier.cn/problem_show.php?pid=1672) | 游戏通关 | [ROJ 5008](/problem/5008)（ROJ 题号 5008） |
| 3 | [1673](https://ybt.ssoier.cn/problem_show.php?pid=1673) | 楼间跳跃 | [ROJ 5009](/problem/5009)（ROJ 题号 5009） |
| 4 | [1674](https://ybt.ssoier.cn/problem_show.php?pid=1674) | 堆蛋糕 | [ROJ 5010](/problem/5010)（ROJ 题号 5010） |
| 5 | [1675](https://ybt.ssoier.cn/problem_show.php?pid=1675) | 塔 | [ROJ 5011](/problem/5011)（ROJ 题号 5011） |
| 6 | [1676](https://ybt.ssoier.cn/problem_show.php?pid=1676) | 手机游戏 | [ROJ 5012](/problem/5012)（ROJ 题号 5012） |
| 7 | [1677](https://ybt.ssoier.cn/problem_show.php?pid=1677) | 软件开发 | [ROJ 5013](/problem/5013)（ROJ 题号 5013） |
| 8 | [1678](https://ybt.ssoier.cn/problem_show.php?pid=1678) | 独木桥 | [ROJ 5014](/problem/5014)（ROJ 题号 5014） |
| 9 | [1679](https://ybt.ssoier.cn/problem_show.php?pid=1679) | 子集 | [ROJ 5015](/problem/5015)（ROJ 题号 5015） |
| 10 | [1680](https://ybt.ssoier.cn/problem_show.php?pid=1680) | 序列 | [ROJ 5016](/problem/5016)（ROJ 题号 5016） |
| 11 | [1681](https://ybt.ssoier.cn/problem_show.php?pid=1681) | 统计方案 | [ROJ 5017](/problem/5017)（ROJ 题号 5017） |
| 12 | [1682](https://ybt.ssoier.cn/problem_show.php?pid=1682) | 最小字典序 | [ROJ 1682](/problem/1682) |
| 13 | [1683](https://ybt.ssoier.cn/problem_show.php?pid=1683) | 稗田阿求 | [ROJ 1683](/problem/1683) |
| 14 | [1684](https://ybt.ssoier.cn/problem_show.php?pid=1684) | 翻转序列 | [ROJ 1684](/problem/1684) |
| 15 | [1685](https://ybt.ssoier.cn/problem_show.php?pid=1685) | 新版方格取数 | [ROJ 1685](/problem/1685) |
| 16 | [1686](https://ybt.ssoier.cn/problem_show.php?pid=1686) | 最小操作次数 | [ROJ 1686](/problem/1686) |
| 17 | [1687](https://ybt.ssoier.cn/problem_show.php?pid=1687) | 积水问题 | [ROJ 1687](/problem/1687) |
| 18 | [1688](https://ybt.ssoier.cn/problem_show.php?pid=1688) | 最优路径 | [ROJ 1688](/problem/1688) |
| 19 | [1689](https://ybt.ssoier.cn/problem_show.php?pid=1689) | 堆排问题 | [ROJ 1689](/problem/1689) |
| 20 | [1690](https://ybt.ssoier.cn/problem_show.php?pid=1690) | 棋盘问题 | [ROJ 1690](/problem/1690) |

<a id="sec-2"></a>
#### 第1章 贪心算法

<a id="sec-3"></a>
#### 第2章 二分与三分

<a id="sec-4"></a>
#### 第3章 深搜

<a id="sec-5"></a>
#### 第4章 广搜

<a id="sec-6"></a>
### 二、字符串算法(高手训练)

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1691](https://ybt.ssoier.cn/problem_show.php?pid=1691) | 文章评分 | [ROJ 1691](/problem/1691) |
| 2 | [1692](https://ybt.ssoier.cn/problem_show.php?pid=1692) | 字符串编码 | [ROJ 1692](/problem/1692) |
| 3 | [1693](https://ybt.ssoier.cn/problem_show.php?pid=1693) | 正确答案 | [ROJ 1693](/problem/1693) |
| 4 | [1694](https://ybt.ssoier.cn/problem_show.php?pid=1694) | 回文串 | [ROJ 1694](/problem/1694) |
| 5 | [1695](https://ybt.ssoier.cn/problem_show.php?pid=1695) | 独特的树叶 | [ROJ 1695](/problem/1695) |
| 6 | [1696](https://ybt.ssoier.cn/problem_show.php?pid=1696) | 前缀和 | [ROJ 1696](/problem/1696) |
| 7 | [1697](https://ybt.ssoier.cn/problem_show.php?pid=1697) | 深意 | [ROJ 1697](/problem/1697) |
| 8 | [1698](https://ybt.ssoier.cn/problem_show.php?pid=1698) | 字符串匹配 | [ROJ 1698](/problem/1698) |
| 9 | [1699](https://ybt.ssoier.cn/problem_show.php?pid=1699) | 石环 | [ROJ 1699](/problem/1699) |
| 10 | [1700](https://ybt.ssoier.cn/problem_show.php?pid=1700) | PFS集合 | [ROJ 1700](/problem/1700) |
| 11 | [1701](https://ybt.ssoier.cn/problem_show.php?pid=1701) | 最大值 | [ROJ 1701](/problem/1701) |
| 12 | [1702](https://ybt.ssoier.cn/problem_show.php?pid=1702) | 异或运算 | [ROJ 1702](/problem/1702) |
| 13 | [1703](https://ybt.ssoier.cn/problem_show.php?pid=1703) | 量子纠缠 | [ROJ 1703](/problem/1703) |
| 14 | [1704](https://ybt.ssoier.cn/problem_show.php?pid=1704) | 奇特的猫 | [ROJ 1704](/problem/1704) |
| 15 | [1705](https://ybt.ssoier.cn/problem_show.php?pid=1705) | DNA序列 | [ROJ 1705](/problem/1705) |
| 16 | [1706](https://ybt.ssoier.cn/problem_show.php?pid=1706) | 串包含问题 | [ROJ 1706](/problem/1706) |
| 17 | [1707](https://ybt.ssoier.cn/problem_show.php?pid=1707) | 敲键盘 | [ROJ 1707](/problem/1707) |
| 18 | [1708](https://ybt.ssoier.cn/problem_show.php?pid=1708) | 无限链计数 | [ROJ 1708](/problem/1708) |
| 19 | [1709](https://ybt.ssoier.cn/problem_show.php?pid=1709) | 寻找好串 | [ROJ 1709](/problem/1709) |

<a id="sec-7"></a>
#### 第1章 哈希表

<a id="sec-8"></a>
#### 第2章 KMP算法

<a id="sec-9"></a>
#### 第3章 Trie树

<a id="sec-10"></a>
#### 第4章 AC自动机

<a id="sec-11"></a>
### 三、图论(高手训练)

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1710](https://ybt.ssoier.cn/problem_show.php?pid=1710) | 构造完全图 | [ROJ 1710](/problem/1710) |
| 2 | [1711](https://ybt.ssoier.cn/problem_show.php?pid=1711) | 最小花费 | [ROJ 1711](/problem/1711) |
| 3 | [1712](https://ybt.ssoier.cn/problem_show.php?pid=1712) | 汉堡店 | [ROJ 1712](/problem/1712) |
| 4 | [1713](https://ybt.ssoier.cn/problem_show.php?pid=1713) | 生成树 | [ROJ 1713](/problem/1713) |
| 5 | [1714](https://ybt.ssoier.cn/problem_show.php?pid=1714) | 地壳运动 | [ROJ 1714](/problem/1714) |
| 6 | [1715](https://ybt.ssoier.cn/problem_show.php?pid=1715) | 公交旅行 | [ROJ 1715](/problem/1715) |
| 7 | [1716](https://ybt.ssoier.cn/problem_show.php?pid=1716) | 次短路计数 | [ROJ 1716](/problem/1716) |
| 8 | [1717](https://ybt.ssoier.cn/problem_show.php?pid=1717) | 负环 | [ROJ 1717](/problem/1717) |
| 9 | [1718](https://ybt.ssoier.cn/problem_show.php?pid=1718) | 益智游戏 | [ROJ 1718](/problem/1718) |
| 10 | [1719](https://ybt.ssoier.cn/problem_show.php?pid=1719) | 过河 | [ROJ 1719](/problem/1719) |
| 11 | [1720](https://ybt.ssoier.cn/problem_show.php?pid=1720) | 均值最小环 | [ROJ 1720](/problem/1720) |
| 12 | [1721](https://ybt.ssoier.cn/problem_show.php?pid=1721) | 最小边权和 | [ROJ 1721](/problem/1721) |
| 13 | [1722](https://ybt.ssoier.cn/problem_show.php?pid=1722) | 骑士游戏 | [ROJ 1722](/problem/1722) |
| 14 | [1723](https://ybt.ssoier.cn/problem_show.php?pid=1723) | 交通 | [ROJ 1723](/problem/1723) |
| 15 | [1724](https://ybt.ssoier.cn/problem_show.php?pid=1724) | 小K的农场 | [ROJ 1724](/problem/1724) |
| 16 | [1725](https://ybt.ssoier.cn/problem_show.php?pid=1725) | 账本核算 | [ROJ 1725](/problem/1725) |
| 17 | [1726](https://ybt.ssoier.cn/problem_show.php?pid=1726) | 矩阵 | [ROJ 1726](/problem/1726) |
| 18 | [1727](https://ybt.ssoier.cn/problem_show.php?pid=1727) | 魔棒 | [ROJ 1727](/problem/1727) |
| 19 | [1728](https://ybt.ssoier.cn/problem_show.php?pid=1728) | 构造序列 | [ROJ 1728](/problem/1728) |
| 20 | [1729](https://ybt.ssoier.cn/problem_show.php?pid=1729) | 魔法石 | [ROJ 1729](/problem/1729) |
| 21 | [1730](https://ybt.ssoier.cn/problem_show.php?pid=1730) | 二分图 | [ROJ 1730](/problem/1730) |
| 22 | [1731](https://ybt.ssoier.cn/problem_show.php?pid=1731) | 最大流 | [ROJ 1731](/problem/1731) |
| 23 | [1732](https://ybt.ssoier.cn/problem_show.php?pid=1732) | 情报传递 | [ROJ 1732](/problem/1732) |
| 24 | [1733](https://ybt.ssoier.cn/problem_show.php?pid=1733) | 连续数字区间 | [ROJ 1733](/problem/1733) |
| 25 | [1734](https://ybt.ssoier.cn/problem_show.php?pid=1734) | 删边问题 | [ROJ 1734](/problem/1734) |
| 26 | [1735](https://ybt.ssoier.cn/problem_show.php?pid=1735) | 环上计数 | [ROJ 1735](/problem/1735) |
| 27 | [1736](https://ybt.ssoier.cn/problem_show.php?pid=1736) | 最大连通块 | [ROJ 1736](/problem/1736) |
| 28 | [1737](https://ybt.ssoier.cn/problem_show.php?pid=1737) | 邮递员 | [ROJ 1737](/problem/1737) |
| 29 | [1738](https://ybt.ssoier.cn/problem_show.php?pid=1738) | 圆桌聚会 | [ROJ 1738](/problem/1738) |
| 30 | [1739](https://ybt.ssoier.cn/problem_show.php?pid=1739) | 观光巴士 | [ROJ 1739](/problem/1739) |
| 31 | [1740](https://ybt.ssoier.cn/problem_show.php?pid=1740) | 星空穿越 | [ROJ 1740](/problem/1740) |

<a id="sec-12"></a>
#### 第1章 最小生成树

<a id="sec-13"></a>
#### 第2章 最短路径

<a id="sec-14"></a>
#### 第3章 SPFA算法的优化

<a id="sec-15"></a>
#### 第4章 差分约束系统

<a id="sec-16"></a>
#### 第5章 强连通分量

<a id="sec-17"></a>
#### 第6章 割点和桥

<a id="sec-18"></a>
#### 第7章 欧拉回路

<a id="sec-19"></a>
### 四、数据结构(高手训练)

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1741](https://ybt.ssoier.cn/problem_show.php?pid=1741) | 电子速度 | [ROJ 1741](/problem/1741) |
| 2 | [1742](https://ybt.ssoier.cn/problem_show.php?pid=1742) | 导线问题 | [ROJ 1742](/problem/1742) |
| 3 | [1743](https://ybt.ssoier.cn/problem_show.php?pid=1743) | 数羊 | [ROJ 1743](/problem/1743) |
| 4 | [1744](https://ybt.ssoier.cn/problem_show.php?pid=1744) | 跳台阶 | [ROJ 1744](/problem/1744) |
| 5 | [1745](https://ybt.ssoier.cn/problem_show.php?pid=1745) | 分组 | [ROJ 1745](/problem/1745) |
| 6 | [1746](https://ybt.ssoier.cn/problem_show.php?pid=1746) | 矩阵最值 | [ROJ 1746](/problem/1746) |
| 7 | [1747](https://ybt.ssoier.cn/problem_show.php?pid=1747) | 奶牛排队 | [ROJ 1747](/problem/1747) |
| 8 | [1748](https://ybt.ssoier.cn/problem_show.php?pid=1748) | 大数计数 | [ROJ 1748](/problem/1748) |
| 9 | [1749](https://ybt.ssoier.cn/problem_show.php?pid=1749) | 矩阵求和 | [ROJ 1749](/problem/1749) |
| 10 | [1750](https://ybt.ssoier.cn/problem_show.php?pid=1750) | 取数字 | [ROJ 1750](/problem/1750) |
| 11 | [1751](https://ybt.ssoier.cn/problem_show.php?pid=1751) | 字符串排序 | [ROJ 1751](/problem/1751) |
| 12 | [1752](https://ybt.ssoier.cn/problem_show.php?pid=1752) | 纪念碑 | [ROJ 1752](/problem/1752) |
| 13 | [1753](https://ybt.ssoier.cn/problem_show.php?pid=1753) | 区间连通性 | [ROJ 1753](/problem/1753) |
| 14 | [1754](https://ybt.ssoier.cn/problem_show.php?pid=1754) | 栈的维护 | [ROJ 1754](/problem/1754) |
| 15 | [1755](https://ybt.ssoier.cn/problem_show.php?pid=1755) | 星际探测 | [ROJ 1755](/problem/1755) |
| 16 | [1756](https://ybt.ssoier.cn/problem_show.php?pid=1756) | 过路费 | [ROJ 1756](/problem/1756) |
| 17 | [1757](https://ybt.ssoier.cn/problem_show.php?pid=1757) | 避难向导 | [ROJ 1757](/problem/1757) |
| 18 | [1758](https://ybt.ssoier.cn/problem_show.php?pid=1758) | 连通能力 | [ROJ 1758](/problem/1758) |
| 19 | [1759](https://ybt.ssoier.cn/problem_show.php?pid=1759) | 采访计划 | [ROJ 1759](/problem/1759) |
| 20 | [1760](https://ybt.ssoier.cn/problem_show.php?pid=1760) | 树上数颜色 | [ROJ 1760](/problem/1760) |
| 21 | [1761](https://ybt.ssoier.cn/problem_show.php?pid=1761) | 最小割 | [ROJ 1761](/problem/1761) |
| 22 | [1762](https://ybt.ssoier.cn/problem_show.php?pid=1762) | 与非 | [ROJ 1762](/problem/1762) |
| 23 | [1763](https://ybt.ssoier.cn/problem_show.php?pid=1763) | 简单树 | [ROJ 1763](/problem/1763) |
| 24 | [1764](https://ybt.ssoier.cn/problem_show.php?pid=1764) | 社会送温暖 | [ROJ 1764](/problem/1764) |
| 25 | [1765](https://ybt.ssoier.cn/problem_show.php?pid=1765) | 树上斐波那契 | [ROJ 1765](/problem/1765) |

<a id="sec-20"></a>
#### 第1章 树状数组

<a id="sec-21"></a>
#### 第2章 RMQ问题

<a id="sec-22"></a>
#### 第3章 线段树

<a id="sec-23"></a>
#### 第4章 倍增求LCA

<a id="sec-24"></a>
#### 第5章 树链剖分

<a id="sec-25"></a>
### 五、动态规划(高手训练)

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1766](https://ybt.ssoier.cn/problem_show.php?pid=1766) | 成绩单 | [ROJ 1766](/problem/1766) |
| 2 | [1767](https://ybt.ssoier.cn/problem_show.php?pid=1767) | 字符合并 | [ROJ 1767](/problem/1767) |
| 3 | [1768](https://ybt.ssoier.cn/problem_show.php?pid=1768) | 交换 | [ROJ 1768](/problem/1768) |
| 4 | [1769](https://ybt.ssoier.cn/problem_show.php?pid=1769) | 景中人 | [ROJ 1769](/problem/1769) |
| 5 | [1770](https://ybt.ssoier.cn/problem_show.php?pid=1770) | 跳跳棋 | [ROJ 1770](/problem/1770) |
| 6 | [1771](https://ybt.ssoier.cn/problem_show.php?pid=1771) | 仓库选址 | [ROJ 1771](/problem/1771) |
| 7 | [1772](https://ybt.ssoier.cn/problem_show.php?pid=1772) | 动漫排序 | [ROJ 1772](/problem/1772) |
| 8 | [1773](https://ybt.ssoier.cn/problem_show.php?pid=1773) | 消息传递 | [ROJ 1773](/problem/1773) |
| 9 | [1774](https://ybt.ssoier.cn/problem_show.php?pid=1774) | 大逃杀 | [ROJ 1774](/problem/1774) |
| 10 | [1775](https://ybt.ssoier.cn/problem_show.php?pid=1775) | 梦中漫步 | [ROJ 1775](/problem/1775) |
| 11 | [1776](https://ybt.ssoier.cn/problem_show.php?pid=1776) | 最大值 | [ROJ 1776](/problem/1776) |
| 12 | [1777](https://ybt.ssoier.cn/problem_show.php?pid=1777) | 寻找整数 | [ROJ 1777](/problem/1777) |
| 13 | [1778](https://ybt.ssoier.cn/problem_show.php?pid=1778) | 好数字 | [ROJ 1778](/problem/1778) |
| 14 | [1779](https://ybt.ssoier.cn/problem_show.php?pid=1779) | 第K小数 | [ROJ 1779](/problem/1779) |
| 15 | [1780](https://ybt.ssoier.cn/problem_show.php?pid=1780) | 修墙 | [ROJ 1780](/problem/1780) |
| 16 | [1781](https://ybt.ssoier.cn/problem_show.php?pid=1781) | 死亡之树 | [ROJ 1781](/problem/1781) |
| 17 | [1782](https://ybt.ssoier.cn/problem_show.php?pid=1782) | 分层图 | [ROJ 1782](/problem/1782) |
| 18 | [1783](https://ybt.ssoier.cn/problem_show.php?pid=1783) | 矩阵填数 | [ROJ 1783](/problem/1783) |
| 19 | [1784](https://ybt.ssoier.cn/problem_show.php?pid=1784) | 山谷 | [ROJ 1784](/problem/1784) |
| 20 | [1785](https://ybt.ssoier.cn/problem_show.php?pid=1785) | 简单的期望 | [ROJ 1785](/problem/1785) |
| 21 | [1786](https://ybt.ssoier.cn/problem_show.php?pid=1786) | 01背包 | [ROJ 1786](/problem/1786) |
| 22 | [1787](https://ybt.ssoier.cn/problem_show.php?pid=1787) | 保龄球 | [ROJ 1787](/problem/1787) |
| 23 | [1788](https://ybt.ssoier.cn/problem_show.php?pid=1788) | 爬山 | [ROJ 1788](/problem/1788) |
| 24 | [1789](https://ybt.ssoier.cn/problem_show.php?pid=1789) | 分班 | [ROJ 1789](/problem/1789) |
| 25 | [1790](https://ybt.ssoier.cn/problem_show.php?pid=1790) | 序列划分 | [ROJ 1790](/problem/1790) |
| 26 | [1791](https://ybt.ssoier.cn/problem_show.php?pid=1791) | 太空飞船 | [ROJ 1791](/problem/1791) |
| 27 | [1792](https://ybt.ssoier.cn/problem_show.php?pid=1792) | 小P的牧场 | [ROJ 1792](/problem/1792) |
| 28 | [1793](https://ybt.ssoier.cn/problem_show.php?pid=1793) | 鏖战字符串 | [ROJ 1793](/problem/1793) |
| 29 | [1794](https://ybt.ssoier.cn/problem_show.php?pid=1794) | 分数 | [ROJ 1794](/problem/1794) |

<a id="sec-26"></a>
#### 第1章 区间类动态规划

<a id="sec-27"></a>
#### 第2章 树形动态规划

<a id="sec-28"></a>
#### 第3章 数位动态规划

<a id="sec-29"></a>
#### 第4章 状态压缩类动态规划

<a id="sec-30"></a>
#### 第5章 单调队列优化动态规划

<a id="sec-31"></a>
#### 第6章 斜率优化动态规划

<a id="sec-32"></a>
### 六、数学基础(高手训练)

| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |
| ---: | --- | --- | --- |
| 1 | [1795](https://ybt.ssoier.cn/problem_show.php?pid=1795) | 散步 | [ROJ 1795](/problem/1795) |
| 2 | [1796](https://ybt.ssoier.cn/problem_show.php?pid=1796) | 斐波那契串 | [ROJ 1796](/problem/1796) |
| 3 | [1797](https://ybt.ssoier.cn/problem_show.php?pid=1797) | K维斐波那契 | [ROJ 1797](/problem/1797) |
| 4 | [1798](https://ybt.ssoier.cn/problem_show.php?pid=1798) | 递推数列 | [ROJ 1798](/problem/1798) |
| 5 | [1799](https://ybt.ssoier.cn/problem_show.php?pid=1799) | 数列 | [ROJ 1799](/problem/1799) |
| 6 | [1800](https://ybt.ssoier.cn/problem_show.php?pid=1800) | 质数 | [ROJ 1800](/problem/1800) |
| 7 | [1801](https://ybt.ssoier.cn/problem_show.php?pid=1801) | 异或 | [ROJ 1801](/problem/1801) |
| 8 | [1802](https://ybt.ssoier.cn/problem_show.php?pid=1802) | 寿司晚宴 | [ROJ 1802](/problem/1802) |
| 9 | [1803](https://ybt.ssoier.cn/problem_show.php?pid=1803) | 列数字 | [ROJ 1803](/problem/1803) |
| 10 | [1804](https://ybt.ssoier.cn/problem_show.php?pid=1804) | 最大真因数 | [ROJ 1804](/problem/1804) |
| 11 | [1805](https://ybt.ssoier.cn/problem_show.php?pid=1805) | 数数 | [ROJ 1805](/problem/1805) |
| 12 | [1806](https://ybt.ssoier.cn/problem_show.php?pid=1806) | 计算器 | [ROJ 1806](/problem/1806) |
| 13 | [1807](https://ybt.ssoier.cn/problem_show.php?pid=1807) | 区间计数 | [ROJ 1807](/problem/1807) |
| 14 | [1808](https://ybt.ssoier.cn/problem_show.php?pid=1808) | 斐波那契数列 | [ROJ 1808](/problem/1808) |
| 15 | [1809](https://ybt.ssoier.cn/problem_show.php?pid=1809) | 日食 | [ROJ 1809](/problem/1809) |
| 16 | [1810](https://ybt.ssoier.cn/problem_show.php?pid=1810) | 登山 | [ROJ 1810](/problem/1810) |
| 17 | [1811](https://ybt.ssoier.cn/problem_show.php?pid=1811) | 多项式相乘 | [ROJ 1811](/problem/1811) |
| 18 | [1812](https://ybt.ssoier.cn/problem_show.php?pid=1812) | 网格 | [ROJ 1812](/problem/1812) |
| 19 | [1813](https://ybt.ssoier.cn/problem_show.php?pid=1813) | 图的计数 | [ROJ 1813](/problem/1813) |
| 20 | [1814](https://ybt.ssoier.cn/problem_show.php?pid=1814) | 方格染色 | [ROJ 1814](/problem/1814) |
| 21 | [1815](https://ybt.ssoier.cn/problem_show.php?pid=1815) | 放石子 | [ROJ 1815](/problem/1815) |
| 22 | [1816](https://ybt.ssoier.cn/problem_show.php?pid=1816) | 取石子 | [ROJ 1816](/problem/1816) |
| 23 | [1817](https://ybt.ssoier.cn/problem_show.php?pid=1817) | 染色游戏 | [ROJ 1817](/problem/1817) |
| 24 | [1818](https://ybt.ssoier.cn/problem_show.php?pid=1818) | 树上取石子 | [ROJ 1818](/problem/1818) |
| 25 | [1819](https://ybt.ssoier.cn/problem_show.php?pid=1819) | 字符串游戏 | [ROJ 1819](/problem/1819) |

<a id="sec-33"></a>
#### 第1章 快速幂矩乘

<a id="sec-34"></a>
#### 第2章 素数约数

<a id="sec-35"></a>
#### 第3章 同余问题

<a id="sec-36"></a>
#### 4章 组合数学

<a id="sec-37"></a>
#### 第5章 博弈论

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
