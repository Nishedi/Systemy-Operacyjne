from Bullet import Bullet
from tkinter import PhotoImage
import time
import random
from Object import Object


class Player(Object):

    def __init__(self, threadMenager, possition, map):
        possition = (12, 10)
        super().__init__(possition[1], possition[0], map)
        self.score = 0
        self.ammo = 10
        self.threadMenager = threadMenager
        self.player_image = PhotoImage(file="pictures/player_right.png")
        self.letter = 'P'
        self.mapObject.update_map(self.possition[0], self.possition[1], self.letter)
        self.direction = 'Right'
        self.spawn()
        self.thread.start()


    def add_score(self, score):
        self.score += score
    def spawn(self):
        try:
            self.mapObject.mutex.acquire()
            possition = self.mapObject.findEmptyPlace()
            self.possition[0], self.possition[1] = possition[1], possition[0]
            self.mapObject.update_map(self.possition[0], self.possition[1], self.letter)
        finally:
            self.mapObject.mutex.release()
    def changePhotoDirection(self):
        if (self.direction == 'Up'):
            self.player_image = PhotoImage(file="pictures//player_up.png")
        elif (self.direction == 'Down'):
            self.player_image = PhotoImage(file="pictures//player_down.png")
        elif (self.direction == 'Left'):
            self.player_image = PhotoImage(file="pictures//player_left.png")
        elif (self.direction == 'Right'):
            self.player_image = PhotoImage(file="pictures//player_right.png")


    def add_ammo(self):
        self.ammo += 1

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            if self.direction == 'Right':
                Bullet(self.get_possition()[0]+1, self.get_possition()[1], self.direction, self.threadMenager, self.mapObject)
            if self.direction == 'Left':
                Bullet(self.get_possition()[0]-1, self.get_possition()[1], self.direction, self.threadMenager, self.mapObject)
            if self.direction == 'Up':
                Bullet(self.get_possition()[0], self.get_possition()[1]-1, self.direction, self.threadMenager, self.mapObject)
            if self.direction == 'Down':
                Bullet(self.get_possition()[0], self.get_possition()[1]+1, self.direction, self.threadMenager, self.mapObject)

    def get_score(self):
        return self.score

    def threadLoop(self):
        while self.isRunning:
            self.move(0)
            time.sleep(0.5)




    def steerPlayer(self, event=None):
        if event.keysym == 'Up' or event.keysym == 'Down' or event.keysym == 'Left' or event.keysym == 'Right':
            self.direction = event.keysym
            self.changePhotoDirection()

        if event.keysym == 'space':
            self.shoot()



