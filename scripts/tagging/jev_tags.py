#!/usr/bin/env python3
"""jev 直连打分器：给 new_ROJ 题目产出 tag 草案（.tmp/tag_drafts.json）。

直连 https://api.typesafe.ai/v1/systemone，不走任何 proxy（显式清空代理 handler）。
密钥取自 ~/.typesafe/jev-lgp888.keys（每行一个，10 个），轮换/并发使用，绝不打印。

用法：
    jev_tags.py dryrun --pids 1069 1678 2000 3000 4000   # 5 题干跑（含 LIS 题验证）
    jev_tags.py run [--limit N] [--cohort missing|existing] [--workers 5] [--resume]

请求体（每题一次调用）：
    {"state": "<题面文本>", "model": "jev-latest",
     "questions": {"category": {"type": "choice", ...}, "tag_<规范词>": {"type": "noul", ...}}}
响应解析：answers.<key>.noul / answers.<key>.choice + probabilities + confidence。

输出 .tmp/tag_drafts.json：
    {"updated": ..., "drafts": [{"pid", "title", "category", "candidates": [{"tag","p"}], "confidence"}]}

韧性：422/429/529 指数退避重试（≤5 次）；单 key 连续失败 3 次换下一个；
全部 key 不可用时报告暂停并以退出码 3 结束。
"""

from __future__ import annotations

# scripts/tagging/queue.py 与标准库 queue 同名：先移除脚本目录的 import 遮蔽
import pathlib as _pathlib
import sys as _sys
_script_dir = str(_pathlib.Path(__file__).resolve().parent)
if _script_dir in _sys.path:
    _sys.path.remove(_script_dir)

import argparse
import concurrent.futures
import json
import pathlib
import re
import sys
import threading
import time
import urllib.error
import urllib.request

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
KEYS_PATH = pathlib.Path("~/.typesafe/jev-lgp888.keys").expanduser()
VOCAB_PATH = REPO_ROOT / "scripts" / "tagging" / "vocabulary.json"
QUEUE_PATH = REPO_ROOT / "scripts" / "tagging" / "queue.jsonl"
DRAFT_PATH = REPO_ROOT / ".tmp" / "tag_drafts.json"
ENDPOINT = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"
RETRY_STATUS = {422, 429, 529}
MAX_ATTEMPTS = 5
KEY_FAIL_LIMIT = 3
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))  # 直连，忽略代理环境变量


class Pause(Exception):
    """所有 key 都不可用：报告暂停。"""


class KeyPool:
    """10 个 key 轮换；单 key 连续失败 3 次即摘除。线程安全。"""

    def __init__(self, keys: list[str]):
        if not keys:
            raise Pause(f"{KEYS_PATH} 里没有可用 key")
        self._keys = keys
        self._bad = {k: 0 for k in keys}
        self._idx = 0
        self._lock = threading.Lock()

    def take(self) -> str:
        with self._lock:
            live = [k for k in self._keys if self._bad[k] < KEY_FAIL_LIMIT]
            if not live:
                raise Pause("全部 key 连续失败达到上限，需要人工检查认证后继续")
            key = live[self._idx % len(live)]
            self._idx += 1
            return key

    def report(self, key: str, ok: bool) -> None:
        with self._lock:
            self._bad[key] = 0 if ok else self._bad[key] + 1

    def live_count(self) -> int:
        with self._lock:
            return sum(1 for k in self._keys if self._bad[k] < KEY_FAIL_LIMIT)


def load_keys() -> list[str]:
    if not KEYS_PATH.exists():
        raise Pause(f"缺少密钥文件 {KEYS_PATH}")
    keys = [line.strip() for line in KEYS_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    return keys


def load_vocab() -> tuple[list[dict], dict[str, str]]:
    data = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))
    tags = data["tags"]
    alias2canon = {}
    for entry in tags:
        for a in entry["aliases"]:
            alias2canon[a] = entry["tag"]
    return tags, alias2canon


def extract_state(config: dict, content: str) -> str:
    """title + 【题目描述】+【输入】+【输出】（去掉样例）。"""
    title = str(config.get("title") or "")
    lines = content.splitlines()
    wanted, current = [], None
    head_re = re.compile(r"^#{1,6}\s*(?:【)?\s*([^【】#]{0,20}?)\s*(?:】)?\s*$")
    for line in lines:
        m = head_re.match(line.strip())
        if m:
            name = m.group(1)
            if re.search(r"题目描述|题面|^描述", name):
                current = "desc"
            elif re.search(r"输入(?!样例)", name):
                current = "in"
            elif re.search(r"输出(?!样例)", name):
                current = "out"
            else:
                current = None
            if current:
                wanted.append(f"\n【{name}】")
            continue
        if current:
            wanted.append(line)
    body = "\n".join(wanted).strip()
    if not body:
        body = content[:4000]
    return f"标题：{title}\n{body}"[:6000]


def pick_candidates(text: str, tags: list[dict], alias2canon: dict[str, str], k: int = 12) -> list[str]:
    """粗分类：别名命中打分 -> 命中词 + 高分粗分类的代表词，补足 8~12 个候选。"""
    scores: dict[str, float] = {}
    for entry in tags:
        canon = entry["tag"]
        for alias in entry["aliases"]:
            if len(alias) < 2:  # 单字别名（如“串”“搜”）只用于归并，不参与命中
                continue
            hits = text.count(alias)
            if hits:
                scores[canon] = scores.get(canon, 0.0) + hits * (1.0 + 0.15 * len(alias))
    parent_score: dict[str, float] = {}
    for entry in tags:
        parent_score[entry["parent"]] = parent_score.get(entry["parent"], 0.0) + scores.get(entry["tag"], 0.0)
    picked: list[str] = []

    def add(tag: str) -> None:
        if tag not in picked:
            picked.append(tag)

    for tag in sorted(scores, key=lambda t: (-scores[t], t)):
        add(tag)
    for parent in sorted(parent_score, key=lambda p: (-parent_score[p], p)):
        if parent_score[parent] <= 0:
            continue
        members = [t["tag"] for t in tags if t["parent"] == parent]
        members.sort(key=lambda t: (-scores.get(t, 0.0), t))
        for tag in members:
            if len(picked) >= k:
                break
            add(tag)
        if len(picked) >= k:
            break
    generic = ["动态规划", "贪心", "模拟", "数学", "搜索", "字符串", "图论", "数据结构",
               "二分", "排序", "构造", "递推"]
    for tag in generic:
        if len(picked) >= k:
            break
        add(tag)
    return picked[:k]


def build_questions(tags: list[dict], candidates: list[str]) -> dict:
    by_tag = {t["tag"]: t for t in tags}
    parents = sorted({t["parent"] for t in tags})
    questions: dict[str, dict] = {
        "category": {
            "type": "choice",
            "instructions": "这道编程题的主算法类别最接近下列哪一项？",
            "criteria": {p: f"{p} 类算法问题" for p in parents},
        }
    }
    for canon in candidates:
        entry = by_tag[canon]
        questions[f"tag_{canon}"] = {
            "type": "noul",
            "instructions": f"解决这道题是否主要需要「{canon}」？",
            "criteria": {
                "true": f"解法核心涉及{canon}（{entry['definition']}）",
                "false": f"解法核心不需要{canon}，或只是次要工具",
            },
        }
    return questions


def call_jev(pool: KeyPool, state: str, questions: dict) -> dict:
    body = json.dumps({"state": state, "model": MODEL, "questions": questions}, ensure_ascii=False).encode("utf-8")
    last_error = None
    for attempt in range(MAX_ATTEMPTS):
        key = pool.take()
        req = urllib.request.Request(
            ENDPOINT, data=body, method="POST",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )
        try:
            with OPENER.open(req, timeout=90) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            pool.report(key, True)
            return payload
        except urllib.error.HTTPError as error:
            last_error = f"HTTP {error.code}"
            retryable = error.code in RETRY_STATUS or error.code >= 500
            pool.report(key, error.code != 401)
            if not retryable and error.code not in RETRY_STATUS:
                try:
                    detail = error.read().decode("utf-8", "replace")[:300]
                except Exception:
                    detail = ""
                raise RuntimeError(f"jev 不可重试错误 {error.code}: {detail}")
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            last_error = f"网络错误: {error}"
            pool.report(key, False)
        if attempt < MAX_ATTEMPTS - 1:
            time.sleep(min(2 ** attempt, 16))
    raise RuntimeError(f"重试 {MAX_ATTEMPTS} 次仍失败：{last_error}")


def normalize(pid: str, title: str, candidates: list[str], payload: dict) -> dict:
    answers = payload.get("answers") or payload.get("result", {}).get("answers") or {}
    cat = answers.get("category") or {}
    category = cat.get("choice") or cat.get("answer") or ""
    confidence = cat.get("confidence")
    if confidence is None:
        probs = cat.get("probabilities") or {}
        confidence = max(probs.values()) if probs else 0.0
    out = []
    for canon in candidates:
        ans = answers.get(f"tag_{canon}") or {}
        p = ans.get("noul")
        if p is None:
            p = ans.get("probability", ans.get("answer"))
        try:
            p = float(p)
        except (TypeError, ValueError):
            p = 0.5
        out.append({"tag": canon, "p": round(p, 4)})
    out.sort(key=lambda c: -c["p"])
    try:
        confidence = round(float(confidence), 4)
    except (TypeError, ValueError):
        confidence = 0.0
    return {"pid": pid, "title": title, "category": category,
            "candidates": out, "confidence": confidence}


def load_drafts() -> dict[str, dict]:
    if DRAFT_PATH.exists():
        data = json.loads(DRAFT_PATH.read_text(encoding="utf-8"))
        return {d["pid"]: d for d in data.get("drafts", [])}
    return {}


def save_drafts(drafts: dict[str, dict]) -> None:
    DRAFT_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = DRAFT_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(
        {"updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
         "drafts": [drafts[p] for p in sorted(drafts)]},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(DRAFT_PATH)


def iter_targets(cohort: str | None, limit: int | None) -> list[dict]:
    rows = []
    for line in QUEUE_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if cohort and row["cohort"] != cohort:
            continue
        rows.append(row)
    rows.sort(key=lambda r: r["pid"])
    return rows[:limit] if limit else rows


def process_one(pool: KeyPool, tags: list[dict], alias2canon: dict[str, str], row: dict) -> dict:
    pdir = REPO_ROOT / row["path"]
    config = json.loads((pdir / "config.json").read_text(encoding="utf-8"))
    content_path = pdir / "content.md"
    content = content_path.read_text(encoding="utf-8") if content_path.exists() else ""
    state = extract_state(config, content)
    candidates = pick_candidates(state, tags, alias2canon)
    questions = build_questions(tags, candidates)
    payload = call_jev(pool, state, questions)
    return normalize(row["pid"], str(config.get("title") or row.get("title") or ""), candidates, payload)


def run(args: argparse.Namespace) -> int:
    tags, alias2canon = load_vocab()
    pool = KeyPool(load_keys())
    drafts = load_drafts() if args.resume else {}
    if args.pids:
        rows = [{"pid": p, "path": f"problems/{p}"} for p in args.pids]
    else:
        rows = [r for r in iter_targets(args.cohort, args.limit) if r["pid"] not in drafts]
    print(f"待打分 {len(rows)} 题，已有草案 {len(drafts)}，并发 {args.workers}", flush=True)
    done = fail = 0
    lock = threading.Lock()
    results: list[dict] = []

    def work(row: dict) -> dict:
        return process_one(pool, tags, alias2canon, row)

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(work, row): row for row in rows}
        for future in concurrent.futures.as_completed(futures):
            row = futures[future]
            try:
                draft = future.result()
            except Pause as error:
                print(f"\n[暂停] {error}", flush=True)
                return 3
            except Exception as error:  # noqa: BLE001
                fail += 1
                print(f"[fail] {row['pid']}: {error}", flush=True)
                continue
            with lock:
                drafts[draft["pid"]] = draft
                results.append(draft)
                done += 1
                if done % 25 == 0 or done == len(rows):
                    save_drafts(drafts)
                    print(f"[{done}/{len(rows)}] 最近: {draft['pid']} {draft['category']} "
                          f"{[c['tag'] for c in draft['candidates'][:3]]} conf={draft['confidence']}", flush=True)
    save_drafts(drafts)
    print(f"完成 {done}，失败 {fail}，草案总数 {len(drafts)} -> {DRAFT_PATH}", flush=True)
    return 0 if fail == 0 else 1


def dryrun(args: argparse.Namespace) -> int:
    tags, alias2canon = load_vocab()
    pool = KeyPool(load_keys())
    rows = [{"pid": p, "path": f"problems/{p}"} for p in args.pids]
    ok, drafts = True, {}
    for row in rows:
        try:
            draft = process_one(pool, tags, alias2canon, row)
        except Exception as error:  # noqa: BLE001
            print(f"[fail] {row['pid']}: {error}")
            ok = False
            continue
        drafts[draft["pid"]] = draft
        print(json.dumps(draft, ensure_ascii=False))
    # 干跑判据：LIS 类题（--dp-pid）「动态规划」概率应 ≥ 0.8
    if args.dp_pid:
        draft = drafts.get(args.dp_pid)
        p = next((c["p"] for c in (draft or {}).get("candidates", []) if c["tag"] == "动态规划"), None)
        if p is None or p < 0.8:
            print(f"[判据失败] LIS 题 {args.dp_pid} 动态规划 p={p}，要求 ≥0.8")
            ok = False
        else:
            print(f"[判据通过] LIS 题 {args.dp_pid} 动态规划 p={p}")
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="jev 直连打分器（new_ROJ tag 批次）")
    parser.add_argument("command", choices=["dryrun", "run"])
    parser.add_argument("--pids", nargs="*")
    parser.add_argument("--cohort", choices=["missing", "existing"])
    parser.add_argument("--limit", type=int)
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--resume", action="store_true", help="跳过 .tmp/tag_drafts.json 已有草案")
    parser.add_argument("--dp-pid", help="dryrun 判据：该 LIS 题的「动态规划」概率须 ≥ 0.8")
    args = parser.parse_args()
    if args.command == "dryrun":
        if not args.pids:
            parser.error("dryrun 需要 --pids")
        return dryrun(args)
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
