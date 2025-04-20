import os
import requests
import folium
import polyline
import googlemaps
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

def get_traffic_info(origin, destination, departure_time="now"):
    url = "https://maps.googleapis.com/maps/api/directions/json"

    params = {
        "origin": origin,
        "destination": destination,
        "departure_time": departure_time,
        "traffic_model": "best_guess",
        "mode": "driving",
        "key": GOOGLE_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return {"error": f"APIエラー: {response.status_code}"}

    data = response.json()

    if data.get("status") != "OK":
        return {"error": f"APIステータス異常: {data.get('status')}"}

    if not data.get("routes"):
        return {"error": "ルートが取得できませんでした"}

    route = data["routes"][0]["legs"][0]

    polyline_points = data["routes"][0].get("overview_polyline", {}).get("points")
    if not polyline_points:
        return {"error": "ルートポリライン（地図線）が取得できませんでした"}

    return {
        "origin": route["start_address"],
        "destination": route["end_address"],
        "distance": route["distance"]["text"],
        "duration": route["duration"]["text"],
        "duration_in_traffic": route.get("duration_in_traffic", {}).get("text", "不明"),
        "summary": data["routes"][0].get("summary", ""),
        "polyline": polyline_points
    }

def create_map(origin, destination):
    # origin: 住所文字列, destination: {"name": str, "lat": float, "lon": float}
    origin_loc = gmaps.geocode(origin)[0]["geometry"]["location"]

    m = folium.Map(location=[destination["lat"], destination["lon"]], zoom_start=10)

    folium.Marker(
        location=[destination["lat"], destination["lon"]],
        popup=f"ゴルフ場: {destination['name']}",
        icon=folium.Icon(color="blue")
    ).add_to(m)

    folium.Marker(
        location=[origin_loc["lat"], origin_loc["lng"]],
        popup="自宅",
        icon=folium.Icon(color="green")
    ).add_to(m)

    # ルート取得と描画
    directions = gmaps.directions(
        origin=origin,
        destination=f"{destination['lat']},{destination['lon']}",
        mode="driving",
        departure_time="now",
        traffic_model="best_guess"
    )

    if directions and "overview_polyline" in directions[0]:
        route_polyline = directions[0]["overview_polyline"]["points"]
        points = polyline.decode(route_polyline)
        folium.PolyLine(points, color="blue", weight=4, opacity=0.6).add_to(m)

    return m
