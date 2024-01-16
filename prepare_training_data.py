import fileinput
import logging
import os
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


def main():
    label_2_text = {key: [] for key in avaliable_labels}

    for line in fileinput.input("./datasets/all.tsv"):
        line = line.strip()
        line = line.split("\t")
        if len(line) != 2:
            logging.warning("Invalid line: %s", line)
            continue
        content, explain = line

        if not content or not explain:
            logging.warning("Invalid line: %s", line)
            continue

        for label in avaliable_labels:
            if label in explain:
                label_2_text[label].append(content)

    # print number of samples for each label
    for label in avaliable_labels:
        logging.warning(
            "Label: %s, number of samples: %d", label, len(label_2_text[label])
        )

    # remove old data
    os.remove("./datasets/dev.tsv")
    os.remove("./datasets/test.tsv")
    os.remove("./datasets/train.tsv")

    # # write header
    # with open("./datasets/dev.tsv", "a") as f:
    #     f.write("text\tlabel\n")
    # with open("./datasets/test.tsv", "a") as f:
    #     f.write("text\tlabel\n")
    # with open("./datasets/train.tsv", "a") as f:
    #     f.write("text\tlabel\n")

    # shuffle and extract 10 sample each label as dev and test set respectively.
    # remaining as training set.

    for label in avaliable_labels:
        random.shuffle(label_2_text[label])
        label_id = str(avaliable_labels.index(label))
        with open("./datasets/dev.tsv", "a") as f:
            for line in label_2_text[label][:10]:
                f.write(line + "\t" + label_id + "\n")
        with open("./datasets/test.tsv", "a") as f:
            for line in label_2_text[label][10:20]:
                f.write(line + "\t" + label_id + "\n")
        with open("./datasets/train.tsv", "a") as f:
            if label == "compliant":
                for line in label_2_text[label][20:20000]:
                    f.write(line + "\t" + label_id + "\n")
            else:
                for line in label_2_text[label][20:]:
                    f.write(line + "\t" + label_id + "\n")

    # shuffle training set
    subprocess.call(
        "shuf ./datasets/train.tsv > ./datasets/train.tsv.tmp && mv ./datasets/train.tsv.tmp ./datasets/train.tsv",
        shell=True,
    )


if __name__ == "__main__":
    main()
