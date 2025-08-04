# 🏢 ChurnSentinel API

## 🚨 O que é?

**ChurnSentinel API** é uma solução baseada em Inteligência Artificial criada para **detectar automaticamente o risco de fuga (churn) de clientes** a partir de textos de relacionamento e respostas de NPS. É seu sentinela digital que monitora sinais de evasão para equipes de Customer Success agirem antes da perda acontecer!

---

## 💡 Como funciona?

O modelo faz a **análise de sentimentos e padrões** em frases e comentários vindos de pesquisas NPS ou interações de relacionamento.  
Ele identifica termos e contextos que historicamente indicam alta chance de cancelamento ou migração do cliente para outra plataforma, gerando uma predição automática ("FUGA" ou "Não Fuga").

- **Entrada:** Texto individual (ex: comentário de cliente) ou planilha Excel (.xlsm, .xlsx) com a coluna `Resumo`
- **Saída:** Predição de risco (Alto risco de churn ou Não fuga)

---

## 🔬 Como é treinado o modelo?

O ChurnSentinel utiliza o BERT em português (modelo base `neuralmind/bert-large-portuguese-cased`), **fine-tuned** com exemplos reais de clientes que saíram ou permaneceram.

1. **Pré-processamento:**  
   - Geração de dataset binário (`fuga_dataset.csv`) a partir de frases rotuladas com regex e revisão humana.
   - Exemplo: Textos que mencionam migração/teste/concorrentes (mas não citam "Zimbra") são rotulados como "fuga".

2. **Treinamento:**  
   - Treinamento supervisionado usando a biblioteca `transformers` da Hugging Face, com separação treino/teste.
   - Métricas avaliadas: acurácia, recall, f1-score.

3. **Inferência:**  
   - O modelo recebe qualquer texto (ou planilha com coluna `Resumo`), normaliza em minúsculo e retorna a predição + score de confiança.

---

## 🚀 Como usar (localmente)

1. Clone o repositório:
    ```bash
    git clone https://github.com/ViniciusKanh/ChurnSentinel.git
    cd ChurnSentinel/ChurnSentinel-API
    ```

2. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

3. Rode localmente:
    ```bash
    python app.py
    ```

4. Use a interface web:
    - Analise textos individuais ou envie arquivos Excel com coluna **Resumo**.

---

## 🌐 Demonstração Online

Acesse o Space do Hugging Face para testar online (sem instalar nada):

👉 https://huggingface.co/spaces/ViniciusKanh/ChurnSentinel-API

---

## 🤝 Como contribuir/ajudar no modelo?

- **Envie exemplos reais** (anonimizados) de comentários que representam fuga ou não fuga.
- **Sugira novas regras, regex ou termos** que indiquem risco de churn.
- **Teste o app e reporte falsos positivos/negativos** via Issues ou PR.
- **Compartilhe feedback** sobre como adaptar para outros segmentos!

Pull requests, sugestões e correções são muito bem-vindos!

---

## 🛠️ Estrutura do repositório

```
ChurnSentinel/
 └── ChurnSentinel-API/
      ├── app.py               # Interface Gradio
      ├── requirements.txt     # Dependências
      ├── README.md            # Este arquivo
      ├── data/                # (opcional) Datasets de treino
      └── app/model/           # Modelo treinado (.bin, config)
```

---

## 👨‍💻 Autor

Desenvolvido por [ViniciusKanh](https://huggingface.co/ViniciusKanh)  
Mais: [LinkedIn](https://www.linkedin.com/in/viniciuskanh/) | [GitHub](https://github.com/ViniciusKanh)

---

