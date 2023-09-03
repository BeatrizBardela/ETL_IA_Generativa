sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

import pandas as pd
df = pd.read_excel('C:/Users/Beatriz/Desktop/Santander_Bootcamp/Desafio_IA_Generativa/SDW2023.csv.xlsx')
user_ids = df['UserID'].tolist()
# print(user_ids)

import requests
import json

def get_user(id):
    response = requests.get(f'{sdw2023_api_url}/users/{id}')
    print(response)
    return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
# print(json.dumps(users, indent=2))

openai_api_key = 'secret_key'
import openai
openai.api_key = openai_api_key

def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
      {
          "role": "system",
          "content": "Você é um especialista em marketing bancário."
      },
      {
          "role": "user",
          "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)"
      }
    ]
  )
  return completion.choices[0].message.content.strip('\"')

for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].append({
      "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
      "description": news
  })