# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pochurl is a personal "read it later" RSS feed powered by Firebase Cloud Functions (Python 3.13) and Firestore. Users POST links to an HTTP endpoint; the function fetches the page, extracts content via `readability-lxml`, categorizes it, and stores an Atom XML entry in Firestore. GET endpoints serve Atom feeds filtered by category.

## Commands

```bash
# Install dependencies
uv sync

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_main.py

# Run a single test by name
uv run pytest tests/test_main.py::test_url_regex

# Lint
uv run ruff check

# Format check
uv run ruff format --check

# Auto-fix and format
uv run ruff check --fix && uv run ruff format

# Regenerate functions/requirements.txt and virtual env (needed before deploy and emulate)
make functions-requirements && make functions-venv

# Start Firebase emulators locally
make emulators

# Deploy to Firebase
firebase deploy
```

## Architecture

### Code Structure

- `functions/main.py` — Cloud Functions entry point; defines all HTTP endpoints decorated with `@https_fn.on_request(region="europe-west1")`
- `functions/lib/detect_category.py` — URL-pattern-based category detection (github, docs, article, app)
- `functions/lib/extract_content.py` — Fetches page and extracts title + HTML content via `readability-lxml`
- `functions/lib/entry_to_xml.py` — Renders a single Atom `<entry>` XML string
- `tests/` — pytest tests; `pythonpath = ["functions"]` so imports work as `from functions.main import ...` and `from lib.xxx import ...`

### Data Flow

1. `POST /add_entry` with `{"link": "..."}` → validate URL → auto-detect or use provided category → `extract_content` → `entry_to_xml` → upsert Firestore doc
2. `GET /get_entries` (or `/get_github`, `/get_articles`, `/get_docs`, `/get_apps`) → query Firestore `entries` collection → join pre-rendered `xml_content` fields → return Atom feed

### Firestore Schema

- **Collection**: `entries`
- **Document ID**: base64-encoded URL
- **Fields**: `link`, `title`, `category`, `updated` (ISO timestamp), `xml_content` (pre-rendered Atom `<entry>`)

### Key Design Choice

`xml_content` is pre-rendered and stored at write time, so feed generation is a simple string join with no per-entry processing.

## Rules

- Always read `MY_NOTES.md` for context on current tasks (do not commit this file)
- Run lint and tests before committing
- Commits must use conventional commits with emoji prefix: `✨ feat`, `🔧 fix`, `🔄 refactor`, `✅ test`, `📝 docs`
- Line length: 120 characters (ruff config)
