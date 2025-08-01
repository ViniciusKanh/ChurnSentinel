from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
import torch, sys

MODEL_DIR = "app/model/bert-fuga-churnsentinel"   # <-- novo caminho

device    = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tok       = AutoTokenizer.from_pretrained(MODEL_DIR)
model     = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR).to(device)
model.eval()

def classificar(texto:str):
    texto = texto.lower()
    inp = tok(texto[:512], return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        probs = softmax(model(**inp).logits, dim=1).cpu().numpy()[0]
    fuga_prob = probs[1]
    return (fuga_prob >= 0.5, float(fuga_prob))

if __name__ == "__main__":
    frase = " ".join(sys.argv[1:]) or "cliente migrando emails para o google workspace"
    fuga, prob = classificar(frase)
    print("⚠️  FUGA!" if fuga else "✅ Sem indício de fuga", "| score:", round(prob,4))
