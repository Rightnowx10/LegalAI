from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=400)
    return splitter.split_documents(docs)
