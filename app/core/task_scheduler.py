import threading
from queue import Queue


class TaskScheduler:
    def __init__(self, log):
        self.queue = Queue()
        self.log = log

    def add(self, task):
        self.queue.put(task)

    def start(self, worker):
        def run():
            while not self.queue.empty():
                task = self.queue.get()
                worker(task)

            self.log("🏁 downloads finalizados")

        threading.Thread(target=run, daemon=True).start()