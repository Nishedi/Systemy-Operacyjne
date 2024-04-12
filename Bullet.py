import threading
from Object import Object
import time
class Bullet(Object):
    def __init__(self, canva, x, y, direction, objects):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.direction = direction
        self.canvas = canva
        self.rectangle = self.canvas.create_rectangle(self.x, self.y, self.x+2, self.y+2, fill="black")
        self.objects = objects
        objects.append(self)
        self.thread = threading.Thread(target=self.threadLoop, args=())
        self.isRunning = True
        self.thread.start()

    def threadLoop(self):
        while self.isRunning:
            print(self.possition)
            # self.show_yourself()
            self.move()

            time.sleep(0.1)

    def show_yourself(self):
        self.canvas.delete(self.rectangle)
        self.rectangle = self.canvas.create_rectangle(self.possition[0]*40, self.possition[1]*40, self.possition[0]*40+40, self.possition[1]*40+40, fill="black")
    def move(self):
        collision = [0, 0, 0, 0, 0]
        for object in self.objects:
            if object is self:
                continue
            collision2 = self.checkCollision(object, self.direction)
            for i in range(5):
                if collision2[i] == 1:
                    collision[i] = 1
        if collision[0] == 1:
            self.isRunning = False

        if collision[0] == 0:
            self.possitionChanged = True
        if self.direction == 'Up' and collision[4] != 1:
            self.possition[1] -= 1
        if self.direction == 'Down' and collision[3] != 1:
            self.possition[1] += 1
        if self.direction == 'Left' and collision[2] != 1:
            self.possition[0] -= 1
        if self.direction == 'Right' and collision[1] != 1:
            self.possition[0] += 1



