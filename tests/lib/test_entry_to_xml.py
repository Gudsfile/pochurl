from functions.lib.entry_to_xml import entry_to_xml


def test_basic_entry():
    result = entry_to_xml(
        "entry123",
        "https://example.com",
        "Example Title",
        "app",
        "2024-01-01T00:00:00",
        "Example content",
    )

    assert "<entry>" in result
    assert "<id>entry123</id>" in result
    assert "<title type=" in result
    assert "Example Title" in result
    assert "<category>app</category>" in result
    assert '<link href="https://example.com"></link>' in result
    assert "<updated>2024-01-01T00:00:00</updated>" in result
    assert "<content type=" in result
    assert "Example content" in result
    assert "</entry>" in result
    assert result.startswith("<entry>")


def test_github_category():
    result = entry_to_xml(
        "abc123",
        "https://github.com/user/repo",
        "Repository Name",
        "github",
        "2024-01-01T00:00:00",
        "Description",
    )
    assert "<category>github</category>" in result


def test_special_characters_in_content():
    result = entry_to_xml(
        "entry",
        "https://example.com",
        "Title with <special> chars",
        "app",
        "2024-01-01",
        "Content with & and <![CDATA[",
    )
    assert "<![CDATA[Title with <special> chars]]></title>" in result
    assert "<![CDATA[Content with & and <![CDATA[]]></content>" in result
