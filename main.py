import numpy
import pygame
import sys
import math
import random

PLAYER = 1
IA = 2

COLOR_BLUE = (0, 0, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_COUNT = 4
SQUARESIZE = 100

match = True
turn = 0

pygame.init()

FONT = pygame.font.SysFont("Helvetica", 75)


def showText(text, color=COLOR_YELLOW):
    screen.blit(FONT.render(text, 1, color), (40, 10))


def newBoard():
    return numpy.zeros((6, 7))


def setLocation(board, row, col, piece):
    if row is False:
        return row

    board[row][col] = piece
    return True


def hasLocation(board, col):
    return board[5][col] == 0


def nextRow(board, col):
    for r in range(6):
        if board[r][col] == 0:
            return r

    return False


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


def setPlay(board, column, piece):
    if (not hasLocation(board, column)):
        return False

    return setLocation(board, nextRow(board, column), column, piece)


def evaluateWindow(window):
    score = 0
    if window.count(IA) == 4:
        score += 1000
    if window.count(IA) == 3 and window.count(0) == 1:
        score += 500
    elif window.count(IA) == 2 and window.count(0) == 2:
        score += 100

    if window.count(PLAYER) == 3 and window.count(0) == 1:
        score -= 800
    return score


def scorePosition(board):
    score = 0
    center = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    score += center.count(IA) * 6

    for row in range(ROW_COUNT):
        rows = [int(i) for i in list(board[row, :])]
        for column in range(COLUMN_COUNT - 3):
            window = rows[column: column + WINDOW_COUNT]
            score += evaluateWindow(window)

    for column in range(COLUMN_COUNT):
        columns = [int(i) for i in list(board[:, column])]
        for row in range(ROW_COUNT - 3):
            window = columns[row: row + WINDOW_COUNT]
            score += evaluateWindow(window)

    for row in range(ROW_COUNT - 3):
        for column in range(COLUMN_COUNT - 3):
            window = [board[row + i][column + i] for i in range(WINDOW_COUNT)]
            score += evaluateWindow(window)

    for row in range(ROW_COUNT - 3):
        for column in range(COLUMN_COUNT - 3):
            window = [board[row+3-i][column+i] for i in range(WINDOW_COUNT)]
            score += evaluateWindow(window)
    return score


def getValidLocations():
    locations = []
    for column in range(COLUMN_COUNT):
        if hasLocation(board, column):
            locations.append(column)
    return locations


def bestMove(board):
    locations = getValidLocations()
    bestScore = -100000
    bestColumn = random.choice(locations)
    for column in locations:
        tmpBoard = board.copy()
        setPlay(tmpBoard, column, IA)
        score = scorePosition(tmpBoard)

        if score > bestScore:
            bestScore = score
            bestColumn = column

        print(str(column) + ' ' + str(score))
    return bestColumn


def newRound(board, column, piece):
    if (setPlay(board, int(column), piece) and not winning(board, piece)):
        setPlay(board, bestMove(board), IA)


def getSize():
    return (
        COLUMN_COUNT * SQUARESIZE,
        (ROW_COUNT+1) * SQUARESIZE
    )


def winning(board, piece):
    for column in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT):
            if board[row][column] == piece and board[row][column + 1] == piece and board[row][column + 2] == piece and board[row][column + 3] == piece:
                return True

        for row in range(ROW_COUNT - 3):
            if board[row][column] == piece and board[row + 1][column + 1] == piece and board[row + 2][column + 2] == piece and board[row + 3][column + 3] == piece:
                return True

        for row in range(3, ROW_COUNT):
            if board[row][column] == piece and board[row - 1][column + 1] == piece and board[row - 2][column + 2] == piece and board[row - 3][column + 3] == piece:
                return True

    for column in range(COLUMN_COUNT):
        for row in range(ROW_COUNT-3):
            if board[row][column] == piece and board[row + 1][column] == piece and board[row + 2][column] == piece and board[row + 3][column] == piece:
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
            newRound(board, math.floor((event.pos[0] / SQUARESIZE)), PLAYER)
            if winning(board, PLAYER):
                showText('Você Ganhou')
                match = False
            elif winning(board, IA):
                showText('Você Perdeu')
                match = False

    showBoard()

    if not match:
        pygame.time.wait(5000)
