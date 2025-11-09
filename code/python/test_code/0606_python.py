# From: Local RAG System Setup Guide
# Date: 2025-10-17T18:28:21.796000
# Context: **YES - This is exactly what you need!** A local RAG system where ALL your research lives and can be queried persistently.

## **🎯 RECOMMENDED SETUP: Local RAG System**

### **Best Solution: Ollama + ...

# install_rag.py
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import Ollama

# 1. Load all your documents
loader = DirectoryLoader('/path/to/your/research', glob="**/*.md")
docs = loader.load()

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(docs)

# 3. Create embeddings and vector store
embeddings = OllamaEmbeddings(model="llama3.1:8b")
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./research_db"
)

# 4. Create RAG chain
llm = Ollama(model="llama3.1:70b")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# 5. Query
result = qa_chain("What is the 0.35 constraint parameter?")
print(result['result'])