#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APPLE_SCRIPT = ROOT / "scripts" / "apple_app_store.mjs"


def ensure_pythonpath():
    venv_lib = ROOT / ".venv" / "lib"
    if venv_lib.exists():
        venv_site = next(venv_lib.glob("python*/site-packages"), None)
        if venv_site and str(venv_site) not in sys.path:
            sys.path.insert(0, str(venv_site))

    target_dir = ROOT / ".python-packages"
    if target_dir.exists() and str(target_dir) not in sys.path:
        sys.path.insert(0, str(target_dir))


def ensure_google_dep():
    try:
        ensure_pythonpath()
        import google_play_scraper  # noqa: F401
        return
    except Exception as exc:  # noqa: BLE001
        raise SystemExit("google-play-scraper is not installed. Run: bash scripts/setup.sh") from exc


def run_apple(*parts):
    command = ["node", str(APPLE_SCRIPT), *parts]
    completed = subprocess.run(command, cwd=str(ROOT), check=True, capture_output=True, text=True)
    stdout = completed.stdout.strip()
    lines = [line for line in stdout.splitlines() if not line.startswith("[openclaw_state_patch]")]
    stdout = "\n".join(lines).strip()
    return json.loads(stdout)


def google_app(package_name: str, lang: str, country: str):
    ensure_google_dep()
    from google_play_scraper import app

    return app(package_name, lang=lang, country=country)


def google_search(term: str, lang: str, country: str, limit: int):
    ensure_google_dep()
    from google_play_scraper import search

    return search(term, lang=lang, country=country, n_hits=limit)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode", required=True)

    google = sub.add_parser("google")
    google_sub = google.add_subparsers(dest="command", required=True)
    google_app_p = google_sub.add_parser("app")
    google_app_p.add_argument("package")
    google_app_p.add_argument("--lang", default="en")
    google_app_p.add_argument("--country", default="us")
    google_search_p = google_sub.add_parser("search")
    google_search_p.add_argument("term")
    google_search_p.add_argument("--lang", default="en")
    google_search_p.add_argument("--country", default="us")
    google_search_p.add_argument("--limit", type=int, default=10)

    apple = sub.add_parser("apple")
    apple_sub = apple.add_subparsers(dest="command", required=True)
    apple_app_p = apple_sub.add_parser("app")
    apple_app_p.add_argument("identifier")
    apple_app_p.add_argument("--lang", default="en-us")
    apple_app_p.add_argument("--country", default="us")
    apple_search_p = apple_sub.add_parser("search")
    apple_search_p.add_argument("term")
    apple_search_p.add_argument("--lang", default="en-us")
    apple_search_p.add_argument("--country", default="us")
    apple_search_p.add_argument("--limit", type=int, default=10)

    compare = sub.add_parser("compare")
    compare.add_argument("--google", dest="google_package", required=True)
    compare.add_argument("--apple", dest="apple_identifier", required=True)
    compare.add_argument("--google-lang", default="en")
    compare.add_argument("--google-country", default="us")
    compare.add_argument("--apple-lang", default="en-us")
    compare.add_argument("--apple-country", default="us")

    args = parser.parse_args()

    if args.mode == "google" and args.command == "app":
        result = google_app(args.package, args.lang, args.country)
    elif args.mode == "google" and args.command == "search":
        result = google_search(args.term, args.lang, args.country, args.limit)
    elif args.mode == "apple" and args.command == "app":
        result = run_apple("app", args.identifier, "--lang", args.lang, "--country", args.country)
    elif args.mode == "apple" and args.command == "search":
        result = run_apple("search", args.term, "--limit", str(args.limit), "--lang", args.lang, "--country", args.country)
    elif args.mode == "compare":
        result = {
            "google": google_app(args.google_package, args.google_lang, args.google_country),
            "apple": run_apple("app", args.apple_identifier, "--lang", args.apple_lang, "--country", args.apple_country),
        }
    else:
        raise SystemExit("unsupported command")

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
