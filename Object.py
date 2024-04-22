class Object:
    def __init__(self, x, y):
        x, y = 1 ,1
        self.possition = [x, y]
        self.previousPosition = [x, y]
        self.init = True
        self.possitionChanged = True
        self.isRunning = True

    def get_possition(self):
        return [self.possition[0], self.possition[1]]

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
    def checkCollision(self, objekt, direction):
        a = self.possition
        p = objekt.get_possition()
        res = [0,0,0,0,0]
        r, l, u, d = 0, 0, 0, 0
        if direction == 'Right':
            r = 1
        if direction == 'Left':
            l = -1
        if direction == 'Down':
            d = 1
        if direction == 'Up':
            u = -1

        if a[0]+r == p[0] and a[1] == p[1]: #right
            res[0]=1
            res[1]=1
        if a[0]+l == p[0] and a[1] == p[1]: #left
            res[0]=1
            res[2]=1
        if a[1]+d == p[1] and a[0] == p[0]: #down
            res[0]=1
            res[3]=1
        if a[1]+u == p[1] and a[0] == p[0]: #up
            res[0]=1
            res[4]=1
        return res
