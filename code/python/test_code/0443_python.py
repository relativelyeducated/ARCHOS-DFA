# From: GEEKOM A9 Max AI Performance Overview
# Date: 2025-10-07T21:09:27.068000
# Context: Sounds like a solid pivot—CUDA's ecosystem is unbeatable for seamless fine-tuning and LoRA workflows with tools like Hugging Face, Automatic1111, or PEFT, especially since you've got the AMD setup in ...

from peft import LoraConfig, get_peft_model
   from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
   from datasets import load_dataset

   model_name = "microsoft/Phi-3.5-mini-instruct"
   tokenizer = AutoTokenizer.from_pretrained(model_name)
   model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="cuda")

   # LoRA config (low-rank for efficiency)
   lora_config = LoraConfig(r=16, lora_alpha=32, target_modules=["qkv_proj"], lora_dropout=0.05)
   model = get_peft_model(model, lora_config)

   # Load raw dataset (e.g., your NLP texts/JSON)
   dataset = load_dataset("json", data_files="your_raw_data.json", split="train")

   # Fine-tune
   training_args = TrainingArguments(output_dir="./lora_phi", num_train_epochs=3, per_device_train_batch_size=4, gradient_accumulation_steps=4, fp16=True)
   trainer = Trainer(model=model, args=training_args, train_dataset=dataset, tokenizer=tokenizer)
   trainer.train()  # CUDA handles the heavy lift—saves adapter weights

   # Merge & test
   model.save_pretrained("fine_tuned_phi_lora")