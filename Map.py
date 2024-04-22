import random

from Object import Object
class MapLoader:
    def __init__(self, filename):
        self.map = []
        self.sizeOfArea=self.load_map2(filename)

    def load_map2(self, filename):
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

    def get_size(self):
        return self.sizeOfArea

    def findEmptyPlace(self):
        emptyPossition = [0,0]
        emptyPossition[0], emptyPossition[1] = random.randint(0, len(self.map) - 1), random.randint(0, len(self.map[0]) - 1)
        while self.map[emptyPossition[0]][emptyPossition[1]]!= ' ':
            emptyPossition[0], emptyPossition[1] = random.randint(0, len(self.map) - 1), random.randint(0,
                                                                                                        len(self.map[0]) - 1)
        return emptyPossition

