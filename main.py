import math
import random
from graphics.graphics import *

WIDTH = 600
HEIGHT = 600
ROWS = 50
COLS = 50
START = Point(0, 0)
END = Point(40, 30)
WX = WIDTH/ROWS
WY = HEIGHT/COLS
SOLVED = False

grid = []

class Node():
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.x = i *(WX)
        self.y = j *(WY)
        self.g = 0
        self.h = 0
        self.f = 0
        self.start = False
        self.end = False
        self.previous = None
        self.neighbours = []
        self.obstacle = True if random.random() < 0.25 else False
        self.path = False
        self.color = self.getColor()
        self.r = Rectangle(Point(self.x, self.y), Point(self.x + WX-1, self.y + WY-1))

    def getColor(self):
        if self.start:
            return color_rgb(0, 100, 150)
        elif self.end:
            return color_rgb(255, 0, 50)
        if self.path:
            return "green"
        elif self.obstacle:
            return "black"
        else:
            return "white"

    def show(self, win):
        self.r.setFill(self.getColor())
        self.r.setOutline(self.getColor())
        self.r.draw(win)


    def undraw(self):
        self.r.undraw()

    def redraw(self, win):
        self.undraw()
        self.show(win)


    def setColor(self, color):
        self.color = color

    def setG(self, value=None): 
        if value:
            self.g = value
        else:
            self.g = Node.distFrom(grid[int(START.x)][int(START.y)], self)

    def getG(self): return self.g

    def setH(self): 
        self.h = Node.distFrom(self, grid[max(0, int(END.x)-1)][max(0, int(END.y)-1)])

    def getH(self): return self.h

    def setF(self, value):
        self.f = value

    def getF(self): return self.f

    @staticmethod
    def distFrom(a, b):
        return math.sqrt((b.i - a.i)**2 + (b.j - a.j)**2)

    def get_neighbours(self):
        for i in range(max(0, self.i - 1), min(ROWS, self.i + 2)):
            for j in range(max(0, self.j - 1), min(COLS, self.j + 2)):
                if i != self.i or j != self.j:
                    self.neighbours.append(grid[i][j])





def main():
    win = GraphWin("A*", WIDTH, HEIGHT)

    for i in range(ROWS):
        _ = []
        for j in range(COLS):
            n = Node(i, j)
            _.append(n)

        grid.append(_)

    
    grid[int(START.x)][int(START.y)].start = True
    grid[max(0, int(END.x)-1)][max(0, int(END.y)-1)].end = True
    grid[int(START.x)][int(START.y)].obstacle = False
    grid[max(0, int(END.x)-1)][max(0, int(END.y)-1)].obstacle = False

    
    for i in range(ROWS):
        for j in range(COLS):
            grid[i][j].show(win)

    for i in range(ROWS):
        for j in range(COLS):
            grid[i][j].get_neighbours()
            grid[i][j].setG()
            grid[i][j].setH()


    def draw_path(path):
        # print(len(path))
        for p in path:
            p.undraw()
            p.path = True
            p.redraw(win)
            # print(p.i, p.j)
            # p.show(win)

    def construct_path(current):
        path = []
        path.append(current)
        current =  current
        while current.previous:
            path.insert(0, current.previous)
            current = current.previous

        draw_path(path)

    
    openSet = []
    closedSet = []
    openSet.append(grid[0][0])
    
    # print(len(openSet))
    while len(openSet) > 0:
        
        current = openSet[0]
        if current.i == max(0, END.x-1) and current.j == max(0, END.y-1):
            SOLVED = True
            construct_path(current)
            
        
        openSet.remove(current)

        for neighbour in current.neighbours:
            
            tempG = current.getG() + 1

            if tempG < neighbour.getG():
                neighbour.previous = current
                neighbour.setG(value=tempG)
                neighbour.setF(neighbour.getG() + neighbour.getH())

                if neighbour not in openSet and not neighbour.obstacle:
                    openSet.append(neighbour)

        # construct_path(openSet[len(openSet)-1])

    if not SOLVED:
        print("NO SOLUTION!!")

    win.getMouse()
    win.close()




if __name__ == "__main__":
    main()