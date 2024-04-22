import threading
from Object import Object
import time
class Bullet(Object):
    def __init__(self, x, y, direction, objects, map):
        super().__init__(x, y, map)
        self.direction = direction

        self.objects = objects
        self.map[self.possition[1]][self.possition[0]] = 'B'
        self.thread.start()


    def threadLoop(self):
        while self.isRunning:
            self.move()
            time.sleep(0.1)

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
            self.map[self.possition[1]][self.possition[0]] = ' '
        self.checkHitting()

    def checkHitting(self):
        for object in self.objects:
            if object.get_possition() == self.possition:
                object.isRunning = False
                self.isRunning = False
                self.map[self.possition[1]][self.possition[0]] = ' '
                self.objects.remove(object)



