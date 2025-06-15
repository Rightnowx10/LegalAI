import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urlparse
from langchain.schema import Document

def scrape_and_save_judgment_to_text_file_and_document(url: str, output_dir: str = "scraped_judgments") -> Document | None:
    """
    Scrapes a legal judgment from Indian Kanoon, saves it to a text file,
    and also returns it as a LangChain Document object with metadata.

    Args:
        url (str): Indian Kanoon judgment URL.
        output_dir (str): Directory for saving .txt files.

    Returns:
        Document | None: LangChain Document object or None if failed.
    """
    os.makedirs(output_dir, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error loading page {url}: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # --- Metadata extraction ---
    doc_id = re.search(r'/doc/(\d+)/', url)
    doc_id = doc_id.group(1) if doc_id else "unknown_id"

    title = soup.find("h2", class_="doc_title")
    full_title_string = title.get_text(strip=True) if title else "No Title Found"

    court = soup.find("h2", class_="docsource_main")
    court = court.get_text(strip=True) if court else "No Court Found"

    bench = soup.find("h3", class_="doc_bench")
    bench = bench.get_text(strip=True) if bench else "No Bench Found"

    citations = soup.find("h3", class_="doc_citations")
    citations = citations.get_text(strip=True) if citations else "No Citations Found"

    date_match = re.search(r'on (\d{1,2} [A-Za-z]+, \d{4})$', full_title_string)
    date_of_judgment = date_match.group(1) if date_match else "No Date Found"

    parties_match = re.search(r'(.+)\s+vs\s+(.+?)(?:\s+on\s+\d{1,2} [A-Za-z]+, \d{4})?$', full_title_string)
    petitioner = parties_match.group(1).strip() if parties_match else "N/A"
    respondent = parties_match.group(2).strip() if parties_match else "N/A"

    # --- Judgment text extraction ---
    full_text_parts = []
    doc_content_div = soup.find("div", id="doccontent")

    if doc_content_div:
        for child in doc_content_div.children:
            if child.name in ["p", "h1", "h2", "h3", "h4", "h5", "li"]:
                text = child.get_text(strip=True)
                if text:
                    full_text_parts.append(text)
            elif child.name == "blockquote":
                text = child.get_text(strip=True)
                if text:
                    full_text_parts.append(f"> {text}")
            elif child.name == "div":
                class_list = child.get("class", [])
                if "section_title" in class_list:
                    text = child.get_text(strip=True)
                    if text:
                        full_text_parts.append(f"\n## {text}\n")
                elif "doc_inner_content" in class_list:
                    for el in child.find_all(["p", "blockquote", "li", "h1", "h2", "h3", "h4", "h5"]):
                        text = el.get_text(strip=True)
                        if text:
                            full_text_parts.append(f"> {text}" if el.name == "blockquote" else text)
                elif child.name == "p" and child.get("data-structure"):
                    section_type = child["data-structure"]
                    text = child.get_text(strip=True)
                    if text:
                        full_text_parts.append(f"\n--- {section_type} ---\n{text}")
    else:
        print(f"Warning: #doccontent not found for {url}, falling back to all <p> in body.")
        for p in soup.find("body").find_all("p"):
            text = p.get_text(strip=True)
            if text:
                full_text_parts.append(text)

    full_text_content = "\n\n".join(t for t in full_text_parts if t.strip())

    # --- Save to file ---
    safe_title = re.sub(r'[^\w\s-]', '', full_title_string).strip()
    safe_title = re.sub(r'\s+', '_', safe_title)[:100]
    filename = f"{safe_title}_{doc_id}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"--- Judgment Metadata ---\n")
        f.write(f"Title: {full_title_string}\n")
        f.write(f"Document ID: {doc_id}\n")
        f.write(f"Source URL: {url}\n")
        f.write(f"Court: {court}\n")
        f.write(f"Bench: {bench}\n")
        f.write(f"Date of Judgment: {date_of_judgment}\n")
        f.write(f"Petitioner(s): {petitioner}\n")
        f.write(f"Respondent(s): {respondent}\n")
        f.write(f"Citations: {citations}\n")
        f.write(f"\n--- Judgment Content ---\n\n")
        f.write(full_text_content)

    if not full_text_content.strip():
        print(f"Warning: No significant text extracted from {url}. File created but may be empty.")
        return None

    print(f"✅ Saved to: {filepath}")

    # --- Return Document object for RAG ---
    return Document(
        page_content=full_text_content,
        metadata={
            "title": full_title_string,
            "doc_id": doc_id,
            "source": url,
            "court": court,
            "bench": bench,
            "citations": citations,
            "date_of_judgment": date_of_judgment,
            "petitioner": petitioner,
            "respondent": respondent
        }
    
