from generator import Task



class TaskSend:
    def __init__(self, ):
        pass

    def exe(self, task: Task):
        print("===")
        # print(len(task.prices))
        print(task.__dict__)

        print("===")

    def start(self):
        print("start - TaskSend")

    def end(self):
        print("start - TaskSend")
