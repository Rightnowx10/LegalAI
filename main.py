import os
from dotenv import load_dotenv
load_dotenv()

from scraping.kanoon_scraper import load_indiankanoon_page
from scraping.url_fetcher import search_case_url_refined
from utils.splitter import split_documents
from utils.embedder import get_vectorstore
from utils.rag_chain import get_rag_chain
from query_rewriter import rewrite_and_decompose
from query_router import route_query_type
from prompts import prompts  # ✅ Correct import
from scraping.raw_judgement_scraper import scrape_and_save_judgment_to_text_file_and_document

query = input("Enter legal query to search: ")

url = search_case_url_refined(query, exact_phrase=True, doc_type='judgments')

if not url:
    print("No results found for the given query and filters. Please try another query.")
    exit()

print(f"URL fetched: {url}")

doc = scrape_and_save_judgment_to_text_file_and_document(url)
docs = [doc] if doc else []

if not docs:
    print(f"No significant content could be loaded from {url}.")
    exit()

print("Loaded document:", docs[0].metadata.get("title"))

splits = split_documents(docs)
vectorstore, retriever = get_vectorstore(splits)

while True:
    user_q = input("Ask a question about the judgment (type 'exit' to quit): ")
    if user_q.lower() in ["exit", "quit"]:
        break

    rewritten_queries = rewrite_and_decompose(user_q)
    final_answer = ""
    
    for query in rewritten_queries:
        prompt_type = route_query_type(query)
        prompt_template = prompts.get(prompt_type, prompts["general"])  # fallback to general
        rag_chain = get_rag_chain(retriever, prompt_template)
        result = rag_chain.invoke(query)
        final_answer += f"\n\nQuery: {query}\nAnswer: {result.strip()}"

    print("\nFinal Answer:\n", final_answer.strip())
