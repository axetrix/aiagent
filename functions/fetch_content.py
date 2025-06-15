import requests

from google.genai import types
from bs4 import BeautifulSoup


def fetch_content(working_directory: str, url: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        print("callicng with: ", url)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        return soup.get_text()

    except requests.exceptions.RequestException as e:
        return f"Error: Failing during fetching {url}: {e}"


schema_fetch_content = types.FunctionDeclaration(
    name="fetch_content",
    description="Get content by provided url it usually in html format. This is the ability to get content of site by URL",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "url": types.Schema(
                type=types.Type.STRING,
                description="URL that representse the resource that we want to get content",
            ),
        },
    ),
)
