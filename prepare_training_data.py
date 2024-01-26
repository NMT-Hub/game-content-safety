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

label_2_exp = {
    "compliant": "合规: 不含有毒性内容。玩家之间的正常交流。",
    "pornography": "色情: 发送色情评论或色情信息的链接。",
    "violent": "暴力: 发送暴力言论。",
    "toxicity": "毒性：发送辱骂性言论。",
    "politics": "政治：发送政治敏感言论。",
    "advertising": "广告：发送与游戏无关的宣传信息，以及相关社交媒体链接。",
    "boycotting games": "抵制游戏：鼓励大家不玩这款游戏，如称这款游戏是骗局，说这款游戏浪费时间，煽动大家玩其他游戏等。",
    "cheating": "作弊：包括但不限于在游戏中发表如“我是内部人”，“我将使用脚本”，“我可以黑账号”等作弊相关言论。",
    "buying and selling resources": "买卖资源：包括但不限于在游戏中发表如“我在卖资源”，“我在买资源”，“我在卖账号”，“我在买账号”，“基地酒精1美元/百万，宝石1美元/百万，请私下联系xxx”等关于买卖资源的言论。",
    "buying and selling account": "买卖账号：例如，“该账号出售500美元，请私下联系xxx”等。",
    "non-official recharging": "非官方渠道充值：涉及“代购礼包”，“低价购买礼包”等言论，宣传通过非官方渠道充值，第三方充值等。",
    "diverting players to other games": "引流：涉及邀请参加其他游戏，邀请玩家加入其他游戏（出于重定向玩家的目的）。"
}


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

    # shuffle and extract 10 sample each label as dev and test set respectively.
    # remaining as training set.

    for label in avaliable_labels:
        random.shuffle(label_2_text[label])
        label_id = str(avaliable_labels.index(label))
        with open(f"./datasets/{label}.tsv", "a") as f:
            for line in label_2_text[label]:
                f.write(line + "\t" + label_id + "\n")


if __name__ == "__main__":
    main()
