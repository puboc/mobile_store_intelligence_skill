#!/usr/bin/env node
import store from 'app-store-scraper';

const [, , command, ...args] = process.argv;

function parseArgs(argv) {
  const positional = [];
  const opts = {};
  for (let i = 0; i < argv.length; i += 1) {
    const part = argv[i];
    if (part.startsWith('--')) {
      const key = part.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith('--')) {
        opts[key] = true;
      } else {
        opts[key] = next;
        i += 1;
      }
    } else {
      positional.push(part);
    }
  }
  return { positional, opts };
}

function asInt(value, fallback) {
  const n = Number.parseInt(String(value ?? ''), 10);
  return Number.isFinite(n) ? n : fallback;
}

const { positional, opts } = parseArgs(args);
const country = String(opts.country || 'us');
const lang = String(opts.lang || 'en-us');

async function main() {
  if (command === 'app') {
    const value = positional[0];
    if (!value) throw new Error('missing app identifier');
    const payload = { country, lang };
    if (/^\d+$/.test(value)) payload.id = Number(value);
    else payload.appId = value;
    const result = await store.app(payload);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (command === 'search') {
    const term = positional.join(' ').trim();
    if (!term) throw new Error('missing search term');
    const num = asInt(opts.limit || opts.num, 10);
    const page = asInt(opts.page, 1);
    const result = await store.search({ term, num, page, country, lang });
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  throw new Error(`unsupported command: ${command || ''}`);
}

main().catch((error) => {
  console.error(error?.stack || String(error));
  process.exit(1);
});
