import datetime
import time



# from tasks import TaskList

from task import TaskSend
from task import ThreadTaskExe
from task.generator.base_task import TaskList, BaseTask as Task
from task.parser.parser_base_tast import TaskExe


# from tasks.result.sample import TaskSend

def start() -> (TaskList, ThreadTaskExe, TaskSend):
    task_list = TaskList()
    task_send = TaskSend()
    task_send.start()
    task_list.start()
    task_exe = ThreadTaskExe(task_list, task_send, TaskExe)
    task_exe.before_start()
    return task_list, task_exe, task_send


def end(task_list: TaskList, task_exe: ThreadTaskExe, task_send: TaskSend, ):
    task_list.end()
    task_exe.end()
    task_send.end()


def work(task_list: TaskList, task_exe: ThreadTaskExe, task_send: TaskSend, ):
    print(datetime.datetime.now(), "Start")

    task_exe.start()
    task_exe.join()

    print(datetime.datetime.now(), "End")


def main():
    task_list, task_exe, task_send = start()
    work(task_list, task_exe, task_send)
    end(task_list, task_exe, task_send)


if __name__ == '__main__':
    main()
