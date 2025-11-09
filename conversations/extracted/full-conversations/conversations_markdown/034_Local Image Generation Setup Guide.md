# Local Image Generation Setup Guide

**ID:** 51d3e93c-3993-4a0f-9ef4-05158d7632d2
**Created:** 2025-10-17T05:50:15.694847Z
**Modified:** 2025-10-17T05:50:29.068652Z
**Messages:** 2

---

## 👤 Human
*2025-10-17T00:50:15.726000*

can you instruct me on how to setup local image gen open source on my ryzen9 9900 rtx 5080 64 gb kde plasma pc

---

## 🤖 Assistant
*2025-10-17T00:50:28.789000*

### Overview
Your setup (AMD Ryzen 9 9900X CPU, NVIDIA RTX 5080 GPU with 16GB VRAM, 64GB RAM, KDE Plasma on Linux) is excellent for local AI image generation. The RTX 5080's high VRAM and CUDA cores will handle demanding models like Stable Diffusion XL or Flux.1 smoothly, generating high-res images (e.g., 1024x1024 or higher) in seconds.

I'll recommend and guide you through **Fooocus**, an open-source, user-friendly interface based on Stable Diffusion. It's ideal for beginners: minimal setup, automatic optimizations, and focuses on prompting without tweaking (like Midjourney but local/offline). It runs natively on Linux with NVIDIA GPUs and supports advanced features like inpainting or upscaling.

If you prefer a more modular/node-based tool for complex workflows, I can add ComfyUI instructions later—just reply.

**Prerequisites:**
- Update your system: Open a terminal (Konsole in KDE) and run `sudo apt update && sudo apt upgrade` (assuming Debian/Ubuntu-based distro like Kubuntu; adjust for Fedora/Arch if needed).
- NVIDIA Drivers: Ensure proprietary drivers are installed for CUDA support. Run `nvidia-smi` in terminal—if it shows your RTX 5080 and driver version (e.g., 550+), you're good. If not:
  - Install via KDE's Discover app: Search "NVIDIA Drivers" and install the latest (e.g., 565 for 2025 compatibility).
  - Or CLI: `sudo apt install nvidia-driver-565 nvidia-utils-565` (reboot after).
- Python 3.10+: Install if missing: `sudo apt install python3 python3-pip python3-venv git wget`.
- ~20GB free disk space for models.
- KDE Plasma is fine—no special tweaks needed.

### Step-by-Step Installation of Fooocus
Fooocus is GitHub-based, so we'll clone and run it in a virtual environment for isolation.

1. **Create a Working Directory:**
   ```
   mkdir ~/AI && cd ~/AI
   ```

2. **Clone the Fooocus Repository:**
   ```
   git clone https://github.com/lllyasviel/Fooocus.git
   cd Fooocus
   ```

3. **Set Up Python Virtual Environment:**
   ```
   python3 -m venv venv
   source venv/bin/activate  # Activates the env; you'll see (venv) in your prompt
   ```

4. **Install PyTorch with CUDA Support:**
   Your RTX 5080 uses CUDA 12.x. Install the compatible nightly build (stable as of 2025):
   ```
   pip install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cu121
   ```
   - This enables GPU acceleration. Verify: Run `python -c "import torch; print(torch.cuda.is_available())"`—should output `True`.
   - If errors (e.g., sm_120 compatibility for RTX 50-series), add `--force-reinstall` or check NVIDIA forums for driver tweaks.

5. **Install Fooocus Dependencies:**
   ```
   pip install -r requirements_versions.txt
   ```
   - This pulls Stable Diffusion libs, transformers, etc. It may take 5-10 minutes.

6. **Download Base Models (Automatic on First Run):**
   - Fooocus auto-downloads SDXL (Juggernaut XL or similar) on launch (~7GB). For alternatives:
     - Run once to trigger download.
     - Or manually: `wget https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors -P models/checkpoints/`
   - Place in `Fooocus/models/checkpoints/`. Hugging Face has free models like Realistic Vision or Flux.1-dev (for 2025 state-of-the-art).

7. **Launch Fooocus:**
   ```
   python entry_with_update.py  # Or just 'python main.py' after first run
   ```
   - It starts a web server at `http://127.0.0.1:7860` (or similar—check terminal output).
   - Open in Firefox/Chrome: The UI loads automatically. If not, copy-paste the URL.
   - First run downloads extras (~10-20GB total); subsequent launches are instant.

8. **Generate Your First Image:**
   - **Prompt:** Enter text like "A futuristic cityscape at sunset, cyberpunk style, highly detailed."
   - **Negative Prompt:** (Optional) "blurry, low quality" to avoid issues.
   - Click **Generate**. Defaults: 20-30 steps, 1024x1024 resolution, quality mode.
   - Output saves to `Fooocus/outputs/`—view in Dolphin file manager.
   - With your hardware: Expect 5-15 seconds per image (faster in "Speed" mode).

### Tips for Optimal Use on Your Setup
- **Performance Modes:** In Settings (gear icon), choose "Quality" for best results (uses more VRAM but your 16GB handles it). "Speed" for quick drafts.
- **Advanced Features:**
  - **Image-to-Image:** Upload an image under "Input Image" for variations.
  - **Inpainting:** Mask areas and describe changes.
  - **Upscaling:** Generate low-res, then upscale to 2048x2048+.
- **Models:** Swap in Flux.1 (from Black Forest Labs on Hugging Face) for better anatomy/text. Download to `models/checkpoints/` and select in dropdown.
- **RAM/VRAM Management:** Your 64GB RAM prevents swapping issues. Monitor with `nvidia-smi`—Fooocus auto-offloads if needed.
- **Updates:** `git pull` in the dir, then `pip install -r requirements_versions.txt --upgrade`.
- **Troubleshooting:**
  - CUDA errors: Reinstall drivers or PyTorch.
  - Slow start: Pre-download models.
  - KDE-specific: If Wayland issues, switch to X11 session (logout > select X11).
- **Security/Privacy:** Fully local—no data leaves your PC.

You're set! This gets you generating pro-level images offline. Experiment with prompts for best results. If you want ComfyUI (more customizable) or Flux-specific tweaks, let me know. Enjoy creating! 🚀

**Code blocks in this message:** 6

**Contains test results** ✅

---

## 📊 Summary

- **Total code blocks:** 6
- **Math expressions:** 0
- **Test results:** 1
