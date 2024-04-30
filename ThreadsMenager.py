import threading
import time

from Enemy import Enemy
class ThreadMenager:
    def __init__(self, map):
        self.EnemyThreads = []
        self.allThreads = []
        self.mutex = threading.Lock()
        self.isRunning = True
        self.bulletsDropperThread = threading.Thread(target=self.bulletsDropper, args=(map,))
        self.bulletsDropperThread.start()
        # for i in range(10):
        #     self.add_thread(Enemy(map.findEmptyPlace(), map))

    def bulletsDropper(self, map):
        while self.isRunning:
            map.mutex.acquire()
            possition = map.findEmptyPlace()
            map.update_map(possition[1], possition[0], 'A')
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