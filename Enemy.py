import threading
import time
import random
from tkinter import PhotoImage

from Object import Object

class Enemy(Object):

    def __init__(self, canvas, objects, possition, map):
        super().__init__(possition[0], possition[1])
        self.directions = ['Up', 'Down', 'Left', 'Right']
        self.direction = self.directions[random.randint(0,3)]
        self.isRunning = True
        self.canvas = canvas
        self.objects = objects
        self.image = PhotoImage(file="pictures/mob.png")
        self.map = map
        thread = threading.Thread(target=self.threadLoop, args=())
        thread.start()

    def threadLoop(self):
        while self.isRunning:
            self.move()
            time.sleep(1)

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

        self.map[self.possition[1]][self.possition[0]] = 'E'
        if mode == 1 and collision[0] == 1:
            if collision[1] == 1:
                if collision[3] == 1:
                    self.setDirection(['Down', 'Right'])
                elif collision[4] == 1:
                    self.setDirection(['Up', 'Right'])
                else:
                    self.setDirection(['Right'])
            elif collision[2] == 1:
                if collision[3] == 1:
                    self.setDirection(['Left', 'Down'])
                elif collision[4] == 1:
                    self.setDirection(['Left', 'Up'])
                else:
                    self.setDirection(['Left'])
            else:
                if collision[3] == 1:
                    self.setDirection(['Down'])
                elif collision[4] == 1:
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
