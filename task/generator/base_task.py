import time

import requests

from task.generator.key import Key, SheetNames
from task.settings import URL_SERVER, URL_WB_SEARCH, URL_WB_MAIN
from task.settings import SLEEP


class BaseTask:
    def __init__(self, obj: dict):
        self.isValid = True
        # self.url = URL_WB_MAIN
        # self.prices = []

        self.obj = obj
        if type(self.obj) != dict:
            # self.isValid = False
            self.obj = dict()
        # self.get_value()

    def get_sheet_name(self):
        return self.get_value(Key.sheetName, SheetNames.НеОпределён)

    # def get_url(self):
    #    return self.get_value(key=Key.url, default=URL_WB_MAIN)

    def set_value(self, key: str, value):
        self.obj[key] = value

    def get_value(self, key: str, default):
        # print(key, default, self.obj)
        ret = self.obj[key]
        return ret if ret else default

    def __str__(self):
        return self.get_value(Key.key,"____");

class TaskList:

    def get_tasks(self):
        for obj in self.get_Objs():
            # print(obj)
            task = BaseTask(obj)
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
                response = requests.get(F"{URL_SERVER}?{Key.sheetName}={SheetNames.Предметы}")
                has_error = 0
                # print("response.text = ",response.text)
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
