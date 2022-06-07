import time

import requests

from task.generator.key import Key, SheetNames
from task.settings import URL_SERVER, URL_WB_SEARCH, URL_WB_MAIN
from task.settings import SLEEP


class BaseTask:
    def __init__(self, obj: dict):
        self.isValid = True

        self.obj = obj
        if type(self.obj) != dict:
            self.isValid = False
            self.obj = dict()

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
        return f"""{self.get_value(Key.row, "000"):5} | {self.get_value(Key.sheetName, SheetNames.НеОпределён):12} | {self.get_value(Key.key, "____")}"""


class TaskList:
    SheetNamesList = [
        SheetNames.Карточки,
        SheetNames.Предметы,
        SheetNames.Продавцы,
    ]

    def get_tasks(self)-> BaseTask:
        obj = None
        for sheet_name in self.SheetNamesList:
            obj = self.get_objs_by_sheet_name(sheet_name=sheet_name, obj=obj)
            if obj: break
        task = BaseTask(obj)
        return task

    def get_objs_by_sheet_name(self, sheet_name, obj=None):
        # obj = None
        try:
            url = F"{URL_SERVER}?{Key.sheetName}={sheet_name}"
            # print("url = ", url)
            response = requests.get(url)
            # print("response.text = ",response.text)
            if response.text:
                obj = response.json()
        except:
            pass
            # print("Ошибка при получении задания")
        return obj

    def start(self):
        print("start - TaskList")

    def end(self):
        print("end - TaskList")
