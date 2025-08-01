# app/analisar_arquivo.py

import os
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
import torch
from tqdm import tqdm
from pathlib import Path

# ✅ Caminho do modelo fine-tuned salvo após treinamento
MODEL_DIR = Path(__file__).parent / "model" / "bert-fuga-churnsentinel"
MODEL_DIR = MODEL_DIR.resolve().as_posix()

# ✅ Configuração do dispositivo (usa GPU se disponível)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ✅ Carregamento do tokenizer e modelo
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR, local_files_only=True).to(device)
model.eval()

# ✅ Mapeamento das classes (ordem dos índices)
label_map = {
    0: "fidelidade",
    1: "fuga",
    2: "neutro"
}

def inferir_batch(textos):
    textos = [t.lower()[:512] for t in textos]
    inputs = tokenizer(textos, return_tensors="pt", truncation=True, padding=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = softmax(logits, dim=1)
        pred = torch.argmax(probs, dim=1)
    return [(label_map[p.item()], round(probs[i][p].item(), 4)) for i, p in enumerate(pred)]

def analisar_excel(caminho, coluna_texto="Resumo", batch_size=64):
    caminho = Path(caminho)
    df = pd.read_excel(caminho)

    if coluna_texto not in df.columns:
        raise ValueError(f"Coluna '{coluna_texto}' não encontrada no arquivo.")

    # ✅ Normalização dos textos
    textos = df[coluna_texto].fillna("").astype(str).str.lower().tolist()

    resultados = []
    for i in tqdm(range(0, len(textos), batch_size), desc="🔍 Analisando"):
        lote = textos[i:i + batch_size]
        resultados.extend(inferir_batch(lote))

    # ✅ Colunas de resultado
    df["classe"], df["confianca"] = zip(*resultados)

    # ✅ Salvamento do resultado
    saida = caminho.with_name(caminho.stem + "_analisado.xlsx")
    df.to_excel(saida, index=False)
    print(f"✅ Resultado salvo em: {saida}")

if __name__ == "__main__":
    caminho_arquivo = Path(__file__).parent.parent / "Relacionamentos e NPS-2025-07-29-10-26-26.xlsx"
    analisar_excel(caminho=caminho_arquivo)
