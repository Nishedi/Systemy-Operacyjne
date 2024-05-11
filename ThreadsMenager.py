import threading
import time

from Enemy import Enemy
class ThreadMenager:
    def __init__(self, map):
        self.EnemyThreads = [] # this is a list of all enemies nothing more
        self.allThreads = [] # this is a list of all threads that are running to control all game
        self.mutex = threading.Lock() # this is a lock that will be used to protect the list of threads
        self.isRunning = True # this is a flag that will be used to stop all threads (including this)
        self.bulletsDropperThread = threading.Thread(target=self.bulletsDropper, args=(map,)) #this is a thread that will drop bullets
        self.bulletDropperStatus = 0 # 0 - not dropping
        self.bulletsDropperPeriod = 5 # when dropperStatus reach 5, it will drop bullet
        self.mobSpawner = threading.Thread(target=self.mobSpawner, args=(map,)) # this is a thread that will spawn enemies
        self.mobSpawnerPeriod = 10 # same as above
        self.mobSpawnerStatus = 0
        self.startTime = time.time()

    def setDifficulty(self, difficulty): # this is a method that will set difficulty of the game
        if difficulty == 0:
            self.bulletsDropperPeriod = 5
            self.mobSpawnerPeriod = 10
        if difficulty == 1:
            self.bulletsDropperPeriod = 7
            self.mobSpawnerPeriod = 7
        if difficulty == 2:
            self.bulletsDropperPeriod = 10
            self.mobSpawnerPeriod = 5

    def startThreads(self): # this method will start all threads = start the game
        for thread in self.allThreads:
            thread.startThread()
        self.bulletsDropperThread.start()
        self.mobSpawner.start()

    def mobSpawner(self, map): # this is a method that will spawn enemies used in mobSpawner thread
        incrementer = 1
        while self.isRunning:
            if time.time()-self.startTime>30*incrementer:
                incrementer+=1
                self.mobSpawnerPeriod-=1
            self.mobSpawnerStatus = 0
            while self.mobSpawnerStatus < self.mobSpawnerPeriod:
                time.sleep(1)
                self.mobSpawnerStatus += 1
            enemy = Enemy((0, 0), map, self)
            enemy.startThread()
            self.add_thread(enemy)

    def bulletsDropper(self, map): # this is a method that will drop bullets used in bulletsDropper thread
        while self.isRunning:
            self.bulletDropperStatus = 0
            while self.bulletDropperStatus < self.bulletsDropperPeriod:
                time.sleep(1)
                self.bulletDropperStatus += 1
            try:
                map.mutex.acquire()
                possition = map.findEmptyPlace()
                if possition:
                    map.update_map(possition[1], possition[0], 'A')
            finally:
                map.mutex.release()

    def add_thread(self, thread): # this is a method that will add thread to the list of threads keeping the list safe
        try:
            self.mutex.acquire()
            self.EnemyThreads.append(thread)
            self.allThreads.append(thread)
        finally:
            self.mutex.release()

    def remove_thread(self, thread): # this is a method that will remove thread from the list of threads keeping the list safe
        try:
            self.mutex.acquire()
            self.EnemyThreads.remove(thread)
        finally:
            self.mutex.release()

    def closeAll(self): # this is a method that will stop all threads = end the game
        self.isRunning = False
        self.bulletsDropperThread.join()
        self.mobSpawner.join()
        for thread in self.allThreads:
            thread.isRunning = False
            thread.thread.join()

    def checkHitting(self, possition): # this is a method that will check if bullet hit an enemy
        try:
            self.mutex.acquire()
            for object in self.EnemyThreads:
                if object.get_possition() == possition:
                    object.isRunning = False
                    self.EnemyThreads.remove(object)
                    return True
            return False
        finally:
            self.mutex.release()