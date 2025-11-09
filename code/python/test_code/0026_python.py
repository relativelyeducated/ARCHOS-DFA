# From: ASUS ROG Strix G16CHR-XS776S Specs
# Date: 2025-10-04T17:32:02.845000
# Context: Yes, I can code! I can help with a wide range of programming tasks, from writing scripts for your AI-optimized PC build (e.g., Python for LLM fine-tuning with Unsloth/Axolotl) to automating setup task...

# Install dependencies (run once in terminal):
# pip install unsloth[colab-new] torch datasets peft trl bitsandbytes accelerate

from unsloth import FastLanguageModel
import torch
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments
from peft import LoraConfig
import os

# 1. Setup: Ensure GPU is detected
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}, GPU: {torch.cuda.get_device_name(0)}")  # Should show RTX 5080

# 2. Load quantized model (fits in 16GB VRAM)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/llama-3-8b-bnb-4bit",  # 8B model, 4-bit for low VRAM
    max_seq_length=2048,
    dtype=torch.bfloat16,  # RTX 5080 loves BF16 for speed
    load_in_4bit=True,
    device_map="auto"
)

# 3. Configure LoRA for efficient fine-tuning
lora_config = LoraConfig(
    r=16,  # Low-rank adapters (small footprint)
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = FastLanguageModel.get_peft_model(model, lora_config)

# 4. Load your dataset (replace with your JSONL path)
dataset = load_dataset("json", data_files="/path/to/your_dataset.jsonl", split="train")

# 5. Setup trainer
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",  # Adjust based on your JSONL (e.g., "instruction", "response")
    max_seq_length=2048,
    args=TrainingArguments(
        per_device_train_batch_size=2,  # Fits 16GB VRAM
        gradient_accumulation_steps=4,  # Effective batch size 8
        warmup_steps=10,
        max_steps=100,  # ~1hr on RTX 5080 for 10k samples
        learning_rate=2e-4,
        fp16=False,  # BF16 preferred
        bf16=True,
        logging_steps=10,
        output_dir="./fine_tuned_model",
        save_strategy="steps",
        save_steps=50,
        optim="adamw_8bit",
        seed=42
    )
)

# 6. Train and save
trainer.train()
model.save_pretrained("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")

# 7. Export to GGUF for inference (e.g., with Ollama)
# Run in terminal: `unsloth export ./fine_tuned_model --format gguf`
print("Fine-tuning complete! Model saved to ./fine_tuned_model")