import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from langchain_core.documents import Document
from typing import List
import re

def load_indiankanoon_page(url: str) -> List[Document]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error loading page {url}: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    # Extract title
    title_tag = soup.find(["h1", "h2"], class_="doc_title")
    full_title_string = title_tag.get_text(strip=True) if title_tag else "No title"
    metadata = {"title": full_title_string, "source": url}

    # Extract bench
    bench_tag = soup.find("h3", class_="doc_bench")
    if bench_tag:
        metadata["bench"] = bench_tag.get_text(strip=True)

    # Extract date from title
    date_match = re.search(r'on (\d{1,2} [A-Za-z]+, \d{4})$', full_title_string)
    if date_match:
        metadata["date"] = date_match.group(1)
        metadata["title"] = full_title_string.replace(f" on {date_match.group(1)}", "").strip()

    # Try to find main content in #doccontent first
    doc_content_div = soup.find("div", id="doccontent")
    if doc_content_div:
        paragraphs = doc_content_div.find_all("p")
        full_text = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
    else:
        print(f"doccontent not found for {url}, trying fallback extraction")
        # Fallback: get all paragraphs in the page
        paragraphs = soup.find_all("p")
        full_text = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

    if len(full_text.strip()) < 10:
        print(f"No significant content could be loaded from {url}. This judgment might have an unusual structure or no text content.")
        return []

    return [Document(page_content=full_text, metadata=metadata)]
