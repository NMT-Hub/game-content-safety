import fileinput
import logging
import re

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


for line in fileinput.input("./datasets/all.tsv"):
    line = line.strip()
    line = line.split("\t")
    if len(line) != 2:
        logging.warning("Invalid line: %s", line)
        continue
    content, explain = line

    for label in avaliable_labels:
        if label in explain:
            print("\t".join([label, content]))

with open("./datasets/labels.txt", "w") as f:
    for label in avaliable_labels:
        f.write(label + "\n")
