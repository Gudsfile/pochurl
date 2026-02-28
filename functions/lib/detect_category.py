def detect_category(url: str) -> str:
    """Detect category based on URL patterns."""
    url_lower = url.lower()

    if "github.com" in url_lower:
        return "github"

    if any(
        pattern in url_lower
        for pattern in [
            "/docs/",
            "/documentation/",
            "readthedocs.io",
            "gitbook.io",
            "docs.",
            "/guide/",
            "/manual/",
        ]
    ):
        return "docs"

    if any(
        pattern in url_lower
        for pattern in [
            "medium.com",
            "substack.com",
            "blog.",
            ".blog",
            "/blog",
            "dev.to",
            "hashnode.dev",
        ]
    ):
        return "article"

    return "misc"
