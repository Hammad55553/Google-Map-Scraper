import requests
import json

url = "http://127.0.0.1:8000/api/inbox"
payload = {
    "gmail_address": "hammadaslam78612@gmail.com",
    "app_password": "tqmb xojp sjux yjjm",
    "limit": 5,
    "category": "primary"
}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=payload)
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(e)
