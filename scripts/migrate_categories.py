"""
2026-02-28
Migrate existing Firestore entries to add the category field.

Older entries don't have the 'category' field, which causes them to be
missing from filtered feeds (get_github, get_articles, etc.). This script:
1. Fetches all entries without a 'category' field
2. Detects category based on URL patterns
3. Regenerates xml_content with the category
4. Updates only 'category' and 'xml_content' fields (does NOT modify 'updated')

Usage:
    uv run python -m scripts.migrate_categories
"""

import firebase_admin
from firebase_admin import credentials, firestore

from functions.lib.detect_category import detect_category
from functions.lib.entry_to_xml import entry_to_xml
from functions.lib.extract_content import extract_content


def main():
    if not firebase_admin._apps:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    entries_ref = db.collection("entries")

    docs_without_category = [doc for doc in entries_ref.stream() if doc.to_dict().get("category") is None]

    if not docs_without_category:
        print("No entries to migrate.")
        return

    print(f"Found {len(docs_without_category)} entries without category.")
    print("Starting migration...\n")

    batch = db.batch()
    count_by_category: dict[str, int] = {}

    for doc in docs_without_category:
        entry_id = doc.id
        link = doc.get("link")
        title = doc.get("title")
        updated = doc.get("updated")
        _, content = extract_content(link)
        category = detect_category(link)
        xml_content = entry_to_xml(entry_id, link, title, category, updated, content)

        batch.update(
            doc.reference,
            {"category": category, "xml_content": xml_content},
        )

        count_by_category[category] = count_by_category.get(category, 0) + 1

    batch.commit()

    print("Migration complete!")
    print("\nEntries migrated by category:")
    for category, count in sorted(count_by_category.items()):
        print(f"  {category}: {count}")


if __name__ == "__main__":
    main()
