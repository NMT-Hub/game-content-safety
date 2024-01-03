import re
import torch
import fasttext
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from google_translate import translate_text

# load tokenizer and model weights
tokenizer = RobertaTokenizer.from_pretrained('./models/roberta_toxicity_classifier', local_files_only=True)
model = RobertaForSequenceClassification.from_pretrained('./models/roberta_toxicity_classifier', local_files_only=True).eval().cuda()

lang_id_model = fasttext.load_model('./models/lid.176.bin')
lang_id_small_model = fasttext.load_model('./models/lid.176.ftz')



text = "Farkle oil"

mapping = { 
    0: 'compliant',
    1: 'toxic'
}


async def roberta_toxicity_classify(text):
    text = re.sub(r'\s+', ' ', text.strip())
    # detect if current line is English. use fasttext
    if len(text.split()) < 3:
        # lang_pred = lang_id_small_model.predict(text)
        lang_pred = lang_id_model.predict(text)
    else:
        lang_pred = lang_id_model.predict(text)
    if lang_pred[0][0] != '__label__en':
        # google translate
        text = await translate_text(text, lang_pred[0][0][9:], 'en')

    with torch.no_grad():
        # prepare the input
        inputs = tokenizer.batch_encode_plus([text], return_tensors='pt', padding=True).input_ids.cuda()
        # inference
        result = model(inputs).logits.cpu().numpy()[0]

        result = mapping[result.argmax()]
        return {"label": result, "explanation": "Toxicity content"}


if __name__ == "__main__":
    import asyncio
    text = "草你妈"
    print(asyncio.run(roberta_toxicity_classify(text)))
