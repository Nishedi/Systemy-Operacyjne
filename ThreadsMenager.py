import threading
from Enemy import Enemy
class ThreadMenager:
    def __init__(self, map):
        self.EnemyThreads = []
        self.allThreads = []
        self.mutex = threading.Lock()
        for i in range(10):
            self.add_thread(Enemy(map.findEmptyPlace(), map))


    def add_thread(self, thread):
        try:
            self.mutex.acquire()
            self.EnemyThreads.append(thread)
        finally:
            self.mutex.release()

    def remove_thread(self, thread):
        try:
            self.mutex.acquire()
            self.EnemyThreads.remove(thread)
        finally:
            self.mutex.release()

    def closeAll(self):
        for thread in self.EnemyThreads:
            thread.isRunning = False
            thread.thread.join()

    def checkHitting(self, possition):
        try:
            self.mutex.acquire()
            for object in self.EnemyThreads:
                if object.get_possition() == possition:
                    object.isRunning = False
                    self.isRunning = False
                    self.EnemyThreads.remove(object)
                    return True
            return False
        finally:
            self.mutex.release()