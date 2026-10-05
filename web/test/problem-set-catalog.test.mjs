import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { MarkdownRenderer } from '../server/markdown-renderer.mjs';
import { ProblemCatalog } from '../server/problem-catalog.mjs';
import { ProblemSetCatalog } from '../server/problem-set-catalog.mjs';

function temporaryDirectory(prefix) {
  return fs.mkdtempSync(path.join(os.tmpdir(), prefix));
}

function writeProblem(rootDir, id, title) {
  const dir = path.join(rootDir, id);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'config.json'), JSON.stringify({ title }));
  fs.writeFileSync(path.join(dir, 'content.md'), `### 题目描述\n\n${title}。\n`);
}

function fixture() {
  const problemsRoot = temporaryDirectory('roj-problems-test-');
  const setsRoot = temporaryDirectory('roj-problem-sets-test-');
  writeProblem(problemsRoot, '1001', '示例题甲');
  writeProblem(problemsRoot, '1002', '示例题乙');

  const renderer = new MarkdownRenderer();
  const problems = new ProblemCatalog(problemsRoot, renderer, { warn() {} });
  problems.load();
  const sets = new ProblemSetCatalog(setsRoot, renderer, problems, { warn() {} });
  return { problemsRoot, setsRoot, sets };
}

function writeSet(setsRoot, slug, markdown) {
  fs.writeFileSync(path.join(setsRoot, `${slug}.md`), markdown);
}

test('problem sets load with order sorting and draft filtering', () => {
  const { setsRoot, sets } = fixture();
  try {
    writeSet(setsRoot, 'zebra', '---\ntitle: 斑马\norder: 2\n---\n\n[甲](/problem/1001)\n');
    writeSet(setsRoot, 'alpha', '---\ntitle: 阿尔法\norder: 1\n---\n\n[乙](/problem/1002)\n');
    writeSet(setsRoot, 'plain', '---\ntitle: 无序号\n---\n\n[甲](/problem/1001)\n');
    writeSet(setsRoot, 'hidden', '---\ntitle: 草稿\ndraft: true\n---\n\n[甲](/problem/1001)\n');
    writeSet(setsRoot, 'Bad_Slug', '---\ntitle: 非法\n---\n\nx\n');

    const list = sets.list();
    assert.deepEqual(list.map((entry) => entry.slug), ['alpha', 'zebra', 'plain']);
    assert.equal(sets.get('hidden'), null);
    assert.equal(sets.get('missing'), null);
  } finally {
    fs.rmSync(setsRoot, { recursive: true, force: true });
  }
});

test('render marks missing problems and decorates progress checkboxes', () => {
  const { setsRoot, sets } = fixture();
  try {
    writeSet(setsRoot, 'sample', [
      '---',
      'title: 示例题目单',
      '---',
      '',
      '- [甲](/problem/1001)',
      '- [幽灵](/problem/9999)',
      '- [外链](https://example.com/problem/1001)'
    ].join('\n'));

    const rendered = sets.render(sets.get('sample'));
    assert.deepEqual(rendered.problemLinks.map((link) => link.id), ['1001']);
    assert.deepEqual(rendered.missingLinks.map((link) => link.id), ['9999']);
    assert.match(rendered.html, /data-progress-id="1001"/);
    assert.match(rendered.html, /class="problem-link is-missing"/);
    assert.equal((rendered.html.match(/data-progress-id=/g) || []).length, 1);
    // 外部链接不该被当成题目链接
    assert.ok(!rendered.html.includes('data-progress-id="1001"') || !/example\.com[^"]*"[^>]*>.*progress/.test(rendered.html));
  } finally {
    fs.rmSync(setsRoot, { recursive: true, force: true });
  }
});

test('stats prefer explicit frontmatter counts and fall back to links', () => {
  const { setsRoot, sets } = fixture();
  try {
    writeSet(setsRoot, 'explicit', '---\ntitle: 显式统计\nitems: 895\ncovered: 667\n---\n\n[甲](/problem/1001)\n');
    writeSet(setsRoot, 'fallback', '---\ntitle: 自动统计\n---\n\n[甲](/problem/1001)\n[乙](/problem/1002)\n[幽灵](/problem/9999)\n');

    const explicit = sets.render(sets.get('explicit'));
    assert.deepEqual(explicit.stats, { items: 895, covered: 667, linked: 1 });

    const fallback = sets.render(sets.get('fallback'));
    assert.deepEqual(fallback.stats, { items: 3, covered: 2, linked: 2 });
  } finally {
    fs.rmSync(setsRoot, { recursive: true, force: true });
  }
});

test('render is cached per slug and refreshed after file changes', () => {
  const { setsRoot, sets } = fixture();
  try {
    writeSet(setsRoot, 'cached', '---\ntitle: 缓存\n---\n\n[甲](/problem/1001)\n');
    const entry = sets.get('cached');
    const first = sets.render(entry);
    assert.equal(sets.render(entry), first);

    writeSet(setsRoot, 'cached', '---\ntitle: 缓存\n---\n\n[乙](/problem/1002)\n');
    const refreshed = sets.render(sets.get('cached'));
    assert.notEqual(refreshed, first);
    assert.deepEqual(refreshed.problemLinks.map((link) => link.id), ['1002']);
  } finally {
    fs.rmSync(setsRoot, { recursive: true, force: true });
  }
});
