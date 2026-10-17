---
name: roj
description: Use the ROJ read-only problem website from an AI or terminal. Trigger whenever the user asks to search, fetch, read, download, inspect, or locally test a problem from roj.ac.cn, or asks how to use the ROJ problem data. This skill covers the bundled scripts/roj.py client; never treat ROJ as a submission or remote judging service.
compatibility: Requires Python 3.10+, network access for API and data commands, zstd plus GNU tar for archive extraction, and g++ plus the system diff command for local C++ testing.
---

# ROJ Client

Use `scripts/roj.py` to interact with the read-only ROJ site. The website serves
problem metadata, Markdown/PDF statements, and public test data. It does not accept
accounts, source-code submissions, or remote judging requests.

Run the globally installed script from any directory with Python 3:

```sh
python3 ~/.agents/skills/roj/scripts/roj.py --help
```

Set `ROJ_URL` or pass `--base-url` when using a local or staging server:

```sh
ROJ_URL=https://roj.ac.cn python3 ~/.agents/skills/roj/scripts/roj.py list
python3 ~/.agents/skills/roj/scripts/roj.py --base-url http://127.0.0.1:3033 list
```

## Commands

### Find problems

`list` searches by numeric ID or title. It automatically follows all result pages;
use `--page N` when only one page is needed.

```sh
python3 ~/.agents/skills/roj/scripts/roj.py list
python3 ~/.agents/skills/roj/scripts/roj.py list "最短路"
python3 ~/.agents/skills/roj/scripts/roj.py list --page 2
python3 ~/.agents/skills/roj/scripts/roj.py --json list "二分"
```

Use `--json` for tool or AI consumption. JSON output is also available after a
subcommand, for example `list --json`.

### Read a problem

`get` prints metadata followed by the raw Markdown statement. PDF-only problems
print the browser URL instead; the CLI does not attempt to convert PDFs to text.

```sh
python3 ~/.agents/skills/roj/scripts/roj.py get 1000
python3 ~/.agents/skills/roj/scripts/roj.py get 10000 --no-markdown
python3 ~/.agents/skills/roj/scripts/roj.py --json get 1000
```

### Download public data

Data ships as one immutable `tar.zst` archive per problem. The default collection
directory is `./roj-data/`: the archive lands at `./roj-data/<id>.tar.zst` and is
extracted so the data ends up in `./roj-data/<id>/data/`. The command reads the ROJ
manifest first, downloads `<id>.tar.zst` from the configured archive sources
(csps 主站 first, oidata 备用 as fallback), verifies it with `zstd -t`, extracts it,
and cross-checks every extracted file against the manifest (path + size). A cached
archive is reused without re-downloading; an existing `data/` directory is never
overwritten. `--force` re-downloads and re-extracts. `--output` names the
collection directory instead of `./roj-data`.

```sh
python3 ~/.agents/skills/roj/scripts/roj.py download 1000
python3 ~/.agents/skills/roj/scripts/roj.py download 1000 --output ./data --force
```

Extraction requires the system `zstd` and GNU `tar` commands. The archive contains
the whole `data/` tree; there is no per-file download.

Downloads resume: an interrupted transfer keeps its bytes in `<id>.tar.zst.part` and
the next run continues with an HTTP `Range` request from where it stopped (the two
archive channels support byte ranges). A server that ignores `Range` or reports a
size mismatch makes the client restart that source from scratch; `--force` discards
the partial file.

### Test C++ locally

`test` is local-only. It compiles with `g++ -std=c++17 -O2`, runs each matching
`.in`/`.out` or `.in`/`.ans` pair, applies the problem time limit when present, and
compares output with `diff -b`. A non-zero program exit is `RE`; timeout is `TLE`;
different output is `WA`; all matching cases are `AC`. Memory limits are reported
but are not forcibly imposed by this Python client.

Data lookup is offline by default: `--data-dir DIR` or any `data/` directory found
under the current working directory.

If no data exists, add `--download` to explicitly fetch the archive into
`./roj-data/` and extract it. This is the only `test` mode that uses the network.
When combined with `--download`, `--data-dir` is treated as the collection directory
(archive at `<dir>/<id>.tar.zst`, data at `<dir>/<id>/data/`).

```sh
python3 ~/.agents/skills/roj/scripts/roj.py test 1000 main.cpp
python3 ~/.agents/skills/roj/scripts/roj.py test 1000 main.cpp --data-dir ./tests/1000
python3 ~/.agents/skills/roj/scripts/roj.py test 1000 main.cpp --download
python3 ~/.agents/skills/roj/scripts/roj.py --json test 1000 main.cpp
```

The command returns exit status 0 only when compilation succeeds and every data
pair is `AC`. A missing pair, compiler error, network failure, or test failure is
non-zero. JSON test results include the problem metadata, selected data directory,
compiler details, per-case status, elapsed time, and any diagnostics.

## Safe operating rules

- Treat IDs and paths as untrusted input. Never construct a shell command from a
  problem title or a manifest filename.
- Download only the problem archive named by `/api/problem/<id>/data`; its bytes
  come from the configured archive sources. Do not expose or copy `std.cpp`, solution
  files, generators, checkers, or legacy `down/` files.
- Do not claim that a local `AC` is an official submission result. It only means the
  program matched the public data with this client's comparison rule.
- Keep downloaded data in a user-selected working directory and inspect it before
  running unfamiliar source code.

## API reference

The client uses these read-only endpoints:

```text
GET /api/problems?q=<query>&page=<number>
GET /api/problem/<id>
GET /api/problem/<id>/markdown
GET /api/problem/<id>/data
```

`/api/problem/<id>/data` returns `archive` (with `name` `<id>.tar.zst`), a `sources`
array, and a `files` array that is informational only. Each source contains an `id`,
a display `label`, and a `baseUrl` (an archive directory ending in `/`); append
`archive.name` to that base URL to download the whole problem archive. The normal
source order is csps 主站 followed by oidata 备用.

The problem metadata response contains `id`, `title`, `time`, `memory`, `tags`,
`source`, `statementKind`, `hasMarkdown`, `hasPdf`, and `hasPublicData`. A missing
Markdown statement on a PDF-only problem is expected, not an API failure.
