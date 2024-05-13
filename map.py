"""
    This file contains class MapLoader that is used to load
    map from file and do some operations on it.
"""
import random
import threading
class MapLoader:
    """
    Class that will load map from file and do some operations on it.
    """
    def __init__(self, filename): # constructor of class with map file name
        """
        Initialize MapLoader object.
        """
        self.map2d = [] # list for map elements
        # load map from file and set size of area
        self.size_of_area=self.load_map(filename)
        self.mutex = threading.Lock() # mutex for map
        self.range_distance = 10 # base range distance for enemies
        self.spawn_zone = 10 # base space near player where enemies cant be spawned

    def set_difficult(self, difficult):
        """
        Method that will set difficult of the game.
        """
        if difficult == 0: # easy
            self.range_distance = 10 # range distance for enemies
            self.spawn_zone = 10 # space near player where enemies cant be spawned
        if difficult == 1: # medium
            self.range_distance = 15
            self.spawn_zone = 8
        if difficult == 2: # hard
            self.range_distance = 20
            self.spawn_zone = 5

    def load_map(self, filename):
        """
        Method that will load map from file.
        """
        lines = 0
        size = 0
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                size = line
                c = []
                for char in line:
                    if char != '\n':
                        c.append(char)
                self.map2d.append(c)
                lines += 1
        return (lines * 40, len(size) * 40, lines, len(size))

    def get_what_is_in(self, x, y):
        """
        Method that will return what is in the map on given possition.
        """
        return self.map2d[y][x]

    def update_map(self, x, y, letter):
        """
        Method that will update map on given possition.
        """
        self.map2d[y][x] = letter

    def get_size(self):
        """
        Method that will return size of the map, used to create propely size of the window.
        """
        return self.size_of_area

    def find_empty_place(self):
        """
        Method that will find empty place on the map.
        """
        empty_possition = [0,0]
        # random possition
        empty_possition[0], empty_possition[1] = (random.randint(0, len(self.map2d) - 1),
                                                random.randint(0, len(self.map2d[0]) - 1))
        # while there is no empty place
        while self.get_what_is_in(empty_possition[1], empty_possition[0]) != ' ':
            # keep looking for empty place
            empty_possition[0], empty_possition[1] = (random.randint(0, len(self.map2d) - 1),
                                                    random.randint(0, len(self.map2d[0]) - 1))
        return empty_possition # return empty place

    def find_empty_place_enemy(self):
        """
        Method that will find empty place for enemy.
        """
        possition = self.find_empty_place() # find empty place
        # find player near enemy
        player_possition = self.find_player([possition[1],possition[0]], self.spawn_zone)
        counter = 0
        while player_possition and counter < 1000:
            possition = self.find_empty_place()
            counter += 1
        if player_possition:
            return False
        return possition


    def find_nearest_path(self, start_position, end_position):
        """
        Method that will find nearest path from start to end - BFS.
        """
        # if there is no player possition or player is on the same possition as enemy
        if not start_position or start_position == end_position:
            return False # return False (rare case)
        distance_map = [[]] # map of distances to goal point
        for i in range(len(self.map2d)): # fill every point with very big number
            distance_map.append([]) # create new row
            for j in range(len(self.map2d[i])): # for every column
                distance_map[i].append(1000000) # fill with very big number
        distance_map[start_position[1]][start_position[0]] = 0 # at goal set distance to 0
        queue = [start_position] # create queue with start possition
        while len(queue)!=0: # while queue is not empty
            current = queue.pop(0) # get first element from queue
            neighbours = self.create_neighbours(current) # get neighbours of current possition
            for neighbour in neighbours: # for every neighbour
                # if there is wall, skip possition
                if self.map2d[neighbour[1]][neighbour[0]] == 'X':
                    continue
                # if there is player, skip possition
                if self.map2d[neighbour[1]][neighbour[0]] == 'P':
                    continue
                # if distance is set to very big number
                if (distance_map[neighbour[1]][neighbour[0]] >
                        distance_map[current[1]][current[0]]+1):
                    # set distance to current distance + 1
                    distance_map[neighbour[1]][neighbour[0]] \
                        = distance_map[current[1]][current[0]] + 1
                    queue.append(neighbour) # add neighbour to queue
        neighbours = self.create_neighbours(end_position) # get neighbours of end possition
        # if distance is 1, return False - cant move
        if distance_map[end_position[1]][end_position[0]] == 1:
            return False
        for neighbour in neighbours: # for every neighbour
            # if neighbour is closer to goal than end possition (current possition)
            try:
                if (int(distance_map[neighbour[1]][neighbour[0]])
                        < int(distance_map[end_position[1]][end_position[0]])):
                    if self.check_collision(neighbour)==0: # if neighbour is empty
                        return neighbour # return neighbour
            except:
                print(neighbour)

        return False # return False - cant move

    def create_neighbours(self, possition):
        """
        Method that will create neighbours of given possition.
        """
        neighbours = []
        neighbours.append((possition[0]+1, possition[1])) # right
        neighbours.append((possition[0]-1, possition[1])) # left
        neighbours.append((possition[0], possition[1]+1)) # down
        neighbours.append((possition[0], possition[1]-1)) # up
        return neighbours

    def check_collision(self, possition):
        """
        Method that will check if there is any collision on given possition.
        """
        a = possition
        if self.get_what_is_in(a[0], a[1]) == 'E':
            return 1
        if self.get_what_is_in(a[0], a[1]) == 'X':
            return 1
        return 0

    def find_player(self, my_possition, distance=10):
        """
        Method that will find player near given possition (range is given).
        """
        for i in range(my_possition[1] - distance, my_possition[1] + distance):
            for j in range(my_possition[0] - distance, my_possition[0] + distance):
                if i < 0 or j < 0 or i >= len(self.map2d) or j >= len(self.map2d[i]):
                    continue
                if self.map2d[i][j] == 'P':
                    return (j, i)
        return False
