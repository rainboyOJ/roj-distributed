import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { MarkdownRenderer } from '../server/markdown-renderer.mjs';

function render(markdown, env = {}) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'roj-markdown-test-'));
  const filePath = path.join(dir, 'content.md');
  fs.writeFileSync(filePath, markdown);
  try {
    return new MarkdownRenderer().renderFile(filePath, env);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

test('standalone anchors survive escaping so in-page links resolve', () => {
  const { html, toc } = render([
    '## 目录',
    '',
    '- [第一章 栈](#sec-1)',
    '',
    '<a id="sec-1"></a>',
    '### 第一章 栈',
    '',
    '正文。',
    ''
  ].join('\n'));

  assert.match(html, /<a id="sec-1"><\/a>/);
  assert.doesNotMatch(html, /&lt;a id=/);
  // 渲染器给标题自动加的 id 仍在，两套锚点互不干扰
  assert.match(html, /<h3 id="第一章-栈">第一章 栈<\/h3>/);
  assert.deepEqual(toc.map((item) => item.id), ['目录', '第一章-栈']);
});

test('anchors work when they directly follow a list without a blank line', () => {
  const { html } = render([
    '- [下载 a.in](https://example.com/a.in)',
    '<a id="sec-2"></a>',
    '## 下一节',
    ''
  ].join('\n'));

  assert.match(html, /<a id="sec-2"><\/a>/);
  assert.doesNotMatch(html, /&lt;a id=/);
  assert.match(html, /<h2 id="下一节">下一节<\/h2>/);
});

test('standalone html comments are dropped from the output', () => {
  const { html } = render([
    '正文第一段。',
    '',
    '<!-- roj:downloads:start -->',
    '## 下发数据',
    '',
    '- [下载 a.in](https://example.com/a.in)',
    '<!-- roj:downloads:end -->',
    '',
    '结尾。',
    ''
  ].join('\n'));

  assert.doesNotMatch(html, /roj:downloads/);
  assert.doesNotMatch(html, /&lt;!--/);
  assert.match(html, /<h2 id="下发数据">下发数据<\/h2>/);
  assert.match(html, /正文第一段。/);
  assert.match(html, /结尾。/);
});

test('other raw html stays escaped', () => {
  const { html } = render([
    '<script>alert(1)</script>',
    '',
    '<a id="x" onclick="alert(1)">点我</a>',
    '',
    '<a id="x" href="/problem/1001"></a>',
    '',
    '<a id="bad id"></a>',
    ''
  ].join('\n'));

  assert.doesNotMatch(html, /<script>/);
  assert.match(html, /&lt;script&gt;/);
  assert.doesNotMatch(html, /onclick="alert/);
  assert.match(html, /&lt;a id=/);
  assert.doesNotMatch(html, /<a id="x"><\/a>/);
});
