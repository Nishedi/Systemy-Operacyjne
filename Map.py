import random

from Object import Object
class MapLoader:
    def __init__(self, filename):
        self.map = []
        self.sizeOfArea=self.load_map(filename)
        self.map2 = []
        self.load_map2(filename)

    def load_map2(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                str = []
                for i in range(len(line)):
                    if(line[i]!='\n'):
                        str.append(line[i])
                self.map2.append(str)


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
        emptyPossition = [0,0]
        emptyPossition[0], emptyPossition[1] = random.randint(0, len(self.map2)-1), random.randint(0, len(self.map2[0])-1)
        while self.map2[emptyPossition[0]][emptyPossition[1]]!=' ':
            emptyPossition[0], emptyPossition[1] = random.randint(0, len(self.map2)-1), random.randint(0,
                                                                                                     len(self.map2[0])-1)
        return emptyPossition

