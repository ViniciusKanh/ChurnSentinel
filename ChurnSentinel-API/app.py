import gradio as gr
import pandas as pd

def predict(text):
    # Aqui pode integrar o modelo real de churn!
    texto = text.lower()
    sinais_risco = [
        "cancelamento", "migrando", "deixando", "insatisfeito", "não quero mais", "vou sair"
    ]
    if any(sinal in texto for sinal in sinais_risco):
        return "🚨 Classe prevista: FUGA (alto risco de churn)"
    return "✅ Classe prevista: Não fuga (baixo risco de churn)"

def analisar_arquivo(file):
    try:
        df = pd.read_excel(file, engine="openpyxl")
    except Exception as e:
        return f"Erro ao ler o arquivo: {e}", None

    # Checa coluna Resumo
    if "Resumo" not in df.columns:
        return "❌ Coluna 'Resumo' não encontrada.", None

    # Converte para minúsculo, processa cada linha
    df["Resumo"] = df["Resumo"].fillna("").astype(str).str.lower()
    predicoes = df["Resumo"].apply(predict)
    df["Predição"] = predicoes
    # Exibe até 50 linhas no preview
    preview = df[["Resumo", "Predição"]].head(50).to_markdown(index=False)
    # Salva resultado
    saida = "resultado_analise.xlsx"
    df.to_excel(saida, index=False)
    return preview, saida

with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue", secondary_hue="gray")) as demo:
    gr.Markdown("""
    # 🏢 **ChurnSentinel API**
    Sentinela inteligente para detectar risco de fuga de cliente.<br>
    _Analise frases individualmente ou em lote via planilha Excel._
    """)
    with gr.Tab("🔎 Análise de Texto"):
        gr.Markdown("Cole um feedback de relacionamento ou NPS abaixo para analisar:")
        inp = gr.Textbox(label="Texto do relacionamento/NPS do cliente", lines=4, placeholder="Digite ou cole aqui...", elem_id="text-input")
        out = gr.Textbox(label="Predição", elem_id="pred-output")
        btn = gr.Button("Analisar", variant="primary")
        btn.click(predict, inp, out)
    with gr.Tab("📁 Análise em Arquivo"):
        gr.Markdown("Envie uma planilha `.xlsm` ou `.xlsx` contendo a coluna **Resumo**.")
        inp_file = gr.File(label="Arquivo Excel (.xlsm ou .xlsx)", file_types=[".xlsm", ".xlsx"])
        out_markdown = gr.Markdown()
        out_file = gr.File(label="Download da planilha analisada")
        btn2 = gr.Button("Analisar Arquivo", variant="primary")
        btn2.click(analisar_arquivo, inputs=inp_file, outputs=[out_markdown, out_file])

demo.launch()
