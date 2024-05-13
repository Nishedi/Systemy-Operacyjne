import random
import threading
class MapLoader:
    def __init__(self, filename): # constructor of class with map file name
        self.map = [] # list for map elements
        self.sizeOfArea=self.load_map(filename) # load map from file and set size of area
        self.mutex = threading.Lock() # mutex for map
        self.rangeDistance = 10 # base range distance for enemies
        self.spawnZone = 10 # base space near player where enemies cant be spawned

    def setDifficult(self, difficult): # method that will set difficult of the game
        if difficult == 0: # easy
            self.rangeDistance = 10 # range distance for enemies
            self.spawnZone = 10 # space near player where enemies cant be spawned
        if difficult == 1: # medium
            self.rangeDistance = 15
            self.spawnZone = 8
        if difficult == 2: # hard
            self.rangeDistance = 20
            self.spawnZone = 5

    def load_map(self, filename): # method that will load map from file
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

    def get_what_is_in(self, x, y): # method that will return what is in the map on given possition
        return self.map[y][x]

    def update_map(self, x, y, letter): # method that will update map on given possition
        self.map[y][x] = letter

    def get_size(self): #used to create propely size of the window
        return self.sizeOfArea

    def findEmptyPlace(self): # method that will find empty place on the map
        emptyPossition = [0,0]
        emptyPossition[0], emptyPossition[1] = random.randint(0, len(self.map) - 1), random.randint(0, len(self.map[0]) - 1) # random possition
        while self.get_what_is_in(emptyPossition[1], emptyPossition[0]) != ' ': # while there is no empty place
            emptyPossition[0], emptyPossition[1] = random.randint(0, len(self.map) - 1), random.randint(0, len(self.map[0]) - 1) # keep looking for empty place
        return emptyPossition # return empty place

    def findEmptyPlaceEnemy(self): # method that will find empty place for enemy
        possition = self.findEmptyPlace() # find empty place
        possition2 = [0,0] # swap values (invalid format od find empty place)
        possition2[0] = possition[1]
        possition2[1] = possition[0]
        playerPossition = self.findPlayer(possition2, self.spawnZone) # find player near enemy
        iter = 0
        while playerPossition and iter < 10:
            possition = self.findEmptyPlace()
            iter += 1
        if playerPossition:
            return False
        return possition


    def findNearestPath(self, startPosition, endPosition): # method that will find nearest path from start to end - BFS
        if not startPosition or startPosition == endPosition: # if there is no player possition or player is on the same possition as enemy
            return False # return False (rare case)
        distanceMap = [[]] # map of distances to goal point
        for i in range(len(self.map)): # fill every point with very big number
            distanceMap.append([]) # create new row
            for j in range(len(self.map[i])): # for every column
                distanceMap[i].append(1000000) # fill with very big number
        distanceMap[startPosition[1]][startPosition[0]] = 0 # at goal set distance to 0
        queue = [startPosition] # create queue with start possition
        while len(queue)!=0: # while queue is not empty
            current = queue.pop(0) # get first element from queue
            neighbours = self.createNeighbours(current) # get neighbours of current possition
            for neighbour in neighbours: # for every neighbour
                if self.map[neighbour[1]][neighbour[0]] == 'X': continue # if there is wall, skip possition
                if self.map[neighbour[1]][neighbour[0]] == 'P': continue # if there is player, skip possition
                # if distanceMap[neighbour[1]][neighbour[0]] == 1000000:
                if distanceMap[neighbour[1]][neighbour[0]] > distanceMap[current[1]][current[0]]+1: # if distance is set to very big number
                    distanceMap[neighbour[1]][neighbour[0]] = distanceMap[current[1]][current[0]] + 1 # set distance to current distance + 1
                    queue.append(neighbour) # add neighbour to queue
        neighbours = self.createNeighbours(endPosition) # get neighbours of end possition
        if distanceMap[endPosition[1]][endPosition[0]] == 1: # if distance is 1, return False - cant move, to remove !!!
            return False
        for neighbour in neighbours: # for every neighbour
            if int(distanceMap[neighbour[1]][neighbour[0]]) < int(distanceMap[endPosition[1]][endPosition[0]]): # if neighbour is closer to goal than end possition (current possition)
                if self.checkCollision(neighbour)==0: # if neighbour is empty
                    return neighbour # return neighbour

        return False # return False - cant move

    def createNeighbours(self, possition): # method that will create neighbours of given possition
        neighbours = []
        neighbours.append((possition[0]+1, possition[1])) # right
        neighbours.append((possition[0]-1, possition[1])) # left
        neighbours.append((possition[0], possition[1]+1)) # down
        neighbours.append((possition[0], possition[1]-1)) # up
        return neighbours

    def checkCollision(self, possition): # method that will check if there is any collision on given possition
        a = possition
        if self.get_what_is_in(a[0], a[1]) == 'E':
            return 1
        if self.get_what_is_in(a[0], a[1]) == 'X':
            return 1
        return 0

    def findPlayer(self, myPossition, distance=10): # method that will find player near given possition (range is given)
        for i in range(myPossition[1] - distance, myPossition[1] + distance):
            for j in range(myPossition[0] - distance, myPossition[0] + distance):
                if i < 0 or j < 0 or i >= len(self.map) or j >= len(self.map[i]):
                    continue
                if self.map[i][j] == 'P':
                    return (j, i)
        return False