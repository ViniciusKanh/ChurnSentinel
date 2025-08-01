from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    TrainingArguments, Trainer
)
from datasets import load_dataset
import numpy as np, evaluate, os, torch, random

MODEL_BASE   = "neuralmind/bert-large-portuguese-cased"
DATA_CSV     = "data/fuga_dataset.csv"
OUT_DIR      = "app/model/bert-fuga-churnsentinel"
SEED         = 42

# — reproducibilidade
torch.manual_seed(SEED); np.random.seed(SEED); random.seed(SEED)

# — carregar dataset HuggingFace
ds = load_dataset("csv", data_files=DATA_CSV, delimiter=";")
ds = ds["train"].train_test_split(test_size=0.2, seed=SEED)
tokenizer = AutoTokenizer.from_pretrained(MODEL_BASE)

def tok(batch):
    # garante string e evita NaN
    textos = [str(t) if t is not None else "" for t in batch["texto"]]
    return tokenizer(
        textos,
        truncation=True,
        padding="max_length",
        max_length=256,
    )

ds_tok = ds.map(tok, batched=True)
labels = 2  # 0 ou 1

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_BASE, num_labels=labels
)

args = TrainingArguments(
    output_dir           = OUT_DIR,
    evaluation_strategy  = "epoch",
    per_device_train_batch_size = 4,
    per_device_eval_batch_size  = 4,
    num_train_epochs     = 3,
    weight_decay         = 0.01,
    save_strategy        = "no",
    learning_rate        = 2e-5,
    load_best_model_at_end=False
)

metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return metric.compute(predictions=preds, references=labels)

trainer = Trainer(
    model           = model,
    args            = args,
    train_dataset   = ds_tok["train"],
    eval_dataset    = ds_tok["test"],
    tokenizer       = tokenizer,
    compute_metrics = compute_metrics
)

trainer.train()
trainer.save_model(OUT_DIR)
tokenizer.save_pretrained(OUT_DIR)
print(f"✅ Modelo salvo em {OUT_DIR}")
