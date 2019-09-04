#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import permutations

# Cell Definition
#   - cellType: monster/mirror
#   - value for monster: 0 for none, 1 for Ghost, 2 for Vampire, 3 for Zombie
#   - value for mirror: 0 for \, 1 for /
#   - fixed: indicating whether this cell is known for sure. Should always be `True` for mirrors


class Cell:
    def __init__(self, cellType, value, fixed,x,y):
        self.cellType = cellType
        self.value = value
        self.fixed = fixed
        self.x=x
        self.y=y
    def FindPath(self):
        direction=['N','E','S','W']
        is_through_mirror=False
        sol=[]
        # beginning from north, move alongside the path to find four point at border (applies on cell which is default not to be a mirror)
        for start_d in direction:
            current_d=start_d
            i=self.x
            j=self.y
            while(i!=-1 and j!=-1 and i!=PUZZLESIZE and j!=PUZZLESIZE):
                i,j=move(i,j,current_d)
                if(i!=-1 and j!=-1 and i!=PUZZLESIZE and j!=PUZZLESIZE):
                    if(cells[i][j].cellType=="mirror"):
                        current_d=turn(current_d,cells[i][j].value)
                        is_through_mirror=True
            sol.append([i,j,is_through_mirror])
            is_through_mirror=False
        return sol

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


# PUZZLESIZE = 4


# No random generation process is taken. Please refer to https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/undead.html to initiate the puzzle for current stage.
def initPuzzle():
    amount = {
        "ghost": 2,
        "vampire": 2,
        "zombie": 8
    }

    # Let's start with a 4x4 puzzle
    cells = []
    cells1 = []
    cells2 = []
    cells3 = []
    cells4 = []

    cells1.append(Cell('monster', 2, False, 0, 0))
    cells1.append(Cell('monster', 3, False, 0, 1))
    cells1.append(Cell('monster', 3, False, 0, 2))
    cells1.append(Cell('monster', 3, False, 0, 3))

    cells2.append(Cell('monster', 3, False, 1, 0))
    cells2.append(Cell('mirror', 0, False, 1, 1))
    cells2.append(Cell('monster', 3, False, 1, 2))
    cells2.append(Cell('monster', 3, False, 1, 3))

    cells3.append(Cell('monster', 1, False, 2, 0))
    cells3.append(Cell('monster', 1, False, 2, 1))
    cells3.append(Cell('mirror', 1, False, 2, 2))
    cells3.append(Cell('monster', 3, False, 2, 3))

    cells4.append(Cell('monster', 2, False, 3, 0))
    cells4.append(Cell('mirror', 0, False, 3, 1))
    cells4.append(Cell('monster', 3, False, 3, 2))
    cells4.append(Cell('mirror', 0, False, 3, 3))

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

    borders4.append(4)
    borders4.append(3)
    borders4.append(2)
    borders4.append(1)

    borders1.append(3)
    borders1.append(3)
    borders1.append(4)
    borders1.append(3)

    borders2.append(4)
    borders2.append(3)
    borders2.append(2)
    borders2.append(3)

    borders3.append(3)
    borders3.append(0)
    borders3.append(2)
    borders3.append(3)

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

def process_sol_to_points(sol):#transfer the "sol" we get (like [-1,2,TRUE] to [0,2,TRUE]) so that it represent border[0][2]
    points=[]
    for i in range(4):
        a=sol[i]
        if a[0] == -1:
            points.append([0,a[1],a[2]])
        elif a[0] == PUZZLESIZE:
            points.append([2,a[1],a[2]])
        elif a[1] == -1:
            points.append([3,a[0],a[2]])
        elif a[1] == PUZZLESIZE:
            points.append([1,a[0],a[2]])
    return points

def process_border(cells,i,j,value):
    sol=cells[i][j].FindPath()
    points=process_sol_to_points(sol)
    for m in range(4):#iterater the four points
        if value == 1: #it's ghost
            if points[m][2] == True: #See if this point is through the mirror
                borders[points[m][0]][points[m][1]]-=1
        if value == 2: #it's vampire
            if points[m][2] == False:
                borders[points[m][0]][points[m][1]]-=1
        if value == 3: # it's zombie
            borders[points[m][0]][points[m][1]]-=1

# TODO: Implementation required
def isValidPuzzle(cells, borders):
    for i in range(PUZZLESIZE):
        for j in range(PUZZLESIZE):
            if cells[i][j].cellType == 'mirror':
                continue
            else:
                if cells[i][j].value == 0:
                    continue
                else: process_border(cells,i,j,cells[i][j].value)
    for sub_borders in borders:
        for a in sub_borders:
            if a<0:
                return False
    return True

# Deprecated code. Using itertools instead for now
# Generate all permutations of the given list
# def getPermutation(monsterList):
#     l = []
#     print(monsterList)
#     if len(monsterList) <= 1:
#         return [monsterList]
#     for i in range(len(monsterList)):
#         c = monsterList[i]
#         remList = monsterList[:i] + monsterList[i+1:]
#         for p in getPermutation(remList):
#             print(p)
#             subList = [c] + p
#             if subList not in l:
#                 l.append(subList)
#     return l


# Get a plain list of monsters TBD
def getMonsterList(amount):
    monsterList = []
    for _ in range(amount["ghost"]):
        monsterList.append(1)

    for _ in range(amount["vampire"]):
        monsterList.append(2)

    for _ in range(amount["zombie"]):
        monsterList.append(3)

    return monsterList


def findAllSolutions(cells, borders, amount):
    totalSol = 0

    monsterList = getMonsterList(amount)
    # monsterPerm = getPermutation(monsterList)
    monsterPerm = permutations(
        monsterList, len(monsterList))
    # for trial in set(monsterPerm):
    #     index = 0
    #     for lenIndex in range(PUZZLESIZE):
    #         for widIndex in range(PUZZLESIZE):
    #             if cells[lenIndex][widIndex].cellType == "monster":
    #                 cells[lenIndex][widIndex].value = trial[index]
    #                 index += 1
    #     if isValidPuzzle(cells, borders) == True:
    #         totalSol += 1
    #         if totalSol <= 3:
    #             print("Solution " + str(totalSol) + ":")
    #             printPuzzle(cells, borders, amount)
    if isValidPuzzle(cells, borders) == True:
        totalSol += 1

    return totalSol


if __name__ == "__main__":
    cells, borders, amount = initPuzzle()
    global PUZZLESIZE
    PUZZLESIZE=len(cells)
    printPuzzle(cells, borders, amount)
    print("Start finding solutions...")
    print("It might take a few minutes, please be patient...")
    solNum = findAllSolutions(cells, borders, amount)
    print("There are " + str(solNum) + " solutions in all")