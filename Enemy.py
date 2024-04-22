import time
import random

from Object import Object

class Enemy(Object):

    def __init__(self, possition, map):
        possition = (1,1)
        super().__init__(possition[1], possition[0], map)
        self.directions = ['Up', 'Down', 'Left', 'Right']
        self.direction = self.directions[random.randint(0,3)]

        self.letter = 'E'
        self.map[self.possition[1]][self.possition[0]] = self.letter
        self.thread.start()



    def threadLoop(self):
        time.sleep(1)
        while self.isRunning:
            self.move()
            time.sleep(1)



