import asyncio

from typing import Any
from azure.ai.contentsafety.aio import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions

CONTENT_SAFETY_KEY = "f0e9b0df97ec40ec9a7d6a3d40f4e540"

CONTENT_SAFETY_ENDPOINT = "https://ai-content-ifun.cognitiveservices.azure.com/"


async def analyze_text_async(text: str) -> dict[str, Any]:
    # analyze text async
    key = CONTENT_SAFETY_KEY
    endpoint = CONTENT_SAFETY_ENDPOINT

    # Create an Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    async with client:
        # Construct a request
        request = AnalyzeTextOptions(text=text)

        # Analyze text
        try:
            response = await client.analyze_text(request)
        except HttpResponseError as e:
            print("Analyze text failed.")
            if e.error:
                print(f"Error code: {e.error.code}")
                print(f"Error message: {e.error.message}")
                raise
            print(e)
            raise

    result = response.as_dict()["categoriesAnalysis"]
    if all(item["severity"] == 0 for item in result):
        return {
            "label": "compliant",
        }
    else:
        most_severe = max(result, key=lambda x: x["severity"])
        return {
            "label": most_severe["category"],
            "severity": most_severe["severity"],
        }


async def main():
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
    ] + [line.strip() for line in open("./test_set.txt").readlines()]

    for text in test_texts:
        result = await analyze_text_async(text)
        print(text)
        print(result)
        print()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
