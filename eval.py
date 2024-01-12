import transformers

import datasets

model_path = "./checkpoints/mt5-base-finetune/checkpoint-4000/"

config = transformers.AutoConfig.from_pretrained(
    model_path,
    local_files_only=True,
)
tokenizer = transformers.AutoTokenizer.from_pretrained(
    model_path,
    local_files_only=True,
)
model = transformers.MT5ForConditionalGeneration.from_pretrained(
    model_path,
    local_files_only=True,
    config=config,
)


# infer
data = [
    "boss u motherfucker",
    "草你妈",
    "搏一搏单车变摩托，赶紧来吧，可直接加微f-fak-fas",
    "我认为Player16195000005提问的Q5答案是A:1.5公里",
    "我解散了所有部隊……這樣你就可以攻擊我的別墅",
    "法克油",
    "who is that? new porn star?",
    "宝石便宜卖了,加v 线下私聊",
    'Thằng này to hơn tý này Đậu',
]

# tokenize
for line in data:
    input_ids = tokenizer.encode(line, return_tensors="pt")

    # Generate translation using the model
    translated_ids = model.generate(input_ids, num_beams=5)

    # Decode the translated text
    translated_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True)
    print(translated_text)


