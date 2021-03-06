import time

import requests
from task.settings import URL_SERVER, URL_WB_SEARCH, URL_WB_MAIN
from task.settings import SLEEP

class Key:
    row = "row"
    key = "key"
    on = "on"
    last = "last"
    isValid = "isValid"
    value = "value"
    prices = "prices"
    error = "error"
    wait = "_!_ЖДИ_!_"


class Task:
    def __init__(self, obj: dict):

        self.isValid = True
        self.url = URL_WB_MAIN
        # self.prices = []
        if type(obj) != dict:
            self.isValid = False
            return

        self.obj = obj
        if not self.obj[Key.key]:
            self.isValid = False
        elif f"{self.obj[Key.key]}".find(URL_WB_MAIN) != -1:
            self.url = f"{self.obj[Key.key]}"
        else:
            # https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&search=%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82+%D1%81%D0%BE%D1%81%D0%B5%D0%B4
            self.url = f"{URL_WB_SEARCH}{self.obj[Key.key]}"

        if self.isValid:
            self.obj[Key.prices] = []
        else:
            self.obj[Key.error] = "Ошибка Валидации"

        # print(self.url)

    def add_price(self, price):
        self.obj[Key.prices].append(price)

    def get_prices(self):
        return self.obj[Key.prices]


class TaskList:

    def get_tasks(self):
        for obj in self.get_Objs():
            # print(obj)
            task = Task(obj)
            if not task.isValid:
                continue

            if task.obj[Key.key] == Key.wait:
                sek = task.obj[Key.value]
                if not sek:
                    sek = 60 * 15
                print(f"Ждем Задание {task.obj[Key.key]} {sek} секунд")
                time.sleep(sek)
                continue

            yield task


    # count = 0
    def get_Objs(self):
        has_error = 0
        while True:
            try:
                 response = requests.get(URL_SERVER)
                 has_error = 0
            except:
                time.sleep(SLEEP * has_error)
                has_error += 1
                if has_error > 20: has_error = 20

            if response.status_code != 200:
                # sek = 6 * 3
                # print(f"response.status_code={response.status_code} ждем {sek} секунд")
                # time.sleep(sek)
                print("Ошибка при получении задания")
                yield {Key.key: Key.wait, Key.value: 30}

                continue

            try:
                obj = response.json()
            except:
                print("Заданий нет")
                obj = None

            # print(obj)
            if not obj:
                break
            has_error = 0
            yield obj

    def start(self):
        print("start - TaskList")

    def end(self):
        print("end - TaskList")


def connect():
    # url = "https://script.google.com/macros/s/AKfycbx2Jm6G5vZLIgOYE8Bd2FWRevyn6KQKAGgEU4OTV4TUeIEYZ_RBFaJ7Ldau9MNzVTNq3w/exec"
    response = requests.get(URL_SERVER)
    print(response)
    print(response.json())
    print(type(response.json()))


if __name__ == '__main__':
    # import time

    taskList = TaskList()
    for t in taskList.get_tasks():
        print(t.__dict__)
        print("count", taskList.count)
        time.sleep(3)
        print("---------------------------------------")
