import time
import random

from Object import Object

class Enemy(Object):

    def __init__(self, possition, map, threadMenager):
        super().__init__(possition[1], possition[0], map)
        self.letter = 'E'
        self.spawn()
        self.threadMenager = threadMenager
        self.thread.start()

    def spawn(self):
        try:
            self.mapObject.mutex.acquire()
            possition = self.mapObject.findEmptyPlace()
            self.possition[0], self.possition[1] = possition[1], possition[0]
            self.mapObject.update_map(self.possition[0], self.possition[1], self.letter)
        finally:
            self.mapObject.mutex.release()

    def findPlayer(self, distance=10):
        for i in range(self.possition[1] - distance, self.possition[1] + distance):
            for j in range(self.possition[0] - distance, self.possition[0] + distance):
                if i < 0 or j < 0 or i >= len(self.mapObject.map) or j >= len(self.mapObject.map[i]):
                    continue
                if self.mapObject.map[i][j] == 'P':
                    return (j, i)
        return False

    def checkCollision2(self, possition):
        a = possition
        if self.mapObject.get_what_is_in(a[0], a[1]) == 'E':
            return 1
        if self.mapObject.get_what_is_in(a[0], a[1]) == 'X':
            return 1
        if self.mapObject.get_what_is_in(a[0], a[1]) == 'P':
            self.threadMenager.closeAll()
            return 1
        return 0

    def move(self, mode=1):
        try:
            self.mapObject.mutex.acquire()
            self.mapObject.update_map(self.possition[0], self.possition[1], ' ')
            playerPossition = self.findPlayer()
            if playerPossition:
                possition = self.algorithm(playerPossition)
            if not playerPossition or not possition:
                goodNeighbours = []
                for neighbour in self.createNeighbours(self.possition):
                    if self.checkCollision2(neighbour)==0:
                        goodNeighbours.append(neighbour)
                if len(goodNeighbours) == 0:
                    return
                possition = goodNeighbours[random.randint(0, len(goodNeighbours)-1)]
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
                if distanceMap[neighbour[1]][neighbour[0]] == 1000000:
                    distanceMap[neighbour[1]][neighbour[0]] = distanceMap[current[1]][current[0]] + 1
                    queue.append(neighbour)
        neighbours = self.createNeighbours(endPosition)
        if distanceMap[endPosition[1]][endPosition[0]] == 1:
            return False
        for neighbour in neighbours:
            if int(distanceMap[neighbour[1]][neighbour[0]]) < int(distanceMap[endPosition[1]][endPosition[0]]):
                if self.checkCollision2(neighbour)==0:
                    return neighbour

        return False



    def threadLoop(self):
        while self.isRunning:
            self.move()
            time.sleep(1+random.randint(0,100)/1000)
        self.mapObject.update_map(self.possition[0], self.possition[1], ' ')



