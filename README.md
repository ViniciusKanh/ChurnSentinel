# 🏢 ChurnSentinel API
## 🚨 O que é?

**ChurnSentinel API** é uma plataforma inteligente desenvolvida para **identificação preditiva do risco de churn (fuga) de clientes** em ambientes SaaS e serviços recorrentes.  
O sistema emprega modelos avançados de **Processamento de Linguagem Natural (NLP)**, usando aprendizado de máquina supervisionado (fine-tuning de BERT em português), para **interpretar sinais, sentimentos e intenções presentes em textos de relacionamento, respostas de NPS, tickets e históricos de contato**.

Agindo como um verdadeiro **sentinela digital**, a solução monitora, avalia e alerta as equipes de Customer Success sobre potenciais riscos de evasão, permitindo que estratégias proativas sejam aplicadas antes do cliente abandonar a base.

---

## 💡 Como funciona?

O pipeline do **ChurnSentinel** opera em três etapas principais:

1. **Coleta e Normalização**  
   Textos de interações com clientes (NPS, chamados, feedbacks, e-mails, registros de CRM) são reunidos e **normalizados** (minúsculas, limpeza de caracteres, remoção de ruídos).

2. **Detecção de Padrões e Sinais de Risco**  
   O modelo examina o texto em busca de padrões linguísticos, palavras-chave e contextos que indicam **potencial intenção de migração, insatisfação, testes de concorrentes, pedidos de cancelamento** ou outras situações correlatas.  
   Ele diferencia menções contextuais (“estamos testando o Gmail”) de casos neutros (“cliente utiliza Office, mas está satisfeito com Zimbra”).

3. **Classificação e Predição**  
   - **Entrada:**  
     - Texto individual (ex: comentário de cliente, chamado, resposta NPS)  
     - Ou planilha Excel (.xlsm, .xlsx) com a coluna `Resumo` contendo os textos a analisar
   - **Processamento:**  
     - O texto é transformado em embeddings pelo modelo BERT, que avalia a probabilidade de pertencer às classes **fuga** ou **não fuga**
   - **Saída:**  
     - Predição binária:  
       - `"FUGA"` (alto risco de churn, recomenda ação imediata)
       - `"Não Fuga"` (baixo risco de churn, monitoramento rotineiro)
     - Score de confiança para priorização dos casos

O usuário pode interagir via interface web, enviando frases ou planilhas completas, e baixar relatórios detalhados das análises para integrar aos processos internos.

---

### ⚡ **Diferenciais**
- Modelagem baseada em exemplos reais, com refinamento de regras para minimizar falsos positivos.
- Pipeline flexível: fácil de adaptar para outros setores, linguagens e domínios.
- Apoio a análises em lote via planilhas — ideal para operações CS de alta escala.
- Fácil integração com sistemas internos (via API ou batch).

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

👉 https://huggingface.co/spaces/ViniciusKhan/ChurnSentinel-API

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

