# AGENTS.md

## Project Overview

Pochurl - Personal RSS feed powered by API, deployed on Firebase Cloud Functions (Python).

- **Stack**: Python 3.10, Firebase Cloud Functions, Firestore
- **functions/** folder: Cloud Functions code
- **Entry point**: `functions/main.py`
- **Tests**: `functions/tests/`

## Development Commands

```bash
# Install dependencies using uv (recommended)
uv sync

# Install dev dependencies only
uv sync --group dev

# Run all tests
uv run pytest

# Run a single test file
uv run pytest functions/tests/test_main.py

# Run a single test by name
uv run pytest functions/tests/test_main.py::TestUrlValidation::test_valid_https_url

# Run tests with verbose output
uv run pytest -v

# Run linter (ruff check)
uv run ruff check

# Run formatter check
uv run ruff format --check

# Auto-fix linting issues
uv run ruff check --fix

# Format code automatically
uv run ruff format

# Local development with Firebase emulators
firebase emulators:start

# Deploy to Firebase (requires authentication)
firebase deploy
```

## Code Style Guidelines

### General

- Python with type hints required for all function signatures
- Use f-strings for string formatting
- 4 spaces indentation (no tabs)
- Maximum ~75 lines per function
- Maximum line length: 88 characters (ruff default)

### Naming Conventions

- **Functions**: `snake_case` (e.g., `detect_category`, `extract_content`)
- **Classes**: `PascalCase` (e.g., `TestUrlValidation`, `TestDetectCategory`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `URL_REGEX`, `CATEGORIES`, `FEED_HEADER`)
- **Variables**: `snake_case` (e.g., `entry_id`, `link`, `title`)
- **Private functions**: prefix with underscore (e.g., `_helper_function`)

### Imports

- Standard library imports first
- Third-party imports second
- Local imports last
- Separate groups with blank lines
- Sort imports alphabetically within each group

### Type Hints

- Use type hints for all function parameters and return types
- Use `typing` module for complex types (List, Dict, Optional, etc.)

### Docstrings

- Use triple quotes for docstrings
- First line: brief description (imperative mood)
- Subsequent lines: detailed explanation if needed
- Include args, returns, raises sections for complex functions

### Error Handling

- Use specific exception types when possible
- Return appropriate HTTP status codes for HTTP functions
- Handle failures gracefully (e.g., fallback to trafilatura on readability failure)

### Firebase Cloud Functions

- Use `@https_fn.on_request()` decorator for HTTP endpoints
- Use `https_fn.Request` and `https_fn.Response` types
- Return `https_fn.Response` with appropriate status codes

### Firestore

- Collection: `entries`
- Document ID: base64 encoded URL
- Fields: `link`, `title`, `updated`, `xml_content`, `category`

## Testing Guidelines

- Use pytest with pytest-mock for mocking
- Test classes: prefix with `Test` (e.g., `TestUrlValidation`)
- Test methods: prefix with `test_` (e.g., `test_valid_https_url`)
- Test one thing per test method
- Use descriptive test names that explain what is being tested

## Architecture

### Firestore Schema

- **Collection**: `entries`
- **Document ID**: base64 encoded URL
- **Fields**:
  - `link` (string): original URL
  - `title` (string): page title
  - `category` (string): one of "github", "docs", "article", "app"
  - `updated` (string): ISO format timestamp
  - `xml_content` (string): pre-rendered XML entry

### HTTP Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/add_entry` | POST | Add/update entry with `{"link": "..."}` |
| `/get_entries` | GET | Get all entries as RSS XML |
| `/get_github` | GET | Get GitHub entries as RSS |
| `/get_articles` | GET | Get article entries as RSS |
| `/get_docs` | GET | Get documentation entries as RSS |
| `/get_apps` | GET | Get app/site entries as RSS |

## Deployment

- Via GitHub Action (`.github/workflows/release.yml`)
- Triggers on published GitHub release
- Generates `requirements.txt` via `uv export --format requirements-txt`

## Rules

- Always read `MY_NOTES.md` for context on current tasks
- Check `firestore.rules` before any data modification
- Do not commit secrets (use `.gitignore`)
- Do not commit `MY_NOTES.md` file
- Run lint and tests before committing

## Commit Rules

- In English
- Use conventional commits with emoji prefix: `✨`, `🔄`, `📝`, `✅`, `🔧`, `🚑`, etc.
- Examples: `✨ Add new feature`, `🔄 Refactor code`, `📝 Update docs`, `✅ Add tests`, `🔧 Fix bug`
- Always commit after completing a task (don't leave changes uncommitted)
