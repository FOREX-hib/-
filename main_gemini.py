#!/usr/bin/env python3
"""
Запуск:  python3 main_gemini.py
Ключ:      (Gemini)
"""
import os
import google.generativeai as genai

# 1. Подключаем ключ
genai.configure(
    api_key=""
)

# 2. Выбираем модель
model = genai.GenerativeModel("gemini-1.5-flash")

# 3. Генерируем пост
prompt = "Сгенерируй короткий маркетинговый пост для telegram-канала на тему «День без Wi-Fi»."
response = model.generate_content(prompt)

# 4. Вывод
print("📄 Сгенерированный пост:")
print("-" * 40)
print(response.text)