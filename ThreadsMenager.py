import threading
from Enemy import Enemy
class ThreadMenager:
    def __init__(self, map):
        self.threads = []
        self.mutex = threading.Lock()
        for i in range(10):
            self.add_thread(Enemy(map.findEmptyPlace(), map))


    def add_thread(self, thread):
        try:
            self.mutex.acquire()
            self.threads.append(thread)
        finally:
            self.mutex.release()

    def remove_thread(self, thread):
        try:
            self.mutex.acquire()
            print("Trying to remove thread...")
            self.threads.remove(thread)
        finally:
            self.mutex.release()

    def closeAll(self):
        for thread in self.threads:
            thread.isRunning = False
            thread.thread.join()

    def checkHitting(self, possition):
        try:
            self.mutex.acquire()
            print(1)
            objectToRemove = None
            for object in self.threads:
                if object.get_possition() == possition:
                    object.isRunning = False
                    self.isRunning = False
                    objectToRemove = object
            if objectToRemove != None:
                self.remove_thread(objectToRemove)
        except:
            print("some error")
        finally:
            print(2)
            self.mutex.release()