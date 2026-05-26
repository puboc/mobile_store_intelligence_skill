---
name: Mobile Store Intelligence
---

Use this skill when the user wants app intelligence from the Apple App Store or Google Play Store.

## What this skill handles

- Look up app details by App Store ID, bundle ID, or Google Play package name
- Search the Apple App Store by keyword
- Search the Google Play Store by keyword
- Compare the same product across iOS and Android stores
- Pull ratings, reviews, install signals, pricing, developer info, and release metadata

## Workspace files

- `vendor/app-store-scraper` — vendored Apple App Store scraper source
- `vendor/google-play-scraper` — vendored Google Play scraper source
- `requirements.txt` — Python install target for the vendored Google Play scraper
- `package.json` — Node install target for the vendored Apple App Store scraper
- `scripts/setup.sh` — installs local dependencies into this skill folder from vendored sources
- `scripts/mobile_store_intel.py` — unified CLI wrapper
- `scripts/apple_app_store.mjs` — Apple App Store adapter

## First step

If `.venv` or `node_modules` is missing, run:

```bash
bash scripts/setup.sh
```

## Commands

### Google Play app detail

```bash
python3 scripts/mobile_store_intel.py google app com.duolingo.learningapp
```

### Google Play search

```bash
python3 scripts/mobile_store_intel.py google search duolingo --limit 5
```

### Apple App Store app detail by numeric id

```bash
python3 scripts/mobile_store_intel.py apple app 570060128
```

### Apple App Store app detail by bundle id

```bash
python3 scripts/mobile_store_intel.py apple app com.duolingo
```

### Apple App Store search

```bash
python3 scripts/mobile_store_intel.py apple search duolingo --limit 5
```

### Compare both stores

```bash
python3 scripts/mobile_store_intel.py compare \
  --google com.duolingo.learningapp \
  --apple com.duolingo
```

## Notes

- Apple lookups use the vendored `app-store-scraper` Node package.
- Google Play lookups use the vendored `google-play-scraper` Python package.
- Setup installs from local vendored source; no GitHub pull is required at runtime.
- Country defaults to `us` and language defaults to `en` unless overridden.
- Output is JSON so other scripts and agents can consume it easily.
