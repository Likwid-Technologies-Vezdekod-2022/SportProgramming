import json

import requests


def count_passed_tasks(username: str) -> int:
    response = requests.get(url=f'https://codeforces.com/api/user.status?handle={username}')
    tasks = []

    if response.status_code == 200:

        content = json.loads(response.content.decode())

        for submission in content['result']:

            if submission['problem']['name'] not in tasks:
                tasks.append(submission['problem']['name'])

        return len(tasks)

    else:

        raise Exception('Ошибка запроса')


with open('participants.txt', 'r', encoding='utf-8') as file:
    participants = file.readlines()
    print(participants)

for participant in participants:
    count_of_passed_tasks = count_passed_tasks(username=participant)
    print(f'{participant} --> {count_of_passed_tasks}')
