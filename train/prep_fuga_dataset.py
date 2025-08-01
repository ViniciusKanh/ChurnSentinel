"""
Gera um CSV binário (fuga / sem_fuga) a partir do Cancelamento Total.xlsx
Uso: python -m train.prep_fuga_dataset
"""
import re, pandas as pd
from pathlib import Path

RAW_XLSX   = Path("data/Relacionamento e NPS.xlsx")     # coloque aqui ou ajuste path
OUT_CSV    = Path("data/fuga_dataset.csv")            # saída final

# ——————————————————————————————————————————————————————
REGEX_FUGA = re.compile(
    r"\b("
    r"migrar|migração|migrou|mudaram|trocar|substituir|"
    r"testando|avaliando|comparando|concorrente|"
    r"google|workspace|gmail|microsoft|office|365|outlook|exchange|"
    r"outro fornecedor|outra plataforma|reduzir custo|cancelar"
    r")\b",
    flags=re.I
)

def marca_fuga(texto: str) -> int:
    return int(bool(REGEX_FUGA.search(texto)))

def main():
    df = pd.read_excel(RAW_XLSX)
    if "Resumo" not in df.columns:
        raise ValueError("Coluna 'Resumo' não encontrada!")

    df["texto"]  = df["Resumo"].fillna("").astype(str).str.lower()
    df["label"]  = df["texto"].apply(marca_fuga)          # 1 = fuga
    df[["texto", "label"]].to_csv(OUT_CSV, index=False, sep=";")
    print(f"✅ Dataset salvo em {OUT_CSV.resolve()} — {df.label.value_counts().to_dict()}")

if __name__ == "__main__":
    main()
