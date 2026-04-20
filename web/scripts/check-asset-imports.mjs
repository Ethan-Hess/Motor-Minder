import { readdir, readFile } from 'node:fs/promises';
import { join, relative } from 'node:path';

const SRC_DIR = new URL('../src', import.meta.url);
const SOURCE_EXTENSIONS = new Set(['.js', '.jsx', '.ts', '.tsx']);
const FORBIDDEN_IMPORT = /from\s+["']\/assets\//;

async function getSourceFiles(dirPath) {
  const entries = await readdir(dirPath, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    const fullPath = join(dirPath, entry.name);

    if (entry.isDirectory()) {
      files.push(...(await getSourceFiles(fullPath)));
      continue;
    }

    const ext = entry.name.slice(entry.name.lastIndexOf('.'));
    if (SOURCE_EXTENSIONS.has(ext)) {
      files.push(fullPath);
    }
  }

  return files;
}

async function findForbiddenImports() {
  const srcPath = SRC_DIR.pathname;
  const files = await getSourceFiles(srcPath);
  const violations = [];

  for (const filePath of files) {
    const content = await readFile(filePath, 'utf8');
    const lines = content.split('\n');

    lines.forEach((line, index) => {
      if (FORBIDDEN_IMPORT.test(line)) {
        violations.push({
          file: relative(process.cwd(), filePath),
          line: index + 1,
          text: line.trim(),
        });
      }
    });
  }

  return violations;
}

const violations = await findForbiddenImports();

if (violations.length > 0) {
  console.error('Disallowed root asset import(s) found. Use @/assets/... for source assets.');
  for (const item of violations) {
    console.error(`- ${item.file}:${item.line} ${item.text}`);
  }
  process.exit(1);
}

console.log('Asset import check passed.');
