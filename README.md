# Pochurl

[![CI/CD Pipeline](https://github.com/Gudsfile/pochurl/actions/workflows/ci.yml/badge.svg)](https://github.com/Gudsfile/pochurl/actions/workflows/ci.yml)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Personal RSS feed for links you want to read later.

## Deployment

```shell
firebase deploy
```

## Usage

### Add Links

To add entries to your RSS feed, use your Cloud Functions endpoint:

```shell
curl --request POST \
     --url https://add-entry-<SOMETHING>.app/ \
     --header 'Content-Type: application/json' \
     --data '{
         "link": "<THE LINK TO READ LATER>"
     }'
```

You can also specify a category:

```shell
curl --request POST \
     --url https://add-entry-<SOMETHING>.app/ \
     --header 'Content-Type: application/json' \
     --data '{
         "link": "<THE LINK>",
         "category": "github"
     }'
```

Available categories: `github`, `docs`, `article`, `app`

[See more examples](#examples).

### Read Feed

Your RSS feed is available at your function's address (e.g., `https://get-entries-<SOMETHING>.app`).

You can use your favorite RSS feed reader ([NetNewsWire](https://github.com/Ranchero-Software/NetNewsWire) or any other) to read your "Read it Later" links.

### Filtered Feeds

You can also subscribe to specific categories:

- `get-github` - GitHub repositories
- `get-articles` - Blog posts and articles
- `get-docs` - Documentation
- `get-apps` - App/website links

## Examples

### Apple Shortcut

You can use the adding query in several ways.

For example, with Apple Shortcuts (like this one: [Pochurl Shortcut](https://www.icloud.com/shortcuts/d89744ccfe504ef8b504aae3b27b6aa0)) you can simply add a link to your feed from the share menu.

![Apple Shortcut usage](img/apple_shortcut.gif)
