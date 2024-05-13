"""
This file contains Enemy class which is responsible for enemy object in the game.
"""
import time
import random
from object import Object

class Enemy(Object):
    """
    Class which represent enemy object in the game.
    """
    def __init__(self, map2d, thread_menager):
        """
        Initialize Enemy object.
        """
        super().__init__(map2d)
        self.letter = 'E' # Letter which represent enemy on the map
        self.spawn() # Spawn enemy on empty place
        self.thread_menager = thread_menager #threadMenager to stop the game

    def spawn(self):
        """
        Function which spawn enemy
        """
        try:
            # Lock the map mutex to avoid synchronization problems
            self.map_object.mutex.acquire()
            # Find empty place which is not near player
            possition = self.map_object.find_empty_place_enemy()
            if not possition: # If there is no empty place,
                return # return
            self.possition[0], self.possition[1] = possition[1], possition[0] # Set new possition
            # Update map
            self.map_object.update_map(self.possition[0], self.possition[1], self.letter)
        finally:
            self.map_object.mutex.release() # No matter what unlock the mutex

    def check_collision(self, possition):
        """
        Function to check if bullet is going to hit something.
        """
        a = possition
        if self.map_object.get_what_is_in(a[0], a[1]) == 'E': # Check if there is enemy
            return 1
        if self.map_object.get_what_is_in(a[0], a[1]) == 'X': # Check if there is wall
            return 1
        if self.map_object.get_what_is_in(a[0], a[1]) == 'B': # Check if there is player
            self.is_running = False
            return 1
        if self.map_object.get_what_is_in(a[0], a[1]) == 'P': # Check if there is player
            self.thread_menager.close_all()
            return 1
        return 0

    def move(self):
        """
        Function which move enemy
        """
        try:
            self.map_object.mutex.acquire() # Lock the map mutex to avoid synchronization problems
            # Find where player is
            player_possition = self.map_object.find_player(self.possition,
                                                           self.map_object.range_distance)
            if player_possition: # If player is found, find the nearest path to him
                possition = self.map_object.find_nearest_path(player_possition, self.possition)
            # If player is not found or path is not found, move randomly
            if not player_possition or not possition:
                good_neighbours = [] # List of possible neighbours
                # Check all neighbours
                for neighbour in self.map_object.create_neighbours(self.possition):
                    # If neighbour is empty, add it to the list
                    if self.check_collision(neighbour)==0:
                        good_neighbours.append(neighbour)
                if len(good_neighbours) == 0: # If there is no empty neighbours, return
                    return
                # Choose random neighbour
                possition = good_neighbours[random.randint(0, len(good_neighbours)-1)]
            # Remove enemy from the map
            self.map_object.update_map(self.possition[0], self.possition[1], ' ')
            self.possition = possition # Set new possition
            self.map_object.update_map(self.possition[0], self.possition[1],
                                       self.letter) # Update map
        finally: # No matter what unlock the mutex
            self.map_object.mutex.release() # Release the mutex

    def thread_loop(self):
        """
        Main loop of the enemy thread.
        """
        while self.is_running: # While enemy is alive
            self.move() # Move enemy
            time.sleep(1+random.randint(0,100)/1000) # wait for a while
            # If enemy is dead, remove him from the map
        self.map_object.update_map(self.possition[0], self.possition[1], ' ')
