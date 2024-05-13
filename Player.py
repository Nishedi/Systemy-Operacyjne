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
        self.direction = 'Right'
        self.spawn()

    def addOneScore(self):
        try:
            self.mutex.acquire()
            self.score += 1
        finally:
            self.mutex.release()
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
            if self.direction == 'Right' and self.mapObject.get_what_is_in(self.possition[0]+1, self.possition[1]) == ' ':
                Bullet(self.get_possition()[0]+1, self.get_possition()[1], self.direction, self.threadMenager, self.mapObject, self)
                self.ammo -= 1
            if self.direction == 'Left' and self.mapObject.get_what_is_in(self.possition[0]-1, self.possition[1]) == ' ':
                Bullet(self.get_possition()[0]-1, self.get_possition()[1], self.direction, self.threadMenager, self.mapObject, self)
                self.ammo -= 1
            if self.direction == 'Up' and self.mapObject.get_what_is_in(self.possition[0], self.possition[1]-1) == ' ':
                Bullet(self.get_possition()[0], self.get_possition()[1]-1, self.direction, self.threadMenager, self.mapObject, self)
                self.ammo -= 1
            if self.direction == 'Down' and self.mapObject.get_what_is_in(self.possition[0], self.possition[1]+1) == ' ':
                Bullet(self.get_possition()[0], self.get_possition()[1]+1, self.direction, self.threadMenager, self.mapObject, self)
                self.ammo -= 1

    def get_score(self):
        return self.score

    def threadLoop(self):
        while self.isRunning:
            self.move()
            time.sleep(0.5)
        print("End of the game!")

    def checkCollision(self, map, direction):
        a = self.possition
        res = [0,0,0,0,0]
        whatIsHere = ' '
        right = self.mapObject.get_what_is_in(a[0]+1, a[1])
        left = self.mapObject.get_what_is_in(a[0]-1, a[1])
        up = self.mapObject.get_what_is_in(a[0], a[1]-1)
        down = self.mapObject.get_what_is_in(a[0], a[1]+1)
        if right == 'X' or right == 'E':
            if direction == 'Right':
                whatIsHere = right
                res[0] = 1
                res[1] = 1
        if left == 'X' or left == 'E':
            if direction == 'Left':
                whatIsHere = left
                res[0] = 1
                res[2] = 1
        if up == 'X' or up == 'E':
            if direction == 'Up':
                whatIsHere = up
                res[0] = 1
                res[4] = 1
        if down == 'X' or down == 'E':
            if direction == 'Down':
                whatIsHere = down
                res[0] = 1
                res[3] = 1
        if whatIsHere == 'E':
            self.threadMenager.closeAll()
        return res

    def checkMap(self):
        if self.mapObject.get_what_is_in(self.possition[0], self.possition[1]) == 'A':
            self.add_ammo()
    def move(self):
        try:
            self.mapObject.mutex.acquire()
            collision = self.checkCollision(self.map, self.direction)
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
            self.checkMap()
            self.mapObject.update_map(self.possition[0], self.possition[1], self.letter)

        finally:
            self.mapObject.mutex.release()


    def steerPlayer(self, event=None):
        if event.keysym == 'Up' or event.keysym == 'Down' or event.keysym == 'Left' or event.keysym == 'Right':
            self.direction = event.keysym
            self.changePhotoDirection()
        if event.keysym == 'space':
            self.shoot()
