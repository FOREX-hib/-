import google.generativeai as genai

genai.configure(api_key="AIzaSyCX-fRnapjtFiLi13pr_EHYEsRv8EYnVlA")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Привет! Как дела?")
print(response.text)