# new_ROJ

一个分布式的 OJ 系统：题面与代码进 Git，测试数据不进 Git、按题打包成不可变的 `tar.zst` 归档，经两条只读通道（csps 主站 + oidata 备用）分发；用户的评测最终全部在本地完成。

## Language

**题目**:
一个可浏览、可本地评测的编程问题，由题目内容、题目代码和测试数据共同构成。
_Avoid_: 试题、任务

**题目内容**:
进入 Git 的、描述和识别题目的资料：`content.md`/`content.pdf`（题面）、`config.json`（title/time/memory）、`data.json`（公开数据清单）。
_Avoid_: 数据、元数据（`data.json` 是清单而非数据本体）

**题目代码**:
进入 Git 的、与题目相关的源代码：`std.cpp`（标程）、`data.py`（测试数据生成器）。
_Avoid_: 测试数据（生成器是脚本，不是数据本体）

**测试数据**:
不进 Git 的、用于评测的数据本体：`data/` 下的 `.in`/`.out`（及 `.ans` 等）以及派生的 `data.zip`。通过 BT（主要）+ HTTP（临时）分发。
_Avoid_: 数据、题目内容、公开数据
