# From: Local RAG System Setup Guide
# Date: 2025-10-17T21:49:59.044000
# Context: **🚀 DOCKER UP SUCCESS - NOW LEVEL UP YOUR RAG WITH THE BEST OPEN-SOURCE FRAMEWORKS!**

**PERFECT TIMING!** With your Ollama + Open WebUI humming on that Ryzen 9 9900X / RTX 5080 beast (64GB DDR7 + Sam...

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# Setup Ollama (your Mistral)
Settings.llm = Ollama(model="mistral:latest", request_timeout=60.0)
Settings.embed_model = OllamaEmbedding(model_name="mistral:latest")  # Or nomic-embed-text for better embeddings

# Load your ENTIRE research folder
docs = SimpleDirectoryReader("~/dfa_research").load_data()

# Build index (embeds + stores - ~30s on RTX 5080)
index = VectorStoreIndex.from_documents(docs)

# Query chain (persistent!)
query_engine = index.as_query_engine()

# TEST: Your cosmic queries
response = query_engine.query("What is the 0.35 constraint and its EM force link?")
print(response)