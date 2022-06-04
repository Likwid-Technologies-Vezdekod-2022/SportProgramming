import json
from typing import Union

import requests


class ApiRequests:
    def __init__(self, usernames):
        self.usernames: list = usernames

    def get_task(self) -> str:

        all_tasks: Union[list, set] = []
        for username in self.usernames:
            all_tasks += self.get_user_tasks(username=username)

        solved_tasks = set(all_tasks)

        tasks_for_solving = self.get_tasks_for_solving()

        for task in tasks_for_solving:
            if task['name'] not in solved_tasks:
                return task

    @staticmethod
    def get_user_tasks(username):
        response = requests.get(url=f'https://codeforces.com/api/user.status?handle={username}')

        tasks = []

        if response.status_code == 200:

            content = json.loads(response.content.decode())

            for submission in content['result']:
                if submission['problem']['name'] not in tasks:
                    tasks.append(submission['problem']['name'])

            return tasks

        else:

            raise Exception('Ошибка запроса')

    @staticmethod
    def get_tasks_for_solving() -> list:
        response = requests.get(url=f'https://codeforces.com/api/problemset.problems?')

        tasks = []

        if response.status_code == 200:

            content = json.loads(response.content.decode())
            for problem in content['result']['problems']:
                task = {'name': problem['name'], 'id': problem['contestId'], 'index': problem['index']}
                tasks.append(task)

            return tasks

        else:

            raise Exception('Ошибка запроса')
