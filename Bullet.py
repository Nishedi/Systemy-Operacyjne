import threading
from Object import Object
import time
from Enemy import Enemy
class Bullet(Object):
    def __init__(self, x, y, direction, threadMenager, map, player):
        super().__init__(x, y, map)
        self.direction = direction
        self.threadMenager = threadMenager
        self.mapObject.update_map(self.possition[0], self.possition[1], 'B')
        self.player = player
        self.thread.start()



    def threadLoop(self):
        self.checkCollisionEnemy()
        while self.isRunning:
            self.move()
            time.sleep(0.1)

    def checkCollision(self, map, direction):
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

    def checkCollisionEnemy(self):
        if self.threadMenager.checkHitting(self.possition):
            self.mapObject.update_map(self.possition[0], self.possition[1], ' ')
            self.player.addOneScore()
            self.isRunning = False
            return True

    def move(self, mode=1):
        try:
            self.mapObject.mutex.acquire()
            collision = self.checkCollision(self.map, self.direction)
            self.mapObject.update_map(self.possition[0], self.possition[1], ' ')
            if self.direction == 'Up' and collision[4] != 1:
                self.possition[1] -= 1
            if self.direction == 'Down' and collision[3] != 1:
                self.possition[1] += 1
            if self.direction == 'Left' and collision[2] != 1:
                self.possition[0] -= 1
            if self.direction == 'Right' and collision[1] != 1:
                self.possition[0] += 1
            if self.checkCollisionEnemy():
                return
            if collision[0] == 1:
                self.mapObject.update_map(self.possition[0], self.possition[1], ' ')
                self.isRunning = False
                return
            self.mapObject.update_map(self.possition[0], self.possition[1], 'B')
        finally:
            self.mapObject.mutex.release()
