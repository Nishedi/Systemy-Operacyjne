from Bullet import Bullet
from tkinter import PhotoImage
import time
import random
from Object import Object


class Player(Object):

    def __init__(self, objects, possition, map):
        possition = (1, 10)
        super().__init__(possition[1], possition[0], map)
        self.score = 0
        self.ammo = 10
        self.objects = objects
        self.player_image = PhotoImage(file="pictures/player_right.png")
        self.letter = 'P'
        self.map[self.possition[1]][self.possition[0]] = self.letter
        self.direction = 'Left'

        self.thread.start()


    def add_score(self, score):
        self.score += score

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
                bullet = Bullet(self.get_possition()[0]+1, self.get_possition()[1], self.direction, self.objects, self.map)
            if self.direction == 'Left':
                bullet = Bullet(self.get_possition()[0]-1, self.get_possition()[1], self.direction, self.objects, self.map)
            if self.direction == 'Up':
                bullet = Bullet(self.get_possition()[0], self.get_possition()[1]-1, self.direction, self.objects, self.map)
            if self.direction == 'Down':
                bullet = Bullet(self.get_possition()[0], self.get_possition()[1]+1, self.direction, self.objects, self.map)

    def get_score(self):
        return self.score

    def get_name(self):
        return self.name

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



