# Library Checker 题目合并价值调研

> 背景：评估 [yosupo06/library-checker-problems](https://github.com/yosupo06/library-checker-problems)（judge.yosupo.jp 的题目源仓库）能否并入 ROJ 题库、价值几何。
> 调研时间 2026-10；数据为克隆仓库实测统计，工具链为本机实际运行验证。

## 结论速览

| 维度 | 结论 |
| --- | --- |
| 项目是什么 | judge.yosupo.jp 官方题目源，**算法/数据结构库的"验证题"（模板题）**，不是 OI 思维题 |
| 规模 | **253 题**，15 个类目；Apache 2.0 许可，**可合法再分发** |
| 有价值吗 | **有，且与 ROJ 现有题库高度互补**——ROJ 缺"纯模板题"，LC 缺中文题面和 OI 情境，正好拼上 |
| 能合并吗 | **能**。工具链已实测跑通（生成器出数据 → 标程出答案）；ROJ 已有先例：`problems/1415` 就是 `rectangle_add_point_get` 的中文化导入 |
| 主要障碍 | ① 52 题是 special judge（ROJ 本地评测目前只支持 `diff -b`）② 题面英/日双语需中译 ③ 全量数据体量约数 GB（不进 Git，走现有打包通道即可） |
| 建议 | 分批导入，首批选纯 diff 判题的"数据结构/树/字符串"模板题，配套建一份「Library Checker 模板题单」 |

## 一、项目是什么

Library Checker（全称 library-checker-problems）是 [judge.yosupo.jp](https://judge.yosupo.jp) 的题目源仓库，由 yosupo06 维护，被 ACPC、AtCoder 等社区广泛用作**库正确性/复杂度验证基准**。它的定位非常明确：

- 每题对应一个**经典数据结构或算法的标准接口**（如 unionfind、point_add_range_sum、suffixarray、matrix_det）；
- 题面只陈述接口与约束，**不讲故事、不设思维陷阱**，考的是"把这个模板写对、写快"；
- 测试数据以"能卡掉错误/低效实现"为第一目标，配套 naive 解、故意写错的解（wa.cpp）和卡常解（tle.cpp）做交叉验证。

一句话：**它是算法库的单元测试集，不是竞赛题库**。

## 二、规模与分布（实测统计）

253 道题（不含 `test/` 自测目录），按类目：

| 类目 | 题数 | 代表题目 |
| --- | ---: | --- |
| Data Structure | 43 | unionfind、range_affine_range_sum、range_kth_smallest、持久化/可并堆/李超线段树类 |
| Graph | 36 | scc、shortest_path、assignment、min_cost_b_flow、general_matching、支配树、色数 |
| Polynomial | 26 | 多项式 exp/log/composition、多点求值、插值、因式分解 |
| Number Theory | 22 | factorize、counting_primes、kth_root_mod、离散对数、Bernoulli 数 |
| Tree | 20 | lca、vertex_add_path_sum、动态树（Link-Cut）、树同构 |
| Enumerative Combinatorics | 17 | 第二类斯特林数、Bell 数、分拆数 |
| Linear Algebra | 17 | matrix_det、特征多项式、F2 线性方程组 |
| Convolution | 15 | 卷积（含 mod 1e9+7 / 2^64 / gcd-lcm / min-plus 凸） |
| String | 11 | zalgorithm、suffixarray、回文树、Lyndon 分解 |
| Geometry | 8 | 凸包、最近点对、曼哈顿 MST |
| Big Integer | 6 | 高精度加/乘/除（含十六进制版） |
| Other / Set Power Series / Sample | 17 | two_sat、LIS、集合幂级数等 |

## 三、题目工程特点（这是它最值钱的部分）

### 3.1 每题是一套完整的"可复现评测资产"

```text
<problem>/
├── info.toml        # 时限、测试点构成、约束参数 [params]
├── task.md          # 题面（英/日双语，@{param.X} 参数化模板）
├── gen/             # 测试数据生成器（C++，共 1482 个 .cpp）
│   ├── example_00.in
│   ├── random.cpp / max_random.cpp / 卡 FFT 的 fft_killer.cpp ...
├── sol/
│   ├── correct.cpp  # 标程
│   └── naive.cpp / wa.cpp / tle.cpp   # 对拍与交叉验证用
├── verifier.cpp     # testlib 输入校验器（约束强制）
├── checker.cpp      # testlib 输出校验器
└── hash.json        # 全部 in/out 的 SHA256，保证数据可复现一致
```

### 3.2 关键统计（实测）

| 指标 | 数值 | 含义 |
| --- | ---: | --- |
| diff 判题（wcmp checker） | 201 题 | 输出唯一确定，可直接对接 ROJ 的 `diff -b` |
| **special judge** | **52 题** | 输出任意合法解（最短路方案、匹配、拓扑序等），需要 checker 支持 |
| 多解答（对拍素材） | 149 题 | 其中 95 题带 naive 暴力——现成的对拍器和数据强度证明 |
| 时限分布 | 5s × 143、10s × 103、其余少量 | 时限宽松（yosupo 评测机口径），数据规模大 |
| 生成器 | 1482 个 C++ + 638 个样例 .in | 生成器本身是题目资产，可反复重生成数据 |
| 数据体量（抽样） | unionfind 一题：in 34MB + out 1.9MB | 253 题全量估计 **数 GB 级**（in 大 out 小） |

### 3.3 质量保障机制

- **verifier 强制约束**：每题输入校验器卡死数据范围，杜绝越界数据；
- **多解交叉验证**：`[[solutions]]` 里声明 `wrong = true` / `allow_tle` / `expect = "RE"`，CI 会校验 wa 解真的 WA、tle 解真的慢，保证数据"卡得住"；
- **hash.json + CI 全量生成**：数据内容被哈希锁定，任何生成器改动都会被发现；
- **对抗性生成器**：如 `fft_killer.cpp` 专卡 FFT 精度、`carry_chain.cpp` 专卡进位链，是"防 AK 数据"级别的强度。

### 3.4 许可证

Apache 2.0。**允许再分发、修改、商用**，只需保留版权声明与 NOTICE。把题目、生成器、数据打包进 ROJ（含 BT/HTTP 分发）没有法律障碍；建议在导入题目的 `content.md` 来源栏注明 `Library Checker (yosupo06) - <problem_id>`（1415 已是此格式）。

## 四、与 ROJ 的对比

| 维度 | ROJ（现状 1894 题） | Library Checker（253 题） |
| --- | --- | --- |
| 定位 | OI/NOIP/省选训练（一本通 227 题、牛客、CSP-S、省选模拟等） | 算法库验证 · 模板题 |
| 题面 | 中文 `content.md`，有情境/背景 | 英/日双语 `task.md`，纯接口描述 |
| 痛点分布 | 动态规划 285、模拟 284、数学 272、图论 209…… | 集中在数据结构/多项式/数论等"实现了才得分"的领域 |
| 数据结构类 | 仅 101 题标签为数据结构（线段树 24、树状数组 23、并查集 25） | 43 题全是数据结构标准接口，且含持久化、李超、李超、动态树等 ROJ 缺的进阶货 |
| 测试数据 | cyaron `data.py` 自动生成 + 自产/搜刮 | C++ 对抗性生成器 + verifier + 多解交叉验证，强度业界标杆 |
| 评测方式 | 本地 `roj.py test`（`diff -b`） | 201 题 diff、52 题 special judge |
| 标程 | 774 题缺 `std.cpp` | 100% 带 correct.cpp（还常带 naive/wa/tle） |

**互补性结论**：ROJ 的题偏"想得到"，LC 的题偏"写得对写得快"。ROJ 的数据结构标签只占 5%，恰好是 LC 的全部家底；而 LC 没有中文、没有 OI 情境、没有思维训练价值，正好由 ROJ 现有体系补足。

## 五、价值评估

### 值得合并的理由

1. **填模板题真空**：学完线段树想练手"裸题"，ROJ 现有题多是带情境的综合题；LC 提供 253 道"纯接口"标准题，是教材章节的天然配套练习；
2. **数据强度一骑绝尘**：自带对抗性生成器 + wa/tle 交叉验证，比 cyaron 随机数据强一个档次，本地评测/对拍教学价值极高（95 题现成 naive 可当对拍器）；
3. **覆盖面补强**：多项式全家桶、集合幂级数、min-cost flow、一般匹配、支配树、动态树、特征多项式……这批高级货 ROJ 基本没有，且都是省选+/集训队常见工具；
4. **可复现、可维护**：Apache 2.0 + 全量生成器 + hash 锁定，出问题能重新生成数据，不依赖任何网盘；
5. **有成功先例**：`problems/1415`（矩形加点求和 = rectangle_add_point_get）已完整走通"翻译 + 导入 + 打包"流程。

### 局限（要清醒的部分）

1. **思维训练价值低**：题面直接给接口，没有"怎么想到"的过程，对 NOIP 选手的建模能力帮助有限——它是课后习题册，不是例题课；
2. **题面需中译**：英/日双语没有中文，253 题翻译 + 人工校对是主要人力成本（机器翻译初稿 + 人工校对可行）；
3. **与现有题有重叠**：并查集、线段树、最短路等基础货 ROJ 已有 OI 情境版；重复导入意义不大，应选 LC 版数据更强或接口更标准的题；
4. **52 题 special judge 是硬骨头**：`roj.py test` 目前只支持 `diff -b`，输出方案类题目（shortest_path、assignment、general_matching 等）本地评测会误判，需先扩展 checker 支持或暂缓这批；
5. **时限口径不同**：LC 时限 5s/10s 是 yosupo 评测机口径，直接搬会过松，需按数据规模换算成 ROJ 的毫秒值（如 unionfind 数据 34MB 可给 2000ms）。

## 六、合并可行性（已实测验证）

### 6.1 格式映射

| Library Checker | ROJ | 转换方式 |
| --- | --- | --- |
| `info.toml`（title/timelimit/params） | `config.json` | 直译；时限换算成 ms；tags 按类目映射（数据结构/图论/数学/字符串/计算几何…） |
| `task.md`（@{param.X} 模板） | `content.md` | 先用 `[params]` 展开模板变量，再按 ROJ 四段式（题目描述/输入/输出/样例）中译重排 |
| `gen/`（C++ 生成器） | `data.py`（生成器，可选） | 可保留 C++ 生成器作为题目代码资产（不进公开下载），或封装成脚本驱动 |
| `sol/correct.cpp` | `std.cpp` | 直接采用 |
| `gen/example_00.in` + 输出 | 题面里的输入/输出样例 | 自动抽取 |
| 生成的 `in/` `out/` | `problems/<id>/data/`（gitignored）+ `data.json` | 生成后按现有 manifest 流程打包 `<id>.tar.zst` 上通道 |
| `checker.cpp` | — | **暂无对应**，52 题 special judge 需扩展 `roj.py test` 或暂缓 |
| `verifier.cpp` / `hash.json` | — | 作为质量保障资产留档（可放题目代码区），ROJ 不消费 |

### 6.2 工具链实测（本机通过）

```text
./generate.py -p aplusb      → 12 组数据生成 ✓（gen → in，correct.cpp → out）
./generate.py -p unionfind   → 18 组数据生成 ✓，in 34MB / out 1.9MB
```

即"LC 生成器 → ROJ `data/` + `data.json`"这条路完全走得通，剩下的是写一个批处理转换脚本。

### 6.3 导入规范对齐

按 `.agents/skills/add-roj-problem/SKILL.md` 的既有约定：

- **ID 段位**：LC 题是"其他题目"性质但批量大，建议单独开段（如 `30000+`，用 `find-empty-roj-id.py --start 30000`），与一本通（1000+）和比赛题（20000+）都隔开，方便整体管理；
- **来源标注**：`"source": "Library Checker (yosupo06) - <problem_id>"`（沿用 1415 格式）；
- **走先预览后确认**的批量导入流程，不自动 commit；
- `std.cpp`/生成器/checker 属于"题目代码"，不进公开下载清单。

## 七、建议方案

1. **先试点 3～5 题**（建议 unionfind、point_add_range_sum、staticrmq、zalgorithm、lca——全是 diff 判题、覆盖数据结构/字符串/树），走通"翻译 + 生成 + 打包 + 站点展示"全流程后再批量；
2. **首批排除 special judge 题**，或同期给 `roj.py test` 增加 checker 支持（二选一，前者快）；
3. **建立「Library Checker 模板题单」**（`problem-sets/library-checker.md`）：这批题单独成单比散落在题库里更有导航价值，也方便按教材章节勾选进度；
4. **翻译策略**：AI 初译 + 术语表统一（query→查询、persistent→可持久化等）+ 抽样人工校对；`@{param.X}` 展开与样例抽取写进转换脚本，不手工做；
5. **优先级**（按与 ROJ 互补度排序）：数据结构（43）→ 树（20）→ 图（36，先 diff 题）→ 字符串（11）→ 多项式/数论（48）→ 其余；
6. **重叠题不重复导入**：并查集等 ROJ 已有情境题的，只取 LC 中"更强接口"版本（如 unionfind_with_potential、range_parallel_unionfind）。

## 附录：本次调研的原始数据

- 仓库克隆分析：253 个 `info.toml`（排除 `test/`）；
- 类目统计来自 `categories.toml`；
- checker/solution/generator 统计来自对每题 `checker.cpp`、`sol/`、`gen/` 目录的逐题扫描；
- 数据体量来自本机 `generate.py` 实跑 aplusb 与 unionfind 的 `du` 结果；
- ROJ 侧标签/来源统计来自对 `problems/*/config.json` 的全量扫描（1894 份）。
