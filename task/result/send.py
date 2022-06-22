# from generator import Task
import requests
import time

from task.generator.key import SheetNames, Key
from task.settings import URL_SERVER, SLEEP
from task.generator.base_task import BaseTask as Task


class TaskSend:
    def __init__(self, ):
        pass

    # def exe(self, tasks: Task):
    def exe(self, task: Task):
        # print("===")
        # print(len(tasks.prices))
        # data = {"last": "", "prices": "[1,2,3,4,5,6]", "key": "Прикормки для рыб", "isValid": "", "on": "", "row": 18}
        has_error = 0
        while True:
            try:
                data = task.obj
                # print("send data", data)

                url = F"{URL_SERVER}?{Key.sheetName}={task.get_value(Key.sheetName,'')}"

                response = requests.post(url, json=data)
                # print(response)
                # print(response.text)
                break
            except:
                print("Ошибка при отправке результата")
                time.sleep(SLEEP + SLEEP * has_error)
                has_error += 1
                if has_error > 20: has_error = 20

        # {"last": "", "prices": "[1,2,3,4,5,6]", "key": "Прикормки для рыб", "isValid": "", "on": "", "row": 18}
        # print(tasks.__dict__)
        # print("===")

    def start(self):
        print("start - TaskSend")

    def end(self):
        print("start - TaskSend")


def connect():
    # url = "https://script.google.com/macros/s/AKfycbx2Jm6G5vZLIgOYE8Bd2FWRevyn6KQKAGgEU4OTV4TUeIEYZ_RBFaJ7Ldau9MNzVTNq3w/exec"
    data = {"last": "", "value": [1, 2, 3, 4, 5, 6], "key": "Прикормки для рыб", "isValid": "", "on": "", "row": 18}
    # url = URL_SERVER + f"?{Key.sheetName}={SheetNames.Задачи}"
    url = F"{URL_SERVER}?{Key.sheetName}={SheetNames.Задачи}"
    print(url)
    response = requests.post(url, json=data)
    print(response)

    print(response.text)
    # print(type(response.json()))


if __name__ == '__main__':
    connect()
