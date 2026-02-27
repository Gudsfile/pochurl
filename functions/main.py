import datetime
import re
from base64 import b64encode

from firebase_admin import firestore, initialize_app
from firebase_functions import https_fn
from firebase_functions.params import SecretParam
from lib.detect_category import detect_category
from lib.entry_to_xml import entry_to_xml
from lib.extract_content import extract_content

initialize_app()

URL_REGEX = re.compile(
    r"^https?://"
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
    r"localhost|"
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    r"(?::\d+)?"
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)

CATEGORIES = {"github", "docs", "article", "app"}

FEED_HEADER = f"""
<?xml version="1.1" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <id>https://github.com/Gudsfile/Pochurl</id>
    <title>Pochurl - what do I have to read?</title>
    <updated>{datetime.datetime.now().isoformat()}</updated>
    <generator>https://github.com/Gudsfile/Pochurl</generator>
    <icon>https://en.wikipedia.org/static/favicon/wikipedia.ico</icon>
"""

FEED_FOOTER = """
</feed>
"""

REGION = "europe-west1"
MAX_INSTANCES = 1
API_KEY = SecretParam("POCHURL_API_KEY")


@https_fn.on_request(region=REGION, max_instances=MAX_INSTANCES, secrets=[API_KEY])
def add_entry(req: https_fn.Request) -> https_fn.Response:
    """Take the body passed to this HTTP endpoint and insert it into
    a new document in the entries collection. Updates 'updated' field if entry exists."""
    if req.headers.get("X-API-Key") != API_KEY.value:
        return https_fn.Response("Unauthorized", status=401)

    link = req.json.get("link")

    if link is None:
        return https_fn.Response("No link parameter provided", status=400)

    if not URL_REGEX.match(link):
        return https_fn.Response("Invalid URL provided", status=400)

    client = firestore.client()
    db = client.collection("entries")

    entry_id = b64encode(bytes(link, encoding="utf-8")).decode("utf-8")
    doc_ref = db.document(entry_id)

    category = req.json.get("category")
    if category not in CATEGORIES:
        category = detect_category(link)

    updated = datetime.datetime.now().isoformat()
    title, content = extract_content(link)
    entry = {
        "link": link,
        "title": title,
        "category": category,
        "updated": updated,
        "xml_content": entry_to_xml(entry_id, link, title, category, updated, content),
    }

    existing_doc = doc_ref.get()
    if existing_doc.exists:
        doc_ref.update(entry)
        return https_fn.Response(f"Entry with ID {entry_id} updated.")

    doc_ref.set(entry)
    return https_fn.Response(f"Entry with ID {entry_id} added.")


@https_fn.on_request(region=REGION, max_instances=MAX_INSTANCES)
def get_entries(req: https_fn.Request) -> https_fn.Response:
    """Return the feed XML from the entries collection, sorted by updated date."""
    client = firestore.client()
    db = client.collection("entries")

    entries = db.order_by("updated", direction=firestore.Query.DESCENDING).stream()
    feed_content = "\n".join([entry.get("xml_content") for entry in entries])
    feed = f"{FEED_HEADER}\n{feed_content}\n{FEED_FOOTER}"

    return https_fn.Response(feed, mimetype="text/xml", headers={"Cache-Control": "public, max-age=3600"})


@https_fn.on_request(region=REGION, max_instances=MAX_INSTANCES)
def get_github(req: https_fn.Request) -> https_fn.Response:
    """Return the GitHub entries feed."""
    return get_filtered_entries("github")


@https_fn.on_request(region=REGION, max_instances=MAX_INSTANCES)
def get_articles(req: https_fn.Request) -> https_fn.Response:
    """Return the article/blog entries feed."""
    return get_filtered_entries("article")


@https_fn.on_request(region=REGION, max_instances=MAX_INSTANCES)
def get_docs(req: https_fn.Request) -> https_fn.Response:
    """Return the documentation entries feed."""
    return get_filtered_entries("docs")


@https_fn.on_request(region=REGION, max_instances=MAX_INSTANCES)
def get_apps(req: https_fn.Request) -> https_fn.Response:
    """Return the app/site entries feed."""
    return get_filtered_entries("app")


def get_filtered_entries(category: str) -> https_fn.Response:
    """Return filtered entries by category."""
    client = firestore.client()
    db = client.collection("entries")

    entries = db.where("category", "==", category).order_by("updated", direction=firestore.Query.DESCENDING).stream()
    feed_content = "\n".join([entry.get("xml_content") for entry in entries])
    feed = f"{FEED_HEADER}\n{feed_content}\n{FEED_FOOTER}"

    return https_fn.Response(feed, mimetype="text/xml", headers={"Cache-Control": "public, max-age=3600"})
