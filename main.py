import requests
from bs4 import BeautifulSoup
from termcolor import colored
import copy

sudoku = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
]

URL = 'https://nine.websudoku.com/?level=4'

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

code = soup.find("a", {"title":"Copy link for this puzzle"}).contents

table = soup.find(
    "table", {"id": "puzzle_grid"})

for i in range(len(table.contents)):
    for j in range(len(table.contents[i])):
        if ('value' in table.contents[i].contents[j].contents[0].attrs):
            sudoku[i][j] = int(table.contents[i].contents[j].contents[0].attrs.get('value'))
        else:
            continue
#sudoku_backup = sudoku.copy()
sudoku_backup = copy.deepcopy(sudoku)

def findNextCellToFill(sudoku):
    for x in range(9):
        for y in range(9):
            if sudoku[x][y] == 0:
                return x, y
    return -1, -1

def isValid(sudoku, i, j, e):
    rowOk = all([e != sudoku[i][x] for x in range(9)])
    if rowOk:
        columnOk = all([e != sudoku[x][j] for x in range(9)])
        if columnOk:
            secTopX, secTopY = 3*(i//3), 3*(j//3)
            for x in range(secTopX, secTopX+3):
                for y in range(secTopY, secTopY+3):
                    if sudoku[x][y] == e:
                        return False
            return True
    return False


def solveSudoku(sudoku, i=0, j=0):
    i, j = findNextCellToFill(sudoku)
    if i == -1:
        return True

    for e in range(1, 10):
        if isValid(sudoku, i, j, e):
            sudoku[i][j] = e
            if solveSudoku(sudoku, i, j):
                return True
            sudoku[i][j] = 0
    return False


def printsudoku(sudoku,sudoku_backup):
    print("\n\n\n\n\n")
    for i in range(len(sudoku)):
        line = ""
        if i == 3 or i == 6:
            print("---------------------")
        for j in range(len(sudoku[i])):
            if j == 3 or j == 6:
                line += "| "
            if sudoku_backup[i][j]==0:
                line += colored(str(sudoku[i][j]), 'red')+" "
            else:
                line += str(sudoku[i][j])+" "
        print(line)

solveSudoku(sudoku)
printsudoku(sudoku,sudoku_backup)
print(code)
