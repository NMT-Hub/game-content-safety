from typing import List, Union

import torch
import torch.nn.functional as F
import transformers

from prepare_training_data import avaliable_labels, label_2_exp

model_path = "./models/xlm-roberta-base-finetuned/"

config = transformers.AutoConfig.from_pretrained(
    model_path,
    local_files_only=True,
)
tokenizer = transformers.AutoTokenizer.from_pretrained(
    model_path,
    local_files_only=True,
)
model = transformers.XLMRobertaForSequenceClassification.from_pretrained(
    model_path,
    config=config,
    local_files_only=True,
)

test_texts = [
    "boss u motherfucker",
    "草你妈",
    "搏一搏单车变摩托，赶紧来吧，可直接加微f-fak-fas",
    "我认为Player16195000005提问的Q5答案是A:1.5公里",
    "我解散了所有部隊……這樣你就可以攻擊我的別墅",
    "法克油",
    "who is that? new porn star?",
    "宝石便宜卖了,加v 线下私聊",
    "Thằng này to hơn tý này Đậu",
]


model.eval()


def predict(text: Union[str, List[str]]):
    if isinstance(text, str):
        batch = False
        text = [text]
    else:
        batch = True

    inputs = tokenizer(
        text, return_tensors="pt", padding=True, truncation=True, max_length=128
    )
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=-1).cpu().numpy().tolist()
    probs = F.softmax(logits, dim=-1).cpu().numpy().tolist()

    result = []
    for text, prediction in zip(test_texts, predictions):
        result.append(avaliable_labels[prediction])


    if batch:
        return result

    else:
        return {
            "label": result[0],
            "explanation": label_2_exp.get(result[0], ""),
            "prob": probs[0][predictions[0]]
        }


if __name__ == "__main__":
    predictions = predict(test_texts)

    for text, prediction in zip(test_texts, predictions):
        print(text, "\t", prediction)
