#main.py
from app.classify import analisar_texto

if __name__ == "__main__":
    while True:
        entrada = input("\nDigite um texto para analisar (ou 'sair'):\n> ")
        if entrada.lower() == "sair":
            break
        label, prob = analisar_texto(entrada)
        print(f"📌 Classe: {label} — Confiança: {round(prob, 4)}")