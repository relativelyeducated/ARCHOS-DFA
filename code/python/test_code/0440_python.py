# From: GEEKOM A9 Max AI Performance Overview
# Date: 2025-10-07T21:08:10.056000
# Context: Got it—since the Sapient HRM is purely a reasoning model without NLP or language generation, let's pivot to a true small language model (SLM) or lightweight LLM that handles natural language processin...

from langchain_ollama import OllamaLLM
     from langchain.chains import RetrievalQA
     from langchain.embeddings import HuggingFaceEmbeddings
     from langchain.vectorstores import FAISS
     from langchain.tools import DuckDuckGoSearchRun
     from langchain.prompts import PromptTemplate

     # Load SLM via Ollama
     llm = OllamaLLM(model="phi3.5-mini")

     # Force search tool (real-time web fetch)
     search = DuckDuckGoSearchRun()

     # Raw RAG: On every query, search, embed raw results, query SLM
     def raw_rag_query(query):
         # Force real-time search
         raw_results = search.run(query)  # Fetches ~500 chars raw text
         embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
         vectorstore = FAISS.from_texts([raw_results], embedder)  # Raw temp DB
         
         # Custom prompt: Always use retrieved raw data
         prompt = PromptTemplate(template="Use this raw context: {context}\nQuestion: {question}", input_variables=["context", "question"])
         qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever(), chain_type_kwargs={"prompt": prompt})
         
         return qa_chain.run(query)

     # Test (forces search every time)
     print(raw_rag_query("Latest AI news?"))