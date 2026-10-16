# ROJ Skill 安装说明

这是一份给 OpenCode、Codex 或 Claude Code 使用的安装指令。用户要求安装
ROJ Skill 时，请按下面的流程执行。不要下载或克隆整个仓库。

**安装位置固定为 `~/.agents/skills/roj/`**（全局 Skill 目录），安装后在任意
目录都可以运行。不要装到项目级目录，也不要改用其他路径。

## 目标文件

只从 GitHub Raw 下载以下三个文件：

```text
https://raw.githubusercontent.com/rainboyOJ/roj-distributed/master/.agents/skills/roj/SKILL.md
https://raw.githubusercontent.com/rainboyOJ/roj-distributed/master/.agents/skills/roj/scripts/roj.py
https://raw.githubusercontent.com/rainboyOJ/roj-distributed/master/.agents/skills/roj/agents/openai.yaml
```

安装命令默认先访问 GitHub Raw；直连失败时，自动改用
`https://gh-proxy.com/https://raw.githubusercontent.com/...` 重试。可以通过
`RAW_BASE` 和 `RAW_MIRROR` 环境变量替换默认地址。

不要凭猜测覆盖一个已经存在的 `roj` Skill。`~/.agents/skills/roj/` 已存在且
内容不是本仓库版本时，先报告差异并请求用户确认；目录不存在时才创建。

## 安装步骤

```sh
set -eu

RAW_BASE="${RAW_BASE:-https://raw.githubusercontent.com/rainboyOJ/roj-distributed/master}"
RAW_MIRROR="${RAW_MIRROR:-https://gh-proxy.com}"
RAW_BASE="${RAW_BASE%/}"
RAW_MIRROR="${RAW_MIRROR%/}"
SKILL_DIR="$HOME/.agents/skills/roj"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

download_raw() {
  path="$1"
  output="$2"
  direct_url="${RAW_BASE}/${path}"
  mirror_url="${RAW_MIRROR}/${direct_url}"
  if curl -fL --retry 2 --connect-timeout 10 "$direct_url" -o "$output"; then
    return 0
  fi
  printf 'GitHub Raw 直连失败，改用加速源：%s\n' "$mirror_url" >&2
  curl -fL --retry 2 --connect-timeout 10 "$mirror_url" -o "$output"
}

download_raw ".agents/skills/roj/SKILL.md" "$TMP_DIR/SKILL.md"
download_raw ".agents/skills/roj/scripts/roj.py" "$TMP_DIR/roj.py"
download_raw ".agents/skills/roj/agents/openai.yaml" "$TMP_DIR/openai.yaml"

mkdir -p "$SKILL_DIR/scripts" "$SKILL_DIR/agents"
cp "$TMP_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"
cp "$TMP_DIR/roj.py" "$SKILL_DIR/scripts/roj.py"
cp "$TMP_DIR/openai.yaml" "$SKILL_DIR/agents/openai.yaml"
chmod +x "$SKILL_DIR/scripts/roj.py"
```

如果系统没有 `curl`，使用等价的 `wget`，但仍然只下载上面列出的文件。不要使用
`git clone`，也不要把 `roj/`、`data/` 或整个仓库复制到 Skill 目录。

## 依赖

- Python 3.10+（脚本只用标准库）；
- `download` 下载归档需要系统 `zstd` 与 GNU `tar`（macOS 用 `brew install zstd gnu-tar`）；
- `test` 本地评测需要 `g++` 与 `diff`。

## 验证

安装后检查文件存在，并运行：

```sh
python3 ~/.agents/skills/roj/scripts/roj.py --help
python3 ~/.agents/skills/roj/scripts/roj.py get 1000
python3 ~/.agents/skills/roj/scripts/roj.py download 1000
```

`download 1000` 成功的表现：`./roj-data/1000.tar.zst` 归档落盘，
`./roj-data/1000/data/` 下是测试数据（`problem1.in`、`problem1.out` …）。
数据归档从 ROJ 的两站双通道下载（csps 主站 / oidata 备用），不经过 GitHub。
