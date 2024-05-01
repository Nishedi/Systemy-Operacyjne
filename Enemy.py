import time
import random

from Object import Object

class Enemy(Object):

    def __init__(self, possition, map):
        super().__init__(possition[1], possition[0], map)
        self.directions = ['Up', 'Down', 'Left', 'Right']
        self.direction = self.directions[random.randint(0,3)]
        self.letter = 'E'
        self.spawn()
        self.thread.start()

    def spawn(self):
        try:
            self.mapObject.mutex.acquire()
            possition = self.mapObject.findEmptyPlace()
            self.possition[0], self.possition[1] = possition[1], possition[0]
            self.mapObject.update_map(self.possition[0], self.possition[1], self.letter)
        finally:
            self.mapObject.mutex.release()

    def findPlayer(self):
        for i in range(len(self.mapObject.map)):
            for j in range(len(self.mapObject.map[i])):
                if self.mapObject.map[i][j] == 'P':
                    return (j, i)

    def checkCollision2(self, map, possition):
        a = possition
        if self.mapObject.get_what_is_in(a[0], a[1]) == 'E':
            return 1
        return 0
    def move(self, mode=1):
        collision = [0,0,0,0,0]
        try:
            self.mapObject.mutex.acquire()
            collision = self.checkCollision(self.map, self.direction)
            self.mapObject.update_map(self.possition[0], self.possition[1], ' ')
            possition = self.algorithm(self.findPlayer())
            if possition and self.checkCollision2(self.map, possition)==0:
                self.possition = possition
            self.mapObject.update_map(self.possition[0],self.possition[1], self.letter)

        finally:
            self.mapObject.mutex.release()


    def createNeighbours(self, possition):
        neighbours = []
        neighbours.append((possition[0]+1, possition[1]))
        neighbours.append((possition[0]-1, possition[1]))
        neighbours.append((possition[0], possition[1]+1))
        neighbours.append((possition[0], possition[1]-1))
        return neighbours

    def algorithm(self, startPosition):
        if not startPosition or startPosition == self.possition:
            return False
        endPosition = self.possition
        distanceMap = [[]]
        for i in range(len(self.mapObject.map)):
            distanceMap.append([])
            for j in range(len(self.mapObject.map[i])):
                distanceMap[i].append(1000000)
        distanceMap[startPosition[1]][startPosition[0]] = 0
        queue = [startPosition]
        while len(queue)!=0:
            current = queue.pop(0)
            neighbours = self.createNeighbours(current)
            for neighbour in neighbours:
                if self.mapObject.map[neighbour[1]][neighbour[0]] == 'X': continue
                if self.mapObject.map[neighbour[1]][neighbour[0]] == 'P': continue
                # if self.mapObject.map[neighbour[1]][neighbour[0]] == 'E': continue
                if distanceMap[neighbour[1]][neighbour[0]] == 1000000:
                    distanceMap[neighbour[1]][neighbour[0]] = distanceMap[current[1]][current[0]] + 1
                    queue.append(neighbour)
        neighbours = self.createNeighbours(endPosition)
        toreturn = []
        if distanceMap[endPosition[1]][endPosition[0]] == 1:
            return False
        for neighbour in neighbours:
            if int(distanceMap[neighbour[1]][neighbour[0]]) < int(distanceMap[endPosition[1]][endPosition[0]]):
                if self.checkCollision2(self.map, neighbour)==0:
                    return neighbour

        return False



    def threadLoop(self):
        while self.isRunning:
            self.move()
            time.sleep(1+random.randint(0,100)/1000)
        self.mapObject.update_map(self.possition[0], self.possition[1], ' ')



