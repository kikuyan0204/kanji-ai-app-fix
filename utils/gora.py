import os
import requests
from dotenv import load_dotenv

load_dotenv()
RAKUTEN_API_KEY = os.getenv("RAKUTEN_API_KEY")

SEARCH_API = "https://app.rakuten.co.jp/services/api/Gora/GoraGolfCourseSearch/20170623"

def search_golf_courses(area=None, fee=None, style=None, name=None, count=5):
    params = {
        "applicationId": RAKUTEN_API_KEY,
        "format": "json",
        "hits": count,
    }

    if area:
        params["keyword"] = area
    if fee:
        params["feeMax"] = fee
    if style:
        params["playStyle"] = style
    if name:
        params["keyword"] = name

    # 🔽 この位置に print() を追加します！
    print("===== 送信パラメータ =====")
    print(params)

    res = requests.get(SEARCH_API, params=params)

    if res.status_code == 200:
        try:
            data = res.json()
            print("===== 受信レスポンス（一部） =====")
            print(data.get("Items", "Itemsなし"))
            return data.get("Items", [])
        except Exception as e:
            print("レスポンス解析中にエラー:", e)
            return []
    else:
        print("HTTPエラー:", res.status_code)
    return []