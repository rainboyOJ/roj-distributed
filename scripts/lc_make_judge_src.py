#!/usr/bin/env python3
"""lc_make_judge_src.py — 为 judge 验证生成完全自包含源文件。

judge 在 Docker 内编译提交，任何外部路径 include（相对或绝对）都不可见。
本工具把源文件的 #include "..." 递归内联为文件内容（头文件自身的相对 include
同样内联），按绝对路径去重（近似 include guard），angle include 原样保留。

用法：python3 scripts/lc_make_judge_src.py <源文件> <输出名>
裸名（如 "random.h"）额外在 <LC仓库>/common/ 下查找。
"""
import re
import sys
from pathlib import Path

LC_ROOT = Path.home() / "mycode/RBOOK_series/library-checker-problems"
OUT_DIR = Path("/tmp/lc-import/round2/verify")

INC_RE = re.compile(r'#include\s+"([^"]+)"')


def resolve(inc: str, cur: Path) -> Path | None:
    cand = (cur.parent / inc).resolve()
    if cand.exists():
        return cand
    cand = (LC_ROOT / "common" / inc).resolve()
    return cand if cand.exists() else None


def inline(path: Path, seen: set[Path], depth: int = 0) -> str:
    if depth > 8:
        raise RuntimeError(f"include 过深: {path}")
    seen.add(path.resolve())
    out = []
    for line in path.read_text().splitlines(keepends=True):
        m = INC_RE.match(line.strip())
        if m:
            tgt = resolve(m.group(1), path)
            if tgt is None:
                print(f"WARN 无法解析 include: {m.group(1)} (in {path.name})", file=sys.stderr)
                out.append(line)
            elif tgt.resolve() in seen:
                out.append(f"/* skipped dup: {tgt.name} */\n")
            else:
                out.append(f"/* ==== begin {tgt.name} ==== */\n")
                out.append(inline(tgt, seen, depth + 1))
                out.append(f"/* ==== end {tgt.name} ==== */\n")
        else:
            out.append(line)
    return "".join(out)


def main() -> int:
    src = Path(sys.argv[1]).resolve()
    name = sys.argv[2]
    text = inline(src, set())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{name}.cpp"
    out.write_text(text)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
