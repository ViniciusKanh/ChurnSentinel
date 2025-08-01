import gradio as gr

def predict(text):
    # Aqui você pode integrar seu modelo real de churn!
    # Exemplo básico de regra para simulação
    texto = text.lower()
    sinais_risco = ["cancelamento", "migrando", "deixando", "insatisfeito", "não quero mais", "vou sair"]
    if any(sinal in texto for sinal in sinais_risco):
        return "🚨 Classe prevista: FUGA (alto risco de churn)"
    return "✅ Classe prevista: Não fuga (baixo risco de churn)"

demo = gr.Interface(
    fn=predict,
    inputs=gr.Textbox(lines=4, label="Texto do relacionamento/NPS do cliente"),
    outputs=gr.Textbox(label="Predição"),
    title="ChurnSentinel API 🏢",
    description="Sentinela inteligente para detectar risco de fuga de cliente. Cole aqui um texto de relacionamento ou NPS para analisar o risco."
)

if __name__ == "__main__":
    demo.launch()