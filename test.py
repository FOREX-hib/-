from openai import OpenAI

client = OpenAI(
    api_key="sk-EPL96nbX8sMtH5YivslkeeFiwDjxgfPRwgDnREqE0YASJaDV",
    base_url="https://sg.uiuiapi.com/v1"
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Привет!"}]
)

print(response.choices[0].message.content)
