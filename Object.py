import random
import threading
import time
class Object:
    def __init__(self, map):
        self.possition = [0, 0] # possition of the object
        self.mapObject = map # map object
        self.map = self.mapObject.map # map - 2D list
        self.isRunning = True # is thread active
        self.thread = threading.Thread(target=self.threadLoop, args=()) # thread
        self.mutex = threading.Lock() # mutex

    def startThread(self):
        self.thread.start() # start thread

    def spawn(self): # spawn object on the map
        try:
            self.mapObject.mutex.acquire() # lock the mutex
            possition = self.mapObject.findEmptyPlace() # find empty place
            self.possition[0], self.possition[1] = possition[1], possition[0] #assaing new possition
            self.mapObject.update_map(self.possition[0], self.possition[1], self.letter) # update map
        finally: # no matter what unlock the mutex
            self.mapObject.mutex.release()

    def get_possition(self): # get possition of the object
        try:
            self.mutex.acquire() # lock the mutex
            possition = [self.possition[0], self.possition[1]] # get possition
        finally:
            self.mutex.release() # no matter what unlock the mutex
        return possition # return possition

    def threadLoop(self): # main loop of the object thread
        while self.isRunning:
            pass

    def move(self):
        pass