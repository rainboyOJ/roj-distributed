import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';
import MarkdownIt from 'markdown-it';
import Katex from 'katex';
import TexMath from 'markdown-it-texmath';
import Container from 'markdown-it-container';
import taskCheckbox from 'markdown-it-task-checkbox';
import insDel from 'markdown-it-ins-del';
import sub from 'markdown-it-sub';
import sup from 'markdown-it-sup';
import mark from 'markdown-it-mark';
import abbr from 'markdown-it-abbr';
import { full as emoji } from 'markdown-it-emoji';
import twemoji from 'twemoji';

const ADMONITION_TITLES = { note: '注', info: '信息', tip: '提示', warning: '注意', danger: '警告', example: '示例', quote: '引用' };

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
}

function slugify(value) {
  const base = String(value || '').trim().toLocaleLowerCase().replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-+|-+$/g, '');
  return base || 'section';
}

function uniqueHeadingId(base, used) {
  let id = base;
  let count = 2;
  while (used.has(id)) id = `${base}-${count++}`;
  used.add(id);
  return id;
}

// 题目单/题面里的两种「安全裸 HTML」：空锚点与 HTML 注释。
// 渲染器整体是 html:false（题面来自外部抓取，不能放行任意标签），
// 但这两类必须原样生效，否则会在页面上显示成转义后的文字：
//   - `<a id="sec-1"></a>`：题目单正文目录的锚点，放行后才能让 `#sec-1` 跳转；
//   - `<!-- ... -->`：生成区块标记（如 `<!-- ybt:generated:start -->`）与
//     `<!-- roj:downloads:start -->`，应当不可见。
// id 只允许字母/数字/下划线/连字符，避免把任意属性放进来。
const SAFE_ANCHOR_RE = /^<a\s+id="([A-Za-z0-9_-]+)"\s*>\s*<\/a>$/;
const HTML_COMMENT_RE = /^<!--.*-->$/;

function standaloneLine(state, line) {
  const start = state.bMarks[line] + state.tShift[line];
  return state.src.slice(start, state.eMarks[line]).trim();
}

function safeRawBlocks(md) {
  // alt 里带 paragraph：让这两类块同时充当段落终止符。
  // 否则紧跟在列表/段落后面、中间没有空行的锚点或注释会被吞进段落里。
  md.block.ruler.before('paragraph', 'roj_safe_anchor', (state, startLine, endLine, silent) => {
    const match = SAFE_ANCHOR_RE.exec(standaloneLine(state, startLine));
    if (!match) return false;
    if (silent) return true;
    const token = state.push('roj_anchor', '', 0);
    token.map = [startLine, startLine + 1];
    token.content = match[1];
    state.line = startLine + 1;
    return true;
  }, { alt: ['paragraph'] });

  md.block.ruler.before('paragraph', 'roj_html_comment', (state, startLine, endLine, silent) => {
    if (!HTML_COMMENT_RE.test(standaloneLine(state, startLine))) return false;
    if (silent) return true;
    state.line = startLine + 1;  // 整行丢弃，不产出 token
    return true;
  }, { alt: ['paragraph'] });

  md.renderer.rules.roj_anchor = (tokens, index) => `<a id="${escapeHtml(tokens[index].content)}"></a>\n`;
}

function normalizeLanguage(value) {
  const language = String(value || '').trim().toLocaleLowerCase().split(/\s+/, 1)[0] || 'text';
  const map = { cxx: 'cpp', 'c++': 'cpp', cc: 'cpp', h: 'c', py: 'python', js: 'javascript', ts: 'typescript', sh: 'bash', plaintext: 'text', plain: 'text' };
  return map[language] || language.replace(/[^a-z0-9_-]/g, '') || 'text';
}

function encodePath(value) {
  return value.split('/').map((part) => encodeURIComponent(part)).join('/');
}

function localImageUrl(src, env) {
  const cleanSrc = src.split('#', 1)[0].split('?', 1)[0];
  const resourceDir = env.resourceDir || env.problemDir;
  if (!resourceDir || !cleanSrc || cleanSrc.startsWith('/') || cleanSrc.includes('\\') || cleanSrc.includes('..')) return null;
  const fullPath = path.resolve(resourceDir, cleanSrc);
  const relative = path.relative(resourceDir, fullPath);
  const normalizedRelative = relative.split(path.sep).join('/');
  const extension = path.extname(fullPath).toLocaleLowerCase();
  if (!relative || relative.startsWith('..') || path.isAbsolute(relative) || !['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'].includes(extension)) return null;
  if (env.assetScope && normalizedRelative !== env.assetScope && !normalizedRelative.startsWith(`${env.assetScope}/`)) return null;
  if (!fs.existsSync(fullPath) || !fs.statSync(fullPath).isFile()) return null;
  const assetBase = env.assetBase || `/problem/${encodeURIComponent(env.problemId)}/asset`;
  const urlRelative = env.assetScope && normalizedRelative.startsWith(`${env.assetScope}/`)
    ? normalizedRelative.slice(env.assetScope.length + 1)
    : normalizedRelative;
  return `${assetBase}/${encodePath(urlRelative)}`;
}

function addHeadingIds(tokens, env) {
  const used = new Set();
  for (let index = 0; index < tokens.length; index += 1) {
    const token = tokens[index];
    if (token.type !== 'heading_open' || !['h2', 'h3'].includes(token.tag)) continue;
    const inline = tokens[index + 1];
    const id = uniqueHeadingId(slugify(inline?.content), used);
    token.attrSet('id', id);
    env.toc.push({ id, level: Number(token.tag.slice(1)), text: inline?.content || '' });
  }
}

function extractProblemLinks(tokens) {
  const links = [];
  const seen = new Set();
  for (const token of tokens) {
    if (token.type !== 'inline' || !token.children) continue;
    for (let index = 0; index < token.children.length; index += 1) {
      const child = token.children[index];
      if (child.type !== 'link_open') continue;
      const href = child.attrGet('href') || '';
      const match = href.match(/^\/problem\/(\d+)(?:[?#].*)?\/?$/);
      if (!match || seen.has(match[1])) continue;
      const labelParts = [];
      for (let labelIndex = index + 1; labelIndex < token.children.length; labelIndex += 1) {
        const labelToken = token.children[labelIndex];
        if (labelToken.type === 'link_close') break;
        if (['text', 'code_inline', 'emoji'].includes(labelToken.type)) labelParts.push(labelToken.content);
      }
      seen.add(match[1]);
      links.push({ id: match[1], label: labelParts.join('').trim() || match[1] });
    }
  }
  return links;
}

/**
 * 题目单渲染：给 /problem/<id> 链接加进度复选框；死链降级标注，不静默失败。
 * 只在 env.decorateProblemLinks 开启时生效，不影响题面/比赛渲染。
 */
function decorateProblemLinks(tokens, env) {
  const exists = typeof env.problemExists === 'function' ? env.problemExists : () => true;
  for (const token of tokens) {
    if (token.type !== 'inline' || !token.children) continue;
    for (let index = 0; index < token.children.length; index += 1) {
      const child = token.children[index];
      if (child.type !== 'link_open') continue;
      const match = (child.attrGet('href') || '').match(/^\/problem\/(\d+)(?:[?#].*)?\/?$/);
      if (!match) continue;
      const id = match[1];
      child.meta = { problemId: id };
      if (!exists(id)) {
        child.attrJoin('class', 'problem-link is-missing');
        child.attrSet('title', `题目 ${id} 在本站不存在`);
        continue;
      }
      child.attrJoin('class', 'problem-link');
      if (!env.progressCheckboxes) continue;
      child.meta.checkbox = true;
      for (let closeIndex = index + 1; closeIndex < token.children.length; closeIndex += 1) {
        const candidate = token.children[closeIndex];
        if (candidate.type !== 'link_close') continue;
        candidate.meta = { checkboxFor: id };
        break;
      }
    }
  }
}

export class MarkdownRenderer {
  constructor() {
    this.md = new MarkdownIt({ html: false, linkify: true, typographer: true, breaks: false });
    this.md.use(safeRawBlocks);
    this.md.use(TexMath, { engine: Katex, delimiters: ['dollars', 'beg_end', 'julia'], katexOptions: { strict: false, throwOnError: false, macros: { '\\R': '\\mathbb{R}' } } });
    this.md.use(taskCheckbox, { disabled: true });
    this.md.use(insDel).use(sub).use(sup).use(mark).use(abbr).use(emoji);

    this.md.use(Container, 'line', {
      validate: (params) => params.trim() === 'line',
      render: (tokens, index) => tokens[index].nesting === 1 ? '<div class="sample-group">\n' : '</div>\n'
    });

    for (const type of Object.keys(ADMONITION_TITLES)) {
      this.md.use(Container, type, {
        validate: (params) => params.trim().split(/\s+/, 1)[0] === type,
        render: (tokens, index) => tokens[index].nesting === 1
          ? `<aside class="admonition admonition-${type}"><div class="admonition-title">${ADMONITION_TITLES[type]}</div>\n`
          : '</aside>\n'
      });
    }

    this.md.renderer.rules.fence = (tokens, index) => {
      const token = tokens[index];
      const language = normalizeLanguage(token.info);
      const content = token.content.replace(/\n$/, '');
      const label = language === 'text' ? '文本' : language;
      return `<div class="code-block"><div class="code-toolbar"><span class="code-language">${escapeHtml(label)}</span><button class="code-copy-button" type="button" data-copy-code>复制</button></div><pre><code class="language-${escapeHtml(language)}">${escapeHtml(content)}</code></pre></div>\n`;
    };

    this.md.renderer.rules.image = (tokens, index, options, env) => {
      const token = tokens[index];
      const source = token.attrGet('src') || '';
      const alt = token.content || '题面图片';
      const remote = /^(?:https?:)?\/\//i.test(source) ? source.replaceAll(' ', '%20') : null;
      const local = remote ? null : localImageUrl(source, env);
      if (!remote && !local) return `<span class="md-image-missing" role="img" aria-label="${escapeHtml(alt)}">图片暂缺：${escapeHtml(alt)}</span>`;
      const title = token.attrGet('title');
      const titleAttr = title ? ` title="${escapeHtml(title)}"` : '';
      return `<img class="md-image" src="${escapeHtml(remote || local)}" alt="${escapeHtml(alt)}" loading="lazy"${titleAttr}>`;
    };

    const defaultLinkOpen = this.md.renderer.rules.link_open || ((tokens, index, opts, env, self) => self.renderToken(tokens, index, opts));
    this.md.renderer.rules.link_open = (tokens, index, options, env, self) => {
      const href = tokens[index].attrGet('href') || '';
      if (/^https?:\/\//i.test(href)) {
        tokens[index].attrSet('target', '_blank');
        tokens[index].attrSet('rel', 'noopener noreferrer');
      }
      const html = defaultLinkOpen(tokens, index, options, env, self);
      if (!tokens[index].meta?.checkbox) return html;
      const id = tokens[index].meta.problemId;
      return `<span class="progress-item">${
        `<input class="progress-checkbox" type="checkbox" data-progress-id="${escapeHtml(id)}" aria-label="标记题目 ${escapeHtml(id)} 已完成">`
      }${html}`;
    };

    this.md.renderer.rules.link_close = (tokens, index, options, env, self) => {
      const html = self.renderToken(tokens, index, options);
      return tokens[index].meta?.checkboxFor ? `${html}</span>` : html;
    };

    this.md.renderer.rules.emoji = (tokens, index) => twemoji.parse(tokens[index].content);
  }

  renderFile(filePath, env = {}) {
    const parsed = matter(fs.readFileSync(filePath, 'utf8'));
    const renderEnv = { ...env, toc: [] };
    const tokens = this.md.parse(parsed.content, renderEnv);
    addHeadingIds(tokens, renderEnv);
    if (env.decorateProblemLinks) decorateProblemLinks(tokens, renderEnv);
    return {
      html: this.md.renderer.render(tokens, this.md.options, renderEnv),
      toc: renderEnv.toc,
      frontMatter: parsed.data,
      problemLinks: extractProblemLinks(tokens)
    };
  }
}
