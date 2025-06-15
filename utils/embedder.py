from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
import tempfile
import shutil



def get_vectorstore(splits):
    embedding_model_name = "law-ai/InLegalBERT"
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    temp_dir = tempfile.mkdtemp()
    shutil.rmtree(temp_dir, ignore_errors=True)  # ensures it's clean
    _last_temp_dir = temp_dir
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=temp_dir
    )
    return vectorstore, vectorstore.as_retriever(search_kwargs={"k": 5})
