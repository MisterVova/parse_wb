import datetime
import time

# from execute import TaskExe
# from generator import TaskList
# from result import TaskSend

from task import TaskExe
from task import TaskList
from task import TaskSend


def start() -> (TaskList, TaskExe, TaskSend):
    task_list = TaskList()
    task_exe = TaskExe()
    task_send = TaskSend()
    task_list.start()
    task_exe.start()
    task_send.start()
    return (task_list, task_exe, task_send)


def end(task_list: TaskList, task_exe: TaskExe, task_send: TaskSend, ):
    task_list.end()
    task_exe.end()
    task_send.end()


def work(task_list: TaskList, task_exe: TaskExe, task_send: TaskSend, ):
    print(datetime.datetime.now(), "Start")

    steep = 0
    for task in task_list.get_tasks():
        print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
        print(datetime.datetime.now(), "Steep", steep, "Start", sep=": ")
        print(task.url)
        # try:
        task_exe.exe(task)
        # except Exception:
        #     pass
        task_send.exe(task)

        # print(task.__dict__)
        print(datetime.datetime.now(), "Steep", steep, "Finish", sep=": ")
        steep += 1
        if steep > 10:
            break
        # time.sleep(1)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print()
    print(datetime.datetime.now(), "End")


def main():
    task_list, task_exe, task_send = start()
    work(task_list, task_exe, task_send)
    end(task_list, task_exe, task_send)


if __name__ == '__main__':
    main()
