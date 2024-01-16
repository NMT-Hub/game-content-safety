# train xlm-roberta model
import evaluate
from transformers import (AutoConfig, AutoModelForSequenceClassification,
                          AutoTokenizer, Trainer, TrainingArguments,
                          default_data_collator)

from datasets import load_dataset
from prepare_training_data import avaliable_labels

# load model and tokenizer
config = AutoConfig.from_pretrained(
    "./models/xlm-roberta-base", num_labels=12, local_files_only=True
)
label2id = {label: i for i, label in enumerate(avaliable_labels)}

tokenizer = AutoTokenizer.from_pretrained(
    "./models/xlm-roberta-base",
    use_fast=True,
    local_files_only=True,
    label2id=label2id,
    id2label={i: label for i, label in enumerate(avaliable_labels)},
)
model = AutoModelForSequenceClassification.from_pretrained(
    "./models/xlm-roberta-base", config=config, local_files_only=True
)


# load datasets
def tokenize_function(examples):
    input_ = tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)
    return input_


train_dataset = load_dataset(
    "csv",
    data_files={
        "train": "./datasets/train.tsv",
        "dev": "./datasets/dev.tsv",
        "test": "./datasets/test.tsv",
    },
    delimiter="\t",
    column_names=["text", "label"],
    cache_dir="./datasets/cache",
)


tokenized_datasets = train_dataset.map(tokenize_function, batched=True)

metric = evaluate.load("accuracy")


# metric function
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = predictions.argmax(axis=1)
    return metric.compute(predictions=predictions, references=labels)


# training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=5,
    per_device_train_batch_size=96,
    per_device_eval_batch_size=96,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    greater_is_better=True,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["dev"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
    data_collator=default_data_collator,
)

# train
trainer.train()

# evaluate
trainer.evaluate()

# save model
trainer.save_model("./models/xlm-roberta-base-finetuned")
