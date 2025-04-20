import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# .env 読み込み
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")


# 指定日の天気予報を取得する関数（3時間ごとの予報から最も昼に近いものを選ぶ）
def get_forecast_for_date(lat, lon, target_date, api_key=API_KEY, units="metric", lang="ja"):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": units,
        "lang": lang
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return {"error": f"APIエラー: {response.status_code}"}

    data = response.json()
    forecast_list = data.get("list", [])
    if not forecast_list:
        return {"error": "天気データが取得できませんでした"}

    target_datetime_start = datetime.combine(target_date, datetime.min.time())
    target_datetime_end = target_datetime_start + timedelta(days=1)

    # 指定日（当日中）のデータに絞る
    filtered_forecasts = [
        f for f in forecast_list
        if target_datetime_start <= datetime.fromtimestamp(f["dt"]) < target_datetime_end
    ]

    if not filtered_forecasts:
        return {"error": "指定日の天気データが見つかりませんでした"}

    # 昼12:00に最も近い予報を選ぶ
    def time_distance(f):
        forecast_time = datetime.fromtimestamp(f["dt"]).time()
        return abs((datetime.combine(target_date, forecast_time) - datetime.combine(target_date, datetime.strptime("12:00", "%H:%M").time())).total_seconds())

    best_forecast = min(filtered_forecasts, key=time_distance)
    return {
        "datetime": datetime.fromtimestamp(best_forecast["dt"]).strftime("%Y-%m-%d %H:%M"),
        "description": best_forecast["weather"][0]["description"],
        "temp": best_forecast["main"]["temp"],
        "humidity": best_forecast["main"]["humidity"],
        "wind": best_forecast["wind"]["speed"]
    }
