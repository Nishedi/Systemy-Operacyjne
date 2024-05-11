import threading
import time

from Enemy import Enemy
class ThreadMenager:
    def __init__(self, map):
        self.EnemyThreads = []
        self.allThreads = []
        self.mutex = threading.Lock()
        self.isRunning = True
        self.oderThreads = []
        self.bulletsDropperThread = threading.Thread(target=self.bulletsDropper, args=(map,))
        # self.bulletsDropperThread.start()
        self.mobSpawner = threading.Thread(target=self.mobSpawner, args=(map,))
        # self.mobSpawner.start()

        for i in range(10):
            self.add_thread(Enemy(map.findEmptyPlace(), map, self))


    def startThreads(self):
        for thread in self.allThreads:
            thread.startThread()
        self.bulletsDropperThread.start()
        self.mobSpawner.start()

    def mobSpawner(self, map):
        while not self.isRunning:
            try:
                map.mutex.acquire()
                self.add_thread(Enemy(map.findEmptyPlace(), map, self).startThread())
            finally:
                map.mutex.release()
            time.sleep(10)

    def bulletsDropper(self, map):
        while self.isRunning:
            try:
                map.mutex.acquire()
                possition = map.findEmptyPlace()
                map.update_map(possition[1], possition[0], 'A')
            finally:
                map.mutex.release()
            time.sleep(10)


    def add_thread(self, thread):
        try:
            self.mutex.acquire()
            self.EnemyThreads.append(thread)
            self.allThreads.append(thread)
        finally:
            self.mutex.release()

    def remove_thread(self, thread):
        try:
            self.mutex.acquire()
            self.EnemyThreads.remove(thread)
        finally:
            self.mutex.release()

    def closeAll(self):
        self.isRunning = False
        self.bulletsDropperThread.join()
        self.mobSpawner.join()
        for thread in self.allThreads:
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