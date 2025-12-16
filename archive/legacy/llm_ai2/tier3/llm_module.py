import os
import requests

TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY", "")
MODEL_NAME = os.environ.get("TOGETHER_MODEL", "mistralai/Mistral-7B-Instruct-v0.1")

def query_together_ai(prompt: str, max_tokens=500, temperature=0.7):
    if not TOGETHER_API_KEY:
        raise RuntimeError("TOGETHER_API_KEY is not set")
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": 0.9,
        "stop": ["</s>"]
    }

    response = requests.post(
        "https://api.together.xyz/inference",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()["output"]["choices"][0]["text"].strip()
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")

# --- The following test harness code is omitted in production --- 