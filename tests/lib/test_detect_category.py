from pytest import mark

from functions.lib.detect_category import detect_category


@mark.parametrize(
    "url, category",
    [
        ("https://github.com/user/repo", "github"),
        ("https://github.com/orgname", "github"),
        ("https://gist.github.com/user/id", "github"),
        ("https://docs.example.com", "docs"),
        ("https://example.com/docs/", "docs"),
        ("https://package.readthedocs.io", "docs"),
        ("https://book.gitbook.io", "docs"),
        ("https://example.com/guide/", "docs"),
        ("https://example.com/manual/", "docs"),
        ("https://medium.com/@user/post", "article"),
        ("https://user.substack.com/p/post", "article"),
        ("https://blog.example.com/post", "article"),
        ("https://dev.to/user/post", "article"),
        ("https://user.hashnode.dev/post", "article"),
        ("https://github.blog/open-source/maintainers/what-to-expect-for-open-source-in-2026/", "article"),
        ("https://example.com", "misc"),
        ("https://example.com/about", "misc"),
        ("HTTPS://GITHUB.COM/USER/REPO", "github"),
    ],
)
def test_detect_category(url, category):
    assert detect_category(url) == category
