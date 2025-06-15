import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from langchain_core.documents import Document
from typing import List
import re

def search_case_url_refined(query, exact_phrase=False, doc_type=None, title_only=False):
    """
    Searches Indian Kanoon for a case URL with refined filtering options.
    Note: The 'doc_type' parameter in this function is still available if you want
    to filter search results by type, but the load_indiankanoon_page function
    will no longer use it for content extraction.

    Args:
        query (str): The search query.
        exact_phrase (bool): If True, enclose the query in double quotes for an exact phrase search.
        doc_type (str, optional): Restrict search to a specific document type.
                                  Examples: 'judgments', 'acts', 'bills', 'rules'.
        title_only (bool): If True, search only in the title of documents using 'title:' operator.

    Returns:
        str: The URL of the most relevant case, or None if not found.
    """
    search_terms = query.replace(' ', '+')

    if exact_phrase:
        search_terms = f'"{search_terms}"'
    if title_only:
        search_terms = f'title:{search_terms}'
    if doc_type:
        search_terms = f'{search_terms}+doctypes:{doc_type}' # This filter remains for search results

    search_url = f"https://indiankanoon.org/search/?formInput={search_terms}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36)"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error making search request: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    link_tag = soup.select_one("div.result a[href^='/doc/'], h3.act_title a[href^='/doc/'], div.judgment_title a[href^='/doc/']")

    if link_tag:
        return urljoin("https://indiankanoon.org", link_tag["href"])

    link_tag_fallback = soup.select_one("a[href^='/doc/']")
    if link_tag_fallback:
        return urljoin("https://indiankanoon.org", link_tag_fallback["href"])

    return None