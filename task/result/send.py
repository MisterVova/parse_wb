# from generator import Task
import requests
import time
from task.settings import URL_SERVER, SLEEP


class TaskSend:
    def __init__(self, ):
        pass

    # def exe(self, task: Task):
    def exe(self, task):
        # print("===")
        # print(len(task.prices))
        # data = {"last": "", "prices": "[1,2,3,4,5,6]", "key": "Прикормки для рыб", "isValid": "", "on": "", "row": 18}
        has_error = 0
        while True:
            try:
                data = task.obj
                requests.post(URL_SERVER, json=data)
                break
            except:
                print("Ошибка при отправке результата")
                time.sleep(SLEEP + SLEEP * has_error)
                has_error += 1
                if has_error > 20: has_error = 20

        # {"last": "", "prices": "[1,2,3,4,5,6]", "key": "Прикормки для рыб", "isValid": "", "on": "", "row": 18}
        # print(task.__dict__)
        # print("===")

    def start(self):
        print("start - TaskSend")

    def end(self):
        print("start - TaskSend")


def connect():
    # url = "https://script.google.com/macros/s/AKfycbx2Jm6G5vZLIgOYE8Bd2FWRevyn6KQKAGgEU4OTV4TUeIEYZ_RBFaJ7Ldau9MNzVTNq3w/exec"
    data = {"last": "", "prices": "[1,2,3,4,5,6]", "key": "Прикормки для рыб", "isValid": "", "on": "", "row": 18}
    response = requests.post(URL_SERVER, json=data)
    print(response)
    # print(response.json())
    # print(type(response.json()))


if __name__ == '__main__':
    connect()
