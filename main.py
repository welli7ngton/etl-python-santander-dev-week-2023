import pandas as pd
import requests
import json
import openai


df = pd.read_csv('SDW2023.csv')
user_ids = df['UserID'].tolist()
print(user_ids)


sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'


def get_user(_id):
    response = requests.get(f'{sdw2023_api_url}/users/{_id}')
    print(f'get user {_id} ok')
    print(response.status_code)
    return response.json() if response.status_code == 200 else None


for _id in user_ids:
    users = []
    user = get_user(_id)

    if user is not None:
        print('ok')
        users.append(user)


# users = [user for id in user_ids if (user := get_user(id)) is not None]
# print(users)
print(json.dumps(users, indent=2), 'aqui')


openai.api_key = "CHANGE-ME"


def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em markting bancário."
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


def update_user(user):
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False


for user in users:
    success = update_user(user)
    print(f"User {user['name']} updated? {success}!")
