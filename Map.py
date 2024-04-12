import random

from Object import Object
class MapLoader:
    def __init__(self, filename):
        self.map = []
        self.sizeOfArea=self.load_map(filename)

    def load_map(self, filename):
        x=0
        with open(filename, 'r') as file:
            for line in file:

                for i in range(len(line)):
                    if line[i] == 'X':
                        self.map.append(Object(i,x))
                x += 1
        return (x*40, len(line)*40, x, len(line))

    def get_map(self):
        return self.map

    def get_size(self):
        return self.sizeOfArea

    def findEmptyPlace(self):
        emptyPossition = []
        isEmpty = False
        while not isEmpty:
            emptyPossition = [random.randint(1, self.sizeOfArea[3]-1), random.randint(1, self.sizeOfArea[2]-1)]
            isEmpty = True
            for object in self.map:
                if object.get_possition() == emptyPossition:
                    isEmpty = False
                    break
        return emptyPossition