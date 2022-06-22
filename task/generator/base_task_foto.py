import time

import requests

from task.generator.base_task import BaseTask
from task.generator.key import Key, SheetNames
from task.settings.settings_foto import URL_SERVER,  SLEEP


class TaskList:
    SheetNamesList = [
        SheetNames.Фото,
        # SheetNames.Карточки,
        # SheetNames.Предметы,
        # SheetNames.Продавцы,
    ]

    def get_tasks(self) -> BaseTask:
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
