import numpy
import pygame
import sys
import math

PLAYER_ROUNDS = 1
ALPHAB_ROUNDS = 2

COLOR_BLUE = (0, 0, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

SQUARESIZE = 100

match = True
turn = 0

pygame.init()


def newBoard():
    return numpy.zeros((6, 7))


def setLocation(row, col, rounds):
    board[row][col] = rounds


def hasVacant(col):
    return board[5][col] == 0


def nextRow(col):
    for r in range(6):
        if board[r][col] == 0:
            return r


def showBoard():
    for column in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            pygame.draw.rect(screen, COLOR_BLUE, (column*SQUARESIZE,
                             row*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, COLOR_BLACK, (int(
                column*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), getRadius())

    for column in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if board[row][column] == 1:
                pygame.draw.circle(screen, COLOR_RED, (int(
                    column * SQUARESIZE + SQUARESIZE / 2), ((ROW_COUNT+1) * SQUARESIZE) - int(row * SQUARESIZE + SQUARESIZE / 2)), getRadius())
            elif board[row][column] == 2:
                pygame.draw.circle(screen, COLOR_YELLOW, (int(
                    column * SQUARESIZE + SQUARESIZE / 2), (COLUMN_COUNT * SQUARESIZE) - int(row * SQUARESIZE + SQUARESIZE / 2)), getRadius())

    pygame.display.update()


def setPlay(column, rounds):
    if (not hasVacant(column)):
        return False

    setLocation(nextRow(column), column, rounds)
    return True


def newRound(column, rounds):
    done = False
    while not done:
        if (setPlay(int(column), rounds)):
            done = True


def getSize():
    return (
        COLUMN_COUNT * SQUARESIZE,
        (ROW_COUNT+1) * SQUARESIZE
    )


def getRadius():
    return int(SQUARESIZE/2 - 5)


def mouseHover(event):
    pygame.draw.rect(screen, COLOR_BLACK,
                     pygame.Rect(0, 0, (COLUMN_COUNT * SQUARESIZE), SQUARESIZE))

    pygame.draw.circle(screen, COLOR_RED,
                       (event.pos[0], int(SQUARESIZE/2)), getRadius())

    pygame.display.update()


size = getSize()
board = newBoard()

screen = pygame.display.set_mode(size)

showBoard()

while match:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            sys.exit()

        if (event.type == pygame.MOUSEMOTION):
            mouseHover(event)

        if (event.type == pygame.MOUSEBUTTONDOWN):
            print('click:' + str(math.floor((event.pos[0] / SQUARESIZE))))
            newRound(math.floor((event.pos[0] / SQUARESIZE)), PLAYER_ROUNDS)

    showBoard()
