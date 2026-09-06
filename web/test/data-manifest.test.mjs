import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { archiveFileName, downloadSources, normalizeDownloadConfig } from '../server/download-config.mjs';
import { isPublicDataPath, readDataManifest } from '../server/data-manifest.mjs';

function temporaryDirectory() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'roj-manifest-test-'));
}

test('public data paths reject traversal and unsupported names', () => {
  assert.equal(isPublicDataPath('sample/01.in'), true);
  assert.equal(isPublicDataPath('sample/01.OUT'), true);
  assert.equal(isPublicDataPath('../01.in'), false);
  assert.equal(isPublicDataPath('sample/../01.in'), false);
  assert.equal(isPublicDataPath('sample\\01.in'), false);
  assert.equal(isPublicDataPath('.cache/01.in'), false);
  assert.equal(isPublicDataPath('std.cpp'), false);
});

test('data manifest reads sorted public files without touching data contents', () => {
  const root = temporaryDirectory();
  try {
    fs.writeFileSync(path.join(root, 'data.json'), JSON.stringify({
      files: [
        { path: '1.ans', size: 8 },
        { path: '1.in', size: 4 }
      ]
    }));
    const manifest = readDataManifest(root, { warn() {} });
    assert.deepEqual(manifest, {
      files: [
        { path: '1.ans', size: 8 },
        { path: '1.in', size: 4 }
      ],
      invalid: false,
      reason: null
    });
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('missing or invalid data manifests become empty and invalid', () => {
  const root = temporaryDirectory();
  try {
    const missing = readDataManifest(root, { warn() {} });
    assert.equal(missing.invalid, true);
    assert.deepEqual(missing.files, []);

    fs.writeFileSync(path.join(root, 'data.json'), JSON.stringify({ files: [{ path: '../private.in', size: 2 }] }));
    const invalid = readDataManifest(root, { warn() {} });
    assert.equal(invalid.invalid, true);
    assert.deepEqual(invalid.files, []);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('download config normalizes archive sources and drops invalid entries', () => {
  const config = normalizeDownloadConfig({
    download: {
      sources: [
        { id: 'csps', label: '主站', baseUrl: 'https://csps.de5.net/roj-data/' },
        { id: 'broken', label: '坏源', baseUrl: 'file:///private' },
        { id: 'unparsable', baseUrl: 'not-a-url' }
      ]
    }
  });
  assert.deepEqual(config.download.sources, [
    { id: 'csps', label: '主站', baseUrl: 'https://csps.de5.net/roj-data/' }
  ]);
  assert.deepEqual(downloadSources(config), config.download.sources);
});

test('missing or empty sources fall back to the two default channels', () => {
  const config = normalizeDownloadConfig({});
  assert.deepEqual(config.download.sources, [
    { id: 'csps', label: '主站 csps.de5.net', baseUrl: 'https://csps.de5.net/roj-data/' },
    { id: 'oidata', label: '备用 oidata.cc.cd', baseUrl: 'https://oidata.cc.cd/roj-data/' }
  ]);
});

test('archive file name is derived from the numeric problem id', () => {
  assert.equal(archiveFileName('1460'), '1460.tar.zst');
});
