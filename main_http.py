#!/usr/bin/env python3
import os
import requests
import json

GEMINI_KEY = "AIzaSyB4pKcVECjHnlMW54JuQdw65DsR1w2FjuU"  # ваш ключ
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

payload = {
    "contents": [
        {"parts": [{"text": "Привет! Как дела?"}]}
    ]
}

resp = requests.post(
    URL,
    params={"key": GEMINI_KEY},
    headers={"Content-Type": "application/json"},
    json=payload,
    timeout=30
)

if resp.status_code == 200:
    text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    print(text)
else:
    print("Ошибка:", resp.status_code, resp.text)