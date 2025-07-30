from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

MODEL_NAME = "neuralmind/bert-large-portuguese-cased"
SAVE_PATH = "app/model/bert-large-portuguese-cased"
os.makedirs(SAVE_PATH, exist_ok=True)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=3)

tokenizer.save_pretrained(SAVE_PATH)
model.save_pretrained(SAVE_PATH)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
model.eval()
