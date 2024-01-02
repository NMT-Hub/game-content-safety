SYSTEM_PROMPT = """
I want to perform content safety recognition and filtering for the speech in the game chat system. The main requirements are as follows.

Speech Characteristics: Include but are not limited to insults, racial discrimination, inappropriate remarks related to pornography/gambling/drugs, etc. Handle flexibly according to the specific conversation context.
Spreading Cheating Speech

Speech Characteristics: Include but are not limited to releasing statements like "I'm a shill" or "I use scripts" or "I can hack accounts" in games, among other cheating-related remarks.
Speech Related to Buying and Selling Resources

Speech Characteristics: For example, statements like "Base liquor $1/M, gems $1/M, contact xxx for offline private chat", etc.
Speech Related to Buying and Selling Accounts

Speech Characteristics: For example, statements like "This account for sale at $500, contact xxx for offline private chat", etc.
Speech about Recharging via Non-official Channels

Speech Characteristics: Speech involving "buying gift packages on behalf", "buying gift packages at low prices", etc., spreading recharging through non-official channels, proxy recharging, etc.
Washing People/Draining Traffic

Speech Characteristics: Involves inviting information for other games, inviting players to join other games (draining traffic).

Categories Divided: Compliant, Incendiary Speech, Boycotting the Game, Washing People/Draining Traffic, Pornography, Violence, Politics, Advertising, Spreading Cheating Speech, Speech about Buying and Selling Resources, Speech about Buying and Selling Accounts, Speech about Recharging via Non-official Channels.

Please label the given sentences with specific categories
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
2. You're so bad, uninstall the game, loser! 
3. Everyone should stop playing this game, it's a total scam!
4. Why waste your time here? Everyone's moving to [another platform or game].
5. pornhub.com
6. Do you dare to come here and I will kill you?
7. Israel should destroy Palestine
8. Visit [url] to buy cheap in-game currency fast and safely!
9. Just use this glitch to get unlimited coins, it's easy and they'll never catch you
10. Selling epic weapon for 50 bucks, legit and fast delivery.
11. Anyone selling their account? Need a new one with good stats.
12. Get double the diamonds for half the price! PM me for non-official top-up.
"""
         },
        {
            "role": "assistant",
            "content": """
1. Compliant
2. Incendiary Speech
3. Boycotting the Game
4. Washing People/Draining Traffic
5. Pornography
6. Violence
7. Politics
8. Advertising
9. Spreading Cheating Speech
10. Speech about Buying and Selling Resources
11. Speech about Buying and Selling Accounts
12. Speech about Recharging via Non-official Channels.
"""
        },
    {"role": "user", "content": "\n".join([f"{i+1}. {x}" for i, x in enumerate(texts)])},
    ]
    chat_completion_resp = await client.chat.completions.create(
        messages=messages, timeout=30, model=DEPLOYMENT_ID, temperature=0.0
    )
    response = chat_completion_resp.choices[0].message.content

    if not response.endswith("\n"):
        response += "\n"
    labels = re.findall(r"\d+\.\s*(.*)\n", response, re.MULTILINE)

    if len(labels) != len(texts):
        logger.warning(f"ChatGPT failed: {response}")
        return ["UNK"] * len(texts)
    return labels


async def main():
    num = 0
    batch = []

    # for line in tqdm(fileinput.input("./data/data.txt")):
    for line in tqdm(sys.stdin):
        num += 1
        batch.append(line.strip())
        if num % 10 == 0:
            labels = await label_toxity_texts(batch)
            for t, l in zip(batch, labels):
                print(f"{t}\t{l}")
            batch = []

    if batch:
        labels = await label_toxity_texts(batch)
        for t, l in zip(batch, labels):
            print(f"{t}\t{l}")
        
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
