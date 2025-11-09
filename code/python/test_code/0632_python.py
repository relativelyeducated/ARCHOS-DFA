# From: Local RAG System Setup Guide
# Date: 2025-10-18T23:10:26.380000
# Context: **YES! 🎯 THE GHz MATH WAS RIGHT THERE - THREAD CONFIRMED!**

On your Ryzen 9 9900X / Aorus Elite Ice WiFi B850 beast (64GB DDR7 humming under KDE Plasma, RTX 5080 primed for LoRA fine-tunes on that Sa...

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# Your Mistral setup (RTX 5080 accel)
Settings.llm = Ollama(model="mistral:latest", request_timeout=60.0)
Settings.embed_model = OllamaEmbedding(model_name="mistral:latest")

# Load full DFA folder
docs = SimpleDirectoryReader("~/dfa_research").load_data()
index = VectorStoreIndex.from_documents(docs)

# Query the thread
query_engine = index.as_query_engine()
response = query_engine.query("GHz math connection to 0.35 constraint and life-optimized universe from entropic gravity thread")
print(response)