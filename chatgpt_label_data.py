SYSTEM_PROMPT = """
Your role is to identify and categorize sensitive information in various forms of communication within a gaming environment. You will focus on detecting inappropriate comments, such as abusive language, racial discrimination, and references to inappropriate content like gambling or drugs. Additionally, you'll identify discussions about cheating, selling or buying game resources or accounts, unauthorized channel transactions, and soliciting for other games. Your goal is to maintain a safe and respectful gaming community by flagging these types of content across different communication mediums like alliance chat, world chat, private messages, emails, game nicknames, avatars, alliance nicknames, and alliance announcements.

Categories Divided: 
- compliant: No toxity contents. Normal communication among players.
- pornography: Sending pornographic remarks or links to pornographic information.
- violence: Sending violent remarks.
- toxity: Sending abusive remarks.
- politics: Sending politically sensitive remarks.
- advertising: Sending promotional messages unrelated to the game, as well as related social media links.
- boycotting games: Encouraging everyone not to play this game, such as saying that this game is a scam, saying that this game is a waste of time, inciting everyone to play other games, etc.
- cheating: Characteristics of the Statements: Including but not limited to making statements in games such as 'I am a shill', 'I will use scripts', 'I can hack accounts', and other related cheating statements."
- buying and selling resources: Characteristics of the Statements: Including but not limited to making statements in games such as 'I am selling resources', 'I am buying resources', 'I am selling accounts', 'I am buying accounts', 'Base alcohol $1/M, gems $1/M, contact xxx offline for private chat', and so on." and other related statements about buying and selling resources. 
- buying and selling account: Discussions Related to Buying and Selling Accounts: For example, 'This account for sale at $500, contact xxx offline for private chat', and so on.
- non-official recharging: Recharging Through Non-Official Channels: Statements involving 'purchasing gift packs on behalf', 'buying gift packs at a low price', and other similar remarks, promoting recharging through non-official channels, third-party recharging, etc.
- diverting players to other games: Involving Invitations to Other Games, Inviting Players to Join Other Games (For the Purpose of Redirecting Players).

Please label the given multilingual sentences with specific categories with the given categories with detailed explanations. 
"""

import sys
import openai
import re
from tqdm import tqdm
from typing import List
import fileinput

from loguru import logger

AZURE_OPENAI_API_KEY="4d9ec5a0a2d94d428cae2636e8e609de"
AZURE_OPENAI_ENDPOINT="https://ifunazure.openai.azure.com/"
DEPLOYMENT_ID="ifun_translation"

client = openai.AsyncAzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=DEPLOYMENT_ID,
    api_version="2023-07-01-preview"
)

async def label_toxity_texts(texts: List[str]) -> List[str]:
    # Compliant, Incendiary Speech, Boycotting the Game, Washing People/Draining Traffic, Pornography, Violence, Politics, Advertising, Spreading Cheating Speech, Speech about Buying and Selling Resources, Speech about Buying and Selling Accounts, Speech about Recharging via Non-official Channels.
    # 合规、煽动性言论、抵制游戏、洗人/引流、色情、暴力、政治、广告、散布作弊言论、买卖资源言论、买卖账号言论、非官方渠道充值言论
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": """
1. yeah , they have t5 bro
2. pornhub.com
3. Do you dare to come here and I will kill you?
4. Israel should destroy Palestine
5. 搏一搏单车变摩托，赶紧来吧，可直接加微f-fak-fas
6. Cùng nhau nổ tung màn hình và lấn át máy chủ trò chơi
7. Todos deveriam parar de jogar este jogo, é uma farsa total!
8. the script can directly complete the level.
9. 宝石便宜卖了,加v 线下私聊
10. power leveling services, for account purchases message me privately
11. Add me for an 80% discount on top-up vouchers 
12. Why waste your time here? Everyone's moving to LOL
13. 🤩🤩🤩👌☕
14. hlo
15. go fuck yourself
"""
         },
        {
            "role": "assistant",
            "content": """
1. Normal game discussion. 't5 bro' Likely referring to some aspect of the game. Labeled as 'compliant'.
2. pornographic website. Labeled as 'pornography'
3. Threatening to kill the other person. Labeled as 'violence'.
4. Politically sensitive comments. Labeled as 'politics'.
5. Involving private message promotion advertisements. Labeled as 'advertising'.
6. Inciting players to take actions that destroy the game. Labeled as 'boycotting games'
7. Encouraging everyone not to play this game is part of a speech advocating for boycotting the game. Labeled as 'boycotting games'.
8. Cheating with scripts. Labeled as 'cheating'.
9. Selling gems. Labeled as 'buying and selling resources'.
10. Selling accounts. Labeled as 'buying and selling account'.
11. Recharging through non-official channels. Labeled as 'non-official recharging'.
12. Saying playing this game is a waste of time, inciting everyone to play LOL instead. Labeled as 'diverting players to other games'.
13. Emoji. Labeled as 'compliant'.
14. Greating. Labeled as 'compliant'.
15. Abusive remarks. Labeled as 'toxity'.
"""
        },
    {"role": "user", "content": "\n".join([f"{i+1}. {x}" for i, x in enumerate(texts)])},
    ]
    chat_completion_resp = await client.chat.completions.create(
        messages=messages, timeout=30, model=DEPLOYMENT_ID, temperature=0.0,
    )
    response = chat_completion_resp.choices[0].message.content

    if not response.endswith("\n"):
        response += "\n"

    explanations = re.findall(r"(\d+\..*)\n", response, re.MULTILINE)
    if len(explanations) != len(texts):
        explanations = re.split(r"[\n\r]+", response.strip())
    labels = []
    for e in explanations:
        m = re.match(r".*Labeled as '(.*)'\.*", e)
        if m:
            labels.append(m.group(1))
        else:
            labels.append("unclear")

    explanations = [re.sub(r"\d+\.", "", e).strip() for e in explanations]

    if len(labels) != len(texts) or len(explanations) != len(texts):
        logger.warning(f"ChatGPT failed: {response}")
        return ["UNK"] * len(texts), ["UNK"] * len(texts)
    return explanations, labels


async def label_toxity_text(text: str) -> str:
    input_texts = [
    "k gimme a sec to see if magician got last battle thirst prize",
    "win did u finish all smuggling event?",
    text,
    ]
    explanations, labels = await label_toxity_texts(input_texts)
    return explanations[-1], labels[-1]


async def main():
    num = 0
    batch = []
    batch_size = 20

    # for line in tqdm(fileinput.input("./data/data.txt")):
    for line in tqdm(sys.stdin):
        num += 1
        batch.append(line.strip())
        if num % batch_size == 0:
            explanations, labels = await label_toxity_texts(batch)
            for t, e, l in zip(batch, explanations, labels):
                print(f"{l}\t{t}\t{e}")
            batch = []

    if batch:
        explanations, labels  = await label_toxity_texts(batch)
        for t, e, l in zip(batch, explanations, labels):
            print(f"{l}\t{t}\t{e}")
        
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
