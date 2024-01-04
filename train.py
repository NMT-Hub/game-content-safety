import datasets
import transformers

config = transformers.AutoConfig.from_pretrained(
    "./models/mt5-base/",
    local_files_only=True,
)
tokenizer = transformers.AutoTokenizer.from_pretrained(
    "./models/mt5-base/",
    local_files_only=True,
)
model = transformers.MT5ForConditionalGeneration.from_pretrained(
    "./models/mt5-base/",
    local_files_only=True,
    config=config,
).to("cuda")


# seq2seq datasets load from tsv files
dataset = datasets.load_dataset(
    "csv",
    data_files="./datasets/all.tsv",
    delimiter="\t",
    column_names=["input_column", "target_column"],
)
def preprocess_function(examples):
    inputs = [ex for ex in examples['input_column']]
    targets = [ex for ex in examples['target_column']]
    model_inputs = tokenizer(inputs, max_length=140, truncation=True, padding="max_length")
    # Set up the tokenizer for targets
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=140, truncation=True, padding="max_length")

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

def filter_function(example):
    return isinstance(example["input_column"], str) and isinstance(example["target_column"], str)

dataset = dataset.filter(filter_function)
tokenized_datasets = dataset.map(preprocess_function, batched=True)


# finetune the model with the dataset
model.train()
model.resize_token_embeddings(len(tokenizer))

training_args = transformers.TrainingArguments(
    output_dir="./checkpoints/mt5-base-finetune/",
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_train_batch_size=32,
    do_eval=False,
    save_steps=1000,
    save_total_limit=1,
    prediction_loss_only=True,
    logging_steps=10,
    logging_dir="./checkpoints/mt5-base-finetune/logs/",
    dataloader_num_workers=4,
    run_name="run_name",
    warmup_steps=500,                
    weight_decay=0.01,
)

trainer = transformers.Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    tokenizer=tokenizer,
)

trainer.train()

# save the model
trainer.save_model("./models/mt5-base-finetune/")
