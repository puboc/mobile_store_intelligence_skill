# Mobile Store Intelligence Skill

Skill repo for querying Apple App Store and Google Play metadata from OpenClaw-compatible agents.

## Vendored upstream repositories

This repo includes local copies of:

- `vendor/app-store-scraper` — https://github.com/facundoolano/app-store-scraper
- `vendor/google-play-scraper` — https://github.com/JoMingyu/google-play-scraper

The setup script installs from these local vendored sources so runtime does not need to clone or pull them from GitHub.

## Quick start

```bash
bash scripts/setup.sh
python3 scripts/mobile_store_intel.py google app com.duolingo.learningapp
python3 scripts/mobile_store_intel.py apple search duolingo --limit 5
```
