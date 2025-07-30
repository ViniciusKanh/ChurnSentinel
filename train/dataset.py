import pandas as pd
from sklearn.model_selection import train_test_split

def carregar_dados(caminho_csv, label_col="label", text_col="texto"):
    df = pd.read_csv(caminho_csv, sep=";")
    df = df[[text_col, label_col]].dropna()
    df[text_col] = df[text_col].astype(str).str.lower()

    label_map = {label: idx for idx, label in enumerate(sorted(df[label_col].unique()))}
    df["label_id"] = df[label_col].map(label_map)

    return train_test_split(
        df[text_col].tolist(),
        df["label_id"].tolist(),
        test_size=0.2,
        random_state=42
    ), label_map
