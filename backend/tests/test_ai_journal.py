import httpx
import json

url = "http://127.0.0.1:8000/generate"
payload = {
    "system": "Convert this transcript into a professional journal entry. Use this EXACT structure:\n\nDAILY JOURNAL ENTRY\nDate: 2026-03-07\n--------------------------------------------------\n\n[The cleaned up transcription text]\n\n--------------------------------------------------\nQUICK NOTES:\n- Key Insight: [Generate a key insight from the text]\n- Action Item: [Generate a specific action item]\n\nGRATITUDE:\n- I am thankful for: [Generate something to be thankful for based on the content]\n\n--------------------------------------------------\nEnd of Transcript.",
    "prompt": "I went to the park today and saw a dog. It was a golden retriever. We played fetch for a while and then I came home."
}

try:
    response = httpx.post(url, json=payload, timeout=120.0)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
