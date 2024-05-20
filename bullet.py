"""
Module to manage bullet objects.
"""
import time
from object import Object
class Bullet(Object):
    """
    Class to manage bullet objects.
    """
    def __init__(self, x, y, direction, thread_menager, map2d, player):
        """
        Initialize Bullet object.
        """
        super().__init__(map2d)
        self.possition = [x,y]
        self.direction = direction # direction of the bullet (where it is going)
        self.thread_menager = thread_menager # threadMenager object that will be
        # used to check if bullet hit an enemy
        self.map_object.update_map(self.possition[0],
                                   self.possition[1], 'B') # update map with bullet
        self.player = player # player object that will be used to add score
        self.thread.start() # start thread

    def thread_loop(self):
        """
        Function to manage bullet thread.
        """
        # check if bullet hit an enemy (the first time, before first move)
        self.check_collision_enemy()
        while self.is_running: # while bullet had not hit anything
            self.move() # move bullet
            time.sleep(0.1) # wait for 0.1 s

    def check_collision(self, direction):
        """
        Function to check if bullet is going to hit something.
        """
        a = self.possition # get bullet possition
        res = [0,0,0,0,0] # list of possible collisions
        right = self.map_object.get_what_is_in(a[0] + 1, a[1]) # get what is on the right
        left = self.map_object.get_what_is_in(a[0] - 1, a[1])  # get what is on the left
        up = self.map_object.get_what_is_in(a[0], a[1] - 1)    # get what is up
        down = self.map_object.get_what_is_in(a[0], a[1] + 1)  # get what is down
        if right == 'X': # if there is wall on the right
            if direction == 'Right': # and bullet is going right
                res[0] = 1 # set collision flag - there is any collision
                res[1] = 1 # set collision flag - there is right collision
        if left == 'X': # if there is wall on the left
            if direction == 'Left': # and bullet is going left
                res[0] = 1 # set collision flag - there is any collision
                res[2] = 1 # set collision flag - there is left collision
        if up == 'X' : # if there is wall up
            if direction == 'Up': # and bullet is going up
                res[0] = 1 # set collision flag - there is any collision
                res[4] = 1 # set collision flag - there is up collision
        if down == 'X': # if there is wall down
            if direction == 'Down': # and bullet is going down
                res[0] = 1 # set collision flag - there is any collision
                res[3] = 1 # set collision flag - there is down collision
        return res # return list of collisions

    def check_collision_enemy(self):
        """
        Function to check if bullet hit an enemy.
        """
        # if bullet hit an enemy, logic of stopping enemy thread is in threadMenager
        if self.thread_menager.check_hitting(self.possition):
            # remove bullet from the map
            self.map_object.update_map(self.possition[0], self.possition[1], ' ')
            self.player.add_one_score() # add score to the player
            self.is_running = False # end the bullet thread
            return True # return that bullet hit an enemy
        return False

    def move(self):
        """
        Function to move bullet.
        """
        try: # try to lock the mutex
            self.map_object.mutex.acquire()
            # check if there is any collision
            collision = self.check_collision(self.direction)
            # remove bullet from the map
            previous_possition = self.possition.copy()
            if self.check_collision_enemy(): # check if bullet hit an enemy
                return # if bullet hit an enemy, return
            self.map_object.update_map(previous_possition[0], previous_possition[1], ' ')
            # if bullet is going up and there is no collision up
            if self.direction == 'Up' and collision[4] != 1:
                self.possition[1] -= 1 # move bullet up
             # if bullet is going down and there is no collision down
            if self.direction == 'Down' and collision[3] != 1:
                self.possition[1] += 1 # move bullet down
            # if bullet is going left and there is no collision left
            if self.direction == 'Left' and collision[2] != 1:
                self.possition[0] -= 1 # move bullet left
            # if bullet is going right and there is no collision right
            if self.direction == 'Right' and collision[1] != 1:
                self.possition[0] += 1 # move bullet right
            if self.check_collision_enemy(): # check if bullet hit an enemy
                return # if bullet hit an enemy, return
            if collision[0] == 1: # if there is any collision
                # remove bullet from the map
                self.is_running = False # end the bullet thread
            else: # if there is no collision
                # update map with bullet
                self.map_object.update_map(self.possition[0], self.possition[1], 'B')
        finally:
            self.map_object.mutex.release() # release the mutex
