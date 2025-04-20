import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("HOTPEPPER_API_KEY")
BASE_URL = "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/"

def search_restaurants(keyword: str, location: str, budget: str, count: int = 5):
    params = {
        "key": API_KEY,
        "format": "json",
        "keyword": keyword,
        "address": location,
        "budget": budget,
        "count": count
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        try:
            return response.json()["results"]["shop"]
        except KeyError:
            return []
    return []
