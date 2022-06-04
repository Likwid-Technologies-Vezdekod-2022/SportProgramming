import json

import requests


def count_passed_tasks(username: str) -> int:
    response = requests.get(url=f'https://codeforces.com/api/user.status?handle={username}')

    if response.status_code == 200:

        content = json.loads(response.content.decode())
        success_counter: int = 0
        for submission in content['result']:
            if submission['verdict'] == 'OK':
                success_counter += 1
    else:

        raise Exception('Ошибка запроса')

    return success_counter


with open('participants.txt', 'r', encoding='utf-8') as file:
    participants = file.readlines()
    print(participants)

for participant in participants:
    count_of_passed_tasks = count_passed_tasks(username=participant)
    print(count_of_passed_tasks)
