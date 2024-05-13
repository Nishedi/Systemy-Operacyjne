"""
This file contains the Player class which is responsible for the player object in the game.
"""
import time
from tkinter import PhotoImage
from object import Object
from bullet import Bullet

class Player(Object):
    """
    Class which represent player object in the game.
    """
    def __init__(self, thread_menager, map2d):
        """
        Initialize Player object.
        """
        super().__init__(map2d)
        self.score = 0  # Score of the player
        self.ammo = 10  # Ammo of the player - default 10
        self.thread_menager = thread_menager  # ThreadMenager object to stop the game
        self.player_image = PhotoImage(file="pictures/player_right.png")  # Photo of the player
        self.letter = 'P'  # Letter which represent player on the map
        self.direction = 'Right'  # Default - start direction
        self.spawn()  # Spawn player on the map

    def add_one_score(self):
        """
        Add one to score.
        """
        with self.mutex:  # Lock the mutex
            self.score += 1

    def change_photo_direction(self):
        """
        Change photo depend of direction he is going.
        """
        if self.direction == 'Up':
            self.player_image = PhotoImage(file="pictures//player_up.png")
        elif self.direction == 'Down':
            self.player_image = PhotoImage(file="pictures//player_down.png")
        elif self.direction == 'Left':
            self.player_image = PhotoImage(file="pictures//player_left.png")
        elif self.direction == 'Right':
            self.player_image = PhotoImage(file="pictures//player_right.png")

    def add_ammo(self):
        """
        Add ammo.
        """
        self.ammo += 1

    def shoot(self):
        """
        Function to shoot.
        """
        if self.ammo > 0:
            # if there is no wall on the right
            if (self.direction == 'Right' and (not
                    self.map_object.get_what_is_in(self.possition[0] + 1,
                                                   self.possition[1]) == 'X')):
                Bullet(self.get_possition()[0] + 1, self.get_possition()[1],
                       self.direction, self.thread_menager, self.map_object, self)
                self.ammo -= 1
            if (self.direction == 'Left' and
                    not self.map_object.get_what_is_in(self.possition[0] - 1,
                                                       self.possition[ 1]) == 'X'):
                Bullet(self.get_possition()[0] - 1, self.get_possition()[1],
                       self.direction, self.thread_menager, self.map_object, self)
                self.ammo -= 1
            if (self.direction == 'Up' and
                    not self.map_object.get_what_is_in(self.possition[0],
                                                       self.possition[1] - 1) == 'X'):
                Bullet(self.get_possition()[0], self.get_possition()[1] - 1,
                       self.direction, self.thread_menager, self.map_object, self)
                self.ammo -= 1
            if (self.direction == 'Down' and
                    not self.map_object.get_what_is_in(self.possition[0],
                                                       self.possition[1] + 1) == 'X'):
                Bullet(self.get_possition()[0], self.get_possition()[1] + 1,
                       self.direction, self.thread_menager, self.map_object, self)
                self.ammo -= 1

    def thread_loop(self):
        """
        Main loop of the player thread.
        """
        while self.is_running:
            self.move()
            time.sleep(0.5)
        print("End of the game!")

    def check_collision(self, direction):  # Check if there is any collision
        """
        Function to check if there is any collision.
        """
        a = self.possition
        res = [0, 0, 0, 0, 0]
        what_is_here = ' '
        right = self.map_object.get_what_is_in(a[0] + 1, a[1])
        left = self.map_object.get_what_is_in(a[0] - 1, a[1])
        up = self.map_object.get_what_is_in(a[0], a[1] - 1)
        down = self.map_object.get_what_is_in(a[0], a[1] + 1)
        if right in ('X', 'E'):
            if direction == 'Right':
                what_is_here = right
                res[0] = 1
                res[1] = 1
        if left in ('X', 'E'):
            if direction == 'Left':
                what_is_here = left
                res[0] = 1
                res[2] = 1
        if up in ('X', 'E'):
            if direction == 'Up':
                what_is_here = up
                res[0] = 1
                res[4] = 1
        if down in ('X', 'E'):
            if direction == 'Down':
                what_is_here = down
                res[0] = 1
                res[3] = 1
        if what_is_here == 'E':
            self.thread_menager.close_all()
        return res

    def check_map(self):
        """
        Check if there is a bullet on the map.
        """
        if self.map_object.get_what_is_in(self.possition[0], self.possition[1]) == 'A':
            self.add_ammo()

    def move(self): # Move player
        """
        Function to move player.
        """
        try:
            self.map_object.mutex.acquire() # Lock the mutex
            collision = self.check_collision(self.direction) # Check if there is any collision
            if collision[0] == 0: # If there is no collision
                self.map_object.update_map(self.possition[0], self.possition[1], ' ')
                # If player is going up and there is no collision up
            if self.direction == 'Up' and collision[4] != 1:
                self.possition[1] -= 1
            if self.direction == 'Down' and collision[3] != 1: #...
                self.possition[1] += 1
            if self.direction == 'Left' and collision[2] != 1:
                self.possition[0] -= 1
            if self.direction == 'Right' and collision[1] != 1:
                self.possition[0] += 1
            if collision[0] == 0:
                self.check_map()  # Check if there is a bullet on the map
                # Update map
                self.map_object.update_map(self.possition[0], self.possition[1], self.letter)
        finally:
            self.map_object.mutex.release() # Release the mutex

    def steer_player(self, event=None):
        """
        Function to steer player.
        """
        if event.keysym in ('Up', 'Down', 'Left', 'Right'):
            self.direction = event.keysym
            self.change_photo_direction()
        if event.keysym == 'space':
            self.shoot()
