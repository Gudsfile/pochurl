import requests
from readability import Document


def extract_content(link: str):
    headers = {
        "User-Agent": "Pochurl/0.1.0",
    }

    try:
        response = requests.get(link, timeout=20, headers=headers)
        doc = Document(response.content)
        title = doc.title()
        content = doc.summary()

        if not title or not content:
            return title, "Empty title or content from readability"

        return title, content

    except Exception as e:
        return "Error", f"{e}"
