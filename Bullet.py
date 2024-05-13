from Object import Object
import time
class Bullet(Object):
    def __init__(self, x, y, direction, threadMenager, map, player):
        super().__init__(map)
        self.possition = [x,y]
        self.direction = direction # direction of the bullet (where it is going)
        self.threadMenager = threadMenager # threadMenager object that will be used to check if bullet hit an enemy
        self.mapObject.update_map(self.possition[0], self.possition[1], 'B') # update map with bullet
        self.player = player # player object that will be used to add score
        self.thread.start() # start thread

    def threadLoop(self): # main loop of the bullet thread
        self.checkCollisionEnemy() # check if bullet hit an enemy (the first time, before first move)
        while self.isRunning: # while bullet had not hit anything
            self.move() # move bullet
            time.sleep(0.1) # wait for 0.1 s

    def checkCollision(self, map, direction): # check if bullet is going to hit something
        a = self.possition # get bullet possition
        res = [0,0,0,0,0] # list of possible collisions
        right = self.mapObject.get_what_is_in(a[0]+1, a[1]) # get what is on the right
        left = self.mapObject.get_what_is_in(a[0]-1, a[1])  # get what is on the left
        up = self.mapObject.get_what_is_in(a[0], a[1]-1)    # get what is up
        down = self.mapObject.get_what_is_in(a[0], a[1]+1)  # get what is down
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

    def checkCollisionEnemy(self): # check if bullet hit an enemy
        if self.threadMenager.checkHitting(self.possition): # if bullet hit an enemy, logic of stopping enemy thread is in threadMenager
            self.mapObject.update_map(self.possition[0], self.possition[1], ' ') # remove bullet from the map
            self.player.addOneScore() # add score to the player
            self.isRunning = False # end the bullet thread
            return True # return that bullet hit an enemy

    def move(self, mode=1): # move bullet
        try: # try to lock the mutex
            self.mapObject.mutex.acquire()
            collision = self.checkCollision(self.map, self.direction)   # check if there is any collision
            self.mapObject.update_map(self.possition[0], self.possition[1], ' ') # remove bullet from the map
            if self.direction == 'Up' and collision[4] != 1: # if bullet is going up and there is no collision up
                self.possition[1] -= 1 # move bullet up
            if self.direction == 'Down' and collision[3] != 1: # if bullet is going down and there is no collision down
                self.possition[1] += 1 # move bullet down
            if self.direction == 'Left' and collision[2] != 1: # if bullet is going left and there is no collision left
                self.possition[0] -= 1 # move bullet left
            if self.direction == 'Right' and collision[1] != 1: # if bullet is going right and there is no collision right
                self.possition[0] += 1 # move bullet right
            if self.checkCollisionEnemy(): # check if bullet hit an enemy
                return # if bullet hit an enemy, return
            if collision[0] == 1: # if there is any collision
                self.mapObject.update_map(self.possition[0], self.possition[1], ' ') # remove bullet from the map
                self.isRunning = False # end the bullet thread
            else: # if there is no collision
                self.mapObject.update_map(self.possition[0], self.possition[1], 'B') # update map with bullet
        finally:
            self.mapObject.mutex.release() # release the mutex
