import math
import random
from graphics.graphics import *

## BRUHH
WIN = None
WIDTH = 600
HEIGHT = 600
ROWS = 10
COLS = 10
START = Point(0, 0)
END = Point(1, 1)
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
        self.obstacle = False # True if random.random() < 0.25 else False
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

    def show(self, WIN):
        self.r.setFill(self.getColor())
        # self.r.setOutline(self.getColor())
        self.r.draw(WIN)


    def undraw(self):
        self.r.undraw()

    def redraw(self, WIN):
        self.undraw()
        self.show(WIN)


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

    def contains(self, p):
        return (((p.x > self.x) and (p.x < self.x + WX -1)) and ((p.y > self.y) and(p.y < self.y + WY -1)))

    def get_neighbours(self):
        for i in range(max(0, self.i - 1), min(ROWS, self.i + 2)):
            for j in range(max(0, self.j - 1), min(COLS, self.j + 2)):
                if i != self.i or j != self.j:
                    self.neighbours.append(grid[i][j])


def draw_path(path):
    # print(len(path))
    for p in path:
        p.undraw()
        p.path = True
        p.redraw(WIN)
        # print(p.i, p.j)
        # p.show(WIN)

def construct_path(current):
    path = []
    path.append(current)
    current =  current
    while current.previous:
        path.insert(0, current.previous)
        current = current.previous

    draw_path(path)

def getLowest(openSet):
    lowest = float("inf")
    lowestNode = None
    for i in range(len(openSet)):
        if openSet[i].getF() < lowest:
            lowestNode = openSet[i]
        
    return lowestNode

def Astar(grid):
    print("A starring...")
    openSet = []
    closedSet = []
    openSet.append(grid[int(START.x)][int(START.y)])
    
    # print(len(openSet))
    grid[int(START.x)][int(START.y)].setF(grid[int(START.x)][int(START.y)].getG()+grid[int(START.x)][int(START.y)].getH())  
    while len(openSet) > 0:
        global SOLVED
        
        current = getLowest(openSet)
        if current.i == max(0, END.x-1) and current.j == max(0, END.y-1):
            SOLVED = True
            print("**A starred**")
            
            return construct_path(current)
            
        
        openSet.remove(current)
        closedSet.append(current)
        for neighbour in current.neighbours:
            if neighbour in closedSet:
                continue
            
            tempG = current.getG() + 1 #Node.distFrom(current, neighbour)

            if tempG < neighbour.getG():
                neighbour.previous = current
                neighbour.setG(value=tempG)
                neighbour.setF(neighbour.getG() + neighbour.getH())

                if neighbour not in openSet and not neighbour.obstacle:
                    openSet.append(neighbour)
            # if neighbour in closedSet and tempG >= neighbour.getG():
            #         continue
            # if neighbour not in closedSet or tempG < neighbour.getG():
            #     neighbour.previous = current
            #     neighbour.setG(value=tempG)
            #     neighbour.setF(neighbour.getG() + neighbour.getH())
            #     if neighbour not in openSet:
            #         openSet.append(neighbour)

        # construct_path(openSet[len(openSet)-1])


def main():
    global SOLVED
    global WIN
    global grid
    WIN = GraphWin("A*", WIDTH, HEIGHT)
    WIN.bind()
    for i in range(ROWS):
        _ = []
        for j in range(COLS):
            n = Node(i, j)
            _.append(n)

        grid.append(_)

    
    for i in range(ROWS):
        for j in range(COLS):
            grid[i][j].show(WIN)

        
    while True:
        k = WIN.getKey()
        if k.lower() == "s":
            m = WIN.getMouse()
            for i in range(ROWS):
                for j in range(COLS):
                    if grid[i][j].contains(m):
                        START.x , START.y = i, j
                        grid[i][j].start = True
                        grid[i][j].redraw(WIN)

        if k.lower() == "e":
            m = WIN.getMouse()
            for i in range(ROWS):
                for j in range(COLS):
                    if grid[i][j].contains(m):
                        END.x, END.y = i+1, j+1
                        grid[i][j].end = True
                        grid[i][j].redraw(WIN)

        if k.lower() == "w":
            # obs = []
            def add_to_obs(event):
                m = Point(event.x_root, event.y_root)
                print(m)
                for i in range(ROWS):
                    for j in range(COLS):
                        if grid[i][j].contains(m):
                            if not grid[i][j].obstacle:
                                grid[i][j].obstacle = True
                                grid[i][j].redraw(WIN)
                # obs.append([event.x_root, event.y_root])

            WIN.bind("<B1-Motion>", add_to_obs)
            
                

        if k.lower() == "d":
            m = WIN.getMouse()
            for i in range(ROWS):
                for j in range(COLS):
                    if grid[i][j].contains(m):
                        grid[i][j].obstacle = False
                        grid[i][j].redraw(WIN)


        if k.lower() == "a":
            for i in range(ROWS):
                for j in range(COLS):
                    grid[i][j].get_neighbours()
                    grid[i][j].setG()
                    grid[i][j].setH()
            Astar(grid)
            # construct_path()
            if not SOLVED:
                print("NO SOLUTION!!")

        if k.lower() == "x":
            try:
                WIN.close()
            except GraphicsError:
                break



    # Astar()
    


    # WIN.getMouse()
    # WIN.close()




if __name__ == "__main__":
    main()