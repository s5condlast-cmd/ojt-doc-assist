import httpx
import json

url = "http://127.0.0.1:8000/generate"
payload = {
    "system": "You are a helpful assistant.",
    "prompt": "Say hello!"
}

try:
    response = httpx.post(url, json=payload, timeout=60.0)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
