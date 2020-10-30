from button_class import*
from settings import*
from solver import*
from main import*
import numpy as np
import pygame
import bs4
import requests
import copy
from collections import deque

class App():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('sUdOkU')
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.mouseCoor = None
        self.selectedCell = None
        self.selectedCellCoor = None
        self.lockedCells = []
        self.incorrectCells = []
        self.pencilCells = []
        self.buttons = []
        self.solved = False
        self.visualizeSolve = False
        self.grid = DEFAULTBOARD
        self.deepGrid = copy.deepcopy(self.grid)
        self.difficulty = 1
        self.difficultyRects = []
        self.visualizeSolveRect = ()
        self.undoStack = deque()
        self.redoStack = deque()
        self.startTime = time.time()
        self.elapsedTime = time.time() - self.startTime
        self.action = None
        self.load()

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()

        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                self.running = False
            # mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mouseOnGrid():
                    self.selectedCell = self.getSelectedCell()
                    # print(self.selectedCell)
                    self.selectedCellCoor = self.getCellCoor(self.selectedCell)
                    # print(self.selectedCellCoor)
                else:
                    # button click
                    self.selectedCell = None
                    for button in self.buttons:
                        if button.hovered:
                            button.click()
                    # difficulty click
                    self.updateDifficulty()
                    # visualize solve click
                    self.updateVisualizeSolveRect()
            # keyboard input
            if event.type == pygame.KEYDOWN:
                # '1'-'9' input
                if self.isInt(event.unicode) and int(event.unicode) != 0:
                    numberInput = int(event.unicode)
                    print(numberInput)
                    # if there is a selected cell that is not locked, change its value
                    if self.selectedCell and self.selectedCell not in self.lockedCells:
                        # changing cell value
                        self.grid[self.selectedCell[1]][self.selectedCell[0]] = numberInput
                        # appending change to undo stack
                        self.undoStack.append(copy.deepcopy(self.grid))

                        # if len(self.undoStack) == 0:
                        #     self.undoStack.append(copy.deepcopy(self.grid))
                        # elif self.undoStack[-1] != self.grid:
                        #     self.undoStack.append(copy.deepcopy(self.grid))

                # escape input
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # 'c' (check) input
                if event.key == pygame.K_c:
                    self.check()
                # 'r' (clear) input
                if event.key == pygame.K_r:
                    self.clear()
                # 's' (solve) input
                if event.key == pygame.K_s:
                    self.solve()
                # allow the following inputs if a cell is selected
                if self.selectedCell:
                    # backspace input and '0' input
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_0:
                        self.grid[self.selectedCell[1]][self.selectedCell[0]] = 0
                        self.undoStack.append(copy.deepcopy(self.grid))
                        try:
                            self.incorrectCells.remove(self.selectedCell)
                        except:
                            pass
                    # up input
                    if event.key == pygame.K_UP:
                        if self.selectedCell[1] > 0:
                            self.selectedCell = (self.selectedCell[0], self.selectedCell[1]-1)
                            print(self.selectedCell)
                    # down input
                    if event.key == pygame.K_DOWN:
                        if self.selectedCell[1] < 8:
                            self.selectedCell = (self.selectedCell[0], self.selectedCell[1]+1)
                            print(self.selectedCell)
                    # left input
                    if event.key == pygame.K_LEFT:
                        if self.selectedCell[0] > 0:
                            self.selectedCell = (self.selectedCell[0]-1, self.selectedCell[1])
                            print(self.selectedCell)
                    # right input
                    if event.key == pygame.K_RIGHT:
                        if self.selectedCell[0] < 8:
                            self.selectedCell = (self.selectedCell[0]+1, self.selectedCell[1])
                            print(self.selectedCell)

    def update(self):
        self.mouseCoor = pygame.mouse.get_pos()
        self.updateButtons()
        self.updateTime()

    def draw(self):
        self.window.fill(LIGHTPURPLE)
        self.drawIncorrectCells()
        self.drawSelectedCell()
        self.drawGrid()
        self.drawNumbers()
        self.drawLockedCells()
        self.drawButtons()
        self.drawDifficulty()
        self.drawVisualize()
        self.drawTime()
        self.drawAction()

        # myFont = pygame.font.SysFont(FONT, FONTSIZE)
        # textSurface = myFont.render('Text', False, (0,0,0))
        # self.window.blit(textSurface, (0,0))

        pygame.display.update()

    def load(self):
        self.loadLockedCells()
        self.loadButtons()

# ---------- update() helpers ---------- #

    def getSelectedCell(self):
        cell = self.selectedCell
        x, y = self.mouseCoor
        # mouse is within horizontal grid boundaries
        if x > GRIDCOOR[0] and x < GRIDCOOR[0]+GRIDDIM[0]:
            # mouse is within vertical grid boundaries
            if y > GRIDCOOR[1] and y < GRIDCOOR[1]+GRIDDIM[1]:
                x, y = ((x - GRIDCOOR[0]) // CELLSIZE), ((y - GRIDCOOR[1]) // CELLSIZE)
                # if (x, y) not in self.lockedCells:
                cell = (x, y)
        return cell

    def getCellCoor(self, cell):
        # cell = self.getSelectedCell()
        if cell:
            coor = ((GRIDCOOR[0] + cell[0] * CELLSIZE),
                    (GRIDCOOR[1] + cell[1] * CELLSIZE))
        return coor

    def mouseOnGrid(self):
        x, y = self.mouseCoor
        # if mouse is within horizontal grid boundaries
        if x > GRIDCOOR[0] and x < GRIDCOOR[0]+GRIDDIM[0]:
            # if mouse is within vertical grid boundaries
            if y > GRIDCOOR[1] and y < GRIDCOOR[1]+GRIDDIM[1]:
                return True
        return False

    def updateButtons(self):
        for button in self.buttons:
            button.update(self.mouseCoor)

    def updateDifficulty(self):
        for i, rect in enumerate(self.difficultyRects):
            # mouse is within horizontal boundaries of
            (x, y) = self.mouseCoor
            if x > rect[0][0] and x < rect[0][0] + rect[1][0]:
                if y > rect[0][1] and y < rect[0][1] + rect[1][1]:
                    self.difficulty = i+1

    def updateVisualizeSolveRect(self):
        rect = self.visualizeSolveRect
        (x, y) = self.mouseCoor
        if x > rect[0][0] and x < rect[0][0] + rect[1][0]:
            if y > rect[0][1] and y < rect[0][1] + rect[1][1]:
                self.visualizeSolve = not self.visualizeSolve

    def updateTime(self):
        if self.elapsedTime != self.startTime:
            self.elapsedTime = time.time() - self.startTime

# ---------- draw() helpers ---------- #

    def drawIncorrectCells(self):
        if self.incorrectCells:
            for cell in self.incorrectCells:
                coor = self.getCellCoor(cell)
                pygame.draw.rect(self.window, INCORRECTCELLCOLOR, (coor[0], coor[1], CELLSIZE, CELLSIZE))

    def drawSelectedCell(self):
        if self.selectedCell:
            cell = self.getCellCoor(self.selectedCell)
            if cell:
                pygame.draw.rect(self.window,
                                 SELECTEDCELLCOLOR,
                                 (cell[0], cell[1], CELLSIZE, CELLSIZE))

    def drawGrid(self):
        # drawing outer lines
        pygame.draw.rect(self.window, BLACK, (GRIDCOOR, GRIDDIM), MAINBORDER)

        # drawing vertical lines
        for i in range(9):
            thickness = INNERBORDER
            if i % 3 == 0:
                thickness = MAINBORDER
            pygame.draw.line(self.window,
                             BLACK,
                             (GRIDCOOR[0] + CELLSIZE * i, GRIDCOOR[1]),
                             (GRIDCOOR[0] + CELLSIZE * i, GRIDCOOR[1] + GRIDDIM[1]),
                             thickness)

        # drawing horizontal lines
        for i in range(9):
            thickness = INNERBORDER
            if i % 3 == 0:
                thickness = MAINBORDER
            pygame.draw.line(self.window,
                             BLACK,
                             (GRIDCOOR[0], GRIDCOOR[1] + CELLSIZE * i),
                             (GRIDCOOR[0] + GRIDDIM[0], GRIDCOOR[1] + CELLSIZE * i),
                             thickness)

    def drawNumbers(self):
        fontObj = pygame.font.SysFont(FONT, FONTSIZE)
        for i, row in enumerate(self.grid):
            for j, num in enumerate(row):
                if num == 0:
                    continue
                textSurface = fontObj.render(str(num), False, WHITE)
                fontWidth = textSurface.get_width()
                fontHeight = textSurface.get_height()
                self.window.blit(textSurface, (GRIDCOOR[0]+CELLSIZE*j+(CELLSIZE-fontWidth)//2,
                                               GRIDCOOR[1]+CELLSIZE*i+(CELLSIZE-fontHeight)//2))

    def drawLockedCells(self):
        fontObj = pygame.font.SysFont(FONT, FONTSIZE)
        for i, row in enumerate(self.deepGrid):
            for j, num in enumerate(row):
                if num == 0:
                    continue
                textSurface = fontObj.render(str(num), False, BLACK)
                fontWidth = textSurface.get_width()
                fontHeight = textSurface.get_height()
                self.window.blit(textSurface, (GRIDCOOR[0]+CELLSIZE*j+(CELLSIZE-fontWidth)//2,
                                               GRIDCOOR[1]+CELLSIZE*i+(CELLSIZE-fontHeight)//2))

    def drawButtons(self):
        for button in self.buttons:
            button.draw(self.window)

    def drawDifficulty(self):
        # drawing the word "difficulty"
        fontObj = pygame.font.SysFont(FONT, FONTSIZE-5)
        textSurface = fontObj.render('Difficulty:', False, BLACK)
        self.window.blit(textSurface,
                         ((GRIDCOOR[0]-BUTTONDIM[0])//2+35, (GRIDCOOR[0]-BUTTONDIM[0])//2+BUTTONDIM[1]+5))
        # drawing difficulty numbers
        for i in range(1,5):
            fontObj = pygame.font.SysFont(FONT, FONTSIZE - 5)
            textSurface = fontObj.render(str(i), False, BLACK)
            coor = ((GRIDCOOR[0]-BUTTONDIM[0])//2-13, (GRIDCOOR[0]-BUTTONDIM[0])//2+BUTTONDIM[1]+30)
            dim = (textSurface.get_height(), textSurface.get_height())
            # drawing boxes
            if self.difficulty == i:
                pygame.draw.rect(self.window,
                                 GREY,
                                 ((coor[0]+30*i, coor[1]), dim))
            else:
                pygame.draw.rect(self.window,
                                 WHITE,
                                 ((coor[0]+30*i, coor[1]), dim))
            if ((coor[0]+30*i, coor[1]), dim) not in self.difficultyRects:
                self.difficultyRects.append(((coor[0]+30*i, coor[1]), dim))
            # drawing numbers
            self.window.blit(textSurface,
                         ((GRIDCOOR[0]-BUTTONDIM[0])//2+30*i-7, (GRIDCOOR[0]-BUTTONDIM[0])//2+BUTTONDIM[1]+30))

    def drawVisualize(self):
        fontObj = pygame.font.SysFont(FONT, FONTSIZE-10)
        textSurface = fontObj.render('visualize', False, BLACK)
        dim = (textSurface.get_width(), textSurface.get_height())
        coor = (((GRIDCOOR[0]-BUTTONDIM[0])//2)+(BUTTONDIM[0]-dim[0])//2, GRIDCOOR[1]+CELLSIZE//2+(CELLSIZE*2)*2+CELLSIZE)

        if self.visualizeSolve:
            pygame.draw.rect(self.window, GREY, (coor, dim))
        else:
            pygame.draw.rect(self.window, WHITE, (coor, dim))
        self.window.blit(textSurface,coor)

        if len(self.visualizeSolveRect) == 0:
            self.visualizeSolveRect = ((coor, dim))

    def drawTime(self):
        fontObj = pygame.font.SysFont(FONT, FONTSIZE)
        textSurface = fontObj.render('Time: {}'.format(str(int(self.elapsedTime))), False, BLACK)
        self.window.blit(textSurface, (0,HEIGHT-textSurface.get_height()-20))

    def drawAction(self):
        if self.action:
            fontObj = pygame.font.SysFont(FONT, FONTSIZE)
            textSurface = fontObj.render(self.action, False, BLACK)

            self.window.blit(textSurface, (WIDTH - textSurface.get_width()-10, HEIGHT - textSurface.get_height()))

    # ---------- load() helpers ---------- #

    def loadLockedCells(self):
        for y, row in enumerate(self.grid):
            for x, num in enumerate(row):
                if num:
                    self.lockedCells.append((x, y))

    def loadButtons(self):
        # new game
        button = Button((GRIDCOOR[0]-BUTTONDIM[0])//2, (GRIDCOOR[0]-BUTTONDIM[0])//2,
                        BUTTONDIM[0]+50, BUTTONDIM[1],
                        color=GREY,
                        text='New Game', function=self.newGame)
        self.buttons.append(button)

        # check
        button = Button((GRIDCOOR[0]-BUTTONDIM[0])//2, GRIDCOOR[1]+CELLSIZE//2,
                        BUTTONDIM[0], BUTTONDIM[1],
                        text='Check', function=self.check)
        self.buttons.append(button)

        # clear
        button = Button((GRIDCOOR[0]-BUTTONDIM[0]) // 2, GRIDCOOR[1] + CELLSIZE // 2 + CELLSIZE * 2,
                        BUTTONDIM[0], BUTTONDIM[1],
                        color=LIGHTRED,
                        text='Clear', function=self.clear)
        self.buttons.append(button)

        # solve
        button = Button((GRIDCOOR[0]-BUTTONDIM[0])//2, GRIDCOOR[1]+CELLSIZE//2+(CELLSIZE*2)*2,
                        BUTTONDIM[0], BUTTONDIM[1],
                        color=LIGHTGREEN,
                        text='Solve', function=self.solve)
        self.buttons.append(button)

        # undo
        button = Button((GRIDCOOR[0]-BUTTONDIM[0])//2, GRIDCOOR[1]+CELLSIZE//2+(CELLSIZE*2)*3,
                        BUTTONDIM[0]//2-1, BUTTONDIM[1],
                        color=GREY,
                        text='<-', function=self.undo)
        self.buttons.append(button)

        # redo
        button = Button((GRIDCOOR[0]-BUTTONDIM[0])//2+BUTTONDIM[0]//2, GRIDCOOR[1]+CELLSIZE//2+(CELLSIZE*2)*3,
                        BUTTONDIM[0]//2, BUTTONDIM[1],
                        color=GREY,
                        text='->', function=self.redo)
        self.buttons.append(button)

        # reset time
        button = Button(0, HEIGHT-25,
                        CELLSIZE,
                        CELLSIZE//2,
                        color=GREY,
                        text='reset', fontSize=18, function=self.resetTime)
        self.buttons.append(button)

# ---------- check() and check() helpers ---------- #

    def check(self):
        self.incorrectCells = []
        self.checkRows()
        self.checkColumns()
        self.checkSquares()
        if 0 not in np.array(self.grid).flatten() and len(self.incorrectCells) == 0:
            self.solved = True
        else:
            self.solved = False
        self.action = '{} incorrect cell(s).'.format(len(self.incorrectCells))
        if self.solved:
            self.action = 'congratulations! you solved the board in {} seconds!'.format(str(int(self.elapsedTime)))
        self.selectedCell = None
        # print(self.incorrectCells)
        print('undo: {}'.format(self.undoStack))
        print('   {} elements'.format(len(self.undoStack)))
        print('redo: {}'.format(self.redoStack))
        print('   {} elements'.format(len(self.redoStack)))

    def checkRows(self):
        possibles = [[1,2,3,4,5,6,7,8,9] for i in range(9)]

        # loop through locked cells first to remove possibilities
        for y, row in enumerate(self.deepGrid):
            for x, num in enumerate(row):
                if num in possibles[y]:
                    possibles[y].remove(num)

        # loop through remaining cells to remove possibilities
        for y, row in enumerate(self.grid):
            for x, num in enumerate(row):
                if (x, y) not in self.lockedCells and num != 0:
                    if num in possibles[y]:
                        possibles[y].remove(num)
                    else:
                        if (x, y) not in self.incorrectCells:
                            self.incorrectCells.append((x, y))

    def checkColumns(self):
        possibles = [[1,2,3,4,5,6,7,8,9] for i in range(9)]

        # loop through locked cells first to remove possibilities
        for x in range(9):
            for y in range(9):
                num = self.deepGrid[y][x]
                # num = self.deepGrid[y][x]
                if num in possibles[x]:
                    possibles[x].remove(num)

        # loop through remaining cells to remove possibilities
        for x in range(9):
            for y in range(9):
                num = self.grid[y][x]
                if (x, y) not in self.lockedCells and num != 0:
                    if num in possibles[x]:
                        possibles[x].remove(num)
                    else:
                        if (x, y) not in self.incorrectCells:
                            self.incorrectCells.append((x, y))

    def checkSquares(self):
        possibles = [[1,2,3,4,5,6,7,8,9] for i in range(9)]

        # loop through locked cells first to remove possibles
        for y1 in range(3):
            for x1 in range(3):
                i = x1+y1*3
                for y2 in range(3):
                    for x2 in range(3):
                        (x, y) = (x1*3+x2, y1*3+y2)
                        num = self.deepGrid[y][x]
                        if num in possibles[i]:
                            possibles[i].remove(num)

        # loop through remaining cells to remove possibles
        for y1 in range(3):
            for x1 in range(3):
                i = x1+y1*3
                for y2 in range(3):
                    for x2 in range(3):
                        (x, y) = (x1*3+x2, y1*3+y2)
                        num = self.grid[y][x]
                        if (x, y) not in self.lockedCells and num != 0:
                            if num in possibles[i]:
                                possibles[i].remove(num)
                            else:
                                if (x, y) not in self.incorrectCells:
                                    self.incorrectCells.append((x, y))

# ---------- other functions ---------- #

    def getGrid(self, difficulty=1):
        grid = [[0 for i in range(9)] for i in range(9)]

        # using response object to get table, then rows, then digits
        resp = requests.get('https://nine.websudoku.com/?level={}'.format(difficulty))
        soup = bs4.BeautifulSoup(resp.text, features='html.parser')
        table = soup.find('table', attrs={'id': 'puzzle_grid'})
        rows = table.find_all('tr')

        # creating grid
        for y, row in enumerate(rows):
            for x, digitObject in enumerate(row.find_all('td')):
                digit = digitObject.find('input').get('value')
                if digit == None:
                    digit = '0'
                grid[y][x] = int(digit)

        return grid

    def newGame(self):
        self.selectedCell = None
        self.lockedCells = []
        self.incorrectCells = []
        self.solved = False
        self.grid = self.getGrid(self.difficulty)
        self.deepGrid = copy.deepcopy(self.grid)
        self.undoStack.clear()
        self.redoStack.clear()
        self.startTime = time.time()
        self.elapsedTime = time.time() - self.startTime
        self.loadLockedCells()
        self.action = 'new game.'

    def clear(self):
        self.grid = copy.deepcopy(self.deepGrid)
        self.incorrectCells = []
        self.selectedCell = None
        self.undoStack.append(self.grid)
        self.action = 'board cleared.'

    def solve(self):
        self.clear()
        self.action = 'solving...'
        solve(self.grid, app=self, visualize=self.visualizeSolve)
        self.selectedCell = None
        self.action = 'board solved.'

    def undo(self):
        if len(self.undoStack) != 0:
            item = self.undoStack.pop()
            self.grid = item
            self.redoStack.append(item)
            self.action = 'undo.'
        else:
            self.grid = copy.deepcopy(self.deepGrid)

    def redo(self):
        if len(self.redoStack) != 0:
            item = self.redoStack.pop()
            self.grid = item
            self.undoStack.append(item)
            self.action = 'redo.'

    def resetTime(self):
        self.startTime = time.time()
        self.elapsedTime = time.time() - self.startTime

    def isInt(self, unicode):
        try:
            int(unicode)
            return True
        except:
            return False
