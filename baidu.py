import asyncio
import aiohttp

API_KEY = "WgEkcfp6wQ7pWrVqu2y88OS1"
SECRET_KEY = "y0mP2CYQ1fTXzBLdP90IVwEblMcY86VX"


async def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params) as response:
            response_data = await response.json()
            return response_data.get("access_token")


async def get_text_censor(text):
    """
    文本审核
    :return: None
    """
    access_token = await get_access_token()
    url = (
        "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined?access_token="
        + access_token
    )
    payload = {"text": text}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    # response = requests.request("POST", url, headers=headers, data=payload)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as response:
            return await response.json()


def main():
    payload = {
        # "text": "搏一搏单车变摩托，赶紧来吧，可直接加微f-fak-fas",
        # "text": "我认为Player16195000005提问的Q5答案是A:1.5公里",
        # "text": "我解散了所有部隊……這樣你就可以攻擊我的別墅",
        "text": "法克油",
        # "text": "who is that? new porn star?",
        # "text": "宝石便宜卖了,加v 线下私聊"
    }
    print(asyncio.run(get_text_censor(payload["text"])))


if __name__ == "__main__":
    main()
