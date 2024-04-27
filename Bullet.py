import threading
from Object import Object
import time
from Enemy import Enemy
class Bullet(Object):
    def __init__(self, x, y, direction, threadMenager, map):
        super().__init__(x, y, map)
        self.direction = direction
        self.threadMenager = threadMenager
        self.map[self.possition[1]][self.possition[0]] = 'B'
        self.thread.start()


    def threadLoop(self):
        while self.isRunning:
            self.move()
            time.sleep(0.1)
        self.map[self.possition[1]][self.possition[0]] = ' '

    def checkCollision2(self, map, direction):
        a = self.possition
        res = [0,0,0,0,0]

        right = self.mapObject.get_what_is_in(a[0]+1, a[1])
        left = self.mapObject.get_what_is_in(a[0]-1, a[1])
        up = self.mapObject.get_what_is_in(a[0], a[1]-1)
        down = self.mapObject.get_what_is_in(a[0], a[1]+1)
        if right == 'X' :
            if direction == 'Right':
                res[0] = 1
                res[1] = 1
        if left == 'X':
            if direction == 'Left':
                res[0] = 1
                res[2] = 1
        if up == 'X' :
            if direction == 'Up':
                res[0] = 1
                res[4] = 1
        if down == 'X':
            if direction == 'Down':
                res[0] = 1
                res[3] = 1
        return res
    def move(self, mode=1):
        collision = self.checkCollision2(self.map, self.direction)
        if collision[0] == 0:
            self.map[self.possition[1]][self.possition[0]] = ' '
        if self.direction == 'Up' and collision[4] != 1:
            self.possition[1] -= 1
        if self.direction == 'Down' and collision[3] != 1:
            self.possition[1] += 1
        if self.direction == 'Left' and collision[2] != 1:
            self.possition[0] -= 1
        if self.direction == 'Right' and collision[1] != 1:
            self.possition[0] += 1
        self.map[self.possition[1]][self.possition[0]] = 'B'
        if collision[0] == 1:
            self.isRunning = False

        self.threadMenager.checkHitting(self.possition)
