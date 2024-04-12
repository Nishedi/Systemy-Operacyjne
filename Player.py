from Bullet import Bullet
from tkinter import PhotoImage
import random
import time
from Object import Object
import threading

class Player(Object):

    def __init__(self, canvas, x, y, objects, possition):
        super().__init__(possition[0], possition[1])
        self.size = 40
        self.score = 0
        self.ammo = 10
        self.canvas = canvas
        self.objects = objects
        self.player_image = PhotoImage(file="pictures/player_right.png")
        self.direction = 'Right'
        thread = threading.Thread(target=self.threadLoop, args=())
        thread.start()

    def add_score(self, score):
        self.score += score


    def show_yourself(self):
        if(self.direction == 'Up'):
            player_image = PhotoImage(file="pictures//player_up.png")
        elif(self.direction == 'Down'):
            player_image = PhotoImage(file="pictures//player_down.png")
        elif(self.direction == 'Left'):
            player_image = PhotoImage(file="pictures//player_left.png")
        elif(self.direction == 'Right'):
            player_image = PhotoImage(file="pictures//player_right.png")

        self.canvas.create_image(self.possition[0]*self.size, self.possition[1]*self.size, anchor='nw', image=player_image)
        self.canvas.player_image = player_image


    def add_ammo(self):
        self.ammo += 1

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            if self.direction == 'Right':
                bullet = Bullet(self.canvas, self.get_possition()[0]+1, self.get_possition()[1], self.direction, self.objects)
            if self.direction == 'Left':
                bullet = Bullet(self.canvas, self.get_possition()[0]-1, self.get_possition()[1], self.direction, self.objects)
            if self.direction == 'Up':
                bullet = Bullet(self.canvas, self.get_possition()[0], self.get_possition()[1]-1, self.direction, self.objects)
            if self.direction == 'Down':
                bullet = Bullet(self.canvas, self.get_possition()[0], self.get_possition()[1]+1, self.direction, self.objects)

    def get_score(self):
        return self.score

    def get_name(self):
        return self.name

    def threadLoop(self):
        while True:
            self.movePlayer(0)
            # self.show_yourself()
            time.sleep(0.1)
    def movePlayer(self, mode=1):
        collision = [0,0,0,0,0]
        for object in self.objects:
            if object is self:
                continue
            collision2 = self.checkCollision(object, self.direction)
            for i in range(5):
                if collision2[i]==1:
                    collision[i]=1
        if self.direction == 'Up' and collision[4]!=1:
            self.possition[1] -= 1
        if self.direction == 'Down' and collision[3]!=1:
            self.possition[1] += 1
        if self.direction == 'Left' and collision[2]!=1:
            self.possition[0] -= 1
        if self.direction == 'Right' and collision[1]!=1:
            self.possition[0] += 1
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

    def steerPlayer(self, event=None, mode=0):

        if event.keysym == 'Up' or event.keysym == 'Down' or event.keysym == 'Left' or event.keysym == 'Right':
            self.direction = event.keysym
        if event.keysym == 'space':
            self.shoot()



