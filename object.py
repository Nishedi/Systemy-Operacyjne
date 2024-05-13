"""
Module for the Object class
"""
import threading

class Object:
    """
    Class to manage objects on the map.
    """
    def __init__(self, map2d):
        """
        Object initializer
        """
        self.possition = [0, 0] # possition of the object
        self.map_object = map2d # map object
        self.map = self.map_object.map2d # map - 2D list
        self.is_running = True # is thread active
        self.letter = ' '
        self.thread = threading.Thread(target=self.thread_loop, args=()) # thread
        self.mutex = threading.Lock() # mutex

    def start_thread(self):
        """
        Function to start the object thread.
        """
        self.thread.start() # start thread

    def spawn(self):
        """
        Function to spawn object on the map.
        """
        with self.map_object.mutex:
            possition = self.map_object.find_empty_place() # find empty place
            self.possition[0], self.possition[1] = possition[1], possition[0] #assaing new possition
            self.map_object.update_map(self.possition[0], self.possition[1], self.letter)#update map

    def get_possition(self):  # get position of the object
        """
        Function to get position of the object.
        """
        with self.mutex:  # Lock the mutex
            position = [self.possition[0], self.possition[1]]  # Get position
        return position  # Return position

    def thread_loop(self): # main loop of the object thread
        """
        skeleton to inherit
        """
        while self.is_running:
            pass

    def move(self):
        """
        Skeleton to inherit
        """
