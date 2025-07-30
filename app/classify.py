# app/classify.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
import torch
import os

# Atualize este caminho para o modelo fine-tuned treinado localmente
MODEL_DIR = os.path.join(os.path.dirname(__file__), "model", "bert-large-portuguese-cased")

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()

label_map = {
    0: "fidelidade",
    1: "fuga",
    2: "neutro"
}

def analisar_texto(texto):
    texto = texto.lower()  # Garante minúsculas na inferência
    inputs = tokenizer(texto[:512], return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = softmax(logits, dim=1)
        pred = torch.argmax(probs, dim=1).item()
    return label_map[pred], float(probs[0][pred])