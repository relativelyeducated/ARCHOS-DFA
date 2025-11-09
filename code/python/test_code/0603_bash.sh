# From: Local RAG System Setup Guide
# Date: 2025-10-17T18:28:21.796000
# Context: **YES - This is exactly what you need!** A local RAG system where ALL your research lives and can be queried persistently.

## **🎯 RECOMMENDED SETUP: Local RAG System**

### **Best Solution: Ollama + ...

docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main