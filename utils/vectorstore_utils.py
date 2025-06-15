from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import tempfile
import os # Import os for potential cleanup if you switch to persistent later

# You might want to make this a global variable or handle it in main.py's scope
# if you want to explicitly clean up temp dirs after the script finishes.
# For this immediate fix, it's not strictly necessary as mkdtemp creates a new one each time.
_last_temp_dir = None

def split_documents(docs):
    """
    Splits a list of LangChain Document objects into smaller chunks.
    Ensures each chunk carries the metadata from its original document.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=400)
    # The splitter naturally carries metadata from the parent document to its splits
    return splitter.split_documents(docs)

def create_vectorstore(splits: list, embedding, target_doc_id: str = None):
    """
    Creates a Chroma vector store from document splits and returns a retriever.
    
    Args:
        splits (list): A list of LangChain Document objects (chunks).
                       Each Document MUST have a 'doc_id' in its metadata.
        embedding: The embedding model to use (e.g., HuggingFaceEmbeddings).
        target_doc_id (str, optional): The ID of the specific document
                                       to filter retrieval results by.
                                       If None, no metadata filter is applied.
    
    Returns:
        langchain.vectorstores.base.VectorStoreRetriever: A retriever instance
                                                            configured with k and optional filter.
    """
    global _last_temp_dir

    temp_dir = tempfile.mkdtemp()
    _last_temp_dir = temp_dir # Store for potential manual cleanup at end of script

    print(f"Creating new temporary Chroma vector store in: {temp_dir}")

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=temp_dir
    )

    # Configure search arguments for the retriever
    search_kwargs = {"k": 5} # Increased k to 5 (or higher, e.g., 8-10 for briefs)

    # Apply metadata filter if a target_doc_id is provided
    if target_doc_id:
        print(f"Configuring retriever to filter by doc_id: {target_doc_id}")
        search_kwargs["filter"] = {"doc_id": target_doc_id}

    return vectorstore.as_retriever(search_kwargs=search_kwargs)