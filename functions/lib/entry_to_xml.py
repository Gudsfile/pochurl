def entry_to_xml(entry_id, link, title, category, updated, content):
    header = "<entry>"
    id_xml = f"""<id>{entry_id}</id>"""
    title_xml = f"""<title type="html"><![CDATA[{title}]]></title>"""
    category_xml = f"""<category>{category}</category>"""
    updated_xml = f"""<updated>{updated}</updated>"""
    content_xml = f"""<content type="html"><![CDATA[{content}]]></content>"""
    link_xml = f"""<link href="{link}"></link>"""
    footer = "</entry>"
    return "\n".join(
        [
            header,
            id_xml,
            title_xml,
            category_xml,
            link_xml,
            updated_xml,
            content_xml,
            footer,
        ]
    )
