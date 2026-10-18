# Library Checker 第二轮实施计划：测试数据生成

> 目标：为 30000–30251 共 252 题生成测试数据 `problems/<id>/data/{1..N}.in/.out` 并更新 `data.json`。
> 本轮**不打包上传**（`<id>.tar.zst` 与上传单独一轮）。
> 依据：四路侦察报告（LC 生成机制 / ROJ 清单规范 / 依赖与 SPJ 表 / judge 流程），2026 年。

## 0. 事实基础（侦察结论摘要）

- LC 官方流水线 `./generate.py -p <lc_id>`：`gen/X <seed>` 生成 `in/X_XX.in`（seed 0..number-1）→ `sol/correct` 产出 `out/*.out` → 默认模式 `assert_hashes()` 与上游 `hash.json` 逐字节校验（macOS arm64 实测 4 题 100% 一致，可复现）。
- 全库 253 题约 6039 case（均值 24/题）；产物命名 `<gen名>_XX.in`，需重映射为 ROJ `1..N`。
- ROJ：`data.json` schema `{"files":[{"path","size"}]}`（无 hash），扫描 `problems/<id>/data/`，单文件硬上限 100 MiB；`data/` 被 gitignore（数据本体走 tar.zst 分发）。
- judge：`judge <src> --data-dir problems/<id>/data`；config.json `time/memory` 生效；编译 `g++ -std=c++17 -O2` 无 -I 透传，引号 include 相对源文件解析 → 验证直接提交 LC 原路径 `sol/correct.cpp` 零补齐；外部 checker 签名 `<in> <participant> <expected>`，LC testlib checker 编译后（`-I common`）可直接用。
- SPJ 现状：52 题标注 + **新发现 diff 组内 29 题自定义 checker**（30225 已证实误分类），需三档审计（A 唯一可 diff / B 任选解需 checker / C 表示自由度）。
- 体量预估：全批 in+out 约 3–20GB（中位 ~5GB）；~12 题有单文件 >100 MiB 风险，须生成时实测（params 模板注入，纸面判断有盲区）。

## 1. 流水线（每题）

```
① cd LC仓库 && ./generate.py -p <lc_id>        # 生成 + hash 逐字节校验（失败降级 --dev 并记录）
② case 映射：example_* 排最前，其余按 casename 字典序 → 编号 1..N
   拷贝 in/X_XX.in → new_ROJ/problems/<id>/data/<k>.in，out 同理
③ 单文件 >100MiB → 立即暂停该题，登记超限清单（SKILL 硬规定）
④ generate-data-manifest.py --root problems --problem <id>   # 更新 data.json
⑤ 验证：
   - diff 组：judge <LC sol/correct.cpp 路径> --data-dir problems/<id>/data → 必须全 AC
   - SPJ 组：编译 LC checker（-I common）→ judge --checker <checker> → participant=correct 输出必须 AC
   - 附加自检：checker(in, out, out) 双通过（对齐 generate.py 内建行为）
⑥ LC 侧产物 --clean（控磁盘）；映射表存 /tmp/lc-import/round2/<roj_id>.map
```

## 2. 测试点策略（用户已拍板 2026）

- **全量保留 LC 非 example case**：生成器按 small/random/max/hack 分布精心构造，不裁剪；**题面样例不进 data/**（example* 剔除）。
- 映射：剔除 example* 后按文件名字典序 → `1..N`，`.in/.out` 同编号；映射表存 `/tmp/lc-import/round2/<roj_id>.map`。
- 单文件 >100MiB 护栏：停下登记，不自行裁剪。
- 验证强度（已拍板）：**judge 全量 AC 验证**（diff 组 diff / SPJ 组 --checker），另加 hash 一致性。
- SPJ 标注修正（已拍板）：审计后直接改 content.md，随本轮交付。

## 3. 第 0 步：SPJ 分类审计（先行，半天）

- 对 diff 组 29 题逐一读 checker，三档定性（A/B/C）；同步核查 SPJ 52 题是否有误标注反例。
- 产出：修正 content.md SPJ 标注（B/C 题补「special judge」注记）+ 最终 diff/SPJ 清单 + 30225 等转组。
- 该步决定 ⑤ 验证走 diff 还是 checker。

## 4. 派发矩阵

- 角色：新建 `lc-data-worker`（只读任务卡，只写 `problems/<id>/data/` 与 `data.json`，不 git、不打包、单题粒度、严格自检）。
- 池：**2× heibai + 2× small-sheep**（总并发 4，独占 tab；heibai 额度耗尽 → 全转 small-sheep）。
- 任务卡由主线程预处理生成（lc_id、lc_path、case 数、SPJ 档、checker 路径、映射规则），worker 零探索。
- 批次：按体量分档排程（小题 2–3 题/卡，重题 1 题/卡）；完成即补位。
- 预计总时长：生成侧 ~4–8 小时（卷积/数论重题 10–20 分钟/题）。

## 5. 验收标准

- 252 题 `data/` 齐备、`.in/.out` 成对、命名 `1..N` 连续；
- `data.json` 全量 `--check` 通过（含 20439–20442 旧问题隔离）；
- hash 与上游一致（或 --dev 降级有登记）；
- diff 组 judge 全 AC（提交 = LC correct.cpp）；SPJ 组 checker 全通过；
- 超限/异常/降级清单齐全；不 commit，出总结报告待审。

## 6. 风险与对策

| 风险 | 对策 |
|---|---|
| 单文件 >100MiB | 停下登记，裁剪 or 等 LFS 决策（默认裁剪 random 之外的巨型 case） |
| hash 不一致（平台漂移） | --dev 降级 + 登记；产物仍以 LC 生成器为准 |
| mtime 缓存误判已生成 | 一律 --dev 或先 --clean 再生成 |
| 磁盘 20GB+ | 分批生成、每批完结即 LC --clean；磁盘水位监控 |
| judge 验证环境 | 全局 judge（Docker/executor）；本地 judge.py 直跑在 macOS 会 SE |
| checker 依赖 testlib.h | 编译 checker 时 -I LC/common，产出二进制放 /tmp/lc-import/round2/checker-bin/ |
