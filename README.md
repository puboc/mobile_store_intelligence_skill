# Mobile Store Intelligence Skill

Skill repo for querying Apple App Store and Google Play metadata from OpenClaw-compatible agents.

## Included upstream libraries

- `app-store-scraper` (Node.js) for Apple App Store lookups
- `google-play-scraper` (Python) for Google Play lookups

## Quick start

```bash
bash scripts/setup.sh
python3 scripts/mobile_store_intel.py google app com.duolingo.learningapp
python3 scripts/mobile_store_intel.py apple search duolingo --limit 5
```
