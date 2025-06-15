# 🧠 Legal AI Assistant for Indian Law (RAG-based)

This project is a domain-specific **Retrieval-Augmented Generation (RAG)** assistant tailored for Indian legal professionals and law students. It automates tasks like judgment analysis, fact extraction, and case brief generation using modern LLM pipelines, vector databases, and dynamic prompt engineering.

---

## 🚀 Features

- 🔍 **Judgment Search & Scraping** from [Indian Kanoon](https://indiankanoon.org)
- 📄 **Raw Judgment Preprocessing** and chunking with metadata
- 📚 **Vector Store with Filtering** using `Chroma` and `InLegalBERT`
- 🧠 **LLM-based Retrieval & Answering** (via Gemini 1.5 / GPT-4)
- 🗂️ **Case Brief Generator** (Facts, Issues, Law, Reasoning, Conclusion)
- ✅ **Fact Classifier Module** *(WIP)*:
  - Tags factual statements
  - Scores importance
  - Extracts chronology and fact type
- 🧪 **Evaluation Setup**: Track speed, accuracy, and quality across real judgments

---

## 🏗️ Tech Stack

| Tool                | Purpose                           |
|---------------------|-----------------------------------|
| **LangChain**       | RAG pipeline, routing, chains     |
| **Google Gemini 1.5** | Main LLM for reasoning           |
| **HuggingFace Embeddings** | Legal embedding model (`InLegalBERT`) |
| **Chroma**          | Vector store with doc filtering   |
| **BeautifulSoup**   | Judgment scraping                 |
| **Python (modular)**| Clean architecture & CLI support  |

---

## 📁 Directory Structure

legal-rag-assistant/
│
├── main.py # Main controller script
├── .env # API keys and configuration
│
├── scraping/
│ ├── url_fetcher.py # Searches and fetches Indian Kanoon links
│ ├── raw_judgment_scraper.py # Scrapes judgment body text
│
├── vectorstore/
│ ├── embedder.py # Sets up embedding model
│ └── store_utils.py # Chunking and vector storage
│
├── rag_pipeline/
│ ├── rag_chain.py # Full RAG chain logic
│ ├── prompt_router.py # Dynamic prompt routing
│ └── query_rewriter.py # Query rewriting for clarity
│
├── fact_classifier/ # (Planned)
│ └── fact_classifier.py # Fact tagging, scoring, chronology extraction
│
├── scraped_raw_judgments/ # Local scraped text files
└── README.md



## 🔧 How to Run

1. **Install dependencies:**

```bash
pip install -r requirements.txt


Set your environment variables in .env:

GOOGLE_API_KEY=your_gemini_key

