import random
import threading
import time
class Object:
    def __init__(self, x, y, map):
        self.possition = [x, y]
        self.mapObject = map
        self.map = self.mapObject.map
        self.isRunning = True
        self.thread = threading.Thread(target=self.threadLoop, args=())
        self.mutex = threading.Lock()


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



    def checkCollision2(self, map, direction):
        a = self.possition
        res = [0,0,0,0,0]
        objectsToCheck = ['X', 'E', 'P']

        right = self.mapObject.get_what_is_in(a[0]+1, a[1])
        left = self.mapObject.get_what_is_in(a[0]-1, a[1])
        up = self.mapObject.get_what_is_in(a[0], a[1]-1)
        down = self.mapObject.get_what_is_in(a[0], a[1]+1)
        if right == 'X' or right == 'E' or right == 'P':
            if direction == 'Right':
                res[0] = 1
                res[1] = 1
        if left == 'X' or left == 'E' or left == 'P':
            if direction == 'Left':
                res[0] = 1
                res[2] = 1
        if up == 'X' or up == 'E' or up == 'P':
            if direction == 'Up':
                res[0] = 1
                res[4] = 1
        if down == 'X' or down == 'E' or down == 'P':
            if direction == 'Down':
                res[0] = 1
                res[3] = 1



        return res
    def move(self, mode=1):
        collision = self.checkCollision2(self.map, self.direction)
        try:
            self.mutex.acquire()
            if collision[0]==0:
                self.mapObject.update_map(self.possition[0], self.possition[1], ' ')
            if self.direction == 'Up' and collision[4]!=1:
                self.possition[1] -= 1
            if self.direction == 'Down' and collision[3]!=1:
                self.possition[1] += 1
            if self.direction == 'Left' and collision[2]!=1:
                self.possition[0] -= 1
            if self.direction == 'Right' and collision[1]!=1:
                self.possition[0] += 1
            self.map[self.possition[1]][self.possition[0]] = self.letter
        finally:
            self.mutex.release()
        if mode == 1 and collision[0]==1:
            if collision[1]==1:
                if collision[3]==1:
                    self.setDirection(['Down','Right'])
                elif collision[4]==1:
                    self.setDirection(['Up','Right'])
                else:
                    self.setDirection(['Right'])
            elif collision[2]==1:
                if collision[3]==1:
                    self.setDirection(['Left', 'Down'])
                elif collision[4]==1:
                    self.setDirection(['Left','Up'])
                else:
                    self.setDirection(['Left'])
            else:
                if collision[3]==1:
                    self.setDirection(['Down'])
                elif collision[4]==1:
                    self.setDirection(['Up'])
                else:
                    self.setDirection(['Right'])
        elif mode == 1 and random.randint(0, 5) == 0:
            self.setDirection([])
    def setDirection(self, forbidden_directions):
        if len(forbidden_directions) == 4:
            return
        self.direction = random.choice(["Up", "Down", "Left", "Right"])
        while self.direction in forbidden_directions:
            self.direction = random.choice(["Up", "Down", "Left", "Right"])