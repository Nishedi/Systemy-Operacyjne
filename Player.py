from Bullet import Bullet
from tkinter import PhotoImage
import time
from Object import Object


class Player(Object):
    def __init__(self, threadMenager, map):
        super().__init__(map)
        self.score = 0  # Score of the player
        self.ammo = 10  # Ammo of the player - default 10
        self.threadMenager = threadMenager  # ThreadMenager object to stop the game
        self.player_image = PhotoImage(file="pictures/player_right.png")  # Photo of the player
        self.letter = 'P'  # Letter which represent player on the map
        self.direction = 'Right'  # Default - start direction
        self.spawn()  # Spawn player on the map

    def addOneScore(self):  # Add one score
        try:
            self.mutex.acquire()  # Lock the mutex
            self.score += 1  # Add one score
        finally:
            self.mutex.release()  # No matter what unlock the mutex

    def add_score(self, score):
        self.score += score  # Add score

    def changePhotoDirection(self):  #change photo depend of direction he is going
        if (self.direction == 'Up'):
            self.player_image = PhotoImage(file="pictures//player_up.png")
        elif (self.direction == 'Down'):
            self.player_image = PhotoImage(file="pictures//player_down.png")
        elif (self.direction == 'Left'):
            self.player_image = PhotoImage(file="pictures//player_left.png")
        elif (self.direction == 'Right'):
            self.player_image = PhotoImage(file="pictures//player_right.png")

    def add_ammo(self):  # Add ammo
        self.ammo += 1

    def shoot(self):  # Shoot
        if self.ammo > 0:
            if self.direction == 'Right' and not self.mapObject.get_what_is_in(self.possition[0] + 1, self.possition[
                1]) == 'X':  # if there is no wall on the right
                Bullet(self.get_possition()[0] + 1, self.get_possition()[1], self.direction, self.threadMenager,
                       self.mapObject, self)  # create bullet thread
                self.ammo -= 1
            if self.direction == 'Left' and not self.mapObject.get_what_is_in(self.possition[0] - 1, self.possition[
                1]) == 'X':  # if there is no wall on the left
                Bullet(self.get_possition()[0] - 1, self.get_possition()[1], self.direction, self.threadMenager,
                       self.mapObject, self)  # create bullet thread
                self.ammo -= 1
            if self.direction == 'Up' and not self.mapObject.get_what_is_in(self.possition[0], self.possition[
                                                                                                   1] - 1) == 'X':  # if there is no wall up
                Bullet(self.get_possition()[0], self.get_possition()[1] - 1, self.direction, self.threadMenager,
                       self.mapObject, self)  # create bullet thread
                self.ammo -= 1
            if self.direction == 'Down' and not self.mapObject.get_what_is_in(self.possition[0], self.possition[
                                                                                                     1] + 1) == 'X':  # if there is no wall down
                Bullet(self.get_possition()[0], self.get_possition()[1] + 1, self.direction, self.threadMenager,
                       self.mapObject, self)  # create bullet thread
                self.ammo -= 1

    def get_score(self):
        return self.score

    def threadLoop(self):  # Main loop of the player thread
        while self.isRunning:
            self.move()
            time.sleep(0.5)
        print("End of the game!")

    def checkCollision(self, map, direction):  # Check if there is any collision
        a = self.possition
        res = [0, 0, 0, 0, 0]
        whatIsHere = ' '
        right = self.mapObject.get_what_is_in(a[0] + 1, a[1])
        left = self.mapObject.get_what_is_in(a[0] - 1, a[1])
        up = self.mapObject.get_what_is_in(a[0], a[1] - 1)
        down = self.mapObject.get_what_is_in(a[0], a[1] + 1)
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

    def checkMap(self):  # Check if there is a bullet on the map
        if self.mapObject.get_what_is_in(self.possition[0], self.possition[1]) == 'A':
            self.add_ammo()

    def move(self): # Move player
        try:
            self.mapObject.mutex.acquire() # Lock the mutex
            collision = self.checkCollision(self.map, self.direction) # Check if there is any collision
            self.checkMap() # Check if there is a bullet on the map
            if collision[0] == 0: # If there is no collision
                self.mapObject.update_map(self.possition[0], self.possition[1], ' ')
            if self.direction == 'Up' and collision[4] != 1: # If player is going up and there is no collision up
                self.possition[1] -= 1
            if self.direction == 'Down' and collision[3] != 1: #...
                self.possition[1] += 1
            if self.direction == 'Left' and collision[2] != 1:
                self.possition[0] -= 1
            if self.direction == 'Right' and collision[1] != 1:
                self.possition[0] += 1
            self.mapObject.update_map(self.possition[0], self.possition[1], self.letter) # Update map

        finally:
            self.mapObject.mutex.release() # Release the mutex

    def steerPlayer(self, event=None):
        if event.keysym == 'Up' or event.keysym == 'Down' or event.keysym == 'Left' or event.keysym == 'Right':
            self.direction = event.keysym
            self.changePhotoDirection()
        if event.keysym == 'space':
            self.shoot()
