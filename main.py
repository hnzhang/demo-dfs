# Import Modules
import os
import pygame as pg
import time
import threading

import pglib

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")
board = [
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


history_track = set()
targetRow = 0; targetCol = 8 
currentPos = [0, 0]
found = False

def depthFirstSearch(board, history, row, col):
    global found
    global currentPos
    if board[row][col] != 0 and (row, col) in history:
        return
    #print(f"depthFirstSearch: row {row} col {col}")
    history.add((row, col))
    currentPos[0] = row; currentPos[1] = col
    if row == targetRow and col == targetCol:
        found = True
        return
    time.sleep(2)
    for (deltaRow, deltaCol) in ( (1, 0), (-1, 0), (0, 1), (0, -1)):
        if found:
            break
        newCol = col + deltaCol; newRow = row + deltaRow
        # print(f"newRow {newRow} newCol {newCol}")
        if newRow >= 0 and newRow < len(board) and newCol >= 0 and newCol < len(board[newRow]):
            # print(f"board[{newRow}][{newCol}]: {board[newRow][newCol]}")
            if  board[newRow][newCol] == 0 and (newRow, newCol) not in history:
                depthFirstSearch(board, history, newRow, newCol)


def main():
    global currentPos
    global history_track
    pg.init()
    
    frame_per_second = 60
    clock = pg.time.Clock()

    screen = pg.display.set_mode((640, 480))
    screen_color = (255, 255, 255)
    pg.display.set_caption("Depth search demo...")

    game_over = False
    height = 20; width = 20
    startX = 20; startY = 20
    colors  = [ (255, 255, 255), (255, 0, 0), (0, 255, 0)]
    depthFirstSearch_thread = threading.Thread(target = depthFirstSearch, args = (board, history_track, 6, 0))
    depthFirstSearch_thread.start()
    while not game_over:
        player_input = ""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over = True
            elif event.type == pg.KEYUP:
                if event.unicode == 'Q' or event.unicode == 'q': 
                    game_over = True
                elif event.unicode: # expect to have A, S, D, W, Q
                    player_input = event.unicode

        screen.fill(screen_color)
        for i in range(len(board)):
            for j in range(len(board[i])):
                color = colors[board[i][j]]
                if board[i][j] == 0 and (i, j) in history_track: color = colors[2]
                pglib.draw_place(screen, startX + j * width , startY + i * height, width, height, color)
        pglib.draw_place(screen, (currentPos[1] + 1) * width, (currentPos[0] + 1) * height, width, height, (0, 0, 0))

        pg.display.update()
        clock.tick(frame_per_second)

    pg.quit()

if __name__ == "__main__":
    main()
    #depthFirstSearch(board, set(), 6, 0)
