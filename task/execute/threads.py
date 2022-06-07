import threading
import datetime
import traceback

from task.generator.base_task import TaskList
from task.settings import THREADS_COUNT,SLEEP
# from task import Task
import time

class ThreadParser(threading.Thread):

    def __init__(self, task_list:TaskList , task_send, task_exe_class, name):
        threading.Thread.__init__(self)
        self.name = name
        self.task_list = task_list
        self.task_send = task_send
        self.task_exe_class = task_exe_class
        self.task_exe = self.task_exe_class()

    def run(self):
        while True:
            task = self.task_list.get_tasks()
            if not task.isValid:
                break
                # time.sleep(300)
            try:
                self.task_exe.exe(task)
                self.task_send.exe(task)
                print(self.name, task, task.obj, sep=" | ")
            except:
                print("Ошибка при парсинге")
                traceback.print_exc()


    def before_start(self):
        self.task_exe.start()
        print(f"start - {self.name}")

    def end(self):
        self.task_exe.end()
        print(f"end - {self.name}")


class ThreadTaskExe(threading.Thread):

    def __init__(self, task_list, task_send, task_exe_class):
        threading.Thread.__init__(self)
        self.task_list = task_list
        self.task_send = task_send
        self.task_exe_class = task_exe_class
        # self.THREADS_COUNT = THREADS_COUNT
        self.threads_parser = []  # -> [ThreadParser]

    def run(self):
        for tp in self.threads_parser:
            tp.start()
            time.sleep(SLEEP)

        for tp in self.threads_parser:
            tp.join()

    def before_start(self):
        count = THREADS_COUNT if THREADS_COUNT else 1
        for c in range(count):
            name = f"-ThreadParser nr.{c}-"
            tp = ThreadParser(self.task_list, self.task_send, self.task_exe_class, name)
            self.threads_parser.append(tp)

        for tp in self.threads_parser:
            tp.before_start()
        print("start - ThreadTaskExe")

    def end(self):
        for tp in self.threads_parser:
            tp.end()
        print("end - ThreadTaskExe")


def print_date(threadName, counter):
    datefields = []
    today = datetime.date.today()
    datefields.append(today)
    print(
        "%s[%d]: %s" % (threadName, counter, datefields[0])
    )


if __name__ == '__main__':
    pass
    # threads = []
    # # Создать треды
    # thread1 = myThread("Thread", 1)
    # thread2 = myThread("Thread", 2)
    #
    # # Запустить треды
    # thread1.start()
    # thread2.start()
    #
    # # Добавить треды в список
    # threads.append(thread1)
    # threads.append(thread2)
    #
    # # Дождитесь завершения всех потоков
    # for t in threads:
    #     t.join()
    #
    # print("Exiting the Program!!!")
