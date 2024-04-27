import time
import random

from Object import Object

class Enemy(Object):

    def __init__(self, possition, map):
        super().__init__(possition[1], possition[0], map)
        self.directions = ['Up', 'Down', 'Left', 'Right']
        self.direction = self.directions[random.randint(0,3)]
        self.letter = 'E'
        self.map[self.possition[1]][self.possition[0]] = self.letter
        self.thread.start()
    def threadLoop(self):
        while self.isRunning:
            self.move()
            time.sleep(1+random.randint(0,100)/1000)
        self.map[self.possition[1]][self.possition[0]] = ' '
        print("dead")



