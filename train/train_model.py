# train/train_model.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
from train.dataset import carregar_dados
import os

# Caminhos
MODEL_PATH = "app/model/bert-large-portuguese-cased"
OUTPUT_PATH = "app/model/bert-finetuned-churnsentinel"

# Carregar dados CSV
(X_train, X_test, y_train, y_test), label_map = carregar_dados("data/exemplos_nps.csv")

# Tokenizador do modelo grande
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# Função de tokenização
def tokenize(batch):
    return tokenizer(batch["texto"], truncation=True, padding="max_length", max_length=256)

# Preparar datasets HuggingFace
train_dataset = Dataset.from_dict({"texto": X_train, "label": y_train}).map(tokenize, batched=True)
test_dataset = Dataset.from_dict({"texto": X_test, "label": y_test}).map(tokenize, batched=True)

# Carregar modelo com número de classes correto
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, num_labels=len(label_map))

# Argumentos de treino
args = TrainingArguments(
    output_dir=OUTPUT_PATH,
    evaluation_strategy="epoch",
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=4,
    weight_decay=0.01,
    logging_dir="logs",
    logging_steps=10,
    save_strategy="no",  # ⛔ NÃO salvar checkpoints intermediários
    load_best_model_at_end=False  # ✅ não depende de checkpoints
)
# Treinador
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    tokenizer=tokenizer
)

# Executar treino
trainer.train()

# Salvar modelo fine-tuned
trainer.save_model(OUTPUT_PATH)
tokenizer.save_pretrained(OUTPUT_PATH)

print("✅ Modelo fine-tuned salvo com sucesso em:", OUTPUT_PATH)
