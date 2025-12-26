import requests
import json

url = "http://127.0.0.1:8002/ai/explain"
payload = {
    "plot_length_ft": 40,
    "plot_width_ft": 60,
    "floors": 2,
    "location": "city",
    "building_type": "house",
    "quality": "standard",
    "budget_lakhs": 50
}
try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
