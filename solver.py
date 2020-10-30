import numpy as np
import time
from app_class import*
from main import*


board = (
    [1,0,0, 0,0,0, 0,0,0],
    [2,0,0, 0,0,0, 0,0,0],
    [3,0,0, 0,0,0, 0,0,0],
    [4,0,0, 0,0,0, 0,0,0],
    [5,0,0, 0,0,0, 0,0,0],
    [6,0,0, 0,0,0, 0,0,0],
    [7,0,0, 0,0,0, 0,0,0],
    [8,0,0, 0,0,0, 0,0,0],
    [9,0,0, 0,0,0, 0,0,0]
)

def print_board(board):
    
    temp = np.array(board).reshape(81)
    condition = ''
    
    if np.all(temp):
        condition = 'solved'
    else:
        condition = 'unsolved'
        
    print('Your %s Sudoku board:' % condition)
    print()
    
    for i in range(len(board)):
        
        # printing horizontal dividor after every third row
        if i % 3 == 0 and i != 0:
            print('-----   -----   -----')
        
        for j in range(len(board)):
            
            # printing vertical dividor after every third column
            if j % 3 == 0 and j != 0:
                print('| ', end='')
            
            # printing every number 
            if j != len(board):
                print(str(board[i][j]) + ' ', end='')
            else:
                print()
        
        print()
            
def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                # row, column
                return (i, j) 
    
    return None
            
def valid(board, num, pos):
    
    # check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
        
    # check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
        
    # check square
    square_x = pos[1] // 3
    square_y = pos[0] // 3
    
    for i in range(len(board) // 3):
        for j in range(len(board[0]) // 3):
            if board[i + square_y * 3][j + square_x * 3] == num and (pos[0] != i and pos[1] != j):
                return False
            
    return True

def solve(board, app=None, visualize=False, sleep=0.015):
    
    # finding unsolved space
    find = find_empty(board)
    
    # if no unsolved space, the board is solved
    if not find:
        return True
    
    # found unsolved space
    else:
        row, col = find
        
    # checking numbers 1-9 in unsolved space
    for i in range(1, 10):

        # if 'i' is valid, input into space
        if valid(board, i, (row, col)):

            ###
            # time.sleep(0.015)
            # app.drawNumbers()
            ###

            board[row][col] = i
            if app and visualize:
                time.sleep(sleep)
                app.draw()
                pygame.display.update()

            # continue solving new board with 'i'. 
            # if unsolvable, reset space to zero
            if not solve(board, app, visualize):
                board[row][col] = 0
            
            # board is solvable
            else:
                return True
            
    # board is unsolvable
    return False

