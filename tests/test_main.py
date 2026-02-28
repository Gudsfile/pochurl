from pytest import mark

from functions.main import CATEGORIES, URL_REGEX


@mark.parametrize(
    "input, is_a_match",
    [
        ("http://example.com", True),
        ("https://example.com/path/to/page", True),
        ("https://example.com/path?query=value", True),
        ("https://example.com:8080/path", True),
        ("http://localhost:5000", True),
        ("example.com", False),
        ("http://example", False),
        ("https://example com", False),
    ],
)
def test_url_regex(input, is_a_match):
    assert bool(URL_REGEX.match(input)) == is_a_match


def test_valid_categories():
    assert {"github", "docs", "article", "misc"} == CATEGORIES
