import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification

# load tokenizer and model weights
tokenizer = RobertaTokenizer.from_pretrained('./models/roberta_toxicity_classifier', local_files_only=True)
model = RobertaForSequenceClassification.from_pretrained('./models/roberta_toxicity_classifier', local_files_only=True).eval().cuda()


text = "Farkle oil"

mapping = { 
    0: 'natural',
    1: 'toxic'
}


with torch.no_grad():
    # prepare the input
    inputs = tokenizer.batch_encode_plus([text], return_tensors='pt', padding=True).input_ids.cuda()
    # inference
    result = model(inputs).logits.cpu().numpy()[0]

    result = mapping[result.argmax()]

    print("法克油")
    print(text)
    print(result)
