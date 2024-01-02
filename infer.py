import torch
import tqdm
import re
import fasttext
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import fileinput

# load tokenizer and model weights
tokenizer = RobertaTokenizer.from_pretrained('./models/roberta_toxicity_classifier', local_files_only=True)
model = RobertaForSequenceClassification.from_pretrained('./models/roberta_toxicity_classifier', local_files_only=True).eval().cuda()

mapping = { 
    0: 'natural',
    1: 'toxic'
}

lang_id_model = fasttext.load_model('./models/lid.176.bin')
lang_id_small_model = fasttext.load_model('./models/lid.176.ftz')


cur_num = 0
batch = []
for line in tqdm.tqdm(fileinput.input("./data/data.txt")):
    line = re.sub(r'\s+', ' ', line.strip())
    # detect if current line is English. use fasttext
    if len(line.split()) < 3:
        lang_pred = lang_id_small_model.predict(line)
    else:
        lang_pred = lang_id_model.predict(line)
    if lang_pred[0][0] != '__label__en':
        print(line + "\t" + 'non-English')
        continue

    batch.append(line)
    cur_num += 1

    if cur_num == 32:
        with torch.no_grad():
            # prepare the input
            inputs = tokenizer.batch_encode_plus(batch, return_tensors='pt', padding=True)
            # inference
            result = model(inputs.input_ids.cuda(), inputs.attention_mask.cuda()).logits.cpu().numpy()
            for i in range(len(result)):
                print(batch[i] + "\t" + mapping[result[i].argmax()])
            batch = []
            cur_num = 0

