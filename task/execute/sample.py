# from generator import Task
from task.generator.simple import Task


class TaskExe:

    def __init__(self):
        pass

    def exe(self, task) -> Task:
        import random
        for i in range(random.randint(10, 20)):
            task.add_price(random.randint(100, 200))
        return task

    def start(self):
        print("start - TaskExe")

    def end(self):
        print("end - TaskExe")


if __name__ == '__main__':
    pass
# for t in TaskList.get_tasks():
#     print(t.__dict__)
