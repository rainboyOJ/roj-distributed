import fs from 'node:fs';
import path from 'node:path';
import { parse } from 'yaml';

export const DEFAULT_DOWNLOAD_CONFIG = Object.freeze({
  download: {
    sources: [
      { id: 'csps', label: '主站 csps.de5.net', baseUrl: 'https://csps.de5.net/roj-data/' },
      { id: 'oidata', label: '备用 oidata.cc.cd', baseUrl: 'https://oidata.cc.cd/roj-data/' }
    ]
  }
});

function asObject(value) {
  return value && typeof value === 'object' && !Array.isArray(value) ? value : {};
}

function optionalUrl(value) {
  if (typeof value !== 'string' || !value.trim()) return null;
  try {
    const url = new URL(value.trim());
    return url.protocol === 'http:' || url.protocol === 'https:' ? url.toString().replace(/\/$/, '') : null;
  } catch {
    return null;
  }
}

function normalizeSource(value, index) {
  const item = asObject(value);
  const id = typeof item.id === 'string' && item.id.trim() ? item.id.trim() : `source-${index}`;
  const label = typeof item.label === 'string' && item.label.trim() ? item.label.trim() : id;
  const url = optionalUrl(item.baseUrl);
  if (!url) return null;
  return { id, label, baseUrl: `${url}/` };
}

export function normalizeDownloadConfig(value = {}) {
  const root = asObject(value);
  const download = asObject(root.download);
  let sources = Array.isArray(download.sources)
    ? download.sources.map(normalizeSource).filter(Boolean)
    : [];
  if (!sources.length) sources = [...DEFAULT_DOWNLOAD_CONFIG.download.sources];
  return { download: { sources } };
}

export function loadDownloadConfig(configPath, logger = console) {
  let parsed = {};
  let invalid = false;
  try {
    const source = fs.readFileSync(path.resolve(configPath), 'utf8');
    parsed = parse(source) || {};
  } catch (error) {
    if (error.code !== 'ENOENT') {
      invalid = true;
      logger.warn?.({ err: error, configPath }, 'Download config could not be read; using defaults');
    }
  }
  const config = normalizeDownloadConfig(parsed);
  return { config, invalid, configPath: path.resolve(configPath) };
}

export function archiveFileName(problemId) {
  return `${encodeURIComponent(problemId)}.tar.zst`;
}

export function downloadSources(config) {
  return config.download.sources;
}
