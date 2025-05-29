from transformers import AutoModel, AutoTokenizer

# This will download the model and tokenizer into ~/.cache/huggingface
print("📥 Downloading model...")
AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
print("✅ Model downloaded and cached.")
