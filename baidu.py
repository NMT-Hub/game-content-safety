import requests

API_KEY = "WgEkcfp6wQ7pWrVqu2y88OS1"
SECRET_KEY = "y0mP2CYQ1fTXzBLdP90IVwEblMcY86VX"

def main():
        
    url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined?access_token=" + get_access_token()
    
    payload={
        "text": "搏一搏单车变摩托，赶紧来吧，可直接加微f-fak-fas",
        "text": "我认为Player16195000005提问的Q5答案是A:1.5公里",
        "text": "我解散了所有部隊……這樣你就可以攻擊我的別墅",
        "text": "法克油"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    main()

