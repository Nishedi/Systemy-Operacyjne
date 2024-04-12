import threading
import time
from random import random
from tkinter import PhotoImage

from Object import Object

class Enemy(Object):

    def __init__(self, canvas, objects, possition):
        super().__init__(possition[0], possition[1])
        self.directions = ['Up', 'Down', 'Left', 'Right']
        self.direction = self.directions[int(random()*4)]
        self.isRunning = True
        self.canvas = canvas
        self.objects = objects
        self.image = PhotoImage(file="pictures/mob.png")
        thread = threading.Thread(target=self.threadLoop, args=())
        thread.start()

    def show_yourself(self):
        # self.canvas.create_image(self.possition[0]*40, self.possition[1]*40, anchor='nw', image=self.image)
        # self.canvas.mob_image = self.image
        pass

    def threadLoop(self):
        while self.isRunning:
            self.show_yourself()
            self.move()
            time.sleep(1)

    def move(self):
        collision = [0, 0, 0, 0, 0]
        for object in self.objects:
            if object is self:
                continue
            collision2 = self.checkCollision(object, self.direction)
            for i in range(5):
                if collision2[i] == 1:
                    collision[i] = 1
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
        if collision[0] == 1:
            pass
