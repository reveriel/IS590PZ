#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Cell Definition
#   - cellType: monster/mirror
#   - value for monster: 0 for none, 1 for Ghost, 2 for Vampire, 3 for Zombie
#   - value for mirror: 0 for \, 1 for /
#   - fixed: indicating whether this cell is known for sure. Should always be `True` for mirrors
#   - x: the x index of a cell, start from 0
#   - y: the y index of a cell, start from 0
#   - FindPath(): starting from a cell, find the corresponding 4 pairs of [i,j] which indicate a point in the border and return whether its through the mirror

class Cell:
    def __init__(self, cellType, value, fixed,x,y):
        self.cellType = cellType
        self.value = value
        self.fixed = fixed
        self.x=x
        self.y=y
    def FindPath(self):
        i=x
        j=y
        direction=['N','E','S','W']
        is_through_mirror=False
        sol=[]
        # beginning from north, move alongside the path to find four point at border (applies on cell which is default not to be a mirror)
        for start_d in direction:
            current_d=start_d
            while(i!=-1 & j!=-1 & x!=PUZZLESIZE & y!=PUZZLESIZE):
                move(i,j,current_d)
                if(cells[i][j].cellType=="mirror"):
                    current_d=turn(current_d,cells[i][j].value)
                    is_through_mirror=True
            sol.append([i,j,is_through_mirror])
            is_through_mirror=False

def move(x,y,dire):
    x0=x
    y0=y
    if dire == 'N':
        x0-=1
    if dire == 'E':
        y0+=1
    if dire == 'S':
        x0+=1
    if dire == 'W':
        y0-=1
    return x0,y0

def turn(current_d,mirror_d):
    if(current_d == 'N'):
        if(mirror_d == 0):
             return 'W'
        else: return 'E'
    if(current_d == 'E'):
        if(mirror_d == 0):
             return 'S'
        else: return 'N'
    if(current_d == 'S'):
        if(mirror_d == 0):
             return 'E'
        else: return 'W'
    if(current_d == 'W'):
        if(mirror_d == 0):
             return 'N'
        else: return 'S'

# Define switch for monster & mirror for convenience
def monster(i):
    switcher = {
        0: '*',
        1: 'G',
        2: 'V',
        3: 'Z'
    }
    return switcher.get(i, "Invalid monster type!")


def mirror(i):
    switcher = {
        0: '\\',
        1: '/'
    }
    return switcher.get(i, "Invalid mirror type!")


def initPuzzleSize(n):
    global PUZZLESIZE
    PUZZLESIZE=n


# No random generation process is taken. Please refer to https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/undead.html to initiate the puzzle for current stage.
def initPuzzle(PUZZLESIZE):
    amount = {
        "ghost": 0,
        "vampire": 0,
        "zombie": 0
    }

    # Let's start with a 4x4 puzzle
    cells = []
    cells1 = []
    cells2 = []
    cells3 = []
    cells4 = []

    cells1.append(Cell('monster', 0, False))
    cells1.append(Cell('monster', 0, False))
    cells1.append(Cell('monster', 0, False))
    cells1.append(Cell('monster', 0, False))

    cells2.append(Cell('monster', 0, False))
    cells2.append(Cell('monster', 0, False))
    cells2.append(Cell('monster', 0, False))
    cells2.append(Cell('monster', 0, False))

    cells3.append(Cell('monster', 0, False))
    cells3.append(Cell('monster', 0, False))
    cells3.append(Cell('monster', 0, False))
    cells3.append(Cell('monster', 0, False))

    cells4.append(Cell('monster', 0, False))
    cells4.append(Cell('monster', 0, False))
    cells4.append(Cell('monster', 0, False))
    cells4.append(Cell('monster', 0, False))

    cells.append(cells1)
    cells.append(cells2)
    cells.append(cells3)
    cells.append(cells4)

    # For borders, the first dimension of the array indicates which border it is taking care of.
    # To be specific, 0 for left border, 1 for top border, 2 for right border and 3 for bottom border.
    # Then borders[0][0] indicates the first row of left border, borders[0][1] indicates the second row of left border, borders[1][0] indicates the first column of the top border and so on.
    borders = []
    borders1 = []
    borders2 = []
    borders3 = []
    borders4 = []

    borders1.append(4)
    borders1.append(3)
    borders1.append(2)
    borders1.append(1)

    borders2.append(3)
    borders2.append(3)
    borders2.append(4)
    borders2.append(3)

    borders3.append(4)
    borders3.append(3)
    borders3.append(2)
    borders3.append(3)

    borders4.append(3)
    borders4.append(0)
    borders4.append(2)
    borders4.append(3)

    borders.append(borders1)
    borders.append(borders2)
    borders.append(borders3)
    borders.append(borders4)

    return cells, borders, amount


# Print the puzzle out based on current map
def printPuzzle(cells, borders, amount):
    print("Ghost: " + str(amount["ghost"]), end=' ')
    print("Vampire: " + str(amount["vampire"]), end=' ')
    print("Zombie: " + str(amount["zombie"]) + "\n")

    print("    ", end='')
    for i in range(PUZZLESIZE):
        print(str(borders[1][i]) + "  ", end='')
    print('\n')

    for i in range(PUZZLESIZE):
        print(" " + str(borders[0][i]) + " ", end='')
        for j in range(PUZZLESIZE):
            if cells[i][j].cellType == "monster":
                print(" " + monster(cells[i][j].value) + " ", end='')
            else:
                print(" " + mirror(cells[i][j].value) + " ", end='')
        print(" " + str(borders[2][i]) + " ", end='')
        print('\n')

    print("    ", end='')
    for i in range(PUZZLESIZE):
        print(str(borders[3][i]) + "  ", end='')
    print('\n')

def is_valid_puzzle(cells):
    


if __name__ == "__main__":
    cells, borders, amount = initPuzzle(PUZZLESIZE)
    printPuzzle(cells, borders, amount)