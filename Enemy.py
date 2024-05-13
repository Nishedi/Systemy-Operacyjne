import time
import random
from Object import Object

class Enemy(Object):
    def __init__(self, possition, map, threadMenager):
        super().__init__(possition[1], possition[0], map)
        self.letter = 'E'
        self.spawn()
        self.threadMenager = threadMenager

    def spawn(self): # Function which spawn enemy
        try:
            self.mapObject.mutex.acquire() # Lock the map mutex to avoid synchronization problems
            possition = self.mapObject.findEmptyPlaceEnemy() # Find empty place which is not near player
            if not possition: # If there is no empty place,
                return # return
            self.possition[0], self.possition[1] = possition[1], possition[0] # Set new possition
            self.mapObject.update_map(self.possition[0], self.possition[1], self.letter) # Update map
        finally:
            self.mapObject.mutex.release() # No matter what unlock the mutex

    def checkCollision(self, possition):
        a = possition
        if self.mapObject.get_what_is_in(a[0], a[1]) == 'E': # Check if there is enemy
            return 1
        if self.mapObject.get_what_is_in(a[0], a[1]) == 'X': # Check if there is wall
            return 1
        if self.mapObject.get_what_is_in(a[0], a[1]) == 'P': # Check if there is player
            self.threadMenager.closeAll()
            return 1
        return 0

    def move(self, mode=1): # Function which move enemy
        try:
            self.mapObject.mutex.acquire() # Lock the map mutex to avoid synchronization problems
            playerPossition = self.mapObject.findPlayer(self.possition) # Find where player is
            if playerPossition: # If player is found, find the nearest path to him
                possition = self.mapObject.findNearestPath(playerPossition, self.possition)
            if not playerPossition or not possition: # If player is not found or path is not found, move randomly
                goodNeighbours = [] # List of possible neighbours
                for neighbour in self.mapObject.createNeighbours(self.possition): # Check all neighbours
                    if self.checkCollision(neighbour)==0: # If neighbour is empty, add it to the list
                        goodNeighbours.append(neighbour)
                if len(goodNeighbours) == 0: # If there is no empty neighbours, return
                    return
                possition = goodNeighbours[random.randint(0, len(goodNeighbours)-1)] # Choose random neighbour
            self.mapObject.update_map(self.possition[0], self.possition[1], ' ') # Remove enemy from the map
            self.possition = possition # Set new possition
            self.mapObject.update_map(self.possition[0],self.possition[1], self.letter) # Update map
        finally: # No matter what unlock the mutex
            self.mapObject.mutex.release() # Release the mutex

    def threadLoop(self): # Main loop of the enemy thread
        while self.isRunning: # While enemy is alive
            self.move() # Move enemy
            time.sleep(1+random.randint(0,100)/1000) # wait for a while
        self.mapObject.update_map(self.possition[0], self.possition[1], ' ') # If enemy is dead, remove him from the map



