import random
import threading

from Object import Object
class MapLoader:
    def __init__(self, filename):
        self.map = []
        self.sizeOfArea=self.load_map(filename)
        self.mutex = threading.Lock()
        self.rangeDistance = 10
        self.spawnZone = 10

    def setDifficult(self, difficult):
        if difficult == 0:
            self.rangeDistance = 10
            self.spawnZone = 10
        if difficult == 1:
            self.rangeDistance = 15
            self.spawnZone = 8
        if difficult == 2:
            self.rangeDistance = 20
            self.spawnZone = 5

    def load_map(self, filename):
        lines = 0
        with open(filename, 'r') as file:
            for line in file:
                str = []
                for i in range(len(line)):
                    if(line[i]!='\n'):
                        str.append(line[i])
                self.map.append(str)
                lines += 1
        return (lines * 40, len(line) * 40, lines, len(line))

    def get_map(self):
        return self.map

    def get_what_is_in(self, x, y):
        return self.map[y][x]

    def update_map(self, x, y, letter):
        self.map[y][x] = letter

    def get_size(self):
        return self.sizeOfArea

    def findEmptyPlace(self):
        emptyPossition = [0,0]
        emptyPossition[0], emptyPossition[1] = random.randint(0, len(self.map) - 1), random.randint(0, len(self.map[0]) - 1)
        while self.get_what_is_in(emptyPossition[1], emptyPossition[0]) != ' ':
            emptyPossition[0], emptyPossition[1] = random.randint(0, len(self.map) - 1), random.randint(0,
                                                                                                            len(self.map[0]) - 1)
        return emptyPossition

    def findEmptyPlaceEnemy(self):
        possition = self.findEmptyPlace()
        possition2 = [0,0]
        possition2[0] = possition[1]
        possition2[1] = possition[0]
        playerPossition = self.findPlayer(possition2, 5)
        iter = 0
        while playerPossition and iter < 10:
            possition = self.findEmptyPlace()
            iter += 1
        if playerPossition:
            return False
        return possition


    def findNearestPath(self, startPosition, endPosition):
        if not startPosition or startPosition == endPosition:
            return False
        distanceMap = [[]]
        for i in range(len(self.map)):
            distanceMap.append([])
            for j in range(len(self.map[i])):
                distanceMap[i].append(1000000)
        distanceMap[startPosition[1]][startPosition[0]] = 0
        queue = [startPosition]
        while len(queue)!=0:
            current = queue.pop(0)
            neighbours = self.createNeighbours(current)
            for neighbour in neighbours:
                if self.map[neighbour[1]][neighbour[0]] == 'X': continue
                if self.map[neighbour[1]][neighbour[0]] == 'P': continue
                if distanceMap[neighbour[1]][neighbour[0]] == 1000000:
                    distanceMap[neighbour[1]][neighbour[0]] = distanceMap[current[1]][current[0]] + 1
                    queue.append(neighbour)
        neighbours = self.createNeighbours(endPosition)
        if distanceMap[endPosition[1]][endPosition[0]] == 1:
            return False
        for neighbour in neighbours:
            if int(distanceMap[neighbour[1]][neighbour[0]]) < int(distanceMap[endPosition[1]][endPosition[0]]):
                if self.checkCollision(neighbour)==0:
                    return neighbour

        return False

    def createNeighbours(self, possition):
        neighbours = []
        neighbours.append((possition[0]+1, possition[1]))
        neighbours.append((possition[0]-1, possition[1]))
        neighbours.append((possition[0], possition[1]+1))
        neighbours.append((possition[0], possition[1]-1))
        return neighbours

    def checkCollision(self, possition):
        a = possition
        if self.get_what_is_in(a[0], a[1]) == 'E':
            return 1
        if self.get_what_is_in(a[0], a[1]) == 'X':
            return 1
        return 0

    def findPlayer(self, myPossition, distance=10):
        for i in range(myPossition[1] - distance, myPossition[1] + distance):
            for j in range(myPossition[0] - distance, myPossition[0] + distance):
                if i < 0 or j < 0 or i >= len(self.map) or j >= len(self.map[i]):
                    continue
                if self.map[i][j] == 'P':
                    return (j, i)
        return False