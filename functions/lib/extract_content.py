import requests
from readability import Document


def extract_content(link: str):
    headers = {
        "User-Agent": "Pochurl/0.1.0",
    }

    try:
        response = requests.get(link, timeout=20, headers=headers)
        doc = Document(response.content.decode("utf-8"))
        return doc.title(), doc.summary()

    except Exception as e:
        return "Error", f"{e}"


if __name__ == "__main__":
    import sys

    print(extract_content(sys.argv[1]))
