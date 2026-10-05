import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';

const DISPLAY_KEYS = new Set(['title', 'description', 'tags', 'order', 'draft', 'items', 'covered', 'source']);

function optionalString(value) {
  return typeof value === 'string' && value.trim() ? value.trim() : null;
}

function optionalCount(value) {
  const count = Number(value);
  return Number.isInteger(count) && count >= 0 ? count : null;
}

function formatValue(value) {
  if (Array.isArray(value)) return value.map((item) => formatValue(item)).join(', ');
  if (value && typeof value === 'object') return JSON.stringify(value);
  return String(value);
}

function metadataEntries(data, entry) {
  const fields = [];
  const add = (label, value) => {
    if (value !== null && value !== undefined && value !== '') fields.push({ label, value: formatValue(value) });
  };

  add('简介', entry.description);
  add('标签', entry.tags.length ? entry.tags : null);
  add('题目数', entry.items);
  add('本站收录', entry.covered);
  add('来源', entry.source);

  for (const [key, value] of Object.entries(data)) {
    if (DISPLAY_KEYS.has(key) || value === null || value === undefined || value === '') continue;
    add(key, value);
  }
  return fields;
}

function fileSignature(rootDir) {
  if (!fs.existsSync(rootDir)) return 'missing';
  const files = fs.readdirSync(rootDir, { withFileTypes: true })
    .filter((item) => item.isFile() && path.extname(item.name).toLocaleLowerCase() === '.md')
    .map((item) => {
      const filePath = path.join(rootDir, item.name);
      try {
        const stat = fs.statSync(filePath);
        return `${item.name}:${stat.mtimeMs}:${stat.size}`;
      } catch {
        return null;
      }
    })
    .filter(Boolean)
    .sort();
  return files.join('|');
}

export class ProblemSetCatalog {
  constructor(rootDir, renderer, problemCatalog, options = {}) {
    this.rootDir = path.resolve(rootDir);
    this.renderer = renderer;
    this.problemCatalog = problemCatalog;
    this.logger = options.logger || console;
    this.entries = [];
    this.signature = null;
    this.renderCache = new Map();
  }

  refreshIfNeeded() {
    const signature = fileSignature(this.rootDir);
    if (signature !== this.signature) this.load(signature);
    return this.entries;
  }

  load(signature = fileSignature(this.rootDir)) {
    const entries = [];
    const seen = new Set();
    let names = [];
    try {
      names = fs.readdirSync(this.rootDir, { withFileTypes: true });
    } catch (error) {
      this.logger.warn?.({ err: error, problemSetsRoot: this.rootDir }, 'Problem set directory cannot be read');
    }

    for (const item of names) {
      if (!item.isFile() || path.extname(item.name).toLocaleLowerCase() !== '.md') continue;
      const slug = path.basename(item.name, path.extname(item.name));
      if (!/^[a-z0-9_-]+$/.test(slug)) {
        this.logger.warn?.({ file: item.name }, 'Problem set file has an invalid slug');
        continue;
      }
      if (seen.has(slug)) {
        this.logger.warn?.({ slug, file: item.name }, 'Duplicate problem set slug');
        continue;
      }

      const filePath = path.join(this.rootDir, item.name);
      let parsed;
      try {
        parsed = matter(fs.readFileSync(filePath, 'utf8'));
      } catch (error) {
        this.logger.warn?.({ err: error, file: item.name }, 'Problem set frontmatter cannot be parsed');
        continue;
      }
      if (!parsed.data || typeof parsed.data !== 'object' || Array.isArray(parsed.data)) {
        this.logger.warn?.({ file: item.name }, 'Problem set frontmatter must be an object');
        continue;
      }

      const title = optionalString(parsed.data.title);
      if (!title) {
        this.logger.warn?.({ file: item.name }, 'Problem set title is missing');
        continue;
      }
      if (parsed.data.draft === true) continue;

      const order = Number(parsed.data.order);
      const tags = Array.isArray(parsed.data.tags)
        ? parsed.data.tags.filter((tag) => typeof tag === 'string' && tag.trim()).map((tag) => tag.trim())
        : [];
      const entry = {
        slug,
        title,
        description: optionalString(parsed.data.description),
        tags,
        order: Number.isFinite(order) ? order : null,
        items: optionalCount(parsed.data.items),
        covered: optionalCount(parsed.data.covered),
        source: optionalString(parsed.data.source),
        filePath,
        metadata: null
      };
      entry.metadata = metadataEntries(parsed.data, entry);
      entries.push(entry);
      seen.add(slug);
    }

    entries.sort((a, b) => {
      if (a.order !== null && b.order !== null && a.order !== b.order) return a.order - b.order;
      if (a.order !== null && b.order === null) return -1;
      if (a.order === null && b.order !== null) return 1;
      return a.title.localeCompare(b.title, 'zh-Hans-CN');
    });
    this.entries = entries;
    this.signature = signature;
    this.renderCache.clear();
    return entries;
  }

  list() {
    return this.refreshIfNeeded();
  }

  get(slug) {
    this.refreshIfNeeded();
    return this.entries.find((entry) => entry.slug === String(slug)) || null;
  }

  render(entry) {
    if (!entry) return null;
    this.refreshIfNeeded();
    const cached = this.renderCache.get(entry.slug);
    if (cached) return cached;

    const rendered = this.renderer.renderFile(entry.filePath, {
      resourceDir: this.rootDir,
      assetScope: entry.slug,
      assetBase: `/problem-set/${encodeURIComponent(entry.slug)}/asset`,
      decorateProblemLinks: true,
      progressCheckboxes: true,
      problemExists: (id) => Boolean(this.problemCatalog.get(id))
    });

    const validLinks = [];
    const missingLinks = [];
    for (const link of rendered.problemLinks) {
      const problem = this.problemCatalog.get(link.id);
      if (!problem) {
        this.logger.warn?.({ problemSet: entry.slug, problemId: link.id }, 'Problem set links to a missing problem');
        missingLinks.push(link);
        continue;
      }
      validLinks.push({ ...link, title: problem.title, href: `/problem/${encodeURIComponent(problem.id)}` });
    }

    // 显式统计优先（由生成脚本维护）；否则按正文链接计数。
    const items = entry.items ?? validLinks.length + missingLinks.length;
    const covered = entry.covered ?? validLinks.length;

    const result = {
      ...rendered,
      problemLinks: validLinks,
      missingLinks,
      stats: { items, covered, linked: validLinks.length }
    };
    this.renderCache.set(entry.slug, result);
    return result;
  }

  assetPath(entry, resourcePath) {
    if (!entry || typeof resourcePath !== 'string' || resourcePath.includes('\0')) return null;
    let decoded;
    try {
      decoded = decodeURIComponent(resourcePath).replaceAll('\\', '/');
    } catch {
      return null;
    }
    if (!decoded || decoded.startsWith('/') || decoded.includes('..')) return null;
    const extension = path.extname(decoded).toLocaleLowerCase();
    if (!['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'].includes(extension)) return null;
    const resolved = path.resolve(this.rootDir, entry.slug, decoded);
    const relative = path.relative(path.join(this.rootDir, entry.slug), resolved);
    if (!relative || relative.startsWith('..') || path.isAbsolute(relative)) return null;
    if (!fs.existsSync(resolved) || !fs.statSync(resolved).isFile()) return null;
    return resolved;
  }
}
