import fileinput
import os
import logging
import random
import subprocess

avaliable_labels = [
    "compliant",
    "pornography",
    "violence",
    "toxicity",
    "politics",
    "advertising",
    "boycotting games",
    "cheating",
    "buying and selling resources",
    "buying and selling account",
    "non-official recharging",
    "diverting players to other games",
]

label_2_text = {key: [] for key in avaliable_labels}


for line in fileinput.input("./datasets/all.tsv"):
    line = line.strip()
    line = line.split("\t")
    if len(line) != 2:
        logging.warning("Invalid line: %s", line)
        continue
    content, explain = line

    for label in avaliable_labels:
        if label in explain:
            label_2_text[label].append(content)

# print number of samples for each label
for label in avaliable_labels:
    logging.warning("Label: %s, number of samples: %d", label, len(label_2_text[label]))

# remove old data
os.remove("./datasets/dev.tsv")
os.remove("./datasets/test.tsv")
os.remove("./datasets/train.tsv")

# shuffle and extract 10 sample each label as dev and test set respectively.
# remaining as training set.

for label in avaliable_labels:
    random.shuffle(label_2_text[label])
    with open("./datasets/dev.tsv".format(label), "a") as f:
        for line in label_2_text[label][:10]:
            f.write(line + "\t" + label + "\n")
    with open("./datasets/test.tsv".format(label), "a") as f:
        for line in label_2_text[label][10:20]:
            f.write(line + "\t" + label + "\n")
    with open("./datasets/train.tsv".format(label), "a") as f:
        for line in label_2_text[label][20:]:
            f.write(line + "\t" + label + "\n")


# shuffle training set
subprocess.call(
    "shuf ./datasets/train.tsv > ./datasets/train.tsv.tmp && mv ./datasets/train.tsv.tmp ./datasets/train.tsv",
    shell=True,
)
