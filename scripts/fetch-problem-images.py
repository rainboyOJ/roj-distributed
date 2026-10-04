#!/usr/bin/env python3
"""把题面里的悬空图片引用从原站抓回本地。

`problems/<id>/content.md` 里的图片引用有两类来源，都可从原 OJ 直接取回：

* 一本通（ybt.ssoier.cn:8088）——引用形如 `pic/1167.gif`，原站同名路径直接可下。
  注意原站会跨 pid 引图（pid 1258 的题面用的是 `pic/1284.gif`），所以必须按引用名
  原样下载，不能按 id 猜。另有极少数引用误带了前导斜杠（`/pic/1424.gif`）。
* AcWing（cdn.acwing.com）——引用形如 `/media/article/image/2019/...jpg`，需要带
  `Referer: https://www.acwing.com/`，否则 403。这类引用以 `/` 开头，渲染器
  （web/server/markdown-renderer.mjs 的 localImageUrl）会拒绝，所以必须改写成相对路径。

本地落盘规则：`problems/<id>/pic/<stem>.<真实扩展名>`

* stem 沿用原引用（一本通用 `1167`、`1662a`，AcWing 用 `<id>-<序号>`）。
* 扩展名以图片魔数为准，不信任 URL 后缀——原站确实存在 `pic/1437.png` 实为 JPEG、
  `pic/1448.jpg` 实为 GIF 的情况，而 web 服务端是按扩展名发 Content-Type 的
  （web/server/index.mjs 的 asset 路由），不一致会导致浏览器拿到错误的 MIME。

题面引用只在必要时改写（去前导斜杠、换扩展名、AcWing 绝对路径转相对路径）。
远端 URL 引用（http/https 开头）不动。脚本幂等：本地已有且魔数与后缀一致的文件会跳过，
跳过时不需要联网。

用法：
    python3 scripts/fetch-problem-images.py --check    # 只报告，不写盘、不联网
    python3 scripts/fetch-problem-images.py            # 抓缺失的图并改写题面
    python3 scripts/fetch-problem-images.py --force     # 重新下载已有图片
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_DIR = REPO_ROOT / "problems"
IMAGE_REF_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 Chrome/120 Safari/537.36"
)

# 魔数 → 规范扩展名。既用来确认下回来的确实是图片（而不是错误页），也用来定后缀。
MAGIC = {
    b"\xff\xd8\xff": ".jpg",
    b"\x89PNG\r\n\x1a\n": ".png",
    b"GIF87a": ".gif",
    b"GIF89a": ".gif",
}

REMOTE_RE = re.compile(r"^(?:https?:)?//", re.I)


def sniff_extension(data: bytes) -> str | None:
    for magic, extension in MAGIC.items():
        if data.startswith(magic):
            return extension
    return None


class Source:
    """一个原站图床的规则。"""

    name = ""
    base = ""
    headers: dict[str, str] = {}

    def matches(self, ref: str) -> bool:
        raise NotImplementedError

    def url(self, ref: str) -> str:
        raise NotImplementedError

    def stem(self, problem_id: str, ref: str, index: int) -> str:
        raise NotImplementedError


class YbtSource(Source):
    name = "一本通"
    base = "http://ybt.ssoier.cn:8088/"

    def matches(self, ref: str) -> bool:
        return ref.lstrip("/").startswith("pic/")

    def url(self, ref: str) -> str:
        return self.base + urllib.parse.quote(ref.lstrip("/"))

    def stem(self, problem_id: str, ref: str, index: int) -> str:
        return Path(ref.lstrip("/")).stem


class AcwingSource(Source):
    name = "AcWing"
    base = "https://cdn.acwing.com"
    headers = {"Referer": "https://www.acwing.com/"}

    def matches(self, ref: str) -> bool:
        return ref.startswith("/media/")

    def url(self, ref: str) -> str:
        return self.base + urllib.parse.quote(ref)

    def stem(self, problem_id: str, ref: str, index: int) -> str:
        # 原文件名带中文和 `.jpe.jpg` / `.jpg.gif` 这类畸形后缀，一律换成
        # `<id>-<该题内序号>`，顺序与题面中的出现顺序一致。
        return f"{problem_id}-{index}"


SOURCES = [AcwingSource(), YbtSource()]


class Task:
    def __init__(self, problem_id: str, content_path: Path, ref: str, source: Source, index: int):
        self.problem_id = problem_id
        self.content_path = content_path
        self.dir = content_path.parent
        self.ref = ref
        self.source = source
        self.stem = source.stem(problem_id, ref, index)

    @property
    def url(self) -> str:
        return self.source.url(self.ref)

    def rel_for(self, extension: str) -> str:
        return f"pic/{self.stem}{extension}"

    def resolve_existing(self) -> Path | None:
        """找出已落盘且后缀与真实编码一致的那份；纯本地判断，不联网。"""
        for candidate in sorted((self.dir / "pic").glob(f"{self.stem}.*")):
            if not candidate.is_file():
                continue
            with candidate.open("rb") as handle:
                magic = sniff_extension(handle.read(8))
            if magic is not None and magic == candidate.suffix.lower():
                return candidate
        return None



def collect() -> list[Task]:
    tasks: list[Task] = []
    for content_path in sorted(PROBLEMS_DIR.glob("*/content.md")):
        problem_id = content_path.parent.name
        if not problem_id.isdigit():
            continue
        text = content_path.read_text(encoding="utf-8")
        counters: dict[str, int] = {}
        for match in IMAGE_REF_RE.finditer(text):
            ref = match.group(1).strip()
            if REMOTE_RE.match(ref) or ref.startswith("data:"):
                continue
            source = next((item for item in SOURCES if item.matches(ref)), None)
            if source is None:
                print(f"  ! {problem_id}: 无法识别的引用 {ref}", file=sys.stderr)
                continue
            counters[source.name] = counters.get(source.name, 0) + 1
            tasks.append(Task(problem_id, content_path, ref, source, counters[source.name]))
    return tasks


def fetch(task: Task) -> bytes:
    request = urllib.request.Request(
        task.url, headers={"User-Agent": USER_AGENT, **task.source.headers}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status}")
        return response.read()


def write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".part")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def rewrite_ref(task: Task, rel: str) -> bool:
    """把题面里的引用改成 `rel`；返回是否真的改了。"""
    if rel == task.ref:
        return False
    text = task.content_path.read_text(encoding="utf-8")
    if f"]({task.ref})" not in text:
        raise RuntimeError(f"{task.content_path}: 找不到引用 {task.ref}")
    task.content_path.write_text(text.replace(f"]({task.ref})", f"]({rel})"), encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--check", action="store_true", help="只报告状态，不写盘、不联网")
    parser.add_argument("--force", action="store_true", help="已有图片也重新下载")
    args = parser.parse_args()

    tasks = collect()
    if not tasks:
        print("没有发现需要处理的本地图片引用。")
        return 0

    downloaded = skipped = rewritten = 0
    failures: list[tuple[Task, str]] = []

    for task in tasks:
        existing = None if args.force else task.resolve_existing()
        if existing is not None:
            rel = existing.relative_to(task.dir).as_posix()
            if rel != task.ref:
                if args.check:
                    print(f"待改写 {task.problem_id}: {task.ref} -> {rel}")
                else:
                    rewrite_ref(task, rel)
                    rewritten += 1
                    print(f"REF {task.problem_id}: {task.ref} -> {rel}")
            skipped += 1
            continue

        if args.check:
            print(f"缺失 {task.problem_id}: {task.ref} <- {task.source.name} {task.url}")
            downloaded += 1
            continue

        try:
            data = fetch(task)
        except (urllib.error.URLError, RuntimeError, OSError) as error:
            failures.append((task, str(error)))
            continue

        extension = sniff_extension(data[:8])
        if extension is None:
            failures.append((task, f"返回的不是图片（{len(data)} 字节）"))
            continue

        rel = task.rel_for(extension)
        write_atomic(task.dir / rel, data)
        if rewrite_ref(task, rel):
            rewritten += 1
        downloaded += 1
        note = f"，后缀按魔数修正为 {extension}" if Path(task.ref).suffix.lower() != extension else ""
        print(f"OK  {task.problem_id}: {rel}（{len(data)} 字节，{task.source.name}{note}）")

    if args.check:
        print(f"\n合计 {len(tasks)} 处引用：就绪 {skipped}，待下载 {downloaded}")
    else:
        print(f"\n合计 {len(tasks)} 处引用：跳过 {skipped}，下载 {downloaded}，改写题面 {rewritten}")
    for task, error in failures:
        print(f"失败 {task.problem_id}: {task.ref} <- {task.url}：{error}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
