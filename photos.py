"""
Module to manage game photos.
"""
from tkinter import PhotoImage

class Photos:  # class with photos
    """
    Class to manage game photos.
    """
    def __init__(self):
        """
        Initialize Photos class.
        """
        self.enemy = PhotoImage(file="pictures/mob.png")
        self.ammo = PhotoImage(file="pictures/ammo.png")
        self.wall = PhotoImage(file="pictures/wall.png")

    def return_enemy(self):
        """
        Return enemy photo.
        """
        return self.enemy

    def return_ammo(self):
        """
        Return ammo photo.
        """
        return self.ammo

    def return_wall(self):
        """
        Return wall photo.
        """
        return self.wall
