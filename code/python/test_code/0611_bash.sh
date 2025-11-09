# From: Local RAG System Setup Guide
# Date: 2025-10-17T18:28:32.153000
# Context: **ABSOLUTELY! 🚀 Let's build your Local RAG system RIGHT NOW!** 

This is going to be **game-changing** for your cosmic fine-tuning research. I'll guide you **step-by-step** through the **QUICKEST 5-mi...

# ONE COMMAND (installs everything)
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data --name open-webui --restart always \
  ghcr.io/open-webui/open-webui:main