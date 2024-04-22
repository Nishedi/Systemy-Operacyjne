import random
import threading
class Object:
    def __init__(self, x, y, map):
        self.possition = [x, y]
        self.map = map
        self.isRunning = True
        self.thread = threading.Thread(target=self.threadLoop, args=())


    def get_possition(self):
        return [self.possition[0], self.possition[1]]

    def threadLoop(self):
        while self.isRunning:
            pass

    def checkCollision2(self, map, direction):
        a = self.possition
        res = [0,0,0,0,0]
        if map[a[1]][a[0]+1] == 'X':
            if direction == 'Right':
                res[0] = 1
                res[1] = 1
        if map[a[1]][a[0]-1] == 'X':
            if direction == 'Left':
                res[0] = 1
                res[2] = 1
        if map[a[1]-1][a[0]] == 'X':
            if direction == 'Up':
                res[4] = 1
                res[0] = 1
        if map[a[1]+1][a[0]] == 'X':
            if direction == 'Down':
                res[3] = 1
                res[0] = 1
        return res
    def move(self, mode=1):
        collision = self.checkCollision2(self.map, self.direction)
        if collision[0]==0:
            self.map[self.possition[1]][self.possition[0]]=' '
        if self.direction == 'Up' and collision[4]!=1:
            self.possition[1] -= 1
        if self.direction == 'Down' and collision[3]!=1:
            self.possition[1] += 1
        if self.direction == 'Left' and collision[2]!=1:
            self.possition[0] -= 1
        if self.direction == 'Right' and collision[1]!=1:
            self.possition[0] += 1

        self.map[self.possition[1]][self.possition[0]] = self.letter
        if mode == 1 and collision[0]==1:
            if collision[1]==1:
                if collision[3]==1:
                    self.setDirection(['Down','Right'])
                elif collision[4]==1:
                    self.setDirection(['Up','Right'])
                else:
                    self.setDirection(['Right'])
            elif collision[2]==1:
                if collision[3]==1:
                    self.setDirection(['Left', 'Down'])
                elif collision[4]==1:
                    self.setDirection(['Left','Up'])
                else:
                    self.setDirection(['Left'])
            else:
                if collision[3]==1:
                    self.setDirection(['Down'])
                elif collision[4]==1:
                    self.setDirection(['Up'])
                else:
                    self.setDirection(['Right'])
        elif mode == 1 and random.randint(0, 5) == 0:
            self.setDirection([])
    def setDirection(self, forbidden_directions):
        if len(forbidden_directions) == 4:
            return
        self.direction = random.choice(["Up", "Down", "Left", "Right"])
        while self.direction in forbidden_directions:
            self.direction = random.choice(["Up", "Down", "Left", "Right"])