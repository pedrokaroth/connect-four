import numpy
import pygame
import sys
import math

PLAYER = 1
ALPHAB = 2

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

FONT = pygame.font.SysFont("Helvetica", 75)


def showText(text, color=COLOR_YELLOW):
    screen.blit(FONT.render(text, 1, color), (40, 10))


def newBoard():
    return numpy.zeros((6, 7))


def setLocation(row, col, piece):
    board[row][col] = piece


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


def setPlay(column, piece):
    if (not hasVacant(column)):
        return False

    setLocation(nextRow(column), column, piece)
    return True


def newRound(column, piece):
    done = False
    while not done:
        if (setPlay(int(column), piece)):
            done = True


def getSize():
    return (
        COLUMN_COUNT * SQUARESIZE,
        (ROW_COUNT+1) * SQUARESIZE
    )


def winning(piece):
    winning = 0
    for column in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT):
            if board[row][column] == piece and board[row][column + 1] == piece and board[row][column + 2] == piece and board[row][column + 3] == piece:
                return True


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
            newRound(math.floor((event.pos[0] / SQUARESIZE)), PLAYER)
            if winning(PLAYER):
                showText('Você ganhou')
                match = False

    showBoard()

    if not match:
        pygame.time.wait(5000)
