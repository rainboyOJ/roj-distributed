# roj-distributed

一个**分布式**的 OJ（Online Judge）系统：

- **题面与代码进 Git** —— 题目内容（`content.md`/`content.pdf`）、元数据（`config.json`）、题目代码（`std.cpp`、`data.py`）全部随仓库版本管理；
- **测试数据不进 Git** —— 数据本体通过 **BT（主要）+ HTTP（临时）** 分发，按题目打包成独立归档；
- **评测在本地完成** —— 网站只读展示题目与公开数据，用户的评测最终全部在本地进行。

## 核心流程

```text
GitHub(题面+代码+数据清单) ──浏览──> 只读题面站(web/)
                                  │
                                  └─ data.json 清单 → 按题打包 <id>.tar.zst
                                                        │
                                        csps 主站 + oidata 备用（HTTP, Range 续传）
                                                        │
                                            用户本地: 下载归档 → 解压 → 评测(roj.py test)
```

- 题目元数据与题面在仓库 `problems/<id>/` 下，站点启动时自动发现；
- 每题 `data.json` 只记录公开数据的清单（路径 + 大小），数据本体由 BT/HTTP 通道分发，不进仓库；
- 评测与提交无关：`roj.py test` 在本地编译运行、比对公开数据。

## 目录结构

```text
problems/      题目记录: config.json / content.md / std.cpp / data.json
contests/      比赛页面 (Markdown 记录)
problem-sets/  题目单 (Markdown 记录)
web/           只读题面站 (Fastify + Pug 服务端渲染, Vite 构建)
scripts/       迁移等辅助脚本
.agents/skills/ 导入与访问题目等工作流 (add-roj-problem / roj 等)
```

## 题目单

网站提供「题目单」功能（导航 → 题目单）：按主题/教材整理的刷题清单，题目链接直接跳站内题面，支持浏览器本地勾选进度（可导出/导入）。题目单文件放在 `problem-sets/` 下，详见 [web/README.md](web/README.md)。

现有题目单：

- [problem-sets/ybt.md](problem-sets/ybt.md)：按 [ybt.ssoier.cn](https://ybt.ssoier.cn/index.php) 左侧分类索引整理的《信息学奥赛一本通（C++版）》题目单（C++编程语言 / 基础算法 / 数据结构基础 / 算法提高篇 / 高手训练篇），逐题标注 ROJ 收录情况与同题异号对照。
  表格区由 `python3 scripts/gen_ybt_list.py` 生成（数据快照：`scripts/ybt_catalog.json`），引言与笔记可手工编辑。

## 本地运行

```sh
cd web
npm install
npm run build   # 先构建静态资源
npm run start   # 默认 http://127.0.0.1:3033/
```

环境变量：`PORT`、`HOST`、`ROJ_ROOT`（题目目录，默认 `web/../problems`）、`CONTESTS_ROOT`、`DOWNLOAD_CONFIG`。

## 命令行客户端

```sh
python3 .agents/skills/roj/scripts/roj.py list "二分"
python3 .agents/skills/roj/scripts/roj.py get 20015
python3 .agents/skills/roj/scripts/roj.py download 20015
python3 .agents/skills/roj/scripts/roj.py test 20015 main.cpp --download
```

客户端只读：检索/阅读题面、下载数据归档并本地评测。详见 `.agents/skills/roj/SKILL.md`。

## 导入新题目

导入遵循「先预览、后确认」的工作流，ID 分配与 manifest 生成均有配套脚本，详见 `.agents/skills/add-roj-problem/SKILL.md`。

## 数据分发

每题测试数据打包为不可变的 `<id>.tar.zst` 归档（内含 `data/`），经两条只读通道分发：`csps.de5.net`（主站）+ `oidata.cc.cd`（备用），均支持 Range 断点续传；不再提供单文件下载。通道配置见 `web/config.yaml`。

测试数据本地存放在各题目录的 `problems/<id>/data/`（gitignored，不进 Git）；`problems/<id>/data.json` 是其清单（路径/大小）。打包上传后若归档未更新，该题数据下载会 404。
