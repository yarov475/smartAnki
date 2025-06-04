import requests
from bs4 import BeautifulSoup
import readability
from readability.readability import Document

def scrape_webpage(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL: {url} ({response.status_code})")

    # Extract main content using readability
    doc = Document(response.text)
    html = doc.summary()
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n", strip=True)
