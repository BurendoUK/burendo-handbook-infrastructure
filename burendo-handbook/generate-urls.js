const fs = require('fs');
const path = require('path');

const DOCS_DIR = path.join(__dirname, 'docs');
const BASE_URL = 'http://localhost:3000/docs'; // or your live URL

function getAllMarkdownFiles(dir, prefix = '') {
  let results = [];
  const list = fs.readdirSync(dir);

  list.forEach((file) => {
    const fullPath = path.join(dir, file);
    const relativePath = path.join(prefix, file);
    const stat = fs.statSync(fullPath);

    if (stat && stat.isDirectory()) {
      results = results.concat(getAllMarkdownFiles(fullPath, relativePath));
    } else if (file.endsWith('.md') || file.endsWith('.mdx')) {
      const noExt = relativePath.replace(/\.mdx?$/, '').replace(/\\/g, '/');
      results.push(`${BASE_URL}/${noExt}`);
    }
  });

  return results;
}

const urls = getAllMarkdownFiles(DOCS_DIR);
fs.writeFileSync('urls.txt', urls.join('\n'), 'utf-8');
console.log(`Generated ${urls.length} URLs in urls.txt`);
