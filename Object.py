import random
import threading
import time
class Object:
    def __init__(self, map):
        self.possition = [0, 0]
        self.mapObject = map
        self.map = self.mapObject.map
        self.isRunning = True
        self.thread = threading.Thread(target=self.threadLoop, args=())
        self.mutex = threading.Lock()

    def startThread(self):
        self.thread.start()

    def spawn(self):
        try:
            self.mapObject.mutex.acquire()
            possition = self.mapObject.findEmptyPlace()
            self.possition[0], self.possition[1] = possition[1], possition[0]
            self.mapObject.update_map(self.possition[0], self.possition[1], self.letter)
        finally:
            self.mapObject.mutex.release()

    def get_possition(self):
        try:
            self.mutex.acquire()
            possition = [self.possition[0], self.possition[1]]
        finally:
            self.mutex.release()
        return possition

    def threadLoop(self):
        while self.isRunning:
            pass

    def move(self):
        pass